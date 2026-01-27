#!/usr/bin/env python3
"""
PreToolUse Hook: 민감 파일 보호

Edit 또는 Write 도구 사용 전 민감 파일 수정 시도를 차단합니다.

보호 대상:
- .env, .env.* (환경변수 파일)
- *.pem, *.key, *.p12 (인증서/키 파일)
- credentials*, secrets* (인증 정보)
- *_rsa, *_dsa, *_ecdsa, *_ed25519 (SSH 키)
- .npmrc, .pypirc (패키지 관리자 인증)
- .netrc, .htpasswd (네트워크/웹 인증)
- kubeconfig, *-kubeconfig* (Kubernetes 설정)
"""

import json
import sys
from fnmatch import fnmatch
from pathlib import Path
from typing import List, Tuple


# 민감 파일 패턴 정의
SENSITIVE_PATTERNS = [
    # 환경변수 파일
    '.env',
    '.env.*',
    '*.env',

    # 인증서 및 키 파일
    '*.pem',
    '*.key',
    '*.p12',
    '*.pfx',
    '*.jks',
    '*.keystore',

    # 인증 정보 파일
    'credentials',
    'credentials.*',
    '*credentials*',
    'secrets',
    'secrets.*',
    '*secrets*',

    # SSH 키
    'id_rsa',
    'id_dsa',
    'id_ecdsa',
    'id_ed25519',
    '*_rsa',
    '*_dsa',
    '*_ecdsa',
    '*_ed25519',
    '*.pub',  # 공개키도 보호 (변조 방지)

    # 패키지 관리자 인증
    '.npmrc',
    '.pypirc',
    '.yarnrc',
    '.gem/credentials',

    # 네트워크/웹 인증
    '.netrc',
    '.htpasswd',
    '.htaccess',

    # Kubernetes
    'kubeconfig',
    '*-kubeconfig*',
    '*.kubeconfig',

    # 클라우드 설정
    '.aws/credentials',
    '.gcloud/*credentials*',
    'service-account*.json',

    # 데이터베이스
    '*.sqlite',
    '*.db',

    # 기타 민감 파일
    '.git-credentials',
    '.docker/config.json',
    'token',
    'token.*',
    '*token*.json',
    'api_key*',
    'apikey*',
]

# 항상 허용하는 패턴 (예외)
ALLOWED_PATTERNS = [
    '*.env.example',
    '*.env.sample',
    '*.env.template',
    '.env.example',
    '.env.sample',
    '.env.template',
    'credentials.example',
    'secrets.example',
]


def matches_pattern(filename: str, patterns: List[str]) -> bool:
    """파일명이 패턴 목록 중 하나와 일치하는지 확인합니다."""
    filename_lower = filename.lower()
    for pattern in patterns:
        if fnmatch(filename_lower, pattern.lower()):
            return True
    return False


def is_sensitive_file(file_path: str) -> Tuple[bool, str]:
    """
    파일이 민감 파일인지 확인합니다.

    Returns:
        (is_sensitive, matched_pattern): 민감 파일 여부와 매칭된 패턴
    """
    path = Path(file_path)
    filename = path.name

    # 허용 패턴 먼저 확인
    if matches_pattern(filename, ALLOWED_PATTERNS):
        return False, ''

    # 민감 패턴 확인 (파일명)
    for pattern in SENSITIVE_PATTERNS:
        if fnmatch(filename.lower(), pattern.lower()):
            return True, pattern

    # 경로 전체에서 패턴 확인
    full_path = str(path).lower()
    for pattern in SENSITIVE_PATTERNS:
        # 경로 구성요소로 확인
        if '/' in pattern:
            if fnmatch(full_path, f'*{pattern.lower()}*'):
                return True, pattern

    return False, ''


def main():
    """메인 함수: 민감 파일 수정 시도를 차단합니다."""
    # stdin에서 도구 사용 정보 읽기
    try:
        input_data = json.load(sys.stdin)
    except Exception:
        return

    tool_name = input_data.get('tool_name', '')
    tool_input = input_data.get('tool_input', {})

    # Edit 또는 Write 도구만 검사
    if tool_name not in ('Edit', 'Write'):
        return

    file_path = tool_input.get('file_path', '')
    if not file_path:
        return

    # 민감 파일 확인
    is_sensitive, matched_pattern = is_sensitive_file(file_path)

    if is_sensitive:
        filename = Path(file_path).name

        # 차단 메시지 출력
        result = {
            'decision': 'block',
            'reason': f"보안: 민감 파일 '{filename}' 수정이 차단되었습니다 (패턴: {matched_pattern})"
        }
        print(json.dumps(result))

        # stderr로 상세 안내 출력
        print(f"\n[Sensitive File Guard] 🔒 민감 파일 수정 차단", file=sys.stderr)
        print(f"  파일: {file_path}", file=sys.stderr)
        print(f"  패턴: {matched_pattern}", file=sys.stderr)
        print(f"  사유: .env, 인증서, 키 파일 등 민감 파일은 자동 수정이 금지됩니다.", file=sys.stderr)
        print(f"  해결: 필요시 수동으로 파일을 편집하세요.", file=sys.stderr)


if __name__ == "__main__":
    main()
