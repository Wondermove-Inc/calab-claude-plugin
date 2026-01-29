---
name: clarification-protocol
description: |
  Subagent clarification protocol - return flags instead of AskUserQuestion.
  Auto-loaded by subagents that need user clarification.
  서브에이전트에서 AskUserQuestion 대신 플래그를 반환하여 메인 컨텍스트에서 처리.
user-invocable: false
---

# Clarification Protocol for Subagents

## CRITICAL: No AskUserQuestion - Return Flags Instead

**DO NOT use AskUserQuestion in this agent.**

This agent runs as a subagent and AskUserQuestion calls do not display in the CLI.
Instead, return flags and data that the calling skill (main context) will use to call AskUserQuestion.

## When User Clarification is Needed

Instead of calling AskUserQuestion, set flags in the return result:

### Return Format

```json
{
  "needs_clarification": true,
  "clarification_type": "<type>",
  "clarification_data": {
    "question": "사용자에게 표시할 질문",
    "header": "짧은 헤더 (12자 이내)",
    "options": [
      {"value": "option1", "label": "옵션 1", "description": "설명"},
      {"value": "option2", "label": "옵션 2", "description": "설명"}
    ],
    "multiSelect": false
  }
}
```

### Clarification Types

| clarification_type | When to set | Data to include |
|--------------------|-------------|-----------------|
| scope | 개발 범위 불명확 | scope_options |
| tech_decision | 기술 스택 선택 필요 | tech_options |
| architecture_pattern | 아키텍처 패턴 선택 | pattern_options |
| priority | 우선순위 결정 필요 | priority_options |
| validation_failure | Task 검증 실패 | affected_phases |
| test_failure | 테스트 실패 대응 | failure_options |
| null | 명확한 요청, 결정 불필요 | - |

### Example: Scope Clarification

```json
{
  "needs_clarification": true,
  "clarification_type": "scope",
  "clarification_data": {
    "question": "개발 범위를 확인합니다. 어느 영역에 해당하나요?",
    "header": "범위",
    "options": [
      {"value": "backend", "label": "백엔드", "description": "API, 서비스, 데이터 처리"},
      {"value": "frontend", "label": "프론트엔드", "description": "UI, 컴포넌트, 화면"},
      {"value": "full_stack", "label": "전체", "description": "여러 영역에 걸친 기능"}
    ]
  }
}
```

### Example: Tech Decision

```json
{
  "needs_clarification": true,
  "clarification_type": "tech_decision",
  "clarification_data": {
    "question": "인증 방식을 선택해주세요.",
    "header": "인증",
    "options": [
      {"value": "jwt", "label": "JWT (권장)", "description": "무상태, 확장성 좋음"},
      {"value": "session", "label": "Session", "description": "서버 측 상태 관리"},
      {"value": "oauth", "label": "OAuth 2.0", "description": "외부 인증 연동"}
    ]
  }
}
```

## IMPORTANT Rules

1. **DO NOT use AskUserQuestion** - this agent runs in a subagent context
2. **Return flags instead** - the calling skill will handle user interaction
3. **Include clarification_data** with all necessary information
4. **Use Korean for user-facing strings** (label, description, question)
5. **Keep options to 2-4 choices** - AskUserQuestion supports max 4 options
6. **NO MARKDOWN in clarification_data** - AskUserQuestion renders as plain text

---

## Text Formatting Rules (CRITICAL)

⚠️ **AskUserQuestion은 CLI에서 plain text로 렌더링됩니다. Markdown은 지원되지 않습니다.**

### 금지된 패턴

| 패턴 | 문제 | 대체 |
|------|------|------|
| `**bold**` | `**` 그대로 출력됨 | `[대괄호]` 사용 |
| `*italic*` | `*` 그대로 출력됨 | 그냥 텍스트 |
| `` `code` `` | 백틱 그대로 출력됨 | 따옴표 또는 그대로 |
| `# Header` | `#` 그대로 출력됨 | 이모지 prefix |

### 올바른 예시

```json
{
  "clarification_data": {
    "question": "추가 파일이 발견되었습니다.\n\n[원래 계획] 17개 파일\n[추가 발견] 5개 파일",
    "header": "추가 파일",
    "options": [
      {"value": "include", "label": "포함하여 진행 (권장)", "description": "추가 파일도 함께 처리"},
      {"value": "skip", "label": "건너뛰기", "description": "원래 계획만 진행"}
    ]
  }
}
```

### 레이블 표현 가이드

| 용도 | 권장 형식 |
|------|----------|
| 섹션 레이블 | `[레이블] 내용` |
| 강조 | `⚠️ 중요:` 또는 대문자 |
| 파일명 | `filename.tsx` 또는 `"filename.tsx"` |
| 숫자 | `17개 파일` 또는 `(17개)` |
