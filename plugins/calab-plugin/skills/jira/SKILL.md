---
name: jira
description: |
  JIRA 연동 기능을 제공합니다. Worktree와 JIRA 간 양방향 동기화를 지원합니다.
  USE WHEN: JIRA, jira, 지라, 이슈, issue, 티켓, ticket,
  동기화, sync, synchronize, 연동, connect, integration,
  프로젝트 관리, project management,
  스프린트, sprint, 백로그, backlog,
  에픽, epic, 스토리, story, 태스크, task, 서브태스크, subtask,
  할당, assign, 담당자, assignee,
  상태, status, 진행, progress, 완료, done,
  Atlassian, Confluence
argument-hint: "[--init|--pull|--push|--link|--status|--sync]"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
agent: jira-connector
agents:
  primary: jira-connector
  orchestration:
    init: [jira-connector]
    pull: [jira-connector, Explore]
    push: [jira-connector]
    sync: [jira-connector, Explore]
    status: [jira-connector]
---

# /jira - JIRA 연동

> **Worktree ↔ JIRA 양방향 동기화**

## 사용법

```bash
/jira                      # 양방향 동기화 (기본)
/jira --init               # 초기 설정
/jira --pull               # JIRA → Worktree 동기화
/jira --push               # Worktree → JIRA 동기화
/jira --link TASK-001 AUTH-102  # 수동 매핑
/jira --status             # 연동 상태 확인
/jira --sync               # 양방향 동기화
/jira --help               # 도움말
```

## 🤖 에이전트 호출 (필수)

> **이 스킬은 반드시 jira-connector 에이전트를 통해 실행해야 합니다.**

### --init 단계

```
Task(
  subagent_type="calab-plugin:jira-connector",
  description="JIRA 연동 초기 설정",
  prompt="""
  **역할**: JIRA 연동 전문가

  **목표**: JIRA 연결 설정 및 초기화

  **수행 단계**:
  1. 환경 변수 확인 (JIRA_EMAIL, JIRA_API_TOKEN)
  2. jira_config.json 생성
  3. 연결 테스트 실행
  4. 프로젝트 키 확인

  **산출물**:
  - .claude/jira_config.json
  - .claude/jira_mapping.json (초기)

  **제약 조건**:
  - ❌ API 토큰 로그 출력 금지
  - ✅ 연결 실패 시 명확한 오류 메시지
  """
)
```

### --pull / --push / --sync 단계

```
Task(
  subagent_type="calab-plugin:jira-connector",
  description="JIRA {pull|push|sync} 동기화",
  prompt="""
  **역할**: JIRA 동기화 전문가

  **목표**: {--pull: JIRA→Worktree | --push: Worktree→JIRA | --sync: 양방향}

  **동기화 항목**:
  - 이슈 상태 (To Do ↔ pending, In Progress ↔ in_progress, Done ↔ done)
  - 이슈 제목/설명
  - 담당자
  - 코멘트

  **충돌 해결**:
  - --prefer-jira: JIRA 우선
  - --prefer-worktree: Worktree 우선
  - 기본: 최신 타임스탬프 우선

  **출력 형식**:
  | Worktree | JIRA | 방향 | 상태 |
  |----------|------|------|------|
  """
)
```

### --status 단계

```
Task(
  subagent_type="calab-plugin:jira-connector",
  description="JIRA 연동 상태 확인",
  prompt="""
  **역할**: 연동 상태 분석가

  **목표**: 현재 JIRA 연동 상태 보고

  **확인 항목**:
  - 연결 상태 (성공/실패)
  - 매핑된 이슈 수
  - 마지막 동기화 시간
  - 동기화 대기 중인 항목

  **출력 형식**:
  연결 상태: ✅ 연결됨
  프로젝트: AUTH
  매핑: 12개 이슈
  마지막 동기화: 2025-01-28 10:00
  """
)
```

---

## 인자 파싱

입력: $ARGUMENTS

### 옵션별 라우팅

1. **`--help` 또는 `-h`** → 도움말 출력

2. **`--init`** → `references/init.md` 실행
   - 환경 변수 확인 (JIRA_EMAIL, JIRA_API_TOKEN)
   - jira_config.json 생성
   - 연결 테스트

3. **`--pull`** → `references/pull.md` 실행
   - JIRA 이슈 상태 조회
   - Worktree 상태 업데이트
   - `--force` 전체 강제 동기화

4. **`--push`** → `references/push.md` 실행
   - Worktree → JIRA 이슈 생성/업데이트
   - Epic-Story-Task 계층 유지
   - `--dry-run` 미리보기

5. **`--link [TASK-ID] [JIRA-KEY]`** → `references/link.md` 실행
   - 수동 매핑 생성
   - `--list` 매핑 목록
   - `--unlink` 연결 해제

6. **`--status`** → `references/status.md` 실행
   - 연결 상태 확인
   - 매핑 통계
   - `--detailed` 상세 정보

7. **`--sync` 또는 옵션 없음** → `references/sync.md` 실행
   - 양방향 동기화
   - 충돌 감지 및 해결
   - `--prefer-jira` JIRA 우선
   - `--prefer-worktree` Worktree 우선

## 설정 파일

### jira_config.json
```json
{
  "jira": {
    "enabled": true,
    "base_url": "https://company.atlassian.net",
    "project_key": "AUTH",
    "auto_sync": {
      "on_task_start": true,
      "on_task_done": true,
      "on_blocker": true
    }
  }
}
```

### jira_mapping.json
```json
{
  "project_key": "AUTH",
  "base_url": "https://company.atlassian.net",
  "mappings": {
    "TASK-001": "AUTH-102",
    "TASK-002": "AUTH-103"
  },
  "reverse_mappings": {
    "AUTH-102": "TASK-001",
    "AUTH-103": "TASK-002"
  },
  "last_sync": "2025-01-15T10:00:00Z"
}
```

## 환경 변수

```bash
# 필수
export JIRA_EMAIL="your-email@company.com"
export JIRA_API_TOKEN="your-api-token"

# API 토큰 생성:
# https://id.atlassian.com/manage-profile/security/api-tokens
```

## 동기화 흐름

```
┌─────────────────────────────────────────┐
│            /jira 동기화 흐름              │
├─────────────────────────────────────────┤
│                                         │
│   Worktree              JIRA            │
│   ┌───────┐            ┌───────┐       │
│   │TASK-001│◄──────────│AUTH-102│       │
│   │TASK-002│───────────►AUTH-103│       │
│   │TASK-003│◄─────────►│AUTH-104│       │
│   └───────┘   양방향    └───────┘       │
│                                         │
│   /jira --push: Worktree → JIRA        │
│   /jira --pull: JIRA → Worktree        │
│   /jira --sync: 양방향                  │
│                                         │
└─────────────────────────────────────────┘
```

## 상태 매핑

| Worktree | JIRA |
|----------|------|
| pending | To Do |
| in_progress | In Progress |
| done | Done |
| blocked | Blocked (+ 코멘트) |

## 레거시 명령어 호환

| 이전 명령어 | 신규 명령어 |
|------------|------------|
| `/jira-init` | `/jira --init` |
| `/jira-pull` | `/jira --pull` |
| `/jira-push` | `/jira --push` |
| `/jira-link` | `/jira --link` |
| `/jira-status` | `/jira --status` |
| `/jira-sync` | `/jira` 또는 `/jira --sync` |

## 워크플로우

```
1. /jira --init           # 초기 설정
      ↓
2. /jira --push           # 첫 동기화 (Worktree → JIRA)
      ↓
3. /jira --sync           # 이후 양방향 동기화
      ↓
4. /jira --status         # 상태 확인
```

## 자동 동기화

`auto_sync` 설정 시 자동 동작:

| Worktree 이벤트 | JIRA 동작 |
|----------------|-----------|
| `/worktree start TASK-001` | JIRA 이슈 → In Progress |
| `/worktree done TASK-001` | JIRA 이슈 → Done |
| `/worktree block TASK-001` | JIRA 이슈 → Blocked + 코멘트 |

## 다음 단계

| 상황 | 권장 명령어 |
|------|------------|
| 처음 사용 | `/jira --init` |
| JIRA에 새 이슈 생성 | `/jira --push` |
| JIRA 변경 가져오기 | `/jira --pull` |
| 정기 동기화 | `/jira --sync` |
| 상태 확인 | `/jira --status` |
