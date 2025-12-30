#!/usr/bin/env python3
"""
Stop Hook - 세션 종료 시 자동 요약 저장

트리거: Claude Code 응답 완료 시
동작: 작업 진행 상황 자동 저장, 세션 요약 생성
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent.parent.parent
STATE_PATH = PROJECT_ROOT / '.claude-state'
MEMORY_PATH = PROJECT_ROOT / '.claude' / 'memory'


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


def update_session_stats(stop_reason: str):
    """세션 통계 업데이트"""
    stats_file = STATE_PATH / 'session_stats.json'
    stats = load_json(stats_file)

    today = datetime.now().strftime('%Y-%m-%d')

    if 'daily_stats' not in stats:
        stats['daily_stats'] = {}

    if today not in stats['daily_stats']:
        stats['daily_stats'][today] = {
            'interactions': 0,
            'first_interaction': datetime.now().isoformat(),
            'last_interaction': None
        }

    stats['daily_stats'][today]['interactions'] += 1
    stats['daily_stats'][today]['last_interaction'] = datetime.now().isoformat()
    stats['last_stop_reason'] = stop_reason

    save_json(stats_file, stats)


def create_checkpoint():
    """현재 상태 체크포인트 생성"""
    checkpoint_file = STATE_PATH / 'checkpoint.json'
    worktree_file = STATE_PATH / 'worktree.json'

    worktree = load_json(worktree_file)

    checkpoint = {
        'timestamp': datetime.now().isoformat(),
        'current_task': worktree.get('current_task', ''),
        'progress': worktree.get('progress', {}),
        'auto_saved': True
    }

    save_json(checkpoint_file, checkpoint)


def log_stop_event(stop_reason: str):
    """Stop 이벤트 로깅"""
    log_file = STATE_PATH / 'activity.log'

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] [STOP] reason={stop_reason}\n"

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)


def main():
    """
    메인 함수 - Hook Entry Point

    Stop 이벤트에서 호출됩니다.
    Claude Code가 응답을 완료했을 때 실행됩니다.
    """
    try:
        input_data = json.load(sys.stdin)
        stop_reason = input_data.get('stop_reason', 'unknown')

        # 세션 통계 업데이트
        update_session_stats(stop_reason)

        # 체크포인트 생성 (자동 저장)
        create_checkpoint()

        # 이벤트 로깅
        log_stop_event(stop_reason)

    except Exception as e:
        # 에러 시 조용히 통과
        pass


if __name__ == '__main__':
    main()
