# Clean Architecture Best Practices

## 핵심 원칙

### 의존성 규칙 (The Dependency Rule)

```
                    ┌─────────────────────────┐
                    │   Frameworks & Drivers  │  ← 가장 바깥
                    │  (Infrastructure Layer) │
                    └───────────┬─────────────┘
                                ↓
                    ┌───────────────────────┐
                    │   Interface Adapters   │
                    │    (Adapters Layer)    │
                    └───────────┬────────────┘
                                ↓
                    ┌───────────────────────┐
                    │      Use Cases         │
                    │  (Application Layer)   │
                    └───────────┬────────────┘
                                ↓
                    ┌───────────────────────┐
                    │       Entities         │  ← 가장 안쪽
                    │    (Domain Layer)      │
                    └───────────────────────┘
```

**화살표 방향 = 의존 방향**
- 바깥 레이어는 안쪽 레이어에 의존
- 안쪽 레이어는 바깥 레이어를 절대 모름

---

## Layer 1: Domain (Entities)

### 엔티티 패턴

```typescript
// ✅ 좋은 예: 순수 도메인 엔티티
export class User {
  private constructor(
    private readonly _id: string,
    private _email: Email,
    private _name: string,
    private readonly _createdAt: Date,
    private _updatedAt: Date,
  ) {}

  // Factory Method (생성)
  static create(props: CreateUserProps): User {
    // 비즈니스 규칙 검증
    if (props.name.length < 2) {
      throw new ValidationError('name', 'Must be at least 2 characters');
    }

    return new User(
      crypto.randomUUID(),
      Email.create(props.email),
      props.name,
      new Date(),
      new Date(),
    );
  }

  // Reconstitute (DB에서 복원)
  static reconstitute(props: UserProps): User {
    return new User(
      props.id,
      Email.create(props.email),
      props.name,
      props.createdAt,
      props.updatedAt,
    );
  }

  // Getters
  get id(): string { return this._id; }
  get email(): Email { return this._email; }
  get name(): string { return this._name; }

  // Business Methods
  changeName(newName: string): void {
    if (newName.length < 2) {
      throw new ValidationError('name', 'Must be at least 2 characters');
    }
    this._name = newName;
    this._updatedAt = new Date();
  }

  changeEmail(newEmail: string): void {
    this._email = Email.create(newEmail);
    this._updatedAt = new Date();
  }
}
```

### 값 객체 (Value Object) 패턴

```typescript
// ✅ 이메일 값 객체
export class Email {
  private readonly value: string;

  private constructor(value: string) {
    this.value = value;
  }

  static create(value: string): Email {
    if (!Email.isValid(value)) {
      throw new ValidationError('email', 'Invalid email format');
    }
    return new Email(value.toLowerCase());
  }

  private static isValid(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  getValue(): string {
    return this.value;
  }

  equals(other: Email): boolean {
    return this.value === other.value;
  }

  toString(): string {
    return this.value;
  }
}

// ✅ Money 값 객체
export class Money {
  private constructor(
    private readonly amount: number,
    private readonly currency: string,
  ) {}

  static create(amount: number, currency: string = 'KRW'): Money {
    if (amount < 0) {
      throw new ValidationError('amount', 'Cannot be negative');
    }
    return new Money(amount, currency);
  }

  add(other: Money): Money {
    if (this.currency !== other.currency) {
      throw new DomainError('Cannot add different currencies');
    }
    return new Money(this.amount + other.amount, this.currency);
  }

  multiply(factor: number): Money {
    return new Money(this.amount * factor, this.currency);
  }

  getAmount(): number { return this.amount; }
  getCurrency(): string { return this.currency; }
}
```

### 리포지토리 인터페이스 (Domain에서 정의)

```typescript
// src/domain/interfaces/IUserRepository.ts
import { User } from '../entities/User';

export interface IUserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  findAll(options?: FindAllOptions): Promise<User[]>;
  save(user: User): Promise<void>;
  delete(id: string): Promise<void>;
  exists(id: string): Promise<boolean>;
}

export interface FindAllOptions {
  skip?: number;
  take?: number;
  orderBy?: { field: string; direction: 'asc' | 'desc' };
}
```

---

## Layer 2: Application (Use Cases)

### 유스케이스 패턴

```typescript
// src/application/use-cases/user/CreateUserUseCase.ts
import { IUseCase } from '../../interfaces/IUseCase';
import { IUserRepository } from '@domain/interfaces/IUserRepository';
import { IEmailService } from '../../ports/IEmailService';
import { User } from '@domain/entities/User';
import { CreateUserDto } from '../../dtos/user/CreateUserDto';
import { UserResponseDto } from '../../dtos/user/UserResponseDto';

export class CreateUserUseCase implements IUseCase<CreateUserDto, UserResponseDto> {
  constructor(
    private readonly userRepository: IUserRepository,
    private readonly emailService: IEmailService,
  ) {}

  async execute(input: CreateUserDto): Promise<UserResponseDto> {
    // 1. DTO 유효성 검사
    CreateUserDto.validate(input);

    // 2. 비즈니스 규칙 검사
    const existingUser = await this.userRepository.findByEmail(input.email);
    if (existingUser) {
      throw new ConflictError('User', 'email', input.email);
    }

    // 3. 엔티티 생성
    const user = User.create({
      email: input.email,
      name: input.name,
    });

    // 4. 영속화
    await this.userRepository.save(user);

    // 5. 부수 효과 (선택적)
    await this.emailService.sendWelcomeEmail(user.email.getValue());

    // 6. 응답 DTO 반환
    return UserResponseDto.from(user);
  }
}
```

### DTO 패턴

```typescript
// src/application/dtos/user/CreateUserDto.ts
import { ValidationError } from '@domain/errors/DomainError';

export interface CreateUserDto {
  email: string;
  name: string;
}

export const CreateUserDto = {
  validate(dto: CreateUserDto): void {
    const errors: string[] = [];

    if (!dto.email || !dto.email.includes('@')) {
      errors.push('Valid email is required');
    }
    if (!dto.name || dto.name.length < 2) {
      errors.push('Name must be at least 2 characters');
    }

    if (errors.length > 0) {
      throw new ValidationError('CreateUserDto', errors.join(', '));
    }
  }
};

// src/application/dtos/user/UserResponseDto.ts
import { User } from '@domain/entities/User';

export class UserResponseDto {
  readonly id: string;
  readonly email: string;
  readonly name: string;
  readonly createdAt: string;

  private constructor(props: Omit<UserResponseDto, 'from'>) {
    Object.assign(this, props);
  }

  static from(user: User): UserResponseDto {
    return new UserResponseDto({
      id: user.id,
      email: user.email.getValue(),
      name: user.name,
      createdAt: user.createdAt.toISOString(),
    });
  }
}
```

### 포트 인터페이스 (외부 서비스)

```typescript
// src/application/ports/IEmailService.ts
export interface IEmailService {
  sendWelcomeEmail(to: string): Promise<void>;
  sendPasswordResetEmail(to: string, token: string): Promise<void>;
}

// src/application/ports/IPaymentGateway.ts
export interface IPaymentGateway {
  charge(amount: number, customerId: string): Promise<PaymentResult>;
  refund(paymentId: string): Promise<void>;
}

export interface PaymentResult {
  success: boolean;
  transactionId?: string;
  error?: string;
}
```

---

## Layer 3: Adapters (Interface Adapters)

### 컨트롤러 패턴

```typescript
// src/adapters/controllers/UserController.ts
import { Request, Response, NextFunction } from 'express';
import { CreateUserUseCase } from '@application/use-cases/user/CreateUserUseCase';
import { GetUserUseCase } from '@application/use-cases/user/GetUserUseCase';

export class UserController {
  constructor(
    private readonly createUserUseCase: CreateUserUseCase,
    private readonly getUserUseCase: GetUserUseCase,
  ) {}

  async create(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const result = await this.createUserUseCase.execute({
        email: req.body.email,
        name: req.body.name,
      });

      res.status(201).json({ data: result });
    } catch (error) {
      next(error);
    }
  }

  async getById(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const result = await this.getUserUseCase.execute({
        id: req.params.id,
      });

      res.status(200).json({ data: result });
    } catch (error) {
      next(error);
    }
  }
}
```

### 리포지토리 구현 패턴

```typescript
// src/adapters/repositories/PrismaUserRepository.ts
import { PrismaClient } from '@prisma/client';
import { IUserRepository, FindAllOptions } from '@domain/interfaces/IUserRepository';
import { User } from '@domain/entities/User';
import { Email } from '@domain/value-objects/Email';

export class PrismaUserRepository implements IUserRepository {
  constructor(private readonly prisma: PrismaClient) {}

  async findById(id: string): Promise<User | null> {
    const data = await this.prisma.user.findUnique({
      where: { id },
    });

    if (!data) return null;

    return this.toDomain(data);
  }

  async findByEmail(email: string): Promise<User | null> {
    const data = await this.prisma.user.findUnique({
      where: { email },
    });

    if (!data) return null;

    return this.toDomain(data);
  }

  async save(user: User): Promise<void> {
    const data = this.toPersistence(user);

    await this.prisma.user.upsert({
      where: { id: user.id },
      update: data,
      create: data,
    });
  }

  async delete(id: string): Promise<void> {
    await this.prisma.user.delete({
      where: { id },
    });
  }

  // Mapper: DB → Domain
  private toDomain(data: any): User {
    return User.reconstitute({
      id: data.id,
      email: data.email,
      name: data.name,
      createdAt: data.createdAt,
      updatedAt: data.updatedAt,
    });
  }

  // Mapper: Domain → DB
  private toPersistence(user: User): any {
    return {
      id: user.id,
      email: user.email.getValue(),
      name: user.name,
      createdAt: user.createdAt,
      updatedAt: user.updatedAt,
    };
  }
}
```

### 게이트웨이 구현 패턴

```typescript
// src/adapters/gateways/SendGridEmailGateway.ts
import sgMail from '@sendgrid/mail';
import { IEmailService } from '@application/ports/IEmailService';

export class SendGridEmailGateway implements IEmailService {
  constructor(apiKey: string) {
    sgMail.setApiKey(apiKey);
  }

  async sendWelcomeEmail(to: string): Promise<void> {
    await sgMail.send({
      to,
      from: 'noreply@example.com',
      subject: 'Welcome!',
      text: 'Welcome to our service!',
    });
  }

  async sendPasswordResetEmail(to: string, token: string): Promise<void> {
    await sgMail.send({
      to,
      from: 'noreply@example.com',
      subject: 'Password Reset',
      text: `Reset your password: ${token}`,
    });
  }
}
```

---

## Layer 4: Infrastructure (Frameworks & Drivers)

### 의존성 주입 컨테이너

```typescript
// src/infrastructure/di/container.ts
import { PrismaClient } from '@prisma/client';
import { PrismaUserRepository } from '@adapters/repositories/PrismaUserRepository';
import { SendGridEmailGateway } from '@adapters/gateways/SendGridEmailGateway';
import { CreateUserUseCase } from '@application/use-cases/user/CreateUserUseCase';
import { UserController } from '@adapters/controllers/UserController';

// 인프라 의존성
const prisma = new PrismaClient();
const emailGateway = new SendGridEmailGateway(process.env.SENDGRID_API_KEY!);

// 리포지토리
const userRepository = new PrismaUserRepository(prisma);

// 유스케이스
const createUserUseCase = new CreateUserUseCase(userRepository, emailGateway);
const getUserUseCase = new GetUserUseCase(userRepository);

// 컨트롤러
export const userController = new UserController(createUserUseCase, getUserUseCase);
```

### HTTP 서버 설정

```typescript
// src/infrastructure/http/server.ts
import express from 'express';
import { userRoutes } from './routes/userRoutes';
import { errorHandler } from './middleware/errorHandler';

export function createServer() {
  const app = express();

  app.use(express.json());
  app.use('/api/v1/users', userRoutes);
  app.use(errorHandler);

  return app;
}

// src/infrastructure/http/routes/userRoutes.ts
import { Router } from 'express';
import { userController } from '../di/container';

const router = Router();

router.post('/', (req, res, next) => userController.create(req, res, next));
router.get('/:id', (req, res, next) => userController.getById(req, res, next));

export const userRoutes = router;
```

---

## 금지 사항

### Domain 레이어에서 금지

```typescript
// ❌ 금지: 프레임워크 import
import { PrismaClient } from '@prisma/client';
import { Injectable } from '@nestjs/common';

// ❌ 금지: 인프라 import
import { config } from '@infrastructure/config';

// ❌ 금지: 어댑터 import
import { UserController } from '@adapters/controllers/UserController';
```

### Application 레이어에서 금지

```typescript
// ❌ 금지: 어댑터 import
import { PrismaUserRepository } from '@adapters/repositories';

// ❌ 금지: 인프라 import
import { prisma } from '@infrastructure/database';

// ✅ 허용: 인터페이스 의존
import { IUserRepository } from '@domain/interfaces/IUserRepository';
```

### 엔티티 직접 노출 금지

```typescript
// ❌ 금지: 엔티티 직접 반환
async getUser(id: string): Promise<User> {
  return this.userRepository.findById(id);
}

// ✅ 올바름: DTO로 변환하여 반환
async getUser(id: string): Promise<UserResponseDto> {
  const user = await this.userRepository.findById(id);
  return UserResponseDto.from(user);
}
```

---

## 코드 작성 체크리스트

### 새 파일 생성 전
- [ ] 이 코드가 속할 레이어 결정 (Domain/Application/Adapters/Infrastructure)
- [ ] 해당 레이어의 디렉토리에 파일 생성 확인
- [ ] import할 대상이 의존성 규칙 준수하는지 확인

### Domain 레이어 작성 시
- [ ] 외부 라이브러리 import 없음
- [ ] 프레임워크 코드 참조 없음
- [ ] 순수 TypeScript만 사용
- [ ] 엔티티는 Factory Method (create) + Reconstitute 패턴 사용
- [ ] 값 객체는 불변 + equals 메서드 구현

### Application 레이어 작성 시
- [ ] Domain 레이어만 import
- [ ] 구현체가 아닌 인터페이스에 의존 (IRepository, IService)
- [ ] 하나의 유스케이스는 하나의 비즈니스 규칙만 담당
- [ ] DTO 유효성 검사 포함
- [ ] 엔티티 직접 반환 금지, DTO로 변환

### Adapters 레이어 작성 시
- [ ] Domain, Application만 import
- [ ] 포트/인터페이스 구현
- [ ] toDomain/toPersistence 매퍼 구현
- [ ] 컨트롤러에서 try-catch 에러 처리

### Infrastructure 레이어 작성 시
- [ ] DI 컨테이너에서 의존성 조립
- [ ] 환경 변수 설정 관리
- [ ] 프레임워크 초기화 코드만 배치

### 코드 작성 후
- [ ] 레이어 경계 위반 없는지 검증
- [ ] 테스트 가능한 구조인지 확인
- [ ] 의존성 역전 원칙 준수

---

## 테스트 전략

### 유닛 테스트 (Use Case)

```typescript
describe('CreateUserUseCase', () => {
  let useCase: CreateUserUseCase;
  let mockUserRepository: jest.Mocked<IUserRepository>;
  let mockEmailService: jest.Mocked<IEmailService>;

  beforeEach(() => {
    mockUserRepository = {
      findById: jest.fn(),
      findByEmail: jest.fn(),
      save: jest.fn(),
      delete: jest.fn(),
    };
    mockEmailService = {
      sendWelcomeEmail: jest.fn(),
      sendPasswordResetEmail: jest.fn(),
    };
    useCase = new CreateUserUseCase(mockUserRepository, mockEmailService);
  });

  it('should create user successfully', async () => {
    mockUserRepository.findByEmail.mockResolvedValue(null);

    const result = await useCase.execute({
      email: 'test@example.com',
      name: 'Test User',
    });

    expect(result.email).toBe('test@example.com');
    expect(mockUserRepository.save).toHaveBeenCalled();
    expect(mockEmailService.sendWelcomeEmail).toHaveBeenCalledWith('test@example.com');
  });

  it('should throw error for duplicate email', async () => {
    mockUserRepository.findByEmail.mockResolvedValue(User.create({
      email: 'test@example.com',
      name: 'Existing',
    }));

    await expect(useCase.execute({
      email: 'test@example.com',
      name: 'New User',
    })).rejects.toThrow(ConflictError);
  });
});
```

---

## 참조

- Robert C. Martin, "Clean Architecture" (2017)
- `skills/clean-architecture-ts/SKILL.md`
- `commands/clean-init-ts.md`
