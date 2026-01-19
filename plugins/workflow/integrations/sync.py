#!/usr/bin/env python3
"""
JIRA Worktree 동기화 모듈

Worktree 구조 ↔ JIRA 이슈 간 양방향 동기화를 담당합니다.
"""

import logging

from .connector import JiraConnector, JiraConnectorError, JiraAPIError


logger = logging.getLogger(__name__)


class WorktreeSyncMixin:
    """
    JiraConnector에 Worktree 동기화 기능을 추가하는 Mixin

    사용법:
        class JiraConnectorWithSync(JiraConnector, WorktreeSyncMixin):
            pass
    """

    def sync_from_worktree(
        self: JiraConnector,
        worktree: dict,
        mapping: dict
    ) -> dict:
        """
        Worktree에서 JIRA로 동기화

        Args:
            worktree: worktree.json 내용
            mapping: jira_mapping.json 내용

        Returns:
            동기화 결과 {'created', 'updated', 'errors'}
        """
        results = {
            'created': [],
            'updated': [],
            'errors': [],
            'mappings': mapping.get('mappings', {}).copy()
        }

        epics = worktree.get('epics', [])

        for epic in epics:
            try:
                # Epic 생성/업데이트
                epic_result = self._sync_epic(epic, results['mappings'])
                if epic_result.get('created'):
                    results['created'].append(epic_result)
                elif epic_result.get('updated'):
                    results['updated'].append(epic_result)

                # Story 처리
                for story in epic.get('stories', []):
                    story_result = self._sync_story(
                        story,
                        epic_result.get('jira_key'),
                        results['mappings']
                    )
                    if story_result.get('created'):
                        results['created'].append(story_result)
                    elif story_result.get('updated'):
                        results['updated'].append(story_result)

                    # Task 처리
                    for task in story.get('tasks', []):
                        task_result = self._sync_task(
                            task,
                            story_result.get('jira_key'),
                            results['mappings']
                        )
                        if task_result.get('created'):
                            results['created'].append(task_result)
                        elif task_result.get('updated'):
                            results['updated'].append(task_result)

            except JiraConnectorError as e:
                results['errors'].append({
                    'item': epic.get('id', 'unknown'),
                    'error': str(e)
                })

        return results

    def _sync_epic(self: JiraConnector, epic: dict, mappings: dict) -> dict:
        """Epic 동기화"""
        epic_id = epic.get('id')
        jira_key = mappings.get(epic_id)

        if jira_key:
            # 기존 이슈 업데이트
            self.update_issue(
                jira_key,
                summary=epic.get('title')
            )
            return {'updated': True, 'worktree_id': epic_id, 'jira_key': jira_key}
        else:
            # 새 이슈 생성
            result = self.create_issue(
                issue_type=self.issue_types.get('epic', 'Epic'),
                summary=epic.get('title', 'Epic'),
                description=epic.get('description', '')
            )
            jira_key = result['key']
            mappings[epic_id] = jira_key
            return {'created': True, 'worktree_id': epic_id, 'jira_key': jira_key}

    def _sync_story(
        self: JiraConnector,
        story: dict,
        epic_key: str | None,
        mappings: dict
    ) -> dict:
        """Story 동기화"""
        story_id = story.get('id')
        jira_key = mappings.get(story_id)

        if jira_key:
            self.update_issue(jira_key, summary=story.get('title'))
            return {'updated': True, 'worktree_id': story_id, 'jira_key': jira_key}
        else:
            result = self.create_issue(
                issue_type=self.issue_types.get('story', 'Story'),
                summary=story.get('title', 'Story'),
                description=story.get('description', ''),
                parent_key=epic_key
            )
            jira_key = result['key']
            mappings[story_id] = jira_key
            return {'created': True, 'worktree_id': story_id, 'jira_key': jira_key}

    def _sync_task(
        self: JiraConnector,
        task: dict,
        story_key: str | None,
        mappings: dict
    ) -> dict:
        """Task 동기화"""
        task_id = task.get('id')
        jira_key = mappings.get(task_id)

        if jira_key:
            self.update_issue(jira_key, summary=task.get('title'))
            # 상태 동기화
            self._sync_task_status(task, jira_key)
            return {'updated': True, 'worktree_id': task_id, 'jira_key': jira_key}
        else:
            result = self.create_issue(
                issue_type=self.issue_types.get('task', 'Task'),
                summary=task.get('title', 'Task'),
                description=task.get('description', ''),
                parent_key=story_key
            )
            jira_key = result['key']
            mappings[task_id] = jira_key
            return {'created': True, 'worktree_id': task_id, 'jira_key': jira_key}

    def _sync_task_status(self: JiraConnector, task: dict, jira_key: str) -> None:
        """Task 상태 동기화"""
        worktree_status = task.get('status', 'pending')
        jira_status = self.status_mapping.get(worktree_status)

        if jira_status:
            try:
                self.transition_issue(jira_key, jira_status)
            except JiraAPIError as e:
                # 전환 불가능한 경우 로깅 후 계속 진행
                logger.debug(f"상태 전환 실패 (무시됨): {jira_key} -> {jira_status}: {e}")


class JiraConnectorWithSync(JiraConnector, WorktreeSyncMixin):
    """Worktree 동기화 기능이 포함된 JiraConnector"""
    pass
