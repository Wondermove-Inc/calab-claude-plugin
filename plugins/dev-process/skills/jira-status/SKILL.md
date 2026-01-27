---
name: workflow:jira-status
description: JIRA 연동 상태를 확인합니다.
allowed-tools: Read, Bash
user-invocable: true
---
# /jira-status

JIRA 연동 상태와 동기화 정보를 확인합니다.

## 사용법

```bash
/jira-status             # 요약 상태
/jira-status --detailed  # 상세 정보
```

## 실행 프로토콜

### Step 1: 설정 로드

```python
config = load_config()
mapping = load_mapping()
worktree = load_worktree()

jira_config = config.get('jira', {})
enabled = jira_config.get('enabled', False)
```

### Step 2: 연결 상태 확인

```python
if enabled:
    connector = JiraConnector(config)
    connection = connector.test_connection()
```

### Step 3: 동기화 상태 분석

```python
# 매핑 통계
total_mappings = len(mapping.get('mappings', {}))

# Worktree 항목 수
worktree_items = count_worktree_items(worktree)

# 미동기화 항목
unsynced = worktree_items - total_mappings

# 마지막 동기화
last_sync = mapping.get('last_sync')
```

## 출력 형식

### 기본 출력

```
============================================
 JIRA 연동 상태
============================================

 연결 정보:
 • 상태: ✅ 연결됨
 • URL: https://company.atlassian.net
 • 프로젝트: AUTH (Authentication System)
 • 사용자: 홍길동 (hong@company.com)

 동기화 상태:
 • 총 매핑: 8개
 • Worktree 항목: 10개
 • 미동기화: 2개

 마지막 동기화: 2025-12-30 10:00:00 (30분 전)

 자동 동기화: ✅ 활성화
 • 태스크 시작 시: ✅
 • 태스크 완료 시: ✅
 • 블로커 등록 시: ✅

============================================
```

### 상세 출력 (--detailed)

```
============================================
 JIRA 연동 상태 (상세)
============================================

 연결 정보:
 • 상태: ✅ 연결됨
 • URL: https://company.atlassian.net
 • 프로젝트: AUTH
 • API 버전: v3

 매핑 상세:

 ┌─────────────┬─────────────┬─────────────┬──────────┐
 │ Worktree    │ JIRA        │ 상태        │ 동기화   │
 ├─────────────┼─────────────┼─────────────┼──────────┤
 │ EPIC-001    │ AUTH-100    │ -           │ ✅       │
 │ STORY-001   │ AUTH-101    │ -           │ ✅       │
 │ TASK-001    │ AUTH-102    │ in_progress │ ✅       │
 │ TASK-002    │ AUTH-103    │ done        │ ✅       │
 │ TASK-003    │ AUTH-104    │ pending     │ ⚠️ 불일치 │
 │ TASK-004    │ -           │ pending     │ ❌ 미동기화│
 └─────────────┴─────────────┴─────────────┴──────────┘

 상태 불일치 상세:
 • TASK-003: Worktree(pending) ≠ JIRA(In Progress)
   └─ 해결: /jira-sync 실행

 미동기화 항목:
 • TASK-004: User 폼 컴포넌트
   └─ 해결: /jira-push 실행

 동기화 히스토리:
 • 2025-12-30 10:00:00 - Push 3개, Pull 2개
 • 2025-12-29 18:00:00 - Push 5개, Pull 0개
 • 2025-12-29 14:00:00 - 초기 동기화 (8개 생성)

============================================
```

### 연결 안됨

```
============================================
 JIRA 연동 상태
============================================

 연결 정보:
 • 상태: ❌ 연결 안됨

 원인:
 • JIRA 연동이 비활성화되어 있습니다.

 해결 방법:
 1. /jira-init <project-key> 실행
 2. 환경변수 설정:
    export JIRA_EMAIL='your-email@company.com'
    export JIRA_API_TOKEN='your-api-token'

============================================
```

### 인증 실패

```
============================================
 JIRA 연동 상태
============================================

 연결 정보:
 • 상태: ❌ 인증 실패

 에러: 401 Unauthorized

 해결 방법:
 1. API 토큰 확인: https://id.atlassian.com/manage-profile/security/api-tokens
 2. 환경변수 재설정:
    export JIRA_API_TOKEN='new-token'
 3. 연결 테스트:
    /jira-init AUTH

============================================
```

## 연계 명령어

- `/jira-init` - 연동 초기화
- `/jira-sync` - 동기화 실행
- `/jira-link --list` - 매핑 목록
- `/worktree status` - Worktree 상태
