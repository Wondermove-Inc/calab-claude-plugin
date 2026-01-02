#!/usr/bin/env python3
"""
Stop Hook - 세션 종료 시 자동 요약 저장 (완전 자동화)

트리거: Claude Code 응답 완료 시
동작:
  1. 작업 진행 상황 자동 저장
  2. CURRENT_CONTEXT.md 자동 업데이트
  3. 변경 파일 기반 작업 요약 생성
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime

# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent.parent.parent
STATE_PATH = PROJECT_ROOT / '.claude-state'
MEMORY_PATH = PROJECT_ROOT / '.claude' / 'memory'


def load_json(path: Path) -> dict | list:
    """JSON 파일 로드"""
    if not path.exists():
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_json(path: Path, data: dict | list):
    """JSON 파일 저장"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_recent_changes() -> list:
    """최근 변경 파일 목록 가져오기"""
    changes_file = STATE_PATH / 'recent_changes.json'
    changes = load_json(changes_file)
    if not isinstance(changes, list):
        return []
    return changes


def get_session_changes() -> list:
    """현재 세션의 변경 파일만 필터링"""
    changes = get_recent_changes()
    if not changes:
        return []

    # 세션 시작 시간 가져오기
    stats_file = STATE_PATH / 'session_stats.json'
    stats = load_json(stats_file)

    today = datetime.now().strftime('%Y-%m-%d')
    daily_stats = stats.get('daily_stats', {}).get(today, {})
    first_interaction = daily_stats.get('first_interaction', '')

    if not first_interaction:
        # 세션 시작 시간이 없으면 최근 10개만 반환
        return changes[-10:]

    # 세션 시작 이후 변경만 필터링
    session_changes = []
    for change in changes:
        change_time = change.get('timestamp', '')
        if change_time >= first_interaction:
            session_changes.append(change)

    return session_changes


def categorize_changes(changes: list) -> dict:
    """변경 파일을 카테고리별로 분류"""
    categories = {
        'commands': [],      # commands/
        'skills': [],        # skills/
        'hooks': [],         # .claude/hooks/
        'templates': [],     # .claude/templates/
        'memory': [],        # .claude/memory/
        'docs': [],          # docs/, README, CLAUDE.md
        'source': [],        # src/, lib/, app/
        'config': [],        # .claude/, config files
        'other': []
    }

    for change in changes:
        path = change.get('file_path', '')

        if 'commands/' in path:
            categories['commands'].append(path)
        elif 'skills/' in path:
            categories['skills'].append(path)
        elif '.claude/hooks/' in path:
            categories['hooks'].append(path)
        elif '.claude/templates/' in path:
            categories['templates'].append(path)
        elif '.claude/memory/' in path:
            categories['memory'].append(path)
        elif '/docs/' in path or 'README' in path or 'CLAUDE.md' in path:
            categories['docs'].append(path)
        elif '/src/' in path or '/lib/' in path or '/app/' in path:
            categories['source'].append(path)
        elif '.claude/' in path:
            categories['config'].append(path)
        else:
            categories['other'].append(path)

    return categories


def generate_work_summary(categories: dict) -> list:
    """카테고리 기반 작업 요약 생성"""
    summary = []

    category_labels = {
        'commands': '명령어',
        'skills': '스킬',
        'hooks': '훅',
        'templates': '템플릿',
        'memory': '메모리',
        'docs': '문서',
        'source': '소스코드',
        'config': '설정',
        'other': '기타'
    }

    for cat, files in categories.items():
        if not files:
            continue

        label = category_labels.get(cat, cat)

        if len(files) == 1:
            # 단일 파일
            filename = Path(files[0]).name
            summary.append(f"{label}: {filename}")
        else:
            # 여러 파일
            filenames = [Path(f).name for f in files[:3]]
            if len(files) > 3:
                summary.append(f"{label}: {', '.join(filenames)} 외 {len(files)-3}개")
            else:
                summary.append(f"{label}: {', '.join(filenames)}")

    return summary


def update_current_context(work_summary: list):
    """CURRENT_CONTEXT.md 자동 업데이트"""
    context_file = MEMORY_PATH / 'CURRENT_CONTEXT.md'

    if not context_file.exists():
        return

    try:
        with open(context_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return

    if not work_summary:
        return

    # 현재 날짜
    today = datetime.now().strftime('%Y-%m-%d')
    timestamp = datetime.now().strftime('%H:%M')

    # "최근 완료된 작업" 섹션 찾기
    section_pattern = r'(## 최근 완료된 작업.*?)(##|\Z)'
    match = re.search(section_pattern, content, re.DOTALL)

    if not match:
        return

    section = match.group(1)

    # 오늘 날짜 섹션이 있는지 확인
    today_header = f"### 이번 세션 ({today})"

    # 새로운 작업 항목 생성
    new_items = [f"- [{timestamp}] {item}" for item in work_summary]
    new_items_text = '\n'.join(new_items)

    if today_header in section:
        # 기존 오늘 섹션에 추가
        updated_section = section.replace(
            today_header,
            f"{today_header}\n{new_items_text}"
        )
    else:
        # 새 오늘 섹션 생성
        section_lines = section.strip().split('\n')
        header = section_lines[0]  # "## 최근 완료된 작업"
        rest = '\n'.join(section_lines[1:])

        updated_section = f"{header}\n\n{today_header}\n{new_items_text}\n{rest}\n"

    # 컨텐츠 업데이트
    updated_content = content.replace(section, updated_section)

    # 마지막 업데이트 시간 갱신
    updated_content = re.sub(
        r'> 마지막 업데이트: .*',
        f'> 마지막 업데이트: {today} {timestamp} (자동)',
        updated_content
    )

    try:
        with open(context_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
    except Exception:
        pass


def update_session_stats(stop_reason: str):
    """세션 통계 업데이트"""
    stats_file = STATE_PATH / 'session_stats.json'
    stats = load_json(stats_file)
    if not isinstance(stats, dict):
        stats = {}

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
    if not isinstance(worktree, dict):
        worktree = {}

    # 세션 변경 사항 가져오기
    session_changes = get_session_changes()
    categories = categorize_changes(session_changes)
    work_summary = generate_work_summary(categories)

    checkpoint = {
        'timestamp': datetime.now().isoformat(),
        'current_task': worktree.get('current_task', ''),
        'progress': worktree.get('progress', {}),
        'session_work': work_summary,  # 세션 작업 요약 추가
        'files_changed': len(session_changes),
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


def clear_processed_changes():
    """처리된 변경 사항 플래그 설정"""
    processed_file = STATE_PATH / 'last_processed.json'
    save_json(processed_file, {
        'timestamp': datetime.now().isoformat(),
        'processed': True
    })


def main():
    """
    메인 함수 - Hook Entry Point

    Stop 이벤트에서 호출됩니다.
    완전 자동화: 사용자 개입 없이 작업 내용 자동 기록
    """
    try:
        input_data = json.load(sys.stdin)
        stop_reason = input_data.get('stop_reason', 'unknown')

        # 1. 세션 변경 사항 분석
        session_changes = get_session_changes()

        if session_changes:
            # 2. 카테고리별 분류
            categories = categorize_changes(session_changes)

            # 3. 작업 요약 생성
            work_summary = generate_work_summary(categories)

            # 4. CURRENT_CONTEXT.md 자동 업데이트
            if work_summary:
                update_current_context(work_summary)

        # 5. 세션 통계 업데이트
        update_session_stats(stop_reason)

        # 6. 체크포인트 생성
        create_checkpoint()

        # 7. 이벤트 로깅
        log_stop_event(stop_reason)

    except Exception as e:
        # 에러 로깅 (디버그용)
        try:
            error_log = STATE_PATH / 'hook_errors.log'
            with open(error_log, 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.now().isoformat()}] session_stop error: {e}\n")
        except Exception:
            pass


if __name__ == '__main__':
    main()
