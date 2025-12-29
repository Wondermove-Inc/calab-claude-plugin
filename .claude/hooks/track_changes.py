#!/usr/bin/env python3
"""
PostToolUse Hook: 파일 변경 추적

이 스크립트는 Edit 또는 Write 도구 사용 후 실행되어
변경된 파일을 추적합니다.
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path


def main():
    project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '.')
    state_dir = Path(project_dir) / '.claude-state'

    # 디렉토리 생성
    state_dir.mkdir(parents=True, exist_ok=True)

    # stdin에서 도구 사용 정보 읽기
    try:
        input_data = json.load(sys.stdin)
    except Exception:
        return  # JSON 파싱 실패 시 조용히 종료

    # 파일 경로 추출
    tool_input = input_data.get('tool_input', {})
    file_path = tool_input.get('file_path', '')

    if not file_path:
        return

    # 변경 파일 로그에 추가
    changes_file = state_dir / 'recent_changes.json'

    changes = []
    if changes_file.exists():
        try:
            with open(changes_file, 'r', encoding='utf-8') as f:
                changes = json.load(f)
        except Exception:
            changes = []

    # 새 변경 기록 추가
    change_record = {
        "timestamp": datetime.now().isoformat(),
        "file_path": file_path,
        "tool": input_data.get('tool_name', 'unknown')
    }

    # 중복 제거 (같은 파일은 최신 것만 유지)
    changes = [c for c in changes if c.get('file_path') != file_path]
    changes.append(change_record)

    # 최근 50개만 유지
    changes = changes[-50:]

    # 저장
    try:
        with open(changes_file, 'w', encoding='utf-8') as f:
            json.dump(changes, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


if __name__ == "__main__":
    main()
