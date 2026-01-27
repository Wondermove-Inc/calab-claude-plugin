#!/usr/bin/env python3
"""
PostToolUse Hook: Worktree 자동 업데이트

트리거: Edit 또는 Write 도구 사용 후
동작:
  1. 소스 코드 파일 변경 감지
  2. worktree.json의 current_task status를 in_progress로 자동 변경
  3. started_at 시간 자동 기록
"""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path


logger = logging.getLogger(__name__)


def get_project_root() -> Path:
    """프로젝트 루트 경로 반환"""
    project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '')
    if project_dir:
        return Path(project_dir)
    return Path(__file__).parent.parent.parent


PROJECT_ROOT = get_project_root()
STATE_DIR = PROJECT_ROOT / '.claude-state'
WORKTREE_FILE = STATE_DIR / 'worktree.json'


# 소스 코드로 간주할 확장자들
SOURCE_EXTENSIONS = {
    '.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs',
    '.py', '.java', '.go', '.rs', '.rb', '.php',
    '.c', '.cpp', '.h', '.hpp', '.cs', '.swift',
    '.kt', '.scala', '.vue', '.svelte'
}

# 무시할 경로 패턴
IGNORE_PATTERNS = [
    '.claude/',
    '.claude-state/',
    'node_modules/',
    '.git/',
    '__pycache__/',
    '.next/',
    'dist/',
    'build/'
]


def load_json(path: Path) -> dict:
    """JSON 파일 로드"""
    if not path.exists():
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.debug(f"JSON 로드 실패: {path}: {e}")
        return {}


def save_json(path: Path, data: dict) -> None:
    """JSON 파일 저장"""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.debug(f"JSON 저장 실패: {path}: {e}")


def is_source_file(file_path: str) -> bool:
    """소스 코드 파일인지 확인"""
    path = Path(file_path)
    return path.suffix.lower() in SOURCE_EXTENSIONS


def should_ignore(file_path: str) -> bool:
    """무시해야 할 파일인지 확인"""
    return any(pattern in file_path for pattern in IGNORE_PATTERNS)


def find_task_in_worktree(
    worktree: dict,
    task_id: str
) -> tuple[int | None, int | None, int | None, dict | None]:
    """
    worktree에서 특정 task를 찾아 반환

    Returns:
        (epic_idx, story_idx, task_idx, task_obj) or (None, None, None, None)
    """
    epics = worktree.get('epics', [])
    for e_idx, epic in enumerate(epics):
        stories = epic.get('stories', [])
        for s_idx, story in enumerate(stories):
            tasks = story.get('tasks', [])
            for t_idx, task in enumerate(tasks):
                if task.get('id') == task_id:
                    return (e_idx, s_idx, t_idx, task)
    return (None, None, None, None)


def update_worktree_status(worktree: dict, task_id: str) -> bool:
    """
    worktree의 current_task status를 in_progress로 변경

    Returns:
        True if updated, False otherwise
    """
    e_idx, s_idx, t_idx, task = find_task_in_worktree(worktree, task_id)

    if task is None:
        return False

    current_status = task.get('status', 'pending')

    # 이미 in_progress 또는 done이면 변경하지 않음
    if current_status in ('in_progress', 'done'):
        return False

    # status를 in_progress로 변경
    worktree['epics'][e_idx]['stories'][s_idx]['tasks'][t_idx]['status'] = 'in_progress'
    worktree['epics'][e_idx]['stories'][s_idx]['tasks'][t_idx]['started_at'] = datetime.now().isoformat()

    # progress 업데이트
    update_progress(worktree)

    return True


def update_progress(worktree: dict) -> None:
    """progress 필드 재계산"""
    total = 0
    done = 0
    in_progress = 0
    blocked = 0
    pending = 0

    for epic in worktree.get('epics', []):
        for story in epic.get('stories', []):
            for task in story.get('tasks', []):
                total += 1
                status = task.get('status', 'pending')
                if status == 'done':
                    done += 1
                elif status == 'in_progress':
                    in_progress += 1
                elif status == 'blocked':
                    blocked += 1
                else:
                    pending += 1

    percentage = round((done / total) * 100) if total > 0 else 0

    worktree['progress'] = {
        'total': total,
        'done': done,
        'in_progress': in_progress,
        'blocked': blocked,
        'pending': pending,
        'percentage': percentage
    }


def main() -> None:
    """메인 함수 - Hook Entry Point"""
    try:
        input_data = json.load(sys.stdin)
    except Exception as e:
        logger.debug(f"stdin 파싱 실패: {e}")
        print("Success")
        return

    # 파일 경로 추출
    tool_input = input_data.get('tool_input', {})
    file_path = tool_input.get('file_path', '')

    if not file_path:
        print("Success")
        return

    # 무시할 파일인지 확인
    if should_ignore(file_path):
        print("Success")
        return

    # 소스 코드 파일인지 확인
    if not is_source_file(file_path):
        print("Success")
        return

    # worktree.json 확인
    if not WORKTREE_FILE.exists():
        print("Success")
        return

    worktree = load_json(WORKTREE_FILE)
    if not worktree:
        print("Success")
        return

    # current_task 확인
    current_task = worktree.get('current_task', '')
    if not current_task:
        print("Success")
        return

    # status 업데이트
    updated = update_worktree_status(worktree, current_task)

    if updated:
        save_json(WORKTREE_FILE, worktree)

    print("Success")


if __name__ == "__main__":
    main()
