#!/usr/bin/env python3
"""
Handoff Validator Hook - /handoff 실행 전 PRD 존재 확인

트리거: UserPromptSubmit 이벤트
동작: /handoff 실행 시 PRD.md 파일 존재 여부 확인

NOTE: 현재 hooks.json에 미등록 (비활성)
"""

import json
import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(os.getcwd())
DOCS_PATH = PROJECT_ROOT / '.claude' / 'docs' / 'active'


def find_latest_prd() -> bool:
    """가장 최근 기능 폴더에 PRD.md가 있는지 확인"""
    if not DOCS_PATH.exists():
        return False

    folders = sorted(
        [f for f in DOCS_PATH.iterdir() if f.is_dir()],
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )

    if not folders:
        return False

    return (folders[0] / 'PRD.md').exists()


def main():
    try:
        input_data = json.load(sys.stdin)
        user_input = input_data.get('user_input', '').strip().lower()

        # /handoff 명령어만 처리
        if not user_input.startswith('/handoff'):
            sys.exit(0)

        if not find_latest_prd():
            print("⚠️  /handoff 실행 불가: PRD.md가 없습니다. 먼저 /plan을 실행하세요.")

    except (json.JSONDecodeError, Exception):
        pass

    sys.exit(0)


if __name__ == '__main__':
    main()
