#!/bin/bash

# ============================================
# Beads (bd) 설치/삭제 스크립트
# ============================================
# macOS 전용 (Homebrew 사용)
#
# 사용법:
#   설치: bash setup-beads.sh install
#   삭제: bash setup-beads.sh uninstall
# ============================================

set -e

# 색상 정의
GREEN='\033[32m'
YELLOW='\033[33m'
CYAN='\033[36m'
RED='\033[31m'
RESET='\033[0m'

# macOS 확인
check_macos() {
    if [[ "$(uname)" != "Darwin" ]]; then
        echo -e "${RED}✗ 이 스크립트는 macOS에서만 지원됩니다.${RESET}"
        exit 1
    fi
}

# Homebrew 확인
check_homebrew() {
    if ! command -v brew &> /dev/null; then
        echo -e "${RED}✗ Homebrew가 설치되어 있지 않습니다.${RESET}"
        echo ""
        echo "  Homebrew 설치:"
        echo '  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        echo ""
        exit 1
    fi
}

# 설치
install_beads() {
    echo "============================================"
    echo " Beads (bd) 설치"
    echo "============================================"
    echo ""

    check_macos
    check_homebrew

    # tap 추가
    echo -e "${CYAN}[1/2]${RESET} Homebrew tap 추가..."
    if brew tap | grep -q "steveyegge/beads"; then
        echo -e "${YELLOW}  → 이미 tap이 추가되어 있음${RESET}"
    else
        brew tap steveyegge/beads
        echo -e "${GREEN}  ✓ tap 추가됨${RESET}"
    fi

    # bd 설치
    echo -e "${CYAN}[2/2]${RESET} bd 설치..."
    if command -v bd &> /dev/null; then
        echo -e "${YELLOW}  → 이미 설치됨, 업그레이드 시도...${RESET}"
        brew upgrade bd 2>/dev/null || echo -e "${GREEN}  ✓ 최신 버전임${RESET}"
    else
        brew install bd
        echo -e "${GREEN}  ✓ bd 설치됨${RESET}"
    fi

    echo ""
    echo "============================================"
    echo -e "${GREEN} ✓ 설치 완료!${RESET}"
    echo "============================================"
    echo ""
    echo " 버전 확인: bd --version"
    echo " 도움말:    bd --help"
    echo ""
}

# 삭제
uninstall_beads() {
    echo "============================================"
    echo " Beads (bd) 삭제"
    echo "============================================"
    echo ""

    check_macos
    check_homebrew

    # bd 삭제
    echo -e "${CYAN}[1/2]${RESET} bd 삭제..."
    if command -v bd &> /dev/null; then
        brew uninstall bd
        echo -e "${GREEN}  ✓ bd 삭제됨${RESET}"
    else
        echo -e "${YELLOW}  → 이미 삭제됨${RESET}"
    fi

    # tap 제거 (선택적)
    echo -e "${CYAN}[2/2]${RESET} Homebrew tap 제거..."
    if brew tap | grep -q "steveyegge/beads"; then
        brew untap steveyegge/beads
        echo -e "${GREEN}  ✓ tap 제거됨${RESET}"
    else
        echo -e "${YELLOW}  → tap이 없음${RESET}"
    fi

    echo ""
    echo "============================================"
    echo -e "${GREEN} ✓ 삭제 완료!${RESET}"
    echo "============================================"
    echo ""
}

# 사용법 출력
show_usage() {
    echo "사용법: $0 [install|uninstall]"
    echo ""
    echo "  install    Beads(bd) 설치 또는 업그레이드"
    echo "  uninstall  Beads(bd) 삭제"
    echo ""
    echo "※ macOS 전용 (Homebrew 필요)"
    echo ""
}

# 메인
case "${1:-install}" in
    install|update|upgrade)
        install_beads
        ;;
    uninstall|remove)
        uninstall_beads
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
