#!/usr/bin/env python3
"""
SessionStart Hook: 세션 시작 시 컨텍스트 자동 복원 안내

이 스크립트는 Claude Code 세션이 시작될 때 실행되어:
1. CLAUDE.md가 없으면 글로벌에서 자동 복사
2. 이전 작업 컨텍스트가 있으면 사용자에게 안내
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path


def setup_project_files(project_dir: Path, home_dir: Path) -> list:
    """
    프로젝트에 필요한 파일들을 글로벌에서 자동 복사

    복사 대상:
    - CLAUDE.md: 플러그인 메인 설명서
    - .claude/memory/: 메모리 템플릿 (없는 경우)
    """
    messages = []

    global_claude_dir = Path(home_dir) / '.claude'
    project_claude_dir = project_dir / '.claude'

    # 1. CLAUDE.md 복사 (프로젝트에 없고 글로벌에 있는 경우)
    project_claude_md = project_dir / 'CLAUDE.md'
    global_claude_md = global_claude_dir / 'CLAUDE.md'

    if not project_claude_md.exists() and global_claude_md.exists():
        try:
            shutil.copy(global_claude_md, project_claude_md)
            messages.append(" ✅ CLAUDE.md 자동 복사됨 (글로벌 → 프로젝트)")
        except Exception as e:
            messages.append(f" ⚠️ CLAUDE.md 복사 실패: {e}")

    # 2. .claude/memory/ 디렉토리 및 템플릿 복사
    project_memory = project_claude_dir / 'memory'
    global_memory = global_claude_dir / 'memory'

    if not project_memory.exists() and global_memory.exists():
        try:
            project_memory.mkdir(parents=True, exist_ok=True)
            # 템플릿 파일들 복사
            for template in global_memory.glob('*.md'):
                dest = project_memory / template.name
                if not dest.exists():
                    shutil.copy(template, dest)
            messages.append(" ✅ 메모리 템플릿 자동 복사됨")
        except Exception as e:
            messages.append(f" ⚠️ 메모리 복사 실패: {e}")

    # 3. .claude-state 디렉토리 생성
    state_dir = project_dir / '.claude-state'
    if not state_dir.exists():
        try:
            state_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

    return messages


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
    project_dir = Path(os.environ.get('CLAUDE_PROJECT_DIR', '.'))
    home_dir = os.environ.get('HOME', '')

    # Step 1: 프로젝트에 필요한 파일 자동 복사
    setup_messages = setup_project_files(project_dir, home_dir)

    # 상태는 프로젝트별, 메모리는 글로벌
    state_dir = project_dir / '.claude-state'
    global_memory_dir = Path(home_dir) / '.claude' / 'memory'
    project_memory_dir = project_dir / '.claude' / 'memory'

    # 프로젝트 메모리 우선, 없으면 글로벌 사용
    memory_dir = project_memory_dir if project_memory_dir.exists() else global_memory_dir

    messages = setup_messages  # 자동 복사 메시지 포함
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
