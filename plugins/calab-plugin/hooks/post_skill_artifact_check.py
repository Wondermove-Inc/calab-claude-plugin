#!/usr/bin/env python3
"""
Post Skill Artifact Check Hook - 스킬/에이전트 완료 후 산출물 검증

트리거: SubagentStop 이벤트
동작: 에이전트 타입별 필수 산출물 존재 여부 검증

산출물 검증 규칙 (CLAUDE.md 기반):
- planner-phase → .claude/docs/active/{feature}/01-brainstorm.md + 02-PRD.md
- design → .claude/docs/active/{feature}/03-architecture.md + 04-ERD.md
- planner-task → .claude/docs/active/{feature}/05-tasks.md + .claude-state/worktree.json
- validator → .claude/docs/active/{feature}/validation-report.md
- reinforcer → .claude/docs/active/{feature}/reinforcer-report.md
- build-error-resolver → .claude/docs/active/{feature}/build-error-report.md
- project-onboarder → .claude/project-context/ (5개 문서)
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# 프로젝트 루트 경로
PROJECT_ROOT = Path(os.getcwd())
STATE_PATH = PROJECT_ROOT / '.claude-state'
DOCS_PATH = PROJECT_ROOT / '.claude' / 'docs' / 'active'
CONTEXT_PATH = PROJECT_ROOT / '.claude' / 'project-context'


# 에이전트별 필수 산출물 정의
AGENT_ARTIFACTS: Dict[str, Dict] = {
    # planner-phase: 브레인스토밍 + PRD 문서
    "calab-plugin:planner-phase": {
        "name": "기획 문서 (브레인스토밍 + PRD)",
        "patterns": [
            "{docs}/*/01-brainstorm.md",
            "{docs}/*/02-PRD.md",
            "{docs}/**/01-brainstorm.md",
            "{docs}/**/02-PRD.md",
        ],
        "required": True,
        "min_count": 2,  # 브레인스토밍 + PRD 둘 다 필요
        "description": "기능 기획 문서 (브레인스토밍 + PRD)"
    },

    # design: 아키텍처 + ERD 문서
    "calab-plugin:design": {
        "name": "설계 문서 (아키텍처 + ERD)",
        "patterns": [
            "{docs}/*/03-architecture.md",
            "{docs}/*/04-ERD.md",
            "{docs}/**/03-architecture.md",
            "{docs}/**/04-ERD.md",
        ],
        "required": True,
        "min_count": 2,  # 아키텍처 + ERD 둘 다 필요
        "description": "아키텍처 및 ERD 설계 문서"
    },

    # planner-task: Task 목록 + Worktree (둘 다 필수)
    "calab-plugin:planner-task": {
        "name": "Task 분해 문서 + Worktree",
        "patterns": [
            "{docs}/*/05-tasks.md",
            "{docs}/**/05-tasks.md",
            "{state}/worktree.json",
        ],
        "required": True,
        "min_count": 2,  # 05-tasks.md + worktree.json 둘 다 필수
        "description": "Task 분해 목록 및 Worktree 상태 파일"
    },

    # validator: 검증 보고서
    "calab-plugin:validator": {
        "name": "검증 보고서",
        "patterns": [
            "{docs}/*/validation-report.md",
            "{docs}/**/validation-report.md",
        ],
        "required": True,
        "description": "AC 검증 보고서"
    },

    # reinforcer: 수정 보고서
    "calab-plugin:reinforcer": {
        "name": "수정 보고서",
        "patterns": [
            "{docs}/*/reinforcer-report.md",
            "{docs}/**/reinforcer-report.md",
        ],
        "required": True,
        "description": "reinforcer 수정 보고서"
    },

    # build-error-resolver: 오류 분석 보고서
    "calab-plugin:build-error-resolver": {
        "name": "빌드 오류 분석 보고서",
        "patterns": [
            "{docs}/*/build-error-report.md",
            "{docs}/**/build-error-report.md",
        ],
        "required": True,
        "description": "빌드 오류 분석 및 해결 보고서"
    },

    # project-onboarder: 5개 컨텍스트 문서
    "calab-plugin:project-onboarder": {
        "name": "프로젝트 컨텍스트 문서",
        "patterns": [
            "{context}/*.md",
        ],
        "required": True,
        "min_count": 3,  # 최소 3개 이상
        "description": "프로젝트 분석 컨텍스트 문서"
    },

    # root-cause-finder: 근본 원인 분석 보고서
    "calab-plugin:root-cause-finder": {
        "name": "근본 원인 분석 보고서",
        "patterns": [
            "{root}/.claude/problem-solving/**/analysis.md",
            "{root}/.claude/problem-solving/**/report.md",
        ],
        "required": True,
        "description": "5 Whys / RCA 분석 보고서"
    },

    # deep-researcher: 리서치 보고서
    "calab-plugin:deep-researcher": {
        "name": "리서치 보고서",
        "patterns": [
            "{root}/.claude/research/*.md",
        ],
        "required": True,
        "description": "심층 리서치 분석 보고서"
    },

    # web-researcher: 웹 리서치 결과
    "calab-plugin:web-researcher": {
        "name": "웹 리서치 결과",
        "patterns": [
            "{root}/.claude/research/*.md",
        ],
        "required": True,
        "description": "웹 검색 및 분석 결과"
    },

    # qa: QA 검증 보고서
    "calab-plugin:qa": {
        "name": "QA 검증 보고서",
        "patterns": [
            "{docs}/*/qa-report.md",
            "{docs}/**/qa-report.md",
        ],
        "required": True,
        "description": "8단계 QA 검증 보고서"
    },

    # bug-fixer: 버그 수정 보고서
    "calab-plugin:bug-fixer": {
        "name": "버그 수정 보고서",
        "patterns": [
            "{root}/.claude/problem-solving/**/fix-report.md",
            "{docs}/**/bug-fix-report.md",
        ],
        "required": True,
        "description": "TDD 기반 버그 수정 보고서"
    },

    # code-reviewer: 코드 리뷰 보고서
    "calab-plugin:code-reviewer": {
        "name": "코드 리뷰 보고서",
        "patterns": [
            "{docs}/*/code-review.md",
            "{docs}/**/code-review.md",
        ],
        "required": True,
        "description": "코드 품질 검토 보고서"
    },

    # security-reviewer: 보안 검토 보고서
    "calab-plugin:security-reviewer": {
        "name": "보안 검토 보고서",
        "patterns": [
            "{docs}/*/security-review.md",
            "{docs}/**/security-review.md",
        ],
        "required": True,
        "description": "OWASP 기반 보안 취약점 분석 보고서"
    },

    # task-validator: Task 검증 보고서
    "calab-plugin:task-validator": {
        "name": "Task 검증 보고서",
        "patterns": [
            "{docs}/*/task-validation.md",
            "{docs}/**/task-validation.md",
        ],
        "required": True,
        "description": "Task 분해 검증 보고서"
    },

    # dev-executor: 구현 완료 보고서
    "calab-plugin:dev-executor": {
        "name": "구현 완료 보고서",
        "patterns": [
            "{docs}/*/implementation-report.md",
            "{docs}/**/implementation-report.md",
        ],
        "required": True,
        "description": "TDD 구현 완료 보고서"
    },

    # dev-workflow: 워크플로우 로그
    "calab-plugin:dev-workflow": {
        "name": "워크플로우 로그",
        "patterns": [
            "{docs}/*/workflow-log.md",
            "{docs}/**/workflow-log.md",
            "{state}/workflow.json",
        ],
        "required": True,
        "description": "개발 워크플로우 진행 로그"
    },

    # doc-updater: 문서 업데이트 보고서
    "calab-plugin:doc-updater": {
        "name": "문서 업데이트 보고서",
        "patterns": [
            "{docs}/*/doc-update-report.md",
            "{docs}/**/doc-update-report.md",
        ],
        "required": True,
        "description": "문서 자동 업데이트 결과 보고서"
    },

    # docs-generator: 생성된 문서 목록
    "calab-plugin:docs-generator": {
        "name": "생성된 문서 목록",
        "patterns": [
            "{docs}/*/generated-docs.md",
            "{docs}/**/generated-docs.md",
        ],
        "required": True,
        "description": "코드 기반 자동 생성된 문서 목록"
    },

    # e2e-runner: E2E 테스트 결과 리포트
    "calab-plugin:e2e-runner": {
        "name": "E2E 테스트 결과 리포트",
        "patterns": [
            "{docs}/*/e2e-report.md",
            "{docs}/**/e2e-report.md",
            "{root}/test-results/*.html",
            "{root}/playwright-report/*.html",
        ],
        "required": True,
        "description": "Playwright/Puppeteer E2E 테스트 결과"
    },

    # jira-connector: 동기화 로그
    "calab-plugin:jira-connector": {
        "name": "JIRA 동기화 로그",
        "patterns": [
            "{docs}/*/jira-sync.md",
            "{docs}/**/jira-sync.md",
            "{state}/jira-sync.json",
        ],
        "required": True,
        "description": "JIRA 양방향 동기화 결과 로그"
    },

    # project-guardian: 규칙 검증 보고서
    "calab-plugin:project-guardian": {
        "name": "규칙 검증 보고서",
        "patterns": [
            "{docs}/*/guardian-report.md",
            "{docs}/**/guardian-report.md",
        ],
        "required": True,
        "description": "프로젝트 규칙 준수 검증 보고서"
    },

    # refactor-cleaner: 리팩토링 결과 보고서
    "calab-plugin:refactor-cleaner": {
        "name": "리팩토링 결과 보고서",
        "patterns": [
            "{docs}/*/refactor-report.md",
            "{docs}/**/refactor-report.md",
        ],
        "required": True,
        "description": "데드 코드 정리 및 리팩토링 결과"
    },

    # agent-verifier: 에이전트 출력 검증 보고서
    "calab-plugin:agent-verifier": {
        "name": "에이전트 출력 검증 보고서",
        "patterns": [
            "{docs}/*/agent-verification-report.md",
            "{docs}/**/agent-verification-report.md",
        ],
        "required": True,
        "description": "병렬 에이전트 산출물 검증 보고서"
    },
}


def load_json(path: Path) -> dict:
    """JSON 파일 로드"""
    if not path.exists():
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_json(path: Path, data: dict):
    """JSON 파일 저장"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def expand_pattern(pattern: str) -> str:
    """패턴의 플레이스홀더 확장"""
    return pattern.format(
        docs=str(DOCS_PATH),
        context=str(CONTEXT_PATH),
        root=str(PROJECT_ROOT),
        state=str(STATE_PATH)
    )


def find_matching_files(pattern: str) -> List[Path]:
    """글로브 패턴에 매칭되는 파일 찾기"""
    import glob
    expanded = expand_pattern(pattern)
    matches = glob.glob(expanded, recursive=True)
    return [Path(m) for m in matches if Path(m).is_file()]


def get_recent_files(files: List[Path], minutes: int = 30) -> List[Path]:
    """최근 N분 이내에 수정된 파일만 필터링"""
    now = datetime.now()
    recent = []
    for f in files:
        try:
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            if (now - mtime).total_seconds() < minutes * 60:
                recent.append(f)
        except OSError:
            pass
    return recent


def check_artifacts(agent_type: str) -> Tuple[bool, str, List[str]]:
    """
    에이전트 타입별 산출물 검증

    Returns:
        (통과여부, 메시지, 발견된_파일목록)
    """
    if agent_type not in AGENT_ARTIFACTS:
        return True, f"[INFO] {agent_type}: 산출물 규칙 미정의 (검증 생략)", []

    spec = AGENT_ARTIFACTS[agent_type]
    artifact_name = spec["name"]
    patterns = spec["patterns"]
    required = spec.get("required", False)
    min_count = spec.get("min_count", 1)

    # 모든 패턴에서 파일 찾기
    all_files = []
    for pattern in patterns:
        matches = find_matching_files(pattern)
        all_files.extend(matches)

    # 중복 제거
    all_files = list(set(all_files))

    # 최근 파일만 필터 (선택적)
    recent_files = get_recent_files(all_files, minutes=60)

    # 검증
    if len(all_files) == 0:
        if required:
            return False, f"[ERROR] {agent_type}: 필수 산출물 '{artifact_name}' 미생성", []
        else:
            return True, f"[WARN] {agent_type}: 산출물 '{artifact_name}' 미생성 (선택적)", []

    if len(all_files) < min_count:
        if required:
            return False, f"[ERROR] {agent_type}: 산출물 부족 ({len(all_files)}/{min_count})", [str(f) for f in all_files]
        else:
            return True, f"[WARN] {agent_type}: 산출물 부족 ({len(all_files)}/{min_count})", [str(f) for f in all_files]

    return True, f"[OK] {agent_type}: 산출물 '{artifact_name}' 확인됨 ({len(all_files)}개)", [str(f) for f in all_files]


def log_result(agent_type: str, passed: bool, message: str, files: List[str]):
    """검증 결과 로깅"""
    state_path = STATE_PATH
    log_file = state_path / 'artifact_check.log'

    state_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = "PASS" if passed else "FAIL"

    log_entry = {
        "timestamp": timestamp,
        "agent_type": agent_type,
        "status": status,
        "message": message,
        "files": files
    }

    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except IOError:
        pass


def update_stats(agent_type: str, passed: bool):
    """산출물 검증 통계 업데이트"""
    stats_file = STATE_PATH / 'artifact_stats.json'
    stats = load_json(stats_file)

    if 'agents' not in stats:
        stats['agents'] = {}

    if agent_type not in stats['agents']:
        stats['agents'][agent_type] = {
            'total_checks': 0,
            'passed': 0,
            'failed': 0
        }

    stats['agents'][agent_type]['total_checks'] += 1
    if passed:
        stats['agents'][agent_type]['passed'] += 1
    else:
        stats['agents'][agent_type]['failed'] += 1

    stats['last_check'] = datetime.now().isoformat()

    save_json(stats_file, stats)


def main():
    """
    메인 함수 - Hook Entry Point

    SubagentStop 이벤트에서 호출됨.
    stdin으로 JSON 데이터 수신.

    Exit Code 정책 (베스트 프랙티스):
    - Exit 0: 성공, stdout → Claude 컨텍스트 (verbose 모드)
    - Exit 2: 차단, stderr → Claude에게 자동 피드백 (재실행 유도)
    - 기타: 비차단 에러, stderr → 사용자만 표시
    """
    try:
        # stdin에서 Claude Code가 전달하는 공식 데이터 읽기
        input_data = json.load(sys.stdin)

        # 필수 필드 추출
        hook_event_name = input_data.get('hook_event_name', '')
        agent_id = input_data.get('agent_id', 'unknown')

        # SubagentStop 이벤트만 처리
        if hook_event_name != 'SubagentStop':
            sys.exit(0)

        # 에이전트 타입 추출 (우선순위: stdin > subagent_stats.json)
        # Claude Code v2.0.42+에서 SubagentStop stdin에 agent_type 직접 제공
        agent_type = input_data.get('agent_type', '')

        # stdin에 없으면 subagent_stats.json에서 조회 (fallback)
        if not agent_type or agent_type in ('unknown', ''):
            stats_file = STATE_PATH / 'subagent_stats.json'
            stats = load_json(stats_file)
            running = stats.get('running', {})
            agent_info = running.get(agent_id, {})
            agent_type = agent_info.get('type', 'unknown')

        # unknown이면 종료
        if agent_type == 'unknown':
            print(f"[ARTIFACT] Agent type unknown for {agent_id[:8]}...", file=sys.stderr)
            sys.exit(0)

        # 산출물 검증
        passed, message, files = check_artifacts(agent_type)

        # 로깅
        log_result(agent_type, passed, message, files)

        # 통계 업데이트
        update_stats(agent_type, passed)

        # 결과 출력 (stderr로)
        print(message, file=sys.stderr)

        # 파일 목록 출력 (있으면)
        if files:
            for f in files[:5]:  # 최대 5개만
                print(f"  → {f}", file=sys.stderr)
            if len(files) > 5:
                print(f"  ... 외 {len(files) - 5}개", file=sys.stderr)

        # 필수 산출물 미생성 시 차단
        # 베스트 프랙티스: JSON decision: block (exit 0) 사용
        if not passed:
            spec = AGENT_ARTIFACTS.get(agent_type, {})
            if spec.get('required', False):
                # JSON 응답 (decision: block)
                response = {
                    "decision": "block",
                    "reason": f"필수 산출물 미생성: {spec.get('name', 'unknown')}",
                    "systemMessage": f"에이전트 {agent_type}의 필수 산출물이 생성되지 않았습니다. "
                                    f"예상 경로: {spec.get('patterns', ['unknown'])[0]}. "
                                    f"산출물을 생성한 후 다시 시도하세요."
                }
                print(json.dumps(response, ensure_ascii=False))

                # stderr로도 출력 (사용자 피드백)
                print(f"\n⚠️  산출물 미생성으로 에이전트 종료 차단", file=sys.stderr)
                print(f"   에이전트: {agent_type}", file=sys.stderr)
                print(f"   필수 산출물: {spec.get('name', 'unknown')}", file=sys.stderr)
                print(f"   예상 경로: {spec.get('patterns', ['unknown'])[0]}", file=sys.stderr)
                print(f"\n📋 산출물 생성 후 다시 시도하세요.", file=sys.stderr)

                # Exit 0 (JSON decision: block이 차단 처리)
                sys.exit(0)

    except json.JSONDecodeError:
        pass
    except Exception as e:
        print(f"[ARTIFACT] Error: {e}", file=sys.stderr)

    sys.exit(0)


if __name__ == '__main__':
    main()
