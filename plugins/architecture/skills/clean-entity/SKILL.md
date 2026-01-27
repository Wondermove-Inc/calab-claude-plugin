---
name: architecture:clean-entity
description: 도메인 엔티티를 생성합니다. 클린 아키텍처 Domain 레이어에 엔티티, 값 객체, 리포지토리 인터페이스를 생성합니다.
allowed-tools: Write, Edit, Glob, Read
argument-hint: <EntityName> [--with-repository] [--with-value-objects]
user-invocable: true
---

# /architecture:clean-entity - 도메인 엔티티 생성

## 설명
클린 아키텍처의 Domain 레이어에 새로운 엔티티를 생성합니다.

## 사용법
```
/architecture:clean-entity <EntityName>
/architecture:clean-entity User
/architecture:clean-entity Product --with-repository
/architecture:clean-entity Order --with-value-objects
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `--with-repository` | 리포지토리 인터페이스도 함께 생성 |
| `--with-value-objects` | 관련 값 객체 생성 |

## 실행 순서

### 1. 사용자에게 엔티티 속성 질문

```
엔티티 '{EntityName}'의 속성을 정의해주세요:
1. 필수 속성 (예: email, name)
2. 선택 속성 (예: bio, avatar)
3. 값 객체로 분리할 속성 (예: Email, Money)
```

### 2. 엔티티 파일 생성

**생성 위치**: Domain 레이어의 엔티티 디렉토리

**필수 구성 요소**:
- Private 필드 (캡슐화)
- Factory Method (`create` 또는 `New{Entity}`)
- Reconstitute Method (DB에서 복원)
- Getter 메서드 (불변성 유지)
- Business Method (비즈니스 로직)
- Equals Method (동등성 비교)

### 3. --with-repository 옵션 시 추가 생성

**리포지토리 인터페이스** (Domain 레이어에 위치):
- `FindByID(id)` - ID로 조회
- `FindAll()` - 전체 조회
- `Save(entity)` - 저장 (생성/수정)
- `Delete(id)` - 삭제

### 4. --with-value-objects 옵션 시 추가 생성

**값 객체** (Domain 레이어에 위치):
- Private 생성자
- Factory Method (유효성 검사 포함)
- Getter 메서드
- Equals 메서드

## 출력 예시

```
엔티티 'User' 생성 완료

생성된 파일:
- [Domain 레이어]/entity/user (또는 entities/User)
- [Domain 레이어]/repository/user_repository (--with-repository)
- [Domain 레이어]/valueobject/email (--with-value-objects)

엔티티 구조:
- id: string (UUID)
- email: Email (Value Object)
- name: string
- createdAt: DateTime
- updatedAt: DateTime

다음 단계:
1. /architecture:clean-usecase CreateUser 로 유스케이스 생성
2. Adapters 레이어에서 리포지토리 구현
```

## 엔티티 설계 원칙

1. **불변성**: 가능한 불변 속성 사용 (private 필드 + getter)
2. **캡슐화**: 비공개 필드 + 공개 메서드
3. **비즈니스 로직**: 엔티티 내부에서 처리
4. **검증**: 생성 시점에 유효성 검사 (Factory Method)
5. **프레임워크 독립**: 순수 언어만 사용

## 언어별 적용

이 스킬은 **공통 구조**만 정의합니다.

**언어별 구현 세부사항**은 반드시 다음 가이드를 따르세요:
- `best-practices/clean-architecture-{lang}.md`

가이드에서 확인할 내용:
- 파일명/디렉토리 네이밍 컨벤션
- 언어별 문법 및 관용구
- 프레임워크 통합 방법
