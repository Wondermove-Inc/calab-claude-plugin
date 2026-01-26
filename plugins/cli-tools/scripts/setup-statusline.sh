#!/bin/bash

# ============================================
# Claude Code Statusline 한방 설치 스크립트
# ============================================
# 사용법: bash setup-statusline.sh
# ============================================

set -e

echo "============================================"
echo " Claude Code Statusline 설치 시작"
echo "============================================"
echo ""

# 색상 정의
GREEN='\033[32m'
YELLOW='\033[33m'
CYAN='\033[36m'
RED='\033[31m'
RESET='\033[0m'

# 1. 사전 요구사항 확인
echo -e "${CYAN}[1/6]${RESET} 사전 요구사항 확인..."

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

if ! command -v bc &> /dev/null; then
    echo -e "${YELLOW}  → bc 설치 중...${RESET}"
    if command -v apt &> /dev/null; then
        sudo apt install -y bc
    elif command -v brew &> /dev/null; then
        brew install bc
    fi
    # 설치 후 재확인
    if ! command -v bc &> /dev/null; then
        echo -e "${RED}  ✗ bc를 수동으로 설치하세요${RESET}"
        exit 1
    fi
fi
echo -e "${GREEN}  ✓ bc 설치됨${RESET}"

# 2. 디렉토리 생성
echo -e "${CYAN}[2/6]${RESET} 디렉토리 생성..."
mkdir -p ~/.claude
mkdir -p ~/.claude/backup
echo -e "${GREEN}  ✓ ~/.claude 디렉토리 준비됨${RESET}"

# 3. 기존 설정 백업
echo -e "${CYAN}[3/6]${RESET} 기존 설정 백업..."
BACKUP_TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=~/.claude/backup/statusline_${BACKUP_TIMESTAMP}

BACKUP_CREATED=false

# settings.json 백업
if [ -f ~/.claude/settings.json ]; then
    mkdir -p "$BACKUP_DIR"
    cp ~/.claude/settings.json "$BACKUP_DIR/settings.json"
    echo -e "${YELLOW}  → settings.json 백업됨${RESET}"
    BACKUP_CREATED=true
fi

# statusline-command.sh 백업
if [ -f ~/.claude/statusline-command.sh ]; then
    mkdir -p "$BACKUP_DIR"
    cp ~/.claude/statusline-command.sh "$BACKUP_DIR/statusline-command.sh"
    echo -e "${YELLOW}  → statusline-command.sh 백업됨${RESET}"
    BACKUP_CREATED=true
fi

if [ "$BACKUP_CREATED" = true ]; then
    echo -e "${GREEN}  ✓ 백업 완료: $BACKUP_DIR${RESET}"
else
    echo -e "${GREEN}  ✓ 백업할 기존 설정 없음${RESET}"
fi

# 4. Statusline 스크립트 생성
echo -e "${CYAN}[4/6]${RESET} Statusline 스크립트 생성..."

cat > ~/.claude/statusline-command.sh << 'STATUSLINE_SCRIPT'
#!/bin/bash

# Read JSON input from stdin
input=$(cat)

# ANSI Color codes
RESET=$'\033[0m'
BOLD=$'\033[1m'
RED=$'\033[31m'
GREEN=$'\033[32m'
YELLOW=$'\033[33m'
BLUE=$'\033[34m'
MAGENTA=$'\033[35m'
CYAN=$'\033[36m'
GRAY=$'\033[90m'

# Extract values from JSON
model_name=$(echo "$input" | jq -r '.model.display_name // "Claude"')
cwd=$(echo "$input" | jq -r '.workspace.current_dir // ""')
remaining=$(echo "$input" | jq -r '.context_window.remaining_percentage // empty')

# Shorten model name
if echo "$model_name" | grep -qi "opus"; then
    model_short=$(echo "$model_name" | sed -E 's/.*([Oo]pus[^"]*)/\1/' | sed 's/^ *//')
elif echo "$model_name" | grep -qi "sonnet"; then
    model_short=$(echo "$model_name" | sed -E 's/.*([Ss]onnet[^"]*)/\1/' | sed 's/^ *//')
elif echo "$model_name" | grep -qi "haiku"; then
    model_short=$(echo "$model_name" | sed -E 's/.*([Hh]aiku[^"]*)/\1/' | sed 's/^ *//')
else
    model_short=$(echo "$model_name" | sed 's/Claude //')
fi

# Get git info
git_info=""
if [ -d "$cwd/.git" ] || git -C "$cwd" rev-parse --git-dir > /dev/null 2>&1; then
    git_branch=$(git -C "$cwd" --no-optional-locks branch --show-current 2>/dev/null || echo "")
    if [ -n "$git_branch" ]; then
        if git -C "$cwd" --no-optional-locks diff-index --quiet HEAD -- 2>/dev/null; then
            git_status=""
        else
            git_status="${RED}✗${RESET}"
        fi
        git_info=" ${GRAY}git:(${GREEN}${git_branch}${GRAY})${RESET}${git_status:+ $git_status}"
    fi
fi

# Create context usage bar
if [ -n "$remaining" ]; then
    used_pct=$(echo "$input" | jq -r '.context_window.used_percentage // 0')
    used_int=${used_pct%.*}
    filled=$(printf "%.0f" $(echo "$used_pct / 10" | bc -l))
    empty=$((10 - filled))

    if [ "$used_int" -lt 50 ]; then
        BAR_COLOR=$GREEN
    elif [ "$used_int" -lt 75 ]; then
        BAR_COLOR=$YELLOW
    else
        BAR_COLOR=$RED
    fi

    filled_bar=""
    empty_bar=""
    for ((i=0; i<filled; i++)); do filled_bar="${filled_bar}█"; done
    for ((i=0; i<empty; i++)); do empty_bar="${empty_bar}░"; done

    context_display=" ${BAR_COLOR}${filled_bar}${GRAY}${empty_bar}${RESET} ${BAR_COLOR}${used_pct}%${RESET}"
else
    context_display=""
fi

dir_name=$(basename "$cwd")

printf "%s" "${BOLD}${MAGENTA}[${model_short}]${RESET}${context_display} ${GRAY}|${RESET} ${CYAN}➜${RESET} ${BOLD}${BLUE}${dir_name}${RESET}${git_info}"
STATUSLINE_SCRIPT

chmod +x ~/.claude/statusline-command.sh
echo -e "${GREEN}  ✓ ~/.claude/statusline-command.sh 생성됨${RESET}"

# 5. settings.json 업데이트
echo -e "${CYAN}[5/6]${RESET} settings.json 업데이트..."

SETTINGS_FILE=~/.claude/settings.json
STATUSLINE_CMD="bash $HOME/.claude/statusline-command.sh"

if [ -f "$SETTINGS_FILE" ]; then
    # 기존 파일이 있는 경우
    if grep -q '"statusLine"' "$SETTINGS_FILE"; then
        echo -e "${YELLOW}  → 기존 statusLine 설정 업데이트${RESET}"
        # jq로 statusLine 업데이트
        tmp=$(mktemp)
        jq --arg cmd "$STATUSLINE_CMD" '.statusLine = {"type": "command", "command": $cmd}' "$SETTINGS_FILE" > "$tmp"
        mv "$tmp" "$SETTINGS_FILE"
    else
        echo -e "${YELLOW}  → statusLine 설정 추가${RESET}"
        # jq로 statusLine 추가
        tmp=$(mktemp)
        jq --arg cmd "$STATUSLINE_CMD" '. + {"statusLine": {"type": "command", "command": $cmd}}' "$SETTINGS_FILE" > "$tmp"
        mv "$tmp" "$SETTINGS_FILE"
    fi
else
    # 새로 생성
    echo -e "${YELLOW}  → settings.json 새로 생성${RESET}"
    cat > "$SETTINGS_FILE" << EOF
{
  "statusLine": {
    "type": "command",
    "command": "$STATUSLINE_CMD"
  }
}
EOF
fi
echo -e "${GREEN}  ✓ settings.json 업데이트됨${RESET}"

# 6. 테스트
echo -e "${CYAN}[6/6]${RESET} 테스트 실행..."
echo ""

TEST_RESULT=$(echo '{"model":{"display_name":"Claude Opus 4.5"},"workspace":{"current_dir":"'$(pwd)'"},"context_window":{"remaining_percentage":40,"used_percentage":60}}' | bash ~/.claude/statusline-command.sh)

echo -e "  테스트 결과: $TEST_RESULT"
echo ""

# 완료
echo "============================================"
echo -e "${GREEN} ✓ 설치 완료!${RESET}"
echo "============================================"
echo ""
echo " 생성/수정된 파일:"
echo "   • ~/.claude/statusline-command.sh"
echo "   • ~/.claude/settings.json (업데이트)"
if [ "$BACKUP_CREATED" = true ]; then
    echo ""
    echo " 백업 위치:"
    echo "   • $BACKUP_DIR"
    echo ""
    echo " 복원 방법:"
    echo "   cp $BACKUP_DIR/settings.json ~/.claude/settings.json"
fi
echo ""
echo " 다음 단계:"
echo "   Claude Code를 재시작하세요: claude"
echo ""
echo "============================================"
