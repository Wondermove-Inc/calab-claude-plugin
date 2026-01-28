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
║   Clean & Hexagonal Architecture Design & Validation   ║
╚════════════════════════════════════════════════════════╝

플러그인 개요
───────────────────────────────────────────────────────────────
  프로젝트에 아키텍처 구조를 자동 생성하고 의존성 규칙을 검증합니다.

  지원 아키텍처:
    • Clean Architecture (4-Layer)
    • Hexagonal Architecture (Ports & Adapters)

명령어 목록
───────────────────────────────────────────────────────────────
  /architecture:clean-init
      Clean Architecture 4-레이어 디렉토리 구조 초기화
      옵션: --force (기존 구조 덮어쓰기)
      예시: /architecture:clean-init

  /architecture:hexa-init
      Hexagonal Architecture 구조 초기화 (Core + Adapter)
      옵션: --force (기존 구조 덮어쓰기)
      예시: /architecture:hexa-init

  /architecture:validate
      아키텍처 준수 여부 검증 (Clean/Hexagonal 자동 감지)
      옵션: --fix (위반 사항 자동 수정)
            --path=<dir> (특정 디렉토리만 검증)
            --type=clean|hexa (아키텍처 유형 명시)
      예시: /architecture:validate --fix

자동 활성화 스킬 (패시브)
───────────────────────────────────────────────────────────────
  다음 스킬은 코드 작성 시 자동으로 활성화됩니다:

  • clean-architecture: 4-레이어 프로젝트에서 의존성 규칙 검증
  • hexagonal-architecture: Core/Adapter 프로젝트에서 Port/Adapter 규칙 검증

자연어 사용 예시
───────────────────────────────────────────────────────────────
  "클린 아키텍처 만들어줘"
      → /architecture:clean-init

  "헥사고날 아키텍처 초기화해줘"
      → /architecture:hexa-init

  "아키텍처 검증해줘"
      → /architecture:validate

  "의존성 위반 고쳐줘"
      → /architecture:validate --fix

관련 문서
───────────────────────────────────────────────────────────────
  • Clean Architecture: best-practices/clean-architecture.md
  • Hexagonal Architecture: best-practices/hexagonal-architecture.md

팁
───────────────────────────────────────────────────────────────
  • 코드 작성 시 아키텍처 규칙이 자동 적용됩니다
  • 의존성 위반 시 경고와 함께 수정 방법을 안내합니다
  • --fix 옵션으로 위반 사항에 대한 리팩토링을 실행할 수 있습니다
  • 아키텍처 유형은 디렉토리 구조로 자동 감지됩니다
```

## 실행 방식

1. 위 형식의 도움말을 콘솔에 출력
2. 프로젝트에서 사용 가능한 best-practices 목록 표시
