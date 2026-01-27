#!/usr/bin/env python3
"""
statusline_command.py - calab-claude-plugin 상태 라인 스크립트

원더 무브 연구소 Claude Plug-in의 상태 라인 표시.
모델명, 컨텍스트 사용량, 현재 디렉토리, Git 브랜치를 표시합니다.

형식: [Model] ████░░░░░░ XX.X% | ➜ directory git:(branch)

색상:
- 초록: 50% 미만
- 노랑: 50-74%
- 빨강: 75% 이상

원본: claude-monitoring-main
적용: calab-claude-plugin v2.3.0+
"""

import json
import sys
import os
import subprocess


# ANSI 색상 코드
COLORS = {
    "reset": "\033[0m",
    "dim_green": "\033[2;32m",
    "dim_yellow": "\033[2;33m",
    "dim_red": "\033[2;31m",
    "gray": "\033[90m",
    "white": "\033[37m",
    "bold_green": "\033[1;32m",
    "cyan": "\033[36m",
}


def get_model_name(data: dict) -> str:
    """모델 이름 추출 (첫 단어만)"""
    model_full = data.get("model", {}).get("display_name", "Unknown")
    return model_full.split()[0] if model_full else "Unknown"


def get_context_info(data: dict) -> tuple:
    """
    컨텍스트 사용량 정보 반환
    Returns: (progress_bar, percent_str, color_code)
    """
    context_window = data.get("context_window", {})
    context_size = context_window.get("context_window_size", 200000)
    usage = context_window.get("current_usage")

    if not usage:
        return "░" * 10, "0%", COLORS["dim_green"]

    # 토큰 계산
    current = (
        usage.get("input_tokens", 0) +
        usage.get("cache_creation_input_tokens", 0) +
        usage.get("cache_read_input_tokens", 0) +
        usage.get("output_tokens", 0)
    )

    percent = (current * 100) / context_size
    percent_int = int(percent)

    # 프로그레스 바 생성 (10칸)
    filled = min(percent_int // 10, 10)
    empty = 10 - filled
    bar = "█" * filled + "░" * empty

    # 색상 결정
    if percent_int >= 75:
        color = COLORS["dim_red"]
    elif percent_int >= 50:
        color = COLORS["dim_yellow"]
    else:
        color = COLORS["dim_green"]

    percent_str = f"{percent:.1f}%"

    return bar, percent_str, color


def get_git_info(cwd: str) -> str:
    """Git 브랜치 및 상태 정보"""
    try:
        # Git 디렉토리 확인
        result = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--git-dir"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return ""

        # 브랜치 이름
        result = subprocess.run(
            ["git", "-C", cwd, "--no-optional-locks", "symbolic-ref", "--short", "HEAD"],
            capture_output=True,
            text=True
        )
        branch = result.stdout.strip() if result.returncode == 0 else "detached"

        # 변경 사항 확인
        result1 = subprocess.run(
            ["git", "-C", cwd, "--no-optional-locks", "diff", "--quiet"],
            capture_output=True
        )
        result2 = subprocess.run(
            ["git", "-C", cwd, "--no-optional-locks", "diff", "--cached", "--quiet"],
            capture_output=True
        )
        has_changes = result1.returncode != 0 or result2.returncode != 0

        if has_changes:
            return f" git:({branch}) ✗"
        else:
            return f" git:({branch})"

    except (subprocess.SubprocessError, OSError):
        return ""


def main():
    # stdin에서 JSON 읽기
    try:
        json_input = sys.stdin.read()
        data = json.loads(json_input)
    except (json.JSONDecodeError, ValueError):
        print("[Unknown] ░░░░░░░░░░ 0% | ➜ unknown")
        return

    # 모델 이름
    model = get_model_name(data)

    # 컨텍스트 정보
    bar, percent_str, ctx_color = get_context_info(data)

    # 디렉토리 정보
    workspace = data.get("workspace", {})
    cwd = workspace.get("current_dir", os.getcwd())
    dir_name = os.path.basename(cwd)

    # Git 정보
    git_status = get_git_info(cwd)

    # 출력 포맷
    # [Model] ████░░░░░░ XX.X% | ➜ directory git:(branch)
    output = (
        f"{COLORS['gray']}[{COLORS['reset']}"
        f"{COLORS['white']}{model}{COLORS['reset']}"
        f"{COLORS['gray']}]{COLORS['reset']} "
        f"{ctx_color}{bar}{COLORS['reset']} {percent_str} | "
        f"{COLORS['bold_green']}➜{COLORS['reset']} "
        f"{COLORS['cyan']}{dir_name}{COLORS['reset']}"
        f"{git_status}"
    )

    print(output, end="")


if __name__ == "__main__":
    main()
