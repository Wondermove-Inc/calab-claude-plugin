---
name: architecture:hexagonal-architecture
description: Hexagonal Architecture(Ports & Adapters)를 강제합니다. Core, Port, Adapter 관련 코드 작성 시 자동 활성화. 포트와 어댑터 규칙을 엄격하게 검사합니다.
allowed-tools: Read, Glob, Grep
user-invocable: false
---

# Hexagonal Architecture Skill

## 패시브 자동 활성화 (필수 적용)

> **이 스킬은 Hexagonal Architecture 프로젝트에서 자동으로 적용됩니다.**
> 사용자가 명시적으로 요청하지 않아도 Claude는 Hexagonal Architecture를 적용해야 합니다.

### 활성화 조건

| 트리거 | 동작 |
|--------|------|
| **core/, adapter/ 디렉토리 존재** | Hexagonal Architecture 적용 |
| **port/ 디렉토리 존재** | Port/Adapter 패턴 적용 |
| **코드 구현 요청** | Core/Adapter 분리 검증 |

### 키워드 감지 (추가 활성화)

다음 키워드 감지 시 명시적으로 활성화:
- "포트", "어댑터", "hexagonal", "port", "adapter"
- "driving", "driven", "input", "output"
- "core", "서비스", "리포지토리"

### 코드 생성 전 필수 검증

**Claude는 코드 생성 전 반드시 다음을 확인해야 합니다:**

```
□ 이 코드가 속할 위치는? (Core 또는 Adapter)
□ Core라면: Domain, Service, Port 중 어디?
□ Adapter라면: Driving 또는 Driven?
□ Port 구현/사용 관계가 올바른가?
□ Core가 Adapter를 import하지 않는가?
```

## 핵심 원칙

### Port & Adapter 규칙

```
┌─────────────────────────────────────────────────────────────┐
│                   Driving Adapters                          │
│               (HTTP Handler, CLI, gRPC)                     │
│                    호출 →                                   │
├─────────────────────────────────────────────────────────────┤
│                   Driving Ports                             │
│               (Service Interfaces)                          │
├─────────────────────────────────────────────────────────────┤
│                  Application Core                           │
│     Domain (Entity, Value Object) + Service                 │
├─────────────────────────────────────────────────────────────┤
│                    Driven Ports                             │
│          (Repository, Gateway Interfaces)                   │
│                    ← 구현                                   │
├─────────────────────────────────────────────────────────────┤
│                   Driven Adapters                           │
│            (PostgreSQL, Redis, HTTP Client)                 │
└─────────────────────────────────────────────────────────────┘
```

**절대 불변의 규칙**: Core는 Adapter를 절대 참조하지 않습니다. (Port만 참조)

## 구조 정의

### 1. Application Core

**역할**: 비즈니스 로직의 핵심

**구성 요소**:
- **Domain**: Entity, Value Object, Domain Event
- **Service**: 비즈니스 로직 구현 (Driving Port 구현)
- **Port**: 외부와의 인터페이스 정의

**규칙**:
- 외부 프레임워크 의존 금지
- Adapter import 금지
- 순수 비즈니스 로직만 포함

### 2. Driving Port (Input Port)

**역할**: 애플리케이션이 제공하는 기능 정의

**예시**:
- `UserService` interface
- `OrderService` interface
- `PaymentService` interface

**규칙**:
- Core 내부에 정의
- 도메인 언어 사용 (기술적 용어 X)
- Service가 이 인터페이스를 구현

### 3. Driven Port (Output Port)

**역할**: 애플리케이션이 필요로 하는 외부 기능 정의

**예시**:
- `UserRepository` interface
- `EmailSender` interface
- `PaymentGateway` interface

**규칙**:
- Core 내부에 정의
- 도메인 언어 사용
- Driven Adapter가 이 인터페이스를 구현

### 4. Driving Adapter (Input Adapter)

**역할**: 외부에서 애플리케이션을 호출

**예시**:
- HTTP Handler/Controller
- CLI Command
- gRPC Server
- Message Consumer

**규칙**:
- Driving Port를 호출
- Core를 import
- 요청/응답 변환 담당

### 5. Driven Adapter (Output Adapter)

**역할**: 애플리케이션이 외부 시스템을 사용

**예시**:
- PostgresUserRepository
- SMTPEmailSender
- StripePaymentGateway
- RedisCache

**규칙**:
- Driven Port를 구현
- Core를 import
- 외부 시스템과 통신

## 의존성 규칙

| 컴포넌트 | 허용된 Import | 금지된 Import |
|----------|---------------|---------------|
| Domain | 표준 라이브러리만 | Service, Port, Adapter |
| Service | Domain, Driven Port | Adapter |
| Driving Port | Domain | Service, Adapter |
| Driven Port | Domain | Service, Adapter |
| Driving Adapter | Core 전체 | Driven Adapter |
| Driven Adapter | Core 전체 | Driving Adapter |

## 코드 작성 시 필수 체크리스트

### 새 파일 생성 전
- [ ] 이 코드가 Core인가 Adapter인가?
- [ ] Core라면 어떤 컴포넌트? (Domain, Service, Port)
- [ ] Adapter라면 Driving인가 Driven인가?
- [ ] 올바른 디렉토리에 생성하는가?

### Port 정의 시
- [ ] Core 내부에 정의했는가?
- [ ] 도메인 언어를 사용했는가?
- [ ] 기술적 세부사항이 노출되지 않았는가?

### Service 구현 시
- [ ] Driving Port를 구현하는가?
- [ ] Driven Port만 의존하는가? (구현체 X)
- [ ] 비즈니스 로직만 포함하는가?

### Adapter 구현 시
- [ ] 올바른 Port를 구현/호출하는가?
- [ ] Core를 import하는가? (역방향 X)
- [ ] 기술적 변환만 담당하는가?

## 사용 가능한 명령어

| 명령어 | 설명 |
|--------|------|
| `/architecture:hexa-init` | 프로젝트에 Hexagonal Architecture 구조 초기화 |
| `/architecture:validate` | 현재 코드의 Hexagonal Architecture 준수 검증 |

## 언어별 적용

이 스킬은 **공통 구조**만 정의합니다.

**언어별 구현 세부사항**은 반드시 다음 가이드를 따르세요:
- [Hexagonal Architecture 가이드](../best-practices/hexagonal-architecture.md)

### 지원 언어 및 자동 감지

| 언어 | 감지 기준 | Core 위치 |
|------|----------|-----------|
| Go | `go.mod` 존재 | `internal/core/` |
| TypeScript | `tsconfig.json` 존재 | `src/core/` |

**언어 감지 규칙**:
- 두 언어 파일이 모두 존재할 경우, **모든 해당 가이드를 참조**
- 단일 언어만 감지되면 해당 가이드만 적용

## Clean Architecture와의 비교

| 관점 | Clean Architecture | Hexagonal Architecture |
|------|-------------------|----------------------|
| 구조 | 4개 레이어 동심원 | Core + Port + Adapter |
| 초점 | 레이어 간 의존성 방향 | Port/Adapter 대칭 구조 |
| 장점 | 명확한 레이어 분리 | 어댑터 교체 용이 |
| 적합한 경우 | 복잡한 도메인 | 다양한 외부 시스템 연동 |

### 선택 기준

**Clean Architecture 선택**:
- 복잡한 도메인 로직이 핵심인 경우
- 명확한 레이어 분리가 필요한 경우
- 팀이 레이어 기반 구조에 익숙한 경우

**Hexagonal Architecture 선택**:
- 다양한 입력/출력 어댑터가 필요한 경우
- 외부 시스템 교체가 빈번한 경우
- 테스트 용이성이 중요한 경우
