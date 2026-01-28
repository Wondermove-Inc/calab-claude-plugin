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

## 🤖 에이전트 실행 (필수)

**⚠️ 이 스킬이 로드되면 아래 지침을 따라 즉시 Task 도구를 호출하세요.**

### --init 단계

**지금 바로 Task 도구를 호출**하세요:
- `subagent_type`: `"calab-plugin:refactor-cleaner"`
- `description`: `"4-Layer 클린 아키텍처 초기화"`
- `prompt`: 아래 프롬프트 내용 사용

**프롬프트 내용:**
```
**역할**: 클린 아키텍처 전문가

**목표**: 4-Layer 디렉토리 구조 생성

**생성 대상**:
- src/domain/ (entities, value-objects, errors, interfaces)
- src/application/ (use-cases, dtos, ports, interfaces)
- src/adapters/ (controllers, presenters, repositories, gateways)
- src/infrastructure/ (http, database, config, di)
- src/shared/ (types, utils)

**기본 파일**:
- DomainError.ts, IUseCase.ts, IRepository.ts
```

### --entity / --usecase 단계

**Task 도구 호출**:
- `subagent_type`: `"calab-plugin:refactor-cleaner"`
- `description`: `"도메인 엔티티/유스케이스 생성: {이름}"`
- `prompt`: 아래 프롬프트 내용 사용

**프롬프트 내용:**
```
**역할**: 도메인 모델링 전문가

**목표**: {--entity: 엔티티 | --usecase: 유스케이스} 생성

**출력 위치**:
- Entity: src/domain/entities/{Name}.ts
- UseCase: src/application/use-cases/{Name}UseCase.ts

**포함 항목**:
- 타입 정의
- 검증 로직
- Repository 인터페이스 (entity)
- Input/Output DTO (usecase)
```

### --validate 단계

**Task 도구 호출**:
- `subagent_type`: `"calab-plugin:code-reviewer"`
- `description`: `"클린 아키텍처 규칙 검증"`
- `prompt`: 아래 프롬프트 내용 사용

**프롬프트 내용:**
```
**역할**: 아키텍처 검증 전문가

**검증 항목**:
1. 레이어 의존성 규칙 (Domain ← Application ← Adapters ← Infrastructure)
2. 금지된 의존성 없음 (Domain → Application 등)
3. 파일 위치 정확성

**출력**: 위반 사항 목록 + 수정 제안
```

**⚠️ 중요**: 이 지침을 읽고 있다면, 사용자에게 텍스트로 응답하지 말고 **Task 도구를 호출**하세요!

---

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
