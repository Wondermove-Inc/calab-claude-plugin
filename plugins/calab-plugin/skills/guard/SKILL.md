---
name: guard
description: |
  규칙 검증. 프로젝트 규칙 준수 여부와 작업 맥락을 확인합니다.
argument-hint: "[--rules|--context|--full]"
allowed-tools: [Read, Grep, Glob, Task]
skills: [project-rules, clarification-protocol, skill-completion-rules]
agents:
  primary: project-guardian
  orchestration:
    rules: [calab-plugin:project-guardian]
    context: [calab-plugin:project-guardian]
    full: [calab-plugin:project-guardian, calab-plugin:code-reviewer]
hooks:
  Stop:
    - hooks:
        - type: command
          command: "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/post_skill_artifact_check.py\""
          once: true
---

# /guard - 규칙 검증

> **프로젝트 규칙 준수 및 작업 맥락 확인**

---

## 사용법

```bash
/guard                      # 기본 규칙 검증
/guard --rules              # 프로젝트 규칙 준수 검사
/guard --context            # 작업 맥락 일관성 확인
/guard --full               # 전체 검증
```

---

## 에이전트 호출 (필수)

> **이 스킬이 로드되면 아래 지침을 따라 Task 도구를 호출하세요.**

```python
Task(
    subagent_type="calab-plugin:project-guardian",
    description="규칙 검증",
    prompt="""
[Role] 프로젝트 가디언
[Goal] 규칙 준수 및 맥락 일관성 확인
[Scope] {--rules|--context|--full}

## 검증 항목
### 규칙 준수 (--rules)
- 파일 크기 제한 (500줄)
- 함수 주석 필수
- 타입 정의 100%
- 네이밍 컨벤션
- 디렉토리 구조

### 맥락 일관성 (--context)
- 현재 작업과 목표 일치
- Task AC 충족 여부
- 작업 방향 이탈 감지

[Output] .claude/docs/active/{feature}/guardian-report.md
"""
)
```

---

## 검증 유형

| 옵션 | 검증 내용 |
|------|----------|
| `--rules` | 프로젝트 코딩 규칙 |
| `--context` | 작업 맥락 일관성 |
| `--full` | 위 전체 + 코드 리뷰 |

---

## 검증 항목

### 코드 규칙
- [ ] 파일 500줄 이하
- [ ] 모든 함수에 주석
- [ ] 타입 정의 완전성
- [ ] 네이밍 컨벤션 준수

### 맥락 검증
- [ ] 현재 Task와 작업 일치
- [ ] AC (Acceptance Criteria) 충족
- [ ] 불필요한 변경 없음

---

## 산출물 (필수)

| 산출물 | 경로 |
|--------|------|
| 검증 보고서 | `.claude/docs/active/{feature}/guardian-report.md` |

### 보고서 형식

```markdown
# Guard Report

## Summary
- 규칙 준수: 95%
- 맥락 일관성: Pass

## Violations
### Rules
- `src/api.ts` - 520줄 (500줄 초과)

### Context
- 현재 작업: TASK-001
- 이탈 감지: 없음

## Recommendations
[개선 권장 사항]
```

---

## 다음 단계 선택 (필수)

| 결과 | 권장 |
|------|------|
| 위반 발견 | `/refactor` 로 수정 |
| 맥락 이탈 | 원래 Task로 복귀 |
| 전체 통과 | 작업 계속 |

> **⚠️ 작업 완료 후 반드시 AskUserQuestion 호출**
>
> 검증이 완료되면 현재 상황을 분석하여 AskUserQuestion으로 다음 단계 선택지를 제시하세요.
> - 검증 결과 요약
> - 발견된 이슈 수정 옵션 (권장 표시, 이슈 있는 경우)
> - 다음 Task 진행 옵션
> - 추가 검증 옵션
> - 종료 옵션
