---
name: workflow:qa-plan
description: QA 계획서를 생성하거나 수정합니다. 테스트 범위, 전략, 케이스를 정의합니다.
allowed-tools: Read, Write, Glob, Grep
user-invocable: true
---
# /qa-plan - QA 계획서 생성

## 설명

QA 계획서를 **상세하게 작성**합니다.
테스트 범위, 전략, 일정, 성공 기준을 명확히 정의합니다.


## 계획서 생성 프로세스

### Step 1: 정보 수집

**수집 항목:**

| 항목 | 소스 | 예시 |
|------|------|------|
| 프로젝트명 | package.json | "marketplace" |
| 기능 목록 | PRD, Worktree | 로그인, 결제, 검색 |
| 페이지 목록 | src/app | /login, /dashboard |
| 컴포넌트 | src/components | Button, Modal |

### Step 2: 테스트 범위 정의

**In-Scope (테스트 대상):**

```markdown
## 테스트 범위

### 포함
- 모든 사용자 대면 페이지
- 핵심 비즈니스 로직
- 폼 제출 및 유효성 검사
- 네비게이션 흐름
- 에러 처리

### 제외
- 관리자 페이지 (별도 QA)
- 외부 API 연동 상세
- 퍼포먼스 테스트
```

### Step 3: 테스트 전략 수립

**테스트 피라미드:**

```
        /\
       /E2E\        ← 10% (MCP Puppeteer)
      /------\
     / Integr \     ← 20% (API 연동)
    /----------\
   /    Unit    \   ← 70% (개별 함수)
  /--------------\
```

**Risk-based Testing:**

| 리스크 레벨 | 기능 예시 | 테스트 강도 |
|-------------|----------|------------|
| Critical | 결제, 인증 | 모든 시나리오 |
| High | 검색, 필터 | 주요 시나리오 |
| Medium | 설정, 알림 | 기본 시나리오 |
| Low | 도움말, 정보 | 스모크 테스트 |

### Step 4: 테스트 케이스 정의

**케이스 유형:**

| 유형 | 설명 | 예시 |
|------|------|------|
| Happy Path | 정상 흐름 | 올바른 로그인 |
| Edge Case | 경계 조건 | 빈 입력, 최대 길이 |
| Error Case | 에러 상황 | 잘못된 비밀번호 |
| Security | 보안 검증 | XSS, CSRF |

**Acceptance Criteria (Given-When-Then):**

```gherkin
Feature: 로그인
  Scenario: 정상 로그인
    Given 로그인 페이지에 접속
    When 올바른 이메일과 비밀번호 입력
    And 로그인 버튼 클릭
    Then 대시보드로 이동
    And 사용자 이름 표시
```

### Step 5: 성공 기준 정의

```markdown
## 성공 기준

### 필수 (Must Pass)
- [ ] P0 테스트 100% 통과
- [ ] Critical 버그 0개
- [ ] 모든 페이지 로드 확인

### 권장 (Should Pass)
- [ ] P1 테스트 95% 이상 통과
- [ ] Major 버그 모두 해결

### 선택 (Nice to Have)
- [ ] P2 테스트 90% 이상 통과
- [ ] 모든 Minor 버그 문서화
```


**승인:**

| 역할 | 이름 | 날짜 |
|------|------|------|
| QA 담당 | Claude AI | {today} |
| 승인자 | | |
```


## 옵션 설명

| 옵션 | 설명 |
|------|------|
| `--edit` | 기존 계획서 수정 모드 |
| `--from-prd` | PRD 문서에서 기능 자동 추출 |
| `--from-worktree` | Worktree에서 태스크 추출 |
| `--template` | 빈 템플릿만 생성 |
