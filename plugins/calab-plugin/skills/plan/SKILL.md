---
name: plan
description: |
  작업 계획 (PRD 작성). 요구사항 분석, 범위 정의, AC 작성을 수행합니다.
  구현은 /handoff로 Codex에 위임합니다.
argument-hint: "[기능명] [--design]"
allowed-tools: [Read, Write, Glob, Grep, Task, WebSearch, AskUserQuestion, mcp__tavily__tavily-search]
skills: [best-practices, project-rules, clarification-protocol, skill-completion-rules]
agents:
  primary: planner-phase
  orchestration:
    plan: [calab-plugin:planner-phase, calab-plugin:deep-researcher]
    explore: [Explore]
---

# /plan - 작업 계획

> **요구사항 분석 → PRD 작성 → /handoff로 Codex에 위임**

## 사용법

```bash
/plan [기능명]             # PRD 작성 (요구사항 + AC + 구현 방향)
/plan [기능명] --design    # PRD + 아키텍처 설계 (대규모 기능)
```

## 워크플로우

```
/plan → /handoff → [Codex 구현] → /review
```

| 단계 | 담당 | 산출물 |
|------|------|--------|
| `/plan` | Opus | PRD (요구사항, AC, 구현 방향) |
| `/handoff` | Opus | Codex용 구현 명세서 |
| 구현 | Codex | 소스코드, 테스트 |
| `/review` | Opus | 검증 결과 |

---

## 에이전트 호출

### 기본: PRD 작성

```python
Task(
    subagent_type="calab-plugin:planner-phase",
    description="작업 계획",
    prompt="""
    ## Goal
    '{feature_name}' PRD 작성

    ## Input
    - 기능명: {feature_name}
    - 사용자 요청: {user_request}
    - 프로젝트 컨텍스트: .claude/project-context/ (있는 경우)

    ## Output (필수)
    .claude/docs/active/{feature_name}/PRD.md

    ## PRD 포함 항목
    1. 문제 정의 + 배경
    2. 목표 (P0/P1/P2)
    3. 기능 요구사항 (Must/Should/Could)
    4. Acceptance Criteria (Given-When-Then)
    5. 비기능 요구사항 (성능, 보안)
    6. 기술 제약사항 + DO NOT CHANGE 영역
    7. 구현 방향 (디렉토리 구조, 핵심 로직 흐름)
    8. 리스크 + Open Questions

    ## Constraints
    - PRD.md 파일명 필수
    - P0 요구사항 최소 1개
    - 검증 가능한 AC 포함
    """
)
```

### --design 옵션: PRD + 아키텍처

대규모 기능 (새 시스템, DB 스키마 변경, 멀티 서비스 연동)에서만 사용합니다.

```python
# PRD 작성 후 아키텍처 추가
Task(
    subagent_type="calab-plugin:planner-phase",
    description="작업 계획 + 아키텍처",
    prompt="""
    ## Goal
    '{feature_name}' PRD + 아키텍처 설계

    ## Output (필수)
    .claude/docs/active/{feature_name}/PRD.md
    .claude/docs/active/{feature_name}/architecture.md

    ## architecture.md 포함 항목 (PRD에 추가)
    - 시스템 아키텍처 다이어그램 (Mermaid)
    - 컴포넌트 구조 + 책임
    - 데이터 흐름 (시퀀스 다이어그램)
    - ERD (DB 사용 시)
    - API 설계 (엔드포인트 목록)
    - 기술 스택 선택 이유
    """
)
```

---

## --design 사용 판단 기준

| 조건 | --design 필요 |
|------|--------------|
| 새 시스템/모듈 신규 생성 | Yes |
| DB 스키마 변경 | Yes |
| 외부 서비스 연동 | Yes |
| 기존 기능 확장/수정 | No — PRD만으로 충분 |
| 버그 수정 | No — `/brainstorm` (원인 분석) → `/plan` (수정 계획) |

---

## 완료 후 다음 단계

PRD 작성 완료 후 사용자에게 안내:

```
PRD 작성 완료: .claude/docs/active/{feature}/PRD.md

다음 단계:
1. /handoff → Codex에 구현 위임 (권장)
2. PRD 수정 요청
3. 직접 구현 (Opus가 코드 작성)
```
