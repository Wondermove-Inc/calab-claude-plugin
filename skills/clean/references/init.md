# /clean --init - 4-Layer 구조 초기화

> **클린 아키텍처 디렉토리 구조 및 기본 파일 생성**

## 실행 절차

### Step 1: 기존 구조 확인

```bash
# src/ 디렉토리 존재 여부 확인
ls -la src/

# 이미 클린 아키텍처 구조인지 확인
ls src/domain src/application src/adapters src/infrastructure 2>/dev/null
```

**이미 존재하면:**
```
⚠️ 클린 아키텍처 구조가 이미 존재합니다.
계속하면 기존 파일을 덮어씁니다.
계속하시겠습니까? (Y/N)
```

### Step 2: 디렉토리 구조 생성

```
src/
├── domain/                    # 도메인 레이어
│   ├── entities/              # 엔티티
│   ├── value-objects/         # 값 객체
│   ├── errors/                # 도메인 에러
│   │   └── DomainError.ts
│   └── interfaces/            # 리포지토리 인터페이스
│
├── application/               # 애플리케이션 레이어
│   ├── use-cases/             # 유스케이스
│   ├── dtos/                  # DTO
│   ├── ports/                 # 포트 인터페이스
│   │   └── IUseCase.ts
│   └── interfaces/            # 서비스 인터페이스
│
├── adapters/                  # 어댑터 레이어
│   ├── controllers/           # 컨트롤러
│   ├── presenters/            # 프레젠터
│   ├── repositories/          # 리포지토리 구현
│   └── gateways/              # 외부 서비스
│
├── infrastructure/            # 인프라 레이어
│   ├── http/                  # HTTP 설정
│   ├── database/              # DB 연결
│   ├── config/                # 설정
│   └── di/                    # 의존성 주입
│       └── container.ts
│
└── shared/                    # 공유 모듈
    ├── types/                 # 공통 타입
    └── utils/                 # 유틸리티
```

### Step 3: 기본 파일 생성

**DomainError.ts:**
```typescript
// src/domain/errors/DomainError.ts

export abstract class DomainError extends Error {
  constructor(
    message: string,
    public readonly code: string
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }

  abstract toJSON(): Record<string, unknown>;
}

export class ValidationError extends DomainError {
  constructor(
    message: string,
    public readonly field?: string
  ) {
    super(message, 'VALIDATION_ERROR');
  }

  toJSON() {
    return {
      code: this.code,
      message: this.message,
      field: this.field,
    };
  }
}

export class NotFoundError extends DomainError {
  constructor(
    public readonly entity: string,
    public readonly id: string
  ) {
    super(`${entity} not found: ${id}`, 'NOT_FOUND');
  }

  toJSON() {
    return {
      code: this.code,
      message: this.message,
      entity: this.entity,
      id: this.id,
    };
  }
}
```

**IUseCase.ts:**
```typescript
// src/application/ports/IUseCase.ts

export interface IUseCase<TInput, TOutput> {
  execute(input: TInput): Promise<TOutput>;
}
```

**container.ts:**
```typescript
// src/infrastructure/di/container.ts

type Factory<T> = () => T;

class Container {
  private services = new Map<string, Factory<unknown>>();
  private singletons = new Map<string, unknown>();

  register<T>(key: string, factory: Factory<T>): void {
    this.services.set(key, factory);
  }

  registerSingleton<T>(key: string, factory: Factory<T>): void {
    this.services.set(key, () => {
      if (!this.singletons.has(key)) {
        this.singletons.set(key, factory());
      }
      return this.singletons.get(key);
    });
  }

  resolve<T>(key: string): T {
    const factory = this.services.get(key);
    if (!factory) {
      throw new Error(`Service not found: ${key}`);
    }
    return factory() as T;
  }
}

export const container = new Container();
```

### Step 4: tsconfig.json 업데이트

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

### Step 5: 완료 보고

```
============================================
 CLEAN INIT 완료
============================================

 📁 생성된 구조:
 • src/domain/          (entities, value-objects, errors, interfaces)
 • src/application/     (use-cases, dtos, ports, interfaces)
 • src/adapters/        (controllers, presenters, repositories, gateways)
 • src/infrastructure/  (http, database, config, di)
 • src/shared/          (types, utils)

 📄 생성된 파일:
 • src/domain/errors/DomainError.ts
 • src/application/ports/IUseCase.ts
 • src/infrastructure/di/container.ts

 ⚙️ 업데이트된 설정:
 • tsconfig.json (paths 추가)

============================================
 다음 단계: /clean --entity {엔티티명}
============================================
```

## 의존성 규칙 (참고)

```
✅ Domain → (없음)
✅ Application → Domain
✅ Adapters → Application, Domain
✅ Infrastructure → 모든 레이어

❌ Domain → Application
❌ Domain → Adapters
❌ Domain → Infrastructure
❌ Application → Adapters
❌ Application → Infrastructure
```
