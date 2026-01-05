---
description: 클린 아키텍처 4-레이어 디렉토리 구조를 초기화합니다. 도메인, 애플리케이션, 어댑터, 인프라 레이어를 자동 생성합니다.
allowed-tools: Write, Edit, Bash
---

# /clean-init - 클린 아키텍처 초기화

## 설명
프로젝트에 클린 아키텍처 디렉토리 구조와 기본 파일들을 생성합니다.

## 사용법
```
/clean-init
```

## 실행 순서

### 1. 디렉토리 구조 생성

다음 디렉토리 구조를 생성합니다:

```
src/
├── domain/
│   ├── entities/
│   ├── value-objects/
│   ├── errors/
│   └── interfaces/
├── application/
│   ├── use-cases/
│   ├── dtos/
│   ├── ports/
│   └── interfaces/
├── adapters/
│   ├── controllers/
│   ├── presenters/
│   ├── repositories/
│   └── gateways/
├── infrastructure/
│   ├── http/
│   ├── database/
│   ├── config/
│   └── di/
└── shared/
    ├── types/
    └── utils/
```

### 2. 기본 파일 생성

#### domain/errors/DomainError.ts
```typescript
export abstract class DomainError extends Error {
  constructor(message: string) {
    super(message);
    this.name = this.constructor.name;
  }
}

export class ValidationError extends DomainError {
  constructor(field: string, message: string) {
    super(`Validation failed for ${field}: ${message}`);
  }
}

export class NotFoundError extends DomainError {
  constructor(entity: string, id: string) {
    super(`${entity} with id ${id} not found`);
  }
}
```

#### application/interfaces/IUseCase.ts
```typescript
export interface IUseCase<TInput, TOutput> {
  execute(input: TInput): Promise<TOutput>;
}
```

#### infrastructure/di/container.ts
```typescript
// 의존성 주입 컨테이너 (tsyringe 또는 수동 구현)
import 'reflect-metadata';

class Container {
  private dependencies = new Map<string, any>();

  register<T>(token: string, implementation: T): void {
    this.dependencies.set(token, implementation);
  }

  resolve<T>(token: string): T {
    const dependency = this.dependencies.get(token);
    if (!dependency) {
      throw new Error(`Dependency ${token} not registered`);
    }
    return dependency;
  }
}

export const container = new Container();
```

### 3. 설정 파일 업데이트

#### tsconfig.json paths 추가
```json
{
  "compilerOptions": {
    "paths": {
      "@domain/*": ["src/domain/*"],
      "@application/*": ["src/application/*"],
      "@adapters/*": ["src/adapters/*"],
      "@infrastructure/*": ["src/infrastructure/*"],
      "@shared/*": ["src/shared/*"]
    }
  }
}
```

### 4. .claude/CLEAN_ARCHITECTURE.md 생성

프로젝트 루트에 클린 아키텍처 가이드 문서를 생성합니다.

## 출력 예시

```
✅ 클린 아키텍처 초기화 완료

생성된 구조:
├── src/domain/          (엔티티 레이어)
├── src/application/     (유스케이스 레이어)
├── src/adapters/        (인터페이스 어댑터 레이어)
├── src/infrastructure/  (프레임워크 레이어)
└── src/shared/          (공유 유틸리티)

생성된 파일:
- domain/errors/DomainError.ts
- application/interfaces/IUseCase.ts
- infrastructure/di/container.ts

다음 단계:
1. /clean-entity User 로 첫 번째 엔티티 생성
2. /clean-usecase CreateUser 로 유스케이스 생성
```

## 참조
- `skills/clean-architecture/SKILL.md`
- `.claude/best-practices/clean-architecture.md`
