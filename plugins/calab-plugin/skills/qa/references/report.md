# /qa --report - QA 보고서 생성

> **테스트 결과 집계 및 릴리스 권고**

## 실행 절차

### Step 1: 데이터 수집
- qa-status.json
- test-results.json
- bugs.json
- screenshots/

### Step 2: 통계 계산
- 우선순위별 Pass Rate
- 버그 심각도별 분류

### Step 3: 보고서 생성

**QA_REPORT.md 구조:**
```markdown
# QA 보고서: {기능명}

## 요약
| 항목 | 값 |
|------|-----|
| 전체 Pass Rate | 95% |
| P0 Pass Rate | 100% |
| Critical Bugs | 0 |

## 우선순위별 결과
## 버그 목록
## 스크린샷
## 릴리스 권고
```

### Step 4: 릴리스 권고 결정

| 조건 | 권고 |
|------|------|
| P0=100%, Critical=0 | ✅ Approved |
| P0≥95%, Critical=0 | ⚠️ Conditional |
| P0<95% 또는 Critical>0 | ❌ Not Approved |

### 출력 파일
- `.claude/docs/active/{feature}/qa/QA_REPORT.md`
- `.claude/docs/active/{feature}/qa/BUG_REPORT.md`
