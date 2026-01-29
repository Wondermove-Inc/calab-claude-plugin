# Calab Claude Plugin

[![Version](https://img.shields.io/badge/version-2.7.0-blue.svg)](https://github.com/Wondermove-Inc/calab-claude-plugin)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-purple.svg)](https://claude.ai/code)

> **일관된 개발 품질을 보장하는** Claude Code 워크플로우 자동화 플러그인

---

## 왜 Calab Plugin인가?

| 문제 | Calab Plugin 해결책 |
|------|---------------------|
| 매번 다른 코드 품질 | 자동 품질 검사 + 베스트 프랙티스 강제 |
| 컨텍스트 유실 (Compact) | 자동 저장/복원으로 작업 연속성 보장 |
| 반복적인 보일러플레이트 | 클린 아키텍처 자동 생성 |
| 문서화 누락 | 코드 변경 시 자동 문서 동기화 |
| 할루시네이션 | validator/reinforcer 에이전트로 검증 |
| 산출물 누락 | 스킬별 필수 산출물 + State Persistence 의무화 |

### 🆕 v2.7.0 변경사항

| 기능 | 설명 |
|------|------|
| **🔍 산출물 검증 훅** | SubagentStop 시 자동 산출물 검증 (post_skill_artifact_check.py) |
| **📋 23개 에이전트 산출물 규칙** | 모든 에이전트에 필수 산출물 100% 정의 |
| **🏷️ USE WHEN 키워드** | 23개 에이전트 전체 활성화 키워드 정의 |
| **✅ 에이전트 완전성 100%** | frontmatter, tools, model, permissionMode 검증 완료 |

### v2.6.0 변경사항

| 기능 | 설명 |
|------|------|
| **📦 산출물 필수화** | 모든 스킬/에이전트에 필수 산출물 정의 |
| **🔄 재검증 체인** | validator→reinforcer→validator 자동 체인 (최대 2회) |
| **✅ State Persistence** | 작업 전/후 상태 저장 체크리스트 의무화 |
| **🔌 Circuit Breaker** | 빌드 오류 3회 반복 시 자동 차단 |
| **📊 Worktree 무결성** | 체크섬 기반 데이터 무결성 검증 |

---

## 한눈에 보기

```
┌──────────────────────────────────────────────────────────────────────┐
│  3개 액티브 스킬  │  6개 패시브 스킬  │  23개 에이전트  │  20개 훅  │
└──────────────────────────────────────────────────────────────────────┘
```

### 스킬 구조

| 유형 | 스킬 | 역할 |
|------|------|------|
| **Active** | `/dev`, `/solve`, `/onboard` | 사용자 호출 메타커맨드 |
| **Passive** | best-practices, code-quality, tdd-workflow, project-rules, work-tracker, clarification-protocol | 자동 로드 |

### 유기적 워크플로우 통합 (2025 Best Practice)

```
/onboard → /dev (plan→design→tasks→build) → QA(자동) → 완료
                                              ↓ 실패
                                           /solve
                                              ↓
                     ┌─────────────────────────┴─────────────────────────┐
                     │ 단순 버그: bug-fixer    │ 복잡한 문제: /dev 재설계  │
                     └─────────────────────────┬─────────────────────────┘
                                              ↓
                                      validator → reinforcer
                                         (최대 2회 재시도)
```

**신뢰도 기반 에스컬레이션**:
- 90%+ → 다음 작업 진행
- 70-89% → reinforcer 자동 호출 → **재검증 필수**
- 50-69% → 사용자 확인 요청
- 0-49% → /solve 에스컬레이션

**재검증 체인 (무한 루프 방지)**:
```
validator → (실패) → reinforcer → validator(재검증) → (2차 실패) → 사용자 결정
```

### 실패 복원력 패턴 (Failure Resilience)

| 패턴 | 설명 | 적용 |
|------|------|------|
| **State Handoff** | 체크섬 검증 + 3중 백업 | 세션 연속성 보장 |
| **Rollback Mechanism** | 빌드/테스트 실패 시 자동 롤백 | 코드 안정성 보장 |
| **Graceful Degradation** | 비즈니스 영향도 기반 우선순위 복구 | 부분 장애 대응 |
| **Exponential Backoff** | 재시도 간격 점진적 증가 | 무한 루프 방지 |
| **Partial Completion** | 중간 실패 시 진행상황 보존 | Task 격리 처리 |
| **Three Developer Loops** | Inner/Middle/Outer 루프 분리 | 관심사별 반복 주기 |
| **Deadlock Prevention** | Task 생성 시 순환 의존성 감지 | 상호 대기 방지 |
| **Heartbeat/Timeout** | 에이전트 크래시 감지 및 Task 해제 | Stale Task 복구 |
| **Proactive Interruption** | 사용자 흐름 방해 최소화 | 배치 알림 처리 |
| **Circuit Breaker** | 빌드 오류 3회 반복 시 차단 | 자동 에스컬레이션 |
| **Artifact Mandatory** | 모든 스킬 산출물 필수 | 누락 방지 |

### 📦 스킬별 필수 산출물 (NEW)

| 스킬/에이전트 | 산출물 | 저장 위치 |
|---------------|--------|----------|
| `/dev --plan` | PRD 문서 | `.claude/docs/active/{feature}/01-PRD.md` |
| `/dev --design` | 아키텍처 문서 | `.claude/docs/active/{feature}/02-architecture.md` |
| `/dev --tasks` | Worktree JSON | `.claude-state/worktree.json` |
| `/solve` | 해결 보고서 | `.claude/problem-solving/resolved/{id}/report.md` |
| `validator` | 검증 보고서 | `.claude/docs/active/{feature}/validation-report.md` |
| `reinforcer` | 수정 보고서 | `.claude/docs/active/{feature}/reinforcer-report.md` |

---

## 빠른 시작

### 1. 마켓플레이스 추가

```bash
# Claude Code 실행 후
/plugin marketplace add Wondermove-Inc/calab-claude-plugin
```

### 2. 플러그인 설치

```bash
# 브라우징으로 설치 (권장)
/plugin
# → Discover 탭에서 calab-plugin 선택

# 또는 직접 설치
/plugin install calab-plugin@calab-marketplace
```

### 3. 설치 확인

```bash
/plugins
# calab-plugin이 목록에 표시되어야 함
```

### 4. CLAUDE.md 적용 (선택)

글로벌 지침을 적용하려면 CLAUDE.md를 복사합니다:

```bash
# 설치된 플러그인에서 CLAUDE.md 복사
curl -o ~/.claude/CLAUDE.md https://raw.githubusercontent.com/Wondermove-Inc/calab-claude-plugin/main/plugins/calab-plugin/CLAUDE.md
```

### 5. 프로젝트 온보딩

```bash
/onboard
```

### 6. 개발 시작

```bash
/dev --plan 사용자 인증 시스템
```

---

## 명령어 (3개 액티브 스킬)

### `/dev` - 개발 워크플로우

| 옵션 | 설명 |
|------|------|
| `--plan` | PRD + PHASE 분해 |
| `--design` | 아키텍처 + ERD 설계 |
| `--tasks` | Task 분해 (TDD 워크플로우) |
| `--build [TASK-ID]` | 태스크 구현 |
| `--architecture` | 클린 아키텍처 관리 |
| `--status` | 진행 상황 확인 |

### `/solve` - 문제 해결

| 옵션 | 설명 |
|------|------|
| `--5whys` | 5 Whys 분석 (반복 문제) |
| `--rca` | Root Cause Analysis (시스템 문제) |
| `--hypothesis` | 가설 기반 접근 |
| `--binary` | Binary Search 디버깅 |
| `--log` | 진행 상태 확인 |
| `--report` | 보고서 생성 |

### `/onboard` - 프로젝트 온보딩

| 옵션 | 설명 |
|------|------|
| `--quick` | 빠른 분석 |
| `--phases` | 단계별 상세 분석 |

### 에이전트 직접 호출

스킬 대신 에이전트를 직접 호출할 수 있습니다:

| 작업 | 에이전트 |
|------|----------|
| 문서 생성/업데이트 | `calab-plugin:doc-updater` |
| JIRA 연동 | `calab-plugin:jira-connector` |
| QA 테스트 | `calab-plugin:qa` |
| 보안 검사 | `calab-plugin:security-reviewer` |
| 품질 검사 | `calab-plugin:code-reviewer` |
| 웹 리서치 | `calab-plugin:web-researcher` |

---

## 패시브 스킬 (6개)

액티브 스킬이나 에이전트 실행 시 **자동으로 로드**됩니다.

| 스킬 | 로드 조건 | 효과 |
|------|----------|------|
| `best-practices` | 대부분의 에이전트에서 로드 | 기술별 베스트 프랙티스 자동 적용 |
| `code-quality` | 코드 생성/수정 에이전트 | 500줄 제한, 함수 주석, 타입 강제 |
| `tdd-workflow` | `/dev --build`, bug-fixer | Red-Green-Refactor 강제 |
| `work-tracker` | dev-workflow, project-guardian | Worktree 자동 업데이트 |
| `project-rules` | 대부분의 에이전트에서 로드 | PROJECT_RULES.md 규칙 적용 |
| `clarification-protocol` | planner, validator 등 | 불확실한 요구사항 명확화 |

---

## 에이전트 (23개)

특화된 작업을 수행하는 서브에이전트입니다.

### 워크플로우 에이전트 (7개)

| 에이전트 | 역할 | 호출 조건 |
|----------|------|----------|
| `dev-workflow` | Plan → Design → Tasks → Build 오케스트레이션 | `/dev` 실행 |
| `planner-phase` | PHASE 기반 기획/분석 | `/dev --plan` 실행 |
| `planner-task` | Task 분해 및 AC 정의 | `/dev --tasks` 실행 |
| `design` | 아키텍처 + ERD 설계 | `/dev --design` 실행 |
| `dev-executor` | 실제 코드 구현 | `/dev --build` 실행 |
| `project-onboarder` | 프로젝트 분석 | `/onboard` 실행 |
| `jira-connector` | JIRA 이슈 동기화 | JIRA 연동 요청 시 |

### 문제 해결 에이전트 (2개)

| 에이전트 | 역할 | 호출 조건 |
|----------|------|----------|
| `root-cause-finder` | 5 Whys, RCA 기반 근본 원인 분석 | `/solve` 실행 |
| `bug-fixer` | 버그 수정 및 테스트 작성 | validator 실패 시 |

### 리서치 에이전트 (2개)

| 에이전트 | 역할 | 호출 조건 |
|----------|------|----------|
| `web-researcher` | Tavily MCP 기반 실시간 웹 검색 | 검색, 조사 요청 시 |
| `deep-researcher` | 검색 결과 종합 분석 및 보고서 | 심층 리서치 요청 시 |

### 품질 에이전트 (4개)

| 에이전트 | 역할 | 호출 조건 |
|----------|------|----------|
| `code-reviewer` | 코드 품질/스타일 검토 | 리뷰 요청 시 |
| `security-reviewer` | OWASP Top 10 검사 | 보안 검사 시 |
| `project-guardian` | 프로젝트 규칙 준수 검증 | 규칙 확인 시 |
| `build-error-resolver` | 빌드/타입 오류 해결 + Circuit Breaker | 빌드 실패 시 |

### 검증/보강 에이전트 (3개)

| 에이전트 | 역할 | 호출 조건 |
|----------|------|----------|
| `validator` | AC/완전성/엣지케이스 검증 | 구현 완료 후 **필수** |
| `task-validator` | Task 단위 검증 | Task 완료 시 |
| `reinforcer` | 검증 실패 항목 자동 수정 | validator 실패 시 |

### 자동화/문서화 에이전트 (4개)

| 에이전트 | 역할 | 호출 조건 |
|----------|------|----------|
| `refactor-cleaner` | 데드 코드/미사용 import 정리 | 리팩토링 시 |
| `e2e-runner` | Playwright/Puppeteer 테스트 | E2E 테스트 시 |
| `doc-updater` | 코드 변경 감지 문서 업데이트 | 문서 동기화 시 |
| `docs-generator` | 문서 자동 생성 | 문서 생성 요청 시 |

### QA 에이전트 (1개)

| 에이전트 | 역할 | 호출 조건 |
|----------|------|----------|
| `qa` | 테스트 계획/실행/보고 | QA 요청 시 |

---

## 프로젝트 구조

```
calab-claude-plugin/
├── .claude-plugin/
│   └── marketplace.json       # 마켓플레이스 정의
│
├── README.md
│
└── plugins/
    └── calab-plugin/          # 플러그인 본체
        ├── .claude-plugin/
        │   └── plugin.json    # 플러그인 메타데이터
        │
        ├── CLAUDE.md          # Claude 지침 (핵심)
        │
        ├── skills/            # 9개 스킬 (3 active + 6 passive)
        │   ├── dev/          # 개발 워크플로우 (active)
        │   ├── solve/        # 문제 해결 (active)
        │   ├── onboard/      # 프로젝트 온보딩 (active)
        │   ├── best-practices/   # (passive)
        │   ├── code-quality/     # (passive)
        │   ├── tdd-workflow/     # (passive)
        │   ├── project-rules/    # (passive)
        │   ├── work-tracker/     # (passive)
        │   └── clarification-protocol/  # (passive)
        │
        ├── agents/            # 23개 에이전트
        │   ├── dev-workflow.md      # 워크플로우
        │   ├── validator.md         # 검증
        │   ├── reinforcer.md        # 보강
        │   ├── code-reviewer.md     # 품질
        │   ├── security-reviewer.md # 보안
        │   └── ...
        │
        └── hooks/             # 20개 훅 스크립트
```

---

## 워크플로우 예시

### 새 기능 개발

```bash
# 1. 기획
/dev --plan 사용자 인증 시스템

# 2. 설계
/dev --design

# 3. 태스크 분해
/dev --tasks

# 4. 구현 (태스크별)
/dev --build TASK-001
/dev --build TASK-002

# 5. QA (에이전트 직접 호출)
"qa 에이전트로 테스트 실행해줘"

# 6. 보안 검사 (에이전트 직접 호출)
"security-reviewer 에이전트로 보안 검사해줘"
```

### 버그 수정

```bash
# 에러 메시지와 함께 실행
/solve TypeError: Cannot read property 'id' of undefined

# 또는 특정 방법론 선택
/solve --5whys      # 반복 문제
/solve --rca        # 시스템 문제
/solve --hypothesis # 불명확한 원인
```

### Compact 후 복구

```bash
# 이전 작업 컨텍스트 복원 (훅에서 자동 안내됨)
# 세션 시작 시 session_start_restore_hint.py 훅이 복원 안내
# 저장된 상태: .claude-state/checkpoint.json
```

---

## 설치 옵션

### 옵션 1: 마켓플레이스 설치 (권장)

```bash
# 1. 마켓플레이스 추가 (GitHub에서 자동 다운로드)
/plugin marketplace add Wondermove-Inc/calab-claude-plugin

# 2. 플러그인 설치
/plugin install calab-plugin@calab-marketplace

# 3. 설치 확인
/plugins
```

### 옵션 2: 인터랙티브 설치

```bash
# 플러그인 브라우저 열기
/plugin

# → "Add Marketplace" 선택
# → "Wondermove-Inc/calab-claude-plugin" 입력
# → "Discover" 탭에서 calab-plugin 선택하여 설치
```

### 옵션 3: 로컬 개발용

```bash
# 리포지토리 클론
git clone https://github.com/Wondermove-Inc/calab-claude-plugin.git

# 로컬 마켓플레이스로 추가
/plugin marketplace add /path/to/calab-claude-plugin
```

---

## 설정

### settings.json

```json
{
  "permissions": {
    "allow": ["Read", "Glob", "Grep", "Write", "Edit"],
    "deny": []
  },
  "hooks": {
    "enabled": true
  }
}
```

### 필수 디렉토리

플러그인이 사용하는 디렉토리:

```
.claude/
├── memory/                # 컨텍스트 저장
│   ├── CURRENT_CONTEXT.md
│   └── PROJECT_RULES.md
├── project-context/       # 프로젝트 분석 결과
│   ├── PROJECT_SUMMARY.md
│   ├── CODE_PATTERNS.md
│   └── ARCHITECTURE.md
├── docs/                  # 생성된 문서
│   ├── active/           # 진행 중 기능
│   └── complete/         # 완료된 기능
└── problem-solving/       # 문제 해결 기록
    ├── active/           # 진행 중 문제
    ├── resolved/         # 해결된 문제
    └── knowledge-base/   # 지식 베이스

.claude-state/             # State Persistence (NEW)
├── checkpoint.json       # 세션 체크포인트
├── worktree.json         # 작업 트리 상태
├── circuit-breaker.json  # Circuit Breaker 상태
└── request-log.jsonl     # 요청 이력
```

---

## 요구사항

- **Claude Code CLI** v1.0.0 이상
- **Node.js** 18+ (일부 훅에서 사용)
- **Python** 3.8+ (일부 훅에서 사용)

---

## 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 라이선스

MIT License - [Wondermove CALab](https://wondermove.net)

---

## 문의

- **Issues**: [GitHub Issues](https://github.com/Wondermove-Inc/calab-claude-plugin/issues)
- **Email**: captain@wondermove.net
