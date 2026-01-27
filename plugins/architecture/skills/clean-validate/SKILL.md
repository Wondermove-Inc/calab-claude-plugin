---
name: architecture:clean-validate
description: 현재 코드의 클린 아키텍처 준수 여부를 검증합니다. 의존성 규칙 위반, 레이어 경계 침범을 검사합니다.
allowed-tools: Read, Glob, Grep
argument-hint: [--fix] [--path=<dir>]
user-invocable: true
---

# /architecture:clean-validate - 클린 아키텍처 검증

## 설명
현재 프로젝트의 클린 아키텍처 준수 여부를 검증합니다.
의존성 규칙 위반, 레이어 경계 침범, 금지된 import를 검사합니다.

## 사용법
```
/architecture:clean-validate
/architecture:clean-validate --path=internal/application
/architecture:clean-validate --fix
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `--path=<dir>` | 특정 디렉토리만 검증 |
| `--fix` | 발견된 문제에 대한 수정 제안 |

## 검증 항목

### 1. 의존성 규칙 검사

| 레이어 | 허용된 Import | 금지된 Import |
|--------|---------------|---------------|
| Domain | 표준 라이브러리만 | Application, Adapters, Infrastructure |
| Application | Domain | Adapters, Infrastructure |
| Adapters | Domain, Application | Infrastructure |
| Infrastructure | 모두 허용 | - |

### 2. 레이어별 검사 내용

#### Domain 레이어
- [ ] 외부 라이브러리 import 없음 (표준 라이브러리 제외)
- [ ] 프레임워크 코드 참조 없음
- [ ] 다른 레이어 import 없음

#### Application 레이어
- [ ] Domain만 import
- [ ] Adapters/Infrastructure import 없음
- [ ] 구현체가 아닌 인터페이스 의존

#### Adapters 레이어
- [ ] Infrastructure import 없음
- [ ] 인터페이스 구현 확인

#### Infrastructure 레이어
- [ ] DI 컨테이너에서 의존성 조립

### 3. 공통 검사 항목

- **엔티티 직접 노출**: API 응답에서 엔티티 직접 반환 금지
- **순환 import**: 레이어 간 순환 의존성 금지
- **구현체 의존**: Application에서 구현체 직접 의존 금지

## 실행 순서

### 1. 프로젝트 스캔
```
프로젝트 검사 중...
- 경로: [프로젝트 루트]
- 파일 수: N개
```

### 2. 레이어별 검사
```
[Domain] 검사 중...
  ✓ entity/user - 규칙 준수
  ✗ entity/order - 위반 발견

[Application] 검사 중...
  ✓ usecase/user/create_user - 규칙 준수
  ✗ usecase/order/create_order - 위반 발견
```

### 3. 위반 사항 보고

```
🔴 클린 아키텍처 위반 발견: N건

1. [파일 경로:라인]
   위반: Domain에서 외부 라이브러리 import
   제안: 값 객체로 분리하거나 표준 라이브러리 사용

2. [파일 경로:라인]
   위반: Application에서 Adapters import
   제안: domain/repository 인터페이스 사용

3. [파일 경로:라인]
   위반: 엔티티 직접 반환
   제안: DTO로 변환하여 반환
```

## 출력 예시

```
클린 아키텍처 검증 완료

검사 결과:
├── Domain:      12 파일 ✓
├── Application: 8 파일  ✓
├── Adapters:    15 파일 (2 위반)
└── Infrastructure: 10 파일 ✓

위반 사항: 2건
1. adapters/handler/user_handler:45 - 엔티티 직접 노출
2. adapters/repository/user_repo:23 - 순환 import

권장 조치:
1. UserHandler에서 UserResponseDto 사용
2. user_repo의 import 경로 수정

--fix 옵션으로 수정 제안을 받을 수 있습니다.
```

## 검증 체크리스트

### 필수 검증
- [ ] 의존성 방향이 안쪽으로만 향하는가
- [ ] Domain이 순수한가 (외부 의존성 없음)
- [ ] Application이 인터페이스에만 의존하는가
- [ ] 엔티티가 직접 노출되지 않는가

### 권장 검증
- [ ] 테스트 가능한 구조인가
- [ ] DTO가 레이어 경계에서 사용되는가
- [ ] 에러가 도메인 에러로 래핑되는가

## 언어별 적용

이 스킬은 **공통 구조**만 정의합니다.

**언어별 구현 세부사항**은 반드시 다음 가이드를 따르세요:
- `best-practices/clean-architecture-{lang}.md`

가이드에서 확인할 내용:
- 파일명/디렉토리 네이밍 컨벤션
- 언어별 문법 및 관용구
- 프레임워크 통합 방법
