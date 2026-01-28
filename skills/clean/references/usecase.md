# /clean --usecase - 유스케이스 생성

> **Application Layer에 유스케이스, DTO, 테스트 생성**

## 사용법

```bash
/clean --usecase CreateUser
/clean --usecase UpdateOrder --with-test
```

## 실행 절차

### Step 1: 유스케이스 정보 수집

사용자에게 질문:

1. **입력 DTO 필드**는 무엇인가요?
   - 예: email, name, password

2. **출력 DTO 필드**는 무엇인가요?
   - 예: id, email, name, createdAt

3. **필요한 의존성**은 무엇인가요?
   - 예: IUserRepository, IEmailService

4. **단위 테스트**를 생성할까요? (Y/N)

### Step 2: Input DTO 생성

**src/application/dtos/{entity}/{UseCaseName}Dto.ts:**

```typescript
// src/application/dtos/user/CreateUserDto.ts

export interface CreateUserInputDto {
  email: string;
  name: string;
  password: string;
}

export interface CreateUserOutputDto {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
}
```

### Step 3: 유스케이스 클래스 생성

**src/application/use-cases/{entity}/{UseCaseName}.ts:**

```typescript
// src/application/use-cases/user/CreateUser.ts

import { IUseCase } from '../../ports/IUseCase';
import { IUserRepository } from '@domain/interfaces/IUserRepository';
import { User } from '@domain/entities/User';
import { Email } from '@domain/value-objects/Email';
import { ValidationError } from '@domain/errors/DomainError';
import { CreateUserInputDto, CreateUserOutputDto } from '../../dtos/user/CreateUserDto';

export class CreateUser implements IUseCase<CreateUserInputDto, CreateUserOutputDto> {
  constructor(
    private readonly userRepository: IUserRepository
  ) {}

  async execute(input: CreateUserInputDto): Promise<CreateUserOutputDto> {
    // 1. Input Validation
    this.validateInput(input);

    // 2. Business Rule Validation
    const email = Email.create(input.email);
    await this.ensureEmailNotExists(email);

    // 3. Create Entity
    const user = User.create({
      email,
      name: input.name,
    });

    // 4. Persist
    await this.userRepository.save(user);

    // 5. Return Output DTO
    return this.toOutputDto(user);
  }

  private validateInput(input: CreateUserInputDto): void {
    if (!input.email) {
      throw new ValidationError('Email is required', 'email');
    }
    if (!input.name || input.name.length < 2) {
      throw new ValidationError('Name must be at least 2 characters', 'name');
    }
  }

  private async ensureEmailNotExists(email: Email): Promise<void> {
    const existing = await this.userRepository.findByEmail(email);
    if (existing) {
      throw new ValidationError('Email already exists', 'email');
    }
  }

  private toOutputDto(user: User): CreateUserOutputDto {
    return {
      id: user.id,
      email: user.email.toString(),
      name: user.name,
      createdAt: user.createdAt,
    };
  }
}
```

### Step 4: 단위 테스트 생성 (선택)

**tests/unit/use-cases/{UseCaseName}.test.ts:**

```typescript
// tests/unit/use-cases/CreateUser.test.ts

import { CreateUser } from '@application/use-cases/user/CreateUser';
import { IUserRepository } from '@domain/interfaces/IUserRepository';
import { User } from '@domain/entities/User';
import { Email } from '@domain/value-objects/Email';
import { ValidationError } from '@domain/errors/DomainError';

describe('CreateUser', () => {
  let createUser: CreateUser;
  let mockUserRepository: jest.Mocked<IUserRepository>;

  beforeEach(() => {
    mockUserRepository = {
      findById: jest.fn(),
      findByEmail: jest.fn(),
      findAll: jest.fn(),
      save: jest.fn(),
      delete: jest.fn(),
      exists: jest.fn(),
    };
    createUser = new CreateUser(mockUserRepository);
  });

  describe('execute', () => {
    // Arrange
    const validInput = {
      email: 'test@example.com',
      name: 'Test User',
      password: 'password123',
    };

    it('should create user when input is valid', async () => {
      // Arrange
      mockUserRepository.findByEmail.mockResolvedValue(null);

      // Act
      const result = await createUser.execute(validInput);

      // Assert
      expect(result.email).toBe(validInput.email);
      expect(result.name).toBe(validInput.name);
      expect(result.id).toBeDefined();
      expect(mockUserRepository.save).toHaveBeenCalledTimes(1);
    });

    it('should throw ValidationError when email already exists', async () => {
      // Arrange
      const existingUser = User.create({
        email: Email.create(validInput.email),
        name: 'Existing User',
      });
      mockUserRepository.findByEmail.mockResolvedValue(existingUser);

      // Act & Assert
      await expect(createUser.execute(validInput))
        .rejects
        .toThrow(ValidationError);
    });

    it('should throw ValidationError when email is empty', async () => {
      // Arrange
      const invalidInput = { ...validInput, email: '' };

      // Act & Assert
      await expect(createUser.execute(invalidInput))
        .rejects
        .toThrow(ValidationError);
    });

    it('should throw ValidationError when name is too short', async () => {
      // Arrange
      const invalidInput = { ...validInput, name: 'A' };

      // Act & Assert
      await expect(createUser.execute(invalidInput))
        .rejects
        .toThrow(ValidationError);
    });
  });
});
```

### Step 5: 완료 보고

```
============================================
 CLEAN USECASE 완료: CreateUser
============================================

 📄 생성된 파일:
 • src/application/dtos/user/CreateUserDto.ts
 • src/application/use-cases/user/CreateUser.ts
 • tests/unit/use-cases/CreateUser.test.ts

 📝 유스케이스 구조:
 • Input: email, name, password
 • Output: id, email, name, createdAt
 • Dependencies: IUserRepository

 🧪 테스트:
 • 정상 케이스: 1개
 • 에러 케이스: 3개

============================================
 다음 단계: /clean --validate
============================================
```

## 유스케이스 설계 규칙

### IUseCase 인터페이스 구현
```typescript
// ✅ Good
class CreateUser implements IUseCase<Input, Output> {
  async execute(input: Input): Promise<Output> { ... }
}
```

### 의존성 주입
```typescript
// ✅ Good - Interface에 의존
constructor(private readonly userRepository: IUserRepository) {}

// ❌ Bad - 구현체에 의존
constructor(private readonly userRepository: PrismaUserRepository) {}
```

### DTO 사용
```typescript
// ✅ Good - DTO로 변환
return this.toOutputDto(user);

// ❌ Bad - Entity 직접 반환
return user;
```

### 단일 책임
```typescript
// ✅ Good - 하나의 유스케이스
CreateUser, UpdateUser, DeleteUser

// ❌ Bad - 여러 책임
UserService.create(), UserService.update(), UserService.delete()
```
