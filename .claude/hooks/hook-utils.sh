#!/bin/bash
#
# hook-utils.sh - calab-claude-plugin 훅 공유 유틸리티
#
# 원더 무브 연구소 Claude Plug-in의 훅 스크립트에서 사용하는 공통 함수:
# - 설정 구성 (Configuration setup)
# - 로깅 (Logging)
# - JSON 검증 (JSON validation)
# - 체크포인트 관리 (v4 FIFO)
#
# 원본: claude-monitoring-main
# 적용: calab-claude-plugin v2.3.0+
#

# Common configuration (sourced by hooks)
setup_hook_config() {
    local hook_name=$1

    # Export configuration variables (declare and assign separately per ShellCheck SC2155)
    local script_dir
    local project_root
    script_dir="$(cd "$(dirname "${BASH_SOURCE[1]}")" && pwd)"
    project_root="$(cd "${script_dir}/../.." && pwd)"

    export SCRIPT_DIR="${script_dir}"
    export PROJECT_ROOT="${project_root}"
    export CHECKPOINTS_FILE="${PROJECT_ROOT}/.claude/workflow-checkpoint.json"
    # Legacy alias for backward compatibility
    export CHECKPOINT_FILE="${CHECKPOINTS_FILE}"
    export LOG_FILE="${PROJECT_ROOT}/.claude/hooks/hook.log"
    export HOOK_NAME="$hook_name"
    export MAX_CHECKPOINTS=5

    # Ensure log directory exists
    mkdir -p "$(dirname "${LOG_FILE}")"
}

# Logging function with hook name prefix
log() {
    local message=$1
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [${HOOK_NAME}] ${message}" >> "${LOG_FILE}"
}

# Check if jq is available
check_jq() {
    if ! command -v jq &> /dev/null; then
        log "ERROR: jq is not installed"
        return 1
    fi
    return 0
}

# Validate JSON string
validate_json() {
    local json_string=$1
    if echo "${json_string}" | jq . > /dev/null 2>&1; then
        return 0
    else
        log "ERROR: Invalid JSON"
        return 1
    fi
}

# Validate checkpoint file exists and is valid JSON
validate_checkpoint_file() {
    local checkpoint_file=$1

    if [[ ! -f "${checkpoint_file}" ]]; then
        log "Checkpoint file does not exist: ${checkpoint_file}"
        return 1
    fi

    if ! jq . "${checkpoint_file}" > /dev/null 2>&1; then
        log "ERROR: Invalid checkpoint JSON in ${checkpoint_file}"
        return 1
    fi

    return 0
}

# Extract field from JSON using jq
json_get() {
    local json_string=$1
    local field=$2
    local default=${3:-""}

    local value
    value=$(echo "${json_string}" | jq -r "${field} // \"${default}\"" 2>/dev/null)

    echo "${value}"
}

# Extract field from checkpoint file
checkpoint_get() {
    local checkpoint_file=$1
    local field=$2
    local default=${3:-""}

    local value
    value=$(jq -r "${field} // \"${default}\"" "${checkpoint_file}" 2>/dev/null)

    echo "${value}"
}

# =============================================================================
# Cross-Platform Date Utilities
# =============================================================================

# Parse ISO-8601 timestamp to epoch seconds (cross-platform)
# Args: iso_timestamp (e.g., "2026-01-25T12:00:00Z")
# Returns: epoch timestamp in seconds
parse_iso_timestamp() {
    local timestamp=$1

    if [[ -z "${timestamp}" ]] || [[ "${timestamp}" == "unknown" ]]; then
        echo "0"
        return
    fi

    local epoch
    if [[ "$(uname)" == "Darwin" ]]; then
        # macOS: Use -j -f options
        epoch=$(date -j -f "%Y-%m-%dT%H:%M:%SZ" "${timestamp}" +%s 2>/dev/null)
    else
        # Linux: Use -d option
        epoch=$(date -d "${timestamp}" +%s 2>/dev/null)
    fi

    echo "${epoch:-0}"
}

# Calculate relative time string from timestamp (cross-platform)
# Args: iso_timestamp
# Returns: Korean relative time string (e.g., "방금 전", "5분 전")
calculate_relative_time() {
    local timestamp=$1
    local relative_time=""

    if [[ -z "${timestamp}" ]] || [[ "${timestamp}" == "unknown" ]]; then
        echo "알 수 없음"
        return
    fi

    local checkpoint_epoch
    checkpoint_epoch=$(parse_iso_timestamp "${timestamp}")

    if [[ "${checkpoint_epoch}" == "0" ]]; then
        echo "알 수 없음"
        return
    fi

    local current_epoch
    current_epoch=$(date +%s)
    local diff_seconds=$((current_epoch - checkpoint_epoch))

    # Handle negative timestamps (future dates)
    if [[ ${diff_seconds} -lt 0 ]]; then
        echo "알 수 없음"
        return
    fi

    if [[ ${diff_seconds} -lt 60 ]]; then
        relative_time="방금 전"
    elif [[ ${diff_seconds} -lt 3600 ]]; then
        relative_time="$((diff_seconds / 60))분 전"
    elif [[ ${diff_seconds} -lt 86400 ]]; then
        relative_time="$((diff_seconds / 3600))시간 전"
    else
        relative_time="$((diff_seconds / 86400))일 전"
    fi

    echo "${relative_time}"
}

# =============================================================================
# Cross-Platform File Locking
# =============================================================================

# Acquire lock using mkdir atomic operation (cross-platform)
# Args: lock_dir
# Returns: 0 on success, 1 on failure
acquire_lock() {
    local lock_dir=$1
    local max_attempts=20
    local attempt=0

    while [[ ${attempt} -lt ${max_attempts} ]]; do
        if mkdir "${lock_dir}" 2>/dev/null; then
            return 0
        fi
        ((attempt++))
        sleep 0.5
    done
    log "ERROR: Failed to acquire lock after ${max_attempts} attempts"
    return 1
}

# Release lock
# Args: lock_dir
release_lock() {
    local lock_dir=$1
    rm -rf "${lock_dir}" 2>/dev/null || true
}

# =============================================================================
# Checkpoint Schema Validation
# =============================================================================

# Validate checkpoint schema based on version
# Args: checkpoint_file
# Returns: 0 if valid, 1 if invalid
validate_checkpoint_schema() {
    local checkpoint_file=$1

    if [[ ! -f "${checkpoint_file}" ]]; then
        log "Schema validation: file does not exist"
        return 1
    fi

    local version
    version=$(jq -r '.version // "1.0"' "${checkpoint_file}" 2>/dev/null)

    case "${version}" in
        "4.0")
            # v4: Must have checkpoints array with at least one entry
            if ! jq -e '.checkpoints | type == "array" and length > 0' "${checkpoint_file}" >/dev/null 2>&1; then
                log "Schema validation failed: v4 requires non-empty checkpoints array"
                return 1
            fi
            ;;
        "3.0")
            # v3: Must have timestamp and session_id
            if ! jq -e '.timestamp and .session_id' "${checkpoint_file}" >/dev/null 2>&1; then
                log "Schema validation failed: v3 requires timestamp and session_id"
                return 1
            fi
            ;;
        *)
            # v1.x or unknown: Must have plan_name and current_phase
            if ! jq -e '.plan_name and .current_phase' "${checkpoint_file}" >/dev/null 2>&1; then
                log "Schema validation failed: v1 requires plan_name and current_phase"
                return 1
            fi
            ;;
    esac

    log "Schema validation passed: version ${version}"
    return 0
}

# =============================================================================
# Checkpoint FIFO Utilities (v4)
# =============================================================================

# Get current checkpoint count
# Returns: number of checkpoints in file
get_checkpoint_count() {
    local checkpoint_file=${1:-"${CHECKPOINTS_FILE}"}

    if [[ ! -f "${checkpoint_file}" ]]; then
        echo "0"
        return
    fi

    local count
    count=$(jq -r '.checkpoints | length // 0' "${checkpoint_file}" 2>/dev/null)
    echo "${count:-0}"
}

# Get latest checkpoint (most recent)
# Returns: JSON object of latest checkpoint or empty object
get_latest_checkpoint() {
    local checkpoint_file=${1:-"${CHECKPOINTS_FILE}"}

    if [[ ! -f "${checkpoint_file}" ]]; then
        echo "{}"
        return
    fi

    jq -r '.checkpoints[-1] // {}' "${checkpoint_file}" 2>/dev/null
}

# Get checkpoint by slot number (0-indexed from oldest)
# Args: slot_number [checkpoint_file]
# Returns: JSON object of checkpoint at slot or empty object
get_checkpoint_by_slot() {
    local slot=$1
    local checkpoint_file=${2:-"${CHECKPOINTS_FILE}"}

    if [[ ! -f "${checkpoint_file}" ]]; then
        echo "{}"
        return
    fi

    jq -r ".checkpoints[${slot}] // {}" "${checkpoint_file}" 2>/dev/null
}

# Get checkpoint by reverse index (1 = latest, 2 = second latest, etc.)
# Args: reverse_index [checkpoint_file]
# Returns: JSON object of checkpoint or empty object
get_checkpoint_by_reverse_index() {
    local index=$1
    local checkpoint_file=${2:-"${CHECKPOINTS_FILE}"}

    if [[ ! -f "${checkpoint_file}" ]]; then
        echo "{}"
        return
    fi

    # Convert 1-indexed to jq negative index (-1 = last, -2 = second last)
    local jq_index=$((-index))
    jq -r ".checkpoints[${jq_index}] // {}" "${checkpoint_file}" 2>/dev/null
}

# Add new checkpoint with FIFO logic (removes oldest if exceeds max)
# Args: new_checkpoint_json [checkpoint_file] [max_checkpoints]
# Returns: 0 on success, 1 on failure
# Note: Uses mkdir-based locking for cross-platform compatibility
add_checkpoint() {
    local new_checkpoint=$1
    local checkpoint_file=${2:-"${CHECKPOINTS_FILE}"}
    local max_count=${3:-${MAX_CHECKPOINTS:-5}}

    # Validate input JSON
    if ! echo "${new_checkpoint}" | jq . > /dev/null 2>&1; then
        log "ERROR: Invalid checkpoint JSON provided to add_checkpoint"
        return 1
    fi

    local lock_dir="${checkpoint_file}.lock"
    local temp_file="${checkpoint_file}.tmp"

    # Ensure checkpoint directory exists
    mkdir -p "$(dirname "${checkpoint_file}")"

    # Acquire cross-platform lock
    if ! acquire_lock "${lock_dir}"; then
        return 1
    fi

    # Ensure lock release on exit
    trap "release_lock '${lock_dir}'" EXIT

    local result=0

    if [[ ! -f "${checkpoint_file}" ]]; then
        # Create new v4 checkpoint file
        jq -n --argjson cp "${new_checkpoint}" --argjson max "${max_count}" '{
            "version": "4.0",
            "max_checkpoints": $max,
            "checkpoints": [$cp]
        }' > "${temp_file}" || result=1
    else
        # Check version and migrate if needed
        local version
        version=$(jq -r '.version // "1.0"' "${checkpoint_file}" 2>/dev/null) || version="1.0"

        local working_file="${checkpoint_file}"
        if [[ "${version}" != "4.0" ]]; then
            # Migrate from v3 or older to v4
            if ! migrate_checkpoint_to_v4 "${checkpoint_file}" "${temp_file}"; then
                log "ERROR: Failed to migrate checkpoint to v4"
                release_lock "${lock_dir}"
                trap - EXIT
                return 1
            fi
            working_file="${temp_file}"
        fi

        # Add new checkpoint and apply FIFO
        jq --argjson cp "${new_checkpoint}" --argjson max "${max_count}" '
            .checkpoints += [$cp] |
            if (.checkpoints | length) > $max then
                .checkpoints = .checkpoints[-$max:]
            else
                .
            end |
            # Update slot numbers
            .checkpoints = [.checkpoints | to_entries[] | .value + {"slot": .key}]
        ' "${working_file}" > "${temp_file}.new" && mv "${temp_file}.new" "${temp_file}" || result=1
    fi

    # Validate and finalize
    if [[ ${result} -eq 0 ]] && jq . "${temp_file}" > /dev/null 2>&1; then
        mv "${temp_file}" "${checkpoint_file}"
    else
        log "ERROR: Generated invalid checkpoint JSON"
        rm -f "${temp_file}" "${temp_file}.new"
        result=1
    fi

    release_lock "${lock_dir}"
    trap - EXIT
    return ${result}
}

# Migrate v3 (or older) checkpoint to v4 format
# Args: old_file new_file
migrate_checkpoint_to_v4() {
    local old_file=$1
    local new_file=$2

    local version
    version=$(jq -r '.version // "1.0"' "${old_file}" 2>/dev/null)

    log "Migrating checkpoint from v${version} to v4"

    if [[ "${version}" == "3.0" ]]; then
        # v3 has single checkpoint structure, wrap it as first entry in array
        jq '{
            "version": "4.0",
            "max_checkpoints": 5,
            "checkpoints": [
                {
                    "slot": 0,
                    "timestamp": .timestamp,
                    "session_id": .session_id,
                    "transcript_path": .transcript_path,
                    "current_work": .current_work,
                    "completed_phases": .completed_phases,
                    "plans_tree": .plans_tree,
                    "summary": (
                        if .current_work.plan_path then
                            (.current_work.plan_path | split("/")[-1] | rtrimstr(".md")) +
                            (if .current_work.last_agent then " (" + .current_work.last_agent + ")" else "" end)
                        else
                            "작업 없음"
                        end
                    )
                }
            ]
        }' "${old_file}" > "${new_file}"
    else
        # v1.x or unknown version - create fresh v4 structure
        jq '{
            "version": "4.0",
            "max_checkpoints": 5,
            "checkpoints": [
                {
                    "slot": 0,
                    "timestamp": .timestamp,
                    "session_id": (.session_id // "unknown"),
                    "current_work": {
                        "plan_path": (".claude/plans/" + (.plan_name // "unknown") + ".md"),
                        "status": (.phase_status // "unknown")
                    },
                    "summary": ((.plan_name // "unknown") + " PHASE " + ((.current_phase // 1) | tostring))
                }
            ]
        }' "${old_file}" > "${new_file}"
    fi

    return $?
}

# Get all checkpoints as array for display
# Returns: JSON array of checkpoints with display info
get_all_checkpoints_display() {
    local checkpoint_file=${1:-"${CHECKPOINTS_FILE}"}

    if [[ ! -f "${checkpoint_file}" ]]; then
        echo "[]"
        return
    fi

    jq -r '.checkpoints // []' "${checkpoint_file}" 2>/dev/null
}
