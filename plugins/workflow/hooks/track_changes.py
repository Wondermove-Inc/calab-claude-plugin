#!/usr/bin/env python3
"""
PostToolUse Hook: 파일 변경 추적 (완전 자동화)

트리거: Edit 또는 Write 도구 사용 후
동작:
  1. 변경된 파일 추적 및 기록
  2. 파일 카테고리 자동 분류
  3. 세션별 변경 통계 관리
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Union


def get_project_root() -> Path:
    """프로젝트 루트 경로 반환"""
    project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '')
    if project_dir:
        return Path(project_dir)
    return Path(__file__).parent.parent.parent


PROJECT_ROOT = get_project_root()
STATE_DIR = PROJECT_ROOT / '.claude-state'


def load_json(path: Path) -> Union[list, dict]:
    """JSON 파일 로드"""
    if not path.exists():
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def save_json(path: Path, data: Union[list, dict]):
    """JSON 파일 저장"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def categorize_file(file_path: str) -> str:
    """파일 경로를 기반으로 카테고리 분류"""
    path = file_path.lower()

    if 'commands/' in path:
        return 'command'
    elif 'skills/' in path:
        return 'skill'
    elif 'hooks/' in path:
        return 'hook'
    elif 'templates/' in path:
        return 'template'
    elif '.claude/memory/' in path:
        return 'memory'
    elif 'best-practices/' in path:
        return 'best-practice'
    elif 'integrations/' in path:
        return 'integration'
    elif '.claude/research/' in path:
        return 'research'
    elif '/docs/' in path or 'readme' in path or 'claude.md' in path:
        return 'documentation'
    elif '/src/' in path or '/lib/' in path or '/app/' in path:
        return 'source'
    elif '/test' in path or '.test.' in path or '.spec.' in path:
        return 'test'
    elif '.json' in path or '.yaml' in path or '.yml' in path:
        return 'config'
    elif '.claude/' in path:
        return 'plugin-config'
    else:
        return 'other'


def get_file_extension(file_path: str) -> str:
    """파일 확장자 추출"""
    path = Path(file_path)
    return path.suffix.lstrip('.') if path.suffix else 'unknown'


def update_session_file_stats(category: str, extension: str):
    """세션별 파일 통계 업데이트"""
    stats_file = STATE_DIR / 'file_stats.json'
    stats = load_json(stats_file)
    if not isinstance(stats, dict):
        stats = {}

    today = datetime.now().strftime('%Y-%m-%d')

    if 'daily' not in stats:
        stats['daily'] = {}

    if today not in stats['daily']:
        stats['daily'][today] = {
            'total_changes': 0,
            'by_category': {},
            'by_extension': {}
        }

    daily = stats['daily'][today]
    daily['total_changes'] += 1

    # 카테고리별 통계
    if category not in daily['by_category']:
        daily['by_category'][category] = 0
    daily['by_category'][category] += 1

    # 확장자별 통계
    if extension not in daily['by_extension']:
        daily['by_extension'][extension] = 0
    daily['by_extension'][extension] += 1

    # 최근 7일만 유지
    dates = sorted(stats['daily'].keys())
    if len(dates) > 7:
        for old_date in dates[:-7]:
            del stats['daily'][old_date]

    save_json(stats_file, stats)


def main():
    """메인 함수 - Hook Entry Point"""
    STATE_DIR.mkdir(parents=True, exist_ok=True)

    # stdin에서 도구 사용 정보 읽기
    try:
        input_data = json.load(sys.stdin)
    except Exception:
        return  # JSON 파싱 실패 시 조용히 종료

    # 파일 경로 추출
    tool_input = input_data.get('tool_input', {})
    file_path = tool_input.get('file_path', '')

    if not file_path:
        return

    # 파일 정보 추출
    category = categorize_file(file_path)
    extension = get_file_extension(file_path)
    tool_name = input_data.get('tool_name', 'unknown')

    # 변경 파일 로그에 추가
    changes_file = STATE_DIR / 'recent_changes.json'
    changes = load_json(changes_file)
    if not isinstance(changes, list):
        changes = []

    # 새 변경 기록 추가
    change_record = {
        "timestamp": datetime.now().isoformat(),
        "file_path": file_path,
        "tool": tool_name,
        "category": category,
        "extension": extension
    }

    # 중복 제거 (같은 파일은 최신 것만 유지)
    changes = [c for c in changes if c.get('file_path') != file_path]
    changes.append(change_record)

    # 최근 100개만 유지
    changes = changes[-100:]

    # 저장
    save_json(changes_file, changes)

    # 세션 통계 업데이트
    update_session_file_stats(category, extension)


if __name__ == "__main__":
    main()
