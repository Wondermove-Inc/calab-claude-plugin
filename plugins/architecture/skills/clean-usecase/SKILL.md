---
name: architecture:clean-usecase
description: 유스케이스를 생성합니다. 클린 아키텍처 Application 레이어에 유스케이스와 관련 DTO를 생성합니다.
allowed-tools: Write, Edit, Glob, Read
argument-hint: <UseCaseName> [--entity=<EntityName>]
user-invocable: true
---

# /architecture:clean-usecase - 유스케이스 생성

## 설명
클린 아키텍처의 Application 레이어에 새로운 유스케이스를 생성합니다.

## 사용법
```
/architecture:clean-usecase <UseCaseName>
/architecture:clean-usecase CreateUser
/architecture:clean-usecase GetOrder --entity=Order
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `--entity=<name>` | 연관된 엔티티 지정 (DTO 자동 생성) |

## 실행 순서

### 1. 사용자에게 유스케이스 정보 질문

```
유스케이스 '{UseCaseName}'를 정의해주세요:
1. 입력 파라미터 (예: email, name)
2. 출력 결과 (예: User 정보)
3. 필요한 외부 의존성 (예: Repository, EmailService)
```

### 2. 유스케이스 파일 생성

**생성 위치**: Application 레이어의 유스케이스 디렉토리

**필수 구성 요소**:
- 생성자 (의존성 주입)
- Execute 메서드 (비즈니스 로직)
- 인터페이스 의존 (구현체 아님)

**Execute 메서드 구조**:
```
1. 입력 유효성 검사
2. 비즈니스 규칙 검사
3. 엔티티 생성/조회
4. 영속화
5. 응답 반환
```

### 3. DTO 파일 생성

**Input DTO**:
- 유스케이스 입력 필드
- Validate 메서드

**Response DTO**:
- 유스케이스 출력 필드
- From 메서드 (엔티티 → DTO 변환)

## 출력 예시

```
유스케이스 'CreateUser' 생성 완료

생성된 파일:
- [Application 레이어]/usecase/user/create_user
- [Application 레이어]/dto/user/create_user_input
- [Application 레이어]/dto/user/user_response

유스케이스 구조:
- 입력: CreateUserInput { email, name }
- 출력: UserResponse { id, email, name, createdAt }
- 의존성: UserRepository

다음 단계:
1. Adapters에서 컨트롤러/핸들러 구현
2. Infrastructure에서 DI 컨테이너에 등록
```

## 유스케이스 설계 원칙

1. **단일 책임**: 하나의 유스케이스는 하나의 비즈니스 규칙만 처리
2. **인터페이스 의존**: 구현체가 아닌 인터페이스에 의존
3. **DTO 사용**: 엔티티를 직접 노출하지 않고 DTO로 변환
4. **검증**: 입력 DTO에서 유효성 검사
5. **트랜잭션 경계**: 유스케이스가 트랜잭션의 경계

## 언어별 적용

이 스킬은 **공통 구조**만 정의합니다.

**언어별 구현 세부사항**은 반드시 다음 가이드를 따르세요:
- `best-practices/clean-architecture-{lang}.md`

가이드에서 확인할 내용:
- 파일명/디렉토리 네이밍 컨벤션
- 언어별 문법 및 관용구
- 프레임워크 통합 방법
