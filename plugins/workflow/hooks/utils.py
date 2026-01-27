#!/usr/bin/env python3
"""
훅 공통 유틸리티 (Hook Utilities)

모든 훅에서 사용하는 공통 함수들을 제공합니다.

기능:
    - 에러 로깅
    - JSON 파일 로드/저장
    - 상태 디렉토리 관리
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

# 경로 설정
HOME = Path.home()
CWD = Path(os.getcwd())
STATE_DIR = CWD / ".claude-state"
ERROR_LOG_FILE = STATE_DIR / "hook_errors.log"


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
