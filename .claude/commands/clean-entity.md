# /clean-entity - 도메인 엔티티 생성

## 설명
클린 아키텍처의 Domain 레이어에 새로운 엔티티를 생성합니다.

## 사용법
```
/clean-entity <EntityName>
/clean-entity User
/clean-entity Product --with-repository
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `--with-repository` | 리포지토리 인터페이스도 함께 생성 |
| `--with-value-objects` | 관련 값 객체 생성 |

## 실행 순서

### 1. 사용자에게 엔티티 속성 질문

```
엔티티 '{EntityName}'의 속성을 정의해주세요:
1. 필수 속성 (예: email, name)
2. 선택 속성 (예: bio, avatar)
3. 값 객체로 분리할 속성 (예: Email, Money)
```

### 2. 파일 생성

#### src/domain/entities/{EntityName}.ts
```typescript
import { Email } from '../value-objects/Email';

export interface {EntityName}Props {
  id: string;
  email: Email;
  name: string;
  createdAt: Date;
  updatedAt: Date;
}

export class {EntityName} {
  private readonly props: {EntityName}Props;

  private constructor(props: {EntityName}Props) {
    this.props = props;
  }

  // Factory Method
  static create(props: Omit<{EntityName}Props, 'id' | 'createdAt' | 'updatedAt'>): {EntityName} {
    return new {EntityName}({
      ...props,
      id: crypto.randomUUID(),
      createdAt: new Date(),
      updatedAt: new Date(),
    });
  }

  // Reconstitution (from DB)
  static reconstitute(props: {EntityName}Props): {EntityName} {
    return new {EntityName}(props);
  }

  // Getters (불변성 유지)
  get id(): string {
    return this.props.id;
  }

  get email(): Email {
    return this.props.email;
  }

  get name(): string {
    return this.props.name;
  }

  // Business Methods
  updateName(name: string): void {
    // 비즈니스 규칙 검증
    if (name.length < 2) {
      throw new ValidationError('name', 'Name must be at least 2 characters');
    }
    this.props.name = name;
    this.props.updatedAt = new Date();
  }

  // Equality
  equals(other: {EntityName}): boolean {
    return this.id === other.id;
  }
}
```

### 3. --with-repository 옵션 시 추가 생성

#### src/domain/interfaces/I{EntityName}Repository.ts
```typescript
import { {EntityName} } from '../entities/{EntityName}';

export interface I{EntityName}Repository {
  findById(id: string): Promise<{EntityName} | null>;
  findAll(): Promise<{EntityName}[]>;
  save(entity: {EntityName}): Promise<void>;
  delete(id: string): Promise<void>;
}
```

### 4. --with-value-objects 옵션 시 추가 생성

#### src/domain/value-objects/{ValueObject}.ts
```typescript
export class Email {
  private readonly value: string;

  private constructor(value: string) {
    this.value = value;
  }

  static create(value: string): Email {
    if (!this.isValid(value)) {
      throw new ValidationError('email', 'Invalid email format');
    }
    return new Email(value);
  }

  private static isValid(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  getValue(): string {
    return this.value;
  }

  equals(other: Email): boolean {
    return this.value === other.value;
  }
}
```

## 출력 예시

```
✅ 엔티티 'User' 생성 완료

생성된 파일:
- src/domain/entities/User.ts
- src/domain/interfaces/IUserRepository.ts
- src/domain/value-objects/Email.ts

엔티티 구조:
- id: string (UUID)
- email: Email (Value Object)
- name: string
- createdAt: Date
- updatedAt: Date

다음 단계:
1. /clean-usecase CreateUser 로 유스케이스 생성
2. Adapters 레이어에서 리포지토리 구현
```

## 엔티티 설계 원칙

1. **불변성**: 가능한 불변 속성 사용
2. **캡슐화**: private 속성 + getter 메서드
3. **비즈니스 로직**: 엔티티 내부에서 처리
4. **검증**: 생성 시점에 유효성 검사
5. **프레임워크 독립**: 순수 TypeScript만 사용

## 참조
- `.claude/skills/clean-architecture/SKILL.md`
- `.claude/best-practices/clean-architecture.md`
