#!/usr/bin/env python3
"""
precompact_save_state.py - calab-claude-plugin 컴팩트 전 상태 저장 훅 (v4)

원더 무브 연구소 Claude Plug-in의 PreCompact 훅.
Claude Code가 컨텍스트 압축을 수행하기 전 현재 워크플로우 상태를 저장합니다.

v4 변경사항:
- FIFO 배열 체크포인트 (최대 5개)
- 각 체크포인트에 슬롯 번호와 요약 포함
- v3 형식에서 자동 마이그레이션

훅 입력 (stdin JSON):
- hook_event_name: "PreCompact"
- session_id: string
- transcript_path: string (대화 JSONL 파일 경로)
- trigger: "manual" | "auto"
- permission_mode: string

종료 코드:
- 0: 성공 (체크포인트 저장 또는 정상 스킵)
- 1 또는 2로 종료하지 않음 (압축 차단 금지)

설계 철학:
- 컨텍스트 압축 차단 금지 (항상 exit 0)
- 의존성 없으면 정상 실패
- 모든 작업 로깅 (디버깅용)
- JSON 쓰기 전 검증으로 손상 방지

원본: claude-monitoring-main
적용: calab-claude-plugin v2.3.0+
"""

import json
import sys
import os
import re
import subprocess
from datetime import datetime, timezone
from glob import glob
from pathlib import Path

# hook_utils에서 유틸리티 임포트
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hook_utils import (
    setup_hook_config,
    log,
    json_get,
    validate_json,
    add_checkpoint,
    CHECKPOINTS_FILE,
)


def find_active_plan(project_root: str) -> tuple:
    """
    가장 최근에 수정된 활성 플랜 파일 찾기
    Returns: (plan_path, plan_name) or (None, None)
    """
    plans_dir = os.path.join(project_root, ".claude", "plans")

    if not os.path.isdir(plans_dir):
        return None, None

    active_plan = None
    active_plan_name = None
    latest_mtime = 0

    for plan_file in glob(os.path.join(plans_dir, "*.md")):
        filename = os.path.basename(plan_file)

        # DESIGN, TASKS 파일 제외
        if filename.endswith("-DESIGN.md") or "-TASKS" in filename:
            continue

        mtime = os.path.getmtime(plan_file)
        if mtime > latest_mtime:
            latest_mtime = mtime
            active_plan = plan_file
            active_plan_name = filename.replace(".md", "")

    return active_plan, active_plan_name


def find_related_docs(project_root: str, plan_name: str) -> tuple:
    """
    관련 DESIGN, TASKS 파일 찾기
    Returns: (design_path, tasks_path)
    """
    plans_dir = os.path.join(project_root, ".claude", "plans")

    design_path = None
    tasks_path = None

    # DESIGN 파일
    design_file = os.path.join(plans_dir, f"{plan_name}-DESIGN.md")
    if os.path.isfile(design_file):
        design_path = f".claude/plans/{plan_name}-DESIGN.md"

    # TASKS 파일 (첫 번째 매칭)
    for tasks_file in glob(os.path.join(plans_dir, f"{plan_name}-TASKS*.md")):
        tasks_path = f".claude/plans/{os.path.basename(tasks_file)}"
        break

    return design_path, tasks_path


def parse_agent_execution_log(plan_file: str) -> tuple:
    """
    플랜 파일에서 Agent Execution Log 파싱
    Returns: (last_agent, last_agent_id, status)
    """
    if not os.path.isfile(plan_file):
        return None, None, "in_progress"

    last_agent = None
    last_agent_id = None
    status = "in_progress"
    in_agent_log = False

    try:
        with open(plan_file, "r", encoding="utf-8") as f:
            for line in f:
                # Agent Execution Log 섹션 감지
                if "## Agent Execution Log" in line or "Agent Execution Log" in line:
                    in_agent_log = True
                    continue

                # 다음 섹션 시작 시 종료
                if in_agent_log and line.startswith("## "):
                    break

                if not in_agent_log:
                    continue

                # 테이블 행 파싱 (두 가지 형식 지원)
                # Format 1: | Agent | agentId | Status | Timestamp |
                # Format 2: | Step | Agent | agentId | Status | Timestamp |

                # Format 2 (Step 포함)
                match = re.match(
                    r'\|\s*[\d.]+\s*\|\s*([a-zA-Z0-9_-]+)\s*\|\s*([a-zA-Z0-9_-]*)\s*\|.*?(completed|pending|in_progress|running)',
                    line
                )
                if match:
                    agent_name = match.group(1)
                    agent_id = match.group(2)
                    agent_status = match.group(3)
                else:
                    # Format 1 (Step 없음)
                    match = re.match(
                        r'\|\s*([a-zA-Z0-9_-]+)\s*\|\s*([a-zA-Z0-9_-]*)\s*\|\s*(pending|in_progress|completed|running)\s*\|',
                        line
                    )
                    if match:
                        agent_name = match.group(1)
                        agent_id = match.group(2)
                        agent_status = match.group(3)
                    else:
                        continue

                # 헤더 행 스킵
                if agent_name in ("Agent", "Step", "---", ""):
                    continue

                # 마지막 에이전트 추적
                last_agent = agent_name
                if agent_id and agent_id != "-":
                    last_agent_id = agent_id

                # 상태 추적
                if agent_status in ("in_progress", "running"):
                    status = "in_progress"

    except OSError as e:
        log(f"플랜 파일 읽기 실패: {e}")

    return last_agent, last_agent_id, status


def collect_completed_phases(project_root: str) -> list:
    """완료된 작업 수집"""
    complete_dir = os.path.join(project_root, ".claude", "plans", "complete")
    phases = []

    if not os.path.isdir(complete_dir):
        return phases

    for date_dir in sorted(glob(os.path.join(complete_dir, "*"))):
        if not os.path.isdir(date_dir):
            continue

        date_name = os.path.basename(date_dir)

        # YYYY-MM-DD 형식 검증
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_name):
            continue

        for plan_file in glob(os.path.join(date_dir, "*.md")):
            filename = os.path.basename(plan_file)

            # DESIGN, TASKS, 레거시 PLAN_/DESIGN_/TASKS_ 파일 제외
            if (filename.endswith("-DESIGN.md") or
                "-TASKS" in filename or
                filename.startswith("DESIGN_") or
                filename.startswith("PLAN_") or
                filename.startswith("TASKS_")):
                continue

            plan_name = filename.replace(".md", "")
            phases.append({
                "name": plan_name,
                "completed_at": date_name,
                "path": f".claude/plans/complete/{date_name}/{filename}"
            })

    return phases


def generate_plans_tree(project_root: str) -> str:
    """플랜 디렉토리 트리 생성"""
    plans_dir = os.path.join(project_root, ".claude", "plans")

    try:
        # tree 명령 시도
        result = subprocess.run(
            ["tree", "-L", "3", "--noreport", plans_dir],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            lines = result.stdout.split("\n")[:50]
            return "\n".join(lines)
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    # 폴백: 간단한 파일 목록
    try:
        files = []
        for md_file in glob(os.path.join(plans_dir, "**", "*.md"), recursive=True):
            rel_path = os.path.relpath(md_file, plans_dir)
            files.append(rel_path)
        return "\n".join(sorted(files)[:30])
    except OSError:
        return ""


def main():
    setup_hook_config("PreCompact")

    # stdin에서 JSON 읽기
    try:
        json_input = sys.stdin.read()
        data = json.loads(json_input)
    except (json.JSONDecodeError, ValueError):
        log("JSON 파싱 실패")
        sys.exit(0)

    log("PreCompact hook triggered (v4)")

    session_id = data.get("session_id", "unknown")
    transcript_path = data.get("transcript_path", "")
    trigger = data.get("trigger", "unknown")

    log(f"Session ID: {session_id}")
    log(f"Transcript path: {transcript_path}")
    log(f"Trigger: {trigger}")

    # 프로젝트 루트
    project_root = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())

    # 타임스탬프 (ISO-8601 UTC)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # 활성 플랜 찾기
    active_plan, active_plan_name = find_active_plan(project_root)

    if not active_plan:
        log("No active plan found, creating minimal checkpoint")

        checkpoint_entry = {
            "timestamp": timestamp,
            "session_id": session_id,
            "transcript_path": transcript_path,
            "current_work": None,
            "completed_phases": [],
            "plans_tree": "",
            "summary": "작업 없음"
        }

        checkpoints_file = os.path.join(project_root, ".claude", "checkpoints.json")
        if add_checkpoint(checkpoint_entry, checkpoints_file):
            log(f"Minimal checkpoint added to FIFO: {checkpoints_file}")
        else:
            log("ERROR: Failed to add minimal checkpoint")

        sys.exit(0)

    log(f"Active plan: {active_plan_name}")

    # 관련 문서 찾기
    design_path, tasks_path = find_related_docs(project_root, active_plan_name)
    log(f"Design path: {design_path or 'none'}")
    log(f"Tasks path: {tasks_path or 'none'}")

    # Agent Execution Log 파싱
    last_agent, last_agent_id, status = parse_agent_execution_log(active_plan)
    log(f"Last agent: {last_agent or 'none'}")
    log(f"Last agent ID: {last_agent_id or 'none'}")
    log(f"Status: {status}")

    # 완료된 작업 수집
    completed_phases = collect_completed_phases(project_root)
    log("Collected completed phases")

    # 플랜 트리 생성
    plans_tree = generate_plans_tree(project_root)
    log("Generated plans tree")

    # current_work 객체 생성
    current_work = {
        "plan_path": f".claude/plans/{active_plan_name}.md",
        "design_path": design_path,
        "tasks_path": tasks_path,
        "status": status,
        "last_agent": last_agent,
        "last_agent_id": last_agent_id
    }

    # 체크포인트 요약
    checkpoint_summary = active_plan_name
    if last_agent:
        checkpoint_summary = f"{active_plan_name} ({last_agent})"

    # 체크포인트 엔트리 생성
    checkpoint_entry = {
        "timestamp": timestamp,
        "session_id": session_id,
        "transcript_path": transcript_path,
        "current_work": current_work,
        "completed_phases": completed_phases,
        "plans_tree": plans_tree,
        "summary": checkpoint_summary
    }

    # 체크포인트 추가
    checkpoints_file = os.path.join(project_root, ".claude", "checkpoints.json")
    if add_checkpoint(checkpoint_entry, checkpoints_file):
        # 개수 확인
        try:
            with open(checkpoints_file, "r", encoding="utf-8") as f:
                cp_data = json.load(f)
            checkpoint_count = len(cp_data.get("checkpoints", []))
        except (json.JSONDecodeError, OSError):
            checkpoint_count = "?"

        log(f"Checkpoint v4 added to FIFO: {checkpoints_file} (total: {checkpoint_count})")
        log(f"Plan: {active_plan_name}, Agent: {last_agent or 'none'}, Phases: {len(completed_phases)}")
    else:
        log("ERROR: Failed to add checkpoint to FIFO")

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # 오류 발생 시에도 압축 차단 금지
        log(f"ERROR: Script failed with {e}")
        sys.exit(0)
