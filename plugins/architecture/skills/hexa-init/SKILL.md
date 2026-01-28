---
name: architecture:hexa-init
description: 프로젝트에 Hexagonal Architecture(Ports & Adapters) 구조를 초기화합니다. Core와 Adapter 디렉토리 구조를 생성합니다.
allowed-tools: Write, Edit, Glob, Read, Bash
argument-hint: [--force]
user-invocable: true
---

# /architecture:hexa-init - Hexagonal Architecture 초기화

## 설명
프로젝트에 Hexagonal Architecture(Ports & Adapters) 구조를 초기화합니다.
Core(Domain + Service + Port)와 Adapter(Driving + Driven) 구조를 생성합니다.

## 사용법
```
/architecture:hexa-init
/architecture:hexa-init --force
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `--force` | 기존 구조가 있어도 덮어쓰기 |

## 실행 순서

### 1. 프로젝트 확인

```
Hexagonal Architecture 구조를 초기화할까요?
- Core 디렉토리 생성 (Domain, Service, Port)
- Adapter 디렉토리 생성 (Driving, Driven)
- 기본 파일 생성
```

### 2. 디렉토리 구조 생성

**Go 프로젝트:**
```
internal/
├── core/                           # Application Core
│   ├── domain/                     # 도메인 모델
│   │   ├── entity/                 # 엔티티
│   │   ├── valueobject/            # 값 객체
│   │   └── event/                  # 도메인 이벤트
│   │
│   ├── service/                    # 애플리케이션 서비스
│   │
│   └── port/                       # 포트 정의
│       ├── driving/                # Driving Ports (Input)
│       └── driven/                 # Driven Ports (Output)
│
├── adapter/                        # 어댑터
│   ├── driving/                    # Driving Adapters (Input)
│   │   └── http/                   # REST API
│   │       └── handler/
│   │
│   └── driven/                     # Driven Adapters (Output)
│       └── persistence/            # 영속화
│
└── config/                         # 설정 및 DI
```

**TypeScript 프로젝트:**
```
src/
├── core/                           # Application Core
│   ├── domain/                     # 도메인 모델
│   │   ├── entities/               # 엔티티
│   │   ├── value-objects/          # 값 객체
│   │   └── events/                 # 도메인 이벤트
│   │
│   ├── services/                   # 애플리케이션 서비스
│   │
│   └── ports/                      # 포트 정의
│       ├── driving/                # Driving Ports (Input)
│       └── driven/                 # Driven Ports (Output)
│
├── adapters/                       # 어댑터
│   ├── driving/                    # Driving Adapters (Input)
│   │   └── http/                   # REST API
│   │
│   └── driven/                     # Driven Adapters (Output)
│       └── persistence/            # 영속화
│
└── config/                         # 설정 및 DI
```

### 3. 기본 파일 생성

**도메인 에러 파일**:
- DomainError: 기본 도메인 에러
- ValidationError: 유효성 검사 에러
- NotFoundError: 리소스 미발견 에러

## 출력 예시

```
Hexagonal Architecture 초기화 완료

생성된 구조:
├── [Core]
│   ├── domain/     (엔티티, 값 객체, 이벤트)
│   ├── service/    (애플리케이션 서비스)
│   └── port/       (Driving/Driven 포트)
│
├── [Adapter]
│   ├── driving/    (HTTP Handler 등)
│   └── driven/     (Repository 구현 등)
│
└── [Config]        (설정, DI 컨테이너)

생성된 파일:
- core/domain/errors.{ext}

다음 단계:
1. Driven Port 정의 (예: UserRepository 인터페이스)
2. Driving Port 정의 (예: UserService 인터페이스)
3. Application Service 구현
4. Adapter 구현
```

## Hexagonal Architecture 핵심 개념

### Port & Adapter 관계

```
┌─────────────────────────────────────────────────────────────┐
│                   Driving Adapters                          │
│               (HTTP Handler, CLI, gRPC)                     │
│                         ▼                                   │
│            ┌──── Driving Ports ────┐                        │
│            │   (Service Interface) │                        │
│            └───────────┬───────────┘                        │
│                        ▼                                    │
│  ┌────────────── Application Core ──────────────┐           │
│  │                                              │           │
│  │   Domain (Entity, Value Object, Event)       │           │
│  │              +                               │           │
│  │   Service (UseCase 구현)                     │           │
│  │                                              │           │
│  └────────────────────┬─────────────────────────┘           │
│                       ▼                                     │
│            ┌──── Driven Ports ────┐                         │
│            │ (Repository, Gateway)│                         │
│            └───────────┬──────────┘                         │
│                        ▼                                    │
│                  Driven Adapters                            │
│            (PostgreSQL, Redis, HTTP Client)                 │
└─────────────────────────────────────────────────────────────┘
```

### Port 종류

| 포트 유형 | 방향 | 역할 | 예시 |
|----------|------|------|------|
| **Driving Port** | 외부 → Core | 애플리케이션이 제공하는 기능 | `UserService` |
| **Driven Port** | Core → 외부 | 애플리케이션이 필요로 하는 기능 | `UserRepository`, `EmailSender` |

### Adapter 종류

| 어댑터 유형 | 역할 | 예시 |
|------------|------|------|
| **Driving Adapter** | Driving Port 호출 | HTTP Handler, CLI, gRPC Server |
| **Driven Adapter** | Driven Port 구현 | PostgresRepository, SMTPEmailSender |

## 언어별 적용

이 스킬은 **공통 구조**만 정의합니다.

**언어별 구현 세부사항**은 반드시 다음 가이드를 따르세요:
- [Hexagonal Architecture 가이드](../best-practices/hexagonal-architecture.md)

가이드에서 확인할 내용:
- 파일명/디렉토리 네이밍 컨벤션
- 언어별 문법 및 관용구
- 의존성 주입 방법
