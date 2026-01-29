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
skills: [code-quality, best-practices, project-rules]
agents:
  primary: root-cause-finder
  orchestration:
    explore: [Explore]
    analyze: [calab-plugin:root-cause-finder, Explore]
    research: [calab-plugin:deep-researcher]
    fix: [calab-plugin:bug-fixer, calab-plugin:code-reviewer]
    validate: [calab-plugin:validator]
    reinforce: [calab-plugin:reinforcer]
    verify: [calab-plugin:code-reviewer, calab-plugin:e2e-runner, calab-plugin:validator]
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

## 🤖 에이전트 실행 (필수)

**⚠️ 이 스킬이 로드되면 아래 지침을 따라 즉시 Task 도구를 호출하세요.**

### 1. 탐색 단계 (문제 파악)

**지금 바로 Task 도구를 호출**하세요:
- `subagent_type`: `"Explore"`
- `description`: `"문제 관련 코드 탐색"`
- `prompt`: 아래 프롬프트 내용 사용

**프롬프트 내용:**
```
**역할**: 코드 탐색 전문가

**목표**: {문제 설명}과 관련된 코드 및 로그 탐색

**탐색 대상**:
- 에러 발생 파일/라인
- 관련 함수 호출 체인
- 최근 변경 사항 (git log)
```

### 2. 분석 단계 (Root Cause Analysis)

**Task 도구 호출**:
```python
Task(
    subagent_type="calab-plugin:root-cause-finder",
    description="근본 원인 분석",
    prompt="""
    **역할**: 문제 해결 전문가

    **목표**: 근본 원인 분석

    **방법론**: {--5whys | --rca | --hypothesis}
    - 5whys: 반복 질문으로 근본 원인 도달
    - rca: 8단계 체계적 분석
    - hypothesis: 가설 검증 사이클

    **문제 정보**:
    {에러 메시지, 스택 트레이스, 관련 파일}

    **🚨 산출물 필수 (CRITICAL)**:
    1. problem-id 생성: PROB-{YYYYMMDD}-{NNN} 형식
    2. 문제 정의서 생성: `.claude/problem-solving/active/{problem-id}/problem.md`
    3. 분석 기록 생성: `.claude/problem-solving/active/{problem-id}/analysis.md`
    ※ 산출물 미생성 시 작업 실패로 간주

    **출력**:
    - 근본 원인 식별 (confidence: high/medium/low)
    - 해결 방안 제시 (P0/P1/P2 우선순위)
    - 생성된 산출물 경로
    """,
    run_in_background=True
)
```

### 3. 수정 단계 (Bug Fix with TDD)

**Task 도구 호출**:
```python
Task(
    subagent_type="calab-plugin:bug-fixer",
    description="버그 수정 (TDD)",
    prompt="""
    **역할**: TDD 버그 수정 전문가

    **목표**: 근본 원인 기반 수정

    **Root Cause**: {root_cause_finder 결과}
    **권장 수정**: {recommended_fix}
    **problem-id**: {이전 단계에서 생성된 problem-id}

    **TDD 워크플로우**:
    1. RED: 버그 재현 테스트 작성 (실패해야 함)
    2. GREEN: 수정 적용 (테스트 통과)
    3. REFACTOR: 코드 정리

    **수정 후 검증**:
    - 회귀 테스트 실행
    - 전체 테스트 스위트 확인

    **🚨 산출물 필수 (CRITICAL)**:
    1. 수정 보고서 생성: `.claude/problem-solving/resolved/{problem-id}/fix-report.md`
    2. active → resolved 폴더로 이동
    ※ 산출물 미생성 시 작업 실패로 간주
    """,
    run_in_background=True
)
```

### 4. 검증 단계

**4-1. 검증 필수 (Task 도구 호출)**:
```python
Task(
    subagent_type="calab-plugin:validator",
    description="수정 검증",
    prompt="""
    **역할**: 완전성 검증 전문가

    **목표**: 해결 완전성 확인

    **problem-id**: {이전 단계에서 사용된 problem-id}

    **검증 항목**:
    - 버그 재현 테스트 통과
    - 회귀 테스트 통과
    - 엣지 케이스 처리
    - 재발 방지 조치 확인
    - 산출물 존재 확인:
      - `.claude/problem-solving/resolved/{problem-id}/fix-report.md`
      - `.claude/problem-solving/resolved/{problem-id}/analysis.md`

    **🚨 산출물 필수 (CRITICAL)**:
    1. 검증 보고서 생성: `.claude/problem-solving/resolved/{problem-id}/validation-report.md`
    2. 지식 베이스 업데이트: `.claude/problem-solving/knowledge-base/solutions.json`
    ※ 산출물 미생성 시 작업 실패로 간주
    """
)
```

**4-2. 검증 실패 시 (Task 도구 호출)**:
```python
if validator_result == "reinforcer 필요":
    Task(
        subagent_type="calab-plugin:reinforcer",
        description="추가 수정",
        prompt="""
        **역할**: 누락/미흡 항목 수정 전문가

        **목표**: validator 결과 기반 누락 항목 수정

        **problem-id**: {problem-id}
        **검증 결과**: {validator_result}

        **🚨 산출물 필수 (CRITICAL)**:
        1. 수정 보고서 업데이트: `.claude/problem-solving/resolved/{problem-id}/reinforcer-report.md`
        ※ 산출물 미생성 시 작업 실패로 간주
        """
    )
```

**⚠️ 중요**: 이 지침을 읽고 있다면, 사용자에게 텍스트로 응답하지 말고 **Task 도구를 호출**하세요!

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
│  ├── root-cause-finder: 근본 원인 분석                  │
│  │   └── 5 Whys / RCA / Hypothesis 방법론              │
│  └── Explore 에이전트: 히스토리 및 변경사항 추적          │
│                                                         │
│  3. 리서치 단계 (Research):                             │
│  └── deep-researcher: 유사 문제/해결책 웹 검색           │
│                                                         │
│  4. 수정 단계 (Fix):                                    │
│  ├── bug-fixer: TDD 기반 버그 수정                      │
│  │   └── RED → GREEN → REFACTOR                        │
│  └── code-reviewer: 수정 코드 검증 (병렬)                │
│                                                         │
│  5. 검증 단계 (Verify):                                 │
│  ├── validator: 해결 완전성 검증 (재발 방지)             │
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

## /dev 워크플로우 연동

### 언제 dev 워크플로우로 전환하는가?

| 상황 | 액션 |
|------|------|
| **단순 버그 수정** | solve 내에서 bug-fixer로 해결 |
| **새 기능 필요** | `/dev --plan` 으로 전환 |
| **대규모 리팩토링** | `/dev --architecture` 로 전환 |
| **설계 변경 필요** | `/dev --design` 으로 전환 |

### 전환 판단 기준

```python
def should_transition_to_dev(root_cause_analysis):
    """
    solve → dev 전환 판단
    """
    # dev 워크플로우로 전환해야 하는 경우
    if root_cause_analysis.requires_new_feature:
        return "/dev --plan {feature_name}"

    if root_cause_analysis.requires_architecture_change:
        return "/dev --architecture"

    if root_cause_analysis.affects_multiple_modules > 3:
        return "/dev --design"

    if root_cause_analysis.requires_database_change:
        return "/dev --plan --design"

    # solve 내에서 해결
    return None
```

### 전환 시 사용자 안내

```
🔀 워크플로우 전환 권장
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
근본 원인 분석 결과, 단순 수정으로 해결 불가합니다.

**원인**: [근본 원인]
**권장 전환**: `/dev --plan {기능명}`

**이유**:
- 새로운 기능 구현 필요
- 3개 이상 모듈 영향
- 설계 변경 필요

전환하시겠습니까? [Y/N]
```

## 다음 단계

| 상황 | 권장 명령어 |
|------|------------|
| 문제 발생 | `/solve "문제 설명"` |
| 깊은 분석 필요 | `/solve --5whys` 또는 `--rca` |
| 진행 확인 | `/solve --log` |
| 완료 후 | `/solve --report` |
| 유사 문제 검색 | `/solve --history "키워드"` |
| **새 기능 필요** | `/dev --plan` |
| **설계 변경 필요** | `/dev --design` |

## 📦 산출물 (CRITICAL - 누락 금지)

> **문제 해결 시 반드시 산출물 생성**

| 단계 | 산출물 | 파일 경로 | 필수 |
|------|--------|----------|------|
| **문제 정의** | 문제 정의서 | `.claude/problem-solving/active/{problem-id}/problem.md` | ✅ |
| **분석** | 분석 기록 | `.claude/problem-solving/active/{problem-id}/analysis.md` | ✅ |
| **가설** | 가설 목록 | `.claude/problem-solving/active/{problem-id}/hypotheses.md` | ⚠️ |
| **해결 후** | 해결 보고서 | `.claude/problem-solving/resolved/{problem-id}/report.md` | ✅ |
| **지식 베이스** | 패턴 등록 | `.claude/problem-solving/knowledge-base/solutions.json` | ✅ |

### 문제 정의서 필수 항목

```markdown
# 문제 정의서: {problem-id}

## 기본 정보
- **ID**: {problem-id}
- **보고 일시**: {timestamp}
- **보고자**: {user}
- **심각도**: [CRITICAL/HIGH/MEDIUM/LOW]

## 증상
- 에러 메시지: {message}
- 발생 위치: {file:line}
- 재현 조건: {conditions}

## 영향 범위
- 영향 받는 기능: {features}
- 영향 받는 사용자: {users}
```

### 해결 보고서 필수 항목

```markdown
# 해결 보고서: {problem-id}

## 근본 원인
- **원인**: {root_cause}
- **분석 방법**: {method} (5whys/rca/hypothesis)
- **신뢰도**: {confidence}%

## 해결 내용
- **수정 파일**: {files}
- **수정 내용**: {changes}
- **테스트 결과**: {test_result}

## 재발 방지
- [ ] 예방 조치 1
- [ ] 예방 조치 2

## 지식 베이스 등록
- 키워드: {keywords}
- 유사 문제 대응 가이드: {guide}
```

## ✅ State Persistence 의무

### 문제 해결 시작 시 필수 작업
- [ ] 1. problem-id 생성 (PROB-NNN 형식)
- [ ] 2. 문제 정의서 생성 → `.claude/problem-solving/active/{id}/problem.md`
- [ ] 3. Worktree 업데이트 → 현재 문제 해결 상태 기록

### 분석 완료 후 필수 작업
- [ ] 1. 분석 기록 생성 → `.claude/problem-solving/active/{id}/analysis.md`
- [ ] 2. 근본 원인 confidence 기록

### 해결 완료 후 필수 작업
- [ ] 1. 해결 보고서 생성 → `.claude/problem-solving/resolved/{id}/report.md`
- [ ] 2. 지식 베이스 업데이트 → `solutions.json`에 패턴 추가
- [ ] 3. active 폴더 → resolved 폴더로 이동
- [ ] 4. Worktree 업데이트 → 해결 상태로 변경

### State 파일 업데이트 예시

```python
def register_solution_to_knowledge_base(problem_id, root_cause, solution, keywords):
    """해결된 문제를 지식 베이스에 등록"""
    kb_path = ".claude/problem-solving/knowledge-base/solutions.json"
    kb = load_json(kb_path)

    kb["solutions"].append({
        "id": problem_id,
        "problem": root_cause["symptom"],
        "cause": root_cause["cause"],
        "solution": solution["description"],
        "keywords": keywords,
        "resolved_at": datetime.now().isoformat(),
        "confidence": root_cause["confidence"]
    })

    # 패턴 업데이트
    for keyword in keywords:
        existing_pattern = find_pattern(kb, keyword)
        if existing_pattern:
            existing_pattern["occurrences"] += 1
        else:
            kb["patterns"].append({
                "keywords": [keyword],
                "likely_causes": [root_cause["cause"]],
                "occurrences": 1
            })

    save_json(kb_path, kb)
    print(f"✅ 지식 베이스 업데이트 완료: {problem_id}")
```

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
- `.claude/problem-solving/knowledge-base/solutions.json` - 해결 패턴
- `.claude-state/worktree.json` - 작업 상태
