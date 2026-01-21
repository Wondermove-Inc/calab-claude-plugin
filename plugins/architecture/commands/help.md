---
description: Architecture 플러그인 도움말을 표시합니다. 모든 명령어와 사용 예시를 확인할 수 있습니다.
allowed-tools: Read
---

# /help - Architecture 플러그인 도움말

## 설명
Architecture 플러그인의 모든 명령어와 사용 예시를 안내합니다.

## 출력 형식

```
╔════════════════════════════════════════════════════════╗
║        🏗️ Architecture Plugin v2.3.0                   ║
║  Clean Architecture Design & Validation (TS, Go)       ║
╚════════════════════════════════════════════════════════╝

📋 플러그인 개요
───────────────────────────────────────────────────────────────
  4-레이어 클린 아키텍처 구조를 자동 생성하고 의존성 규칙을
  검증합니다. TypeScript와 Go 프로젝트를 모두 지원합니다.

  레이어 구조:
    Domain → Application → Adapters → Infrastructure

📌 TypeScript 명령어
───────────────────────────────────────────────────────────────
  /architecture:clean-init-ts
      4-레이어 디렉토리 구조 초기화
      예시: /architecture:clean-init-ts

  /architecture:clean-entity-ts <name>
      도메인 엔티티 생성
      옵션: --with-repository (리포지토리 인터페이스 포함)
      예시: /architecture:clean-entity-ts User --with-repository

  /architecture:clean-usecase-ts <name>
      유스케이스 생성
      옵션: --entity <name> (관련 엔티티 지정)
      예시: /architecture:clean-usecase-ts CreateUser --entity User

  /architecture:clean-validate-ts
      의존성 규칙 검증
      옵션: --fix (위반 사항 자동 수정)
      예시: /architecture:clean-validate-ts --fix

📌 Go 명령어
───────────────────────────────────────────────────────────────
  /architecture:clean-init-go
      Go 4-레이어 디렉토리 구조 초기화
      옵션: --module <name> (Go 모듈명 지정)
      예시: /architecture:clean-init-go --module github.com/myorg/myapp

  /architecture:clean-entity-go <name>
      Go 도메인 엔티티 생성
      옵션: --with-repository, --with-value-objects
      예시: /architecture:clean-entity-go User --with-repository

  /architecture:clean-usecase-go <name>
      Go 유스케이스 생성
      옵션: --entity <name> (관련 엔티티 지정)
      예시: /architecture:clean-usecase-go CreateUser --entity User

  /architecture:clean-validate-go
      Go 의존성 규칙 검증
      옵션: --fix (위반 사항 자동 수정)
      예시: /architecture:clean-validate-go --fix

🔄 자연어 사용 예시
───────────────────────────────────────────────────────────────
  "클린 아키텍처 만들어줘"
      → TypeScript: /architecture:clean-init-ts
      → Go: /architecture:clean-init-go

  "User 엔티티 만들어줘"
      → TypeScript: /architecture:clean-entity-ts User
      → Go: /architecture:clean-entity-go User

  "CreateUser 유스케이스 만들어줘"
      → TypeScript: /architecture:clean-usecase-ts CreateUser
      → Go: /architecture:clean-usecase-go CreateUser

  "아키텍처 검증해줘"
      → TypeScript: /architecture:clean-validate-ts
      → Go: /architecture:clean-validate-go

  💡 프로젝트에 tsconfig.json이 있으면 TypeScript,
     go.mod가 있으면 Go 명령어가 자동 선택됩니다.

🔗 관련 문서
───────────────────────────────────────────────────────────────
  • best-practices/clean-architecture-ts.md - TypeScript 패턴 가이드
  • best-practices/clean-architecture-go.md - Go 패턴 가이드
  • README.md - 플러그인 상세 문서

💡 팁
───────────────────────────────────────────────────────────────
  • TypeScript/Go 코드 작성 시 클린 아키텍처 규칙이 자동 적용됩니다
  • 의존성 위반 시 경고와 함께 수정 방법을 안내합니다
  • --fix 옵션으로 간단한 위반은 자동 수정 가능합니다
```

## 실행 방식

1. 위 형식의 도움말을 콘솔에 출력
2. 현재 프로젝트 언어 감지 시 해당 언어 명령어 강조
