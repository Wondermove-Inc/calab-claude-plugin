#!/bin/bash
#
# precompact-save-state.sh - calab-claude-plugin 컴팩트 전 상태 저장 훅 (v4)
#
# 원더 무브 연구소 Claude Plug-in의 PreCompact 훅.
# Claude Code가 컨텍스트 압축을 수행하기 전 현재 워크플로우 상태를 저장합니다.
#
# v4 변경사항:
# - FIFO 배열 체크포인트 (최대 5개)
# - 각 체크포인트에 슬롯 번호와 요약 포함
# - v3 형식에서 자동 마이그레이션
#
# 훅 입력 (stdin JSON):
# - hook_event_name: "PreCompact"
# - session_id: string
# - transcript_path: string (대화 JSONL 파일 경로)
# - trigger: "manual" | "auto"
# - permission_mode: string
#
# 종료 코드:
# - 0: 성공 (체크포인트 저장 또는 정상 스킵)
# - 1 또는 2로 종료하지 않음 (압축 차단 금지)
#
# 설계 철학:
# - 컨텍스트 압축 차단 금지 (항상 exit 0)
# - 의존성 없으면 정상 실패 (jq)
# - 모든 작업 로깅 (디버깅용)
# - JSON 쓰기 전 검증으로 손상 방지
#
# 원본: claude-monitoring-main
# 적용: calab-claude-plugin v2.3.0+
#

set -euo pipefail

# Error trap for debugging - log errors but don't block compression
trap 'echo "[$(date "+%Y-%m-%d %H:%M:%S")] [PreCompact] ERROR: Script failed at line $LINENO" >> "${HOOK_LOG_FILE:-/tmp/hook.log}"; exit 0' ERR

# Source shared utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=hook-utils.sh
source "${SCRIPT_DIR}/hook-utils.sh"

# Setup configuration
setup_hook_config "PreCompact"

# Read stdin JSON
input=$(cat)

log "PreCompact hook triggered (v4)"

# Check for jq availability (required for JSON processing)
if ! check_jq; then
    # Fail gracefully without jq
    exit 0
fi

# Extract session info from input
session_id=$(json_get "${input}" ".session_id" "unknown")
transcript_path=$(json_get "${input}" ".transcript_path" "")
trigger=$(json_get "${input}" ".trigger" "unknown")

log "Session ID: ${session_id}"
log "Transcript path: ${transcript_path}"
log "Trigger: ${trigger}"

# Generate timestamp in ISO-8601 format (UTC)
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# =============================================================================
# Find Active Plan
# =============================================================================

# Look for plan files in .claude/plans/ (non-PLAN_ prefix, excluding DESIGN and TASKS suffixes)
active_plan=""
active_plan_name=""

# Find most recently modified .md file that is NOT a DESIGN or TASKS file
for plan_file in "${PROJECT_ROOT}"/.claude/plans/*.md; do
    if [[ -f "${plan_file}" ]]; then
        filename=$(basename "${plan_file}")
        # Skip files with -DESIGN.md or -TASKS*.md suffixes
        if [[ ! "${filename}" =~ -DESIGN\.md$ ]] && [[ ! "${filename}" =~ -TASKS.*\.md$ ]]; then
            # Prefer the most recently modified
            if [[ -z "${active_plan}" ]] || [[ "${plan_file}" -nt "${active_plan}" ]]; then
                active_plan="${plan_file}"
                active_plan_name="${filename%.md}"
            fi
        fi
    fi
done

if [[ -z "${active_plan}" ]]; then
    log "No active plan found, creating minimal checkpoint"
    # Create minimal checkpoint entry without plan info
    checkpoint_entry=$(jq -n \
        --arg timestamp "${timestamp}" \
        --arg session_id "${session_id}" \
        --arg transcript_path "${transcript_path}" \
        '{
            timestamp: $timestamp,
            session_id: $session_id,
            transcript_path: $transcript_path,
            current_work: null,
            completed_phases: [],
            plans_tree: "",
            summary: "작업 없음"
        }')
    if validate_json "${checkpoint_entry}"; then
        if add_checkpoint "${checkpoint_entry}" "${CHECKPOINTS_FILE}"; then
            log "Minimal checkpoint added to FIFO: ${CHECKPOINTS_FILE}"
        else
            log "ERROR: Failed to add minimal checkpoint"
        fi
    fi
    exit 0
fi

log "Active plan: ${active_plan_name}"

# =============================================================================
# Find Related Documents (DESIGN, TASKS)
# =============================================================================

design_path=""
tasks_path=""

# Look for corresponding DESIGN file
if [[ -f "${PROJECT_ROOT}/.claude/plans/${active_plan_name}-DESIGN.md" ]]; then
    design_path=".claude/plans/${active_plan_name}-DESIGN.md"
fi

# Look for corresponding TASKS files (may have phase suffix)
for tasks_file in "${PROJECT_ROOT}"/.claude/plans/"${active_plan_name}"-TASKS*.md; do
    if [[ -f "${tasks_file}" ]]; then
        tasks_path=".claude/plans/$(basename "${tasks_file}")"
        break  # Use the first matching TASKS file
    fi
done

log "Design path: ${design_path:-none}"
log "Tasks path: ${tasks_path:-none}"

# =============================================================================
# Parse Agent Execution Log from Plan File
# =============================================================================

last_agent=""
last_agent_id=""
status="in_progress"

# Parse Agent Execution Log table from plan file
if [[ -f "${active_plan}" ]]; then
    # Look for Agent Execution Log section and parse the table
    in_agent_log=false
    while IFS= read -r line; do
        # Detect Agent Execution Log section
        if [[ "$line" =~ "## Agent Execution Log" ]] || [[ "$line" =~ "Agent Execution Log" ]]; then
            in_agent_log=true
            continue
        fi

        # Stop at next section
        if [[ "${in_agent_log}" == true ]] && [[ "$line" =~ ^## ]]; then
            break
        fi

        # Parse table rows - supports two formats:
        # Format 1: | Agent | agentId | Status | Timestamp |
        # Format 2: | Step | Agent | agentId | Status | Timestamp |
        if [[ "${in_agent_log}" == true ]]; then
            agent_name=""
            agent_id=""
            agent_status=""

            # Try Format 2 first (with Step column)
            if [[ "$line" =~ ^\|[[:space:]]*[0-9.]+[[:space:]]*\|[[:space:]]*([a-zA-Z0-9_-]+)[[:space:]]*\|[[:space:]]*([a-zA-Z0-9_-]*)[[:space:]]*\|.*completed ]]; then
                agent_name="${BASH_REMATCH[1]}"
                agent_id="${BASH_REMATCH[2]}"
                agent_status="completed"
            elif [[ "$line" =~ ^\|[[:space:]]*[0-9.]+[[:space:]]*\|[[:space:]]*([a-zA-Z0-9_-]+)[[:space:]]*\|[[:space:]]*([a-zA-Z0-9_-]*)[[:space:]]*\|.*(pending|in_progress|running) ]]; then
                agent_name="${BASH_REMATCH[1]}"
                agent_id="${BASH_REMATCH[2]}"
                agent_status="${BASH_REMATCH[3]}"
            # Try Format 1 (without Step column)
            elif [[ "$line" =~ ^\|[[:space:]]*([a-zA-Z0-9_-]+)[[:space:]]*\|[[:space:]]*([a-zA-Z0-9_-]*)[[:space:]]*\|[[:space:]]*(pending|in_progress|completed|running)[[:space:]]*\| ]]; then
                agent_name="${BASH_REMATCH[1]}"
                agent_id="${BASH_REMATCH[2]}"
                agent_status="${BASH_REMATCH[3]}"
            else
                continue
            fi

            # Skip header row
            if [[ "${agent_name}" == "Agent" ]] || [[ "${agent_name}" == "Step" ]] || [[ "${agent_name}" == "---" ]] || [[ -z "${agent_name}" ]]; then
                continue
            fi

            # Track the last agent entry
            last_agent="${agent_name}"
            if [[ -n "${agent_id}" ]] && [[ "${agent_id}" != "-" ]]; then
                last_agent_id="${agent_id}"
            fi

            # Track overall status
            if [[ "${agent_status}" == "in_progress" ]] || [[ "${agent_status}" == "running" ]]; then
                status="in_progress"
            fi
        fi
    done < "${active_plan}"

    # Log warning if no agent was found in the log
    if [[ -z "${last_agent}" ]]; then
        log "WARNING: No agent found in Agent Execution Log"
    fi
fi

log "Last agent: ${last_agent:-none}"
log "Last agent ID: ${last_agent_id:-none}"
log "Status: ${status}"

# =============================================================================
# Collect Completed Phases
# =============================================================================

completed_phases="[]"
complete_dir="${PROJECT_ROOT}/.claude/plans/complete"

if [[ -d "${complete_dir}" ]]; then
    phases_json="["
    first=true

    # Iterate through date directories
    for date_dir in "${complete_dir}"/*; do
        if [[ -d "${date_dir}" ]]; then
            date_name=$(basename "${date_dir}")

            # Validate date directory name (YYYY-MM-DD format)
            if [[ ! "${date_name}" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
                log "Skipping non-date directory: ${date_name}"
                continue
            fi

            # Find plan files (not DESIGN or TASKS)
            for plan_file in "${date_dir}"/*.md; do
                if [[ -f "${plan_file}" ]]; then
                    filename=$(basename "${plan_file}")

                    # Skip DESIGN, TASKS, and legacy PLAN_/DESIGN_/TASKS_ prefixed files
                    if [[ ! "${filename}" =~ -DESIGN\.md$ ]] && \
                       [[ ! "${filename}" =~ -TASKS.*\.md$ ]] && \
                       [[ ! "${filename}" =~ ^DESIGN_ ]] && \
                       [[ ! "${filename}" =~ ^PLAN_ ]] && \
                       [[ ! "${filename}" =~ ^TASKS_ ]]; then
                        plan_name="${filename%.md}"
                        rel_path=".claude/plans/complete/${date_name}/${filename}"

                        if [[ "${first}" == true ]]; then
                            first=false
                        else
                            phases_json+=","
                        fi

                        phase_obj=$(jq -n -c \
                            --arg name "${plan_name}" \
                            --arg at "${date_name}" \
                            --arg path "${rel_path}" \
                            '{name: $name, completed_at: $at, path: $path}')
                        phases_json+="${phase_obj}"
                    fi
                fi
            done
        fi
    done

    phases_json+="]"
    completed_phases="${phases_json}"
fi

log "Collected completed phases"

# =============================================================================
# Generate Plans Tree
# =============================================================================

plans_tree=""
if command -v tree &> /dev/null; then
    # Use tree command if available
    plans_tree=$(tree -L 3 --noreport "${PROJECT_ROOT}/.claude/plans" 2>/dev/null | head -50 || echo "")
else
    # Fallback to simple ls-based tree
    plans_tree=$(find "${PROJECT_ROOT}/.claude/plans" -maxdepth 3 -type f -name "*.md" 2>/dev/null | \
        sed "s|${PROJECT_ROOT}/.claude/plans/||" | sort | head -30 || echo "")
fi

# Keep plans_tree as raw string (will be properly escaped by jq)
log "Generated plans tree"

# =============================================================================
# Build Current Work Object using jq (proper JSON escaping)
# =============================================================================

# Build current_work JSON using jq -n for proper escaping
current_work=$(jq -n \
    --arg plan_path ".claude/plans/${active_plan_name}.md" \
    --arg design_path "${design_path:-}" \
    --arg tasks_path "${tasks_path:-}" \
    --arg status "${status}" \
    --arg last_agent "${last_agent:-}" \
    --arg last_agent_id "${last_agent_id:-}" \
    '{
        plan_path: $plan_path,
        design_path: (if $design_path == "" then null else $design_path end),
        tasks_path: (if $tasks_path == "" then null else $tasks_path end),
        status: $status,
        last_agent: (if $last_agent == "" then null else $last_agent end),
        last_agent_id: (if $last_agent_id == "" then null else $last_agent_id end)
    }')

# =============================================================================
# Create Checkpoint v4 Entry JSON using jq (proper escaping)
# =============================================================================

# Generate summary for display
checkpoint_summary="${active_plan_name}"
if [[ -n "${last_agent}" ]]; then
    checkpoint_summary="${checkpoint_summary} (${last_agent})"
fi

# Create single checkpoint entry using jq -n for proper JSON construction
checkpoint_entry=$(jq -n \
    --arg timestamp "${timestamp}" \
    --arg session_id "${session_id}" \
    --arg transcript_path "${transcript_path}" \
    --argjson current_work "${current_work}" \
    --argjson completed_phases "${completed_phases}" \
    --arg plans_tree "${plans_tree}" \
    --arg summary "${checkpoint_summary}" \
    '{
        timestamp: $timestamp,
        session_id: $session_id,
        transcript_path: $transcript_path,
        current_work: $current_work,
        completed_phases: $completed_phases,
        plans_tree: $plans_tree,
        summary: $summary
    }')

# Validate and add to FIFO
if validate_json "${checkpoint_entry}"; then
    if add_checkpoint "${checkpoint_entry}" "${CHECKPOINTS_FILE}"; then
        checkpoint_count=$(get_checkpoint_count "${CHECKPOINTS_FILE}")
        log "Checkpoint v4 added to FIFO: ${CHECKPOINTS_FILE} (total: ${checkpoint_count})"
        log "Plan: ${active_plan_name}, Agent: ${last_agent:-none}, Phases: $(echo "${completed_phases}" | jq length)"
    else
        log "ERROR: Failed to add checkpoint to FIFO"
    fi
else
    log "ERROR: Invalid checkpoint entry JSON generated"
    exit 0  # Don't block compression even on error
fi

exit 0
