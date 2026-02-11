#!/bin/bash
# update-progress.sh - 워크플로우 Progress 파일 업데이트 유틸리티
# Usage: bash <script-path> <command> <epic-id> [args...]
#
# Commands:
#   start      <epic-id> <에이전트명>                    - 에이전트 시작 (진행중 표시)
#   complete   <epic-id> <에이전트명> <산출물> [다음에이전트]  - 에이전트 완료
#   checkpoint <epic-id> <에이전트명> <진행률> <현재상태>    - 체크포인트 갱신
#   finish     <epic-id>                                - 정상 완료 (전체 체크 + 완료 표시)
#   cancel     <epic-id>                                - 사용자 취소
#   fail       <epic-id> <에이전트명> <실패원인>           - 에이전트 실패 중단

set -euo pipefail

COMMAND="${1:?Usage: $0 <command> <epic-id> [args...]}"
EPIC_ID="${2:?Epic ID required}"
PROGRESS_FILE=".workflow/progress/${EPIC_ID}.md"
NOW=$(date '+%Y-%m-%d %H:%M')

if [ ! -f "$PROGRESS_FILE" ]; then
  echo "Error: Progress file not found: $PROGRESS_FILE" >&2
  exit 1
fi

# 최종 업데이트 시각 갱신 (macOS sed 호환 - \n 대신 실제 개행 사용)
update_timestamp() {
  sed -i '' "/^## 최종 업데이트/,/^[^#]/{
    /^## 최종 업데이트/!{/^$/!d;}
  }" "$PROGRESS_FILE"
  sed -i '' "/^## 최종 업데이트/a\\
${NOW}" "$PROGRESS_FILE"
}

# "최근 작업" 섹션에 항목 추가 (최신 3건만 유지)
add_recent_work() {
  local entry="$1"
  # 항목 추가
  sed -i '' "/^## 최근 작업/a\\
${entry}" "$PROGRESS_FILE"
  # 4번째 이후 항목 삭제 (## 최근 작업 다음 줄부터 세어 3줄 초과분 제거)
  awk '
    /^## 최근 작업/ { in_section=1; count=0; print; next }
    in_section && /^## / { in_section=0; print; next }
    in_section && /^$/ { print; next }
    in_section {
      count++
      if (count <= 3) print
      next
    }
    { print }
  ' "$PROGRESS_FILE" > "${PROGRESS_FILE}.tmp" && mv "${PROGRESS_FILE}.tmp" "$PROGRESS_FILE"
}

# "다음 세션 지침" 섹션 내용 교체
replace_next_session() {
  local content="$1"
  sed -i '' '/^## 다음 세션 지침/,/^## /{
    /^## 다음 세션 지침/!{/^## /!d;}
  }' "$PROGRESS_FILE"
  sed -i '' "/^## 다음 세션 지침/a\\
${content}" "$PROGRESS_FILE"
}

# "진행 상태" 섹션 내 체크박스만 대상으로 일괄 완료 처리 (Warning 2 대응)
complete_all_in_progress_section() {
  awk '
    /^## 진행 상태/ { in_section=1; print; next }
    in_section && /^## / { in_section=0; print; next }
    in_section && /^- \[ \] \*\*(.+)\*\*/ {
      sub(/^- \[ \] \*\*/, "- [x] ")
      sub(/\*\*.*$/, "")
      print
      next
    }
    in_section && /^- \[ \] / {
      sub(/^- \[ \] /, "- [x] ")
      print
      next
    }
    { print }
  ' "$PROGRESS_FILE" > "${PROGRESS_FILE}.tmp" && mv "${PROGRESS_FILE}.tmp" "$PROGRESS_FILE"
}

case "$COMMAND" in
  start)
    AGENT="${3:?Agent name required}"
    sed -i '' "s/- \[ \] ${AGENT}/- [ ] **${AGENT}** - 진행중/" "$PROGRESS_FILE"
    update_timestamp
    echo "Progress updated: ${AGENT} started"
    ;;

  complete)
    AGENT="${3:?Agent name required}"
    OUTPUT="${4:?Output description required}"
    NEXT_AGENT="${5:-}"
    # 완료 표시
    sed -i '' "s/- \[ \] \*\*${AGENT}\*\*.*/- [x] ${AGENT} - ${OUTPUT} (${NOW})/" "$PROGRESS_FILE"
    # 다음 에이전트 진행중 표시
    if [ -n "$NEXT_AGENT" ]; then
      sed -i '' "s/- \[ \] ${NEXT_AGENT}/- [ ] **${NEXT_AGENT}** - 진행중/" "$PROGRESS_FILE"
    fi
    # 최근 작업 추가
    add_recent_work "${NOW} | ${AGENT} - ${OUTPUT}"
    update_timestamp
    echo "Progress updated: ${AGENT} completed"
    ;;

  checkpoint)
    AGENT="${3:?Agent name required}"
    PERCENT="${4:?Progress percentage required}"
    STATUS="${5:?Current status required}"
    sed -i '' "s/- \[ \] \*\*${AGENT}\*\*.*/- [ ] **${AGENT}** - ${PERCENT}% ${STATUS}/" "$PROGRESS_FILE"
    update_timestamp
    echo "Progress updated: ${AGENT} checkpoint ${PERCENT}%"
    ;;

  finish)
    complete_all_in_progress_section
    replace_next_session "워크플로우 완료"
    update_timestamp
    echo "Progress updated: workflow finished"
    ;;

  cancel)
    replace_next_session "사용자 취소로 중단됨"
    update_timestamp
    echo "Progress updated: workflow cancelled"
    ;;

  fail)
    AGENT="${3:?Agent name required}"
    REASON="${4:?Failure reason required}"
    # 실패 에이전트 표시
    sed -i '' "s/- \[ \] \*\*${AGENT}\*\*.*/- [ ] **${AGENT}** - 실패 (${NOW})/" "$PROGRESS_FILE"
    # 알려진 이슈에 추가
    sed -i '' "/^## 알려진 이슈/a\\
- [ ] ${AGENT} 실패 - ${REASON}" "$PROGRESS_FILE"
    # 다음 세션 지침 업데이트
    replace_next_session "${AGENT} 에이전트 실패로 중단. 수동 개입 후 재개 필요."
    update_timestamp
    echo "Progress updated: ${AGENT} failed"
    ;;

  *)
    echo "Unknown command: $COMMAND" >&2
    echo "Available: start, complete, checkpoint, finish, cancel, fail" >&2
    exit 1
    ;;
esac
