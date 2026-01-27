---
name: architecture:clean-init
description: 프로젝트에 클린 아키텍처 구조를 초기화합니다. 4-레이어 디렉토리 구조와 기본 파일을 생성합니다.
allowed-tools: Write, Edit, Glob, Read, Bash
argument-hint: [--force]
user-invocable: true
---

# /architecture:clean-init - 클린 아키텍처 초기화

## 설명
프로젝트에 클린 아키텍처 4-레이어 구조를 초기화합니다.

## 사용법
```
/architecture:clean-init
/architecture:clean-init --force
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `--force` | 기존 구조가 있어도 덮어쓰기 |

## 실행 순서

### 1. 프로젝트 확인

```
클린 아키텍처 구조를 초기화할까요?
- 4-레이어 디렉토리 생성
- 기본 에러 타입 생성
- 예시 엔티티 생성 (선택)
```

### 2. 4-레이어 디렉토리 구조 생성

```
project/
├── [Domain Layer]
│   ├── entity/           # 엔티티
│   ├── valueobject/      # 값 객체
│   ├── repository/       # 리포지토리 인터페이스
│   └── errors/           # 도메인 에러
│
├── [Application Layer]
│   ├── usecase/          # 유스케이스
│   ├── dto/              # 데이터 전송 객체
│   └── port/             # 외부 서비스 인터페이스
│
├── [Adapters Layer]
│   ├── handler/          # HTTP 핸들러/컨트롤러
│   ├── repository/       # 리포지토리 구현
│   └── gateway/          # 외부 서비스 구현
│
└── [Infrastructure Layer]
    ├── http/             # HTTP 서버 설정
    ├── database/         # DB 연결 설정
    ├── config/           # 환경 설정
    └── di/               # 의존성 주입
```

### 3. 기본 파일 생성

**도메인 에러 파일**:
- DomainError: 기본 도메인 에러
- ValidationError: 유효성 검사 에러
- NotFoundError: 리소스 미발견 에러

## 출력 예시

```
클린 아키텍처 초기화 완료

생성된 구조:
├── [Domain Layer]       (엔티티, 값 객체, 인터페이스)
├── [Application Layer]  (유스케이스, DTO)
├── [Adapters Layer]     (핸들러, 리포지토리 구현)
└── [Infrastructure Layer] (서버, DB, 설정)

생성된 파일:
- [Domain Layer]/errors/errors

다음 단계:
1. /architecture:clean-entity User 로 첫 엔티티 생성
2. /architecture:clean-usecase CreateUser 로 유스케이스 생성
```

## 언어별 적용

이 스킬은 **공통 구조**만 정의합니다.

**언어별 구현 세부사항**은 반드시 다음 가이드를 따르세요:
- `best-practices/clean-architecture-{lang}.md`

가이드에서 확인할 내용:
- 파일명/디렉토리 네이밍 컨벤션
- 언어별 문법 및 관용구
- 프레임워크 통합 방법
