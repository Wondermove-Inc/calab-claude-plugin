#!/usr/bin/env python3
"""
JIRA 자동 동기화 훅

트리거: worktree.json 변경 시
동작: JIRA 이슈 상태 자동 업데이트

환경변수:
- JIRA_EMAIL: Atlassian 계정 이메일
- JIRA_API_TOKEN: API 토큰
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent.parent.parent
INTEGRATIONS_PATH = PROJECT_ROOT / '.claude' / 'integrations'
STATE_PATH = PROJECT_ROOT / '.claude-state'

# 모듈 경로 추가
sys.path.insert(0, str(INTEGRATIONS_PATH))


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


def log_sync(message: str, level: str = 'INFO'):
    """동기화 로그 출력"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[JIRA-SYNC] [{level}] {timestamp} - {message}")


def is_jira_enabled() -> bool:
    """JIRA 연동 활성화 여부 확인"""
    config_path = INTEGRATIONS_PATH / 'jira_config.json'
    config = load_json(config_path)
    return config.get('jira', {}).get('enabled', False)


def get_auto_sync_settings() -> dict:
    """자동 동기화 설정 조회"""
    config_path = INTEGRATIONS_PATH / 'jira_config.json'
    config = load_json(config_path)
    return config.get('jira', {}).get('auto_sync', {})


def detect_changes(old_worktree: dict, new_worktree: dict) -> list:
    """
    Worktree 변경 감지

    Returns:
        변경 목록 [{'type': 'task_start|task_done|blocker', 'task_id': str, ...}]
    """
    changes = []

    def extract_tasks(worktree: dict) -> dict:
        """모든 태스크를 flat dict로 추출"""
        tasks = {}
        for epic in worktree.get('epics', []):
            for story in epic.get('stories', []):
                for task in story.get('tasks', []):
                    tasks[task.get('id')] = task
        return tasks

    old_tasks = extract_tasks(old_worktree)
    new_tasks = extract_tasks(new_worktree)

    # 상태 변경 감지
    for task_id, new_task in new_tasks.items():
        old_task = old_tasks.get(task_id, {})
        old_status = old_task.get('status', 'pending')
        new_status = new_task.get('status', 'pending')

        if old_status != new_status:
            # 상태 변경됨
            if new_status == 'in_progress':
                changes.append({
                    'type': 'task_start',
                    'task_id': task_id,
                    'task': new_task
                })
            elif new_status == 'done':
                changes.append({
                    'type': 'task_done',
                    'task_id': task_id,
                    'task': new_task
                })
            elif new_status == 'blocked':
                changes.append({
                    'type': 'blocker',
                    'task_id': task_id,
                    'task': new_task,
                    'reason': new_task.get('blocker', '')
                })

    return changes


def sync_to_jira(changes: list):
    """
    변경사항을 JIRA에 동기화

    Args:
        changes: 변경 목록
    """
    try:
        from jira_connector import JiraConnector, load_config, load_mapping, save_mapping
    except ImportError as e:
        log_sync(f"jira_connector 모듈 로드 실패: {e}", 'ERROR')
        return

    config = load_config(str(INTEGRATIONS_PATH / 'jira_config.json'))
    mapping = load_mapping(str(STATE_PATH / 'jira_mapping.json'))
    auto_sync = get_auto_sync_settings()

    if not config.get('jira', {}).get('enabled'):
        return

    # 환경변수 확인
    if not os.environ.get('JIRA_EMAIL') or not os.environ.get('JIRA_API_TOKEN'):
        log_sync("JIRA 인증 정보 없음. 환경변수를 설정하세요.", 'WARN')
        return

    connector = JiraConnector(config)
    status_mapping = config.get('jira', {}).get('status_mapping', {})

    for change in changes:
        change_type = change['type']
        task_id = change['task_id']
        jira_key = mapping.get('mappings', {}).get(task_id)

        if not jira_key:
            log_sync(f"JIRA 매핑 없음: {task_id}", 'WARN')
            continue

        try:
            if change_type == 'task_start' and auto_sync.get('on_task_start'):
                jira_status = status_mapping.get('in_progress', 'In Progress')
                connector.transition_issue(jira_key, jira_status)
                log_sync(f"✅ {task_id} → {jira_key}: {jira_status}")

            elif change_type == 'task_done' and auto_sync.get('on_task_done'):
                jira_status = status_mapping.get('done', 'Done')
                connector.transition_issue(jira_key, jira_status)
                log_sync(f"✅ {task_id} → {jira_key}: {jira_status}")

            elif change_type == 'blocker' and auto_sync.get('on_blocker'):
                jira_status = status_mapping.get('blocked', 'Blocked')
                reason = change.get('reason', '블로커 발생')

                try:
                    connector.transition_issue(jira_key, jira_status)
                except Exception:
                    pass  # Blocked 상태 전환 불가능한 워크플로우

                connector.add_comment(
                    jira_key,
                    f"🚫 블로커 발생\n\n사유: {reason}\n\n(Claude Code에서 자동 동기화)"
                )
                log_sync(f"🚫 {task_id} → {jira_key}: 블로커 등록")

        except Exception as e:
            log_sync(f"동기화 실패 ({task_id}): {e}", 'ERROR')

    # 동기화 시간 업데이트
    mapping['last_sync'] = datetime.now().isoformat()
    save_mapping(mapping, str(STATE_PATH / 'jira_mapping.json'))


def main():
    """
    메인 함수 - Hook Entry Point

    이 훅은 worktree.json 파일 변경 시 호출됩니다.
    PostToolUse 이벤트에서 Edit/Write 도구가 worktree.json을 수정할 때 트리거됩니다.
    """
    # JIRA 연동 활성화 확인
    if not is_jira_enabled():
        return

    # 자동 동기화 설정 확인
    auto_sync = get_auto_sync_settings()
    if not auto_sync.get('enabled'):
        return

    # worktree.json 로드
    worktree_path = STATE_PATH / 'worktree.json'
    worktree = load_json(worktree_path)

    # 이전 상태 로드 (캐시)
    cache_path = STATE_PATH / '.worktree_cache.json'
    old_worktree = load_json(cache_path)

    # 변경 감지
    changes = detect_changes(old_worktree, worktree)

    if changes:
        log_sync(f"변경 감지: {len(changes)}건")
        sync_to_jira(changes)

    # 현재 상태 캐시 저장
    save_json(cache_path, worktree)


if __name__ == '__main__':
    main()
