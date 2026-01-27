#!/bin/bash
# ============================================================
# Calab Claude Plugin - 원클릭 설치 스크립트
# ============================================================
# 사용법: ./install.sh
# ============================================================

set -e

# 버전 및 경로 설정
PLUGIN_VERSION="2.3.1"
PLUGIN_NAME="calab-plugin"
PLUGIN_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_HOME="$HOME/.claude"
MARKETPLACE_DIR="$CLAUDE_HOME/calab-marketplace"
LOG_FILE="$PLUGIN_DIR/install.log"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# 로깅 함수
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"; }
info() { echo -e "${BLUE}ℹ${NC} $1"; log "INFO: $1"; }
success() { echo -e "${GREEN}✓${NC} $1"; log "SUCCESS: $1"; }
warning() { echo -e "${YELLOW}⚠${NC} $1"; log "WARNING: $1"; }
error() { echo -e "${RED}✗${NC} $1"; log "ERROR: $1"; }
step() { echo -e "\n${CYAN}${BOLD}[$1]${NC} $2"; log "STEP $1: $2"; }

# 진행 바 표시
show_progress() {
    local current=$1
    local total=$2
    local width=30
    local percent=$((current * 100 / total))
    local filled=$((current * width / total))
    local empty=$((width - filled))
    printf "\r  ["
    printf "%${filled}s" | tr ' ' '█'
    printf "%${empty}s" | tr ' ' '░'
    printf "] %3d%%" $percent
}

# 배너 출력
show_banner() {
    echo ""
    echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}     ${BOLD}Calab Claude Plugin - 원클릭 설치${NC}                       ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}     버전: ${GREEN}v$PLUGIN_VERSION${NC}                                         ${CYAN}║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# 환경 검증
check_environment() {
    step "1/5" "환경 검증"

    local errors=0

    # Python3 확인
    if command -v python3 &> /dev/null; then
        success "Python3 설치됨: $(python3 --version 2>&1 | cut -d' ' -f2)"
    else
        error "Python3가 필요합니다"
        errors=$((errors + 1))
    fi

    # Git 확인
    if command -v git &> /dev/null; then
        success "Git 설치됨"
    else
        warning "Git이 없습니다 (일부 기능 제한)"
    fi

    # plugin.json 확인
    if [ -f "$PLUGIN_DIR/.claude-plugin/plugin.json" ]; then
        success "플러그인 파일 확인됨"
    else
        error "plugin.json을 찾을 수 없습니다"
        errors=$((errors + 1))
    fi

    if [ $errors -gt 0 ]; then
        error "환경 검증 실패 ($errors개 오류)"
        exit 1
    fi

    success "환경 검증 완료"
}

# 이전 설치 정리
clean_previous() {
    step "2/5" "이전 설치 정리"

    # 캐시 정리
    if [ -d "$CLAUDE_HOME/plugins/cache/calab-marketplace" ]; then
        rm -rf "$CLAUDE_HOME/plugins/cache/calab-marketplace"
        success "이전 캐시 삭제됨"
    fi

    # installed_plugins.json에서 제거
    local installed_file="$CLAUDE_HOME/plugins/installed_plugins.json"
    if [ -f "$installed_file" ]; then
        if command -v jq &> /dev/null; then
            local tmp=$(mktemp)
            # JSON 구조: {"version": 2, "plugins": {"calab-plugin@calab-marketplace": [...]}}
            jq 'del(.plugins["calab-plugin@calab-marketplace"])' "$installed_file" > "$tmp" 2>/dev/null && \
            mv "$tmp" "$installed_file" || rm -f "$tmp"
        else
            rm -f "$installed_file"
        fi
    fi

    # known_marketplaces.json에서 제거
    local marketplaces_file="$CLAUDE_HOME/plugins/known_marketplaces.json"
    if [ -f "$marketplaces_file" ]; then
        if command -v jq &> /dev/null; then
            local tmp=$(mktemp)
            # JSON 구조: {"calab-marketplace": {...}}
            jq 'del(.["calab-marketplace"])' "$marketplaces_file" > "$tmp" 2>/dev/null && \
            mv "$tmp" "$marketplaces_file" || rm -f "$tmp"
        else
            rm -f "$marketplaces_file"
        fi
    fi

    # 이전 마켓플레이스 삭제
    if [ -d "$MARKETPLACE_DIR" ]; then
        rm -rf "$MARKETPLACE_DIR"
        success "이전 마켓플레이스 삭제됨"
    fi

    success "정리 완료"
}

# 글로벌 파일 설치
install_global_files() {
    step "3/5" "글로벌 파일 설치"

    mkdir -p "$CLAUDE_HOME"

    local items=(
        "CLAUDE.md:CLAUDE.md"
        ".claude/hooks:hooks"
        ".claude/best-practices:best-practices"
        ".claude/templates:templates"
        ".claude/agents:agents"
        ".claude/integrations:integrations"
        ".claude/memory:memory"
        ".claude/problem-solving:problem-solving"
        ".claude/project-context:project-context"
        ".claude/rules:rules"
        ".claude/scripts:scripts"
    )

    local total=${#items[@]}
    local current=0

    for item in "${items[@]}"; do
        local src="${item%%:*}"
        local dst="${item##*:}"

        if [ -e "$PLUGIN_DIR/$src" ]; then
            if [ -d "$PLUGIN_DIR/$src" ]; then
                mkdir -p "$CLAUDE_HOME/$dst"
                cp -r "$PLUGIN_DIR/$src/"* "$CLAUDE_HOME/$dst/" 2>/dev/null || true
            else
                cp "$PLUGIN_DIR/$src" "$CLAUDE_HOME/$dst"
            fi
        fi

        current=$((current + 1))
        show_progress $current $total
    done

    # 실행 권한 설정
    chmod +x "$CLAUDE_HOME/scripts/"*.py 2>/dev/null || true
    chmod +x "$CLAUDE_HOME/scripts/"*.sh 2>/dev/null || true
    chmod +x "$CLAUDE_HOME/hooks/"*.py 2>/dev/null || true

    echo ""
    success "글로벌 파일 설치 완료 ($total개 항목)"
}

# settings.json 설치
install_settings() {
    step "4/5" "설정 파일 설치"

    if [ -f "$PLUGIN_DIR/.claude/settings.json" ]; then
        # 훅 경로를 글로벌 경로로 변환
        sed 's|\${CLAUDE_PROJECT_DIR}/\.claude/hooks/|'"$CLAUDE_HOME"'/hooks/|g' \
            "$PLUGIN_DIR/.claude/settings.json" > "$CLAUDE_HOME/settings.json"
        success "settings.json 설치됨 (훅 경로 수정됨)"
    else
        warning "settings.json이 없습니다"
    fi
}

# 마켓플레이스 생성
create_marketplace() {
    step "5/5" "마켓플레이스 생성"

    mkdir -p "$MARKETPLACE_DIR/.claude-plugin"
    mkdir -p "$MARKETPLACE_DIR/plugins/$PLUGIN_NAME"

    # 플러그인 파일 복사 (.claude-plugin 안에 commands, skills 포함)
    [ -d "$PLUGIN_DIR/.claude-plugin" ] && cp -r "$PLUGIN_DIR/.claude-plugin" "$MARKETPLACE_DIR/plugins/$PLUGIN_NAME/"

    # marketplace.json 생성
    cat > "$MARKETPLACE_DIR/.claude-plugin/marketplace.json" <<EOF
{
  "\$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "calab-marketplace",
  "description": "Calab Plugin Marketplace - 개발 워크플로우 자동화",
  "owner": {
    "name": "Wondermove CALAB",
    "email": "captain@wondermove.net"
  },
  "plugins": [
    {
      "name": "$PLUGIN_NAME",
      "description": "개발 워크플로우 자동화 플러그인",
      "version": "$PLUGIN_VERSION",
      "source": "./plugins/$PLUGIN_NAME",
      "category": "development"
    }
  ]
}
EOF

    success "마켓플레이스 생성 완료"
}

# 설치 검증
verify_installation() {
    echo ""
    echo -e "${CYAN}${BOLD}[검증]${NC} 설치 상태 확인"
    echo ""

    local passed=0
    local failed=0

    # 필수 파일 확인
    local files=(
        "$CLAUDE_HOME/CLAUDE.md"
        "$CLAUDE_HOME/settings.json"
        "$CLAUDE_HOME/scripts/statusline_command.py"
        "$MARKETPLACE_DIR/.claude-plugin/marketplace.json"
        "$MARKETPLACE_DIR/plugins/$PLUGIN_NAME/.claude-plugin/plugin.json"
    )

    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            echo -e "  ${GREEN}✓${NC} $(basename "$file")"
            passed=$((passed + 1))
        else
            echo -e "  ${RED}✗${NC} $(basename "$file") - 없음"
            failed=$((failed + 1))
        fi
    done

    # 디렉토리 확인
    local dirs=(
        "$CLAUDE_HOME/hooks"
        "$CLAUDE_HOME/best-practices"
        "$MARKETPLACE_DIR/plugins/$PLUGIN_NAME/.claude-plugin/commands"
        "$MARKETPLACE_DIR/plugins/$PLUGIN_NAME/.claude-plugin/skills"
    )

    for dir in "${dirs[@]}"; do
        if [ -d "$dir" ]; then
            local count=$(ls -1 "$dir" 2>/dev/null | wc -l)
            echo -e "  ${GREEN}✓${NC} $(basename "$dir")/ ($count개 파일)"
            passed=$((passed + 1))
        else
            echo -e "  ${RED}✗${NC} $(basename "$dir")/ - 없음"
            failed=$((failed + 1))
        fi
    done

    echo ""
    if [ $failed -eq 0 ]; then
        success "모든 검증 통과 ($passed개 항목)"
        return 0
    else
        warning "검증 완료: $passed 통과, $failed 실패"
        return 1
    fi
}

# 완료 메시지
show_completion() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║${NC}                    ${BOLD}✨ 설치 완료!${NC}                           ${GREEN}║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BOLD}📋 다음 단계 (Claude Code 내부에서 실행):${NC}"
    echo ""
    echo -e "  ${CYAN}# 1. 마켓플레이스 등록${NC}"
    echo -e "  /plugin marketplace add $MARKETPLACE_DIR"
    echo ""
    echo -e "  ${CYAN}# 2. 플러그인 설치${NC}"
    echo -e "  /plugin install $PLUGIN_NAME@calab-marketplace --scope user"
    echo ""
    echo -e "${BOLD}💡 빠른 복사:${NC}"
    echo ""
    echo "/plugin marketplace add $MARKETPLACE_DIR && /plugin install $PLUGIN_NAME@calab-marketplace --scope user"
    echo ""
    echo -e "${BOLD}📁 설치 위치:${NC}"
    echo "  글로벌: $CLAUDE_HOME"
    echo "  마켓플레이스: $MARKETPLACE_DIR"
    echo ""
    echo -e "${BOLD}🔧 사용 가능한 스크립트:${NC}"
    echo "  ./uninstall.sh  - 완전 삭제"
    echo "  ./update.sh     - 업데이트"
    echo ""
    echo -e "로그 파일: ${CYAN}$LOG_FILE${NC}"
    echo ""
}

# 메인 실행
main() {
    # 로그 초기화
    echo "=== 설치 시작: $(date) ===" > "$LOG_FILE"

    show_banner
    check_environment
    clean_previous
    install_global_files
    install_settings
    create_marketplace
    verify_installation
    show_completion

    echo "=== 설치 완료: $(date) ===" >> "$LOG_FILE"
}

main "$@"
