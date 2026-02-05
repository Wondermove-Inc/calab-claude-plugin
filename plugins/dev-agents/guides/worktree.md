# Git Worktree 격리 전략

> 이 문서는 Planner, Coder 에이전트가 참조합니다.

## 개요

복잡한 코드 변경 작업은 Git Worktree를 사용하여 메인 작업 디렉토리와 격리합니다.

## 디렉토리 구조

```
project/
├── tree/                    # Worktree 루트
│   ├── feature-xxx/         # 기능 A 작업
│   └── bugfix-yyy/          # 버그 B 작업
├── .git/
└── (메인 작업 디렉토리)
```

## 브랜치 네이밍

| 유형 | 브랜치명 | Worktree 경로 |
|------|----------|---------------|
| 새 기능 | `plan/feature-xxx` | `tree/feature-xxx/` |
| 버그 수정 | `plan/bugfix-xxx` | `tree/bugfix-xxx/` |
| 리팩토링 | `plan/refactor-xxx` | `tree/refactor-xxx/` |

## Worktree 적용 기준

| 작업 유형 | Worktree 사용 | 이유 |
|----------|--------------|------|
| 새 기능 구현 | ✓ | 격리 필요 |
| 버그 수정 (복잡) | ✓ | 롤백 용이 |
| 단순 수정 | ✗ | 오버헤드 |
| 문서 작업 | ✗ | 충돌 위험 낮음 |

## 명령어

### Worktree 생성
```bash
PLAN_NAME="feature-xxx"
git worktree add tree/${PLAN_NAME} -b plan/${PLAN_NAME}
cd tree/${PLAN_NAME}
```

### Worktree 내 작업
```bash
# 경로 확인
pwd  # tree/{작업명}/ 인지 확인
git branch  # plan/{작업명} 브랜치인지 확인

# 커밋
git add <files>
git commit -m "[type]: 설명"
```

### Worktree 정리 (성공 시)
```bash
cd /path/to/project
git worktree remove tree/${PLAN_NAME}
git merge plan/${PLAN_NAME}
git branch -d plan/${PLAN_NAME}
```

### Worktree 정리 (실패/롤백 시)
```bash
git worktree remove --force tree/${PLAN_NAME}
git branch -D plan/${PLAN_NAME}
```

## 고아 Worktree 검출 및 정리

세션 종료, 에러 발생 등으로 정리되지 않은 worktree가 남을 수 있습니다.

### 검출 명령어
```bash
# tree/ 디렉토리에 남아있는 worktree 확인
ls tree/ 2>/dev/null

# Git worktree 목록 확인
git worktree list
```

### 정리 판단 기준

| 상태 | 조치 |
|------|------|
| 커밋되지 않은 변경 있음 | 사용자에게 확인 후 정리 |
| 커밋만 있고 머지 안됨 | 머지 또는 폐기 선택 제안 |
| 빈 worktree | 즉시 정리 |

### 자동 정리 스크립트
```bash
# 고아 worktree 정리 (커밋되지 않은 변경 없는 경우만)
for wt in tree/*/; do
  name=$(basename "$wt")
  if [ -d "$wt" ]; then
    cd "$wt"
    if [ -z "$(git status --porcelain)" ]; then
      cd -
      git worktree remove "tree/${name}"
      git branch -D "plan/${name}" 2>/dev/null
    else
      echo "[WARN] tree/${name}: 커밋되지 않은 변경 있음"
    fi
  fi
done
```

### 워크플로우 시작 시 검사

Planner는 워크플로우 시작 시 다음을 확인:

1. `tree/` 디렉토리 존재 여부 확인
2. 존재하면 사용자에게 알림:
   ```
   [WARN] 이전 워크플로우의 Worktree가 남아있습니다:
   - tree/feature-xxx (커밋 3개, 머지 안됨)

   정리 방법:
   1. 머지 후 정리: git merge plan/feature-xxx && git worktree remove tree/feature-xxx
   2. 폐기: git worktree remove --force tree/feature-xxx

   계속 진행하시겠습니까?
   ```

## Coder 작업 규칙

1. Planner가 지정한 Worktree 디렉토리에서만 작업
2. 메인 디렉토리 파일 직접 수정 금지
3. 커밋은 Worktree 브랜치에만 수행
