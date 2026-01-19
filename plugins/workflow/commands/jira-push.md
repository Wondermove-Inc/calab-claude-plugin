---
description: Worktree 상태를 JIRA로 동기화합니다 (Push).
allowed-tools: Read, Write, Edit, Bash
argument-hint: [--force] [--dry-run]
---

# /jira-push

현재 Worktree 상태를 JIRA로 동기화합니다.

## 사용법

```bash
/jira-push              # 변경된 항목만 동기화
/jira-push --force      # 전체 강제 동기화
/jira-push --dry-run    # 실제 실행 없이 미리보기
```

## 사전 조건

- `/jira-init` 완료
- `worktree.json`에 데이터 존재
- 환경변수 설정 (`JIRA_EMAIL`, `JIRA_API_TOKEN`)

## 실행 프로토콜

### Step 1: 설정 및 매핑 로드

```python
from jira_connector import (
    JiraConnector, load_config, load_mapping,
    load_worktree, save_mapping
)

config = load_config()
mapping = load_mapping()
worktree = load_worktree()

connector = JiraConnector(config)
```

### Step 2: Worktree 분석

Worktree 구조 파싱:
- Epic 목록
- Story 목록 (Epic 하위)
- Task 목록 (Story 하위)

### Step 3: JIRA 동기화

**새 항목**: JIRA 이슈 생성
```python
# Epic 생성
epic_result = connector.create_issue(
    issue_type='Epic',
    summary=epic['title'],
    description=epic.get('description', '')
)

# Story 생성 (parent로 Epic 연결)
story_result = connector.create_issue(
    issue_type='Story',
    summary=story['title'],
    parent_key=epic_result['key']  # 2025 API: parent 필드 사용
)

# Task 생성 (parent로 Story 연결)
task_result = connector.create_issue(
    issue_type='Task',
    summary=task['title'],
    parent_key=story_result['key']
)
```

**기존 항목**: 상태 업데이트
```python
# 매핑에서 JIRA 키 조회
jira_key = mapping['mappings'].get(task_id)

# 상태 동기화
if task['status'] == 'in_progress':
    connector.transition_issue(jira_key, 'In Progress')
elif task['status'] == 'done':
    connector.transition_issue(jira_key, 'Done')
elif task['status'] == 'blocked':
    connector.transition_issue(jira_key, 'Blocked')
    connector.add_comment(jira_key, f"🚫 블로커: {task.get('blocker', '')}")
```

### Step 4: 매핑 저장

```python
# 새로 생성된 매핑 추가
mapping['mappings'][worktree_id] = jira_key
mapping['reverse_mappings'][jira_key] = worktree_id
mapping['last_sync'] = datetime.now().isoformat()

save_mapping(mapping)
```

## 출력 형식

```
============================================
 JIRA 동기화 (Push)
============================================

 Worktree → JIRA:

 Epic:
 ✅ EPIC-001 → AUTH-100 (생성됨)

 Story:
 ✅ STORY-001 → AUTH-101 (생성됨)
 ✅ STORY-002 → AUTH-105 (생성됨)

 Task:
 ✅ TASK-001 → AUTH-102 (상태: In Progress)
 ✅ TASK-002 → AUTH-103 (상태: Done)
 ✅ TASK-003 → AUTH-104 (생성됨)
 ⏭️ TASK-004 (변경 없음)

 요약:
 • 생성: 5개
 • 업데이트: 2개
 • 스킵: 1개
 • 에러: 0개

 JIRA 대시보드:
 https://company.atlassian.net/browse/AUTH

============================================
```

## --dry-run 출력

```
============================================
 JIRA 동기화 미리보기 (Dry Run)
============================================

 실행 예정 작업:

 [CREATE] Epic "사용자 인증" → Epic 생성
 [CREATE] Story "회원가입" → Story 생성 (parent: Epic)
 [CREATE] Task "User 엔티티" → Task 생성 (parent: Story)
 [UPDATE] TASK-001 → AUTH-102 상태 변경: In Progress

 총 4개 작업 예정

 실제 실행: /jira-push
============================================
```

## 연계 동작

- `/dev tasks` 완료 후 자동 호출 가능 (설정 시)
- `/worktree done` 실행 시 자동 상태 동기화 (훅)

## 다음 단계

- `/jira-status` - 동기화 결과 확인
- `/jira-pull` - JIRA 변경사항 가져오기
