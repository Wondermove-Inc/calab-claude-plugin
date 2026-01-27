#!/usr/bin/env python3
"""
PostToolUse Hook: 코드 품질 검증

이 스크립트는 Edit 또는 Write 도구 사용 후 실행되어
코드 품질 규칙 준수 여부를 검증합니다.

검증 항목:
1. 파일 줄 수 (일반: 300줄, 훅/스크립트: 500줄)
2. 함수 주석 존재 여부
"""

import json
import sys
import os
import re
from pathlib import Path
from datetime import datetime


# 설정 - 파일 유형별 줄 수 제한
FILE_LIMITS = {
    'default': {'max': 300, 'warn': 250},
    'hook': {'max': 500, 'warn': 400}  # 훅/스크립트는 더 유연하게
}

# 훅/스크립트 디렉토리 패턴
HOOK_DIRS = {'hooks', 'scripts', 'bin'}

# 검사 대상 확장자
CODE_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx',
    '.java', '.go', '.rs', '.cpp', '.c', '.h',
    '.cs', '.rb', '.php', '.swift', '.kt'
}

# 제외 디렉토리
EXCLUDE_DIRS = {
    'node_modules', 'dist', 'build', '.git',
    '__pycache__', 'venv', '.venv', 'vendor'
}


def should_skip_file(file_path):
    """검사를 건너뛸 파일인지 확인합니다."""
    path_parts = Path(file_path).parts
    for exclude_dir in EXCLUDE_DIRS:
        if exclude_dir in path_parts:
            return True
    return False


def is_hook_or_script(file_path):
    """훅 또는 스크립트 파일인지 확인합니다."""
    path_parts = Path(file_path).parts
    for hook_dir in HOOK_DIRS:
        if hook_dir in path_parts:
            return True
    return False


def count_lines(file_path):
    """파일의 줄 수를 계산합니다."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except Exception:
        return 0


def check_function_comments(content, file_ext):
    """함수에 주석이 있는지 검사합니다."""
    missing_comments = []

    # 언어별 함수 패턴
    patterns = {
        '.py': r'^(async\s+)?def\s+(\w+)\s*\(',
        '.js': r'(async\s+)?function\s+(\w+)\s*\(|const\s+(\w+)\s*=\s*(async\s+)?\([^)]*\)\s*=>|const\s+(\w+)\s*=\s*async\s+function',
        '.ts': r'(async\s+)?function\s+(\w+)\s*\(|const\s+(\w+)\s*=\s*(async\s+)?\([^)]*\)\s*=>|(\w+)\s*\([^)]*\)\s*:\s*\w+',
        '.tsx': r'(async\s+)?function\s+(\w+)\s*\(|const\s+(\w+)\s*=\s*(async\s+)?\([^)]*\)\s*=>',
        '.jsx': r'(async\s+)?function\s+(\w+)\s*\(|const\s+(\w+)\s*=\s*(async\s+)?\([^)]*\)\s*=>',
        '.java': r'(public|private|protected)?\s*(static)?\s*\w+\s+(\w+)\s*\(',
        '.go': r'func\s+(\w+)\s*\(',
    }

    pattern = patterns.get(file_ext)
    if not pattern:
        return []

    lines = content.split('\n')
    for i, line in enumerate(lines):
        # 들여쓰기가 너무 깊은 줄은 건너뛰기 (내부 함수 등)
        if line.startswith('        '):  # 8칸 이상 들여쓰기
            continue

        match = re.search(pattern, line)
        if match:
            # 함수명 추출
            func_name = None
            for group in match.groups():
                if group and group not in ['async', 'public', 'private', 'protected', 'static', 'const']:
                    if re.match(r'^[a-zA-Z_]\w*$', group):
                        func_name = group
                        break

            if func_name and not func_name.startswith('_') and func_name not in ['if', 'for', 'while', 'switch', 'catch']:
                # 이전 줄들에서 주석 찾기
                has_comment = False
                for j in range(max(0, i-10), i):
                    prev_line = lines[j].strip()
                    # 주석 패턴 확인
                    if prev_line.startswith(('"""', "'''", '/**', '//', '#', '/*', '*')):
                        has_comment = True
                        break
                    # 데코레이터나 어노테이션은 계속 검사
                    if prev_line.startswith('@'):
                        continue
                    # export, async 등 키워드는 계속 검사
                    if prev_line.startswith(('export', 'async', 'public', 'private', 'protected')):
                        continue
                    # 빈 줄은 계속 검사
                    if not prev_line:
                        continue
                    # 다른 코드가 있으면 중단
                    if prev_line and not prev_line.endswith('{') and not prev_line.endswith(','):
                        break

                if not has_comment:
                    missing_comments.append({
                        'line': i + 1,
                        'function': func_name
                    })

    return missing_comments


def print_quality_message(verbose, silent_msg, verbose_lines=None):
    """품질 메시지 출력 (verbose/silent 모드 자동 처리)"""
    if verbose and verbose_lines:
        print("")
        print("=" * 60)
        for line in verbose_lines:
            print(line)
        print("=" * 60)
    else:
        print(silent_msg)


def log_violation(project_dir, violation):
    """품질 위반을 기록합니다."""
    state_dir = Path(project_dir) / '.claude-state'
    state_dir.mkdir(parents=True, exist_ok=True)

    log_file = state_dir / 'quality_violations.json'

    violations = []
    if log_file.exists():
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                violations = json.load(f)
        except Exception:
            violations = []

    violation['timestamp'] = datetime.now().isoformat()
    violations.append(violation)

    # 최근 100개만 유지
    violations = violations[-100:]

    try:
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(violations, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def main():
    project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '.')

    # stdin에서 도구 사용 정보 읽기
    try:
        input_data = json.load(sys.stdin)
    except Exception:
        return

    tool_input = input_data.get('tool_input', {})
    file_path = tool_input.get('file_path', '')

    if not file_path:
        return

    # 제외 디렉토리 확인
    if should_skip_file(file_path):
        return

    # 소스 코드 파일인지 확인
    file_ext = Path(file_path).suffix.lower()
    if file_ext not in CODE_EXTENSIONS:
        return

    # 파일 존재 확인
    if not os.path.exists(file_path):
        return

    # 파일 내용 읽기
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return

    issues = []
    file_name = os.path.basename(file_path)

    # 1. 줄 수 검사 - 파일 유형별 제한 적용
    line_count = count_lines(file_path)

    # 훅/스크립트 파일은 더 유연한 제한 적용
    limits = FILE_LIMITS['hook'] if is_hook_or_script(file_path) else FILE_LIMITS['default']
    max_lines = limits['max']
    warn_threshold = limits['warn']

    # Silent Mode: 간결한 출력
    verbose = os.environ.get('CLAUDE_HOOKS_VERBOSE', '') == '1'

    if line_count > max_lines:
        issue = {
            'type': 'line_count_exceeded',
            'file': file_path,
            'lines': line_count,
            'max': max_lines,
            'severity': 'error'
        }
        issues.append(issue)
        log_violation(project_dir, issue)

        print_quality_message(
            verbose,
            f"[Quality] ❌ {file_name}: {line_count}줄 (최대 {max_lines}줄) → 분리 필요",
            [
                "[CODE QUALITY] 파일 줄 수 초과!",
                f"  파일: {file_name}",
                f"  현재: {line_count}줄 / 최대: {max_lines}줄",
                "  → 파일 분리 필요"
            ]
        )

    elif line_count > warn_threshold:
        if verbose:
            print(f"[Quality] ⚠️ {file_name}: {line_count}/{max_lines}줄 (분리 고려)")

    # 2. 함수 주석 검사
    missing_comments = check_function_comments(content, file_ext)

    if missing_comments:
        issue = {
            'type': 'missing_comments',
            'file': file_path,
            'functions': [mc['function'] for mc in missing_comments],
            'severity': 'warning'
        }
        issues.append(issue)
        log_violation(project_dir, issue)

        funcs = [mc['function'] for mc in missing_comments[:3]]
        extra = f" 외 {len(missing_comments) - 3}개" if len(missing_comments) > 3 else ""

        verbose_lines = [
            "[CODE QUALITY] 함수 주석 누락!",
            f"  파일: {file_name}",
            "  주석이 없는 함수:"
        ]
        for mc in missing_comments[:5]:
            verbose_lines.append(f"    - {mc['function']}() (line {mc['line']})")
        if len(missing_comments) > 5:
            verbose_lines.append(f"    ... 외 {len(missing_comments) - 5}개")

        print_quality_message(
            verbose,
            f"[Quality] ⚠️ {file_name}: 주석 누락 함수 {', '.join(funcs)}{extra}",
            verbose_lines
        )


if __name__ == "__main__":
    main()
