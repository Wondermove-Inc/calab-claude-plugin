#!/usr/bin/env python3
"""
자동 포맷팅 훅 (Auto Format)

파일 수정 후 자동으로 코드 포맷팅을 실행합니다.
PostToolUse 훅으로 Edit/Write 도구 사용 후 실행됩니다.

기능:
    - Prettier 자동 실행 (JS/TS/CSS/JSON/MD)
    - Black 자동 실행 (Python)
    - gofmt 자동 실행 (Go)
    - console.log/print 잔류 경고
    - TypeScript 타입 체크 (선택적)

참고:
    - everything-claude-code의 PostToolUse 훅 기능 참조
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# 경로 설정
CWD = Path(os.getcwd())

# 상수
FORMATTER_TIMEOUT_SECONDS = 30
TYPE_CHECK_TIMEOUT_SECONDS = 60

# 환경 변수 플래그 (CLAUDE_TYPE_CHECK=1로 TypeScript 타입 체크 활성화)
TYPE_CHECK_ENABLED = os.environ.get('CLAUDE_TYPE_CHECK', '') == '1'

# 파일 확장자별 포맷터 설정
FORMATTERS = {
    # JavaScript/TypeScript (Prettier)
    ".js": {"cmd": "prettier", "args": ["--write"]},
    ".jsx": {"cmd": "prettier", "args": ["--write"]},
    ".ts": {"cmd": "prettier", "args": ["--write"]},
    ".tsx": {"cmd": "prettier", "args": ["--write"]},
    ".css": {"cmd": "prettier", "args": ["--write"]},
    ".scss": {"cmd": "prettier", "args": ["--write"]},
    ".json": {"cmd": "prettier", "args": ["--write"]},
    ".md": {"cmd": "prettier", "args": ["--write"]},
    ".yaml": {"cmd": "prettier", "args": ["--write"]},
    ".yml": {"cmd": "prettier", "args": ["--write"]},

    # Python (Black)
    ".py": {"cmd": "black", "args": ["--quiet"]},

    # Go (gofmt)
    ".go": {"cmd": "gofmt", "args": ["-w"]},

    # Rust (rustfmt)
    ".rs": {"cmd": "rustfmt", "args": []},
}

# console.log/print 감지 패턴
DEBUG_PATTERNS = {
    ".js": ["console.log", "console.debug", "debugger"],
    ".jsx": ["console.log", "console.debug", "debugger"],
    ".ts": ["console.log", "console.debug", "debugger"],
    ".tsx": ["console.log", "console.debug", "debugger"],
    ".py": ["print(", "breakpoint()", "pdb.set_trace()"],
    ".go": ["fmt.Println", "fmt.Printf"],
}


def check_command_exists(cmd: str) -> bool:
    """명령어 존재 여부 확인 (크로스플랫폼 호환)"""
    return shutil.which(cmd) is not None


def run_formatter(file_path: str, formatter: Dict) -> Tuple[bool, str]:
    """포맷터 실행"""
    cmd = formatter["cmd"]
    args = formatter["args"]

    if not check_command_exists(cmd):
        return False, f"{cmd} not found"

    try:
        # npx를 통해 실행 (로컬 설치 우선)
        if cmd == "prettier":
            full_cmd = ["npx", cmd] + args + [file_path]
        else:
            full_cmd = [cmd] + args + [file_path]

        # shell=False (기본값)로 shell injection 방지
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            timeout=FORMATTER_TIMEOUT_SECONDS,
            shell=False
        )

        if result.returncode == 0:
            return True, f"Formatted with {cmd}"
        else:
            return False, result.stderr[:200]

    except subprocess.TimeoutExpired:
        return False, "Formatter timeout"
    except Exception as e:
        return False, str(e)[:200]


def check_debug_statements(file_path: str, ext: str) -> List[Dict]:
    """디버그 문 검사

    문자열 리터럴 내의 패턴은 무시하고, 실제 코드의 디버그 문만 감지합니다.
    """
    patterns = DEBUG_PATTERNS.get(ext, [])
    if not patterns:
        return []

    warnings = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            # 주석 라인 스킵
            if stripped.startswith("//") or stripped.startswith("#") or stripped.startswith("*"):
                continue

            for pattern in patterns:
                if pattern in line:
                    # 문자열 리터럴 내부인지 간단 체크 (따옴표 짝수 여부)
                    before_pattern = line.split(pattern)[0]
                    single_quotes = before_pattern.count("'") - before_pattern.count("\\'")
                    double_quotes = before_pattern.count('"') - before_pattern.count('\\"')

                    # 홀수개의 따옴표가 있으면 문자열 내부로 판단
                    if single_quotes % 2 == 0 and double_quotes % 2 == 0:
                        warnings.append({
                            "line": i,
                            "pattern": pattern,
                            "content": stripped[:80]
                        })
    except (IOError, UnicodeDecodeError):
        pass

    return warnings


def run_type_check(file_path: str) -> Tuple[bool, str]:
    """TypeScript 타입 체크 (선택적)"""
    # tsconfig.json이 있는 경우에만 실행
    if not (CWD / "tsconfig.json").exists():
        return True, "No tsconfig.json"

    try:
        # shell=False (기본값)로 shell injection 방지
        result = subprocess.run(
            ["npx", "tsc", "--noEmit", file_path],
            capture_output=True,
            text=True,
            timeout=TYPE_CHECK_TIMEOUT_SECONDS,
            shell=False
        )

        if result.returncode == 0:
            return True, "Type check passed"
        else:
            # 에러 메시지 간략화
            errors = result.stdout.split("\n")[:5]
            return False, "\n".join(errors)

    except (subprocess.TimeoutExpired, FileNotFoundError):
        return True, "Type check skipped"


def main() -> None:
    """메인 실행 함수"""
    try:
        # stdin에서 도구 입력 읽기
        input_data = json.load(sys.stdin)
        tool_input = input_data.get("tool_input", {})
        tool_name = input_data.get("tool_name", "")
    except (json.JSONDecodeError, IOError):
        print(json.dumps({"result": "pass"}))
        return

    # Edit/Write 도구가 아니면 패스
    if tool_name not in ("Edit", "Write"):
        print(json.dumps({"result": "pass"}))
        return

    # 파일 경로 추출
    file_path = tool_input.get("file_path", "")
    if not file_path or not Path(file_path).exists():
        print(json.dumps({"result": "pass"}))
        return

    ext = Path(file_path).suffix.lower()
    messages = []
    warnings = []

    # 1. 포맷터 실행
    if ext in FORMATTERS:
        success, msg = run_formatter(file_path, FORMATTERS[ext])
        if success:
            messages.append(f"✓ {msg}")
        else:
            messages.append(f"⚠ Format failed: {msg}")

    # 2. 디버그 문 검사
    debug_warnings = check_debug_statements(file_path, ext)
    if debug_warnings:
        for warn in debug_warnings[:3]:  # 최대 3개만 표시
            warnings.append(
                f"⚠ Line {warn['line']}: {warn['pattern']} found - {warn['content']}"
            )

    # 3. TypeScript 타입 체크 (ts/tsx 파일만, 환경변수로 활성화)
    if TYPE_CHECK_ENABLED and ext in (".ts", ".tsx"):
        success, msg = run_type_check(file_path)
        if not success:
            warnings.append(f"❌ Type error: {msg[:100]}")

    # 결과 출력
    result = {"result": "pass"}

    if warnings:
        result["result"] = "warn"
        result["message"] = "\n".join(warnings)
    elif messages:
        result["message"] = " | ".join(messages)

    print(json.dumps(result))


if __name__ == "__main__":
    main()
