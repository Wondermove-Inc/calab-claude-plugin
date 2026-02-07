---
name: help
description: Toolkit 플러그인 도움말을 표시합니다. 모든 명령어와 사용 예시를 확인할 수 있습니다.
allowed-tools: Read
disable-model-invocation: true
---

# /help - Toolkit 플러그인 도움말

## 설명
Toolkit 플러그인의 모든 명령어와 사용 예시를 안내합니다.

## 출력 형식

```
╔════════════════════════════════════════════════════════╗
║            🔧 Toolkit Plugin v2.3.0                    ║
║  Research & Problem Solving (5-10 Auto Search)         ║
╚════════════════════════════════════════════════════════╝

📋 플러그인 개요
───────────────────────────────────────────────────────────────
  웹 검색 기반 리서치와 체계적인 문제 해결 방법론을 제공합니다.
  5 Whys, RCA, Fishbone 등 다양한 분석 기법을 지원합니다.

📌 리서치 (Research)
───────────────────────────────────────────────────────────────
  /toolkit:research [주제]
      기본 리서치 (5회 검색)
      예시: /toolkit:research OAuth 2.0

  /toolkit:research [주제] --quick
      빠른 리서치 (3회 검색)
      예시: /toolkit:research JWT --quick

  /toolkit:research [주제] --deep
      심층 리서치 (10회 검색)
      예시: /toolkit:research 클린 아키텍처 --deep

📌 문제 해결 (Solve)
───────────────────────────────────────────────────────────────
  /toolkit:solve [문제]
      자동으로 적합한 방법론 선택
      예시: /toolkit:solve "로그인 시 500 에러"

  /toolkit:solve [문제] --5whys
      5 Whys 방법론 (단일 원인 추적)
      예시: /toolkit:solve "DB 연결 실패" --5whys

  /toolkit:solve [문제] --rca
      Root Cause Analysis (체계적 근본 원인 분석)
      예시: /toolkit:solve "성능 저하" --rca

  /toolkit:solve [문제] --hypothesis
      가설 기반 분석 (가설 수립 → 검증)
      예시: /toolkit:solve "메모리 누수" --hypothesis

  /toolkit:solve [문제] --binary
      이진 탐색 방식 (회귀 버그 추적)
      예시: /toolkit:solve "빌드 실패" --binary

  /toolkit:solve [문제] --fishbone
      Fishbone 분석 (다중 원인 분류)
      예시: /toolkit:solve "응답 지연" --fishbone

📌 문제 해결 보조
───────────────────────────────────────────────────────────────
  /toolkit:solve-log
      진행 중인 문제 분석 로그 확인
      예시: /toolkit:solve-log

  /toolkit:solve-history [키워드]
      과거 해결 사례 검색
      옵션: --recent (최근 사례), --keyword [검색어]
      예시: /toolkit:solve-history 데이터베이스
            /toolkit:solve-history --recent

  /toolkit:solve-report [problem-id]
      해결 보고서 생성
      옵션: --draft, --summary, --full
      예시: /toolkit:solve-report PROB-001 --full

📌 데이터베이스 (MongoDB)
───────────────────────────────────────────────────────────────
  /toolkit:mongodb
      MongoDB 작업 시작 (인터뷰로 접속 정보 수집)
      예시: /toolkit:mongodb

  /toolkit:mongodb [작업 설명]
      작업 힌트와 함께 시작
      예시: /toolkit:mongodb 최근 가입한 사용자 조회
            /toolkit:mongodb 만료된 세션 삭제

📌 Git 도구 (Code Review & Commit)
───────────────────────────────────────────────────────────────
  /toolkit:code-review
      최근 변경사항 리뷰
      예시: /toolkit:code-review
            /toolkit:code-review HEAD~3..HEAD

  /toolkit:code-commit
      변경사항 분석 후 커밋 메시지 생성
      예시: /toolkit:code-commit
            /toolkit:code-commit "인증 기능 수정"

🔄 자연어 사용 예시
───────────────────────────────────────────────────────────────
  "OAuth에 대해 알아봐줘"        → /toolkit:research OAuth
  "자세히 조사해줘"              → /toolkit:research [주제] --deep
  "이 에러 해결해줘"             → /toolkit:solve [에러 내용]
  "근본 원인 분석해줘"           → /toolkit:solve [문제] --rca
  "해결 이력 보여줘"             → /toolkit:solve-history
  "DB에서 사용자 조회해줘"       → /toolkit:mongodb 사용자 조회
  "코드 리뷰해줘"                → /toolkit:code-review
  "커밋해줘"                     → /toolkit:code-commit

📊 문제 해결 방법론
───────────────────────────────────────────────────────────────
  방법론          적합한 상황
  ─────────────   ─────────────────────────────────────
  5 Whys         단일 원인이 예상되는 문제
  RCA            시스템 장애, 프로덕션 이슈
  Hypothesis     원인이 불확실한 상황
  Binary Search  회귀 버그, 특정 변경 지점 찾기
  Fishbone       복잡한 문제, 다중 원인 분석

📁 문서 생성 위치
───────────────────────────────────────────────────────────────
  .claude/
  ├── research/              # 리서치 결과
  │   └── {topic}/
  │       ├── report.md      # 전체 보고서
  │       ├── summary.md     # 1페이지 요약
  │       └── sources.md     # 출처 목록
  │
  └── problem-solving/       # 문제 해결 보고서
      ├── active/            # 진행 중
      └── resolved/          # 해결됨

🔗 관련 문서
───────────────────────────────────────────────────────────────
  • skills/solve/methods/five-whys.md     - 5 Whys 방법론
  • skills/solve/methods/fishbone.md      - Fishbone 분석
  • skills/solve/methods/binary-search.md - 이진 탐색 방식
  • skills/solve/methods/hypothesis.md    - 가설 기반 분석
  • skills/solve/methods/rca.md           - Root Cause Analysis
  • README.md                             - 플러그인 상세 문서

💡 팁
───────────────────────────────────────────────────────────────
  • 에러/버그 언급 시 자동으로 problem-solving 스킬이 활성화됩니다
  • 리서치 결과는 .claude/research/에 자동 저장됩니다
  • 과거 해결 사례가 자동으로 검색되어 참조됩니다
  • --deep 옵션으로 더 깊이 있는 리서치가 가능합니다
```

## 실행 방식

1. 위 형식의 도움말을 콘솔에 출력
2. 최근 리서치/문제 해결 이력이 있으면 관련 정보 표시
