#!/usr/bin/env python3
"""
SessionEnd Hook: 세션 종료 시 현재 상태 자동 저장

이 스크립트는 Claude Code 세션이 종료될 때 실행되어
현재 작업 상태를 자동으로 저장합니다.
"""

import json
import os
from datetime import datetime
from pathlib import Path


def main():
    project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '.')
    state_dir = Path(project_dir) / '.claude-state'

    # 디렉토리 생성
    state_dir.mkdir(parents=True, exist_ok=True)

    # 세션 종료 체크포인트 생성
    checkpoint = {
        "timestamp": datetime.now().isoformat(),
        "event": "session_end",
        "message": "세션 종료 시 자동 저장됨"
    }

    # 기존 체크포인트가 있으면 정보 유지
    checkpoint_file = state_dir / 'checkpoint.json'
    if checkpoint_file.exists():
        try:
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                old_checkpoint = json.load(f)

            # 기존 작업 정보 유지
            for key in ['current_task', 'progress', 'next_steps', 'important_files']:
                if key in old_checkpoint:
                    checkpoint[key] = old_checkpoint[key]
        except Exception:
            pass

    # 체크포인트 저장
    try:
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"체크포인트 저장 실패: {e}")
        return

    print("")
    print(" [SESSION END] 작업 상태가 저장되었습니다.")
    print(f"   시간: {checkpoint['timestamp']}")
    print("")


if __name__ == "__main__":
    main()
