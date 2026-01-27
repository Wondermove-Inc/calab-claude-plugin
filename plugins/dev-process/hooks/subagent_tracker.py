#!/usr/bin/env python3
"""
Subagent Tracker Hook - 서브에이전트 사용 추적

트리거: SubagentStart, SubagentStop 이벤트
동작: 서브에이전트 사용 로깅, 통계 수집
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent.parent.parent
STATE_PATH = PROJECT_ROOT / '.claude-state'


def load_json(path: Path) -> dict:
    """JSON 파일 로드"""
    if not path.exists():
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path: Path, data: dict):
    """JSON 파일 저장"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def track_subagent_start(agent_name: str, agent_id: str):
    """서브에이전트 시작 추적"""
    stats_file = STATE_PATH / 'subagent_stats.json'
    stats = load_json(stats_file)

    if 'agents' not in stats:
        stats['agents'] = {}

    if agent_name not in stats['agents']:
        stats['agents'][agent_name] = {
            'total_invocations': 0,
            'last_invoked': None
        }

    stats['agents'][agent_name]['total_invocations'] += 1
    stats['agents'][agent_name]['last_invoked'] = datetime.now().isoformat()

    # 현재 실행 중인 에이전트 기록
    if 'running' not in stats:
        stats['running'] = {}

    stats['running'][agent_id] = {
        'name': agent_name,
        'started_at': datetime.now().isoformat()
    }

    save_json(stats_file, stats)

    # 로그 출력
    print(f"[SUBAGENT] Started: {agent_name} (id: {agent_id})")


def track_subagent_stop(agent_id: str, result: str):
    """서브에이전트 종료 추적"""
    stats_file = STATE_PATH / 'subagent_stats.json'
    stats = load_json(stats_file)

    running = stats.get('running', {})
    agent_info = running.pop(agent_id, None)

    if agent_info:
        agent_name = agent_info.get('name', 'unknown')
        started_at = agent_info.get('started_at')

        # 실행 시간 계산
        if started_at:
            start_time = datetime.fromisoformat(started_at)
            duration = (datetime.now() - start_time).total_seconds()

            # 평균 실행 시간 업데이트
            if agent_name in stats.get('agents', {}):
                agent_stats = stats['agents'][agent_name]
                prev_avg = agent_stats.get('avg_duration', 0)
                count = agent_stats.get('total_invocations', 1)
                new_avg = ((prev_avg * (count - 1)) + duration) / count
                agent_stats['avg_duration'] = round(new_avg, 2)

        stats['running'] = running
        save_json(stats_file, stats)

        # 로그 출력
        print(f"[SUBAGENT] Stopped: {agent_name} (duration: {duration:.1f}s, result: {result})")
    else:
        print(f"[SUBAGENT] Stopped: unknown agent (id: {agent_id})")


def log_subagent_event(event_type: str, data: dict):
    """서브에이전트 이벤트 로깅"""
    log_file = STATE_PATH / 'subagent.log'

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] [{event_type}] {json.dumps(data, ensure_ascii=False)}\n"

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)


def main():
    """
    메인 함수 - Hook Entry Point

    SubagentStart, SubagentStop 이벤트에서 호출됩니다.
    """
    try:
        input_data = json.load(sys.stdin)

        event_type = input_data.get('event_type', 'unknown')
        agent_name = input_data.get('agent_name', 'unknown')
        agent_id = input_data.get('agent_id', 'unknown')

        if event_type == 'start':
            track_subagent_start(agent_name, agent_id)
            log_subagent_event('START', {
                'agent_name': agent_name,
                'agent_id': agent_id
            })

        elif event_type == 'stop':
            result = input_data.get('result', 'unknown')
            track_subagent_stop(agent_id, result)
            log_subagent_event('STOP', {
                'agent_id': agent_id,
                'result': result
            })

    except Exception as e:
        # 에러 시 조용히 통과
        pass


if __name__ == '__main__':
    main()
