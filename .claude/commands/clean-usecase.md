# /clean-usecase - 유스케이스 생성

## 설명
클린 아키텍처의 Application 레이어에 새로운 유스케이스를 생성합니다.

## 사용법
```
/clean-usecase <UseCaseName>
/clean-usecase CreateUser
/clean-usecase GetUserById --entity User
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `--entity <name>` | 연관된 엔티티 지정 |
| `--with-dto` | 입출력 DTO 함께 생성 |
| `--with-test` | 유닛 테스트 파일 생성 |

## 실행 순서

### 1. 사용자에게 유스케이스 정보 질문

```
유스케이스 '{UseCaseName}'의 정보를 입력해주세요:
1. 입력 데이터 (Input DTO)
2. 출력 데이터 (Output DTO)
3. 필요한 의존성 (Repository, Service)
4. 비즈니스 규칙
```

### 2. 파일 생성

#### src/application/use-cases/{entity}/{UseCaseName}.ts
```typescript
import { IUseCase } from '../../interfaces/IUseCase';
import { I{Entity}Repository } from '@domain/interfaces/I{Entity}Repository';
import { {Entity} } from '@domain/entities/{Entity}';
import { {UseCaseName}Dto } from '../../dtos/{entity}/{UseCaseName}Dto';
import { {Entity}ResponseDto } from '../../dtos/{entity}/{Entity}ResponseDto';

export class {UseCaseName} implements IUseCase<{UseCaseName}Dto, {Entity}ResponseDto> {
  constructor(
    private readonly {entity}Repository: I{Entity}Repository,
    // 추가 의존성
  ) {}

  async execute(input: {UseCaseName}Dto): Promise<{Entity}ResponseDto> {
    // 1. 비즈니스 규칙 검증
    await this.validateBusinessRules(input);

    // 2. 엔티티 생성/조회
    const entity = {Entity}.create({
      // ...input
    });

    // 3. 영속화
    await this.{entity}Repository.save(entity);

    // 4. 응답 DTO 반환
    return {Entity}ResponseDto.from(entity);
  }

  private async validateBusinessRules(input: {UseCaseName}Dto): Promise<void> {
    // 비즈니스 규칙 검증 로직
  }
}
```

### 3. DTO 파일 생성

#### src/application/dtos/{entity}/{UseCaseName}Dto.ts
```typescript
export interface {UseCaseName}Dto {
  // 입력 필드 정의
  email: string;
  name: string;
}

export class {UseCaseName}DtoValidator {
  static validate(dto: {UseCaseName}Dto): void {
    if (!dto.email) {
      throw new ValidationError('email', 'Email is required');
    }
    if (!dto.name || dto.name.length < 2) {
      throw new ValidationError('name', 'Name must be at least 2 characters');
    }
  }
}
```

#### src/application/dtos/{entity}/{Entity}ResponseDto.ts
```typescript
import { {Entity} } from '@domain/entities/{Entity}';

export class {Entity}ResponseDto {
  readonly id: string;
  readonly email: string;
  readonly name: string;
  readonly createdAt: string;

  private constructor(props: {Entity}ResponseDto) {
    Object.assign(this, props);
  }

  static from(entity: {Entity}): {Entity}ResponseDto {
    return new {Entity}ResponseDto({
      id: entity.id,
      email: entity.email.getValue(),
      name: entity.name,
      createdAt: entity.createdAt.toISOString(),
    });
  }
}
```

### 4. --with-test 옵션 시 테스트 생성

#### tests/unit/use-cases/{UseCaseName}.test.ts
```typescript
import { {UseCaseName} } from '@application/use-cases/{entity}/{UseCaseName}';
import { I{Entity}Repository } from '@domain/interfaces/I{Entity}Repository';

describe('{UseCaseName}', () => {
  let useCase: {UseCaseName};
  let mockRepository: jest.Mocked<I{Entity}Repository>;

  beforeEach(() => {
    mockRepository = {
      findById: jest.fn(),
      findAll: jest.fn(),
      save: jest.fn(),
      delete: jest.fn(),
    };
    useCase = new {UseCaseName}(mockRepository);
  });

  describe('execute', () => {
    it('should create entity successfully', async () => {
      // Arrange
      const input = { email: 'test@example.com', name: 'Test User' };

      // Act
      const result = await useCase.execute(input);

      // Assert
      expect(result.email).toBe(input.email);
      expect(mockRepository.save).toHaveBeenCalled();
    });

    it('should throw error for invalid input', async () => {
      // Arrange
      const input = { email: '', name: '' };

      // Act & Assert
      await expect(useCase.execute(input)).rejects.toThrow();
    });
  });
});
```

## 출력 예시

```
✅ 유스케이스 'CreateUser' 생성 완료

생성된 파일:
- src/application/use-cases/user/CreateUserUseCase.ts
- src/application/dtos/user/CreateUserDto.ts
- src/application/dtos/user/UserResponseDto.ts
- tests/unit/use-cases/CreateUserUseCase.test.ts

의존성:
- IUserRepository (Domain)

다음 단계:
1. Adapters 레이어에서 Controller 구현
2. Infrastructure에서 DI 컨테이너에 등록
```

## 유스케이스 설계 원칙

1. **단일 책임**: 하나의 유스케이스 = 하나의 비즈니스 규칙
2. **인터페이스 의존**: 구현체가 아닌 인터페이스에 의존
3. **순수 비즈니스 로직**: 프레임워크/인프라 코드 금지
4. **입출력 분리**: DTO를 통한 명확한 경계
5. **테스트 용이성**: 의존성 주입으로 Mock 가능

## 참조
- `.claude/skills/clean-architecture/SKILL.md`
- `.claude/best-practices/clean-architecture.md`
