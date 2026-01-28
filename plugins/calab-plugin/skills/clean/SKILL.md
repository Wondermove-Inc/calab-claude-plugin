---
name: clean
description: |
  클린 아키텍처를 관리합니다. 4-Layer 구조 초기화, 엔티티 생성, 유스케이스 구현, 규칙 검증을 수행합니다.
  USE WHEN: 클린, clean, 아키텍처, architecture, 레이어, layer, 4-layer,
  도메인, domain, 엔티티, entity, 유스케이스, usecase, use case,
  인터페이스, interface, 포트, port, 어댑터, adapter,
  헥사고날, hexagonal, DDD, domain driven,
  리포지토리, repository, 서비스, service,
  의존성, dependency, 역전, inversion, DIP, SOLID,
  분리, separation, 경계, boundary,
  모듈, module, 계층, 구조, structure
argument-hint: "[--init|--entity|--usecase|--validate] [이름]"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
agent: refactor-cleaner
agents:
  primary: refactor-cleaner
  orchestration:
    init: [refactor-cleaner]
    entity: [refactor-cleaner, code-reviewer]
    usecase: [refactor-cleaner, code-reviewer]
    validate: [code-reviewer, project-guardian, refactor-cleaner]
---

# /clean - 클린 아키텍처

> **4-Layer 클린 아키텍처 구조 관리**

## 사용법

```bash
/clean --init              # 4-Layer 디렉토리 구조 초기화
/clean --entity User       # 도메인 엔티티 생성
/clean --usecase CreateUser # 유스케이스 생성
/clean --validate          # 아키텍처 규칙 검증
/clean --validate --fix    # 검증 + 자동 수정
/clean --help              # 도움말
```

## 인자 파싱

입력: $ARGUMENTS

### 옵션별 라우팅

1. **`--help` 또는 `-h`** → 도움말 출력

2. **`--init`** → `references/init.md` 실행
   - 4-Layer 디렉토리 구조 생성
   - 기본 파일 생성 (DomainError, IUseCase 등)

3. **`--entity [이름]`** → `references/entity.md` 실행
   - 도메인 엔티티 클래스 생성
   - Value Object 생성 (선택)
   - Repository 인터페이스 생성 (선택)

4. **`--usecase [이름]`** → `references/usecase.md` 실행
   - Application 레이어 유스케이스 생성
   - Input/Output DTO 생성
   - 단위 테스트 생성 (선택)

5. **`--validate`** → `references/validate.md` 실행
   - 레이어 의존성 규칙 검증
   - 파일 위치 검증
   - `--fix` 옵션으로 자동 수정

## 4-Layer 구조

```
src/
├── domain/              # 도메인 레이어 (핵심)
│   ├── entities/        # 엔티티
│   ├── value-objects/   # 값 객체
│   ├── errors/          # 도메인 에러
│   └── interfaces/      # 리포지토리 인터페이스
│
├── application/         # 애플리케이션 레이어
│   ├── use-cases/       # 유스케이스
│   ├── dtos/            # DTO
│   ├── ports/           # 포트 인터페이스
│   └── interfaces/      # 서비스 인터페이스
│
├── adapters/            # 어댑터 레이어
│   ├── controllers/     # 컨트롤러
│   ├── presenters/      # 프레젠터
│   ├── repositories/    # 리포지토리 구현체
│   └── gateways/        # 외부 서비스 게이트웨이
│
├── infrastructure/      # 인프라 레이어
│   ├── http/            # HTTP 설정
│   ├── database/        # DB 연결
│   ├── config/          # 설정
│   └── di/              # 의존성 주입
│
└── shared/              # 공유 모듈
    ├── types/           # 공통 타입
    └── utils/           # 유틸리티
```

## 의존성 규칙

```
┌─────────────────────────────────────────┐
│           의존성 흐름 (안쪽→바깥쪽)        │
├─────────────────────────────────────────┤
│                                         │
│    ┌───────────────────────────┐       │
│    │        Domain             │       │
│    │   (외부 의존성 없음)         │       │
│    └───────────────────────────┘       │
│                 ▲                       │
│    ┌───────────────────────────┐       │
│    │      Application          │       │
│    │   (Domain만 의존)          │       │
│    └───────────────────────────┘       │
│                 ▲                       │
│    ┌───────────────────────────┐       │
│    │       Adapters            │       │
│    │ (Domain + Application 의존) │       │
│    └───────────────────────────┘       │
│                 ▲                       │
│    ┌───────────────────────────┐       │
│    │     Infrastructure        │       │
│    │    (모든 레이어 의존)        │       │
│    └───────────────────────────┘       │
│                                         │
└─────────────────────────────────────────┘
```

### 금지된 의존성

```
❌ Domain → Application
❌ Domain → Adapters
❌ Domain → Infrastructure
❌ Application → Adapters
❌ Application → Infrastructure
```

## 레거시 명령어 호환

| 이전 명령어 | 신규 명령어 |
|------------|------------|
| `/clean-init` | `/clean --init` |
| `/clean-entity` | `/clean --entity` |
| `/clean-usecase` | `/clean --usecase` |
| `/clean-validate` | `/clean --validate` |

## 실행 순서 권장

```
1. /clean --init         # 구조 초기화
      ↓
2. /clean --entity User  # 엔티티 생성
      ↓
3. /clean --usecase CreateUser  # 유스케이스 생성
      ↓
4. /clean --validate     # 규칙 검증
```

## 다음 단계

| 완료 후 | 권장 명령어 |
|--------|------------|
| /clean --init | `/clean --entity {이름}` |
| /clean --entity | `/clean --usecase {이름}` |
| /clean --usecase | `/dev --build` 또는 `/clean --validate` |
| /clean --validate | 위반 사항 수정 |

## 참조 파일

### 템플릿 (스킬 내부)

| 용도 | 템플릿 |
|------|--------|
| 아키텍처 설계 | `templates/architecture-template.md` |

### 베스트 프랙티스 (스킬 내부)

- `references/clean-architecture.md` - **클린 아키텍처 (최우선)**
- `references/typescript.md` - TypeScript 패턴
- `references/api-design.md` - API 설계
