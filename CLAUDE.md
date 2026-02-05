> **어떤 상황에서든 동일한 개발 품질을 보장하는** Claude Code 행동 규칙

---

## 목차

1. [플러그인 개요](#플러그인-개요)
2. [핵심 원칙 (5대 규칙)](#핵심-원칙-5대-규칙)
3. [에이전트 가이드](#에이전트-가이드)
4. [검증/보강 패턴](#검증보강-패턴)
5. [스킬 활용](#스킬-활용)
6. [워크플로우](#워크플로우)
7. [품질 규칙](#품질-규칙)
8. [세션 관리](#세션-관리)

---

## 플러그인 개요

### 핵심 구성

```
17개 스킬 (10 active + 7 passive) + 23개 에이전트 + 26개 훅
```

| 영역 | 자동화 내용 |
|------|------------|
| **개발 워크플로우** | Plan → Discuss → Design → Tasks → Build (Wave 병렬) |
| **코드 품질** | 베스트 프랙티스, 500줄 제한, 주석 필수 |
| **문제 해결** | 5 Whys, RCA, 가설 검증 |
| **작업 추적** | Worktree 진행률 + Phase 로드맵 관리 |

### 스킬 구조

| 유형 | 스킬 | 역할 |
|------|------|------|
| **Active (Core)** | dev, solve, onboard | 개발/문제해결/온보딩 |
| **Active (Utility)** | docs, security, research, jira, refactor, e2e, guard | 문서/보안/리서치/JIRA/리팩토링/E2E/규칙검증 |
| **Passive** | best-practices, code-quality, tdd-workflow, project-rules, work-tracker, clarification-protocol, skill-completion-rules | 자동 로드 |

---

## 핵심 원칙 (5대 규칙)

### 1. 할루시네이션 금지

```
❌ 읽지 않은 코드 추측 금지
✅ 파일 먼저 읽고 답변
✅ 불확실하면 "확인 필요" 인정
```

### 2. 에이전트 100% 활용

| 작업 | 에이전트 |
|------|---------|
| 코드베이스 탐색 | `Explore` |
| 코드 리뷰 | `calab-plugin:code-reviewer` |
| 보안 검사 | `calab-plugin:security-reviewer` |
| 완전성 검증 | `calab-plugin:validator` |
| 웹 리서치 | `calab-plugin:web-researcher` |

### 3. Task 완료 검증 필수

> **AC 100% 충족 전까지 다음 Task 금지**

- [ ] AC 100% 충족
- [ ] 기능 동작 확인
- [ ] 엣지 케이스 처리
- [ ] 코드 품질 (500줄↓, 주석, 타입)

### 4. 사용자 선택권 보장 (Checkpoint 분류)

| 타입 | 빈도 | 처리 |
|------|------|------|
| **human-verify** | 90% | 간결 요약 + 자동 진행 옵션 |
| **decision** | 9% | 트레이드오프 분석 + 추천안 제시 |
| **human-action** | 1% | 단계별 가이드 + 완료 대기 |

> 직접 결정할 수 있으면 묻지 마라. 되돌리기 비용이 높을 때만 물어라.

### 5. 컨텍스트 유지 (50% Budget Rule)

- `.claude/memory/CURRENT_CONTEXT.md` - 현재 작업 상태
- `.claude/memory/PROJECT_RULES.md` - 프로젝트 규칙

| 사용률 | 품질 | 액션 |
|--------|------|------|
| **0-30%** | PEAK | 최적 구간 |
| **30-50%** | GOOD | 목표 완료 구간 |
| **50-70%** | DEGRADING | 효율 모드. 생략 발생 |
| **70%+** | POOR | 즉시 분리. 체크포인트 저장 |

---

## 에이전트 가이드

### 네임스페이스 규칙

| 유형 | 호출 방식 | 예시 |
|------|----------|------|
| **기본** | prefix 없음 | `subagent_type="Explore"` |
| **플러그인** | `calab-plugin:` 필수 | `subagent_type="calab-plugin:validator"` |

### 기본 에이전트 (3개)

| 에이전트 | 역할 |
|----------|------|
| **Explore** | 코드베이스 탐색 |
| **Plan** | 구현 계획 수립 |
| **general-purpose** | 범용 작업 |

### 플러그인 에이전트 (23개)

| 에이전트 | 역할 |
|----------|------|
| `code-reviewer` | 코드 품질 검토 |
| `security-reviewer` | 보안 취약점 분석 |
| `validator` | 완전성/AC 검증 |
| `reinforcer` | 검증 실패 항목 수정 |
| `build-error-resolver` | 빌드 오류 해결 |
| `root-cause-finder` | 근본 원인 분석 |
| `bug-fixer` | TDD 버그 수정 |
| `planner-phase` | PRD 및 PHASE 분해 |
| `planner-task` | Task 분해 (TDD) |
| `design` | 아키텍처/ERD 설계 |
| `dev-executor` | TDD 구현 실행 |
| `qa` | 8단계 QA 검증 |
| `web-researcher` | 웹 검색 및 수집 |
| `deep-researcher` | 심층 리서치 분석 |
| `doc-updater` | 문서 자동 업데이트 |
| `docs-generator` | 코드 기반 문서 생성 |
| `project-onboarder` | 프로젝트 온보딩 |
| `project-guardian` | 규칙 준수 검증 |
| `jira-connector` | JIRA 양방향 동기화 |
| `refactor-cleaner` | 데드 코드 정리 |
| `e2e-runner` | E2E 테스트 실행 |
| `task-validator` | Task 분해 검증 |
| `dev-workflow` | 개발 워크플로우 관리 |

### 프롬프트 필수 7요소 (RGOSWOC)

| 요소 | 설명 |
|------|------|
| **R**ole | 역할 정의 |
| **G**oal | 달성 목표 |
| **O**bjective | 세부 목표 |
| **S**cope | 작업 범위 |
| **W**orkflow | 수행 순서 |
| **O**utput | 출력 형식 |
| **C**onstraints | 제약 조건 |

### Task 명세 6요소 (Specificity Test)

> **"다른 Claude 인스턴스가 질문 없이 실행할 수 있는가?"**

| 요소 | 설명 |
|------|------|
| **What** | 구현할 것 (구체적 기능) |
| **How** | 구현 방법 (기술, 패턴) |
| **Avoid + WHY** | 금지 사항 + 이유 |
| **Verify** | 검증 명령어 |
| **Done** | 완료 기준 (AC) |
| **Files** | 생성/수정 파일 목록 |

### Structured Returns (에이전트 간 통신)

> 모든 검증/리뷰 에이전트는 텍스트 + JSON 구조화 결과를 반환한다.

| 에이전트 | result 값 |
|----------|----------|
| `validator` | `passed\|warning\|failed\|critical` + `confidence_score` |
| `code-reviewer` | `passed\|needs_improvement\|failed` + `issues[]` |
| `security-reviewer` | `clean\|warning\|vulnerable\|critical` + `findings[]` |
| `dev-executor` | `success\|failure\|needs_clarification` + `deviations[]` |

### Deviation Rules (dev-executor 자동 수정)

| 자동 수정 (확인 없이) | 사용자 확인 필수 |
|----------------------|-----------------|
| 버그/타입 오류 수정 | 아키텍처 변경 |
| 보안 취약점 수정 | 공개 API 변경 |
| 누락된 에러 처리/검증 | 범위 확장 (scope creep) |
| 의존성/import 수정 | 기존 파일/함수 삭제 |
| 깨진 테스트 수정 | |

### 병렬 vs 순차 실행

| 상황 | 실행 방식 |
|------|----------|
| 독립적인 조사 | **병렬** |
| 결과가 다음 단계 입력 | **순차** |
| 파일 수정 작업 | **순차** (충돌 방지) |
| Wave 내 Task | **병렬** (Fresh Context) |

### Fresh Context Pattern

> **오케스트레이터는 Task 정의만 관리. 구현 코드를 직접 읽지 않는다.**

| 항목 | 규칙 |
|------|------|
| 오케스트레이터 | Task 정의 + worktree.json만 읽기 |
| executor | Fresh 200k context로 독립 실행 |
| 전달 금지 | 이전 Task 구현 결과, 히스토리 |

### Wave 기반 병렬 실행

```
Wave 1: [TASK-001] [TASK-002]  ← 병렬 (의존성 없음)
Wave 2: [TASK-003]             ← Wave 1 완료 후
Wave 3: [TASK-004] [TASK-005]  ← Wave 2 완료 후
```

### 모델 프로필 관리

| 프로필 | 설명 | 비용 |
|--------|------|------|
| **quality** | 모든 단계 opus | 100% |
| **balanced** | 기획 opus + 실행 sonnet (권장) | ~60% |
| **budget** | 모든 단계 haiku/sonnet | ~30% |

설정: `.claude/settings/model-profile.json`

---

## 검증/보강 패턴

### 필수 검증 체인

```
구현 → validator (3레벨 + Goal-Backward) → (실패 시) reinforcer → validator (재검증)
```

| 단계 | 에이전트 | 역할 |
|------|---------|------|
| 1 | 구현 에이전트 | 코드 작성 |
| 2 | `validator` | AC/완전성 검증 **필수** (3레벨 아티팩트 + Goal-Backward) |
| 3 | `code-reviewer` | 품질 검증 |
| 4 | `security-reviewer` | 보안 검사 (API/인증) |
| 5 | `reinforcer` | 레벨별 수정 (실패 시) |
| 6 | `validator` | 재검증 **필수** |

### 3레벨 아티팩트 검증

| 레벨 | 검증 내용 | 신뢰도 기여 |
|------|----------|------------|
| **L1: Existence** | 파일/함수 존재 확인 | 기본 |
| **L2: Substantive** | AC 구현, 에러 처리, 타입 정의 | 중간 |
| **L3: Wired** | import 연결, 라우터 등록, 테스트 연결 | 높음 |

### Goal-Backward 검증

```
사용자 목표 → Observable Truth → 코드 Artifact → Key Link 역추적
```

### 신뢰도 기반 에스컬레이션

| 신뢰도 | 액션 |
|--------|------|
| 90%+ | 다음 Task 진행 |
| 70-89% | reinforcer 호출 |
| 50-69% | 사용자 확인 |
| <50% | `/solve` 에스컬레이션 |

### Plan Checker Loop

> Task 분해 시 planner-task가 자체 검증 (최대 3회) 후 task-validator가 최종 확인

```
planner-task → self_verify (3회) → task-validator (최종)
```

### 검증 우회 금지

| 상황 | 필수 에이전트 |
|------|--------------|
| 새 파일 생성 | `code-reviewer` |
| API 엔드포인트 | `code-reviewer` + `security-reviewer` |
| 인증/인가 로직 | `security-reviewer` |
| Task 완료 | `validator` |

---

## 스킬 활용

### 메타 스킬 (3개)

| 스킬 | 명령어 | 역할 |
|------|--------|------|
| **dev** | `/dev --plan/--discuss/--design/--tasks/--build/--roadmap` | 개발 워크플로우 |
| **solve** | `/solve --5whys/--rca/--hypothesis` | 문제 해결 |
| **onboard** | `/onboard` | 프로젝트 분석 |

### 패시브 스킬 (7개)

| 스킬 | 트리거 |
|------|--------|
| `best-practices` | 기술 키워드 |
| `code-quality` | 코드 생성/수정 |
| `tdd-workflow` | `--tdd`, 테스트 키워드 |
| `project-rules` | 모든 코드 작성 |
| `work-tracker` | 소스 파일 수정 |
| `clarification-protocol` | 서브에이전트 실행 |
| `skill-completion-rules` | Active 스킬 완료 시 |

### 워크플로우 연동

```
/onboard → /dev --plan → --discuss → --design → --tasks → --build → QA
                (ROADMAP)  (선택적)                (Wave)   (Wave 병렬)
                                                              ↓
                                                        실패 시 /solve
```

### solve ↔ dev 전환 기준

| 상황 | 전환 |
|------|------|
| 새 기능 필요 | `/dev --plan` |
| 3개+ 모듈 영향 | `/dev --design` |
| 단순 코드 수정 | `/solve` 내 해결 |
| 빌드 오류 3회+ | `/solve --5whys` |

---

## 워크플로우

### 새 프로젝트

```bash
/onboard   # 프로젝트 분석
```

### 기능 개발

```bash
/dev --plan [기능명]       # PRD 작성 + ROADMAP.md 생성
/dev --discuss             # 그레이 영역 해소 (선택)
/dev --design              # 아키텍처 설계
/dev --tasks               # 태스크 분해 (Wave 할당)
/dev --build --all         # Wave 병렬 실행
/dev --build TASK-001      # 단일 Task 실행
/dev --roadmap complete 1  # Phase 완료 → 다음 Phase
/dev --roadmap milestone "v1.0.0"  # 마일스톤 생성
```

### 문제 해결

```bash
/solve [에러 메시지]   # 자동 방법론 선택
/solve --5whys         # 5 Whys 분석
/solve --rca           # Root Cause Analysis
```

---

## 품질 규칙

### 코드 품질

| 항목 | 기준 |
|------|------|
| 파일 크기 | 500줄 이하 |
| 함수 주석 | 모든 함수 필수 |
| 타입 정의 | 100% 커버리지 |

### 테스트 커버리지

| 항목 | 최소 | 권장 |
|------|------|------|
| 라인 | 70% | 80% |
| 브랜치 | 60% | 70% |
| 함수 | 80% | 90% |

---

## 세션 관리

### 상태 파일

| 파일 | 용도 |
|------|------|
| `.claude-state/checkpoint.json` | 상세 상태 |
| `.claude-state/worktree.json` | 작업 트리 (Wave/Phase 포함) |
| `.claude/docs/active/{feature}/ROADMAP.md` | Phase 로드맵 |
| `.claude/memory/CURRENT_CONTEXT.md` | 비상 복구 |

### 복구 우선순위

```
1. checkpoint.json → 2. worktree.json → 3. CURRENT_CONTEXT.md → 4. /onboard
```

### 자동 동작

| 트리거 | 동작 |
|--------|------|
| 코드 작성 | 품질 검사 |
| 파일 수정 | worktree 업데이트 |
| 세션 시작 | 컨텍스트 안내 + 로그 로테이션 |
| Compact | 체크포인트 저장 |
| 빌드 오류 | `build-error-resolver` 호출 |

---

## 산출물 필수화

### 스킬별 산출물

| 스킬 | 산출물 | 경로 |
|------|--------|------|
| `/dev --plan` | PRD + ROADMAP | `.claude/docs/active/{feature}/01-PRD.md`, `ROADMAP.md` |
| `/dev --discuss` | 구현 결정 | `.claude/docs/active/{feature}/00-CONTEXT.md` |
| `/dev --design` | 아키텍처 | `.claude/docs/active/{feature}/02-architecture.md` |
| `/dev --tasks` | Task 목록 | `.claude/docs/active/{feature}/03-tasks.md` |
| `/solve` | 해결 보고서 | `.claude/problem-solving/resolved/{id}/report.md` |
| `/onboard` | 컨텍스트 문서 | `.claude/project-context/` |

### 에이전트별 산출물

| 에이전트 | 산출물 |
|----------|--------|
| `validator` | `.claude/docs/active/{feature}/validation-report.md` |
| `reinforcer` | `.claude/docs/active/{feature}/reinforcer-report.md` |
| `build-error-resolver` | `.claude/docs/active/{feature}/build-error-report.md` |

> **산출물 미생성 시 작업 실패로 간주**

---

## 명령어 참조

### 코어 스킬

| 명령어 | 옵션 |
|--------|------|
| `/dev` | `--plan`, `--discuss`, `--design`, `--tasks`, `--build [ID\|--wave N\|--all]`, `--roadmap [add\|insert\|remove\|complete\|milestone]`, `--status` |
| `/solve` | `--5whys`, `--rca`, `--hypothesis`, `--log`, `--report` |
| `/onboard` | `--quick`, `--full`, `--phase N`, `--skip-domain` |

### 유틸리티 스킬

| 명령어 | 옵션 | 용도 |
|--------|------|------|
| `/docs` | `--api`, `--component`, `--guide` | 문서 생성 |
| `/security` | `--owasp`, `--secrets`, `--deps` | 보안 검사 |
| `/research` | `--deep`, `--compare` | 웹 리서치 |
| `/jira` | `--sync`, `--create`, `--update` | JIRA 연동 |
| `/refactor` | `--dead-code`, `--duplicates`, `--imports` | 리팩토링 |
| `/e2e` | `--run`, `--debug`, `--record` | E2E 테스트 |
| `/guard` | `--rules`, `--context`, `--full` | 규칙 검증 |

### 에이전트 호출

```bash
"code-reviewer로 품질 검사해줘"
"security-reviewer로 보안 검사해줘"
"web-researcher로 조사해줘"
```

---

## 스킬 자동완성 (링크 설정)

플러그인 스킬을 `/` 자동완성에 표시하려면:

```bash
# 리포지토리에서 실행
./link-skills.sh
```

결과: `~/.claude/skills/calab-*` 심볼릭 링크 생성

```bash
/calab-dev --plan 기능명     # 개발 워크플로우
/calab-solve 에러메시지       # 문제 해결
/calab-docs --api src/api/   # 문서 생성
```

제거: `./link-skills.sh --remove`
