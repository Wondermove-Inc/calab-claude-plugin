#!/bin/bash
#
# sensitive-file-guard.sh - calab-claude-plugin 민감 파일 보호 훅
#
# 원더 무브 연구소 Claude Plug-in의 보안 훅.
# Edit|Write|MultiEdit 도구 사용 전 민감 파일 수정 시도를 차단합니다.
#
# 차단 대상:
#   - .env* (모든 환경 변수 파일)
#   - *credentials*, *secrets* (자격증명/비밀 파일)
#   - *.pem, *.key (인증서/키 파일)
#   - *password*, *token* (패스워드/토큰 파일)
#   - /.ssh/, /.aws/, /secrets/ 등 민감 디렉토리
#
# 원본: claude-monitoring-main
# 적용: calab-claude-plugin v2.3.0+
#

set -euo pipefail

# stdin에서 JSON 읽기
json_input=$(cat)

# jq 존재 확인
if ! command -v jq &> /dev/null; then
  exit 0
fi

# tool_input.file_path 추출
file_path=$(echo "$json_input" | jq -r '.tool_input.file_path // empty' 2>/dev/null)

# 파일 경로가 없으면 통과
if [[ -z "$file_path" ]]; then
  exit 0
fi

# 파일명만 추출 (소문자 변환)
filename=$(basename "$file_path" | tr '[:upper:]' '[:lower:]')

# 허용된 예외 파일 (소스 코드 파일)
ALLOWED_EXCEPTIONS=(
  'tokens.ts'        # metrics 토큰 서비스
  'tokens.test.ts'   # 토큰 테스트 파일
  '*-tokens.spec.ts' # E2E 토큰 테스트 파일
  'usage-tab-tokens.spec.ts' # Usage 토큰 탭 E2E 테스트
)

# 예외 파일 확인
for exception in "${ALLOWED_EXCEPTIONS[@]}"; do
  if [[ "$filename" == "$exception" ]]; then
    exit 0
  fi
done

# 민감 파일 패턴 정의
SENSITIVE_PATTERNS=(
  # 환경 변수 파일
  '.env'
  '.env.*'
  'env.local'
  'env.development'
  'env.production'
  'env.test'

  # 자격증명/비밀
  '*credentials*'
  '*secrets*'
  '*secret*'

  # 인증서/키
  '*.pem'
  '*.key'
  '*.p12'
  '*.pfx'
  '*.jks'

  # 패스워드/토큰
  '*password*'
  '*token*'
  '*apikey*'
  '*api_key*'
  '*api-key*'

  # AWS/GCP/Azure 자격증명
  'credentials'
  'config'  # AWS config
  '*.aws*'
  '*.gcp*'
  '*.azure*'

  # SSH 키
  'id_rsa*'
  'id_ed25519*'
  'id_ecdsa*'
  'authorized_keys'
  'known_hosts'

  # 기타 민감 파일
  '*.keystore'
  '*.truststore'
  'htpasswd'
  'shadow'
)

# 디렉토리 패턴 (경로에 포함되면 차단)
SENSITIVE_DIRS=(
  '/.ssh/'
  '/.aws/'
  '/.gcp/'
  '/.azure/'
  '/secrets/'
  '/credentials/'
  '/private/'
)

# 디렉토리 패턴 검사
for dir_pattern in "${SENSITIVE_DIRS[@]}"; do
  if [[ "$file_path" == *"$dir_pattern"* ]]; then
    cat << EOF >&2

🚨 [보안 경고] 민감 디렉토리 수정 차단됨

   파일: $file_path
   사유: 민감 디렉토리 ($dir_pattern) 내 파일입니다.

   이 파일은 보안상 Claude를 통한 수정이 차단됩니다.
   직접 편집기를 사용하여 수정하세요.

EOF
    exit 2
  fi
done

# 파일명 패턴 검사
for pattern in "${SENSITIVE_PATTERNS[@]}"; do
  # fnmatch 스타일 패턴 매칭
  if [[ "$filename" == $pattern ]]; then
    cat << EOF >&2

🚨 [보안 경고] 민감 파일 수정 차단됨

   파일: $file_path
   패턴: $pattern

   이 파일은 보안상 Claude를 통한 수정이 차단됩니다.
   허용된 작업:
   - 파일 읽기 (Read)
   - 내용 분석/설명

   차단된 작업:
   - 파일 쓰기/수정 (Write/Edit)

   직접 편집기를 사용하여 수정하세요.

EOF
    exit 2
  fi
done

# 통과
exit 0
