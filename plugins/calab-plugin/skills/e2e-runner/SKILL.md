---
name: e2e-runner
description: Playwright/Puppeteer 기반 E2E 테스트를 자동 실행하고 디버깅합니다. E2E, 통합 테스트, 브라우저 테스트 키워드 시 자동 활성화.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, mcp__puppeteer__puppeteer_navigate, mcp__puppeteer__puppeteer_screenshot, mcp__puppeteer__puppeteer_click, mcp__puppeteer__puppeteer_fill, mcp__puppeteer__puppeteer_evaluate
---

# E2E Runner

Playwright/Puppeteer 기반 E2E 테스트를 자동 실행하고 디버깅하는 스킬.

## 🤖 에이전트 실행 (필수)

**⚠️ 이 스킬이 로드되면 아래 지침을 따라 즉시 Task 도구를 호출하세요.**

이 스킬은 e2e-runner 에이전트를 통해 실행됩니다. **지금 바로 Task 도구를 호출**하세요.

**호출 파라미터:**
- `subagent_type`: `"calab-plugin:e2e-runner"`
- `description`: `"E2E 테스트 실행 및 분석"`
- `prompt`: 아래 프롬프트 내용 사용

**프롬프트 내용:**
```
**역할**: E2E 테스트 전문가

**목표**: Playwright/Puppeteer 기반 E2E 테스트 실행 및 결과 분석

**수행 단계**:
1. 테스트 프레임워크 감지 (Playwright, Puppeteer, Cypress)
2. 의존성 및 브라우저 설치 확인
3. 테스트 실행
4. 결과 분석 및 실패 원인 파악
5. 스크린샷/트레이스 확인

**실행 명령**:
- Playwright: npx playwright test --reporter=list
- Puppeteer: npx jest --config=jest.e2e.config.js
- Cypress: npx cypress run

**출력 형식**:
## E2E 테스트 결과
- 총 테스트: N개
- 성공: N개 ✅
- 실패: N개 ❌

### 실패한 테스트
| 테스트 | 파일 | 오류 |
|--------|------|------|

### 권장 조치
1. [파일]: [수정 제안]

**제약 조건**:
- ❌ 테스트 코드 자동 수정 금지 (제안만)
- ✅ 실패 원인 상세 분석 필수
- ✅ 스크린샷 경로 포함
```

**⚠️ 중요**: 이 지침을 읽고 있다면, 사용자에게 텍스트로 응답하지 말고 **Task 도구를 호출**하세요!

---

## 지원 프레임워크

| 프레임워크 | 설정 파일 | 실행 명령 |
|-----------|----------|----------|
| **Playwright** | playwright.config.ts | npx playwright test |
| **Puppeteer** | jest-puppeteer.config.js | npx jest --config=jest.e2e.config.js |
| **Cypress** | cypress.config.ts | npx cypress run |

## 테스트 실행 워크플로우

### Phase 1: 환경 확인
```bash
# 1. 테스트 프레임워크 감지
ls playwright.config.* cypress.config.* jest-puppeteer.config.*

# 2. 의존성 확인
npm list @playwright/test puppeteer cypress

# 3. 브라우저 설치 확인 (Playwright)
npx playwright install --dry-run
```

### Phase 2: 테스트 실행
```bash
# Playwright
npx playwright test --reporter=list

# 특정 파일만
npx playwright test tests/login.spec.ts

# 특정 테스트만
npx playwright test -g "should login successfully"

# 디버그 모드
npx playwright test --debug
```

### Phase 3: 결과 분석
```bash
# 리포트 생성
npx playwright show-report

# 스크린샷/트레이스 확인
ls test-results/
```

## MCP Puppeteer 활용

### 직접 브라우저 조작
```typescript
// 페이지 이동
mcp__puppeteer__puppeteer_navigate({ url: "http://localhost:3000" })

// 스크린샷 캡처
mcp__puppeteer__puppeteer_screenshot({ name: "login-page" })

// 요소 클릭
mcp__puppeteer__puppeteer_click({ selector: "#login-button" })

// 입력 필드 채우기
mcp__puppeteer__puppeteer_fill({
  selector: "#email",
  value: "test@example.com"
})

// JavaScript 실행
mcp__puppeteer__puppeteer_evaluate({
  script: "document.title"
})
```

## 디버깅 가이드

### 테스트 실패 분석
```markdown
## 실패 원인 분석 체크리스트

### 1. 선택자 문제
- [ ] 요소가 DOM에 존재하는가?
- [ ] 선택자가 고유한가?
- [ ] 동적 로딩 대기가 필요한가?

### 2. 타이밍 문제
- [ ] 페이지 로드 완료 대기
- [ ] API 응답 대기
- [ ] 애니메이션 완료 대기

### 3. 환경 문제
- [ ] 개발 서버 실행 중인가?
- [ ] 포트 충돌이 없는가?
- [ ] 환경 변수 설정이 올바른가?
```

### 일반적인 해결책
```typescript
// 요소 대기
await page.waitForSelector('#element', { timeout: 5000 });

// 네트워크 유휴 대기
await page.waitForLoadState('networkidle');

// 명시적 대기
await page.waitForTimeout(1000);

// 조건부 대기
await page.waitForFunction(() => {
  return document.querySelector('#loading') === null;
});
```

## 테스트 패턴

### Page Object Model
```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async navigate() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.fill('#email', email);
    await this.page.fill('#password', password);
    await this.page.click('#submit');
  }
}

// tests/login.spec.ts
test('should login', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.navigate();
  await loginPage.login('user@test.com', 'password');
  await expect(page).toHaveURL('/dashboard');
});
```

### 데이터 기반 테스트
```typescript
const testCases = [
  { email: 'valid@test.com', password: 'valid', expected: 'success' },
  { email: 'invalid@test.com', password: 'wrong', expected: 'error' },
];

for (const tc of testCases) {
  test(`login with ${tc.email}`, async ({ page }) => {
    // ...
  });
}
```

## 출력 형식

```markdown
## E2E 테스트 결과

### 실행 요약
- 총 테스트: 25개
- 성공: 23개 ✅
- 실패: 2개 ❌
- 건너뜀: 0개

### 실패한 테스트
| 테스트 | 파일 | 오류 |
|--------|------|------|
| should display cart | cart.spec.ts:45 | Timeout waiting for #cart-items |
| should checkout | checkout.spec.ts:78 | Element #pay-button not found |

### 스크린샷
- test-results/cart-failure.png
- test-results/checkout-failure.png

### 권장 조치
1. cart.spec.ts: API 응답 대기 추가 필요
2. checkout.spec.ts: 선택자 업데이트 필요 (#pay-button → #payment-submit)
```

## 관련 스킬
- `qa-testing`: QA 테스트 전략
- `problem-solving`: 테스트 실패 디버깅

## 참조
- `.claude/best-practices/testing.md`
- `.claude/best-practices/qa-testing.md`
