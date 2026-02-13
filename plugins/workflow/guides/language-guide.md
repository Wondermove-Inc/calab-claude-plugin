# 아키텍처 설계 원칙 (Architecture Guide)

> 이 문서는 Reviewer 에이전트가 참조합니다.

---

## SOLID 원칙

소프트웨어 설계의 5가지 기본 원칙으로, 유지보수 가능하고 확장 가능한 시스템을 구축하기 위한 가이드입니다.

### S - 단일 책임 원칙 (Single Responsibility Principle)

**정의**: 클래스/모듈은 단 하나의 책임만 가져야 하며, 변경 이유도 하나만 있어야 한다.

**좋은 예**:
```typescript
// ✅ 각 클래스가 하나의 책임만
class UserRepository {
  save(user: User) { /* DB 저장 */ }
  findById(id: string) { /* DB 조회 */ }
}

class UserValidator {
  validate(user: User) { /* 검증 로직 */ }
}

class UserNotifier {
  sendWelcomeEmail(user: User) { /* 이메일 전송 */ }
}
```

**나쁜 예**:
```typescript
// ❌ 하나의 클래스가 여러 책임
class UserService {
  save(user: User) { /* DB 저장 */ }
  validate(user: User) { /* 검증 */ }
  sendEmail(user: User) { /* 이메일 */ }
  calculateDiscount(user: User) { /* 결제 로직 */ }
}
```

**검증 포인트**:
- 클래스/모듈의 변경 이유가 2개 이상인가?
- 여러 도메인의 로직이 혼재되어 있는가?

---

### O - 개방-폐쇄 원칙 (Open-Closed Principle)

**정의**: 확장에는 열려있고, 수정에는 닫혀있어야 한다. 새 기능 추가 시 기존 코드를 변경하지 않아야 한다.

**좋은 예**:
```typescript
// ✅ 인터페이스로 확장 가능
interface PaymentMethod {
  process(amount: number): void;
}

class CreditCardPayment implements PaymentMethod {
  process(amount: number) { /* 신용카드 결제 */ }
}

class PayPalPayment implements PaymentMethod {
  process(amount: number) { /* PayPal 결제 */ }
}

// 새 결제 수단 추가 시 기존 코드 수정 불필요
class BitcoinPayment implements PaymentMethod {
  process(amount: number) { /* 비트코인 결제 */ }
}
```

**나쁜 예**:
```typescript
// ❌ 새 결제 수단 추가 시 기존 코드 수정 필요
class PaymentProcessor {
  process(type: string, amount: number) {
    if (type === 'credit') {
      // 신용카드 결제
    } else if (type === 'paypal') {
      // PayPal 결제
    } else if (type === 'bitcoin') { // 새 수단 추가 시 여기 수정
      // 비트코인 결제
    }
  }
}
```

**검증 포인트**:
- 새 기능 추가 시 기존 코드를 수정하는가?
- if-else 또는 switch-case가 계속 늘어나는가?

---

### L - 리스코프 치환 원칙 (Liskov Substitution Principle)

**정의**: 하위 타입은 상위 타입을 완전히 대체할 수 있어야 한다. 자식 클래스는 부모 클래스의 계약을 위반하지 않아야 한다.

**좋은 예**:
```typescript
// ✅ 자식이 부모의 계약을 준수
interface Bird {
  eat(): void;
}

class Sparrow implements Bird {
  eat() { /* 먹이 섭취 */ }
  fly() { /* 날기 */ }
}

class Penguin implements Bird {
  eat() { /* 먹이 섭취 */ }
  swim() { /* 수영 */ }
}
```

**나쁜 예**:
```typescript
// ❌ 자식이 부모의 계약을 위반
interface Bird {
  fly(): void;
}

class Penguin implements Bird {
  fly() {
    throw new Error("펭귄은 날 수 없음"); // 계약 위반
  }
}
```

**검증 포인트**:
- 자식 클래스가 부모의 메서드를 재정의할 때 예외를 던지는가?
- 자식이 부모의 사전조건을 강화하거나 사후조건을 약화하는가?

---

### I - 인터페이스 분리 원칙 (Interface Segregation Principle)

**정의**: 클라이언트는 사용하지 않는 메서드에 의존하지 않아야 한다. 큰 인터페이스를 작은 인터페이스로 분리하라.

**좋은 예**:
```typescript
// ✅ 클라이언트별로 인터페이스 분리
interface Readable {
  read(): string;
}

interface Writable {
  write(data: string): void;
}

interface Closeable {
  close(): void;
}

class File implements Readable, Writable, Closeable {
  read() { /* 읽기 */ }
  write(data: string) { /* 쓰기 */ }
  close() { /* 닫기 */ }
}

// 읽기만 필요한 클라이언트
class LogReader {
  constructor(private source: Readable) {}
  readLog() {
    return this.source.read(); // 불필요한 write, close 메서드 의존 안 함
  }
}
```

**나쁜 예**:
```typescript
// ❌ 모든 메서드를 강제하는 거대 인터페이스
interface FileOperations {
  read(): string;
  write(data: string): void;
  close(): void;
  encrypt(): void;
  compress(): void;
}

// 읽기만 필요한데 모든 메서드 구현 강제
class LogReader implements FileOperations {
  read() { /* 읽기 */ }
  write() { throw new Error("지원 안 함"); }
  close() { throw new Error("지원 안 함"); }
  encrypt() { throw new Error("지원 안 함"); }
  compress() { throw new Error("지원 안 함"); }
}
```

**검증 포인트**:
- 인터페이스의 메서드 중 일부만 사용하는 클라이언트가 있는가?
- 구현체가 인터페이스 메서드를 빈 구현 또는 예외로 처리하는가?

---

### D - 의존성 역전 원칙 (Dependency Inversion Principle)

**정의**: 고수준 모듈은 저수준 모듈에 의존하지 않아야 한다. 둘 다 추상화에 의존해야 한다.

**좋은 예**:
```typescript
// ✅ 추상화(Port)에 의존
interface UserRepository {
  save(user: User): void;
  findById(id: string): User;
}

// Application 계층 (고수준)
class UserService {
  constructor(private userRepo: UserRepository) {} // 추상화에 의존

  registerUser(user: User) {
    this.userRepo.save(user);
  }
}

// Infrastructure 계층 (저수준)
class MySQLUserRepository implements UserRepository {
  save(user: User) { /* MySQL 저장 */ }
  findById(id: string) { /* MySQL 조회 */ }
}

class MongoUserRepository implements UserRepository {
  save(user: User) { /* MongoDB 저장 */ }
  findById(id: string) { /* MongoDB 조회 */ }
}
```

**나쁜 예**:
```typescript
// ❌ 구체 구현에 의존
class UserService {
  private userRepo = new MySQLUserRepository(); // 구체 클래스에 의존

  registerUser(user: User) {
    this.userRepo.save(user); // DB 변경 시 코드 수정 필요
  }
}
```

**검증 포인트**:
- UseCase/Service가 구체 DB 클래스를 직접 생성하는가?
- 고수준 모듈이 저수준 모듈의 구현 세부사항을 알고 있는가?
- 의존성 주입(DI)을 사용하는가?

---

## SOLID 원칙 적용 체크리스트

아키텍처 리뷰 시 다음 항목을 검증합니다:

| 원칙 | 검증 질문 | Critical 위반 예시 |
|------|-----------|------------------|
| **SRP** | 하나의 클래스/모듈이 여러 책임을 갖는가? | UserService에 인증+결제+이메일 로직 혼재 |
| **OCP** | 새 기능 추가 시 기존 코드를 수정하는가? | 새 결제 수단 추가 시 if-else 수정 |
| **LSP** | 자식이 부모의 계약을 위반하는가? | 인터페이스 메서드에서 예외 발생 |
| **ISP** | 클라이언트가 불필요한 메서드에 의존하는가? | 읽기만 필요한데 write/delete도 구현 강제 |
| **DIP** | 고수준이 저수준에 직접 의존하는가? | UseCase가 `new MySQLRepository()` 직접 생성 |

---

## 언어별 SOLID 적용 예시

### Go
```go
// DIP: 인터페이스에 의존
type UserRepository interface {
    Save(user *User) error
    FindByID(id string) (*User, error)
}

type UserService struct {
    repo UserRepository // 추상화에 의존
}

// SRP: 각 구현체가 하나의 책임
type MySQLUserRepository struct{}
func (r *MySQLUserRepository) Save(user *User) error { /* ... */ }

type RedisUserRepository struct{}
func (r *RedisUserRepository) Save(user *User) error { /* ... */ }
```

### TypeScript
```typescript
// ISP: 작은 인터페이스로 분리
interface Identifiable {
  id: string;
}

interface Timestamped {
  createdAt: Date;
  updatedAt: Date;
}

interface User extends Identifiable, Timestamped {
  name: string;
  email: string;
}

// OCP: 전략 패턴으로 확장
interface ValidationStrategy {
  validate(user: User): boolean;
}

class UserValidator {
  constructor(private strategies: ValidationStrategy[]) {}

  validate(user: User): boolean {
    return this.strategies.every(s => s.validate(user));
  }
}
```

### Python
```python
# LSP: ABC로 계약 정의
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool:
        pass

class CreditCard(PaymentMethod):
    def process(self, amount: float) -> bool:
        # 계약 준수: bool 반환, 예외 없음
        return True

# SRP: 단일 책임
class UserValidator:
    def validate(self, user: dict) -> bool:
        pass

class UserRepository:
    def save(self, user: dict) -> None:
        pass
```

---

## 참고 자료

- [Clean Architecture 가이드](architecture/clean-architecture.md)
- [Hexagonal Architecture 가이드](architecture/hexagonal-architecture.md)
- [API 설계 가이드](architecture/api-design.md)
- [데이터베이스 설계 가이드](architecture/database.md)
