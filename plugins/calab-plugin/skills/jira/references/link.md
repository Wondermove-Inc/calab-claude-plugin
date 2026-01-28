# /jira --link - 수동 매핑 관리

> **Worktree 항목과 JIRA 이슈 수동 연결**

## 사용법
```bash
/jira --link TASK-001 AUTH-102   # 연결
/jira --link --list              # 매핑 목록
/jira --link --unlink TASK-001   # 연결 해제
```

## 실행 절차

### 연결 모드 (기본)

**Step 1**: Worktree ID 유효성 검증
```
worktree.json에서 TASK-001 존재 확인
```

**Step 2**: JIRA 이슈 존재 확인
```bash
curl -u $JIRA_EMAIL:$JIRA_API_TOKEN \
  "$JIRA_URL/rest/api/3/issue/AUTH-102"
```

**Step 3**: 기존 매핑 확인
```
⚠️ TASK-001은 이미 AUTH-100에 매핑되어 있습니다.
덮어쓰시겠습니까? (Y/N)
```

**Step 4**: 양방향 매핑 저장
```json
{
  "mappings": { "TASK-001": "AUTH-102" },
  "reverse_mappings": { "AUTH-102": "TASK-001" }
}
```

### 목록 모드 (--list)
```
============================================
 JIRA MAPPINGS
============================================

 | Worktree | JIRA    | 상태 |
 |----------|---------|------|
 | TASK-001 | AUTH-102| 동기화됨 |
 | TASK-002 | AUTH-103| 동기화됨 |
 | TASK-003 | (없음)  | 미연결 |

============================================
```

### 연결 해제 모드 (--unlink)
- mappings에서 제거
- reverse_mappings에서 제거
