#!/usr/bin/env python3
"""
SessionStart Hook: 세션 시작 시 컨텍스트 자동 복원 안내

이 스크립트는 Claude Code 세션이 시작될 때 실행되어:
1. 메모리 템플릿 자동 복사 (없는 경우)
2. 이전 작업 컨텍스트가 있으면 사용자에게 안내

참고: CLAUDE.md는 글로벌(~/.claude/CLAUDE.md)에서 자동 로드되므로 복사하지 않음
"""

import json
import os
import shutil
from pathlib import Path

from utils import format_time_ago, load_json_file


def setup_project_files(project_dir: Path, home_dir: Path) -> list:
    """
    프로젝트에 필요한 파일들을 글로벌에서 자동 복사

    복사 대상:
    - .claude/memory/: 메모리 템플릿 (없는 경우)

    참고: CLAUDE.md는 글로벌에서 자동 로드되므로 복사하지 않음
    """
    messages = []

    global_claude_dir = Path(home_dir) / '.claude'
    project_claude_dir = project_dir / '.claude'

    # 1. .claude/memory/ 디렉토리 및 템플릿 복사
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

    # 2. .claude-state 디렉토리 생성
    state_dir = project_dir / '.claude-state'
    if not state_dir.exists():
        try:
            state_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

    return messages


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

    # 체크포인트 확인 (새 형식: checkpoints.json)
    checkpoints_file = state_dir / 'checkpoints.json'
    checkpoints = load_json_file(checkpoints_file, default=[])

    # 구버전 호환: checkpoint.json
    if not checkpoints:
        old_checkpoint_file = state_dir / 'checkpoint.json'
        old_checkpoint = load_json_file(old_checkpoint_file)
        if old_checkpoint:
            checkpoints = [old_checkpoint]

    if checkpoints:
        has_context = True
        latest = checkpoints[-1]
        time_ago = format_time_ago(latest.get('timestamp', ''))

        messages.append(f" 체크포인트 {len(checkpoints)}개 발견 (최신: {time_ago})")

        if latest.get('summary'):
            messages.append(f"   요약: {latest['summary'][:50]}")

        if latest.get('current_task'):
            messages.append(f"   작업: {latest['current_task']}")

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

    # Silent Mode: 간결한 출력
    # 환경 변수로 VERBOSE 모드 지원 (CLAUDE_HOOKS_VERBOSE=1)
    verbose = os.environ.get('CLAUDE_HOOKS_VERBOSE', '') == '1'

    if verbose:
        # Verbose 모드: 전체 출력
        if messages:
            print("")
            print("=" * 50)
            print(" [SESSION START] 컨텍스트 복원 안내")
            print("=" * 50)
            for msg in messages:
                print(msg)
            print("")
            if has_context:
                print(" 복원 방법:")
                print("   /restore-context        → 체크포인트 목록 확인")
                print("   /restore-context [N]    → 슬롯 N 복원")

                # 체크포인트 목록 미리보기
                if checkpoints:
                    print("")
                    print(" 저장된 체크포인트:")
                    for cp in reversed(checkpoints[-3:]):
                        slot = cp.get('slot', '?')
                        time_display = cp.get('time_display', format_time_ago(cp.get('timestamp', '')))
                        summary = cp.get('summary', '요약 없음')[:35]
                        print(f"   #{slot} {time_display} - {summary}")

                    if len(checkpoints) > 3:
                        print(f"   ... 외 {len(checkpoints) - 3}개")

            print("=" * 50)
            print("")
    else:
        # Silent 모드: 한 줄 요약
        if has_context:
            cp_count = len(checkpoints) if checkpoints else 0
            if cp_count > 0:
                print(f"[Session] 체크포인트 {cp_count}개 → /restore-context [슬롯]으로 복원")
            else:
                print("[Session] 이전 컨텍스트 존재 → /restore-context로 복원 가능")


if __name__ == "__main__":
    main()
