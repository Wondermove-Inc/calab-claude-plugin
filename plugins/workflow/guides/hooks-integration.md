# Hooks 통합 가이드

> workflow 플러그인의 TDD/리뷰 규칙을 `settings.json` hooks로 **강제**하는 예시입니다. 프롬프트만으로는 우회 가능하지만, hook은 Claude Code 하네스 레벨에서 차단합니다.

## 1. 왜 hook인가

| 강제 수단 | 우회 가능성 | 효과 |
|-----------|------------|------|
| 프롬프트 선언 ("반드시 TDD") | 높음 (합리화로 스킵) | 권고 수준 |
| `allowed-tools` 제한 | 중간 (도구 조합 우회 가능) | 중간 |
| **Hook (exit code 2)** | 낮음 | 블로킹 강제 |

workflow 플러그인은 기본적으로 hook을 포함하지 **않습니다**. 이 가이드는 필요한 사용자가 직접 `settings.json`에 추가할 수 있도록 예시를 제공합니다.

## 2. 권장 hook 구성

### 2-1. TaskCompleted: worker 보고 전 테스트 재실행

```json
{
  "hooks": {
    "TaskCompleted": [
      {
        "matcher": "worker",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/verify-worker-task.sh"
          }
        ]
      }
    ]
  }
}
```

`.claude/hooks/verify-worker-task.sh`:
```bash
#!/usr/bin/env bash
# worker 완료 시점에 테스트/빌드를 재실행하여 보고의 진위 검증
set -e
cd "$(git rev-parse --show-toplevel)"

# 프로젝트 빌드/테스트 명령 (예: Go)
if go test ./... -count=1 >&2; then
  exit 0
else
  cat >&2 <<'MSG'
[hook] 테스트 실패. worker 보고가 허위일 수 있습니다.
메인 Claude: worker 재호출로 재작업 요청하세요.
MSG
  exit 2
fi
```

> 다른 언어 사용 시 테스트 명령 부분만 교체 (`npm test`, `pytest`, `cargo test` 등).

### 2-2. TeammateIdle: 리뷰어가 보고 없이 idle인 경우 재요청

```json
{
  "hooks": {
    "TeammateIdle": [
      {
        "matcher": ".*-reviewer",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/check-reviewer-report.sh"
          }
        ]
      }
    ]
  }
}
```

`.claude/hooks/check-reviewer-report.sh`:
```bash
#!/usr/bin/env bash
# 리뷰 요청 후 피드백 보고 SendMessage 없이 idle로 진입했는지 감지
LAST_LOG=$(ls -t .claude/logs/*.jsonl | head -1)
if ! grep -q '"피드백 보고"' "$LAST_LOG" 2>/dev/null; then
  cat >&2 <<'MSG'
[hook] 리뷰어가 보고 없이 idle입니다. team-lead가 재요청해야 합니다.
MSG
  exit 2
fi
exit 0
```

### 2-3. PreToolUse: worker의 파일 경계 위반 차단

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/check-file-boundary.sh"
          }
        ]
      }
    ]
  }
}
```

`.claude/hooks/check-file-boundary.sh` (개념 예시):
```bash
#!/usr/bin/env bash
# worker는 자신의 담당 경로 외 파일 수정 금지
AGENT="${CLAUDE_AGENT_NAME:-unknown}"
TARGET_FILE="$1"
BOUNDARY_FILE=".claude/boundaries/${AGENT}.txt"

if [[ -f "$BOUNDARY_FILE" ]] && ! grep -qF "$TARGET_FILE" "$BOUNDARY_FILE"; then
  echo "[hook] $AGENT는 $TARGET_FILE을 수정할 수 없습니다 (파일 경계 위반)." >&2
  exit 2
fi
exit 0
```

> 경계 파일은 discovery 단계에서 architect의 작업 분할 결과를 토대로 메인 Claude가 `.claude/boundaries/worker.txt` 형태로 자동 생성하도록 확장 가능.

### 2-4. TaskCreated: task 생성 시 beads 동기화

```json
{
  "hooks": {
    "TaskCreated": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bd comments add \"${CLAUDE_EPIC_ID:-unknown}\" \"[hook] task 생성됨: ${CLAUDE_TASK_TITLE}\""
          }
        ]
      }
    ]
  }
}
```

## 3. 적용 범위

- **프로젝트 단위**: `.claude/settings.json` (레포에 커밋하여 팀원 공유)
- **사용자 단위**: `~/.claude/settings.json` (개인 설정)

## 4. 주의

- Hook 실패는 메인 Claude에 피드백으로 전달됩니다. 해석·조치는 메인 Claude가 수행합니다.
- `exit 2` 대신 `exit 1`을 사용하면 경고만 출력되고 차단되지 않습니다.
- hook 스크립트는 레포에 커밋하지 않으려면 `.gitignore`에 추가하거나 `~/.claude/hooks/`에 배치.

## 5. 참조

- Claude Code Hooks 공식 문서: `https://code.claude.com/docs/en/hooks`
- Hook 종류 (`TeammateIdle`, `TaskCreated`, `TaskCompleted` 등): `https://code.claude.com/docs/en/agent-teams#enforce-quality-gates-with-hooks`
