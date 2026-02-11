#!/bin/bash

# Claude Code Status Line - Display model, context gauge, usage limits, folder, and git branch
# Format: "Model Name | ▓▓▓▓▓░░░░░ | XX% (Rst:Xh) | folder |  branch"

# Read JSON input from stdin
input=$(cat)

# Cache file for usage limits (to avoid hitting API too frequently)
CACHE_FILE="/tmp/claude-usage-cache.json"
CACHE_TTL=60  # Cache for 60 seconds

# Get OAuth token from macOS Keychain
get_oauth_token() {
    local creds
    creds=$(security find-generic-password -s "Claude Code-credentials" -w 2>/dev/null)
    if [ -z "$creds" ]; then
        echo ""
        return
    fi
    echo "$creds" | jq -r '.claudeAiOauth.accessToken // empty' 2>/dev/null
}

# Calculate time remaining from ISO timestamp
calc_time_remaining() {
    local reset_time=$1
    if [ -z "$reset_time" ] || [ "$reset_time" = "null" ]; then
        echo ""
        return
    fi

    # Parse ISO 8601 timestamp (handles +00:00 timezone)
    # Convert to epoch using Python for reliable parsing
    local reset_epoch
    reset_epoch=$(python3 -c "
from datetime import datetime
import sys
try:
    dt = datetime.fromisoformat('$reset_time'.replace('+00:00', '+0000'))
    print(int(dt.timestamp()))
except:
    print(0)
" 2>/dev/null)

    if [ -z "$reset_epoch" ] || [ "$reset_epoch" = "0" ]; then
        echo ""
        return
    fi

    local now_epoch
    now_epoch=$(date "+%s")
    local diff=$((reset_epoch - now_epoch))

    if [ $diff -le 0 ]; then
        echo "now"
        return
    fi

    local hours=$((diff / 3600))
    local mins=$(((diff % 3600) / 60))

    if [ $hours -gt 0 ]; then
        printf "%dh%dm" $hours $mins
    else
        printf "%dm" $mins
    fi
}

# Fetch usage limits from API (with caching)
get_usage_limits() {
    local now_epoch
    now_epoch=$(date "+%s")

    # Check cache
    if [ -f "$CACHE_FILE" ]; then
        local cache_time
        cache_time=$(jq -r '.cached_at // 0' "$CACHE_FILE" 2>/dev/null)
        local age=$((now_epoch - cache_time))

        if [ $age -lt $CACHE_TTL ]; then
            # Use cached data
            cat "$CACHE_FILE"
            return
        fi
    fi

    # Get token
    local token
    token=$(get_oauth_token)
    if [ -z "$token" ]; then
        echo '{"error": "no_token"}'
        return
    fi

    # Fetch from API
    local response
    response=$(curl -s --max-time 2 \
        -H "Accept: application/json" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $token" \
        -H "anthropic-beta: oauth-2025-04-20" \
        -H "User-Agent: claude-code/2.0.31" \
        "https://api.anthropic.com/api/oauth/usage" 2>/dev/null)

    if [ -z "$response" ]; then
        echo '{"error": "fetch_failed"}'
        return
    fi

    # Add timestamp and cache
    echo "$response" | jq --arg ts "$now_epoch" '. + {cached_at: ($ts | tonumber)}' > "$CACHE_FILE" 2>/dev/null
    cat "$CACHE_FILE" 2>/dev/null || echo "$response"
}

# Format usage limits for display
format_usage_limits() {
    local usage_data=$1

    local five_hour_pct
    local five_hour_reset

    five_hour_pct=$(echo "$usage_data" | jq -r '.five_hour.utilization // empty' 2>/dev/null)
    five_hour_reset=$(echo "$usage_data" | jq -r '.five_hour.resets_at // empty' 2>/dev/null)

    if [ -z "$five_hour_pct" ]; then
        echo ""
        return
    fi

    local five_int=${five_hour_pct%.*}
    local five_color
    if [ "$five_int" -lt 50 ]; then
        five_color="\033[32m"  # Green
    elif [ "$five_int" -lt 80 ]; then
        five_color="\033[33m"  # Yellow
    else
        five_color="\033[31m"  # Red
    fi

    local five_remaining=$(calc_time_remaining "$five_hour_reset")
    if [ -n "$five_remaining" ]; then
        echo "${five_color}${five_int}%\033[0m (Rst:${five_remaining})"
    else
        echo "${five_color}${five_int}%\033[0m"
    fi
}

# Helper function to get last N folders from path
# Shows the last N directory names (e.g., last 2: "Workspace/skuber-platform")
get_last_n_folders() {
    local path=$1
    local n=$2
    local home=$HOME

    # Remove home directory prefix if present
    path=${path#$home/}

    # Split path into components
    IFS='/' read -ra parts <<< "$path"
    local len=${#parts[@]}

    # If path has fewer components than requested, show all
    if [ $len -le $n ]; then
        echo "$path"
        return
    fi

    # Get last N components
    local start=$((len - n))
    local result=""
    for ((i=start; i<len; i++)); do
        if [ -n "$result" ]; then
            result="${result}/${parts[$i]}"
        else
            result="${parts[$i]}"
        fi
    done

    echo "$result"
}

# Helper function to create visual gauge with color
# Takes percentage (0-100) and returns a 10-character gauge with ANSI color
# Color scheme:
#   < 60%: Green (safe)
#   60-79%: Yellow (warning)
#   >= 80%: Red (danger/compression imminent)
create_gauge() {
    local pct=$1
    local filled=$((pct / 10))
    local empty=$((10 - filled))

    # Determine color based on percentage
    local color
    if [ $pct -lt 50 ]; then
        color="\033[32m"  # Green
    elif [ $pct -lt 70 ]; then
        color="\033[33m"  # Yellow
    else
        color="\033[31m"  # Red
    fi
    local reset="\033[0m"

    # Build gauge string with color
    local gauge=""
    for ((i=0; i<filled; i++)); do
        gauge="${gauge}▓"
    done
    for ((i=0; i<empty; i++)); do
        gauge="${gauge}░"
    done

    # Apply color to the gauge
    printf "${color}${gauge}${reset}"
}

# Helper function to shorten model name
shorten_model_name() {
    local name=$1
    # Claude Opus 4.5 -> Opus 4.5
    # Claude Sonnet 4.5 -> Sonnet 4.5
    # Claude 3.5 Sonnet -> Sonnet 3.5
    name=$(echo "$name" | sed 's/^Claude //')
    echo "$name"
}

# Helper function to get current git branch
get_git_branch() {
    local path=$1

    # Check if we're in a git repository
    if ! git -C "$path" rev-parse --git-dir &> /dev/null; then
        echo ""
        return
    fi

    # Get current branch name
    local branch=$(git -C "$path" --no-optional-locks branch --show-current 2>/dev/null)

    # If detached HEAD, show short commit hash
    if [ -z "$branch" ]; then
        branch=$(git -C "$path" --no-optional-locks rev-parse --short HEAD 2>/dev/null)
        if [ -n "$branch" ]; then
            branch="detached@${branch}"
        fi
    fi

    echo "$branch"
}

# Extract data from JSON input
model=$(echo "$input" | jq -r '.model.display_name // "Unknown"')
cwd=$(echo "$input" | jq -r '.workspace.current_dir // .cwd')

# Calculate context usage percentage
usage=$(echo "$input" | jq '.context_window.current_usage')
if [ "$usage" != "null" ]; then
    current=$(echo "$usage" | jq '.input_tokens + .cache_creation_input_tokens + .cache_read_input_tokens')
    size=$(echo "$input" | jq '.context_window.context_window_size')
    pct=$((current * 100 / size))
else
    pct=0
fi

# Shorten model name
short_model=$(shorten_model_name "$model")

# Get git branch
git_branch=$(get_git_branch "$cwd")

# Build status line - show last 1 folder
folder_display=$(get_last_n_folders "$cwd" 1)

# Get usage limits
usage_data=$(get_usage_limits)
usage_display=$(format_usage_limits "$usage_data")

# Output the result with colored gauge
printf "%s | " "$short_model"
create_gauge $pct

# Add usage limits if available
if [ -n "$usage_display" ]; then
    printf " | "
    printf "%b" "$usage_display"
fi

# Add folder and git branch
if [ -n "$git_branch" ]; then
    printf " | %s | \033[32mgit:(%s)\033[0m\n" "$folder_display" "$git_branch"
else
    printf " | %s\n" "$folder_display"
fi
