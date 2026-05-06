---
name: toolkit:create-issue
description: 이슈 작성 가이드라인에 따라 beads 이슈 티켓을 생성합니다. 이슈 타입(initiative, epic, task, sub-task, bug)에 맞는 템플릿으로 구조화된 이슈를 작성합니다.
allowed-tools: Bash, Read
disable-model-invocation: true
argument-hint: <이슈 설명> [--type initiative|epic|task|sub-task|bug]
---

# /create-issue - 가이드라인 기반 이슈 티켓 생성

## 설명

이슈 작성 가이드라인에 따라 구조화된 beads 이슈를 생성합니다.
사용자가 제공한 요구사항을 분석하여 적절한 이슈 타입을 판별하고, 해당 타입의 템플릿에 맞춰 제목과 설명을 자동 작성합니다.

## 사용법

```bash
/toolkit:create-issue <이슈 설명>                          # 타입 자동 판별
/toolkit:create-issue <이슈 설명> --type task              # 타입 명시
/toolkit:create-issue <이슈 설명> --type bug               # 버그 이슈
/toolkit:create-issue <이슈 설명> --type epic              # 에픽 이슈
/toolkit:create-issue <이슈 설명> --type sub-task          # 하위 작업
/toolkit:create-issue <이슈 설명> --type initiative        # 이니셔티브
```

## 실행 절차

### Step 1: 요구사항 분석 및 타입 판별

사용자의 입력을 분석하여 이슈 타입을 판별합니다.

**판별 기준:**

| 타입 | 판별 키워드/조건 |
|------|----------------|
| Initiative | 릴리즈 목표, 버전 계획, 분기 목표 |
| Epic | 주요 기능 단위, 여러 작업을 포함하는 기능 |
| Task | 개발 작업, 구현, 연동, API, 컴포넌트 |
| Sub-task | 세부 구현, 단위 작업, 2-8시간 규모 |
| Bug | 버그, 오류, 에러, 결함, 장애, 수정 |

`--type`이 명시되지 않은 경우, 분석 결과를 사용자에게 확인합니다.

### Step 2: 필수 정보 수집

사용자에게 필수 필드를 질문합니다.
이미 인자나 컨텍스트로 파악 가능한 정보는 건너뜁니다.

**공통 필수 필드:**

| 필드 | 설명 | 예시 |
|------|------|------|
| 버전 | YY.Q.N 형식 | 26.1.2 |
| 영역 | Azure, GCP, Backend, Frontend 등 | Azure |
| 우선순위 | P0-P3 | P2 |

**타입별 추가 질문:**

- **Initiative**: 배경, 목적, 주요 업무 카테고리, 기대효과
- **Epic**: 개요, 배경, 주요 내용(Backend/Frontend/Infrastructure), 일정(Week 단위)
- **Task**: 개요, 변경 대상(컴포넌트/파일별), 기술 스펙
- **Sub-task**: 설명, 구현 위치, Acceptance Criteria (→ acceptance 필드)
- **Bug**: 현상, 재현 방법, 예상 동작, 실제 동작, 환경, 영향 범위

### Step 3: 제목 생성

가이드라인의 제목 형식에 따라 제목을 생성합니다.

**타입별 제목 형식:**

| 타입 | 형식 | 예시 |
|------|------|------|
| Initiative | `[YY.Q.N] 릴리즈 주요 목표` | `[26.1.2] Azure/GCP 멀티 클라우드 지원` |
| Epic | `[YY.Q.N][영역] 기능명` | `[26.1.2][Azure] AKS 클러스터 통합` |
| Task | `[YY.Q.N][영역] 작업 내용` | `[26.1.2][Azure] Cost Management API 연동` |
| Sub-task | `[YY.Q.N] 구체적 작업 내용` | `[26.1.2] Azure Cost API 클라이언트 구현` |
| Bug | `[YY.Q.N][영역] 버그 현상` | `[26.1.2][Azure] 비용 데이터 수집 시 타임아웃 발생` |

### Step 4: 필드별 내용 생성

타입별 템플릿에 맞춰 **4개 필드**에 분리 작성합니다.

#### 필드 분리 전략

| 필드 | 용도 |
|------|------|
| `--description` | 핵심 정보 (개요, 배경, 주요 내용) |
| `--acceptance` | 완료/성공 조건 (AC 체크리스트) |
| `--design` | 설계/기술 산출물 (기술 스펙, 아키텍처, 인터페이스) |
| `--notes` | 부가 정보 (일정, 비고, 참조, 환경 등) |

#### Initiative 템플릿

**description:**
```markdown
## 배경
{왜 이번 릴리즈가 필요한가}

## 목적
{핵심 목표}

## 주요 업무
### {카테고리 1}
* {항목}

### {카테고리 2}
* {항목}
```

**acceptance:**
```markdown
- [ ] {기대효과 1 — 정량적 목표}
- [ ] {기대효과 2}
```

**notes:**
```markdown
* 릴리즈 일정: {일정}
* 예상 개발 기간: {기간}
```

#### Epic 템플릿

**description:**
```markdown
## 개요
{기능 설명}

## 배경
{왜 필요한가}

## 주요 내용
### Backend
* {항목}

### Frontend
* {항목}

### Infrastructure
* {항목}
```

**acceptance:**
```markdown
- [ ] {성공 지표 1}
- [ ] {성공 지표 2}
```

**design:**
```markdown
## 기술 스펙
{기술적 세부사항}
```

**notes:**
```markdown
## 일정
* Week 1: {내용}
* Week 2: {내용}
```

#### Task 템플릿

**description:**
```markdown
## 개요
{작업 내용 1-2줄 요약}

## 변경 대상
### 1. {컴포넌트/파일}
* {변경 내용}

### 2. {컴포넌트/파일}
* {변경 내용}
```

**acceptance:**
```markdown
- [ ] AC1: {조건 1}
- [ ] AC2: {조건 2}
```

**design:**
```markdown
## 기술 스펙
{기술적 세부사항}
```

**notes:**
```markdown
## 참조
{관련 문서}
```

#### Sub-task 템플릿

**description:**
```markdown
## 설명
{구체적으로 무엇을 구현할 것인가}

## 구현 위치
{파일 경로}
```

**acceptance:**
```markdown
- [ ] AC1: {조건 1}
- [ ] AC2: {조건 2}
```

**notes:**
```markdown
## 참조
{관련 문서}
```

#### Bug 템플릿

**description:**
```markdown
## 1. 현상 (What)
{무엇이 잘못되었는가}

## 2. 재현 방법 (How to Reproduce)
1. {단계 1}
2. {단계 2}
3. {결과}

## 3. 예상 동작 (Expected)
{정상 동작}

## 4. 실제 동작 (Actual)
{실제 동작}

## 5. 로그/증거 (Evidence)
{에러 로그, 스크린샷}

## 6. RCA - 5 Whys 분석
### Why 1: 왜 문제가 발생했는가?
{답변}

### Why 2: 왜 그런 상황이 발생했는가?
{답변}

### Why 3: 왜 그런 조건이 생겼는가?
{답변}

### Why 4: 왜 그것을 방지하지 못했는가?
{답변}

### Why 5: 왜 시스템이 이를 감지하지 못했는가?
{답변}

### 근본 원인 (Root Cause)
{5 Whys 분석을 통해 도출된 근본 원인}
```

**acceptance:**
```markdown
- [ ] 즉시 수정 완료
- [ ] 재발 방지 조치 완료
- [ ] 영향 범위 확인 완료
```

**design:**
```markdown
## 해결 방안 (Solution)
### 즉시 수정 (Immediate Fix)
{수정 내용}

### 재발 방지 (Prevention)
{장기적 개선}
```

**notes:**
```markdown
## 환경 (Environment)
* 버전: {버전}
* 클라우드: {클라우드}
* 발생 빈도: {빈도}

## 영향 범위 (Impact)
* 영향 받는 버전: {버전}
* 우선순위: {우선순위}
* 임시 조치 (Workaround): {임시 조치}
```

### Step 5: 미리보기 및 확인

생성된 이슈를 사용자에게 미리보기로 보여주고 확인을 받습니다.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 이슈 생성 미리보기
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 타입:         {issue_type}
 제목:         {title}
 우선순위:      P{n}
 레이블:        {labels}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 [description]
 {description 내용}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 [acceptance]
 {acceptance 내용}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 [design] (해당 시)
 {design 내용}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 [notes] (해당 시)
 {notes 내용}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

사용자가 수정을 요청하면 해당 부분을 반영 후 다시 미리보기를 보여줍니다.
사용자가 승인하면 다음 단계로 진행합니다.

### Step 6: beads 이슈 생성

승인된 내용으로 beads 이슈를 생성합니다.

**이슈 타입 매핑:**

| 가이드라인 타입 | beads type |
|---------------|-----------|
| Initiative | epic |
| Epic | epic |
| Task | task |
| Sub-task | task |
| Bug | bug |

**우선순위 매핑:**

| 가이드라인 우선순위 | beads priority |
|-------------------|---------------|
| Critical | 0 |
| High | 1 |
| Medium | 2 |
| Low | 3 |

**생성 명령어:**

```bash
# 필수 필드
bd create "<제목>" --type <beads_type> --priority <beads_priority> \
  --description "<description 내용>" \
  --acceptance "<acceptance 내용>"

# 조건부 필드 (해당 시)
# --design, --notes는 내용이 있을 때만 포함
bd create "<제목>" --type <beads_type> --priority <beads_priority> \
  --description "<description 내용>" \
  --acceptance "<acceptance 내용>" \
  --design "<design 내용>" \
  --notes "<notes 내용>"
```

레이블이 있는 경우:

```bash
bd create "<제목>" --type <beads_type> --priority <beads_priority> \
  --labels "<label1>,<label2>" \
  --description "<description 내용>" \
  --acceptance "<acceptance 내용>"
```

### Step 7: 완료 보고

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 이슈 생성 완료
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 beads ID:     {issue-id}
 타입:         {type}
 제목:         {title}
 우선순위:      P{n}
 상태:         open
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 8: Jira 동기화 여부 확인 (필수)

이슈 생성 후 **반드시** 사용자에게 Jira 동기화 여부를 질문합니다. 자동으로 sync-jira를 호출하지 않습니다.

```
AskUserQuestion:
  question: "생성된 이슈 {issue-id}를 Jira로 동기화할까요?"
  options:
    - "예 — sync-jira 실행"
    - "아니오 — beads에만 유지"
```

| 선택 | 처리 |
|------|------|
| 예 | `/toolkit:sync-jira {issue-id}` 호출. 부모 티켓 등 추가 입력은 sync-jira 스킬 내부에서 사용자에게 질문 |
| 아니오 | 종료. 추후 수동으로 `/toolkit:sync-jira <id>` 호출 가능함을 1줄로 안내 |

> 복수 이슈를 연속 생성한 경우, 각 이슈 생성마다 개별 확인하지 말고 마지막에 일괄로 묻습니다 (`sync-jira` 스킬은 복수 ID 인자를 지원).

## 레이블 가이드

이슈 내용에서 자동으로 적절한 레이블을 추출합니다.

**클라우드별:** `aws`, `azure`, `gcp`, `oci`, `ncp`, `on-premise`
**영역별:** `backend`, `frontend`, `agent`, `infrastructure`
**타입별:** `feature`, `improvement`, `refactoring`, `patch`, `hotfix`

## 주의사항

- 제목은 50자 이내로 간결하게 작성합니다
- 제목에는 반드시 `[YY.Q.N]` 버전 표기를 포함합니다
- Bug 타입은 반드시 RCA(5 Whys) 분석 섹션을 포함합니다
- 정보가 부족한 경우 사용자에게 질문하여 보충합니다
- 설명에서 알 수 없는 항목은 `TBD`로 표기합니다

## 관련 스킬

| 스킬 | 설명 |
|------|------|
| `/toolkit:sync-jira` | 생성된 이슈를 Jira로 동기화 |
| `/toolkit:solve` | 문제 해결 시작 |
