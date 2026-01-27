# Code Quality Failure Messages

> **목적**: code-quality 검증 실패 시 개발자에게 명확한 가이드를 제공하여 빠른 문제 해결을 지원합니다.

---

## ⚠️ File Length Exceeded

**문제**: `{file_path}` 파일이 {actual_lines}줄로 300줄 제한을 초과했습니다.

**영향**: 파일이 너무 길면 유지보수성과 가독성이 저하됩니다.

**해결 방법**:
1. 단일 책임 원칙(SRP) 적용: 파일을 기능별로 분리
2. 큰 함수를 작은 함수로 리팩토링
3. 유틸리티 함수를 별도 파일로 추출
4. 관련 기능을 모듈화하여 분리

**예시**:
```typescript
// ❌ Before: 500줄의 거대한 파일
// src/services/UserService.ts (500줄)
export class UserService {
  async createUser(data: CreateUserDTO) { /* 100줄 */ }
  validateEmail(email: string) { /* 50줄 */ }
  validatePassword(password: string) { /* 50줄 */ }
  hashPassword(password: string) { /* 30줄 */ }
  sendWelcomeEmail(user: User) { /* 80줄 */ }
  // ... 더 많은 메서드
}

// ✅ After: 기능별로 분리
// src/services/UserService.ts (200줄)
export class UserService {
  constructor(
    private validator: UserValidator,
    private mapper: UserMapper,
    private emailService: EmailService
  ) {}

  async createUser(data: CreateUserDTO) {
    const validatedData = this.validator.validate(data);
    const user = this.mapper.toEntity(validatedData);
    // ...
  }
}

// src/services/UserValidator.ts (150줄)
export class UserValidator {
  validateEmail(email: string) { /* ... */ }
  validatePassword(password: string) { /* ... */ }
}

// src/services/UserMapper.ts (150줄)
export class UserMapper {
  toEntity(dto: CreateUserDTO): User { /* ... */ }
  toDTO(user: User): UserDTO { /* ... */ }
}
```

**체크리스트**:
- [ ] 파일의 주요 책임을 식별했는가?
- [ ] 분리할 수 있는 독립적인 기능이 있는가?
- [ ] 각 새 파일이 단일 책임을 가지는가?
- [ ] 분리 후 각 파일이 300줄 이하인가?

---

## ⚠️ Missing Documentation

**문제**: 다음 함수에 JSDoc/docstring이 누락되었습니다:
- `{function_name_1}` at line {line_number}
- `{function_name_2}` at line {line_number}

**영향**: 함수의 목적과 사용법을 알 수 없어 협업에 어려움이 발생하고, 유지보수 시 코드 이해에 시간이 소요됩니다.

**해결 방법**:
각 public 함수에 다음 정보를 포함한 JSDoc/docstring을 추가하세요:
- 함수 설명 (무엇을 하는지)
- @param 각 파라미터 설명 (타입과 의미)
- @returns 반환값 설명 (타입과 의미)
- @throws 발생 가능한 예외 (선택사항)
- @example 사용 예시 (복잡한 경우)

**예시 (TypeScript)**:
```typescript
// ❌ Before: 문서화 없음
async function getUser(userId: string): Promise<User> {
  const user = await this.userRepository.findById(userId);
  if (!user) {
    throw new UserNotFoundError(userId);
  }
  return user;
}

// ✅ After: 완전한 JSDoc
/**
 * 사용자 정보를 조회합니다.
 *
 * 데이터베이스에서 주어진 ID에 해당하는 사용자를 조회하여 반환합니다.
 * 사용자가 존재하지 않으면 예외를 발생시킵니다.
 *
 * @param userId - 조회할 사용자의 고유 ID
 * @returns 조회된 사용자 정보 객체
 * @throws {UserNotFoundError} 사용자가 존재하지 않을 때
 *
 * @example
 * ```typescript
 * const user = await getUser('user-123');
 * console.log(user.name); // "홍길동"
 * ```
 */
async function getUser(userId: string): Promise<User> {
  const user = await this.userRepository.findById(userId);
  if (!user) {
    throw new UserNotFoundError(userId);
  }
  return user;
}
```

**예시 (Python)**:
```python
# ❌ Before: 문서화 없음
def calculate_discount(price: float, user_level: str) -> float:
    if user_level == "VIP":
        return price * 0.8
    elif user_level == "GOLD":
        return price * 0.9
    return price

# ✅ After: 완전한 docstring
def calculate_discount(price: float, user_level: str) -> float:
    """
    사용자 등급에 따라 할인된 가격을 계산합니다.

    VIP 회원은 20%, GOLD 회원은 10% 할인을 받습니다.
    일반 회원은 할인이 적용되지 않습니다.

    Args:
        price (float): 원래 가격 (양수)
        user_level (str): 사용자 등급 ("VIP", "GOLD", "NORMAL")

    Returns:
        float: 할인이 적용된 최종 가격

    Raises:
        ValueError: price가 음수인 경우

    Example:
        >>> calculate_discount(10000, "VIP")
        8000.0
        >>> calculate_discount(10000, "GOLD")
        9000.0
    """
    if price < 0:
        raise ValueError("Price must be non-negative")

    if user_level == "VIP":
        return price * 0.8
    elif user_level == "GOLD":
        return price * 0.9
    return price
```

**체크리스트**:
- [ ] 모든 public 함수에 JSDoc/docstring이 추가되었는가?
- [ ] 각 파라미터의 의미가 명확히 설명되었는가?
- [ ] 반환값의 타입과 의미가 설명되었는가?
- [ ] 예외 상황이 문서화되었는가?
- [ ] 복잡한 함수는 사용 예시를 포함하는가?

---

## ⚠️ Architecture Dependency Violation

**문제**: Clean Architecture 의존성 규칙 위반이 감지되었습니다:
- `{file_path}` (Domain 레이어) → `{target_path}` (Infrastructure 레이어)
- **위반된 의존성 방향**: Domain → Infrastructure ❌

**영향**: 내부 레이어가 외부 레이어에 의존하면 다음과 같은 문제가 발생합니다:
- 비즈니스 로직 테스트가 어려워짐 (외부 의존성 필요)
- 기술 스택 변경 시 도메인 로직까지 수정 필요
- 코드 재사용성 저하
- 순환 의존성 위험 증가

**Clean Architecture 의존성 규칙**:
```
Infrastructure (외부)
    ↑
Adapters (인터페이스 어댑터)
    ↑
Application (유스케이스)
    ↑
Domain (비즈니스 로직) - 어디에도 의존하지 않음
```

**해결 방법**:
의존성 역전 원칙(DIP)을 적용하여 의존성 방향을 수정합니다:

1. **Domain 레이어에 Port(인터페이스) 정의**
2. **Infrastructure/Adapters에서 Port 구현**
3. **Domain은 Port만 참조** (구체적인 구현 모름)

**예시 (TypeScript)**:
```typescript
// ❌ Before: Domain이 Infrastructure 직접 의존
// src/domain/User.ts (Domain 레이어)
import { PostgresClient } from '../../infrastructure/db/postgres'; // ❌ 위반!

export class User {
  async save() {
    const db = new PostgresClient();
    await db.query('INSERT INTO users ...');
  }
}

// ✅ After: 의존성 역전 원칙 적용

// 1. Domain에 Port(인터페이스) 정의
// src/domain/ports/UserRepository.ts (Domain 레이어)
export interface UserRepository {
  save(user: User): Promise<void>;
  findById(id: string): Promise<User | null>;
}

// 2. Domain 엔티티는 Port만 참조
// src/domain/User.ts (Domain 레이어)
export class User {
  constructor(
    public id: string,
    public name: string,
    public email: string
  ) {}

  // 엔티티는 저장 방법을 모름 (Port를 통해 위임)
}

// 3. Application 유스케이스에서 Port 사용
// src/application/usecases/CreateUser.ts (Application 레이어)
export class CreateUserUseCase {
  constructor(
    private userRepository: UserRepository // Port만 의존
  ) {}

  async execute(dto: CreateUserDTO): Promise<User> {
    const user = new User(dto.id, dto.name, dto.email);
    await this.userRepository.save(user); // 구체적인 구현 모름
    return user;
  }
}

// 4. Infrastructure에서 Port 구현
// src/infrastructure/repositories/PostgresUserRepository.ts (Infrastructure 레이어)
import { UserRepository } from '../../domain/ports/UserRepository';
import { PostgresClient } from '../db/postgres';

export class PostgresUserRepository implements UserRepository {
  constructor(private db: PostgresClient) {}

  async save(user: User): Promise<void> {
    await this.db.query(
      'INSERT INTO users (id, name, email) VALUES ($1, $2, $3)',
      [user.id, user.name, user.email]
    );
  }

  async findById(id: string): Promise<User | null> {
    const result = await this.db.query('SELECT * FROM users WHERE id = $1', [id]);
    if (!result.rows[0]) return null;
    return new User(result.rows[0].id, result.rows[0].name, result.rows[0].email);
  }
}

// 5. 의존성 주입 (Infrastructure 레이어에서 조립)
// src/infrastructure/di/container.ts
const postgresClient = new PostgresClient();
const userRepository = new PostgresUserRepository(postgresClient);
const createUserUseCase = new CreateUserUseCase(userRepository);
```

**레이어별 의존성 규칙 요약**:

| 레이어 | 허용된 의존성 | 금지된 의존성 |
|--------|--------------|--------------|
| Domain | 없음 (순수 비즈니스 로직) | Application, Adapters, Infrastructure |
| Application | Domain만 | Adapters, Infrastructure |
| Adapters | Domain, Application | Infrastructure (DI로 주입받음) |
| Infrastructure | 모든 레이어 (조립) | 없음 |

**체크리스트**:
- [ ] Domain 레이어가 외부 레이어를 직접 import하지 않는가?
- [ ] Port(인터페이스)가 Domain 또는 Application 레이어에 정의되었는가?
- [ ] Port 구현체가 Adapters/Infrastructure 레이어에 있는가?
- [ ] 의존성 주입을 통해 구현체가 전달되는가?
- [ ] 각 레이어가 올바른 위치에 있는가?

**참조**:
- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [프로젝트 Clean Architecture 가이드](../../planner/references/clean-architecture.md)

---

## 🔧 자동 수정 가능 여부

| 위반 유형 | 자동 수정 | 수동 수정 필요 |
|----------|----------|---------------|
| 파일 길이 초과 | ❌ | ✅ (의미 파악 필요) |
| JSDoc 누락 | ⚠️ 부분 가능 (기본 템플릿) | ✅ (정확한 설명 필요) |
| 아키텍처 위반 | ❌ | ✅ (설계 재구성 필요) |

---

## 📋 품질 게이트 체크리스트

모든 항목을 확인한 후 커밋하세요:

- [ ] **파일 길이**: 모든 파일이 300줄 이하
- [ ] **문서화**: 모든 public 함수에 JSDoc/docstring 존재
- [ ] **아키텍처**: 레이어 의존성 규칙 준수
- [ ] **테스트**: 모든 테스트 통과
- [ ] **빌드**: 빌드 에러 없음

---

## 💡 추가 도움말

### 품질 검증 재실행

수정 후 품질 검증을 다시 실행하세요:

```python
# 수정 완료 후
Skill(skill="code-quality")
```

### 긴급 상황 시

긴급 수정이 필요한 경우에도 품질 게이트 예외는 없습니다.
- 최소한의 수정으로 문제를 해결하세요
- 품질 검증 통과 후 커밋하세요
- 추가 리팩토링은 별도 작업으로 계획하세요

### 도움이 필요한 경우

- Clean Architecture 가이드: `.claude/skills/planner/references/clean-architecture.md`
- Best Practices: `.claude/skills/best-practices/`
- 문제 해결: `/solve [문제 설명]` 실행
