#!/bin/bash
# ============================================================
# Calab Claude Plugin - 완전 삭제 스크립트
# ============================================================
# 사용법: ./uninstall.sh [--keep-settings]
# ============================================================

set -e

# 버전 및 경로 설정
PLUGIN_NAME="calab-plugin"
CLAUDE_HOME="$HOME/.claude"
MARKETPLACE_DIR="$CLAUDE_HOME/calab-marketplace"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# 옵션 파싱
KEEP_SETTINGS=false
for arg in "$@"; do
    case $arg in
        --keep-settings)
            KEEP_SETTINGS=true
            shift
            ;;
    esac
done

# 로깅 함수
info() { echo -e "${BLUE}ℹ${NC} $1"; }
success() { echo -e "${GREEN}✓${NC} $1"; }
warning() { echo -e "${YELLOW}⚠${NC} $1"; }
error() { echo -e "${RED}✗${NC} $1"; }
step() { echo -e "\n${CYAN}${BOLD}[$1]${NC} $2"; }

# 배너 출력
show_banner() {
    echo ""
    echo -e "${RED}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║${NC}     ${BOLD}Calab Claude Plugin - 완전 삭제${NC}                         ${RED}║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# 삭제 확인
confirm_uninstall() {
    echo -e "${YELLOW}${BOLD}⚠ 경고: 다음 항목이 삭제됩니다:${NC}"
    echo ""
    echo "  • 마켓플레이스: $MARKETPLACE_DIR"
    echo "  • 글로벌 파일: $CLAUDE_HOME/{CLAUDE.md,hooks,scripts,...}"

    if [ "$KEEP_SETTINGS" = false ]; then
        echo "  • 설정 파일: $CLAUDE_HOME/settings.json"
    else
        echo -e "  • 설정 파일: ${GREEN}유지됨 (--keep-settings)${NC}"
    fi

    echo ""
    read -p "계속하시겠습니까? (y/N): " -n 1 -r
    echo ""

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        info "삭제가 취소되었습니다."
        exit 0
    fi
}

# 플러그인 캐시 삭제
remove_plugin_cache() {
    step "1/4" "플러그인 캐시 삭제"

    # 플러그인 캐시 디렉토리 삭제
    if [ -d "$CLAUDE_HOME/plugins/cache/calab-marketplace" ]; then
        rm -rf "$CLAUDE_HOME/plugins/cache/calab-marketplace"
        success "플러그인 캐시 디렉토리 삭제됨"
    else
        info "플러그인 캐시 디렉토리 없음"
    fi

    # installed_plugins.json에서 제거 (우리 플러그인만!)
    local installed_file="$CLAUDE_HOME/plugins/installed_plugins.json"
    if [ -f "$installed_file" ]; then
        if command -v jq &> /dev/null; then
            local tmp=$(mktemp)
            # JSON 구조: {"version": 2, "plugins": {"calab-plugin@calab-marketplace": [...]}}
            if jq 'del(.plugins["calab-plugin@calab-marketplace"])' "$installed_file" > "$tmp" 2>/dev/null; then
                mv "$tmp" "$installed_file"
                success "installed_plugins.json에서 calab-plugin 제거됨"
            else
                rm -f "$tmp"
                warning "jq 처리 실패 - 파일 유지 (다른 플러그인 보호)"
                info "수동으로 calab-plugin@calab-marketplace 항목을 제거하세요"
            fi
        else
            warning "jq가 없음 - 파일 유지 (다른 플러그인 보호)"
            info "수동으로 calab-plugin@calab-marketplace 항목을 제거하세요"
        fi
    fi

    # known_marketplaces.json에서 제거 (calab-marketplace만!)
    local marketplaces_file="$CLAUDE_HOME/plugins/known_marketplaces.json"
    if [ -f "$marketplaces_file" ]; then
        if command -v jq &> /dev/null; then
            local tmp=$(mktemp)
            # JSON 구조: {"calab-marketplace": {...}}
            if jq 'del(.["calab-marketplace"])' "$marketplaces_file" > "$tmp" 2>/dev/null; then
                mv "$tmp" "$marketplaces_file"
                success "known_marketplaces.json에서 calab-marketplace 제거됨"
            else
                rm -f "$tmp"
                warning "jq 처리 실패 - 파일 유지 (다른 마켓플레이스 보호)"
                info "수동으로 calab-marketplace 항목을 제거하세요"
            fi
        else
            warning "jq가 없음 - 파일 유지 (다른 마켓플레이스 보호)"
            info "수동으로 calab-marketplace 항목을 제거하세요"
        fi
    fi
}

# 마켓플레이스 삭제
remove_marketplace() {
    step "2/4" "마켓플레이스 삭제"

    if [ -d "$MARKETPLACE_DIR" ]; then
        rm -rf "$MARKETPLACE_DIR"
        success "마켓플레이스 삭제됨: $MARKETPLACE_DIR"
    else
        info "마켓플레이스 없음"
    fi
}

# 글로벌 파일 삭제
remove_global_files() {
    step "3/4" "글로벌 파일 삭제"

    local items=(
        "CLAUDE.md"
        "hooks"
        "scripts"
        "best-practices"
        "templates"
        "agents"
        "integrations"
        "memory"
        "problem-solving"
        "project-context"
        "rules"
    )

    local removed=0

    for item in "${items[@]}"; do
        if [ -e "$CLAUDE_HOME/$item" ]; then
            rm -rf "$CLAUDE_HOME/$item"
            success "$item 삭제됨"
            removed=$((removed + 1))
        fi
    done

    if [ $removed -eq 0 ]; then
        info "삭제할 글로벌 파일 없음"
    else
        success "글로벌 파일 $removed개 삭제됨"
    fi
}

# 설정 파일 삭제
remove_settings() {
    step "4/4" "설정 파일 처리"

    if [ "$KEEP_SETTINGS" = true ]; then
        info "설정 파일 유지됨 (--keep-settings)"
        return
    fi

    if [ -f "$CLAUDE_HOME/settings.json" ]; then
        # 백업 생성
        cp "$CLAUDE_HOME/settings.json" "$CLAUDE_HOME/settings.json.bak"
        info "백업 생성됨: $CLAUDE_HOME/settings.json.bak"

        rm "$CLAUDE_HOME/settings.json"
        success "settings.json 삭제됨"
    else
        info "settings.json 없음"
    fi
}

# 삭제 검증
verify_removal() {
    echo ""
    echo -e "${CYAN}${BOLD}[검증]${NC} 삭제 상태 확인"
    echo ""

    local remaining=0

    # 마켓플레이스 확인
    if [ -d "$MARKETPLACE_DIR" ]; then
        echo -e "  ${RED}✗${NC} 마켓플레이스 - 남아있음"
        remaining=$((remaining + 1))
    else
        echo -e "  ${GREEN}✓${NC} 마켓플레이스 - 삭제됨"
    fi

    # 주요 파일 확인
    local check_items=("CLAUDE.md" "hooks" "scripts")
    for item in "${check_items[@]}"; do
        if [ -e "$CLAUDE_HOME/$item" ]; then
            echo -e "  ${RED}✗${NC} $item - 남아있음"
            remaining=$((remaining + 1))
        else
            echo -e "  ${GREEN}✓${NC} $item - 삭제됨"
        fi
    done

    echo ""
    if [ $remaining -eq 0 ]; then
        success "모든 항목이 정상적으로 삭제되었습니다."
        return 0
    else
        warning "$remaining개 항목이 남아있습니다."
        return 1
    fi
}

# 완료 메시지
show_completion() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║${NC}                    ${BOLD}✨ 삭제 완료!${NC}                           ${GREEN}║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    if [ "$KEEP_SETTINGS" = true ]; then
        echo -e "${BOLD}💡 참고:${NC}"
        echo "  settings.json이 유지되었습니다."
        echo "  완전 삭제하려면 --keep-settings 없이 다시 실행하세요."
        echo ""
    fi

    echo -e "${BOLD}🔄 재설치하려면:${NC}"
    echo "  ./install.sh"
    echo ""
}

# 메인 실행
main() {
    show_banner
    confirm_uninstall
    remove_plugin_cache
    remove_marketplace
    remove_global_files
    remove_settings
    verify_removal
    show_completion
}

main "$@"
