---
name: tdd-workflow
description: 테스트 주도 개발(TDD) 워크플로우를 강제합니다. 테스트 먼저 작성, 80% 커버리지 요구.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# TDD Workflow Skill

> **테스트 주도 개발 - Red → Green → Refactor**

## 목적

코드 품질과 안정성을 보장하기 위해 TDD 방법론을 강제합니다.

## 핵심 원칙

### 1. Red-Green-Refactor 사이클

```
🔴 RED: 실패하는 테스트 먼저 작성
    ↓
🟢 GREEN: 테스트를 통과하는 최소한의 코드 작성
    ↓
🔵 REFACTOR: 코드 개선 (테스트는 계속 통과)
    ↓
   반복
```

### 2. 커버리지 요구사항

| 커버리지 유형 | 최소 요구 | 권장 |
|-------------|----------|------|
| **라인 커버리지** | 70% | 80% |
| **브랜치 커버리지** | 60% | 70% |
| **함수 커버리지** | 80% | 90% |

### 3. 테스트 피라미드

```
        /\
       /  \     E2E 테스트 (10%)
      /    \    - 핵심 사용자 시나리오
     /------\   - Playwright/Cypress
    /        \
   /          \  통합 테스트 (20%)
  /            \ - API 테스트
 /--------------\- 데이터베이스 테스트
/                \
/                  \  단위 테스트 (70%)
/                    \ - 함수/클래스 테스트
/______________________\- 모킹 활용
```

## TDD 실행 프로토콜

### Step 1: 요구사항 분석

```
입력: 구현할 기능 설명
출력:
  - 기능 요구사항 목록
  - 테스트 케이스 목록 (Given-When-Then)
  - 경계 조건 및 예외 케이스
```

### Step 2: 테스트 케이스 설계

```markdown
## 테스트 케이스: [기능명]

### 정상 케이스
- [ ] TC-001: [시나리오] → 기대 결과
- [ ] TC-002: [시나리오] → 기대 결과

### 경계 케이스
- [ ] TC-003: [빈 입력] → 기대 결과
- [ ] TC-004: [최대값] → 기대 결과

### 예외 케이스
- [ ] TC-005: [잘못된 입력] → 에러 발생
- [ ] TC-006: [네트워크 실패] → 적절한 처리
```

### Step 3: 🔴 RED - 실패하는 테스트 작성

```typescript
// ❌ 테스트가 실패해야 함 (구현 전)
describe('UserService', () => {
  describe('createUser', () => {
    it('should create a user with valid data', async () => {
      // Given
      const userData = {
        email: 'test@example.com',
        name: 'Test User',
      };

      // When
      const result = await userService.createUser(userData);

      // Then
      expect(result.id).toBeDefined();
      expect(result.email).toBe(userData.email);
      expect(result.name).toBe(userData.name);
    });

    it('should throw error for invalid email', async () => {
      // Given
      const userData = { email: 'invalid', name: 'Test' };

      // When & Then
      await expect(userService.createUser(userData))
        .rejects.toThrow('Invalid email format');
    });
  });
});
```

### Step 4: 🟢 GREEN - 최소한의 구현

```typescript
// ✅ 테스트를 통과하는 최소한의 코드
class UserService {
  async createUser(data: CreateUserDto): Promise<User> {
    // 입력 검증
    if (!this.isValidEmail(data.email)) {
      throw new Error('Invalid email format');
    }

    // 사용자 생성
    const user = await this.userRepository.create({
      id: generateId(),
      email: data.email,
      name: data.name,
    });

    return user;
  }

  private isValidEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
}
```

### Step 5: 🔵 REFACTOR - 코드 개선

```typescript
// 🔄 리팩토링 (테스트는 계속 통과)
class UserService {
  constructor(
    private readonly userRepository: UserRepository,
    private readonly emailValidator: EmailValidator,
  ) {}

  async createUser(data: CreateUserDto): Promise<User> {
    this.validateInput(data);
    return this.userRepository.create(this.toUserEntity(data));
  }

  private validateInput(data: CreateUserDto): void {
    if (!this.emailValidator.isValid(data.email)) {
      throw new InvalidEmailError(data.email);
    }
  }

  private toUserEntity(data: CreateUserDto): UserEntity {
    return {
      id: generateId(),
      ...data,
      createdAt: new Date(),
    };
  }
}
```

### Step 6: 커버리지 확인

```bash
# 테스트 실행 및 커버리지 리포트
npm test -- --coverage

# 예상 출력
--------------------|---------|----------|---------|---------|
File                | % Stmts | % Branch | % Funcs | % Lines |
--------------------|---------|----------|---------|---------|
All files           |   85.2  |    72.4  |   90.1  |   84.8  |
 user.service.ts    |   92.3  |    85.7  |   100   |   91.7  |
 email.validator.ts |   100   |    100   |   100   |   100   |
--------------------|---------|----------|---------|---------|
```

## 테스트 작성 규칙

### 1. 테스트 명명 규칙

```typescript
// ✅ 좋은 예: should [동작] when [조건]
it('should return user when valid id is provided', ...)
it('should throw NotFoundError when user does not exist', ...)

// ❌ 나쁜 예
it('test1', ...)
it('user test', ...)
```

### 2. AAA 패턴 (Arrange-Act-Assert)

```typescript
it('should calculate total price with discount', () => {
  // Arrange (준비)
  const items = [{ price: 100 }, { price: 200 }];
  const discount = 0.1;

  // Act (실행)
  const result = calculateTotal(items, discount);

  // Assert (검증)
  expect(result).toBe(270);
});
```

### 3. Given-When-Then 패턴

```typescript
it('should apply discount for premium users', () => {
  // Given: 프리미엄 사용자와 상품
  const user = createPremiumUser();
  const product = createProduct({ price: 1000 });

  // When: 가격 계산
  const price = calculatePrice(user, product);

  // Then: 10% 할인 적용
  expect(price).toBe(900);
});
```

### 4. 모킹 규칙

```typescript
// ✅ 외부 의존성만 모킹
const mockRepository = {
  findById: jest.fn(),
  save: jest.fn(),
};

// ❌ 테스트 대상은 모킹하지 않음
// 실제 로직을 테스트해야 함
```

## 커버리지 미달 시 처리

### 경고 (70-80%)

```
⚠️ 테스트 커버리지 경고
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
현재 커버리지: 75.2%
최소 요구: 70%
권장 수준: 80%

미커버 영역:
  • src/services/payment.ts:45-52 (에러 처리)
  • src/utils/formatter.ts:23-30 (엣지 케이스)

💡 추가 테스트 작성을 권장합니다.
계속 진행하시겠습니까? [Y/N]
```

### 차단 (70% 미만)

```
🚫 테스트 커버리지 부족
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
현재 커버리지: 58.3%
최소 요구: 70%

테스트가 필요한 파일:
  • src/services/auth.ts (커버리지: 32%)
  • src/controllers/user.ts (커버리지: 45%)
  • src/middleware/validation.ts (커버리지: 28%)

❌ 커버리지가 70% 이상이 될 때까지 커밋이 차단됩니다.
테스트를 추가해주세요.
```

## 테스트 파일 위치 규칙

```
src/
├── services/
│   ├── user.service.ts
│   └── user.service.test.ts      # 같은 폴더
├── __tests__/                     # 또는 별도 폴더
│   └── services/
│       └── user.service.test.ts
└── tests/                         # E2E 테스트
    └── e2e/
        └── user.e2e.test.ts
```

## 출력 형식

### TDD 세션 시작

```
🧪 TDD 모드 활성화
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
기능: [기능명]
테스트 케이스: [N]개

📋 테스트 케이스 목록
  1. [ ] 정상 케이스: 유효한 입력으로 생성
  2. [ ] 경계 케이스: 빈 입력 처리
  3. [ ] 예외 케이스: 잘못된 입력 에러

🔴 Step 1: 실패하는 테스트 작성 중...
```

### TDD 세션 완료

```
✅ TDD 사이클 완료
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
테스트: 5개 통과 / 5개 전체
커버리지: 87.3% ✓

📊 커버리지 상세
  • 라인: 87.3%
  • 브랜치: 78.5%
  • 함수: 95.0%

⏱️ 소요 시간
  • 테스트 작성: 15분
  • 구현: 20분
  • 리팩토링: 10분
```

## 참조 파일

- `.claude/best-practices/testing.md` - 테스트 베스트 프랙티스
- `commands/dev-build.md` - --tdd 옵션 사용법
