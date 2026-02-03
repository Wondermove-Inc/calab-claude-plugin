#!/bin/bash

# ============================================
# Claude Code Statusline 설치/삭제/업데이트 스크립트
# ============================================
# 사용법:
#   설치/업데이트: bash setup-statusline.sh install
#   삭제:          bash setup-statusline.sh uninstall
# ============================================

set -e

# 색상 정의
GREEN='\033[32m'
YELLOW='\033[33m'
CYAN='\033[36m'
RED='\033[31m'
RESET='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATUSLINE_SOURCE="$SCRIPT_DIR/statusline-command.sh"
STATUSLINE_DEST="$HOME/.claude/statusline-command.sh"
SETTINGS_FILE="$HOME/.claude/settings.json"

# 사전 요구사항 확인
check_requirements() {
    echo -e "${CYAN}[1/4]${RESET} 사전 요구사항 확인..."

    if ! command -v jq &> /dev/null; then
        echo -e "${YELLOW}  → jq 설치 중...${RESET}"
        if command -v apt &> /dev/null; then
            sudo apt install -y jq
        elif command -v brew &> /dev/null; then
            brew install jq
        else
            echo -e "${RED}  ✗ jq를 수동으로 설치하세요${RESET}"
            exit 1
        fi
    fi
    echo -e "${GREEN}  ✓ jq 설치됨${RESET}"
}

# 설치/업데이트
install_statusline() {
    echo "============================================"
    echo " Claude Code Statusline 설치/업데이트"
    echo "============================================"
    echo ""

    check_requirements

    # 디렉토리 생성
    echo -e "${CYAN}[2/4]${RESET} 디렉토리 생성..."
    mkdir -p ~/.claude
    echo -e "${GREEN}  ✓ ~/.claude 디렉토리 준비됨${RESET}"

    # Statusline 스크립트 복사
    echo -e "${CYAN}[3/4]${RESET} Statusline 스크립트 설치..."
    if [ -f "$STATUSLINE_SOURCE" ]; then
        cp "$STATUSLINE_SOURCE" "$STATUSLINE_DEST"
        chmod +x "$STATUSLINE_DEST"
        echo -e "${GREEN}  ✓ statusline-command.sh 설치됨${RESET}"
    else
        echo -e "${RED}  ✗ 소스 파일을 찾을 수 없음: $STATUSLINE_SOURCE${RESET}"
        exit 1
    fi

    # settings.json 업데이트
    echo -e "${CYAN}[4/4]${RESET} settings.json 업데이트..."

    if [ -f "$SETTINGS_FILE" ]; then
        tmp=$(mktemp)
        jq '.statusLine = {"type": "command", "command": "~/.claude/statusline-command.sh", "padding": 0}' "$SETTINGS_FILE" > "$tmp"
        mv "$tmp" "$SETTINGS_FILE"
        echo -e "${GREEN}  ✓ settings.json 업데이트됨${RESET}"
    else
        cat > "$SETTINGS_FILE" << 'EOF'
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline-command.sh",
    "padding": 0
  }
}
EOF
        echo -e "${GREEN}  ✓ settings.json 생성됨${RESET}"
    fi

    echo ""
    echo "============================================"
    echo -e "${GREEN} ✓ 설치 완료!${RESET}"
    echo "============================================"
    echo ""
    echo " Claude Code를 재시작하세요: claude"
    echo ""
}

# 삭제
uninstall_statusline() {
    echo "============================================"
    echo " Claude Code Statusline 삭제"
    echo "============================================"
    echo ""

    # Statusline 스크립트 삭제
    echo -e "${CYAN}[1/2]${RESET} Statusline 스크립트 삭제..."
    if [ -f "$STATUSLINE_DEST" ]; then
        rm "$STATUSLINE_DEST"
        echo -e "${GREEN}  ✓ statusline-command.sh 삭제됨${RESET}"
    else
        echo -e "${YELLOW}  → 이미 삭제됨${RESET}"
    fi

    # settings.json에서 statusLine 제거
    echo -e "${CYAN}[2/2]${RESET} settings.json 업데이트..."
    if [ -f "$SETTINGS_FILE" ]; then
        tmp=$(mktemp)
        jq 'del(.statusLine)' "$SETTINGS_FILE" > "$tmp"
        mv "$tmp" "$SETTINGS_FILE"
        echo -e "${GREEN}  ✓ statusLine 설정 제거됨${RESET}"
    else
        echo -e "${YELLOW}  → settings.json 없음${RESET}"
    fi

    echo ""
    echo "============================================"
    echo -e "${GREEN} ✓ 삭제 완료!${RESET}"
    echo "============================================"
    echo ""
    echo " Claude Code를 재시작하세요: claude"
    echo ""
}

# 사용법 출력
show_usage() {
    echo "사용법: $0 [install|uninstall]"
    echo ""
    echo "  install    Statusline 설치 또는 업데이트"
    echo "  uninstall  Statusline 삭제"
    echo ""
}

# 메인
case "${1:-install}" in
    install|update)
        install_statusline
        ;;
    uninstall|remove)
        uninstall_statusline
        ;;
    -h|--help|help)
        show_usage
        ;;
    *)
        echo -e "${RED}알 수 없는 명령: $1${RESET}"
        show_usage
        exit 1
        ;;
esac
