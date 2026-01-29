#!/usr/bin/env python3
"""
Log Rotation Hook: 로그 파일 크기 관리

세션 시작 시 실행되어 로그 파일 크기를 체크하고:
- 50KB 초과 시 자동 로테이션 (백업 후 새 파일)
- 최대 3개 백업 유지
- 오래된 백업 자동 삭제

대상 로그:
- .claude/hook.log
- .claude-state/subagent.log
"""

import os
from pathlib import Path
from datetime import datetime


# 설정
MAX_LOG_SIZE_KB = 50  # 50KB 초과 시 로테이션
MAX_BACKUPS = 3       # 최대 백업 개수


def get_file_size_kb(file_path: Path) -> float:
    """파일 크기를 KB로 반환"""
    if file_path.exists():
        return file_path.stat().st_size / 1024
    return 0


def rotate_log(log_path: Path) -> str:
    """
    로그 파일 로테이션 수행

    Returns:
        로테이션 결과 메시지
    """
    if not log_path.exists():
        return ""

    size_kb = get_file_size_kb(log_path)
    if size_kb <= MAX_LOG_SIZE_KB:
        return ""

    # 백업 파일명 생성 (timestamp 포함)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{log_path.stem}_{timestamp}{log_path.suffix}"
    backup_path = log_path.parent / backup_name

    try:
        # 기존 로그 → 백업으로 이동
        log_path.rename(backup_path)

        # 새 빈 로그 파일 생성
        log_path.touch()

        # 오래된 백업 정리
        cleanup_old_backups(log_path)

        return f"  - {log_path.name}: {size_kb:.1f}KB → 로테이션 완료"
    except Exception as e:
        return f"  - {log_path.name}: 로테이션 실패 ({e})"


def cleanup_old_backups(log_path: Path):
    """
    오래된 백업 파일 정리 (MAX_BACKUPS 개수 유지)
    """
    parent_dir = log_path.parent
    stem = log_path.stem
    suffix = log_path.suffix

    # 해당 로그의 백업 파일들 찾기 (예: hook_20240125_143000.log)
    pattern = f"{stem}_*{suffix}"
    backups = sorted(parent_dir.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)

    # MAX_BACKUPS 초과분 삭제
    for old_backup in backups[MAX_BACKUPS:]:
        try:
            old_backup.unlink()
        except Exception:
            pass


def main():
    project_dir = Path(os.environ.get('CLAUDE_PROJECT_DIR', '.'))

    # 로테이션 대상 로그 파일들
    log_files = [
        project_dir / '.claude' / 'hook.log',
        project_dir / '.claude-state' / 'subagent.log',
    ]

    rotated_messages = []
    total_freed_kb = 0

    for log_path in log_files:
        if log_path.exists():
            before_size = get_file_size_kb(log_path)
            result = rotate_log(log_path)
            if result:
                rotated_messages.append(result)
                total_freed_kb += before_size

    # 로테이션이 발생한 경우에만 출력
    if rotated_messages:
        print(f"[Log Rotation] {total_freed_kb:.0f}KB 정리 완료")
        for msg in rotated_messages:
            print(msg)


if __name__ == "__main__":
    main()
