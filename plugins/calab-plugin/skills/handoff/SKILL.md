---
name: handoff
description: |
  Opus → Codex 구현 위임. 분석 결과를 Codex용 구조화된 명세서로 변환합니다.
argument-hint: "[feature-or-task] [--from-plan|--quick]"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion]
skills: [project-rules, work-tracker, clarification-protocol, skill-completion-rules]
agents:
  primary: deep-researcher
  orchestration:
    analyze: [Explore]
hooks:
  Stop:
    - hooks:
        - type: command
          command: "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/post_skill_artifact_check.py\""
          once: true
---

# /handoff - Opus → Codex 구현 위임

> **Opus가 분석/계획한 결과를 Codex가 바로 구현할 수 있는 구조화된 명세서로 변환**

## 사용법

```bash
/handoff [feature-or-task]           # 현재 분석 결과를 Codex용 명세서로 변환
/handoff --from-plan plans/001.md    # 기존 plan 파일 기반으로 생성
/handoff --quick                     # 단일 파일 수정용 경량 명세서
```

## 트리거 키워드

`handoff`, `위임`, `코덱스로`, `codex에게`, `넘겨`, `구현 위임`, `구현 맡겨`

## 목적

Opus의 강점(리서치, 아키텍처 분석, 원인 파악)으로 도출한 결과물을
Codex의 강점(정확한 코드 구현, 버그 감지)으로 연결하는 **브릿지 문서** 생성.

핵심 원칙: **"Codex가 이 문서만 읽고 구현을 완료할 수 있는가?"**

---

## 실행 절차

### Step 1: 컨텍스트 수집

현재 세션에서 Opus가 수행한 작업 결과를 수집:
- 리서치 결과 (있는 경우)
- 원인 분석 결과 (있는 경우)
- 아키텍처 결정 사항
- 변경 대상 파일 목록
- 제약사항 및 금지사항

### Step 2: 명세서 생성

`templates/handoff-template.md` 를 기반으로 명세서 생성.

**저장 위치**: `plans/handoff-{YYYYMMDD}-{feature-slug}.md`

### Step 3: 검증 질문

생성된 명세서에 대해 자기 검증:
1. Codex가 추가 질문 없이 구현 가능한가?
2. 파일 경로가 모두 정확한가?
3. AC가 코드로 검증 가능한가?
4. 금지사항이 명확한가?

### Step 4: 사용자 확인

```
============================================
 HANDOFF 명세서 생성 완료
============================================

 📄 파일: plans/handoff-20260225-db-refactor.md

 📋 요약:
 • 태스크: [설명]
 • 변경 파일: [N]개
 • AC: [N]개

 ✅ Codex 실행 방법:
 codex "plans/handoff-20260225-db-refactor.md 를 읽고 구현해"

============================================
```

---

## 명세서 품질 기준

### 필수 (없으면 생성 불가)
- [ ] Goal이 한 문장으로 명확한가
- [ ] 변경할 파일 경로가 정확한가
- [ ] AC가 EARS 패턴(WHEN/THEN)으로 작성되었는가
- [ ] Constraints(금지사항)가 명시되었는가

### 권장
- [ ] 함수 시그니처가 포함되었는가
- [ ] 기존 코드 패턴 참조가 있는가
- [ ] 검증 명령어가 포함되었는가
- [ ] Edge cases가 열거되었는가

---

## 명세서 크기별 가이드

| 규모 | 파일 수 | 템플릿 | 예상 Codex 시간 |
|------|--------|--------|---------------|
| Small | 1-2 | `--quick` 경량 | 5-10분 |
| Medium | 3-5 | 기본 템플릿 | 15-30분 |
| Large | 6+ | 태스크 분할 권장 | 분할 후 개별 handoff |

Large 규모는 태스크를 분할하여 개별 handoff 문서를 생성하는 것을 권장.

---

## Codex 실행 가이드 (명세서 소비 측)

```bash
# 방법 1: 대화형 모드에서 명세서 참조
codex
> plans/handoff-20260225-db-refactor.md 를 읽고 구현해줘

# 방법 2: 비대화형 exec 모드
codex exec "plans/handoff-20260225-db-refactor.md 의 태스크를 구현하라"

# 방법 3: Plan Mode에서 먼저 검토
codex
> /plan
> plans/handoff-20260225-db-refactor.md 를 읽고 구현 계획을 검토해줘
```

---

## 다음 단계

| 상황 | 명령어 |
|------|--------|
| Codex 구현 완료 후 검증 | `/review` |
| 추가 태스크 위임 | `/handoff [다음 태스크]` |
| 명세서 수정 | 직접 편집 후 Codex 재실행 |
