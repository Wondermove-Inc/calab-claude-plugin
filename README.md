# Flash Plugin v3.1

> Opus + Codex 듀얼 모델 워크플로우를 위한 커스텀 Claude Code 플러그인

## 워크플로우

```
┌─────────────────────────────────────────────────────────┐
│  Opus (Claude Code)                                     │
│                                                         │
│  1. 브레인스토밍  /brainstorm [주제 또는 에러]            │
│       ↓          → 아이디어 발산 / 원인 분석             │
│                  → --5whys, --rca, --hypothesis          │
│                                                         │
│  2. 리서치       /research [주제]  (필요 시)              │
│       ↓          → 기술 조사, 트렌드, 베스트 프랙티스     │
│                                                         │
│  3. 계획         /plan [기능명]                           │
│       ↓          → PRD 작성 (요구사항, AC, 구현 방향)     │
│                  → --design (대규모 기능 시 아키텍처 포함) │
│                                                         │
│  4. 핸드오프     /handoff                                │
│                  → Codex용 구현 명세서 생성               │
└────────────────────┬────────────────────────────────────┘
                     │ 명세서 전달
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Codex                                                  │
│                                                         │
│  "plans/handoff-*.md 를 읽고 구현해"                     │
│  → 명세서의 AC, Constraints, Scope에 따라 구현           │
└────────────────────┬────────────────────────────────────┘
                     │ 구현 완료
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Opus (Claude Code)                                     │
│                                                         │
│  5. 리뷰         /review                                │
│                  → AC 1:1 대조 검증                      │
│       ↓                                                 │
│  ✅ 통과 → 완료                                         │
│  ❌ 미충족 → Codex 재위임 or Opus 직접 수정              │
└─────────────────────────────────────────────────────────┘
```

## 단계별 상세

| # | 누가 | 스킬 | 하는 일 | 산출물 |
|---|------|------|---------|--------|
| 1 | **Opus** | `/brainstorm` | 아이디어 발산, 원인 분석 | 방향성 + 권장안 |
| 2 | **Opus** | `/research` | 기술 조사 (필요 시) | 리서치 요약 |
| 3 | **Opus** | `/plan` | PRD 작성 (요구사항, AC) | `.claude/docs/active/{feature}/PRD.md` |
| 4 | **Opus** | `/handoff` | Codex용 구현 명세서 | `plans/handoff-*.md` |
| 5 | **Codex** | (직접 실행) | 명세서대로 구현 | git commit |
| 6 | **Opus** | `/review` | AC 대조 검증 | 검증 리포트 |

## 에러/장애 해결 플로우

```
/brainstorm --5whys "에러 설명"   # 원인 분석
  → /research (추가 조사 필요 시)
  → /plan (수정 계획)
  → /handoff → [Codex 수정] → /review
```

## 역할 분담

| | Opus (분석/판단) | Codex (정밀 구현) |
|---|---|---|
| **강점** | 리서치, 원인 분석, 기획, 리뷰 | 정확한 코드 작성, 대량 파일 수정 |
| **적합** | "왜" + "무엇을" | "어떻게" |
| **토큰** | 비쌈 → 분석/판단에 집중 | 저렴 → 반복 구현에 활용 |

## 실전 사용 예시

```bash
# 기능 개발
/brainstorm "사용자 알림 시스템"       # 아이디어 구체화
/plan "사용자 알림 시스템"             # PRD 작성
/handoff                              # Codex 명세서 생성
# → Codex 구현 →
/review                               # 검증

# 에러 해결
/brainstorm --rca "간헐적 504 타임아웃"  # 원인 분석
/research "nginx upstream timeout"       # 추가 조사
/plan "504 타임아웃 수정"                # 수정 계획
/handoff                                 # Codex에 위임
```

## 스킬 목록

### 사용자 호출 (7개)

| 스킬 | 설명 |
|------|------|
| `/brainstorm` | 아이디어 발산 + 원인 분석 (`--5whys`, `--rca`, `--hypothesis`) |
| `/plan` | PRD 작성 (요구사항, AC, 구현 방향). `--design` 옵션 |
| `/handoff` | Opus → Codex 구현 위임 명세서 |
| `/review` | Codex 구현물 AC 검증 |
| `/research` | 웹 리서치 + 핵심 요약 |
| `/onboard` | 프로젝트 분석 + 컨텍스트 문서 생성 |
| `/docs` | 문서 자동 생성 (API, 컴포넌트, 가이드) |

### 패시브 (6개) — 자동 적용

| 스킬 | 설명 |
|------|------|
| `best-practices` | 기술별 베스트 프랙티스 (15개 언어) |
| `code-quality` | 코드 품질 규칙 (500줄 제한, 주석) |
| `project-rules` | 프로젝트 규칙 참조 |
| `work-tracker` | 작업 진행 상태 추적 |
| `clarification-protocol` | 서브에이전트 명확화 프로토콜 |
| `skill-completion-rules` | 스킬 완료 후 다음 단계 규칙 |

## 에이전트 (12개)

| 에이전트 | 모델 | 역할 |
|----------|------|------|
| planner-phase | sonnet | PRD 작성 |
| deep-researcher | **opus** | 심층 리서치 분석 |
| web-researcher | sonnet | 웹 검색 데이터 수집 |
| root-cause-finder | **opus** | 근본 원인 분석 |
| bug-fixer | sonnet | TDD 기반 버그 수정 |
| build-error-resolver | sonnet | 빌드 오류 해결 |
| validator | **opus** | AC 충족 검증 |
| reinforcer | sonnet | 검증 실패 항목 수정 |
| project-guardian | **opus** | 규칙 준수 감시 |
| project-onboarder | sonnet | 프로젝트 분석 |
| doc-updater | sonnet | 문서 자동 업데이트 |
| docs-generator | sonnet | 문서 생성 |

## 훅 (3개)

| 훅 | 이벤트 | 역할 |
|----|--------|------|
| sensitive_file_guard | PreToolUse | `.env`, 크레덴셜 파일 수정 차단 |
| precompact_save_state | PreCompact | 컨텍스트 압축 전 상태 저장 |
| session_start_restore_hint | SessionStart | 세션 시작 시 이전 컨텍스트 안내 |

## 원본

[calab-claude-plugin](https://github.com/Wondermove-Inc/calab-claude-plugin) `flash` 브랜치에서 커스텀.
