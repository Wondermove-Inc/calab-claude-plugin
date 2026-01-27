#!/bin/bash
#
# session-start-restore-hint.sh - calab-claude-plugin 세션 시작 복원 힌트 훅 (v4)
#
# 원더 무브 연구소 Claude Plug-in의 SessionStart 훅.
# Claude Code 세션 시작/재개 시 체크포인트 파일을 확인하고 복원 안내를 표시합니다.
#
# v4 변경사항:
# - FIFO 배열 최대 5개 체크포인트 지원
# - 사용 가능한 체크포인트 목록 표시
# - --slot N 옵션으로 특정 체크포인트 복원
#
# 훅 입력 (stdin JSON):
# - hook_event_name: "SessionStart"
# - session_id: string
# - is_resume: boolean
# - agent_type: string | null (2.1.2+)
#
# 종료 코드:
# - 0: 무음 (체크포인트 없음 또는 스킵)
# - 2: Claude에 메시지 표시
#
# 설계 철학:
# - 비침투적: 체크포인트 존재 시에만 메시지 표시
# - 정상 실패: 잘못된 JSON → 무음 모드
# - 사용자 친화적: 명확한 복원 안내 제공
#
# 원본: claude-monitoring-main
# 적용: calab-claude-plugin v2.3.0+
#

set -euo pipefail

# Source shared utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=hook-utils.sh
source "${SCRIPT_DIR}/hook-utils.sh"

# Setup configuration
setup_hook_config "SessionStart"

# Read stdin JSON
input=$(cat)

log "SessionStart hook triggered (v4)"

# Check for jq availability
if ! check_jq; then
    # Fail gracefully without jq
    exit 0
fi

# Extract session info from hook input
session_id=$(json_get "${input}" ".session_id" "unknown")
is_resume=$(json_get "${input}" ".is_resume" "false")
log "Session: ${session_id}, Resume: ${is_resume}"

# Check if checkpoint file exists and is valid
if ! validate_checkpoint_file "${CHECKPOINT_FILE}"; then
    # No checkpoint or invalid checkpoint → silent mode
    log "No valid checkpoint file found"
    exit 0
fi

# Check checkpoint version
checkpoint_version=$(checkpoint_get "${CHECKPOINT_FILE}" ".version" "1.0")
log "Checkpoint version: ${checkpoint_version}"

# =============================================================================
# Helper: Calculate relative time from timestamp
# NOTE: Uses cross-platform calculate_relative_time from hook-utils.sh
# =============================================================================
# The calculate_relative_time function is now provided by hook-utils.sh
# which handles both macOS (date -j) and Linux (date -d) correctly

# =============================================================================
# Handle v4 Checkpoint (FIFO array)
# =============================================================================

if [[ "${checkpoint_version}" == "4.0" ]]; then
    # Get checkpoint count
    checkpoint_count=$(get_checkpoint_count "${CHECKPOINT_FILE}")
    log "v4 Checkpoint: ${checkpoint_count} checkpoints found"

    if [[ ${checkpoint_count} -eq 0 ]]; then
        log "No checkpoints in v4 file"
        exit 0
    fi

    # Get latest checkpoint for primary display
    latest_checkpoint=$(get_latest_checkpoint "${CHECKPOINT_FILE}")
    latest_timestamp=$(echo "${latest_checkpoint}" | jq -r '.timestamp // "unknown"')
    latest_relative_time=$(calculate_relative_time "${latest_timestamp}")

    # Get latest checkpoint details
    has_current_work=$(echo "${latest_checkpoint}" | jq -r '.current_work != null')

    if [[ "${has_current_work}" == "true" ]]; then
        plan_path=$(echo "${latest_checkpoint}" | jq -r '.current_work.plan_path // ""')
        plan_name=$(basename "${plan_path}" .md 2>/dev/null || echo "unknown")
    else
        plan_name="(목표 설정 대기)"
    fi

    # Display header
    cat << EOF
==================================================
 [SESSION START] 컨텍스트 복원 안내
==================================================
 저장된 체크포인트: ${checkpoint_count}개

EOF

    # Display checkpoint list (newest first, 1-indexed for user)
    echo " 복원 가능한 체크포인트:"
    echo ""

    # Iterate checkpoints in reverse order (newest first)
    for ((i = checkpoint_count - 1; i >= 0; i--)); do
        checkpoint=$(jq -r ".checkpoints[${i}]" "${CHECKPOINT_FILE}" 2>/dev/null)
        cp_timestamp=$(echo "${checkpoint}" | jq -r '.timestamp // "unknown"')
        cp_summary=$(echo "${checkpoint}" | jq -r '.summary // "작업 정보 없음"')
        cp_relative=$(calculate_relative_time "${cp_timestamp}")

        # Display index (1-based from newest)
        display_index=$((checkpoint_count - i))
        printf " [%d] %-10s - %s\n" "${display_index}" "${cp_relative}" "${cp_summary}"
    done

    # Count completed phases from latest checkpoint
    completed_count=$(echo "${latest_checkpoint}" | jq -r '.completed_phases | length // 0')

    if [[ ${completed_count} -gt 0 ]]; then
        echo ""
        echo " 완료된 작업 (${completed_count}개):"
        echo "${latest_checkpoint}" | jq -r '.completed_phases[-3:] | .[] | "    - " + .name + " (" + .completed_at + ")"' 2>/dev/null || true
    fi

    # Generate session-start-choice JSON safely using jq
    session_choice_json=$(jq -n \
        --argjson detected true \
        --arg version "4.0" \
        --argjson count "${checkpoint_count}" \
        --arg plan "${plan_name}" \
        --arg time "${latest_relative_time}" \
        '{
            checkpoint_detected: $detected,
            version: $version,
            checkpoint_count: $count,
            latest_plan: $plan,
            latest_time: $time,
            options: ["restore", "fresh", "later"]
        }')

    cat << EOF

 복원 명령:
   /restore-context          - 대화형 선택
   /restore-context --slot N - 특정 시점 (1=최근)

<session-start-choice>
${session_choice_json}
</session-start-choice>
==================================================
EOF

    log "v4 display complete: ${checkpoint_count} checkpoints, latest=${plan_name}"
    exit 2
fi

# =============================================================================
# Handle v3 Checkpoint (single checkpoint - legacy)
# =============================================================================

if [[ "${checkpoint_version}" == "3.0" ]]; then
    # Extract v3 fields
    timestamp=$(checkpoint_get "${CHECKPOINT_FILE}" ".timestamp" "unknown")
    relative_time=$(calculate_relative_time "${timestamp}")
    transcript_path=$(checkpoint_get "${CHECKPOINT_FILE}" ".transcript_path" "")

    # Current work info
    has_current_work=$(jq -r '.current_work != null' "${CHECKPOINT_FILE}" 2>/dev/null)

    if [[ "${has_current_work}" == "true" ]]; then
        plan_path=$(checkpoint_get "${CHECKPOINT_FILE}" ".current_work.plan_path" "")
        status=$(checkpoint_get "${CHECKPOINT_FILE}" ".current_work.status" "unknown")
        last_agent=$(checkpoint_get "${CHECKPOINT_FILE}" ".current_work.last_agent" "null")

        # Extract plan name from path
        plan_name=$(basename "${plan_path}" .md 2>/dev/null || echo "unknown")
    else
        plan_name="(목표 설정 대기)"
    fi

    # Count completed phases
    completed_count=$(jq -r '.completed_phases | length' "${CHECKPOINT_FILE}" 2>/dev/null || echo "0")

    # Build completed phases list (max 3 recent)
    completed_list=""
    if [[ ${completed_count} -gt 0 ]]; then
        completed_list=$(jq -r '.completed_phases[-3:] | .[] | "    - " + .name + " (" + .completed_at + ")"' "${CHECKPOINT_FILE}" 2>/dev/null || echo "")
    fi

    log "v3 Checkpoint: plan=${plan_name}, completed=${completed_count}"

    # Display v3 restoration message
    cat << EOF
==================================================
 [SESSION START] 컨텍스트 복원 안내
==================================================
 마지막 체크포인트: ${relative_time}
   이벤트: session_end
 이전 목표: ${plan_name}...
EOF

    if [[ "${has_current_work}" == "true" ]]; then
        echo " 이전 작업 컨텍스트가 존재합니다."
    fi

    if [[ ${completed_count} -gt 0 ]]; then
        echo ""
        echo " 완료된 작업 (${completed_count}개):"
        echo "${completed_list}"
    fi

    cat << EOF

 '/restore-context' 명령으로
   이전 작업을 이어갈 수 있습니다.
==================================================
EOF

    # Exit 2 to display message to Claude
    exit 2
fi

# =============================================================================
# Handle Legacy (v1.0) Checkpoint
# =============================================================================

timestamp=$(checkpoint_get "${CHECKPOINT_FILE}" ".timestamp" "unknown")
relative_time=$(calculate_relative_time "${timestamp}")
plan_name=$(checkpoint_get "${CHECKPOINT_FILE}" ".plan_name" "unknown")
current_phase=$(checkpoint_get "${CHECKPOINT_FILE}" ".current_phase" "1")
phase_status=$(checkpoint_get "${CHECKPOINT_FILE}" ".phase_status" "unknown")

log "v1 Checkpoint found: ${plan_name} PHASE ${current_phase}"

# Display legacy restoration message
cat << EOF
==================================================
 [SESSION START] 컨텍스트 복원 안내
==================================================
 마지막 체크포인트: ${relative_time}
   이벤트: session_end
 이전 목표: ${plan_name}...
 이전 작업 컨텍스트가 존재합니다.

 '/restore-context' 명령으로
   이전 작업을 이어갈 수 있습니다.
==================================================
EOF

# Exit 2 to display message to Claude
exit 2
