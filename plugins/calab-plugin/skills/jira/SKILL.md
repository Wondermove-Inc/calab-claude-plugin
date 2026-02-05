---
name: jira
description: |
  JIRA 연동. 이슈 생성, 상태 업데이트, 동기화를 수행합니다.
argument-hint: "[--sync|--create|--update|--link] [이슈키]"
allowed-tools: [Read, Write, Grep, Glob, Bash, Task, mcp__claude_ai_Atlassian__getJiraIssue, mcp__claude_ai_Atlassian__createJiraIssue, mcp__claude_ai_Atlassian__editJiraIssue, mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql, mcp__claude_ai_Atlassian__transitionJiraIssue, mcp__claude_ai_Atlassian__addCommentToJiraIssue]
skills: [project-rules, clarification-protocol, skill-completion-rules]
agents:
  primary: jira-connector
  orchestration:
    sync: [calab-plugin:jira-connector]
    create: [calab-plugin:jira-connector]
    update: [calab-plugin:jira-connector]
    link: [calab-plugin:jira-connector]
hooks:
  Stop:
    - hooks:
        - type: command
          command: "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/post_skill_artifact_check.py\""
          once: true
---

# /jira - JIRA 연동

> **이슈 생성, 상태 업데이트, 양방향 동기화**

---

## 사용법

```bash
/jira [이슈키]              # 이슈 정보 조회
/jira --sync                # worktree와 JIRA 동기화
/jira --create [제목]       # 새 이슈 생성
/jira --update [이슈키]     # 이슈 상태 업데이트
/jira --link [이슈키]       # 현재 작업과 이슈 연결
```

---

## 에이전트 호출 (필수)

> **이 스킬이 로드되면 아래 지침을 따라 Task 도구를 호출하세요.**

```python
Task(
    subagent_type="calab-plugin:jira-connector",
    description="JIRA 연동",
    prompt="""
[Role] JIRA 연동 전문가
[Goal] {작업} 수행
[Scope] {이슈키 또는 동기화 범위}

## 작업 유형
- sync: worktree.json ↔ JIRA 양방향 동기화
- create: 새 이슈 생성
- update: 상태 전환 (To Do → In Progress → Done)
- link: Git 브랜치/커밋과 이슈 연결

[Output] 작업 결과 요약
"""
)
```

---

## 동기화 흐름

```
.claude-state/worktree.json
         ↕ 양방향 동기화
      JIRA Issues
```

### 상태 매핑

| Worktree | JIRA |
|----------|------|
| pending | To Do |
| in_progress | In Progress |
| done | Done |

---

## 옵션별 동작

| 옵션 | 동작 |
|------|------|
| `--sync` | 모든 Task 상태 동기화 |
| `--create` | 새 이슈 생성 + worktree 연결 |
| `--update` | 특정 이슈 상태 변경 |
| `--link` | 현재 브랜치와 이슈 연결 |

---

## 산출물

| 산출물 | 필수 |
|--------|------|
| 동기화 결과 로그 | Yes |
| worktree.json 업데이트 | 조건부 |

---

## 다음 단계 선택 (필수)

| 완료 후 | 권장 |
|--------|------|
| 이슈 생성 | `/dev --build` 구현 시작 |
| 동기화 완료 | 작업 진행 확인 |

> **⚠️ 작업 완료 후 반드시 AskUserQuestion 호출**
>
> JIRA 작업이 완료되면 현재 상황을 분석하여 AskUserQuestion으로 다음 단계 선택지를 제시하세요.
