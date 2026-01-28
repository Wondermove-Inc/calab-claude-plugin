# /clean --entity - 도메인 엔티티 생성

> **Domain Layer에 엔티티, 값 객체, 리포지토리 인터페이스 생성**

## 사용법

```bash
/clean --entity User
/clean --entity Order --with-repo
/clean --entity Money --value-object
```

## 실행 절차

### Step 1: 엔티티 정보 수집

사용자에게 질문:

1. **필수 속성**은 무엇인가요?
   - 예: id, email, name

2. **선택 속성**은 무엇인가요?
   - 예: bio, avatarUrl

3. **값 객체(Value Object)**가 필요한 속성이 있나요?
   - 예: Email (이메일 형식 검증)

4. **리포지토리 인터페이스**를 생성할까요? (Y/N)

### Step 2: 엔티티 클래스 생성

**src/domain/entities/{EntityName}.ts:**

```typescript
// src/domain/entities/User.ts

import { Email } from '../value-objects/Email';

interface UserProps {
  id: string;
  email: Email;
  name: string;
  bio?: string;
  avatarUrl?: string;
  createdAt: Date;
  updatedAt: Date;
}

export class User {
  private constructor(private readonly props: UserProps) {}

  // Factory Methods
  static create(props: Omit<UserProps, 'id' | 'createdAt' | 'updatedAt'>): User {
    return new User({
      ...props,
      id: crypto.randomUUID(),
      createdAt: new Date(),
      updatedAt: new Date(),
    });
  }

  static reconstitute(props: UserProps): User {
    return new User(props);
  }

  // Getters (Immutable)
  get id(): string {
    return this.props.id;
  }

  get email(): Email {
    return this.props.email;
  }

  get name(): string {
    return this.props.name;
  }

  get bio(): string | undefined {
    return this.props.bio;
  }

  get avatarUrl(): string | undefined {
    return this.props.avatarUrl;
  }

  get createdAt(): Date {
    return this.props.createdAt;
  }

  get updatedAt(): Date {
    return this.props.updatedAt;
  }

  // Business Methods
  updateProfile(name: string, bio?: string): User {
    return new User({
      ...this.props,
      name,
      bio,
      updatedAt: new Date(),
    });
  }

  changeEmail(email: Email): User {
    return new User({
      ...this.props,
      email,
      updatedAt: new Date(),
    });
  }

  // Equality
  equals(other: User): boolean {
    return this.id === other.id;
  }
}
```

### Step 3: 값 객체 생성 (선택)

**src/domain/value-objects/{ValueObject}.ts:**

```typescript
// src/domain/value-objects/Email.ts

import { ValidationError } from '../errors/DomainError';

export class Email {
  private constructor(private readonly value: string) {}

  static create(email: string): Email {
    if (!Email.isValid(email)) {
      throw new ValidationError('Invalid email format', 'email');
    }
    return new Email(email.toLowerCase().trim());
  }

  private static isValid(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  toString(): string {
    return this.value;
  }

  equals(other: Email): boolean {
    return this.value === other.value;
  }

  get domain(): string {
    return this.value.split('@')[1];
  }
}
```

### Step 4: 리포지토리 인터페이스 생성 (선택)

**src/domain/interfaces/I{EntityName}Repository.ts:**

```typescript
// src/domain/interfaces/IUserRepository.ts

import { User } from '../entities/User';
import { Email } from '../value-objects/Email';

export interface IUserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: Email): Promise<User | null>;
  findAll(): Promise<User[]>;
  save(user: User): Promise<void>;
  delete(id: string): Promise<void>;
  exists(id: string): Promise<boolean>;
}
```

### Step 5: 완료 보고

```
============================================
 CLEAN ENTITY 완료: User
============================================

 📄 생성된 파일:
 • src/domain/entities/User.ts
 • src/domain/value-objects/Email.ts
 • src/domain/interfaces/IUserRepository.ts

 📝 엔티티 구조:
 • 필수 속성: id, email, name, createdAt, updatedAt
 • 선택 속성: bio, avatarUrl
 • 값 객체: Email

 🔧 패턴:
 • Private constructor + Static factory methods
 • Immutable properties (getters only)
 • Business methods return new instance

============================================
 다음 단계: /clean --usecase Create{Entity}
============================================
```

## 엔티티 설계 규칙

### Factory Method 패턴
```typescript
// ✅ Good
static create(props): Entity { ... }
static reconstitute(props): Entity { ... }

// ❌ Bad
constructor(props) { ... }  // public constructor
```

### 불변성 (Immutability)
```typescript
// ✅ Good - Return new instance
updateName(name: string): User {
  return new User({ ...this.props, name });
}

// ❌ Bad - Mutate internal state
updateName(name: string): void {
  this.props.name = name;
}
```

### 값 객체 사용
```typescript
// ✅ Good - Value Object
email: Email;

// ❌ Bad - Primitive
email: string;
```

### 동등성 비교
```typescript
// ✅ Good - ID 기반 비교
equals(other: User): boolean {
  return this.id === other.id;
}
```
