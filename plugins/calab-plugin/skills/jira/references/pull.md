# /jira --pull - JIRA → Worktree 동기화

> **JIRA 변경사항을 Worktree로 가져오기**

## 전제 조건
- /jira --init 완료
- /jira --push 로 초기 동기화 완료

## 실행 절차

### Step 1: 매핑된 이슈 조회
jira_mapping.json에서 매핑 목록 로드

### Step 2: JIRA 이슈 상태 조회
```bash
curl -u $JIRA_EMAIL:$JIRA_API_TOKEN \
  "$JIRA_URL/rest/api/3/issue/AUTH-102"
```

### Step 3: Worktree 상태 업데이트

**역방향 매핑:**
| JIRA | Worktree |
|------|----------|
| To Do | pending |
| In Progress | in_progress |
| Done | done |
| Blocked | blocked |

### Step 4: 충돌 감지
```
⚠️ 충돌 발견: TASK-001
• Worktree: in_progress
• JIRA: done

선택:
[1] JIRA 우선 (done 적용)
[2] Worktree 우선 (유지)
```

### Step 5: Worktree 저장

### 옵션
- `--force`: 전체 강제 동기화 (충돌 무시, JIRA 우선)
