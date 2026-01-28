---
name: architecture:validate
description: 현재 프로젝트의 아키텍처 준수 여부를 검증하고 리팩토링 가이드를 제공합니다. Clean Architecture와 Hexagonal Architecture 모두 지원합니다.
allowed-tools: Read, Glob, Grep, Edit, Write
argument-hint: [--fix] [--path=<dir>] [--type=clean|hexa]
user-invocable: true
---

# /architecture:validate - 아키텍처 검증 및 리팩토링

## 설명
현재 프로젝트의 아키텍처 준수 여부를 검증합니다.
의존성 규칙 위반, 레이어/포트 경계 침범을 검사하고 리팩토링 가이드를 제공합니다.

**지원 아키텍처:**
- Clean Architecture (4-Layer)
- Hexagonal Architecture (Ports & Adapters)

## 사용법
```
/architecture:validate
/architecture:validate --path=internal/application
/architecture:validate --fix
/architecture:validate --type=hexa
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `--path=<dir>` | 특정 디렉토리만 검증 |
| `--fix` | 발견된 문제에 대한 리팩토링 실행 |
| `--type=clean\|hexa` | 아키텍처 유형 명시 (자동 감지 가능) |

## 아키텍처 자동 감지

| 구조 | 감지 기준 | 적용 아키텍처 |
|------|----------|--------------|
| `domain/`, `application/`, `adapters/`, `infrastructure/` | 4-Layer 구조 | Clean Architecture |
| `core/`, `adapter/` + `port/` | Port/Adapter 구조 | Hexagonal Architecture |

**혼재 구조 처리 (mono-repo)**:
- 두 구조가 공존하는 경우: `--type` 옵션으로 명시 필요
- `--path` 옵션으로 특정 서비스 디렉토리 지정 시 해당 경로 기준으로 감지
- 감지 실패 시 사용자에게 아키텍처 유형 선택 요청

## 검증 워크플로우

```
분석 → 레포팅 → 개선안 제시 → [사용자 승인] → 리팩토링
```

### 1. 프로젝트 스캔
```
프로젝트 검사 중...
- 경로: [프로젝트 루트]
- 아키텍처: Clean Architecture (자동 감지)
- 파일 수: N개
```

### 2. 의존성 검사

아키텍처별 의존성 규칙은 해당 가이드를 참조합니다:
- **Clean Architecture**: [의존성 규칙](../best-practices/clean-architecture.md#12-의존성-규칙-the-dependency-rule)
- **Hexagonal Architecture**: [Port & Adapter 규칙](../best-practices/hexagonal-architecture.md#3-port-정의)

### 3. 위반 사항 보고

```
🔴 아키텍처 위반 발견: N건

1. [파일 경로:라인]
   ❌ 위반: Domain에서 외부 라이브러리 import
   💡 제안: 값 객체로 분리하거나 표준 라이브러리 사용
   📝 수정 코드: (--fix 옵션 시 자동 적용)

2. [파일 경로:라인]
   ❌ 위반: Application에서 Adapters import
   💡 제안: domain/repository 인터페이스 사용
   📝 수정 코드: (--fix 옵션 시 자동 적용)

3. [파일 경로:라인]
   ❌ 위반: 엔티티 직접 반환
   💡 제안: DTO로 변환하여 반환
   📝 수정 코드: (--fix 옵션 시 자동 적용)
```

### 4. 리팩토링 제안 (--fix 옵션)

```
리팩토링 계획:

1. [파일A] - 인터페이스 추출
   - 현재: 구현체 직접 의존
   - 변경: 인터페이스 추출 및 DI 적용

2. [파일B] - DTO 추가
   - 현재: 엔티티 직접 노출
   - 변경: ResponseDTO 생성 및 변환

리팩토링을 진행할까요? [Y/n]
```

## 검증 체크리스트

### Clean Architecture 검증

#### Domain 레이어
- [ ] 외부 라이브러리 import 없음 (표준 라이브러리 제외)
- [ ] 프레임워크 코드 참조 없음
- [ ] 다른 레이어 import 없음
- [ ] 비즈니스 로직이 엔티티에 캡슐화

#### Application 레이어
- [ ] Domain만 import
- [ ] Adapters/Infrastructure import 없음
- [ ] 구현체가 아닌 인터페이스 의존
- [ ] 유스케이스가 단일 책임 원칙 준수

#### Adapters 레이어
- [ ] Infrastructure import 없음
- [ ] 인터페이스 구현 확인
- [ ] DTO로 레이어 경계 변환

#### Infrastructure 레이어
- [ ] DI 컨테이너에서 의존성 조립

### Hexagonal Architecture 검증

#### Core
- [ ] Adapter import 없음
- [ ] Port를 통해서만 외부와 통신
- [ ] 비즈니스 로직이 Core에 집중

#### Port
- [ ] Core 내부에 정의
- [ ] 도메인 언어 사용
- [ ] 기술적 세부사항 미노출

#### Adapter
- [ ] Core를 import (역방향 X)
- [ ] Port 구현/호출
- [ ] 다른 Adapter 직접 참조 금지

### 공통 검사 항목

- **엔티티 직접 노출**: API 응답에서 엔티티 직접 반환 금지
- **순환 import**: 컴포넌트 간 순환 의존성 금지
- **구현체 의존**: 비즈니스 로직에서 구현체 직접 의존 금지

## 출력 예시

```
아키텍처 검증 완료 (Clean Architecture)

검사 결과:
├── Domain:      12 파일 ✓
├── Application: 8 파일  ✓
├── Adapters:    15 파일 (2 위반)
└── Infrastructure: 10 파일 ✓

위반 사항: 2건

1. adapters/handler/user_handler.go:45
   ❌ 위반: 엔티티 직접 노출 (User 반환)
   💡 제안: UserResponseDto 사용
   📝 수정:
      - return user
      + return dto.UserResponseFrom(user)

2. adapters/repository/user_repo.go:23
   ❌ 위반: infrastructure 패키지 import
   💡 제안: domain/repository 인터페이스 사용
   📝 수정:
      - import "internal/infrastructure/database"
      + // database 연결은 DI로 주입받음

--fix 옵션으로 자동 리팩토링을 실행할 수 있습니다.
```

## 리팩토링 시나리오

### 시나리오 1: 의존성 역전

**문제**: Application에서 Adapters 직접 참조
```go
// ❌ 잘못된 코드
import "internal/adapters/repository"
userRepo := repository.NewPostgresUserRepository(db)
```

**해결**: 인터페이스 추출 + DI
```go
// ✓ 올바른 코드
// domain/repository/user_repository.go (인터페이스)
type UserRepository interface { ... }

// application/usecase/create_user.go
type CreateUserUseCase struct {
    userRepo repository.UserRepository // 인터페이스 의존
}
```

### 시나리오 2: 엔티티 노출 방지

**문제**: API 응답에서 엔티티 직접 반환
```go
// ❌ 잘못된 코드
func (h *Handler) GetUser(c echo.Context) error {
    user, _ := h.usecase.GetUser(ctx, id)
    return c.JSON(200, user) // 엔티티 직접 노출
}
```

**해결**: DTO 변환
```go
// ✓ 올바른 코드
func (h *Handler) GetUser(c echo.Context) error {
    user, _ := h.usecase.GetUser(ctx, id)
    return c.JSON(200, dto.UserResponseFrom(user))
}
```

### 시나리오 3: Port 추출 (Hexagonal)

**문제**: Service에서 외부 서비스 직접 호출
```go
// ❌ 잘못된 코드
func (s *UserService) CreateUser(...) {
    smtp.Send(email, subject, body) // 외부 서비스 직접 호출
}
```

**해결**: Driven Port 정의 + Adapter 구현
```go
// ✓ 올바른 코드
// port/driven/email_sender.go
type EmailSender interface {
    Send(to, subject, body string) error
}

// service/user_service.go
type UserService struct {
    emailSender port.EmailSender // Port 의존
}
```

## 언어별 적용

**언어별 구현 세부사항**은 반드시 다음 가이드를 따르세요:
- [Clean Architecture 가이드](../best-practices/clean-architecture.md)
- [Hexagonal Architecture 가이드](../best-practices/hexagonal-architecture.md)
