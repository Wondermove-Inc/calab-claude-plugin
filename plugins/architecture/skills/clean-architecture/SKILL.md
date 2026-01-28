---
name: architecture:clean-architecture
description: 클린 아키텍처를 강제합니다. 코드 파일 생성, 레이어, 도메인, 엔티티, 유스케이스 언급 시 자동 활성화. 의존성 규칙을 엄격하게 검사합니다.
allowed-tools: Read, Glob, Grep
user-invocable: false
---

# Clean Architecture Skill

## 🚨 패시브 자동 활성화 (필수 적용)

> **이 스킬은 모든 코드 구현 시 자동으로 적용됩니다.**
> 사용자가 명시적으로 요청하지 않아도 Claude는 클린 아키텍처를 적용해야 합니다.

### 활성화 조건

| 트리거 | 동작 |
|--------|------|
| **코드 파일 생성/수정** | 레이어 위치 검증 |
| **코드 구현 요청** | 4-레이어 구조 적용 |
| **API/서비스 구현** | 의존성 규칙 검증 |

### 키워드 감지 (추가 활성화)

다음 키워드 감지 시 명시적으로 활성화:
- "구현", "만들어", "작성", "개발", "코드"
- "API", "서비스", "핸들러", "컨트롤러", "리포지토리"
- "엔티티", "유스케이스", "DTO"
- "레이어", "계층", "아키텍처"

### 🚨 코드 생성 전 필수 검증

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
Infrastructure → Adapters → Application → Domain
      ↓              ↓           ↓          ↓
  프레임워크     포트 구현   비즈니스    순수 엔티티
    /DB                       로직
```

**절대 불변의 규칙**: 내부 레이어는 외부 레이어를 절대 참조하지 않습니다.

## 4-레이어 구조

### 1. Domain (Entities) - 가장 안쪽

**역할**: 핵심 비즈니스 규칙, 엔티티, 값 객체

**포함 요소**:
- Entity: 비즈니스 엔티티
- Value Object: 불변 값 객체
- Repository Interface: 리포지토리 인터페이스 (구현 아님)
- Domain Error: 도메인 에러

**규칙**:
- 외부 라이브러리 import 금지 (표준 라이브러리만)
- 프레임워크 코드 참조 금지
- 순수 언어만 사용

### 2. Application (Use Cases)

**역할**: 비즈니스 유스케이스 구현

**포함 요소**:
- UseCase: 비즈니스 로직 조율
- DTO: 데이터 전송 객체
- Port: 외부 서비스 인터페이스

**규칙**:
- Domain 레이어만 import 가능
- 구현체가 아닌 인터페이스에 의존
- 하나의 유스케이스는 하나의 비즈니스 규칙

### 3. Adapters (Interface Adapters)

**역할**: 포트/인터페이스 구현, 데이터 변환

**포함 요소**:
- Controller/Handler: HTTP 요청 처리
- Repository Impl: 리포지토리 구현
- Gateway: 외부 서비스 구현
- Presenter: 응답 포맷터

**규칙**:
- Domain, Application만 import 가능
- 포트/인터페이스 구현
- 데이터 변환 담당 (toDomain, toPersistence)

### 4. Infrastructure (Frameworks & Drivers) - 가장 바깥

**역할**: 프레임워크 설정, 의존성 조립

**포함 요소**:
- HTTP Server: 웹 서버 설정
- Database: DB 연결 설정
- Config: 환경 설정
- DI Container: 의존성 주입

**규칙**:
- 모든 레이어 import 가능
- 프레임워크 설정만 담당
- DI 컨테이너에서 의존성 조립

## 레이어별 의존성 규칙

| 레이어 | 허용된 Import | 금지된 Import |
|--------|---------------|---------------|
| Domain | 표준 라이브러리만 | Application, Adapters, Infrastructure |
| Application | Domain | Adapters, Infrastructure |
| Adapters | Domain, Application | Infrastructure |
| Infrastructure | 모두 허용 | - |

## 코드 작성 시 필수 체크리스트

### 새 파일 생성 전
- [ ] 이 코드가 속할 레이어 결정
- [ ] 해당 레이어의 디렉토리 확인
- [ ] import할 대상이 의존성 규칙 준수하는지 확인

### 코드 작성 중
- [ ] Domain: 외부 import 없이 순수 언어 사용
- [ ] Application: Domain만 import, 인터페이스 의존
- [ ] Adapters: 인터페이스 구현, 데이터 변환
- [ ] Infrastructure: DI 컨테이너에서 조립

### 코드 작성 후
- [ ] 레이어 경계 위반 없는지 검증
- [ ] 테스트 가능한 구조인지 확인

## 사용 가능한 명령어

| 명령어 | 설명 |
|--------|------|
| `/architecture:clean-init` | 프로젝트에 클린 아키텍처 구조 초기화 |
| `/architecture:validate` | 현재 코드의 아키텍처 준수 검증 |

## 언어별 적용

**언어별 구현 세부사항**은 반드시 다음 가이드를 따르세요:
- [Clean Architecture 가이드](../best-practices/clean-architecture.md)

가이드에서 확인할 내용:
- Go / TypeScript 디렉토리 구조
- 파일명/디렉토리 네이밍 컨벤션
- 언어별 코드 예시

### 지원 언어 및 자동 감지

| 언어 | 감지 기준 |
|------|----------|
| Go | `go.mod` 존재 |
| TypeScript | `tsconfig.json` 존재 |

**언어 감지 규칙**:
- 두 언어 파일이 모두 존재할 경우 (예: mono-repo), 각 언어 섹션 참조
- 단일 언어만 감지되면 해당 언어 섹션만 적용
