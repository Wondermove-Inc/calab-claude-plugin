#!/bin/bash
#
# link-skills.sh - calab-plugin 스킬을 ~/.claude/skills/에 심볼릭 링크
#
# 사용법:
#   ./link-skills.sh        # 링크 생성
#   ./link-skills.sh --remove  # 링크 제거
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_SKILLS_DIR="$SCRIPT_DIR/plugins/calab-plugin/skills"
TARGET_DIR="$HOME/.claude/skills"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Active 스킬 목록 (/ 자동완성에 표시할 것들)
ACTIVE_SKILLS=(
    "dev"
    "solve"
    "onboard"
    "docs"
    "security"
    "research"
    "jira"
    "refactor"
    "e2e"
    "guard"
)

print_header() {
    echo ""
    echo -e "${BLUE}======================================${NC}"
    echo -e "${BLUE}  calab-plugin 스킬 링크 스크립트${NC}"
    echo -e "${BLUE}======================================${NC}"
    echo ""
}

create_links() {
    print_header

    # 대상 디렉토리 생성
    mkdir -p "$TARGET_DIR"

    echo -e "${YELLOW}플러그인 스킬 디렉토리:${NC} $PLUGIN_SKILLS_DIR"
    echo -e "${YELLOW}링크 대상 디렉토리:${NC} $TARGET_DIR"
    echo ""

    local created=0
    local skipped=0
    local failed=0

    for skill in "${ACTIVE_SKILLS[@]}"; do
        local source_dir="$PLUGIN_SKILLS_DIR/$skill"
        local target_link="$TARGET_DIR/calab-$skill"

        if [ ! -d "$source_dir" ]; then
            echo -e "${RED}[SKIP]${NC} $skill - 소스 디렉토리 없음"
            ((skipped++))
            continue
        fi

        # 기존 링크/디렉토리 확인
        if [ -L "$target_link" ]; then
            # 이미 심볼릭 링크 존재
            local current_target=$(readlink -f "$target_link" 2>/dev/null || echo "")
            if [ "$current_target" = "$source_dir" ]; then
                echo -e "${YELLOW}[EXISTS]${NC} /calab-$skill -> 이미 연결됨"
                ((skipped++))
                continue
            else
                # 다른 곳을 가리키면 제거 후 재생성
                rm "$target_link"
            fi
        elif [ -e "$target_link" ]; then
            echo -e "${RED}[SKIP]${NC} $skill - 충돌: $target_link 이미 존재 (링크 아님)"
            ((skipped++))
            continue
        fi

        # 심볼릭 링크 생성
        if ln -s "$source_dir" "$target_link"; then
            echo -e "${GREEN}[LINK]${NC} /calab-$skill -> $source_dir"
            ((created++))
        else
            echo -e "${RED}[FAIL]${NC} $skill - 링크 생성 실패"
            ((failed++))
        fi
    done

    echo ""
    echo -e "${BLUE}======================================${NC}"
    echo -e "${GREEN}생성됨: $created${NC}"
    echo -e "${YELLOW}스킵됨: $skipped${NC}"
    echo -e "${RED}실패: $failed${NC}"
    echo -e "${BLUE}======================================${NC}"
    echo ""
    echo -e "이제 Claude Code에서 ${GREEN}/calab-${NC}를 입력하면 스킬이 표시됩니다."
    echo -e "예: ${GREEN}/calab-dev${NC}, ${GREEN}/calab-docs${NC}, ${GREEN}/calab-security${NC}"
    echo ""
}

remove_links() {
    print_header

    echo -e "${YELLOW}링크 제거 모드${NC}"
    echo ""

    local removed=0

    for skill in "${ACTIVE_SKILLS[@]}"; do
        local target_link="$TARGET_DIR/calab-$skill"

        if [ -L "$target_link" ]; then
            rm "$target_link"
            echo -e "${GREEN}[REMOVED]${NC} $target_link"
            ((removed++))
        fi
    done

    echo ""
    echo -e "${GREEN}제거된 링크: $removed${NC}"
    echo ""
}

# 메인
case "${1:-}" in
    --remove|-r)
        remove_links
        ;;
    --help|-h)
        echo "사용법: $0 [옵션]"
        echo ""
        echo "옵션:"
        echo "  (없음)      스킬 심볼릭 링크 생성"
        echo "  --remove    스킬 심볼릭 링크 제거"
        echo "  --help      이 도움말 표시"
        ;;
    *)
        create_links
        ;;
esac
