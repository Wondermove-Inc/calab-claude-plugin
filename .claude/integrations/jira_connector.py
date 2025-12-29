#!/usr/bin/env python3
"""
JIRA REST API 커넥터 (2025년 최신 API 기준)

주요 특징:
- REST API v3 사용
- /rest/api/3/search/jql 사용 (기존 /search deprecated)
- parent 필드 사용 (epic-link deprecated)
- ADF(Atlassian Document Format) 지원

환경변수:
- JIRA_EMAIL: Atlassian 계정 이메일
- JIRA_API_TOKEN: API 토큰

사용법:
    from jira_connector import JiraConnector

    connector = JiraConnector(config)
    connector.create_issue('Task', 'Summary', parent_key='PROJ-1')
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

# requests 라이브러리 체크
try:
    import requests
    from requests.auth import HTTPBasicAuth
except ImportError:
    print("Error: requests 라이브러리가 필요합니다.")
    print("설치: pip install requests")
    sys.exit(1)


class JiraConnectorError(Exception):
    """JIRA 커넥터 에러"""
    pass


class JiraAuthError(JiraConnectorError):
    """인증 에러"""
    pass


class JiraAPIError(JiraConnectorError):
    """API 호출 에러"""
    pass


class JiraConnector:
    """
    JIRA Cloud REST API v3 커넥터

    2025년 최신 API 기준:
    - parent 필드로 계층 구조 설정 (epic-link deprecated)
    - /search/jql 엔드포인트 사용 (/search deprecated)
    - ADF 형식 description 지원
    """

    API_VERSION = "3"

    def __init__(self, config: dict):
        """
        커넥터 초기화

        Args:
            config: jira_config.json 내용
        """
        jira_config = config.get('jira', config)

        self.base_url = jira_config.get('base_url', '').rstrip('/')
        self.project_key = jira_config.get('project_key', '')
        self.api_version = jira_config.get('api_version', self.API_VERSION)
        self.issue_types = jira_config.get('issue_types', {})
        self.status_mapping = jira_config.get('status_mapping', {})

        # 환경변수에서 인증 정보 로드
        self.email = os.environ.get('JIRA_EMAIL', '')
        self.api_token = os.environ.get('JIRA_API_TOKEN', '')

        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def _api_url(self, endpoint: str) -> str:
        """API URL 생성"""
        return f'{self.base_url}/rest/api/{self.api_version}/{endpoint}'

    def _get_auth(self) -> HTTPBasicAuth:
        """Basic Auth 객체 반환"""
        if not self.email or not self.api_token:
            raise JiraAuthError(
                "JIRA 인증 정보가 없습니다.\n"
                "환경변수를 설정하세요:\n"
                "  export JIRA_EMAIL='your-email@company.com'\n"
                "  export JIRA_API_TOKEN='your-api-token'"
            )
        return HTTPBasicAuth(self.email, self.api_token)

    def _handle_response(self, response: requests.Response, action: str) -> dict:
        """응답 처리 및 에러 핸들링"""
        if response.status_code == 401:
            raise JiraAuthError("인증 실패: 이메일 또는 API 토큰을 확인하세요.")

        if response.status_code == 403:
            raise JiraAuthError("권한 없음: 해당 프로젝트에 대한 권한이 없습니다.")

        if response.status_code == 404:
            raise JiraAPIError(f"{action} 실패: 리소스를 찾을 수 없습니다.")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('errorMessages', [])
                errors = error_data.get('errors', {})
                raise JiraAPIError(
                    f"{action} 실패 ({response.status_code}): "
                    f"{error_msg or errors}"
                )
            except json.JSONDecodeError:
                raise JiraAPIError(
                    f"{action} 실패 ({response.status_code}): {response.text}"
                )

        # 204 No Content는 빈 dict 반환
        if response.status_code == 204:
            return {}

        try:
            return response.json()
        except json.JSONDecodeError:
            return {}

    def _to_adf(self, text: str) -> dict:
        """
        텍스트를 ADF(Atlassian Document Format)로 변환

        Args:
            text: 일반 텍스트

        Returns:
            ADF 형식 dict
        """
        if not text:
            return None

        # 줄바꿈 처리
        paragraphs = []
        for line in text.split('\n'):
            if line.strip():
                paragraphs.append({
                    'type': 'paragraph',
                    'content': [{'type': 'text', 'text': line}]
                })
            else:
                # 빈 줄은 빈 paragraph
                paragraphs.append({
                    'type': 'paragraph',
                    'content': []
                })

        return {
            'type': 'doc',
            'version': 1,
            'content': paragraphs if paragraphs else [{
                'type': 'paragraph',
                'content': [{'type': 'text', 'text': text}]
            }]
        }

    # ==================== 연결 테스트 ====================

    def test_connection(self) -> dict:
        """
        연결 테스트

        Returns:
            사용자 정보 dict (성공 시)
        """
        try:
            response = requests.get(
                self._api_url('myself'),
                auth=self._get_auth(),
                headers=self.headers,
                timeout=10
            )

            result = self._handle_response(response, '연결 테스트')
            return {
                'success': True,
                'user': result.get('displayName', ''),
                'email': result.get('emailAddress', ''),
                'account_id': result.get('accountId', '')
            }
        except JiraConnectorError as e:
            return {'success': False, 'error': str(e)}
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': f'네트워크 오류: {e}'}

    def get_project(self, project_key: str = None) -> dict:
        """프로젝트 정보 조회"""
        key = project_key or self.project_key

        response = requests.get(
            self._api_url(f'project/{key}'),
            auth=self._get_auth(),
            headers=self.headers
        )

        return self._handle_response(response, '프로젝트 조회')

    # ==================== 이슈 CRUD ====================

    def create_issue(
        self,
        issue_type: str,
        summary: str,
        description: str = '',
        parent_key: str = None,
        labels: List[str] = None,
        assignee_id: str = None,
        custom_fields: dict = None
    ) -> dict:
        """
        이슈 생성 (2025 API 기준)

        Args:
            issue_type: 이슈 타입 (Epic, Story, Task, Sub-task)
            summary: 제목
            description: 설명 (자동으로 ADF 변환)
            parent_key: 부모 이슈 키 (epic-link 대신 parent 사용)
            labels: 라벨 목록
            assignee_id: 담당자 account ID
            custom_fields: 커스텀 필드 dict

        Returns:
            생성된 이슈 정보 {'id', 'key', 'self'}
        """
        fields = {
            'project': {'key': self.project_key},
            'summary': summary,
            'issuetype': {'name': issue_type}
        }

        # Description (ADF 형식)
        if description:
            fields['description'] = self._to_adf(description)

        # Parent 연결 (2025: epic-link 대신 parent 사용)
        if parent_key:
            fields['parent'] = {'key': parent_key}

        # 라벨
        if labels:
            fields['labels'] = labels

        # 담당자
        if assignee_id:
            fields['assignee'] = {'accountId': assignee_id}

        # 커스텀 필드
        if custom_fields:
            fields.update(custom_fields)

        payload = {'fields': fields}

        response = requests.post(
            self._api_url('issue'),
            json=payload,
            auth=self._get_auth(),
            headers=self.headers
        )

        return self._handle_response(response, '이슈 생성')

    def get_issue(
        self,
        issue_key: str,
        fields: List[str] = None,
        expand: List[str] = None
    ) -> dict:
        """
        이슈 조회

        Args:
            issue_key: 이슈 키 (예: PROJ-123)
            fields: 조회할 필드 목록
            expand: 확장할 정보 (changelog, transitions 등)
        """
        params = {}
        if fields:
            params['fields'] = ','.join(fields)
        if expand:
            params['expand'] = ','.join(expand)

        response = requests.get(
            self._api_url(f'issue/{issue_key}'),
            params=params,
            auth=self._get_auth(),
            headers=self.headers
        )

        return self._handle_response(response, '이슈 조회')

    def update_issue(
        self,
        issue_key: str,
        summary: str = None,
        description: str = None,
        labels: List[str] = None,
        custom_fields: dict = None
    ) -> bool:
        """
        이슈 업데이트

        Returns:
            성공 여부
        """
        fields = {}

        if summary:
            fields['summary'] = summary
        if description:
            fields['description'] = self._to_adf(description)
        if labels is not None:
            fields['labels'] = labels
        if custom_fields:
            fields.update(custom_fields)

        if not fields:
            return True  # 변경 사항 없음

        response = requests.put(
            self._api_url(f'issue/{issue_key}'),
            json={'fields': fields},
            auth=self._get_auth(),
            headers=self.headers
        )

        self._handle_response(response, '이슈 업데이트')
        return True

    # ==================== 상태 전환 ====================

    def get_transitions(self, issue_key: str) -> List[dict]:
        """
        가능한 상태 전환 조회

        Returns:
            전환 목록 [{'id', 'name', 'to': {'name', 'id'}}]
        """
        response = requests.get(
            self._api_url(f'issue/{issue_key}/transitions'),
            auth=self._get_auth(),
            headers=self.headers
        )

        result = self._handle_response(response, '전환 조회')
        return result.get('transitions', [])

    def transition_issue(
        self,
        issue_key: str,
        status_name: str,
        comment: str = None
    ) -> bool:
        """
        이슈 상태 전환

        Args:
            issue_key: 이슈 키
            status_name: 전환할 상태명 또는 전환명
            comment: 전환 시 추가할 코멘트

        Returns:
            성공 여부
        """
        transitions = self.get_transitions(issue_key)

        # 상태명 또는 전환명으로 매칭
        target = None
        status_lower = status_name.lower()

        for t in transitions:
            if (t['name'].lower() == status_lower or
                t.get('to', {}).get('name', '').lower() == status_lower):
                target = t
                break

        if not target:
            available = [f"{t['name']} -> {t.get('to', {}).get('name', '')}"
                        for t in transitions]
            raise JiraAPIError(
                f"전환 '{status_name}' 없음.\n"
                f"가능한 전환: {available}"
            )

        payload = {'transition': {'id': target['id']}}

        # 코멘트 추가 (전환 시)
        if comment:
            payload['update'] = {
                'comment': [{
                    'add': {
                        'body': self._to_adf(comment)
                    }
                }]
            }

        response = requests.post(
            self._api_url(f'issue/{issue_key}/transitions'),
            json=payload,
            auth=self._get_auth(),
            headers=self.headers
        )

        self._handle_response(response, '상태 전환')
        return True

    def get_status(self, issue_key: str) -> dict:
        """현재 상태 조회"""
        issue = self.get_issue(issue_key, fields=['status'])
        status = issue.get('fields', {}).get('status', {})
        return {
            'name': status.get('name', ''),
            'category': status.get('statusCategory', {}).get('name', '')
        }

    # ==================== 검색 (2025 신규 API) ====================

    def search_issues(
        self,
        jql: str,
        fields: List[str] = None,
        max_results: int = 50,
        start_at: int = 0
    ) -> List[dict]:
        """
        이슈 검색 (2025년 신규 API)

        주의: /rest/api/3/search는 2025.5.1부터 deprecated
              /rest/api/3/search/jql 사용

        Args:
            jql: JQL 쿼리
            fields: 조회할 필드
            max_results: 최대 결과 수
            start_at: 시작 위치
        """
        payload = {
            'jql': jql,
            'maxResults': max_results,
            'startAt': start_at,
            'fields': fields or ['summary', 'status', 'parent', 'issuetype', 'assignee']
        }

        response = requests.post(
            self._api_url('search/jql'),  # 2025 신규 엔드포인트
            json=payload,
            auth=self._get_auth(),
            headers=self.headers
        )

        result = self._handle_response(response, '이슈 검색')
        return result.get('issues', [])

    def get_project_issues(
        self,
        project_key: str = None,
        issue_type: str = None,
        status: str = None
    ) -> List[dict]:
        """프로젝트의 이슈 목록 조회"""
        key = project_key or self.project_key

        jql_parts = [f'project = {key}']
        if issue_type:
            jql_parts.append(f'issuetype = "{issue_type}"')
        if status:
            jql_parts.append(f'status = "{status}"')

        jql = ' AND '.join(jql_parts) + ' ORDER BY created DESC'

        return self.search_issues(jql)

    # ==================== 코멘트 ====================

    def add_comment(self, issue_key: str, comment: str) -> dict:
        """
        코멘트 추가 (ADF 형식)

        Args:
            issue_key: 이슈 키
            comment: 코멘트 내용
        """
        payload = {
            'body': self._to_adf(comment)
        }

        response = requests.post(
            self._api_url(f'issue/{issue_key}/comment'),
            json=payload,
            auth=self._get_auth(),
            headers=self.headers
        )

        return self._handle_response(response, '코멘트 추가')

    # ==================== Worktree 연동 ====================

    def sync_from_worktree(
        self,
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

    def _sync_epic(self, epic: dict, mappings: dict) -> dict:
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

    def _sync_story(self, story: dict, epic_key: str, mappings: dict) -> dict:
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

    def _sync_task(self, task: dict, story_key: str, mappings: dict) -> dict:
        """Task 동기화"""
        task_id = task.get('id')
        jira_key = mappings.get(task_id)

        if jira_key:
            self.update_issue(jira_key, summary=task.get('title'))
            # 상태 동기화
            worktree_status = task.get('status', 'pending')
            jira_status = self.status_mapping.get(worktree_status)
            if jira_status:
                try:
                    self.transition_issue(jira_key, jira_status)
                except JiraAPIError:
                    pass  # 전환 불가능한 경우 무시
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


# ==================== 유틸리티 함수 ====================

def load_config(config_path: str = None) -> dict:
    """설정 파일 로드"""
    if config_path is None:
        # 기본 경로
        project_root = Path(__file__).parent.parent.parent
        config_path = project_root / '.claude' / 'integrations' / 'jira_config.json'

    config_path = Path(config_path)

    if not config_path.exists():
        return {}

    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_mapping(mapping_path: str = None) -> dict:
    """매핑 파일 로드"""
    if mapping_path is None:
        project_root = Path(__file__).parent.parent.parent
        mapping_path = project_root / '.claude-state' / 'jira_mapping.json'

    mapping_path = Path(mapping_path)

    if not mapping_path.exists():
        return {
            'project_key': None,
            'base_url': None,
            'mappings': {},
            'reverse_mappings': {},
            'last_sync': None,
            'sync_history': []
        }

    with open(mapping_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_mapping(mapping: dict, mapping_path: str = None):
    """매핑 파일 저장"""
    if mapping_path is None:
        project_root = Path(__file__).parent.parent.parent
        mapping_path = project_root / '.claude-state' / 'jira_mapping.json'

    mapping_path = Path(mapping_path)
    mapping_path.parent.mkdir(parents=True, exist_ok=True)

    with open(mapping_path, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)


def load_worktree(worktree_path: str = None) -> dict:
    """Worktree 파일 로드"""
    if worktree_path is None:
        project_root = Path(__file__).parent.parent.parent
        worktree_path = project_root / '.claude-state' / 'worktree.json'

    worktree_path = Path(worktree_path)

    if not worktree_path.exists():
        return {}

    with open(worktree_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# ==================== CLI 테스트 ====================

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='JIRA Connector CLI')
    parser.add_argument('--test', action='store_true', help='연결 테스트')
    parser.add_argument('--url', help='JIRA Base URL')
    parser.add_argument('--project', help='프로젝트 키')

    args = parser.parse_args()

    if args.test:
        config = load_config()
        if args.url:
            config.setdefault('jira', {})['base_url'] = args.url
        if args.project:
            config.setdefault('jira', {})['project_key'] = args.project

        connector = JiraConnector(config)
        result = connector.test_connection()

        if result['success']:
            print(f"✅ 연결 성공!")
            print(f"   사용자: {result['user']}")
            print(f"   이메일: {result['email']}")
        else:
            print(f"❌ 연결 실패: {result['error']}")
