#!/usr/bin/env python3
"""
PreCompact Hook: Compact 실행 전 현재 상태 저장

이 스크립트는 Claude Code가 컨텍스트를 압축하기 전에 실행되어
현재 작업 상태를 자동으로 백업합니다.
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path


def main():
    # 프로젝트 디렉토리 확인
    project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '.')
    state_dir = Path(project_dir) / '.claude-state'
    memory_dir = Path(project_dir) / '.claude' / 'memory'

    # 디렉토리 생성
    state_dir.mkdir(parents=True, exist_ok=True)

    # 체크포인트 데이터 생성
    checkpoint = {
        "timestamp": datetime.now().isoformat(),
        "event": "pre_compact",
        "message": "Compact 실행 전 자동 저장됨"
    }

    # 기존 컨텍스트 파일 백업
    context_file = memory_dir / 'CURRENT_CONTEXT.md'
    if context_file.exists():
        try:
            with open(context_file, 'r', encoding='utf-8') as f:
                checkpoint["last_context"] = f.read()
        except Exception as e:
            checkpoint["context_read_error"] = str(e)

    # 기존 체크포인트가 있으면 히스토리에 추가
    checkpoint_file = state_dir / 'checkpoint.json'
    history_file = state_dir / 'checkpoint_history.json'

    if checkpoint_file.exists():
        try:
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                old_checkpoint = json.load(f)

            # 히스토리 로드 또는 생성
            history = []
            if history_file.exists():
                with open(history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)

            # 이전 체크포인트를 히스토리에 추가 (최대 10개 유지)
            history.append(old_checkpoint)
            history = history[-10:]

            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # 새 체크포인트 저장
    try:
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"체크포인트 저장 실패: {e}", file=sys.stderr)
        return

    # stdout으로 Claude에게 메시지 전달
    print("=" * 50)
    print("[PRE-COMPACT] 컨텍스트 압축 전 자동 저장")
    print("=" * 50)
    print(f" 저장 시간: {checkpoint['timestamp']}")
    print(f" 체크포인트: {checkpoint_file}")
    print("")
    print(" Compact 후 '/restore-context' 명령으로")
    print("   규칙과 작업 상태를 복원할 수 있습니다.")
    print("=" * 50)


if __name__ == "__main__":
    main()
