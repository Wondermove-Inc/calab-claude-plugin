---
name: workflow:jira-init
description: JIRA 연동 초기 설정을 수행합니다.
allowed-tools: Read, Write, Edit, Bash
user-invocable: true
---
# /jira-init

JIRA 연동을 초기화하고 연결을 설정합니다.

## 사용법

```bash
/jira-init AUTH
/jira-init AUTH --url https://company.atlassian.net
```

## 실행 프로토콜

### Step 1: 환경변수 확인

다음 환경변수가 설정되어 있는지 확인:

```bash
echo $JIRA_EMAIL
echo $JIRA_API_TOKEN
```

**설정 안내 (없는 경우):**
```bash
# .bashrc 또는 .zshrc에 추가
export JIRA_EMAIL='your-email@company.com'
export JIRA_API_TOKEN='your-api-token'

# API 토큰 생성: https://id.atlassian.com/manage-profile/security/api-tokens
```

### Step 2: 설정 파일 업데이트

`.claude/integrations/jira_config.json` 업데이트:

```json
{
  "jira": {
    "enabled": true,
    "base_url": "<입력받은 URL>",
    "project_key": "<입력받은 프로젝트 키>",
    ...
  }
}
```

### Step 3: 연결 테스트

```python
from jira_connector import JiraConnector, load_config

config = load_config()
connector = JiraConnector(config)
result = connector.test_connection()
```

### Step 4: 프로젝트 검증

```python
project = connector.get_project()
print(f"프로젝트: {project['name']}")
print(f"이슈 타입: {[it['name'] for it in project['issueTypes']]}")
```

### Step 5: 매핑 파일 초기화

`.claude-state/jira_mapping.json` 초기화:

```json
{
  "project_key": "<프로젝트 키>",
  "base_url": "<JIRA URL>",
  "mappings": {},
  "reverse_mappings": {},
  "last_sync": null,
  "sync_history": []
}
```

## 출력 형식

```
============================================
 JIRA 연동 초기화
============================================

 설정:
 • URL: https://company.atlassian.net
 • 프로젝트: AUTH (Authentication System)
 • 사용자: 홍길동 (hong@company.com)

 연결 테스트: ✅ 성공

 사용 가능한 이슈 타입:
 • Epic
 • Story
 • Task
 • Sub-task
 • Bug

 생성된 파일:
 • .claude/integrations/jira_config.json (업데이트)
 • .claude-state/jira_mapping.json (초기화)

 다음 단계:
 • /jira-push - 현재 Worktree를 JIRA에 생성
 • /jira-status - 연동 상태 확인
============================================
```

## 에러 처리

| 에러 | 원인 | 해결 |
|------|------|------|
| 인증 실패 | API 토큰 오류 | 토큰 재생성 |
| 프로젝트 없음 | 잘못된 키 | 프로젝트 키 확인 |
| 권한 없음 | 접근 권한 부족 | JIRA 관리자 문의 |

## 연계 명령어

- `/jira-push` - Worktree → JIRA 동기화
- `/jira-status` - 연동 상태 확인
