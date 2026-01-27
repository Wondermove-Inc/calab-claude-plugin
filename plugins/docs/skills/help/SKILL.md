---
name: docs:help
description: Docs 플러그인 도움말을 표시합니다. 모든 명령어와 사용 예시를 확인할 수 있습니다.
allowed-tools: Read
user-invocable: true
---

# /docs:help - Docs 플러그인 도움말

## 설명
Docs 플러그인의 모든 명령어와 사용 예시를 안내합니다.

## 출력 형식

```
╔════════════════════════════════════════════════════════╗
║              Docs Plugin v1.0.0                        ║
║  Documentation Content Auto-Generation (Docusaurus)    ║
╚════════════════════════════════════════════════════════╝

플러그인 개요
───────────────────────────────────────────────────────────────
  프로젝트를 분석하여 전문적인 기술 문서 콘텐츠를 자동 생성합니다.
  Docusaurus 기반의 문서 사이트 구조를 지원합니다.

  생성 문서 유형:
    - Getting Started (시작하기)
    - Architecture (아키텍처)
    - API Reference (API 레퍼런스)
    - Components (컴포넌트)
    - Guides (가이드)
    - Configuration (설정)
    - FAQ / Troubleshooting

명령어
───────────────────────────────────────────────────────────────
  /docs:docs
      문서 시스템 개요 및 작성 가이드라인 표시
      예시: /docs:docs

  /docs:generate
      프로젝트 분석 후 전체 문서 자동 생성
      옵션: --only, --force, --verbose, --skip-validation
      예시: /docs:generate
            /docs:generate --only=api,components

  /docs:add [type]
      특정 유형의 문서 개별 추가
      유형: getting-started, architecture, api, component, guide, config, faq, troubleshooting
      예시: /docs:add api
            /docs:add guide "인증 설정하기"
            /docs:add component "Button"

  /docs:update
      코드 변경사항 반영하여 기존 문서 업데이트
      옵션: --since, --regenerate, --dry-run, --force
      예시: /docs:update
            /docs:update --since="2024-01-01"

  /docs:status
      문서 커버리지 및 품질 현황 확인
      옵션: --detailed, --json, --type
      예시: /docs:status
            /docs:status --detailed

  /docs:validate
      문서 품질 검증 (구조, 링크, 코드, 일관성, 완성도)
      옵션: --fix, --strict, --json, --quiet
      예시: /docs:validate
            /docs:validate --fix

자연어 사용 예시
───────────────────────────────────────────────────────────────
  "문서 생성해줘"         → /docs:generate
  "API 문서 추가해줘"     → /docs:add api
  "문서 업데이트해줘"     → /docs:update
  "문서 현황 보여줘"      → /docs:status
  "문서 검증해줘"         → /docs:validate

문서 유형별 필수 항목
───────────────────────────────────────────────────────────────
  Getting Started   15개 항목 (설치, 요구사항, 예시 등)
  Architecture      12개 항목 (다이어그램 4개+ 필수)
  API Reference     20개 항목/엔드포인트
  Component         18개 항목/컴포넌트
  Guide             10개 항목
  Configuration      8개 항목/옵션
  FAQ                5개 항목/질문
  Troubleshooting    6개 항목/이슈

문서 생성 위치
───────────────────────────────────────────────────────────────
  .claude/docs-site/
  ├── images/               # 스크린샷 저장
  ├── getting-started/      # 시작 가이드
  ├── architecture/         # 아키텍처 문서
  ├── api-reference/        # API 레퍼런스
  ├── components/           # 컴포넌트 문서
  ├── guides/               # How-to 가이드
  ├── configuration/        # 설정 문서
  ├── faq.md                # 자주 묻는 질문
  └── troubleshooting.md    # 문제 해결

시각화 규칙
───────────────────────────────────────────────────────────────
  Mermaid 다이어그램:
    - 어두운 배경 → 밝은 글자 (#ffffff)
    - 밝은 배경 → 어두운 글자 (#1e293b)
    - Architecture 문서에 필수 4개 이상

  스크린샷 플레이스홀더:
    <!-- 스크린샷 필요: [설명] -->
    ![스크린샷: 설명](./images/filename.png)

관련 문서
───────────────────────────────────────────────────────────────
  • README.md - 플러그인 상세 문서

팁
───────────────────────────────────────────────────────────────
  • 새 프로젝트 문서화 시 /docs:generate로 전체 생성
  • 특정 영역만 필요하면 /docs:add [type] 사용
  • 코드 변경 후 /docs:update로 문서 동기화
  • /docs:validate로 문서 품질 주기적 점검
```

## 실행 방식

1. 위 형식의 도움말을 콘솔에 출력
2. 문서 생성 여부에 따라 다음 추천 명령어 안내
