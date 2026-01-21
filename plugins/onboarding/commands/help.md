---
description: Onboarding 플러그인 도움말을 표시합니다. 모든 명령어와 사용 예시를 확인할 수 있습니다.
---

# Onboarding 플러그인 도움말

사용자에게 Onboarding 플러그인의 기능과 명령어를 안내합니다.

## 출력 형식

```
╔════════════════════════════════════════════════════════╗
║          📚 Onboarding Plugin v2.3.0                   ║
║  Project Analysis & Onboarding (5 Context Docs)        ║
╚════════════════════════════════════════════════════════╝

📋 플러그인 개요
───────────────────────────────────────────────────────────────
  기존 프로젝트를 분석하여 5개의 컨텍스트 문서를 자동 생성합니다.
  C4 Model 기반의 아키텍처 분석과 코드 패턴 추출을 지원합니다.

  생성되는 문서:
    1. PROJECT_SUMMARY.md  - 프로젝트 개요, 기술 스택
    2. ARCHITECTURE.md     - C4 Model 기반 아키텍처 다이어그램
    3. CODE_PATTERNS.md    - 컴포넌트, API, 훅 패턴
    4. CONVENTIONS.md      - 코딩 컨벤션, 명명 규칙
    5. DOMAIN_KNOWLEDGE.md - 비즈니스 도메인, 용어 사전

📌 명령어
───────────────────────────────────────────────────────────────
  /onboarding:onboard
      전체 프로젝트 분석 + 5개 컨텍스트 문서 생성
      옵션: --skip-domain (도메인 지식 수집 생략)
      예시: /onboarding:onboard
            /onboarding:onboard --skip-domain

  /onboarding:onboard-quick
      핵심만 빠르게 분석 (최소 컨텍스트 구축)
      예시: /onboarding:onboard-quick

  /onboarding:learn [path]
      특정 영역 심층 학습 (폴더/파일 분석)
      예시: /onboarding:learn src/services
            /onboarding:learn src/components/auth

  /onboarding:context-show
      현재 컨텍스트 문서 표시
      예시: /onboarding:context-show

  /onboarding:context-refresh
      컨텍스트 문서 갱신 (코드 변경 후 사용)
      예시: /onboarding:context-refresh

🔄 자연어 사용 예시
───────────────────────────────────────────────────────────────
  "프로젝트 분석해줘"      → /onboarding:onboard
  "빠르게 파악해줘"        → /onboarding:onboard-quick
  "서비스 폴더 분석해줘"   → /onboarding:learn src/services
  "컨텍스트 보여줘"        → /onboarding:context-show
  "컨텍스트 업데이트해줘"  → /onboarding:context-refresh

📊 분석 프로세스
───────────────────────────────────────────────────────────────
  Phase 1: 프로젝트 스캔
    • 설정 파일 분석 (package.json, tsconfig.json 등)
    • 기술 스택 식별 (Frontend, Backend, DB)
    • 디렉토리 구조 매핑

  Phase 2: 코드 패턴 분석
    • 대표 파일 선정 (컴포넌트, API, 서비스)
    • 패턴 추출 (Props, 상태 관리, 에러 처리)

  Phase 3: 아키텍처 분석 (C4 Model)
    • System Context (Level 1)
    • Container Diagram (Level 2)
    • Component Diagram (Level 3)

  Phase 4: 컨텍스트 문서 생성
    • 5개 Markdown 문서 자동 생성
    • Mermaid 다이어그램 포함

  Phase 5: 도메인 지식 수집
    • 인터뷰 형식으로 비즈니스 정보 수집
    • 용어 사전 정리

📁 문서 생성 위치
───────────────────────────────────────────────────────────────
  .claude/memory/
  ├── PROJECT_SUMMARY.md
  ├── ARCHITECTURE.md
  ├── CODE_PATTERNS.md
  ├── CONVENTIONS.md
  └── DOMAIN_KNOWLEDGE.md

🔗 관련 문서
───────────────────────────────────────────────────────────────
  • best-practices/project-onboarding.md - 온보딩 가이드
  • README.md - 플러그인 상세 문서

💡 팁
───────────────────────────────────────────────────────────────
  • 기존 프로젝트에 처음 투입될 때 /onboarding:onboard 실행
  • 시간이 촉박하면 /onboarding:onboard-quick으로 빠르게 파악
  • 특정 모듈을 집중 학습할 때 /onboarding:learn [path] 사용
  • 코드 변경 후 /onboarding:context-refresh로 문서 동기화
```

## 실행 방식

1. 위 형식의 도움말을 콘솔에 출력
2. 컨텍스트 문서 존재 여부에 따라 추천 명령어 안내
