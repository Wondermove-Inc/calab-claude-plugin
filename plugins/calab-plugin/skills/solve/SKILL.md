---
name: solve
description: |
  문제 해결 프로세스를 시작합니다. 체계적인 방법론으로 근본 원인을 분석하고 해결합니다.
  USE WHEN: 에러, error, 버그, bug, 문제, problem, 디버깅, debug, 해결, fix, solve,
  오류, 실패, fail, 안됨, 안돼, 작동안함, 동작안함, not working, broken,
  왜 안되지, 이상해, 원인, cause, 분석, analyze, 추적, trace,
  예외, exception, crash, 크래시, 터짐, 죽음, 멈춤, hang,
  느림, slow, 성능, performance, timeout, 타임아웃
argument-hint: "[--5whys|--rca|--hypothesis|--binary] [문제 설명]"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, WebSearch, mcp__tavily__tavily-search]
agent: build-error-resolver
agents:
  primary: build-error-resolver
  orchestration:
    explore: [Explore]
    analyze: [build-error-resolver, Explore]
    research: [deep-researcher]
    fix: [build-error-resolver, code-reviewer]
    validate: [validator]
    reinforce: [reinforcer]
    verify: [code-reviewer, e2e-runner, validator]
---

# /solve - 문제 해결

> **체계적 문제 분석 및 해결**

## 사용법

```bash
/solve "로그인 실패 오류"       # 기본 문제 해결
/solve --5whys "API 응답 지연"  # 5 Whys 기법
/solve --rca "데이터 손실"      # Root Cause Analysis
/solve --hypothesis "버그"      # 가설 기반 접근
/solve --binary "성능 저하"     # Binary Search 디버깅
/solve --log                    # 진행 중인 분석 확인
/solve --report                 # 보고서 생성
/solve --history                # 과거 해결 이력
/solve --help                   # 도움말
```

## 🤖 에이전트 호출 (필수)

> **이 스킬은 단계별로 적절한 에이전트를 호출해야 합니다.**

### 1. 탐색 단계 (문제 파악)

```
Task(
  subagent_type="Explore",
  description="문제 관련 코드 탐색",
  prompt="""
  **역할**: 코드 탐색 전문가

  **목표**: {문제 설명}과 관련된 코드 및 로그 탐색

  **탐색 대상**:
  - 에러 발생 파일/라인
  - 관련 함수 호출 체인
  - 최근 변경 사항 (git log)
  """
)
```

### 2. 분석 단계

```
Task(
  subagent_type="calab-plugin:build-error-resolver",
  description="문제 원인 분석",
  prompt="""
  **역할**: 문제 해결 전문가

  **목표**: 근본 원인 분석

  **방법론**: {--5whys | --rca | --hypothesis | --binary}

  **출력**:
  - 근본 원인 식별
  - 해결 방안 제시
  """
)
```

### 3. 수정 및 검증 단계

```
// 수정
Task(
  subagent_type="calab-plugin:build-error-resolver",
  description="문제 수정",
  prompt="..."
)

// 검증 (필수)
Task(
  subagent_type="calab-plugin:validator",
  description="수정 검증",
  prompt="해결 완전성 확인, 재발 방지 확인..."
)

// 검증 실패 시
Task(
  subagent_type="calab-plugin:reinforcer",
  description="추가 수정",
  prompt="..."
)
```

---

## 인자 파싱

입력: $ARGUMENTS

### 옵션별 라우팅

1. **`--help` 또는 `-h`** → 도움말 출력

2. **`--5whys`** → 5 Whys 기법 적용
   - "왜?"를 5번 반복하여 근본 원인 도달

3. **`--rca`** → Root Cause Analysis 8단계
   - 체계적 원인 분석 프레임워크

4. **`--hypothesis`** → 가설 기반 접근
   - 가설 → 예측 → 검증 사이클

5. **`--binary`** → Binary Search 디버깅
   - 이진 탐색으로 문제 위치 좁히기

6. **`--log [problem-id]`** → `references/log.md` 실행
   - 진행 중인 문제 해결 상태 확인

7. **`--report [problem-id]`** → `references/report.md` 실행
   - 문제 해결 보고서 생성
   - `--draft` 진행 중 보고서
   - `--summary` 1페이지 요약
   - `--full` 상세 보고서

8. **`--history [keyword]`** → `references/history.md` 실행
   - 과거 해결 이력 검색
   - 유사 문제 발견

9. **옵션 없이 문제 설명만** → 기본 6단계 프로세스

## 6단계 문제 해결 프로세스

```
┌─────────────────────────────────────────┐
│           문제 해결 프로세스              │
├─────────────────────────────────────────┤
│                                         │
│  1. 문제 정의 (Define)                   │
│     └── 증상, 조건, 에러 정보, 영향 범위   │
│                                         │
│  2. 정보 수집 (Gather)                   │
│     └── Git 로그, 파일 분석, 스택 트레이스 │
│                                         │
│  3. 원인 분석 (Analyze)                  │
│     └── 5 Whys, RCA, Fishbone, Binary   │
│                                         │
│  4. 가설 검증 (Hypothesize)              │
│     └── 가설 → 예측 → 검증 → 결과        │
│                                         │
│  5. 해결 구현 (Solve)                    │
│     └── 즉시 수정 + 근본 해결 + 예방 조치  │
│                                         │
│  6. 문서화 (Document)                    │
│     └── 보고서 + 지식 베이스 업데이트      │
│                                         │
└─────────────────────────────────────────┘
```

## 분석 기법

### 5 Whys
```
문제: API 응답 지연

Why 1: 왜 응답이 느린가?
→ DB 쿼리가 느림

Why 2: 왜 DB 쿼리가 느린가?
→ 인덱스 없음

Why 3: 왜 인덱스가 없는가?
→ 마이그레이션 누락

Why 4: 왜 마이그레이션이 누락되었나?
→ 리뷰 프로세스 부재

Why 5: 왜 리뷰가 없었나?
→ 체크리스트 미사용

🎯 근본 원인: 마이그레이션 리뷰 체크리스트 미사용
```

### Root Cause Analysis (8단계)
1. 문제 식별
2. 데이터 수집
3. 원인 요소 파악
4. 근본 원인 결정
5. 권장 조치 개발
6. 솔루션 구현
7. 결과 관찰
8. 지식 공유

### 가설 기반 접근
```
가설 1: "캐시 만료가 원인"
예측: 캐시 무효화 시 해결
검증: 캐시 클리어 후 테스트
결과: ❌ 실패 → 다음 가설

가설 2: "DB 연결 풀 고갈"
예측: 연결 풀 증가 시 해결
검증: maxConnections 증가
결과: ✅ 성공 → 근본 원인 확정
```

## 파일 구조

```
.claude/problem-solving/
├── active/                    # 진행 중
│   └── {problem-id}/
│       ├── problem.md         # 문제 정의
│       ├── analysis.md        # 분석 기록
│       ├── hypotheses.md      # 가설 목록
│       └── report-draft.md    # 초안 보고서
│
├── resolved/                  # 해결 완료
│   └── {problem-id}/
│       └── report.md          # 최종 보고서
│
└── knowledge-base/            # 지식 베이스
    └── solutions.json         # 해결 패턴
```

## 에이전트 오케스트레이션

각 단계별 최적의 에이전트 조합:

```
┌─────────────────────────────────────────────────────────┐
│                 에이전트 오케스트레이션                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 탐색 단계 (Explore):                                │
│  └── Explore 에이전트: 관련 코드 및 로그 탐색            │
│                                                         │
│  2. 분석 단계 (Analyze):                                │
│  ├── build-error-resolver: 오류 패턴 분석               │
│  └── Explore 에이전트: 히스토리 및 변경사항 추적          │
│                                                         │
│  3. 리서치 단계 (Research):                             │
│  └── deep-researcher: 유사 문제/해결책 웹 검색           │
│                                                         │
│  4. 수정 단계 (Fix):                                    │
│  ├── build-error-resolver: 코드 수정                    │
│  └── code-reviewer: 수정 코드 검증 (병렬)                │
│                                                         │
│  5. 검증 단계 (Verify):                                 │
│  ├── validator: 해결 완전성 검증 (AC, 재발 방지)         │
│  ├── code-reviewer: 코드 품질 확인                      │
│  └── e2e-runner: 회귀 테스트 실행 (선택)                 │
│                                                         │
│  6. 보강 단계 (Reinforce) - 검증 실패 시:               │
│  └── reinforcer: 누락/미흡 항목 수정                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 병렬 실행 가능 조합

| 조합 | 실행 방식 | 용도 |
|------|----------|------|
| Explore + deep-researcher | 병렬 | 코드탐색 + 웹리서치 동시 |
| build-error-resolver + code-reviewer | 순차 | 수정 → 검증 |
| validator → reinforcer | 순차 | 완전성 검증 → 보강 (필수 체인) |

## 레거시 명령어 호환

| 이전 명령어 | 신규 명령어 |
|------------|------------|
| `/solve` | `/solve` (유지) |
| `/solve-log` | `/solve --log` |
| `/solve-report` | `/solve --report` |
| `/solve-history` | `/solve --history` |

## 지식 베이스

```json
{
  "solutions": [{
    "id": "PROB-014",
    "problem": "API 응답 지연",
    "cause": "인덱스 누락",
    "solution": "마이그레이션 추가",
    "keywords": ["performance", "database", "index"],
    "resolved_at": "2025-01-15"
  }],
  "patterns": [{
    "pattern_id": "PAT-001",
    "keywords": ["timeout", "connection"],
    "likely_causes": ["연결 풀 고갈", "네트워크 이슈"],
    "occurrences": 5
  }]
}
```

## 다음 단계

| 상황 | 권장 명령어 |
|------|------------|
| 문제 발생 | `/solve "문제 설명"` |
| 깊은 분석 필요 | `/solve --5whys` 또는 `--rca` |
| 진행 확인 | `/solve --log` |
| 완료 후 | `/solve --report` |
| 유사 문제 검색 | `/solve --history "키워드"` |

## 참조 파일

### 템플릿 (스킬 내부)

| 용도 | 템플릿 |
|------|--------|
| 문제 정의 | `templates/problem-definition.md` |
| 해결 보고서 | `templates/solution-report.md` |
| 분석 보고서 | `templates/analysis-report.md` |

### 베스트 프랙티스 (스킬 내부)

- `references/testing.md` - 테스트/디버깅
- `references/typescript.md` - TS 에러 패턴

### 추가 참조 (프로젝트 전역)

- `.claude/best-practices/typescript/ts-error-*.md` - 에러 처리 세부 규칙
