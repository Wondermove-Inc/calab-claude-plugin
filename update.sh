#!/bin/bash
# ============================================================
# Calab Claude Plugin - 자동 업데이트 스크립트
# ============================================================
# 사용법: ./update.sh [--force]
# ============================================================

set -e

# 버전 및 경로 설정
PLUGIN_VERSION="2.4.0"
PLUGIN_NAME="calab-plugin"
PLUGIN_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_HOME="$HOME/.claude"
MARKETPLACE_DIR="$CLAUDE_HOME/calab-marketplace"
LOG_FILE="$PLUGIN_DIR/update.log"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# 옵션 파싱
FORCE_UPDATE=false
for arg in "$@"; do
    case $arg in
        --force)
            FORCE_UPDATE=true
            shift
            ;;
    esac
done

# 로깅 함수
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"; }
info() { echo -e "${BLUE}ℹ${NC} $1"; log "INFO: $1"; }
success() { echo -e "${GREEN}✓${NC} $1"; log "SUCCESS: $1"; }
warning() { echo -e "${YELLOW}⚠${NC} $1"; log "WARNING: $1"; }
error() { echo -e "${RED}✗${NC} $1"; log "ERROR: $1"; }
step() { echo -e "\n${CYAN}${BOLD}[$1]${NC} $2"; log "STEP $1: $2"; }

# 배너 출력
show_banner() {
    echo ""
    echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}     ${BOLD}Calab Claude Plugin - 자동 업데이트${NC}                     ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}     새 버전: ${GREEN}v$PLUGIN_VERSION${NC}                                      ${CYAN}║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# 버전 비교
check_version() {
    step "1/4" "버전 확인"

    local installed_version=""

    # 설치된 버전 확인
    if [ -f "$MARKETPLACE_DIR/plugins/$PLUGIN_NAME/.claude-plugin/plugin.json" ]; then
        installed_version=$(grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' "$MARKETPLACE_DIR/plugins/$PLUGIN_NAME/.claude-plugin/plugin.json" | head -1 | cut -d'"' -f4)
    fi

    if [ -z "$installed_version" ]; then
        warning "설치된 버전을 찾을 수 없습니다."
        info "새로 설치를 진행합니다."
        return 0
    fi

    info "설치된 버전: v$installed_version"
    info "새 버전: v$PLUGIN_VERSION"

    if [ "$installed_version" = "$PLUGIN_VERSION" ] && [ "$FORCE_UPDATE" = false ]; then
        success "이미 최신 버전입니다."
        echo ""
        echo -e "${BOLD}💡 강제 업데이트하려면:${NC}"
        echo "  ./update.sh --force"
        echo ""
        exit 0
    fi

    if [ "$FORCE_UPDATE" = true ]; then
        info "강제 업데이트 모드 (--force)"
    fi

    success "업데이트가 필요합니다."
}

# 백업 생성
create_backup() {
    step "2/4" "백업 생성"

    local backup_dir="$CLAUDE_HOME/backup_$(date '+%Y%m%d_%H%M%S')"

    # 설정 파일 백업
    if [ -f "$CLAUDE_HOME/settings.json" ]; then
        mkdir -p "$backup_dir"
        cp "$CLAUDE_HOME/settings.json" "$backup_dir/"
        success "settings.json 백업됨"
    fi

    # memory 폴더 백업 (사용자 데이터)
    if [ -d "$CLAUDE_HOME/memory" ]; then
        mkdir -p "$backup_dir"
        cp -r "$CLAUDE_HOME/memory" "$backup_dir/"
        success "memory 폴더 백업됨"
    fi

    # project-context 폴더 백업
    if [ -d "$CLAUDE_HOME/project-context" ]; then
        mkdir -p "$backup_dir"
        cp -r "$CLAUDE_HOME/project-context" "$backup_dir/"
        success "project-context 폴더 백업됨"
    fi

    if [ -d "$backup_dir" ]; then
        info "백업 위치: $backup_dir"
    else
        info "백업할 파일 없음"
    fi
}

# 업데이트 실행
run_update() {
    step "3/4" "업데이트 실행"

    # install.sh 실행 (내부적으로 정리 후 설치)
    if [ -f "$PLUGIN_DIR/install.sh" ]; then
        info "install.sh 실행 중..."
        echo ""

        # install.sh 실행 (배너 제외)
        bash "$PLUGIN_DIR/install.sh"
    else
        error "install.sh를 찾을 수 없습니다."
        exit 1
    fi
}

# 업데이트 검증
verify_update() {
    step "4/4" "업데이트 검증"

    local new_version=""

    if [ -f "$MARKETPLACE_DIR/plugins/$PLUGIN_NAME/.claude-plugin/plugin.json" ]; then
        new_version=$(grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' "$MARKETPLACE_DIR/plugins/$PLUGIN_NAME/.claude-plugin/plugin.json" | head -1 | cut -d'"' -f4)
    fi

    if [ "$new_version" = "$PLUGIN_VERSION" ]; then
        success "업데이트 완료: v$new_version"
    else
        warning "버전 확인 필요: $new_version"
    fi
}

# 완료 메시지
show_completion() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║${NC}                  ${BOLD}✨ 업데이트 완료!${NC}                         ${GREEN}║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BOLD}📋 변경사항 확인:${NC}"
    echo "  git log --oneline -5"
    echo ""
    echo -e "${BOLD}🔄 Claude Code에서 플러그인 재설치:${NC}"
    echo "  /plugin uninstall $PLUGIN_NAME"
    echo "  /plugin install $PLUGIN_NAME@calab-marketplace --scope user"
    echo ""
    echo -e "로그 파일: ${CYAN}$LOG_FILE${NC}"
    echo ""
}

# Git 업데이트 (선택)
update_from_git() {
    if [ -d "$PLUGIN_DIR/.git" ]; then
        step "0/4" "Git 업데이트 확인"

        if command -v git &> /dev/null; then
            local current_branch=$(git -C "$PLUGIN_DIR" branch --show-current)
            info "현재 브랜치: $current_branch"

            # 원격 변경사항 확인
            git -C "$PLUGIN_DIR" fetch origin 2>/dev/null || true

            local local_commit=$(git -C "$PLUGIN_DIR" rev-parse HEAD)
            local remote_commit=$(git -C "$PLUGIN_DIR" rev-parse origin/$current_branch 2>/dev/null || echo "")

            if [ -n "$remote_commit" ] && [ "$local_commit" != "$remote_commit" ]; then
                info "원격에 새로운 변경사항이 있습니다."
                read -p "Git에서 최신 버전을 가져올까요? (y/N): " -n 1 -r
                echo ""

                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    git -C "$PLUGIN_DIR" pull origin $current_branch
                    success "Git 업데이트 완료"

                    # 버전 재확인
                    PLUGIN_VERSION=$(grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' "$PLUGIN_DIR/.claude-plugin/plugin.json" | head -1 | cut -d'"' -f4)
                    info "새 버전: v$PLUGIN_VERSION"
                fi
            else
                success "Git 저장소가 최신 상태입니다."
            fi
        fi
    fi
}

# 메인 실행
main() {
    # 로그 초기화
    echo "=== 업데이트 시작: $(date) ===" > "$LOG_FILE"

    show_banner
    update_from_git
    check_version
    create_backup
    run_update
    verify_update
    show_completion

    echo "=== 업데이트 완료: $(date) ===" >> "$LOG_FILE"
}

main "$@"
