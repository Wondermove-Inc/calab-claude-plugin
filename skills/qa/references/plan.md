# /qa --plan - QA 계획서 생성

> **테스트 범위, 전략, 성공 기준 정의**

## 실행 절차

### Step 1: 정보 수집
- PRD에서 기능 목록 추출
- Worktree에서 완료된 태스크 확인
- 라우트/컴포넌트 스캔

### Step 2: 테스트 범위 정의
- **In-Scope**: 테스트할 기능
- **Out-of-Scope**: 제외 기능

### Step 3: 전략 수립
- 테스트 피라미드: 70% Unit, 20% Integration, 10% E2E
- Risk-based Testing 적용

### Step 4: 성공 기준 정의
- P0: 100% Pass 필수
- P1: 95%+ Pass
- P2: 90%+ Pass
- Critical Bug: 0개

### Step 5: 계획서 작성

**QA_PLAN.md 구조:**
```markdown
# QA 계획서: {기능명}

## 테스트 범위
## 테스트 전략
## 테스트 케이스 유형
## 성공 기준
## 일정
## 리스크
```

### 출력 파일
- `.claude/docs/active/{feature}/qa/QA_PLAN.md`
