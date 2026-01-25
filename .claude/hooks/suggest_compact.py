#!/usr/bin/env python3
"""
전략적 컴팩션 제안 훅 (Strategic Compact Suggestion)

컨텍스트 창이 가득 차기 전에 논리적 중단점에서 컴팩션을 제안합니다.
PreToolUse 훅으로 실행되어 각 도구 사용 전에 컨텍스트 상태를 체크합니다.

사용 방법:
    settings.json의 PreToolUse에 등록

참고:
    - everything-claude-code의 strategic-compact 기능 참조
    - 토큰 사용량은 직접 측정 불가하므로 파일 크기/작업량 기반 추정
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 경로 설정
HOME = Path.home()
CLAUDE_DIR = HOME / ".claude"
STATE_DIR = Path(os.getcwd()) / ".claude-state"
COMPACT_STATE_FILE = STATE_DIR / "compact_state.json"

# 임계값 설정
TOOL_CALL_THRESHOLD = 50  # 도구 호출 횟수 임계값
FILE_EDIT_THRESHOLD = 20  # 파일 수정 횟수 임계값
LINES_CHANGED_THRESHOLD = 500  # 변경된 라인 수 임계값
SESSION_DURATION_THRESHOLD = 30  # 세션 지속 시간 (분)


def load_state() -> dict:
    """컴팩션 상태 로드"""
    if COMPACT_STATE_FILE.exists():
        try:
            with open(COMPACT_STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    return {
        "tool_calls": 0,
        "file_edits": 0,
        "lines_changed": 0,
        "session_start": datetime.now().isoformat(),
        "last_suggestion": None,
        "suggestion_count": 0
    }


def save_state(state: dict) -> None:
    """컴팩션 상태 저장"""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with open(COMPACT_STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def calculate_usage_percentage(state: dict) -> float:
    """컨텍스트 사용량 추정 (0.0 ~ 1.0)"""
    tool_ratio = state["tool_calls"] / TOOL_CALL_THRESHOLD
    edit_ratio = state["file_edits"] / FILE_EDIT_THRESHOLD
    lines_ratio = state["lines_changed"] / LINES_CHANGED_THRESHOLD

    # 세션 시간 계산
    try:
        session_start = datetime.fromisoformat(state["session_start"])
        duration_minutes = (datetime.now() - session_start).total_seconds() / 60
        time_ratio = duration_minutes / SESSION_DURATION_THRESHOLD
    except (ValueError, KeyError):
        time_ratio = 0

    # 가중 평균 (도구 호출과 파일 수정에 더 높은 가중치)
    usage = (tool_ratio * 0.3 + edit_ratio * 0.3 + lines_ratio * 0.2 + time_ratio * 0.2)
    return min(usage, 1.0)


def should_suggest_compact(state: dict, usage: float) -> tuple[bool, str]:
    """컴팩션 제안 여부 결정"""

    # 이미 최근에 제안했으면 스킵
    if state.get("last_suggestion"):
        try:
            last = datetime.fromisoformat(state["last_suggestion"])
            if (datetime.now() - last).total_seconds() < 300:  # 5분 이내 재제안 방지
                return False, ""
        except ValueError:
            pass

    # 80% 이상 사용 시 제안
    if usage >= 0.8:
        return True, f"⚠️ 컨텍스트 사용량 {usage*100:.0f}% - 논리적 중단점에서 /compact 권장"

    # 70% 이상이고 의미있는 작업 완료 시점 (파일 수정 후)
    if usage >= 0.7 and state["file_edits"] > 0 and state["file_edits"] % 5 == 0:
        return True, f"💡 작업 중단점 - 컨텍스트 {usage*100:.0f}% 사용 중. /compact 고려"

    return False, ""


def update_state_for_tool(state: dict, tool_input: dict) -> dict:
    """도구 사용에 따른 상태 업데이트"""
    state["tool_calls"] += 1

    # Edit/Write 도구인 경우 파일 수정 카운트
    file_path = tool_input.get("file_path", "")
    if file_path:
        state["file_edits"] += 1

        # 변경된 라인 수 추정
        new_string = tool_input.get("new_string", "")
        old_string = tool_input.get("old_string", "")
        content = tool_input.get("content", "")

        if new_string or old_string:
            # Edit 도구
            lines_changed = abs(new_string.count('\n') - old_string.count('\n')) + 1
        elif content:
            # Write 도구
            lines_changed = content.count('\n') + 1
        else:
            lines_changed = 1

        state["lines_changed"] += lines_changed

    return state


def main():
    """메인 실행 함수"""
    try:
        # stdin에서 도구 입력 읽기
        input_data = json.load(sys.stdin)
        tool_input = input_data.get("tool_input", {})
        tool_name = input_data.get("tool_name", "")
    except (json.JSONDecodeError, IOError):
        # 입력이 없거나 파싱 실패 시 패스
        print(json.dumps({"result": "pass"}))
        return

    # 상태 로드
    state = load_state()

    # Edit/Write 도구인 경우에만 상태 업데이트
    if tool_name in ("Edit", "Write"):
        state = update_state_for_tool(state, tool_input)
    else:
        state["tool_calls"] += 1

    # 사용량 계산
    usage = calculate_usage_percentage(state)

    # 컴팩션 제안 여부 결정
    should_suggest, message = should_suggest_compact(state, usage)

    if should_suggest:
        state["last_suggestion"] = datetime.now().isoformat()
        state["suggestion_count"] += 1
        save_state(state)

        # 경고 메시지 출력 (작업은 계속 진행)
        print(json.dumps({
            "result": "warn",
            "message": message
        }))
    else:
        save_state(state)
        print(json.dumps({"result": "pass"}))


if __name__ == "__main__":
    main()
