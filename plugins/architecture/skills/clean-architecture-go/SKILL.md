---
name: clean-architecture-go
description: Go 프로젝트용 클린 아키텍처를 강제합니다. Go 파일(.go) 생성, 구현, 레이어, 도메인, 엔티티, 유스케이스 언급 시 자동 활성화. 의존성 규칙을 엄격하게 검사합니다.
allowed-tools: Read, Glob, Grep
---

# Clean Architecture Go Skill

## 🚨 패시브 자동 활성화 (필수 적용)

> **이 스킬은 Go 프로젝트의 모든 코드 구현 시 자동으로 적용됩니다.**
> 사용자가 명시적으로 요청하지 않아도 Claude는 클린 아키텍처를 적용해야 합니다.

### 1. 항상 활성화되는 상황

| 트리거 | 동작 |
|--------|------|
| **파일 생성/수정** (.go) | 레이어 위치 검증 |
| **go.mod 존재** | Go 프로젝트로 인식 |
| **코드 구현 요청** | 4-레이어 구조 적용 |
| **API/서비스 구현** | 의존성 규칙 검증 |

### 2. 키워드 감지 (추가 활성화)

다음 키워드 감지 시 명시적으로 활성화:
- "구현", "만들어", "작성", "개발", "코드"
- "API", "서비스", "핸들러", "리포지토리"
- "엔티티", "유스케이스", "DTO"
- "레이어", "계층", "아키텍처"

### 3. 파일 경로 감지

다음 경로의 파일 생성/수정 시 해당 레이어 규칙 적용:
| 경로 패턴 | 레이어 | 적용 규칙 |
|-----------|--------|----------|
| `*/internal/domain/*` | Domain | 외부 import 금지 |
| `*/internal/application/*` | Application | Domain만 import |
| `*/internal/adapters/*` | Adapters | Domain, Application만 |
| `*/internal/infrastructure/*` | Infrastructure | 모두 허용 |

### 4. 🚨 코드 생성 전 필수 검증

**Claude는 코드 생성 전 반드시 다음을 확인해야 합니다:**

```
□ 이 코드가 속할 레이어는? (Domain/Application/Adapters/Infrastructure)
□ 해당 레이어의 디렉토리에 파일을 생성하는가?
□ import할 대상이 의존성 규칙을 준수하는가?
□ 금지된 import가 없는가?
```

## 핵심 원칙

### 의존성 규칙 (Dependency Rule)
```
cmd/ → internal/infrastructure → internal/adapters → internal/application → internal/domain
  ↓            ↓                      ↓                     ↓                    ↓
진입점     프레임워크/DB          포트 구현            비즈니스 로직        순수 엔티티
```

**절대 불변의 규칙**: 내부 레이어는 외부 레이어를 절대 참조하지 않습니다.

## Go 표준 프로젝트 구조

### 전체 디렉토리 구조

```
project/
├── cmd/
│   └── server/
│       └── main.go              # 진입점
├── internal/                     # 비공개 패키지
│   ├── domain/                   # 도메인 레이어 (가장 안쪽)
│   │   ├── entity/              # 엔티티
│   │   ├── valueobject/         # 값 객체
│   │   ├── repository/          # 리포지토리 인터페이스
│   │   └── errors/              # 도메인 에러
│   ├── application/              # 애플리케이션 레이어
│   │   ├── usecase/             # 유스케이스
│   │   ├── dto/                 # 데이터 전송 객체
│   │   └── port/                # 외부 서비스 인터페이스
│   ├── adapters/                 # 어댑터 레이어
│   │   ├── handler/             # HTTP 핸들러
│   │   ├── repository/          # 리포지토리 구현
│   │   └── gateway/             # 외부 서비스 구현
│   └── infrastructure/           # 인프라 레이어 (가장 바깥)
│       ├── http/                # HTTP 서버 설정
│       ├── database/            # DB 연결 설정
│       ├── config/              # 환경 설정
│       └── di/                  # 의존성 주입
├── pkg/                          # 공개 패키지 (재사용 가능)
│   └── logger/
├── api/                          # API 스펙
│   └── openapi.yaml
├── go.mod
├── go.sum
└── Makefile
```

### 1. Domain (Entities) - 가장 안쪽

```
internal/domain/
├── entity/
│   └── user.go              # 순수 비즈니스 엔티티
├── valueobject/
│   └── email.go             # 값 객체
├── repository/
│   └── user_repository.go   # 리포지토리 인터페이스
└── errors/
    └── errors.go            # 도메인 에러
```

**규칙**:
- 외부 라이브러리 import 금지 (표준 라이브러리만)
- 프레임워크 코드 참조 금지
- 순수 Go만 사용

### 2. Application (Use Cases)

```
internal/application/
├── usecase/
│   └── user/
│       ├── create_user.go
│       └── get_user.go
├── dto/
│   └── user/
│       ├── create_user_dto.go
│       └── user_response_dto.go
└── port/
    └── email_service.go     # 외부 서비스 인터페이스
```

**규칙**:
- Domain 레이어만 import 가능
- 구현체가 아닌 인터페이스에 의존
- 하나의 유스케이스는 하나의 비즈니스 규칙

### 3. Adapters (Interface Adapters)

```
internal/adapters/
├── handler/
│   └── user_handler.go      # HTTP 핸들러
├── repository/
│   └── postgres_user_repository.go
└── gateway/
    └── sendgrid_email_gateway.go
```

**규칙**:
- Domain, Application만 import 가능
- 포트/인터페이스 구현
- 데이터 변환 담당

### 4. Infrastructure (Frameworks & Drivers) - 가장 바깥

```
internal/infrastructure/
├── http/
│   ├── server.go
│   └── router.go
├── database/
│   └── postgres.go
├── config/
│   └── config.go
└── di/
    └── container.go         # 의존성 주입
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
- [ ] Domain: 외부 import 없이 순수 Go (표준 라이브러리만)
- [ ] Application: Domain만 import, 인터페이스 의존
- [ ] Adapters: 인터페이스 구현, 데이터 변환
- [ ] Infrastructure: DI 컨테이너에서 조립

### 코드 작성 후
- [ ] 레이어 경계 위반 없는지 검증
- [ ] 테스트 가능한 구조인지 확인

## 사용 가능한 명령어

| 명령어 | 설명 |
|--------|------|
| `/architecture:clean-init-go` | Go 프로젝트에 클린 아키텍처 구조 초기화 |
| `/architecture:clean-entity-go <name>` | 새 도메인 엔티티 생성 |
| `/architecture:clean-usecase-go <name>` | 새 유스케이스 생성 |
| `/architecture:clean-validate-go` | 현재 코드의 클린 아키텍처 준수 검증 |

## 참조 문서

- `best-practices/clean-architecture-go.md` - Go용 상세 패턴 및 예제
- `commands/clean-init-go.md` - Go 초기화 명령어
- `skills/clean-architecture-ts/SKILL.md` - TypeScript 클린 아키텍처 스킬
