# /jira --push - Worktree → JIRA 동기화

> **Worktree 상태를 JIRA로 전송**

## 실행 절차

### Step 1: 설정 로드
- jira_config.json
- jira_mapping.json
- worktree.json

### Step 2: Worktree 분석
Epic → Story → Task 계층 파싱

### Step 3: JIRA 동기화

**새 항목:**
```bash
# Epic 생성
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"fields": {"project": {"key": "AUTH"}, "issuetype": {"name": "Epic"}, "summary": "..."}}' \
  $JIRA_URL/rest/api/3/issue

# Story/Task 생성 (parent_key로 계층 연결)
```

**기존 항목:**
```bash
# 상태 전환
curl -X POST \
  $JIRA_URL/rest/api/3/issue/{issueKey}/transitions \
  -d '{"transition": {"id": "21"}}'
```

### Step 4: 매핑 저장
```json
{
  "mappings": { "TASK-001": "AUTH-102" },
  "reverse_mappings": { "AUTH-102": "TASK-001" }
}
```

### 옵션
- `--force`: 전체 강제 동기화
- `--dry-run`: 미리보기 (실제 전송 안 함)

### 상태 매핑
| Worktree | JIRA |
|----------|------|
| pending | To Do |
| in_progress | In Progress |
| done | Done |
| blocked | Blocked (+ 코멘트) |
