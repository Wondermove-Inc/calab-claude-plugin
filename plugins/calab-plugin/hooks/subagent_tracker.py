#!/usr/bin/env python3
"""
Subagent Tracker Hook - 서브에이전트 사용 추적

트리거: SubagentStart, SubagentStop 이벤트
동작: 서브에이전트 사용 로깅, 통계 수집

공식 Claude Code Hook Input 필드 (v2.0.42+ / v2.0.43+):

SubagentStart (v2.0.43+):
  - session_id: 세션 고유 ID
  - transcript_path: 트랜스크립트 파일 경로
  - hook_event_name: "SubagentStart"
  - agent_id: 에이전트 고유 ID (v2.0.43+)
  - subagent_type: 에이전트 타입 (예: "Explore", "Plan") (v2.0.43+)

SubagentStop (v2.0.42+):
  - session_id: 세션 고유 ID
  - transcript_path: 트랜스크립트 파일 경로
  - hook_event_name: "SubagentStop"
  - agent_id: 에이전트 고유 ID (v2.0.42+)
  - agent_transcript_path: 에이전트 트랜스크립트 경로 (v2.0.42+)
  - stop_hook_active: 스톱 훅 활성 여부
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# 프로젝트 루트 경로 (현재 작업 디렉토리 사용)
PROJECT_ROOT = Path(os.getcwd())
STATE_PATH = PROJECT_ROOT / '.claude-state'

# 홈 디렉토리의 .claude-state도 체크
HOME_STATE_PATH = Path.home() / '.claude' / 'state'


def get_state_path() -> Path:
    """상태 저장 경로 결정"""
    if STATE_PATH.exists() or (PROJECT_ROOT / '.claude').exists():
        return STATE_PATH
    return HOME_STATE_PATH


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


def track_subagent_start(session_id: str, agent_id: str, subagent_type: str, transcript_path: str):
    """서브에이전트 시작 추적 (v2.0.43+ 필드 사용)"""
    state_path = get_state_path()
    stats_file = state_path / 'subagent_stats.json'
    stats = load_json(stats_file)

    # 에이전트 타입별 통계
    if 'agents' not in stats:
        stats['agents'] = {}

    if subagent_type not in stats['agents']:
        stats['agents'][subagent_type] = {
            'total_invocations': 0,
            'last_invoked': None
        }

    stats['agents'][subagent_type]['total_invocations'] += 1
    stats['agents'][subagent_type]['last_invoked'] = datetime.now().isoformat()

    # 현재 실행 중인 에이전트 기록
    if 'running' not in stats:
        stats['running'] = {}

    stats['running'][agent_id] = {
        'type': subagent_type,
        'session_id': session_id,
        'transcript_path': transcript_path,
        'started_at': datetime.now().isoformat()
    }

    # 전체 통계
    if 'total_starts' not in stats:
        stats['total_starts'] = 0
    stats['total_starts'] += 1
    stats['last_start'] = datetime.now().isoformat()

    save_json(stats_file, stats)

    # 로그 출력 (stderr로)
    print(f"[SUBAGENT] Started: {subagent_type} (id: {agent_id[:8]}...)", file=sys.stderr)


def track_subagent_stop(session_id: str, agent_id: str, agent_transcript_path: str, stop_hook_active: bool):
    """서브에이전트 종료 추적 (v2.0.42+ 필드 사용)"""
    state_path = get_state_path()
    stats_file = state_path / 'subagent_stats.json'
    stats = load_json(stats_file)

    running = stats.get('running', {})
    agent_info = running.pop(agent_id, None)

    if agent_info:
        subagent_type = agent_info.get('type', 'unknown')
        started_at = agent_info.get('started_at')

        # 실행 시간 계산
        duration = 0
        if started_at:
            try:
                start_time = datetime.fromisoformat(started_at)
                duration = (datetime.now() - start_time).total_seconds()

                # 평균 실행 시간 업데이트
                if subagent_type in stats.get('agents', {}):
                    agent_stats = stats['agents'][subagent_type]
                    prev_avg = agent_stats.get('avg_duration', 0)
                    count = agent_stats.get('total_invocations', 1)
                    new_avg = ((prev_avg * (count - 1)) + duration) / count
                    agent_stats['avg_duration'] = round(new_avg, 2)
            except (ValueError, TypeError):
                pass

        stats['running'] = running

        # 전체 통계
        if 'total_stops' not in stats:
            stats['total_stops'] = 0
        stats['total_stops'] += 1
        stats['last_stop'] = datetime.now().isoformat()

        save_json(stats_file, stats)

        # 로그 출력 (stderr로)
        print(f"[SUBAGENT] Stopped: {subagent_type} (duration: {duration:.1f}s)", file=sys.stderr)
    else:
        # running에서 찾지 못한 경우에도 기록
        if 'total_stops' not in stats:
            stats['total_stops'] = 0
        stats['total_stops'] += 1
        stats['last_stop'] = datetime.now().isoformat()
        save_json(stats_file, stats)

        print(f"[SUBAGENT] Stopped: unknown (id: {agent_id[:8] if agent_id else 'N/A'}...)", file=sys.stderr)


def extract_type_from_description(description: str) -> str:
    """
    description 필드에서 에이전트 타입 추출

    Task 도구 호출 시 description에 에이전트 정보가 포함될 수 있음
    """
    if not description:
        return ''

    # 알려진 에이전트 타입 패턴
    known_types = [
        'calab-plugin:planner-phase',
        'calab-plugin:design',
        'calab-plugin:planner-task',
        'calab-plugin:dev-executor',
        'calab-plugin:validator',
        'calab-plugin:reinforcer',
        'calab-plugin:code-reviewer',
        'calab-plugin:security-reviewer',
        'calab-plugin:root-cause-finder',
        'calab-plugin:bug-fixer',
        'calab-plugin:qa',
        'calab-plugin:web-researcher',
        'calab-plugin:deep-researcher',
        'calab-plugin:project-onboarder',
        'calab-plugin:doc-updater',
        'calab-plugin:docs-generator',
        'calab-plugin:build-error-resolver',
        'calab-plugin:e2e-runner',
        'calab-plugin:jira-connector',
        'calab-plugin:project-guardian',
        'calab-plugin:refactor-cleaner',
        'calab-plugin:task-validator',
        'calab-plugin:dev-workflow',
        'Explore',
        'Plan',
        'general-purpose',
    ]

    description_lower = description.lower()
    for agent_type in known_types:
        if agent_type.lower() in description_lower:
            return agent_type

    return ''


def log_event(event_type: str, data: dict):
    """이벤트 로깅"""
    state_path = get_state_path()
    log_file = state_path / 'subagent.log'

    state_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] [{event_type}] {json.dumps(data, ensure_ascii=False)}\n"

    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except IOError:
        pass


def main():
    """
    메인 함수 - Hook Entry Point

    사용법: python3 subagent_tracker.py [start|stop]

    Claude Code가 stdin으로 JSON 데이터를 전달합니다.
    v2.0.42+에서 agent_id, agent_transcript_path 필드 추가
    v2.0.43+에서 SubagentStart 훅과 subagent_type 필드 추가
    """
    # 커맨드라인 인자로 이벤트 타입 결정
    event_type = sys.argv[1] if len(sys.argv) > 1 else 'unknown'

    try:
        # stdin에서 Claude Code가 전달하는 공식 데이터 읽기
        input_data = json.load(sys.stdin)

        # 공통 필드
        session_id = input_data.get('session_id', 'unknown')
        transcript_path = input_data.get('transcript_path', '')
        hook_event_name = input_data.get('hook_event_name', event_type)

        # v2.0.42+ 필드
        agent_id = input_data.get('agent_id', 'unknown')

        # 이벤트 로깅
        log_event(hook_event_name, input_data)

        if event_type == 'start' or hook_event_name == 'SubagentStart':
            # v2.0.43+ SubagentStart 필드 - 여러 경로에서 타입 추출 시도
            subagent_type = (
                input_data.get('subagent_type') or
                input_data.get('tool_input', {}).get('subagent_type') or
                input_data.get('agent_type') or
                input_data.get('type') or
                extract_type_from_description(input_data.get('description', '')) or
                'unknown'
            )
            track_subagent_start(session_id, agent_id, subagent_type, transcript_path)

        elif event_type == 'stop' or hook_event_name == 'SubagentStop':
            # v2.0.42+ SubagentStop 필드
            agent_transcript_path = input_data.get('agent_transcript_path', '')
            stop_hook_active = input_data.get('stop_hook_active', False)
            track_subagent_stop(session_id, agent_id, agent_transcript_path, stop_hook_active)

    except json.JSONDecodeError:
        # JSON 파싱 실패 시 조용히 통과
        pass
    except Exception as e:
        # 다른 에러도 조용히 통과 (훅이 실패해도 Claude Code에 영향 주지 않음)
        print(f"[SUBAGENT] Error: {e}", file=sys.stderr)

    # 항상 성공 (exit code 0)
    sys.exit(0)


if __name__ == '__main__':
    main()
