# Toolkit Plugin

> **리서치, 문제 해결, 코드 리뷰/커밋, DB 작업 도구**

---

## 문제 해결 매트릭스

| 상황 | 문제점 | 솔루션 | 명령어 |
|------|--------|--------|--------|
| **기술 조사 필요** | 검색 + 요약 반복 작업 | 5-10회 자동 검색 + 핵심 요약 | `/toolkit:research` |
| **버그 발생** | 원인 파악 어려움 | 5 Whys, RCA 방법론 적용 | `/toolkit:solve` |
| **회귀 버그** | 변경 지점 찾기 어려움 | 이분 탐색 방식 | `/toolkit:solve --binary` |
| **복잡한 문제** | 다중 원인 파악 어려움 | Fishbone 분석 | `/toolkit:solve --fishbone` |
| **DB 작업 필요** | 쿼리 작성 부담 | 인터뷰 기반 MongoDB 작업 | `/toolkit:mongodb` |

---

## 명령어

### 리서치 (Research)

| 명령어 | 옵션 | 자연어 | 설명 |
|--------|------|--------|------|
| `/toolkit:research [주제]` | - | "조사해줘" | 기본 리서치 (5회 검색) |
| `/toolkit:research [주제] --quick` | `--quick` | "빠르게 알아봐줘" | 빠른 리서치 (3회 검색) |
| `/toolkit:research [주제] --deep` | `--deep` | "자세히 조사해줘" | 심층 리서치 (10회 검색) |

### 문제 해결 (Solve)

| 명령어 | 옵션 | 자연어 | 설명 |
|--------|------|--------|------|
| `/toolkit:solve [문제]` | - | "해결해줘" | 자동 방법론 선택 |
| `/toolkit:solve [문제] --5whys` | `--5whys` | "5 Whys로 분석해줘" | 5 Whys 방법론 |
| `/toolkit:solve [문제] --rca` | `--rca` | "근본 원인 분석해줘" | Root Cause Analysis |
| `/toolkit:solve [문제] --hypothesis` | `--hypothesis` | "가설 검증해줘" | 가설 기반 분석 |
| `/toolkit:solve [문제] --binary` | `--binary` | "이분 탐색으로 찾아줘" | 이진 탐색 방식 |
| `/toolkit:solve [문제] --fishbone` | `--fishbone` | "Fishbone으로 분석해줘" | 다중 원인 분류 |
| `/toolkit:solve-log` | - | "분석 로그 보여줘" | 진행 중 문제 확인 |
| `/toolkit:solve-history [키워드]` | `--recent`, `--keyword` | "해결 이력 보여줘" | 과거 사례 검색 |
| `/toolkit:solve-report [id]` | `--draft`, `--summary`, `--full` | "보고서 만들어줘" | 해결 보고서 생성 |

### 데이터베이스 (MongoDB)

| 명령어 | 자연어 | 설명 |
|--------|--------|------|
| `/toolkit:mongodb` | "DB 작업해줘" | 인터뷰로 접속 정보 수집 후 작업 |
| `/toolkit:mongodb [작업]` | "사용자 조회해줘" | 작업 힌트와 함께 시작 |

### Git 도구 (Code Review & Commit)

| 명령어 | 자연어 | 설명 |
|--------|--------|------|
| `/toolkit:code-review` | "코드 리뷰해줘" | 최근 변경사항 리뷰 |
| `/toolkit:code-review [범위]` | "최근 3개 커밋 리뷰해줘" | 특정 범위 리뷰 |
| `/toolkit:code-commit` | "커밋해줘" | 변경사항 분석 후 커밋 메시지 생성 |
| `/toolkit:code-commit [힌트]` | "인증 수정 커밋해줘" | 힌트 기반 커밋 메시지 생성 |

---

## 주요 기능 상세

### 1. 리서치 (Research)

**5-10회 자동 검색 + 핵심 요약:**

```mermaid
flowchart LR
    A["리서치 계획"] --> B["다중 검색"]
    B --> C["핵심 추출"]
    C --> D["종합 분석"]
    D --> E["보고서 생성"]
```

**검색 전략:**

| 검색 | 쿼리 | 목적 |
|------|------|------|
| 1 | "{주제} 정의 개념" | 기본 이해 |
| 2 | "{주제} 장점 benefits" | 장점 파악 |
| 3 | "{주제} 단점 problems" | 단점/주의사항 |
| 4 | "{주제} 사용법 how to" | 적용 방법 |
| 5 | "{주제} 예제 example" | 실제 사례 |
| 6 | "{주제} best practices" | 베스트 프랙티스 |
| 7 | "{주제} vs 대안" | 대안 비교 |
| 8 | "{주제} 2024 2025 latest" | 최신 트렌드 |

**사용 예시:**

```bash
# 기본 리서치 (5회 검색)
/toolkit:research OAuth 2.0

# 빠른 리서치 (3회 검색)
/toolkit:research JWT --quick

# 심층 리서치 (10회 검색)
/toolkit:research 클린 아키텍처 --deep
```

**출력 예시:**

```
============================================
 RESEARCH 완료: OAuth 2.0
============================================

 📊 리서치 통계:
 • 검색 횟수: 8회
 • 분석 출처: 15개
 • 추출 포인트: 23개
 • 핵심 인사이트: 5개

 📁 생성된 문서:
 • .claude/research/oauth-2.0/report.md (전체 보고서)
 • .claude/research/oauth-2.0/summary.md (1페이지 요약)
 • .claude/research/oauth-2.0/sources.md (출처 목록)

 🎯 핵심 요약:
 ┌─────────────────────────────────────────┐
 │ OAuth 2.0은 인가 프레임워크로...         │
 │                                          │
 │ 핵심 포인트:                              │
 │ 1. Authorization Code Grant 권장         │
 │ 2. PKCE 필수 적용                        │
 │ 3. Refresh Token Rotation               │
 └─────────────────────────────────────────┘
```

### 2. 문제 해결 (Solve)

**체계적 문제 해결 프로세스:**

```mermaid
flowchart LR
    A["문제 정의"] --> B["정보 수집"]
    B --> C["원인 분석"]
    C --> D["가설 검증"]
    D --> E["해결"]
    E --> F["문서화"]
```

### 문제 해결 방법론

| 방법 | 설명 | 적합한 상황 |
|------|------|------------|
| **5 Whys** | "왜?"를 5번 반복하여 근본 원인 추적 | 단일 원인 문제 |
| **Fishbone** | 원인을 카테고리별로 분류 (사람, 프로세스, 기술) | 복잡한 문제, 다중 원인 |
| **Binary Search** | 변경 지점을 이분 탐색으로 찾기 | 회귀 버그, 빌드 실패 |
| **Hypothesis** | 가설 수립 → 실험 → 검증 반복 | 불확실한 상황 |
| **RCA** | 체계적 근본 원인 분석 | 시스템 장애, 프로덕션 이슈 |

**사용 예시:**

```bash
# 5 Whys 방법론
/toolkit:solve "로그인 시 500 에러" --5whys

# RCA (Root Cause Analysis)
/toolkit:solve "성능 저하" --rca

# 가설 기반 분석
/toolkit:solve "데이터베이스 연결 실패" --hypothesis

# 이진 탐색 방식
/toolkit:solve "빌드 실패" --binary

# 분석 진행 상황 확인
/toolkit:solve-log

# 과거 해결 사례 검색
/toolkit:solve-history 데이터베이스
/toolkit:solve-history --recent

# 해결 보고서 생성
/toolkit:solve-report PROB-001 --full
```

### 5 Whys 출력 예시

```
🔍 5 Whys 분석: 로그인 시 500 에러

═══════════════════════════════════════════════════════════════

Why 1: 왜 500 에러가 발생했는가?
→ 답변: 인증 서버에서 예외가 발생했다

Why 2: 왜 인증 서버에서 예외가 발생했는가?
→ 답변: 데이터베이스 연결이 끊어졌다

Why 3: 왜 데이터베이스 연결이 끊어졌는가?
→ 답변: 커넥션 풀이 고갈되었다

Why 4: 왜 커넥션 풀이 고갈되었는가?
→ 답변: 커넥션이 반환되지 않고 있었다

Why 5: 왜 커넥션이 반환되지 않았는가?
→ 답변: try-finally 블록 없이 커넥션을 사용하고 있었다

═══════════════════════════════════════════════════════════════

🎯 근본 원인:
   커넥션 사용 시 try-finally 패턴 미적용

💡 해결 방안:
   1. 모든 DB 쿼리에 try-finally 패턴 적용
   2. 커넥션 풀 모니터링 추가
   3. 타임아웃 설정 검토
```

---

## 자동 적용 기능 (패시브 스킬)

| 스킬 | 활성화 조건 | 효과 |
|------|------------|------|
| `research` | 조사/리서치 요청 시 | 다중 검색 + 핵심 요약 |
| `solve` | 에러/버그 언급 시 | 5 Whys, RCA 방법론 자동 적용 |
| `mongodb` | DB 작업 요청 시 | 인터뷰 기반 MongoDB 쿼리 실행 |
| `code-review` | 코드 리뷰 요청 시 | 변경사항 분석 및 개선점 제안 |
| `code-commit` | 커밋 요청 시 | 변경사항 분석 및 커밋 메시지 생성 |

**자동 적용 내용:**
- "~에 대해 알아봐줘" → research 스킬 활성화
- "에러가 발생해요" → solve 스킬 활성화
- "DB에서 조회해줘" → mongodb 스킬 활성화
- "코드 리뷰해줘" → code-review 스킬 활성화
- "커밋해줘" → code-commit 스킬 활성화
- 과거 유사 문제 자동 검색 및 참조

---

## 문서 생성 위치

```
.claude/
├── research/                     # 리서치 결과
│   └── {topic}/
│       ├── report.md             # 전체 보고서
│       ├── summary.md            # 1페이지 요약
│       ├── sources.md            # 출처 목록
│       └── raw/                  # 원본 검색 결과
│
└── solve/                        # 문제 해결 보고서
    ├── active/                   # 진행 중인 문제
    └── resolved/                 # 해결된 문제
        └── {problem-id}/
            ├── report.md         # 해결 보고서
            ├── analysis.md       # 분석 과정
            └── solution.md       # 해결 방안
```

---

## 지식 베이스 자동 구축

문제 해결 시 자동으로 지식 베이스가 구축됩니다:

- 해결된 문제는 자동으로 아카이브
- 유사 문제 발생 시 과거 사례 자동 검색
- 패턴 분석을 통한 재발 방지

```bash
# 과거 해결 사례 검색
/toolkit:solve-history 데이터베이스

# 최근 해결 사례
/toolkit:solve-history --recent

# 키워드로 검색
/toolkit:solve-history --keyword 인증
```

---

## 포함 리소스

- **skills/**:
  - `research/` - 웹 검색 기반 정보 수집 및 분석
  - `solve/` - 체계적 문제 해결 방법론
  - `solve-report/` - 해결 보고서 생성
  - `solve-log/` - 진행 상황 확인
  - `solve-history/` - 과거 이력 조회
  - `mongodb/` - MongoDB 데이터베이스 작업
  - `code-review/` - 코드 리뷰 및 개선점 제안
  - `code-commit/` - 변경사항 분석 및 커밋
  - `help/` - 플러그인 도움말
- **skills/solve/methods/**:
  - five-whys.md
  - fishbone.md
  - binary-search.md
  - hypothesis.md
  - rca.md
