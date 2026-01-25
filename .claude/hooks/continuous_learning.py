#!/usr/bin/env python3
"""
연속 학습 훅 (Continuous Learning)

세션 종료 시 사용된 패턴을 자동으로 추출하여 재사용 가능한 형태로 저장합니다.
SessionEnd/Stop 훅으로 실행됩니다.

기능:
    - 세션에서 자주 사용된 코드 패턴 추출
    - 반복된 수정 패턴 학습
    - 프로젝트별 컨벤션 자동 학습

참고:
    - everything-claude-code의 continuous-learning 기능 참조
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from collections import Counter

# 경로 설정
HOME = Path.home()
CLAUDE_DIR = HOME / ".claude"
LEARNED_DIR = CLAUDE_DIR / "learned"
STATE_DIR = Path(os.getcwd()) / ".claude-state"
HISTORY_FILE = STATE_DIR / "session_history.json"
PATTERNS_FILE = LEARNED_DIR / "patterns.json"


def ensure_dirs():
    """필요한 디렉토리 생성"""
    LEARNED_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)


def load_session_history() -> list:
    """세션 히스토리 로드"""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return []


def load_patterns() -> dict:
    """학습된 패턴 로드"""
    if PATTERNS_FILE.exists():
        try:
            with open(PATTERNS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {
        "code_patterns": [],
        "naming_conventions": {},
        "import_patterns": [],
        "error_fixes": [],
        "last_updated": None
    }


def save_patterns(patterns: dict) -> None:
    """패턴 저장"""
    patterns["last_updated"] = datetime.now().isoformat()
    with open(PATTERNS_FILE, 'w', encoding='utf-8') as f:
        json.dump(patterns, f, indent=2, ensure_ascii=False)


def extract_code_patterns(history: list) -> list:
    """코드 패턴 추출"""
    patterns = []

    for entry in history:
        if entry.get("type") == "edit":
            old_code = entry.get("old_string", "")
            new_code = entry.get("new_string", "")

            # 반복적인 수정 패턴 감지
            if old_code and new_code:
                pattern = {
                    "type": "refactor",
                    "from": old_code[:200],  # 너무 길면 잘라냄
                    "to": new_code[:200],
                    "file_type": Path(entry.get("file", "")).suffix,
                    "count": 1
                }
                patterns.append(pattern)

    return patterns


def extract_naming_conventions(history: list) -> dict:
    """네이밍 컨벤션 추출"""
    conventions = {
        "variables": Counter(),
        "functions": Counter(),
        "classes": Counter(),
        "files": Counter()
    }

    # 파일명에서 패턴 추출
    for entry in history:
        file_path = entry.get("file", "")
        if file_path:
            filename = Path(file_path).stem

            # 케이스 감지
            if "-" in filename:
                conventions["files"]["kebab-case"] += 1
            elif "_" in filename:
                conventions["files"]["snake_case"] += 1
            elif filename[0].isupper():
                conventions["files"]["PascalCase"] += 1
            else:
                conventions["files"]["camelCase"] += 1

    # 가장 많이 사용된 컨벤션 반환
    result = {}
    for key, counter in conventions.items():
        if counter:
            result[key] = counter.most_common(1)[0][0]

    return result


def extract_import_patterns(history: list) -> list:
    """import 패턴 추출"""
    patterns = []
    import_regex = re.compile(r'^(import|from)\s+.+', re.MULTILINE)

    for entry in history:
        new_code = entry.get("new_string", "")
        if new_code:
            imports = import_regex.findall(new_code)
            patterns.extend(imports[:5])  # 최대 5개

    return list(set(patterns))[:20]  # 중복 제거 후 최대 20개


def extract_error_fixes(history: list) -> list:
    """에러 수정 패턴 추출"""
    fixes = []

    for i, entry in enumerate(history):
        # 에러 후 수정 패턴 감지
        if entry.get("type") == "error":
            error_msg = entry.get("message", "")

            # 다음 항목이 수정이면 패턴으로 저장
            if i + 1 < len(history) and history[i + 1].get("type") == "edit":
                fix = {
                    "error": error_msg[:200],
                    "fix": history[i + 1].get("new_string", "")[:200],
                    "file_type": Path(history[i + 1].get("file", "")).suffix
                }
                fixes.append(fix)

    return fixes[:10]  # 최대 10개


def merge_patterns(existing: dict, new: dict) -> dict:
    """기존 패턴과 새 패턴 병합"""
    merged = existing.copy()

    # 코드 패턴 병합 (최대 50개 유지)
    merged["code_patterns"].extend(new.get("code_patterns", []))
    merged["code_patterns"] = merged["code_patterns"][-50:]

    # 네이밍 컨벤션 업데이트
    merged["naming_conventions"].update(new.get("naming_conventions", {}))

    # import 패턴 병합 (최대 30개 유지)
    existing_imports = set(merged.get("import_patterns", []))
    new_imports = set(new.get("import_patterns", []))
    merged["import_patterns"] = list(existing_imports | new_imports)[-30:]

    # 에러 수정 병합 (최대 20개 유지)
    merged["error_fixes"].extend(new.get("error_fixes", []))
    merged["error_fixes"] = merged["error_fixes"][-20:]

    return merged


def generate_learning_report(patterns: dict) -> str:
    """학습 보고서 생성"""
    report = []
    report.append("📚 연속 학습 완료")
    report.append("━" * 40)

    if patterns.get("naming_conventions"):
        report.append("\n📝 네이밍 컨벤션")
        for key, value in patterns["naming_conventions"].items():
            report.append(f"  • {key}: {value}")

    if patterns.get("code_patterns"):
        report.append(f"\n🔄 코드 패턴: {len(patterns['code_patterns'])}개 학습됨")

    if patterns.get("error_fixes"):
        report.append(f"\n🔧 에러 수정 패턴: {len(patterns['error_fixes'])}개 학습됨")

    report.append(f"\n💾 저장 위치: {PATTERNS_FILE}")

    return "\n".join(report)


def main():
    """메인 실행 함수"""
    ensure_dirs()

    # 세션 히스토리 로드
    history = load_session_history()

    if not history:
        print(json.dumps({
            "result": "pass",
            "message": "학습할 세션 히스토리가 없습니다."
        }))
        return

    # 기존 패턴 로드
    existing_patterns = load_patterns()

    # 새 패턴 추출
    new_patterns = {
        "code_patterns": extract_code_patterns(history),
        "naming_conventions": extract_naming_conventions(history),
        "import_patterns": extract_import_patterns(history),
        "error_fixes": extract_error_fixes(history)
    }

    # 패턴 병합 및 저장
    merged_patterns = merge_patterns(existing_patterns, new_patterns)
    save_patterns(merged_patterns)

    # 보고서 생성
    report = generate_learning_report(new_patterns)

    print(json.dumps({
        "result": "pass",
        "message": report
    }))


if __name__ == "__main__":
    main()
