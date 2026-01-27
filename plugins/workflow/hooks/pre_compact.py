#!/usr/bin/env python3
"""
PreCompact Hook: Compact 실행 전 현재 상태 저장

이 스크립트는 Claude Code가 컨텍스트를 압축하기 전에 실행되어
현재 작업 상태를 자동으로 백업합니다.

기능:
    - FIFO 방식 체크포인트 관리 (최대 5개 슬롯)
    - 슬롯 번호와 요약 정보 포함
    - 컨텍스트 파일 자동 백업
"""

import sys
import os
from datetime import datetime
from pathlib import Path

from utils import load_json_file, save_json_file, MAX_CHECKPOINT_SLOTS

# 상수
CHECKPOINT_FILE_NAME = "checkpoints.json"


def get_context_summary(context: str, max_length: int = 100) -> str:
    """컨텍스트에서 요약을 추출합니다."""
    if not context:
        return "빈 컨텍스트"

    # 첫 번째 비어있지 않은 줄 찾기
    lines = [line.strip() for line in context.split('\n') if line.strip()]
    if not lines:
        return "빈 컨텍스트"

    # 제목 줄 찾기 (# 또는 ## 로 시작)
    for line in lines[:10]:
        if line.startswith('#'):
            summary = line.lstrip('#').strip()
            if summary:
                return summary[:max_length]

    # 제목이 없으면 첫 줄 사용
    return lines[0][:max_length]


def main():
    """메인 함수: 체크포인트를 저장합니다."""
    project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '.')
    home_dir = os.environ.get('HOME', '')

    # 상태 디렉토리 (프로젝트별)
    state_dir = Path(project_dir) / '.claude-state'
    state_dir.mkdir(parents=True, exist_ok=True)

    # 메모리 디렉토리 (프로젝트 우선, 없으면 글로벌)
    project_memory = Path(project_dir) / '.claude' / 'memory'
    global_memory = Path(home_dir) / '.claude' / 'memory'
    memory_dir = project_memory if project_memory.exists() else global_memory

    # 체크포인트 파일 경로
    checkpoint_file = state_dir / CHECKPOINT_FILE_NAME

    # 기존 체크포인트 로드
    checkpoints = load_json_file(checkpoint_file, default=[])

    # 다음 슬롯 번호 계산 (FIFO)
    if checkpoints:
        last_slot = checkpoints[-1].get('slot', 0)
        next_slot = (last_slot % MAX_CHECKPOINT_SLOTS) + 1
    else:
        next_slot = 1

    # 현재 컨텍스트 읽기
    context_content = ""
    context_file = memory_dir / 'CURRENT_CONTEXT.md'
    if context_file.exists():
        try:
            with open(context_file, 'r', encoding='utf-8') as f:
                context_content = f.read()
        except IOError as e:
            print(f"컨텍스트 파일 읽기 실패: {e}", file=sys.stderr)

    # 새 체크포인트 생성
    timestamp = datetime.now()
    new_checkpoint = {
        "slot": next_slot,
        "timestamp": timestamp.isoformat(),
        "time_display": timestamp.strftime('%m/%d %H:%M'),
        "event": "pre_compact",
        "summary": get_context_summary(context_content),
        "context": context_content if context_content else None
    }

    # FIFO: 최대 슬롯 수 유지
    checkpoints.append(new_checkpoint)
    if len(checkpoints) > MAX_CHECKPOINT_SLOTS:
        checkpoints = checkpoints[-MAX_CHECKPOINT_SLOTS:]

    # 저장
    if not save_json_file(checkpoint_file, checkpoints):
        print(f"체크포인트 저장 실패: {checkpoint_file}", file=sys.stderr)
        return

    # 출력
    print("")
    print(f"[PreCompact] 체크포인트 #{next_slot} 저장됨 ({timestamp.strftime('%H:%M')})")
    print(f"  요약: {new_checkpoint['summary']}")
    print("")
    print("  복원 방법:")
    print("  - /restore-context 명령으로 체크포인트 목록 확인")
    print("  - /restore-context [슬롯번호] 로 특정 시점 복원")
    print("")

    # 체크포인트 목록 미리보기
    print("  저장된 체크포인트:")
    for cp in reversed(checkpoints[-3:]):
        marker = "→" if cp['slot'] == next_slot else " "
        print(f"  {marker} #{cp['slot']} {cp['time_display']} - {cp['summary'][:40]}")

    if len(checkpoints) > 3:
        print(f"    ... 외 {len(checkpoints) - 3}개")


if __name__ == "__main__":
    main()
