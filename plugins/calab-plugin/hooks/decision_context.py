#!/usr/bin/env python3
"""
decision_context.py - calab-claude-plugin 컨텍스트 인식 결정 훅

원더 무브 연구소 Claude Plug-in의 UserPromptSubmit 훅.
사용자 프롬프트 제출 시 컨텍스트 인식 규칙을 주입합니다.

기능:
  - Core Rules, Context Awareness 규칙 제공
  - 질문 트리거 조건 제공

원본: claude-monitoring-main
적용: calab-claude-plugin v2.4.0+
"""

import json
import sys
import os

# hook_utils에서 유틸리티 임포트
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hook_utils import setup_hook_config, log, json_get


# Core Rules 출력
FULL_RULES = """<core-rules>
## Core Rules

1. **Plan Mode Entry**: When `/wm` skill is invoked
   → Call EnterPlanMode() as the FIRST action
   → Skip remaining hook content

2. **Agent-based Exploration**: When file/code exploration is needed
   → Use `Task(subagent_type="Explore", ...)` instead of direct Glob/Grep
   → Exception: Direct Read is allowed when exact file path is known

3. **User Clarification**: When uncertain or decision is needed
   → Use AskUserQuestion
   → **MUST write in Korean (한국어)**, 2-4 options, mark recommended with "(권장)"
</core-rules>

<context-awareness>
## Context Awareness

**When prior conversation exists**:
- Short commands like "진행해", "수정해줘" → Refer to discussed content
- Do NOT re-ask, proceed directly

**When ambiguous without context**:
- New conversation with "수정해줘" → What? Where?
- Topic change with "다른 거 수정해" → What?
- Clarification needed via AskUserQuestion

**Decision Matrix**:
| Prior Context? | Matches Context? | Action |
|----------------|------------------|--------|
| Yes | Yes | ✅ Proceed |
| Yes | Different topic | ❓ Ask |
| No | - | ❓ Ask |
</context-awareness>

<additional-triggers>
## Additional Question Triggers

Regardless of context, AskUserQuestion required when:
- Affects 3+ files, approach unclear
- Multiple implementation strategies possible
- Modifies public API/interfaces
- User request contradicts discussed plan
</additional-triggers>

<key-principle>
Goal: NOT to ask about everything
Goal: Accurately understand user intent
If prior conversation is clear → Use it
If ambiguous without context → Ask
</key-principle>"""


def main():
    setup_hook_config("DecisionContext")

    # stdin에서 JSON 읽기
    try:
        json_input = sys.stdin.read()
        data = json.loads(json_input)
    except (json.JSONDecodeError, ValueError):
        log("JSON 파싱 실패")
        sys.exit(0)

    # 프롬프트 추출
    prompt = data.get('prompt', '')

    log(f"프롬프트 길이: {len(prompt)}자")

    # Core Rules 출력
    log("Core Rules 출력")
    print(FULL_RULES)

    sys.exit(0)


if __name__ == "__main__":
    main()
