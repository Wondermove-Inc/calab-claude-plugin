#!/usr/bin/env python3
"""
session_start_restore_hint.py - calab-claude-plugin 세션 시작 복원 힌트 훅 (v4)

원더 무브 연구소 Claude Plug-in의 SessionStart 훅.
Claude Code 세션 시작/재개 시 체크포인트 파일을 확인하고 복원 안내를 표시합니다.

v4 변경사항:
- FIFO 배열 최대 5개 체크포인트 지원
- 사용 가능한 체크포인트 목록 표시
- --slot N 옵션으로 특정 체크포인트 복원

훅 입력 (stdin JSON):
- hook_event_name: "SessionStart"
- session_id: string
- is_resume: boolean
- agent_type: string | null (2.1.2+)

종료 코드:
- 0: 무음 (체크포인트 없음 또는 스킵)
- 2: Claude에 메시지 표시

설계 철학:
- 비침투적: 체크포인트 존재 시에만 메시지 표시
- 정상 실패: 잘못된 JSON → 무음 모드
- 사용자 친화적: 명확한 복원 안내 제공

원본: claude-monitoring-main
적용: calab-claude-plugin v2.3.0+
"""

import json
import sys
import os

# hook_utils에서 유틸리티 임포트
# 주의: CHECKPOINT_FILE, CHECKPOINTS_FILE은 setup_hook_config() 호출 후에
#       hook_utils 모듈에서 직접 접근해야 합니다 (import 시점에는 빈 문자열)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hook_utils
from hook_utils import (
    setup_hook_config,
    log,
    validate_checkpoint_file,
    checkpoint_get,
    calculate_relative_time,
    get_checkpoint_count,
    get_latest_checkpoint,
)


def display_v4_checkpoints(checkpoints_file: str) -> None:
    """v4 체크포인트 목록 표시"""
    try:
        with open(checkpoints_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        checkpoints = data.get("checkpoints", [])
        checkpoint_count = len(checkpoints)

        if checkpoint_count == 0:
            log("No checkpoints in v4 file")
            sys.exit(0)

        # 최신 체크포인트 정보
        latest = checkpoints[-1]
        latest_timestamp = latest.get("timestamp", "unknown")
        latest_relative_time = calculate_relative_time(latest_timestamp)

        # 현재 작업 정보
        current_work = latest.get("current_work")
        if current_work:
            plan_path = current_work.get("plan_path", "")
            plan_name = os.path.basename(plan_path).replace(".md", "") if plan_path else "unknown"
        else:
            plan_name = "(목표 설정 대기)"

        # 헤더 출력
        print("=" * 50)
        print(" [SESSION START] 컨텍스트 복원 안내")
        print("=" * 50)
        print(f" 저장된 체크포인트: {checkpoint_count}개")
        print()
        print(" 복원 가능한 체크포인트:")
        print()

        # 체크포인트 목록 (최신순)
        for i in range(checkpoint_count - 1, -1, -1):
            cp = checkpoints[i]
            cp_timestamp = cp.get("timestamp", "unknown")
            cp_summary = cp.get("summary", "작업 정보 없음")
            cp_relative = calculate_relative_time(cp_timestamp)

            display_index = checkpoint_count - i
            print(f" [{display_index}] {cp_relative:10} - {cp_summary}")

        # 완료된 작업 표시
        completed_phases = latest.get("completed_phases", [])
        completed_count = len(completed_phases)

        if completed_count > 0:
            print()
            print(f" 완료된 작업 ({completed_count}개):")
            for phase in completed_phases[-3:]:  # 최근 3개만
                name = phase.get("name", "unknown")
                date = phase.get("completed_at", "")
                print(f"    - {name} ({date})")

        # 복원 선택 JSON
        session_choice = {
            "checkpoint_detected": True,
            "version": "4.0",
            "checkpoint_count": checkpoint_count,
            "latest_plan": plan_name,
            "latest_time": latest_relative_time,
            "options": ["restore", "fresh", "later"]
        }

        print()
        print(" 복원 명령:")
        print("   /restore-context          - 대화형 선택")
        print("   /restore-context --slot N - 특정 시점 (1=최근)")
        print()
        print("<session-start-choice>")
        print(json.dumps(session_choice, ensure_ascii=False, indent=2))
        print("</session-start-choice>")
        print("=" * 50)

        log(f"v4 display complete: {checkpoint_count} checkpoints, latest={plan_name}")
        sys.exit(2)  # 메시지 표시

    except (json.JSONDecodeError, OSError) as e:
        log(f"v4 체크포인트 읽기 실패: {e}")
        sys.exit(0)


def display_v3_checkpoint(checkpoint_file: str) -> None:
    """v3 체크포인트 표시 (레거시)"""
    try:
        with open(checkpoint_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        timestamp = data.get("timestamp", "unknown")
        relative_time = calculate_relative_time(timestamp)

        current_work = data.get("current_work")
        if current_work:
            plan_path = current_work.get("plan_path", "")
            plan_name = os.path.basename(plan_path).replace(".md", "") if plan_path else "unknown"
        else:
            plan_name = "(목표 설정 대기)"

        completed_phases = data.get("completed_phases", [])
        completed_count = len(completed_phases)

        log(f"v3 Checkpoint: plan={plan_name}, completed={completed_count}")

        print("=" * 50)
        print(" [SESSION START] 컨텍스트 복원 안내")
        print("=" * 50)
        print(f" 마지막 체크포인트: {relative_time}")
        print("   이벤트: session_end")
        print(f" 이전 목표: {plan_name}...")

        if current_work:
            print(" 이전 작업 컨텍스트가 존재합니다.")

        if completed_count > 0:
            print()
            print(f" 완료된 작업 ({completed_count}개):")
            for phase in completed_phases[-3:]:
                name = phase.get("name", "unknown")
                date = phase.get("completed_at", "")
                print(f"    - {name} ({date})")

        print()
        print(" '/restore-context' 명령으로")
        print("   이전 작업을 이어갈 수 있습니다.")
        print("=" * 50)

        sys.exit(2)

    except (json.JSONDecodeError, OSError) as e:
        log(f"v3 체크포인트 읽기 실패: {e}")
        sys.exit(0)


def display_v1_checkpoint(checkpoint_file: str) -> None:
    """v1 체크포인트 표시 (레거시)"""
    try:
        with open(checkpoint_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        timestamp = data.get("timestamp", "unknown")
        relative_time = calculate_relative_time(timestamp)
        plan_name = data.get("plan_name", "unknown")
        current_phase = data.get("current_phase", "1")

        log(f"v1 Checkpoint found: {plan_name} PHASE {current_phase}")

        print("=" * 50)
        print(" [SESSION START] 컨텍스트 복원 안내")
        print("=" * 50)
        print(f" 마지막 체크포인트: {relative_time}")
        print("   이벤트: session_end")
        print(f" 이전 목표: {plan_name}...")
        print(" 이전 작업 컨텍스트가 존재합니다.")
        print()
        print(" '/restore-context' 명령으로")
        print("   이전 작업을 이어갈 수 있습니다.")
        print("=" * 50)

        sys.exit(2)

    except (json.JSONDecodeError, OSError) as e:
        log(f"v1 체크포인트 읽기 실패: {e}")
        sys.exit(0)


def main():
    setup_hook_config("SessionStart")

    # stdin에서 JSON 읽기
    try:
        json_input = sys.stdin.read()
        data = json.loads(json_input)
    except (json.JSONDecodeError, ValueError):
        log("JSON 파싱 실패")
        sys.exit(0)

    session_id = data.get("session_id", "unknown")
    is_resume = data.get("is_resume", False)

    log(f"SessionStart hook triggered (v4)")
    log(f"Session: {session_id}, Resume: {is_resume}")

    # v4 체크포인트 파일 우선 확인
    # 주의: setup_hook_config() 호출 후 hook_utils 모듈에서 직접 접근
    checkpoints_file = hook_utils.CHECKPOINTS_FILE
    checkpoint_file = hook_utils.CHECKPOINT_FILE

    if os.path.isfile(checkpoints_file):
        try:
            with open(checkpoints_file, "r", encoding="utf-8") as f:
                cp_data = json.load(f)

            version = cp_data.get("version", "1.0")
            log(f"Checkpoint version: {version}")

            if version == "4.0":
                display_v4_checkpoints(checkpoints_file)
                return
        except (json.JSONDecodeError, OSError):
            pass

    # v3/v1 체크포인트 확인
    if os.path.isfile(checkpoint_file):
        try:
            with open(checkpoint_file, "r", encoding="utf-8") as f:
                cp_data = json.load(f)

            version = cp_data.get("version", "1.0")
            log(f"Checkpoint version: {version}")

            if version == "3.0":
                display_v3_checkpoint(checkpoint_file)
            else:
                display_v1_checkpoint(checkpoint_file)
            return
        except (json.JSONDecodeError, OSError):
            pass

    log("No valid checkpoint file found")
    sys.exit(0)


if __name__ == "__main__":
    main()
