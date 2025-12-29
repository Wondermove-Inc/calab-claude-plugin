---
name: clean-architecture
description: 클린 아키텍처를 강제합니다. 코드 구현, 클래스 생성, 레이어, 도메인, 엔티티, 유스케이스 언급 시 자동 활성화. 의존성 규칙을 엄격하게 검사합니다.
allowed-tools: Read, Glob, Grep
---

# Clean Architecture Skill

## 자동 활성화 조건

이 스킬은 다음 키워드가 감지되면 자동으로 활성화됩니다:
- "코드 작성", "구현", "개발"
- "새 기능", "API", "서비스"
- "엔티티", "유스케이스", "리포지토리"
- "클린 아키텍처", "레이어", "계층"

## 핵심 원칙

### 의존성 규칙 (Dependency Rule)
```
Frameworks → Adapters → Application → Domain
    ↓            ↓           ↓          ↓
 외부 의존    포트 구현    비즈니스    순수 엔티티
```

**절대 불변의 규칙**: 내부 레이어는 외부 레이어를 절대 참조하지 않습니다.

## 4개 레이어 구조

### 1. Domain (Entities) - 가장 안쪽
```
src/domain/
├── entities/          # 순수 비즈니스 엔티티
│   └── User.ts       # 프레임워크 독립적
├── value-objects/     # 값 객체
│   └── Email.ts
├── errors/           # 도메인 에러
│   └── DomainError.ts
└── interfaces/       # 리포지토리 인터페이스
    └── IUserRepository.ts
```

**규칙**:
- 외부 라이브러리 import 금지
- 프레임워크 코드 참조 금지
- 순수 TypeScript만 사용

### 2. Application (Use Cases)
```
src/application/
├── use-cases/         # 비즈니스 로직
│   └── user/
│       ├── CreateUserUseCase.ts
│       └── GetUserUseCase.ts
├── dtos/              # 데이터 전송 객체
│   └── user/
│       ├── CreateUserDto.ts
│       └── UserResponseDto.ts
├── ports/             # 외부 서비스 인터페이스
│   └── IEmailService.ts
└── interfaces/        # 유스케이스 인터페이스
    └── IUseCase.ts
```

**규칙**:
- Domain 레이어만 import 가능
- 구현체가 아닌 인터페이스에 의존
- 하나의 유스케이스는 하나의 비즈니스 규칙

### 3. Adapters (Interface Adapters)
```
src/adapters/
├── controllers/       # HTTP 컨트롤러
│   └── UserController.ts
├── presenters/        # 응답 포맷터
│   └── UserPresenter.ts
├── repositories/      # 리포지토리 구현
│   └── PrismaUserRepository.ts
└── gateways/          # 외부 서비스 구현
    └── SendGridEmailGateway.ts
```

**규칙**:
- Domain, Application만 import 가능
- 포트/인터페이스 구현
- 데이터 변환 담당

### 4. Infrastructure (Frameworks & Drivers) - 가장 바깥
```
src/infrastructure/
├── http/              # Express/Fastify 설정
│   ├── server.ts
│   └── routes/
├── database/          # Prisma/TypeORM 설정
│   ├── prisma/
│   └── migrations/
├── config/            # 환경 설정
│   └── index.ts
└── di/                # 의존성 주입
    └── container.ts
```

**규칙**:
- 모든 레이어 import 가능
- 프레임워크 설정만 담당
- 실제 실행 코드

## 코드 작성 시 필수 체크리스트

### 새 파일 생성 전
- [ ] 이 코드가 속할 레이어 결정
- [ ] 해당 레이어의 디렉토리 확인
- [ ] import할 대상이 의존성 규칙 준수하는지 확인

### 코드 작성 중
- [ ] Domain: 외부 import 없이 순수 TypeScript
- [ ] Application: Domain만 import, 인터페이스 의존
- [ ] Adapters: 인터페이스 구현, 데이터 변환
- [ ] Infrastructure: DI 컨테이너에서 조립

### 코드 작성 후
- [ ] 레이어 경계 위반 없는지 검증
- [ ] 테스트 가능한 구조인지 확인

## 사용 가능한 명령어

| 명령어 | 설명 |
|--------|------|
| `/clean-init` | 프로젝트에 클린 아키텍처 구조 초기화 |
| `/clean-entity <name>` | 새 도메인 엔티티 생성 |
| `/clean-usecase <name>` | 새 유스케이스 생성 |
| `/clean-validate` | 현재 코드의 클린 아키텍처 준수 검증 |

## 참조 문서

- `.claude/best-practices/clean-architecture.md` - 상세 패턴 및 예제
- `.claude/commands/clean-init.md` - 초기화 명령어
