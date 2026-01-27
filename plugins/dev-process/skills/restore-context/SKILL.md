---
name: workflow:restore-context
description: 핵심 규칙과 현재 작업 상태를 복원합니다. Compact 후, 세션 시작 시, 맥락을 잃었을 때 사용하세요.
allowed-tools: Read
user-invocable: true
---
# 컨텍스트 복원

## 실행 순서

### Phase 1: 핵심 규칙 및 컨텍스트 (필수)

다음 파일들을 **반드시** 읽으세요:

| 파일 | 설명 | 중요도 |
|------|------|--------|
| `.claude/memory/PROJECT_RULES.md` | 프로젝트 규칙 | 🔴 필수 |
| `.claude/memory/CURRENT_CONTEXT.md` | 현재 작업 상태 | 🔴 필수 |
| `.claude/memory/WORK_HISTORY.md` | 작업 히스토리 | 🟡 권장 |

### Phase 2: 런타임 상태 (.claude-state/) (필수)

다음 파일들이 존재하면 **모두** 읽으세요:

| 파일 | 설명 | 복원 시 활용 |
|------|------|-------------|
| `checkpoint.json` | 마지막 체크포인트 | 마지막 저장 시점 확인 |
| `checkpoint_history.json` | 체크포인트 히스토리 | 작업 흐름 파악 |
| `worktree.json` | 작업 트리 상태 | 태스크 진행률 확인 |
| `recent_changes.json` | 최근 변경 파일 이력 | 어떤 파일 작업했는지 파악 |
| `prompt_history.json` | 프롬프트 히스토리 | 사용자 의도 흐름 파악 |
| `session_stats.json` | 세션 통계 | 작업량 파악 |
| `quality_violations.json` | 품질 위반 기록 | 미해결 이슈 확인 |

### Phase 3: 선택적 로그 확인

필요시 확인:

| 파일 | 언제 확인 |
|------|----------|
| `activity.log` | 최근 활동 흐름 파악 필요 시 |
| `notifications.log` | 알림 히스토리 필요 시 |
| `subagent.log` | 서브에이전트 사용 이력 필요 시 |


## 복원 우선순위

1. **필수**: PROJECT_RULES.md, CURRENT_CONTEXT.md
2. **높음**: checkpoint.json, worktree.json, recent_changes.json
3. **중간**: prompt_history.json, session_stats.json, quality_violations.json
4. **낮음**: 로그 파일들
