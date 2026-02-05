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

---

## Questioning Philosophy: 생각 파트너, 면접관 아님

> **"사용자의 에너지를 따라가라. 체크리스트를 순회하지 마라."**

### 핵심 원칙

| 원칙 | 설명 |
|------|------|
| **생각 파트너** | 면접관처럼 질문 나열 금지. 사용자의 흐름에 맞춰 대화 |
| **에너지 추적** | 사용자가 관심 보이는 주제를 파고들기 |
| **모호함 도전** | "좋은 UX"처럼 모호한 답변에 구체적 예시 요청 |
| **해석 제시** | 질문만 하지 말고 "이런 의미인가요?" 형태로 해석 포함 |

### Ask vs Decide 판단 기준

> **직접 결정할 수 있으면 묻지 마라. 되돌리기 비용이 높을 때만 물어라.**

| 조건 | 판단 | 예시 |
|------|------|------|
| 정답이 하나 | **직접 결정** | 파일 이름 컨벤션, import 순서 |
| 프로젝트에 패턴 존재 | **패턴 따르기** | 기존 코드에 camelCase면 그대로 |
| 되돌리기 비용 낮음 | **직접 결정** | 유틸 함수 위치, 변수명 |
| 되돌리기 비용 높음 | **질문** | DB 스키마, 공개 API, 아키텍처 |
| 사용자 의도 불명확 | **질문** | 비즈니스 로직, 우선순위, 범위 |
| 기술적 트레이드오프 | **옵션 제시** | 성능 vs 가독성, 라이브러리 선택 |

### 좋은 질문 vs 나쁜 질문

#### 나쁜 질문 (금지 패턴)

```
❌ 체크리스트 순회:
  "에러 처리는 어떻게 할까요?"
  "로깅은 필요한가요?"
  "테스트는 어떤 걸 작성할까요?"
  → 뻔한 질문을 연속으로 던짐. 시간 낭비.

❌ 뻔한 옵션:
  "TypeScript를 사용할까요, JavaScript를 사용할까요?"
  → 프로젝트가 이미 TypeScript면 물어볼 필요 없음.

❌ 면접 분위기:
  "확장성은 고려하시나요?"
  "보안 요구사항이 있나요?"
  → 추상적이고 당연한 질문.
```

#### 좋은 질문 (권장 패턴)

```
✅ 해석을 담은 옵션:
  "JWT 토큰 만료를 1시간으로 설정하려 합니다.
   리프레시 토큰도 필요하시면 sliding window 방식을 추천합니다.
   → 짧은 만료(1h) + 리프레시 토큰
   → 긴 만료(24h) + 리프레시 없음"

✅ 트레이드오프 제시:
  "페이지네이션 방식을 선택해야 합니다.
   → 오프셋: 구현 간단, 대량 데이터 시 느림
   → 커서: 일관된 성능, 구현 복잡"

✅ 모호함 도전:
  사용자: "깔끔한 UI로 만들어줘"
  → "깔끔하다는 게 미니멀 디자인인가요, 아니면 정보 밀도를 높이되
     정렬/여백을 깔끔히 하란 뜻인가요?"

✅ 맥락 기반 구체화:
  "현재 User 모델에 role 필드가 있는데,
   관리자 기능은 role 기반 접근 제어로 구현할까요,
   아니면 별도 permissions 테이블이 필요한가요?"
```

### 질문 안티패턴

| 안티패턴 | 문제 | 대안 |
|----------|------|------|
| **체크리스트 순회** | 사용자 피로, 시간 낭비 | 핵심 1-2개만 질문 |
| **뻔한 질문** | 프로젝트 컨텍스트 무시 | 기존 패턴 확인 후 따르기 |
| **추상적 질문** | 답변도 추상적 | 구체적 시나리오로 질문 |
| **연속 질문** | 대화 흐름 끊김 | 관련 질문 묶어서 한 번에 |
| **결정 회피** | 모든 걸 사용자에게 떠넘김 | 추천안 제시 + 근거 |

---

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
