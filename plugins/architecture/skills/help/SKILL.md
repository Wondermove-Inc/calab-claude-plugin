---
name: architecture:help
description: Architecture 플러그인 도움말을 표시합니다. 모든 명령어와 사용 예시를 확인할 수 있습니다.
allowed-tools: Read
user-invocable: true
---

# /architecture:help - Architecture 플러그인 도움말

## 설명
Architecture 플러그인의 모든 명령어와 사용 예시를 안내합니다.

## 출력 형식

```
╔════════════════════════════════════════════════════════╗
║              Architecture Plugin                       ║
║     Clean Architecture Design & Validation             ║
╚════════════════════════════════════════════════════════╝

플러그인 개요
───────────────────────────────────────────────────────────────
  4-레이어 클린 아키텍처 구조를 자동 생성하고 의존성 규칙을
  검증합니다.

  레이어 구조:
    Infrastructure → Adapters → Application → Domain

명령어 목록
───────────────────────────────────────────────────────────────
  /architecture:clean-init
      4-레이어 디렉토리 구조 초기화
      옵션: --force (기존 구조 덮어쓰기)
      예시: /architecture:clean-init

  /architecture:clean-entity <name>
      도메인 엔티티 생성
      옵션: --with-repository (리포지토리 인터페이스 포함)
            --with-value-objects (값 객체 포함)
      예시: /architecture:clean-entity User --with-repository

  /architecture:clean-usecase <name>
      유스케이스 생성
      옵션: --entity=<name> (관련 엔티티 지정)
      예시: /architecture:clean-usecase CreateUser --entity=User

  /architecture:clean-validate
      의존성 규칙 검증
      옵션: --fix (위반 사항 수정 제안)
            --path=<dir> (특정 디렉토리만 검증)
      예시: /architecture:clean-validate --fix

자연어 사용 예시
───────────────────────────────────────────────────────────────
  "클린 아키텍처 만들어줘"
      → /architecture:clean-init

  "User 엔티티 만들어줘"
      → /architecture:clean-entity User

  "CreateUser 유스케이스 만들어줘"
      → /architecture:clean-usecase CreateUser

  "아키텍처 검증해줘"
      → /architecture:clean-validate

관련 문서
───────────────────────────────────────────────────────────────
  • 언어별 상세 가이드: best-practices/clean-architecture-{lang}.md
  • 플러그인 상세 문서: README.md

팁
───────────────────────────────────────────────────────────────
  • 코드 작성 시 클린 아키텍처 규칙이 자동 적용됩니다
  • 의존성 위반 시 경고와 함께 수정 방법을 안내합니다
  • --fix 옵션으로 위반 사항에 대한 수정 제안을 받을 수 있습니다
```

## 실행 방식

1. 위 형식의 도움말을 콘솔에 출력
2. 프로젝트에서 사용 가능한 best-practices 목록 표시
