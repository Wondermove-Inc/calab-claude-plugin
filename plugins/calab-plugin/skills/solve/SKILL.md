---
name: solve
description: |
  문제 해결 프로세스. 체계적인 방법론으로 근본 원인을 분석하고 해결합니다.
argument-hint: "[--5whys|--rca|--hypothesis|--binary] [문제 설명]"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, WebSearch, mcp__tavily__tavily-search]
skills: [code-quality, best-practices, tdd-workflow, project-rules, work-tracker, clarification-protocol, skill-completion-rules]
agents:
  primary: root-cause-finder
  orchestration:
    explore: [Explore]
    analyze: [calab-plugin:root-cause-finder, Explore]
    research: [calab-plugin:deep-researcher]
    fix: [calab-plugin:bug-fixer, calab-plugin:code-reviewer]
    validate: [calab-plugin:validator]
    reinforce: [calab-plugin:reinforcer]
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/code_quality_validator.py\""
  Stop:
    - hooks:
        - type: command
          command: "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/post_skill_artifact_check.py\""
          once: true
---

# /solve - 문제 해결

> **체계적 문제 분석 및 해결**

---

## Data Flow Contract

### Input (스킬 간 데이터 수신)

| 소스 | 데이터 | 용도 |
|------|--------|------|
| `/dev --build` | 빌드 오류 로그 | 빌드 실패 시 에스컬레이션 |
| QA 실패 | 테스트 실패 로그 | QA 실패 시 에스컬레이션 |

### Output (스킬 간 데이터 전달)

| 단계 | 산출물 | 다음 스킬 Input |
|------|--------|----------------|
| 분석 | `.claude/problem-solving/active/{id}/analysis.md` | 수정 단계 |
| 해결 | `.claude/problem-solving/resolved/{id}/report.md` | `/dev --plan` (기능 전환 시) |
| 지식베이스 | `.claude/problem-solving/knowledge-base/solutions.json` | 유사 문제 검색 |

### State Update

- `.claude/problem-solving/active/` → `resolved/` 이동
- `.claude/problem-solving/knowledge-base/solutions.json` 패턴 등록

---

## 사용법

```bash
/solve "문제 설명"           # 기본 문제 해결
/solve --5whys "문제"        # 5 Whys 기법
/solve --rca "문제"          # Root Cause Analysis
/solve --hypothesis "문제"   # 가설 기반 접근
/solve --log                 # 진행 상황
/solve --report              # 보고서 생성
```

---

## 에이전트 호출 (필수)

> **⚠️ 이 스킬이 로드되면 아래 지침을 따라 Task 도구를 호출하세요.**

### 1. 탐색 단계

```python
Task(
    subagent_type="Explore",
    description="문제 관련 코드 탐색",
    prompt="... (references/explore.md 참조)"
)
```

### 2. 분석 단계

**Routing**: `references/analyze.md` 참조

```python
Task(
    subagent_type="calab-plugin:root-cause-finder",
    description="근본 원인 분석",
    prompt="... (references/analyze.md 참조)"
)
```

**산출물 필수**: `.claude/problem-solving/active/{id}/analysis.md`

### 3. 수정 단계

**Routing**: `references/fix.md` 참조

```python
Task(
    subagent_type="calab-plugin:bug-fixer",
    description="TDD 기반 버그 수정",
    prompt="... (references/fix.md 참조)"
)
```

**산출물 필수**: `.claude/problem-solving/resolved/{id}/fix-report.md`

### 4. 검증 단계

```python
Task(
    subagent_type="calab-plugin:validator",
    description="해결 검증",
    prompt="..."
)
```

**산출물 필수**: `.claude/problem-solving/resolved/{id}/validation-report.md`

---

## 검증/보강 체인 (필수)

```
분석 (root-cause-finder)
    ↓
수정 (bug-fixer)
    ↓
검증 (validator) ─────┬─ 성공 → 지식베이스 등록
    ↓                 │
실패 → reinforcer ────┴─ 재검증 (validator)
```

---

## 6단계 프로세스

```
1. 문제 정의 (Define)     → problem.md
2. 정보 수집 (Gather)     → Git 로그, 파일 분석
3. 원인 분석 (Analyze)    → 5whys/RCA/Hypothesis
4. 가설 검증 (Hypothesize)→ 예측→검증→결과
5. 해결 구현 (Solve)      → TDD 기반 수정
6. 문서화 (Document)      → 지식 베이스 등록
```

---

## 분석 기법

| 기법 | 옵션 | 설명 |
|------|------|------|
| 5 Whys | `--5whys` | "왜?"를 5번 반복 |
| RCA | `--rca` | 8단계 체계적 분석 |
| 가설 검증 | `--hypothesis` | 가설→예측→검증 사이클 |
| Binary Search | `--binary` | 이진 탐색으로 위치 좁히기 |

---

## /dev 전환 기준

| 상황 | 액션 |
|------|------|
| 단순 버그 수정 | solve 내에서 해결 |
| 새 기능 필요 | `/dev --plan` 전환 |
| 설계 변경 필요 | `/dev --design` 전환 |
| 3개+ 모듈 영향 | `/dev --design` 전환 |

---

## 레퍼런스 라우팅

| 옵션 | 참조 파일 |
|------|----------|
| `--5whys` | `references/5whys.md` |
| `--rca` | `references/rca.md` |
| `--hypothesis` | `references/hypothesis.md` |
| `--log` | `references/log.md` |
| `--report` | `references/report.md` |

---

## 파일 구조

```
.claude/problem-solving/
├── active/{problem-id}/
│   ├── problem.md
│   ├── analysis.md
│   └── hypotheses.md
├── resolved/{problem-id}/
│   └── report.md
└── knowledge-base/
    └── solutions.json
```

---

## 다음 단계 선택 (필수)

> **⚠️ 작업 완료 후 반드시 AskUserQuestion 호출**
>
> 문제 해결이 완료되면 현재 상황을 분석하여 AskUserQuestion으로 다음 단계 선택지를 제시하세요.
> - 해결된 문제 요약
> - 새 기능 개발 필요 여부 (권장 표시)
> - 보고서 작성 옵션
> - 추가 문제 분석 옵션
> - 종료 옵션
