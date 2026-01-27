#!/usr/bin/env python3
"""
훅 공통 유틸리티 (Hook Utilities)

모든 훅에서 사용하는 공통 함수들을 제공합니다.

기능:
    - 에러 로깅
    - JSON 파일 로드/저장
    - 상태 디렉토리 관리
    - 파일 락 (동시 접근 보호)
    - 체크포인트 관리 (FIFO)
"""

import fcntl
import json
import os
import time
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 경로 설정
HOME = Path.home()
CWD = Path(os.getcwd())
STATE_DIR = CWD / ".claude-state"
ERROR_LOG_FILE = STATE_DIR / "hook_errors.log"
CHECKPOINT_FILE = STATE_DIR / "checkpoint.json"
CHECKPOINT_HISTORY_FILE = STATE_DIR / "checkpoint_history.json"

# 체크포인트 설정
MAX_CHECKPOINT_HISTORY = 10  # 구버전 히스토리 최대 개수
MAX_CHECKPOINT_SLOTS = 5     # 신버전 FIFO 슬롯 최대 개수


def ensure_state_dir() -> Path:
    """상태 디렉토리가 존재하는지 확인하고 생성합니다."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    return STATE_DIR


def log_error(hook_name: str, error: Exception, context: Optional[Dict] = None) -> None:
    """
    훅 에러를 로그 파일에 기록합니다.

    Args:
        hook_name: 에러가 발생한 훅 이름
        error: 발생한 예외 객체
        context: 추가 컨텍스트 정보 (선택)
    """
    ensure_state_dir()

    timestamp = datetime.now().isoformat()
    error_entry = f"[{timestamp}] {hook_name}: {error}"

    if context:
        context_str = json.dumps(context, ensure_ascii=False, default=str)
        error_entry += f" | context: {context_str}"

    error_entry += "\n"

    try:
        with open(ERROR_LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(error_entry)
    except IOError:
        # 로그 파일 쓰기 실패해도 훅 실행은 계속
        pass


def load_json_file(path: Path, default: Optional[Any] = None) -> Any:
    """
    JSON 파일을 로드합니다.

    Args:
        path: JSON 파일 경로
        default: 파일이 없거나 파싱 실패 시 반환할 기본값

    Returns:
        파싱된 JSON 데이터 또는 기본값
    """
    if default is None:
        default = {}

    if not path.exists():
        return default

    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return default


def save_json_file(path: Path, data: Any, indent: int = 2) -> bool:
    """
    데이터를 JSON 파일로 저장합니다.

    Args:
        path: 저장할 파일 경로
        data: 저장할 데이터
        indent: JSON 들여쓰기 (기본 2)

    Returns:
        저장 성공 여부
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        return True
    except IOError:
        return False


def get_timestamp() -> str:
    """현재 시간을 ISO 형식 문자열로 반환합니다."""
    return datetime.now().isoformat()


def get_today() -> str:
    """오늘 날짜를 YYYY-MM-DD 형식으로 반환합니다."""
    return datetime.now().strftime('%Y-%m-%d')


def get_time() -> str:
    """현재 시간을 HH:MM 형식으로 반환합니다."""
    return datetime.now().strftime('%H:%M')


@contextmanager
def file_lock(lock_path: Path, timeout: int = 5):
    """
    파일 락을 획득하여 동시 접근을 방지합니다.

    Args:
        lock_path: 락 파일 경로
        timeout: 락 획득 대기 시간 (초)

    Yields:
        락이 획득된 파일 객체
    """
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_file = open(lock_path, 'w')
    acquired = False

    try:
        # 즉시 획득 시도
        try:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            acquired = True
        except BlockingIOError:
            # 대기 후 재시도
            start = time.time()
            while time.time() - start < timeout:
                try:
                    fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    acquired = True
                    break
                except BlockingIOError:
                    time.sleep(0.1)

            if not acquired:
                raise TimeoutError(f"Failed to acquire lock: {lock_path}")

        yield lock_file
    finally:
        if acquired:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
        lock_file.close()


def format_time_ago(timestamp_str: str) -> str:
    """
    타임스탬프를 '몇 분/시간 전' 형식으로 변환합니다.

    Args:
        timestamp_str: ISO 형식 타임스탬프 문자열

    Returns:
        상대 시간 문자열 (예: "5분 전", "2시간 전")
    """
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


def save_checkpoint(
    data: Dict[str, Any],
    checkpoint_file: Optional[Path] = None,
    history_file: Optional[Path] = None,
    max_history: int = MAX_CHECKPOINT_HISTORY
) -> bool:
    """
    체크포인트를 저장하고 이전 체크포인트를 히스토리에 추가합니다.

    Args:
        data: 저장할 체크포인트 데이터
        checkpoint_file: 체크포인트 파일 경로 (기본: STATE_DIR/checkpoint.json)
        history_file: 히스토리 파일 경로 (기본: STATE_DIR/checkpoint_history.json)
        max_history: 유지할 최대 히스토리 수

    Returns:
        저장 성공 여부
    """
    checkpoint_file = checkpoint_file or CHECKPOINT_FILE
    history_file = history_file or CHECKPOINT_HISTORY_FILE

    ensure_state_dir()

    # 타임스탬프 자동 추가
    if 'timestamp' not in data:
        data['timestamp'] = get_timestamp()

    try:
        # 기존 체크포인트를 히스토리에 추가
        if checkpoint_file.exists():
            old_checkpoint = load_json_file(checkpoint_file)
            if old_checkpoint:
                history = load_json_file(history_file, default=[])
                history.append(old_checkpoint)
                history = history[-max_history:]
                save_json_file(history_file, history)

        # 새 체크포인트 저장
        return save_json_file(checkpoint_file, data)
    except Exception:
        return False


def load_checkpoint(checkpoint_file: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    """
    가장 최근 체크포인트를 로드합니다.

    Args:
        checkpoint_file: 체크포인트 파일 경로

    Returns:
        체크포인트 데이터 또는 None
    """
    checkpoint_file = checkpoint_file or CHECKPOINT_FILE
    data = load_json_file(checkpoint_file)
    return data if data else None


def get_checkpoint_history(
    history_file: Optional[Path] = None,
    limit: int = 5
) -> List[Dict[str, Any]]:
    """
    체크포인트 히스토리를 가져옵니다.

    Args:
        history_file: 히스토리 파일 경로
        limit: 반환할 최대 항목 수

    Returns:
        체크포인트 히스토리 리스트 (최신순)
    """
    history_file = history_file or CHECKPOINT_HISTORY_FILE
    history = load_json_file(history_file, default=[])
    return list(reversed(history[-limit:]))
