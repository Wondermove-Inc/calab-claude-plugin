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

## Coder 작업 규칙

1. Planner가 지정한 Worktree 디렉토리에서만 작업
2. 메인 디렉토리 파일 직접 수정 금지
3. 커밋은 Worktree 브랜치에만 수행
