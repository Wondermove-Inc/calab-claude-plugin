---
description: Worktree 항목과 JIRA 이슈를 수동으로 연결합니다.
allowed-tools: Read, Write, Edit
argument-hint: <worktree-id> <jira-key>
---

# /jira-link

Worktree 항목과 기존 JIRA 이슈를 수동으로 매핑합니다.

## 사용법

```bash
/jira-link TASK-001 AUTH-102
/jira-link STORY-001 AUTH-100
/jira-link --unlink TASK-001
/jira-link --list
```

## 사용 시나리오

1. **기존 JIRA 이슈 연결**: 이미 JIRA에 있는 이슈를 Worktree에 연결
2. **잘못된 매핑 수정**: 자동 매핑이 잘못된 경우 수동 수정
3. **매핑 해제**: 연결 해제 후 재연결

## 실행 프로토콜

### Step 1: 유효성 검증

```python
# Worktree ID 확인
worktree = load_worktree()
task = find_task_by_id(worktree, worktree_id)
if not task:
    raise Error(f"Worktree에서 '{worktree_id}'를 찾을 수 없습니다.")

# JIRA 이슈 확인
try:
    issue = connector.get_issue(jira_key)
except JiraAPIError:
    raise Error(f"JIRA 이슈 '{jira_key}'를 찾을 수 없습니다.")
```

### Step 2: 기존 매핑 확인

```python
mapping = load_mapping()

# 이미 매핑된 경우 경고
if worktree_id in mapping['mappings']:
    existing_key = mapping['mappings'][worktree_id]
    print(f"⚠️ {worktree_id}는 이미 {existing_key}에 매핑되어 있습니다.")
    print(f"덮어쓰시겠습니까? (y/n)")
```

### Step 3: 매핑 저장

```python
# 양방향 매핑 저장
mapping['mappings'][worktree_id] = jira_key
mapping['reverse_mappings'][jira_key] = worktree_id
mapping['last_sync'] = datetime.now().isoformat()

save_mapping(mapping)
```

## 출력 형식

### 연결 성공

```
============================================
 JIRA 매핑 완료
============================================

 연결됨:
 • Worktree: TASK-001 (User 엔티티 생성)
 • JIRA: AUTH-102 (User 엔티티 생성)

 JIRA 상태: In Progress
 Worktree 상태: in_progress

 ✅ 상태 일치

============================================
```

### 연결 해제

```bash
/jira-link --unlink TASK-001
```

```
============================================
 JIRA 매핑 해제
============================================

 해제됨:
 • TASK-001 ↔ AUTH-102 연결 해제

 ⚠️ 이후 /jira-push 시 새 이슈로 생성됩니다.

============================================
```

### 매핑 목록 조회

```bash
/jira-link --list
```

```
============================================
 JIRA 매핑 목록
============================================

 프로젝트: AUTH
 총 매핑: 8개

 Epic:
 • EPIC-001 ↔ AUTH-100

 Story:
 • STORY-001 ↔ AUTH-101
 • STORY-002 ↔ AUTH-105

 Task:
 • TASK-001 ↔ AUTH-102 (in_progress)
 • TASK-002 ↔ AUTH-103 (done)
 • TASK-003 ↔ AUTH-104 (pending)
 • TASK-004 ↔ AUTH-106 (pending)
 • TASK-005 ↔ AUTH-107 (blocked)

 마지막 동기화: 2025-12-30 10:00:00

============================================
```

## 에러 처리

| 에러 | 원인 | 해결 |
|------|------|------|
| Worktree ID 없음 | 잘못된 ID | `/worktree` 로 확인 |
| JIRA 이슈 없음 | 잘못된 키 | JIRA에서 이슈 키 확인 |
| 이미 매핑됨 | 중복 매핑 | `--unlink` 후 재매핑 |

## 연계 명령어

- `/worktree` - Worktree ID 확인
- `/jira-status` - 매핑 상태 확인
- `/jira-sync` - 동기화 실행
