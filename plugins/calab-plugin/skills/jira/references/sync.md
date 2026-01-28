# /jira --sync - 양방향 동기화

> **Worktree ↔ JIRA 양방향 동기화**

## 실행 절차

### Step 1: 양쪽 상태 수집
- Worktree: worktree.json
- JIRA: 매핑된 모든 이슈 조회

### Step 2: 변경 감지

**비교 기준:**
- last_sync 타임스탬프
- 각 항목의 updated 타임스탬프

**변경 유형:**
| 유형 | 조건 |
|------|------|
| Push | Worktree만 변경 |
| Pull | JIRA만 변경 |
| Conflict | 양쪽 모두 변경 |
| New | Worktree에만 존재 |

### Step 3: 충돌 해결

```
⚠️ 충돌 발견: TASK-001
• Worktree: in_progress (01-15 10:30)
• JIRA: done (01-15 11:00)

선택:
[J] JIRA 우선
[W] Worktree 우선
[S] 개별 선택
```

### Step 4: 동기화 실행
- Push: Worktree → JIRA
- Pull: JIRA → Worktree
- Create: 새 항목 생성

### Step 5: 결과 저장
- worktree.json 업데이트
- jira_mapping.json last_sync 업데이트

### 옵션
- `--prefer-jira`: 충돌 시 JIRA 우선
- `--prefer-worktree`: 충돌 시 Worktree 우선

### 완료 보고
```
============================================
 JIRA SYNC 완료
============================================

 📊 동기화 결과:
 • Push: 3개
 • Pull: 2개
 • 충돌 해결: 1개
 • 새로 생성: 0개

============================================
```
