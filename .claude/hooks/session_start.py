#!/usr/bin/env python3
"""
SessionStart Hook: 세션 시작 시 컨텍스트 자동 복원 안내

이 스크립트는 Claude Code 세션이 시작될 때 실행되어
이전 작업 컨텍스트가 있으면 사용자에게 알려줍니다.
"""

import json
import os
from datetime import datetime
from pathlib import Path


def format_time_ago(timestamp_str):
    """타임스탬프를 '몇 분/시간 전' 형식으로 변환"""
    try:
        timestamp = datetime.fromisoformat(timestamp_str)
        now = datetime.now()
        diff = now - timestamp

        if diff.days > 0:
            return f"{diff.days}일 전"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            return f"{hours}시간 전"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            return f"{minutes}분 전"
        else:
            return "방금 전"
    except Exception:
        return timestamp_str


def main():
    project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '.')
    state_dir = Path(project_dir) / '.claude-state'
    memory_dir = Path(project_dir) / '.claude' / 'memory'

    messages = []
    has_context = False

    # 체크포인트 확인
    checkpoint_file = state_dir / 'checkpoint.json'
    if checkpoint_file.exists():
        try:
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                checkpoint = json.load(f)

            timestamp = checkpoint.get('timestamp', '')
            time_ago = format_time_ago(timestamp)
            event = checkpoint.get('event', 'unknown')

            messages.append(f" 마지막 체크포인트: {time_ago}")
            messages.append(f"   이벤트: {event}")

            if checkpoint.get('current_task'):
                messages.append(f"   작업: {checkpoint['current_task']}")

            has_context = True
        except Exception:
            pass

    # 현재 컨텍스트 파일 확인
    context_file = memory_dir / 'CURRENT_CONTEXT.md'
    if context_file.exists():
        try:
            with open(context_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 현재 목표 추출 시도
            if '## 현재 목표' in content:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if '## 현재 목표' in line or '##  현재 목표' in line:
                        # 다음 비어있지 않은 줄 찾기
                        for j in range(i + 1, min(i + 5, len(lines))):
                            if lines[j].strip() and not lines[j].startswith('#') and not lines[j].startswith('-'):
                                messages.append(f" 이전 목표: {lines[j].strip()[:50]}...")
                                break
                        break

            has_context = True
            messages.append(" 이전 작업 컨텍스트가 존재합니다.")
        except Exception:
            pass

    # 규칙 파일 확인
    rules_file = memory_dir / 'PROJECT_RULES.md'
    if rules_file.exists():
        messages.append(" 프로젝트 규칙 파일이 존재합니다.")

    # 출력
    if messages:
        print("")
        print("=" * 50)
        print(" [SESSION START] 컨텍스트 복원 안내")
        print("=" * 50)
        for msg in messages:
            print(msg)
        print("")
        if has_context:
            print(" '/restore-context' 명령으로")
            print("   이전 작업을 이어갈 수 있습니다.")
        print("=" * 50)
        print("")


if __name__ == "__main__":
    main()
