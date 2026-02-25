# Flash Plugin v3.0

> Opus + Codex 듀얼 모델 워크플로우를 위한 커스텀 Claude Code 플러그인

## Opus ↔ Codex 워크플로우

```
┌─────────────────────────────────────────────────────────┐
│  Opus (Claude Code)                                     │
│                                                         │
│  1. 리서치     /calab-plugin:research [주제]             │
│       ↓                                                 │
│  2. 프로젝트   /calab-plugin:onboard (기존 프로젝트 시)   │
│     분석           ↓                                    │
│  3. 기획       /calab-plugin:dev plan [기능]             │
│       ↓        → plans/에 PRD 생성                      │
│  4. 설계       /calab-plugin:dev design                  │
│       ↓        → 아키텍처 + ERD                         │
│  5. 태스크     /calab-plugin:dev tasks                   │
│     분해       → TASK-001 ~ TASK-N 생성                 │
│       ↓                                                 │
│  6. 핸드오프   /calab-plugin:handoff TASK-001            │
│               → plans/handoff-20260225-xxx.md 생성      │
└────────────────────┬────────────────────────────────────┘
                     │ 명세서 전달
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Codex                                                  │
│                                                         │
│  "plans/handoff-20260225-xxx.md 를 읽고 구현해"          │
│                                                         │
│  → 명세서의 AC, Constraints, Scope에 따라 구현           │
│  → git commit                                           │
└────────────────────┬────────────────────────────────────┘
                     │ 구현 완료
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Opus (Claude Code)                                     │
│                                                         │
│  7. 리뷰       /calab-plugin:review                     │
│               → AC 1:1 대조 검증                        │
│               → Constraints 준수 확인                    │
│       ↓                                                 │
│  ✅ 100% 통과 → 다음 TASK로 (6번 반복)                   │
│  ❌ 미충족    → Codex 재위임 or Opus 직접 수정            │
└─────────────────────────────────────────────────────────┘
```

## 단계별 상세

| # | 누가 | 스킬 | 하는 일 | 산출물 |
|---|------|------|---------|--------|
| 1 | **Opus** | `/calab-plugin:research` | 기술 조사, 레퍼런스 수집 | 리서치 요약 |
| 2 | **Opus** | `/calab-plugin:onboard` | 기존 코드베이스 분석 | 컨텍스트 문서 5종 |
| 3 | **Opus** | `/calab-plugin:dev plan` | 브레인스토밍 + PRD | `plans/prd.md` |
| 4 | **Opus** | `/calab-plugin:dev design` | 아키텍처 + ERD | `plans/architecture.md` |
| 5 | **Opus** | `/calab-plugin:dev tasks` | 태스크 분해 | TASK-001 ~ N |
| 6 | **Opus** | `/calab-plugin:handoff` | Codex용 구현 명세서 생성 | `plans/handoff-*.md` |
| 7 | **Codex** | (직접 실행) | 명세서대로 구현 | git commit |
| 8 | **Opus** | `/calab-plugin:review` | AC 대조 검증 | 검증 리포트 |

## 역할 분담 원칙

| | Opus (분석/판단) | Codex (정밀 구현) |
|---|---|---|
| **강점** | 리서치, 아키텍처, 원인 분석, 리뷰 | 정확한 코드 작성, 대량 파일 수정 |
| **적합** | "왜" + "무엇을" | "어떻게" |
| **토큰** | 비쌈 → 분석/판단에 집중 | 저렴 → 반복 구현에 활용 |

## 실전 사용 예시

```bash
# 1. Opus: 리서치 + 기획
/calab-plugin:research "K8s HPA 커스텀 메트릭"
/calab-plugin:dev plan "HPA 커스텀 메트릭 연동"

# 2. Opus: 설계 + 태스크 분해
/calab-plugin:dev design
/calab-plugin:dev tasks

# 3. Opus: TASK-001을 Codex 명세서로 변환
/calab-plugin:handoff TASK-001

# 4. Codex: 구현 (별도 터미널)
codex "plans/handoff-20260225-hpa-metrics.md 를 읽고 구현해"

# 5. Opus: 검증
/calab-plugin:review --spec plans/handoff-20260225-hpa-metrics.md

# 6. 통과 → 다음 TASK
/calab-plugin:handoff TASK-002
```

핵심은 **6→7→8 루프를 TASK 단위로 반복**하는 것. Opus는 판단, Codex는 구현.

## 전체 스킬 목록 (12개)

| 스킬 | 설명 |
|------|------|
| `/calab-plugin:dev` | Plan/Design/Tasks/Build 워크플로우 |
| `/calab-plugin:solve` | 체계적 문제 해결 (5 Whys, RCA) |
| `/calab-plugin:research` | 웹 리서치 + 핵심 요약 |
| `/calab-plugin:onboard` | 프로젝트 분석 + 컨텍스트 문서 생성 |
| `/calab-plugin:handoff` | Opus → Codex 구현 위임 명세서 |
| `/calab-plugin:review` | Codex 구현물 AC 검증 |
| `/calab-plugin:best-practices` | 기술별 베스트 프랙티스 |
| `/calab-plugin:code-quality` | 코드 품질 규칙 (500줄 제한, 주석) |
| `/calab-plugin:project-rules` | 프로젝트 규칙 참조 |
| `/calab-plugin:work-tracker` | 작업 진행 상태 추적 |
| `/calab-plugin:clarification-protocol` | 서브에이전트 명확화 프로토콜 |
| `/calab-plugin:skill-completion-rules` | 스킬 완료 시 다음 단계 규칙 |

## 에이전트 (13개)

planner-phase, planner-task, design, dev-executor, deep-researcher, web-researcher, root-cause-finder, bug-fixer, build-error-resolver, validator, reinforcer, project-guardian, project-onboarder

## 원본

[calab-claude-plugin](https://github.com/Wondermove-Inc/calab-claude-plugin) `flash` 브랜치에서 커스텀.
