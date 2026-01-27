---
name: workflow:jira-pull
description: JIRA 변경사항을 Worktree로 가져옵니다 (Pull).
allowed-tools: Read, Write, Edit, Bash
user-invocable: true
---
# /jira-pull

JIRA의 변경사항을 Worktree로 동기화합니다.

## 사용법

```bash
/jira-pull           # 변경된 항목만 동기화
/jira-pull --force   # 전체 강제 동기화
```

## 사전 조건

- `/jira-init` 완료
- `/jira-push` 로 최초 동기화 완료
- 매핑 정보 존재 (`jira_mapping.json`)

## 실행 프로토콜

### Step 1: 매핑된 이슈 조회

```python
from jira_connector import JiraConnector, load_config, load_mapping

config = load_config()
mapping = load_mapping()
connector = JiraConnector(config)

# 매핑된 JIRA 키 목록
jira_keys = list(mapping['mappings'].values())
```

### Step 2: JIRA 이슈 상태 조회

```python
for jira_key in jira_keys:
    issue = connector.get_issue(
        jira_key,
        fields=['status', 'summary', 'assignee', 'priority']
    )

    status = issue['fields']['status']['name']
    assignee = issue['fields'].get('assignee', {})
```

### Step 3: Worktree 상태 업데이트

```python
# JIRA 상태 → Worktree 상태 매핑 (역방향)
reverse_status_mapping = {
    'To Do': 'pending',
    'In Progress': 'in_progress',
    'Done': 'done',
    'Blocked': 'blocked'
}

# Worktree 업데이트
worktree_status = reverse_status_mapping.get(jira_status, 'pending')
task['status'] = worktree_status
```

### Step 4: Worktree 저장

```python
# worktree.json 업데이트
save_worktree(worktree)

# 매핑 타임스탬프 업데이트
mapping['last_sync'] = datetime.now().isoformat()
save_mapping(mapping)
```

## 출력 형식

```
============================================
 JIRA 동기화 (Pull)
============================================

 JIRA → Worktree:

 변경 감지:
 🔄 AUTH-102 (TASK-001): To Do → In Progress
    └─ 담당자: 홍길동
 🔄 AUTH-103 (TASK-002): In Progress → Done
 🔄 AUTH-106 (TASK-005): - → Blocked
    └─ 블로커 코멘트 추가됨

 업데이트 완료:
 • TASK-001 상태: in_progress
 • TASK-002 상태: done
 • TASK-005 상태: blocked

 요약:
 • 업데이트: 3개
 • 변경 없음: 5개

============================================
```

## 동기화 충돌 처리

JIRA와 Worktree 상태가 다른 경우:

```
============================================
 충돌 감지
============================================

 TASK-003:
 • Worktree: in_progress (로컬)
 • JIRA: Done (AUTH-104)

 선택:
 1. JIRA 우선 (Pull) - Worktree를 Done으로 변경
 2. Worktree 우선 (Push) - JIRA를 In Progress로 변경
 3. 스킵 - 수동 해결

============================================
```

## 연계 동작

- 관리자가 JIRA에서 우선순위/담당자 변경 시 반영
- JIRA에서 직접 상태 변경 시 Worktree 동기화

## 다음 단계

- `/jira-sync` - 양방향 동기화
- `/worktree status` - 동기화 결과 확인
