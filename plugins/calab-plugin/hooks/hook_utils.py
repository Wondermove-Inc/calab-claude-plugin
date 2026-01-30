#!/usr/bin/env python3
"""
hook_utils.py - calab-claude-plugin 훅 공통 유틸리티

원더 무브 연구소 Claude Plug-in의 훅 공통 유틸리티.
모든 훅 스크립트에서 공유하는 함수들을 제공합니다.

주요 기능:
  - 로깅 (시간 기록 포함)
  - JSON 파싱 및 검증
  - 체크포인트 파일 관리 (v4 FIFO 배열)
  - 파일 락 (동시 접근 방지)
  - 상대 시간 계산

원본: claude-monitoring-main
적용: calab-claude-plugin v2.3.0+
"""

import json
import os
import sys
import subprocess
import fcntl
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, Union
from functools import lru_cache

# 전역 설정
HOOK_NAME = "Unknown"
HOOK_LOG_FILE = "/tmp/hook.log"
PROJECT_ROOT = ""
CHECKPOINT_FILE = ""
CHECKPOINTS_FILE = ""
MAX_CHECKPOINTS = 5

# 성능 최적화: 캐싱
_cache = {
    "project_root": None,
    "git_info": None,
    "git_info_time": 0,
    "config": None,
}
CACHE_TTL = 5  # 캐시 TTL (초)


def setup_hook_config(hook_name: str) -> None:
    """훅 설정 초기화"""
    global HOOK_NAME, HOOK_LOG_FILE, PROJECT_ROOT, CHECKPOINT_FILE, CHECKPOINTS_FILE

    HOOK_NAME = hook_name

    # 프로젝트 루트 찾기
    PROJECT_ROOT = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())

    # 로그 파일 경로 (.claude 디렉토리 내)
    claude_dir = os.path.join(PROJECT_ROOT, ".claude")
    if os.path.isdir(claude_dir):
        HOOK_LOG_FILE = os.path.join(claude_dir, "hook.log")
    else:
        HOOK_LOG_FILE = "/tmp/hook.log"

    # 체크포인트 파일 경로
    CHECKPOINT_FILE = os.path.join(PROJECT_ROOT, ".claude", "checkpoint.json")
    CHECKPOINTS_FILE = os.path.join(PROJECT_ROOT, ".claude", "checkpoints.json")


def log(message: str) -> None:
    """로그 메시지 기록 (시간 포함)"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{HOOK_NAME}] {message}\n"

    try:
        with open(HOOK_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception:
        pass  # 로깅 실패 시 무시


def json_get(json_str: str, path: str, default: Any = None) -> Any:
    """JSON 문자열에서 값 추출 (jq 스타일 경로)"""
    try:
        data = json.loads(json_str)
        # 간단한 경로 파싱 (예: .field.subfield)
        keys = path.strip(".").split(".")
        result = data
        for key in keys:
            if key and isinstance(result, dict):
                result = result.get(key, default)
            else:
                return default
        return result if result is not None else default
    except (json.JSONDecodeError, TypeError):
        return default


def validate_json(json_str: str) -> bool:
    """JSON 문자열 유효성 검증"""
    try:
        json.loads(json_str)
        return True
    except (json.JSONDecodeError, TypeError):
        return False


def validate_checkpoint_file(filepath: str) -> bool:
    """체크포인트 파일 유효성 검증"""
    if not os.path.isfile(filepath):
        return False

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return isinstance(data, dict)
    except (json.JSONDecodeError, OSError):
        return False


def checkpoint_get(filepath: str, path: str, default: Any = None) -> Any:
    """체크포인트 파일에서 값 추출"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 간단한 경로 파싱
        keys = path.strip(".").split(".")
        result = data
        for key in keys:
            if key and isinstance(result, dict):
                result = result.get(key, default)
            else:
                return default
        return result if result is not None else default
    except (json.JSONDecodeError, OSError, TypeError):
        return default


def calculate_relative_time(timestamp_str: str) -> str:
    """ISO-8601 타임스탬프를 상대 시간으로 변환"""
    try:
        # ISO-8601 파싱
        if timestamp_str.endswith("Z"):
            timestamp_str = timestamp_str[:-1] + "+00:00"

        ts = datetime.fromisoformat(timestamp_str)
        now = datetime.now(timezone.utc)

        # 시간대 정보가 없는 경우 UTC로 가정
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)

        diff_seconds = int((now - ts).total_seconds())

        if diff_seconds < 0:
            return "방금 전"
        elif diff_seconds < 60:
            return f"{diff_seconds}초 전"
        elif diff_seconds < 3600:
            return f"{diff_seconds // 60}분 전"
        elif diff_seconds < 86400:
            return f"{diff_seconds // 3600}시간 전"
        else:
            return f"{diff_seconds // 86400}일 전"
    except (ValueError, TypeError):
        return "알 수 없음"


class FileLock:
    """파일 락 컨텍스트 매니저"""

    def __init__(self, filepath: str, timeout: int = 5):
        self.filepath = filepath + ".lock"
        self.timeout = timeout
        self.lock_file = None

    def __enter__(self):
        self.lock_file = open(self.filepath, "w")
        start_time = time.time()

        while True:
            try:
                fcntl.flock(self.lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return self
            except IOError:
                if time.time() - start_time >= self.timeout:
                    raise TimeoutError(f"파일 락 획득 실패: {self.filepath}")
                time.sleep(0.1)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.lock_file:
            fcntl.flock(self.lock_file.fileno(), fcntl.LOCK_UN)
            self.lock_file.close()
            try:
                os.remove(self.filepath)
            except OSError:
                pass


def get_checkpoint_count(filepath: str) -> int:
    """체크포인트 개수 반환"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return len(data.get("checkpoints", []))
    except (json.JSONDecodeError, OSError, KeyError):
        return 0


def get_latest_checkpoint(filepath: str) -> Optional[dict]:
    """가장 최근 체크포인트 반환"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        checkpoints = data.get("checkpoints", [])
        if checkpoints:
            return checkpoints[-1]
        return None
    except (json.JSONDecodeError, OSError, KeyError):
        return None


def add_checkpoint(entry: Union[dict, str], filepath: str) -> bool:
    """체크포인트 추가 (FIFO, 최대 MAX_CHECKPOINTS개)"""
    try:
        # 문자열이면 JSON 파싱
        if isinstance(entry, str):
            entry = json.loads(entry)

        # 기존 파일 읽기
        if os.path.isfile(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {"version": "4.0", "checkpoints": []}

        # 체크포인트 추가
        checkpoints = data.get("checkpoints", [])
        checkpoints.append(entry)

        # FIFO: 최대 개수 초과 시 오래된 것 삭제
        while len(checkpoints) > MAX_CHECKPOINTS:
            checkpoints.pop(0)

        data["checkpoints"] = checkpoints
        data["version"] = "4.0"

        # 파일 쓰기
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True
    except (json.JSONDecodeError, OSError, TypeError) as e:
        log(f"체크포인트 추가 실패: {e}")
        return False


def migrate_checkpoint_to_v4(old_file: str, new_file: str) -> bool:
    """v3 체크포인트를 v4로 마이그레이션"""
    try:
        with open(old_file, "r", encoding="utf-8") as f:
            old_data = json.load(f)

        # v3 형식인지 확인
        if old_data.get("version") == "3.0":
            entry = {
                "timestamp": old_data.get("timestamp", ""),
                "session_id": old_data.get("session_id", ""),
                "transcript_path": old_data.get("transcript_path", ""),
                "current_work": old_data.get("current_work"),
                "completed_phases": old_data.get("completed_phases", []),
                "plans_tree": old_data.get("plans_tree", ""),
                "summary": "마이그레이션됨"
            }

            return add_checkpoint(entry, new_file)

        return False
    except (json.JSONDecodeError, OSError) as e:
        log(f"마이그레이션 실패: {e}")
        return False


def get_git_info(cwd: str, use_cache: bool = True) -> tuple:
    """Git 브랜치 및 상태 정보 반환 (캐싱 지원)"""
    global _cache

    # 캐시 확인 (TTL 내)
    if use_cache and _cache["git_info"] is not None:
        if time.time() - _cache["git_info_time"] < CACHE_TTL:
            return _cache["git_info"]

    try:
        # Git 디렉토리 확인
        result = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            timeout=2  # 타임아웃 추가
        )
        if result.returncode != 0:
            return "", False

        # 브랜치 이름
        result = subprocess.run(
            ["git", "-C", cwd, "--no-optional-locks", "symbolic-ref", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=2
        )
        branch = result.stdout.strip() if result.returncode == 0 else "detached"

        # 변경 사항 확인
        result1 = subprocess.run(
            ["git", "-C", cwd, "--no-optional-locks", "diff", "--quiet"],
            capture_output=True,
            timeout=2
        )
        result2 = subprocess.run(
            ["git", "-C", cwd, "--no-optional-locks", "diff", "--cached", "--quiet"],
            capture_output=True,
            timeout=2
        )
        has_changes = result1.returncode != 0 or result2.returncode != 0

        # 캐시 저장
        _cache["git_info"] = (branch, has_changes)
        _cache["git_info_time"] = time.time()

        return branch, has_changes
    except (subprocess.SubprocessError, OSError, subprocess.TimeoutExpired):
        return "", False


@lru_cache(maxsize=32)
def get_project_root_cached() -> str:
    """프로젝트 루트 캐싱 (불변 값)"""
    return os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())


def fast_json_parse(json_str: str) -> Optional[dict]:
    """빠른 JSON 파싱 (에러 시 None 반환)"""
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return None


if __name__ == "__main__":
    # 테스트용
    setup_hook_config("Test")
    log("hook_utils.py 테스트 완료")
    print("hook_utils.py 로드 성공")
