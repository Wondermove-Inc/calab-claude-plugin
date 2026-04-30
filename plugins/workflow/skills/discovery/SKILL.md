---
name: workflow:discovery
description: 사용자와 Claude가 주제를 함께 탐색하는 대화형 프로세스. 변경 사항·문제점·신규 기능 아이데이션을 라운드 무제한 대화로 정리하고, 사용자 종료 시 task 또는 epic+task 이슈를 산출하거나 산출물 없이 종료합니다.
allowed-tools: Agent, Bash, AskUserQuestion, Read, Grep, Glob
---

# /workflow:discovery 커맨드

사용자와 Claude가 **주제를 함께 탐색하는 대화형 프로세스**입니다. 변경 사항·문제점·신규 기능 아이데이션 등을 **라운드 무제한**으로 진행하고, 사용자가 종료 의사를 표시하면 산출물(이슈)을 만들거나 산출물 없이 종료합니다.

```
/workflow:discovery 인증 모듈 리팩토링 검토              # 자유 텍스트로 주제 시작
/workflow:discovery bd-abc123                          # 기존 epic 보강 모드
```

## 모드 판별

| 입력 | 모드 |
|------|------|
| 자유 텍스트 | **신규 모드** — 주제로 대화 시작, 종료 시 이슈 산출 (선택적) |
| `bd-` 접두사 + type=epic | **Epic 보강 모드** — 기존 epic 컨텍스트로 대화 시작, 종료 시 자식 task 추가 |
| `bd-` 접두사 + type=task | "task는 build를 사용하세요" 안내 후 종료 |

## 핵심 원칙

1. **대화는 사용자 주도** — 라운드 수 무제한. Claude가 강제 종료하지 않음.
2. **Claude는 매 라운드 정리·명확화·옵션 제시** — 사용자 발언을 그대로 받아들이지 말고 가정 표면화·범위 확인·트레이드오프 제시
3. **architect는 필요 시 자동 호출** — 코드 분석이 필요한 시점에 단발 Agent 호출. 누적 대화 컨텍스트를 prompt에 포함
4. **산출물은 선택적** — 이슈 없이 끝나는 경우도 정상 (단순 탐색·아이데이션·결정 보류)
5. **task가 기본, epic은 분할 명백할 때만** — 이슈 생성 직전 architect 종합 호출 결과로 보수적으로 결정
6. **코드 변경 없음** — discovery는 대화·이슈 생성만. worktree·머지·테스트 미사용
7. **종료 후 인계** — 이슈 생성 시 사용자가 `/workflow:build` 수동 호출

> 공통 규칙(금지 사항, 합리화 경고, 신뢰 수준, 혼란 관리, 가정 표면화): [`references/agent-common.md`](../../references/agent-common.md)

## 워크플로우

```
사용자 입력 → [1] 주제 진입 (가벼운 컨텍스트 확인)
            → [2] 대화 루프 (라운드 무제한)
                ↻ 사용자 발언 → Claude 정리/명확화/옵션
                ↻ 필요 시 architect 호출 (코드 분석)
                ↻ 진행 의사 확인 (계속 / 종료)
            → [3] Discovery Gate (종료 시 산출물 분기)
                ├ 이슈 생성 + 종료
                ├ 산출물 없이 종료
                └ 더 진행 (2단계 복귀)
            → [4] 이슈 생성 (조건부, 3단계에서 "이슈 생성" 선택 시)
            → [5] 결과 보고 + build 인계 안내 (또는 단순 종료 보고)
```

## 1단계: 주제 진입

사용자 입력에서 주제를 추출하고 가볍게 컨텍스트만 확인. 별도 게이트 없음.

### 신규 모드

```
사용자 발언 → Claude가 주제 요약 + "어떤 관점에서 시작할까요?" 정도의 가벼운 안내
```

### Epic 보강 모드

```bash
bd show <epic-id>
# type=epic 확인 (task면 "build를 사용하세요" 안내 후 종료)
bd update <epic-id> --status in_progress  # 필요 시
bd comments add <epic-id> "[Discovery] 보강 시작"
```

기존 epic의 description/acceptance와 자식 task 목록을 컨텍스트로 가져온 뒤 2단계 대화 루프 진입.

## 2단계: 대화 루프 (라운드 무제한)

각 라운드는 다음 패턴을 따릅니다. 사용자가 종료 신호를 줄 때까지 반복.

### 라운드 구성

```
사용자 발언 (질문 / 추가 정보 / 결정 / 의견)
  ↓
Claude:
  · 발언 핵심 정리
  · 암묵적 가정 표면화 (`agent-common.md` §6 ASSUMPTIONS 패턴)
  · 필요 시 옵션 A/B 제시 (단일 결론으로 몰지 않음)
  · 필요 시 architect 자동 호출 (아래 §architect 호출 트리거)
  · 다음 진행 안내 (필요한 경우 다음 검토 항목 제안)
  ↓
진행 의사 확인 (선택적, 매 라운드 강제 안 함)
```

### architect 자동 호출 트리거

다음 중 하나에 해당하면 Claude가 architect를 자동 호출하여 코드 분석 결과를 라운드에 반영:

| 트리거 | 호출 목적 |
|--------|----------|
| 사용자가 특정 모듈/함수/파일 언급 | 해당 영역 구조 분석 |
| 영향 범위 모호 (예: "인증 흐름") | 의존성 그래프 / 호출자 추적 |
| 변경 가능성을 가늠해야 함 | 리스크 점검 |
| 사용자가 "코드 봐줘" 같은 명시 요청 | 직접 분석 |

호출 패턴:

```
Agent(
  subagent_type: "workflow:architect",
  model: "opus",
  run_in_background: false,
  description: "Discovery 라운드 코드 분석",
  prompt: "Discovery 진행 중인 주제: {주제 요약}\n\n현재까지 누적 대화 핵심:\n{핵심 3~5줄}\n\n분석 요청: {구체적 질문/범위}\n\n출력: 분석 결과 (설계 초안이나 작업 분할은 아직 불필요. 정보 수집 단계)"
)
```

architect는 단발 호출이므로 매번 새 컨텍스트로 시작. **누적 대화 핵심을 prompt에 포함**하는 게 중요. 무차별 호출 금지 — 코드 분석이 정말 필요한 라운드에서만.

### 진행 의사 확인 (선택적)

매 라운드 끝에 강제로 묻지 않습니다. 다음 신호가 보이면 자연스럽게 3단계 Discovery Gate로 이동:

- **사용자 명시 종료 신호**: "그만", "충분", "끝", "이슈 만들어줘", "정리하자" 등
- **자연스러운 합의 도달**: 변경 사항이 구체적으로 정리되어 더 논의할 항목이 보이지 않음
- **라운드 정체**: 동일 결론이 반복되거나 진전 없음 — Claude가 "이쯤에서 정리할까요?" 제안

## 3단계: Discovery Gate (종료 시 산출물 분기)

종료 신호 감지 시 **Claude가 먼저 산출물 유무를 판단**하고 사용자에게 분기 옵션 제시.

### 3-1. Claude의 산출물 판단

| 판단 | 기준 |
|------|------|
| **산출물 있음** | 변경 사항/AC/범위가 구체적으로 정리되어 task description에 옮길 수 있는 수준 |
| **산출물 없음** | 단순 탐색·아이데이션·결정 보류·정보 수집만 한 경우, 또는 변경 자체가 불필요하다는 결론 |

### 3-2. AskUserQuestion 분기

#### 산출물 있음으로 판단된 경우

```
AskUserQuestion:
  question: "[Discovery Gate] 대화 내용을 정리했습니다. 다음과 같은 변경 사항이 도출되었습니다:\n{2~4줄 요약}\n어떻게 할까요?"
  options:
    - "이슈 생성하고 종료" — 4단계 진행 (architect 종합 호출 → task/epic 산출)
    - "이슈 없이 종료" — 5단계 단순 종료 보고
    - "더 진행" — 2단계 대화 루프 복귀
```

#### 산출물 없음으로 판단된 경우

```
AskUserQuestion:
  question: "[Discovery Gate] 특별한 산출물은 도출되지 않았습니다. 어떻게 할까요?"
  options:
    - "이슈 없이 종료" — 5단계 단순 종료 보고
    - "더 진행" — 2단계 대화 루프 복귀
    - "그래도 이슈 생성" — 4단계 진행 (사용자가 산출물이 있다고 판단한 경우)
```

> 사용자가 "더 진행"을 선택하면 2단계로 복귀. 라운드 수 무제한 원칙에 따라 횟수 제한 없음.

## 4단계: 이슈 생성 (조건부)

3단계에서 "이슈 생성"을 선택한 경우에만 진행.

### 4-1. architect 종합 호출

대화 누적 컨텍스트 + 결정된 변경 사항을 architect에 전달하여 작업 분할 + 리스크 분석을 요청:

```
Agent(
  subagent_type: "workflow:architect",
  model: "opus",
  run_in_background: false,
  description: "Discovery 종합 — 작업 분할 + 리스크",
  prompt: "Discovery 종료 시점 종합 분석.\n\n주제: {주제}\n\n결정된 변경 사항:\n{2~4문장 요약}\n\n누적 대화 핵심:\n{5~10줄}\n\n출력: 작업 분할 draft (단일 Work로 충분하면 단일) + 5개 리스크 체크리스트 결과"
)
```

> 라운드 도중 architect를 이미 여러 번 호출했어도, 종합 호출은 별도로 한 번 더 수행 (단발 호출이라 컨텍스트 통합 필요).

### 4-2. 산출물 결정 규칙

architect의 작업 분할 결과로 task vs epic 보수적으로 결정:

| 조건 | 산출물 |
|------|--------|
| Work 수 = 1 + 수정 허용 파일이 단일 모듈/디렉토리에 한정 + 의존 외부 작업 없음 | **task 1개** (기본) |
| Work 수 = 1이지만 수정 허용 파일이 2개 이상 모듈/디렉토리에 걸침 또는 단계적 마이그레이션 필요 | **epic + 자식 task** (사실상 분할 필요) |
| Work 수 ≥ 2 | **epic + 자식 task N개** |
| 보강 모드 (입력이 epic이었음) | **기존 epic + 자식 task 추가** |

> 의심스러우면 **task 1개**가 기본. epic은 자식 task 2개 이상이 명확할 때만.

### 4-3. 리스크 노출 (조건부)

architect 리스크 분석에 **🔴 (Critical) 1건 이상**이면 사용자에게 한 번 더 확인:

```
AskUserQuestion:
  question: "[Discovery 리스크] 종합 분석에서 다음 리스크가 발견되었습니다:\n{리스크 목록}\n계속 진행할까요?"
  options:
    - "그대로 진행" — 이슈 생성으로 진행
    - "다시 논의" — 2단계 대화 루프 복귀
    - "이슈 없이 종료" — 5단계 단순 종료
```

⚠️/✅ 등급만 있으면 자동으로 4-4로.

### 4-4. 이슈 생성

#### task 단일 케이스

```bash
bd create "<제목>" --type task --priority 2
bd update <task-id> \
  --description "<주제 + 결정된 변경 사항 + 담당 모듈 + 수정 허용 파일 + 읽기 전용 파일 + TDD 계획>" \
  --acceptance "<완료 조건 체크리스트>"
bd comments add <task-id> "[Discovery] 진입 — 라운드 N회, 단일 Work, 리스크: <건수/등급>"
```

> task는 **open 상태 유지** (in_progress 전환은 build 1-A에서).

#### epic + 자식 task 케이스

```bash
# 신규 모드: Epic 생성
bd create "<제목>" --type epic --priority 2
bd update <epic-id> \
  --description "<목적·범위·AC + 결정된 변경 사항 + 설계 핵심>" \
  --acceptance "<Epic 차원 체크리스트>"
bd update <epic-id> --status in_progress
bd comments add <epic-id> "[Discovery] 진입 — 라운드 N회, Work N개 분할, 리스크: <건수/등급>"

# 자식 task 생성 (신규 / 보강 공통)
for each Work in design:
  bd create "Work #<N>: <Work 제목>" --type task --priority 2 --parent <epic-id>
  bd update <task-id> \
    --description "<Work 설명: 담당 모듈, 수정 허용 파일, 읽기 전용 파일, TDD 계획>" \
    --acceptance "<완료 조건>"
  if Work.depends_on:
    bd update <task-id> --blocked-by <prereq-task-id>
done
```

> 자식 task는 **open 상태 유지**.

## 5단계: 결과 보고 + 인계 (또는 단순 종료)

### 5-A. 이슈 생성 케이스 (4단계 진행 시)

#### task 단일

```markdown
Discovery 종료: bd-<task-id> (task 단일)

| 항목 | 결과 |
|------|------|
| 라운드 | N회 |
| architect 호출 | M회 (라운드 도중 N회 + 종합 1회) |
| 산출물 | task 1개 (open) |
| 리스크 | 🔴 N / ⚠️ N |
| 다음 단계 | `/workflow:build bd-<task-id>` |
```

```bash
bd comments add <task-id> "[Discovery] build 인계"
```

#### epic + 자식 task

```markdown
Discovery 종료: bd-<epic-id> (epic + task N개)

| 항목 | 결과 |
|------|------|
| 라운드 | N회 |
| architect 호출 | M회 |
| 산출물 | epic 1개 (in_progress) + task N개 (open) |
| 리스크 | 🔴 N / ⚠️ N |
| 다음 단계 | `/workflow:build bd-<epic-id>` |

`bd list --parent bd-<epic-id>` 로 자식 task 목록 확인.
```

```bash
bd comments add <epic-id> "[Discovery] build 인계"
```

### 5-B. 이슈 미생성 케이스 (산출물 없이 종료)

```markdown
Discovery 종료 (산출물 없음)

| 항목 | 결과 |
|------|------|
| 라운드 | N회 |
| architect 호출 | M회 |
| 결론 | <대화 핵심 결론 1~2줄. 예: "기존 구현 유지가 적절", "추가 정보 수집 후 재논의 필요" 등> |

bd 이슈 생성 없음.
```

bd 기록 없음 (Epic 보강 모드에서는 `[Discovery] 보강 종료 — 산출물 없음` comment 1줄 기록).

## 이슈 comment 기록 표준

전체 키 목록은 [`guides/gate-process.md`](../../guides/gate-process.md) §comment 키 참조. discovery에서 사용하는 키:

| 시점 | 식별자 | 내용 |
|------|--------|------|
| 보강 모드 진입 | `[Discovery] 보강 시작` | 1단계 (보강 모드 한정) |
| 이슈 생성 | `[Discovery] 진입` | 4-4 이슈 생성 직후 (라운드 N, Work 수, 리스크) |
| 보강 산출물 없음 | `[Discovery] 보강 종료 — 산출물 없음` | 5-B (보강 모드 한정) |
| 인계 | `[Discovery] build 인계` | 5-A 직후 |

> 신규 모드에서 산출물 없이 종료하면 comment 기록 없음 (이슈 자체가 미생성).

## 에러 핸들링

| 상황 | 처리 |
|------|------|
| 입력이 task 타입 이슈 | "discovery는 epic 보강 또는 신규 요청만 처리합니다. 단일 task 구현은 /workflow:build를 사용하세요" 안내 후 종료 |
| architect CONFUSION | 혼란 옵션을 사용자에게 전달, 답변 후 architect 재호출 또는 대화 라운드로 흡수 |
| architect 응답 부실 | 다음 라운드에서 더 구체적인 prompt로 재호출 |
| 사용자가 종료 신호 후에도 추가 요청 | 4단계 진행 중이라도 "더 진행"으로 분기 가능 (3-2 분기 옵션 재활용) |
| 무한 대화 우려 | Claude는 종료를 강제하지 않지만, 동일 결론 반복 시 "이쯤에서 정리할까요?" 자연스럽게 제안 가능 |

## 호출 규칙 요약

- architect는 **단발 Agent 호출** — 라운드 도중 자동 호출 가능, 종합 호출 별도 1회
- 각 호출 prompt에 **누적 대화 핵심**을 포함 (단발이라 컨텍스트 손실)
- task / 자식 task는 **open 상태로 생성** — build가 in_progress로 전환
- epic은 **in_progress** — build가 모든 자식 task close 후 사용자 승인 시 close
- 단일 task 케이스에서는 epic 계층 생성 안 함 (보수적 원칙)
- discovery 자체는 코드 변경 없음 — worktree 미사용

## build로의 인계

이슈 생성 후 사용자가 다음 명령으로 진행:

```
/workflow:build bd-<task-id>      # task 단일 모드: 곧장 구현
/workflow:build bd-<epic-id>      # Epic 하이브리드 모드: 자식 task 선택 → 구현
```

build의 모드 판별 흐름은 [`../build/SKILL.md`](../build/SKILL.md) 1단계 참조.

## 지금 시작하세요

사용자가 제시한 주제로 1단계 진입 후 2단계 대화 루프를 시작하세요. 종료는 사용자 신호에 따라.
