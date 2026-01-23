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
