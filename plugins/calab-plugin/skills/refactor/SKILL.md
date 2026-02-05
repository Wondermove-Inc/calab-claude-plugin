---
name: refactor
description: |
  리팩토링. 데드 코드 정리, 중복 제거, 코드 개선을 수행합니다.
argument-hint: "[--dead-code|--duplicates|--imports|--cleanup] [경로]"
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash, Task]
skills: [project-rules, code-quality, clarification-protocol, skill-completion-rules]
agents:
  primary: refactor-cleaner
  orchestration:
    dead-code: [calab-plugin:refactor-cleaner]
    duplicates: [calab-plugin:refactor-cleaner]
    imports: [calab-plugin:refactor-cleaner]
    cleanup: [calab-plugin:refactor-cleaner, calab-plugin:code-reviewer]
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

# /refactor - 리팩토링

> **데드 코드 정리, 중복 제거, 코드 개선**

---

## 사용법

```bash
/refactor [경로]            # 전체 리팩토링 분석
/refactor --dead-code       # 미사용 코드 탐지/제거
/refactor --duplicates      # 중복 코드 탐지
/refactor --imports         # 미사용 import 정리
/refactor --cleanup         # 전체 클린업
```

---

## 에이전트 호출 (필수)

> **이 스킬이 로드되면 아래 지침을 따라 Task 도구를 호출하세요.**

```python
Task(
    subagent_type="calab-plugin:refactor-cleaner",
    description="리팩토링",
    prompt="""
[Role] 리팩토링 전문가
[Goal] {경로}의 코드 품질 개선
[Scope] {--dead-code|--duplicates|--imports|--cleanup}

## 작업 항목
### Dead Code
- 미사용 함수/변수
- 도달 불가 코드
- 주석 처리된 코드

### Duplicates
- 3회+ 반복 패턴
- 복사-붙여넣기 코드
- 유사 로직

### Imports
- 미사용 import
- 중복 import
- 잘못된 경로

[Output]
- 변경 전/후 diff
- 리팩토링 보고서
"""
)
```

---

## 검사 유형

| 옵션 | 설명 |
|------|------|
| `--dead-code` | 미사용 코드 탐지 및 제거 |
| `--duplicates` | 중복 코드 탐지 및 추출 |
| `--imports` | import 문 정리 |
| `--cleanup` | 위 전체 + 포맷팅 |

---

## 산출물 (필수)

| 산출물 | 경로 |
|--------|------|
| 리팩토링 보고서 | `.claude/docs/refactor-report.md` |

### 보고서 형식

```markdown
# Refactoring Report

## Summary
- 제거된 코드: N줄
- 통합된 중복: N개
- 정리된 import: N개

## Changes
### Dead Code Removed
- `file.ts:10-20` - 미사용 함수 `unusedFn`

### Duplicates Extracted
- `utils/helper.ts` - 공통 로직 추출

## Before/After
[diff 또는 비교]
```

---

## 다음 단계 선택 (필수)

| 완료 후 | 권장 |
|--------|------|
| 리팩토링 완료 | 테스트 실행 확인 |
| 대규모 변경 | `/security` 검사 |

> **⚠️ 작업 완료 후 반드시 AskUserQuestion 호출**
>
> 리팩토링이 완료되면 현재 상황을 분석하여 AskUserQuestion으로 다음 단계 선택지를 제시하세요.
