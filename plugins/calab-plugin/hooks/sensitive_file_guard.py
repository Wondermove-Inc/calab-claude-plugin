#!/usr/bin/env python3
"""
sensitive_file_guard.py - calab-claude-plugin 민감 파일 보호 훅

원더 무브 연구소 Claude Plug-in의 보안 훅.
Edit|Write|MultiEdit 도구 사용 전 민감 파일 수정 시도를 차단합니다.

차단 대상:
  - .env* (모든 환경 변수 파일)
  - *credentials*, *secrets* (자격증명/비밀 파일)
  - *.pem, *.key (인증서/키 파일)
  - *password*, *token* (패스워드/토큰 파일)
  - /.ssh/, /.aws/, /secrets/ 등 민감 디렉토리

원본: claude-monitoring-main
적용: calab-claude-plugin v2.3.0+
"""

import json
import sys
import os
import fnmatch

# hook_utils에서 유틸리티 임포트
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hook_utils import setup_hook_config, log

# 허용된 예외 파일 (소스 코드 파일)
ALLOWED_EXCEPTIONS = [
    'tokens.ts',           # metrics 토큰 서비스
    'tokens.test.ts',      # 토큰 테스트 파일
    '*-tokens.spec.ts',    # E2E 토큰 테스트 파일
    'usage-tab-tokens.spec.ts',  # Usage 토큰 탭 E2E 테스트
    'secret.yaml',         # 프로젝트 설정 파일
    '.env',                # 환경 변수 파일
    '.env.example',        # 환경 변수 예시 파일
]

# 민감 파일 패턴 정의
SENSITIVE_PATTERNS = [
    # 환경 변수 파일
    '.env',
    '.env.*',
    'env.local',
    'env.development',
    'env.production',
    'env.test',

    # 자격증명/비밀
    '*credentials*',
    '*secrets*',
    '*secret*',

    # 인증서/키
    '*.pem',
    '*.key',
    '*.p12',
    '*.pfx',
    '*.jks',

    # 패스워드/토큰
    '*password*',
    '*token*',
    '*apikey*',
    '*api_key*',
    '*api-key*',

    # AWS/GCP/Azure 자격증명
    'credentials',
    'config',  # AWS config
    '*.aws*',
    '*.gcp*',
    '*.azure*',

    # SSH 키
    'id_rsa*',
    'id_ed25519*',
    'id_ecdsa*',
    'authorized_keys',
    'known_hosts',

    # 기타 민감 파일
    '*.keystore',
    '*.truststore',
    'htpasswd',
    'shadow',
]

# 디렉토리 패턴 (경로에 포함되면 차단)
SENSITIVE_DIRS = [
    '/.ssh/',
    '/.aws/',
    '/.gcp/',
    '/.azure/',
    '/secrets/',
    '/credentials/',
    '/private/',
]


def match_pattern(filename: str, pattern: str) -> bool:
    """fnmatch 스타일 패턴 매칭"""
    return fnmatch.fnmatch(filename, pattern)


def check_sensitive_file(file_path: str) -> tuple:
    """
    민감 파일 여부 확인
    Returns: (is_sensitive, reason)
    """
    if not file_path:
        return False, None

    # 파일명 추출 (소문자 변환)
    filename = os.path.basename(file_path).lower()

    # 허용된 예외 파일 확인
    for exception in ALLOWED_EXCEPTIONS:
        if match_pattern(filename, exception):
            return False, None

    # 디렉토리 패턴 검사
    file_path_lower = file_path.lower()
    for dir_pattern in SENSITIVE_DIRS:
        if dir_pattern in file_path_lower:
            return True, f"민감 디렉토리 ({dir_pattern})"

    # 파일명 패턴 검사
    for pattern in SENSITIVE_PATTERNS:
        if match_pattern(filename, pattern):
            return True, f"민감 파일 패턴 ({pattern})"

    return False, None


def main():
    setup_hook_config("SensitiveFileGuard")

    # stdin에서 JSON 읽기
    try:
        json_input = sys.stdin.read()
        data = json.loads(json_input)
    except (json.JSONDecodeError, ValueError):
        log("JSON 파싱 실패 - 통과")
        sys.exit(0)

    # tool_input.file_path 추출
    file_path = data.get('tool_input', {}).get('file_path', '')

    # 파일 경로가 없으면 통과
    if not file_path:
        log("파일 경로 없음 - 통과")
        sys.exit(0)

    log(f"파일 검사: {file_path}")

    # 민감 파일 확인
    is_sensitive, reason = check_sensitive_file(file_path)

    if is_sensitive:
        log(f"차단: {reason}")
        # 경고 메시지 출력
        error_message = f"""
🚨 [보안 경고] 민감 파일 수정 차단됨

   파일: {file_path}
   사유: {reason}

   이 파일은 보안상 Claude를 통한 수정이 차단됩니다.
   허용된 작업:
   - 파일 읽기 (Read)
   - 내용 분석/설명

   차단된 작업:
   - 파일 쓰기/수정 (Write/Edit)

   직접 편집기를 사용하여 수정하세요.

"""
        print(error_message, file=sys.stderr)
        sys.exit(2)  # 차단

    log("통과")
    sys.exit(0)


if __name__ == "__main__":
    main()
