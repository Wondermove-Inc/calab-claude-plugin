---
name: toolkit:sync-jira
description: beads 이슈를 Jira 티켓으로 동기화합니다. 이슈 내용을 그대로 Jira에 생성하며, 부모 티켓 지정이 필수입니다.
allowed-tools: Bash, AskUserQuestion, mcp__atlassian__jira_create_issue, mcp__atlassian__jira_get_issue, mcp__atlassian__jira_search
disable-model-invocation: true
argument-hint: <beads-issue-id>
---

# /sync-jira - beads 이슈를 Jira로 동기화

## 설명

beads에서 관리하는 로컬 이슈를 Jira 티켓으로 동기화합니다.
이슈의 제목, 설명, 타입, 우선순위를 그대로 Jira에 반영하며, Jira 부모 티켓은 항상 사용자에게 확인합니다.

## 전제 조건

- Atlassian MCP 서버가 설치 및 연결되어 있어야 합니다
- Jira 프로젝트에 대한 접근 권한이 있어야 합니다

## 사용법

```bash
/toolkit:sync-jira <beads-issue-id>       # 단일 이슈 동기화
/toolkit:sync-jira <id1> <id2> <id3>      # 복수 이슈 동기화
```

> **참고**: beads 이슈 번호를 입력하지 않으면 사용자에게 반드시 질문하여 받습니다.

## 실행 절차

### Step 1: beads 이슈 번호 확인 (필수)

인자로 beads 이슈 번호가 전달되지 않았으면, **반드시** 사용자에게 질문하여 받습니다.
이 단계를 건너뛰지 않습니다. 임의로 추측하거나 자동 선택하지 않습니다.

### Step 2: Jira 부모 티켓 확인 (필수)

사용자에게 Jira 부모 티켓 정보를 **반드시** 질문합니다.

**질문 내용:**
- Jira 부모 티켓 키 (예: `PROJ-123`) 또는 Jira 티켓 URL
- 보고자 (Reporter): 기본값은 Jira 인증 사용자. 변경이 필요하면 이름을 입력

인자로 전달되지 않았으면 반드시 사용자에게 질문하여 받습니다.
이 단계를 건너뛰지 않습니다.

**기본 보고자 확인 방법:**
부모 티켓 조회(`mcp__atlassian__jira_get_issue`) 시 응답의 `reporter` 필드에서 현재 인증 사용자 정보를 참조하거나, 사용자가 별도 지정하지 않으면 Jira API의 인증 계정이 자동으로 보고자가 됩니다.

### Step 3: beads 이슈 조회

```bash
bd show <issue-id> --json
```

JSON 출력에서 다음 필드를 추출합니다:

| beads 필드 | 용도 |
|-----------|------|
| `id` | 동기화 추적용 |
| `title` | Jira 이슈 제목 |
| `description` | Jira 이슈 설명 |
| `issue_type` | Jira 이슈 타입 매핑 |
| `priority` | Jira 우선순위 매핑 |
| `status` | Jira 상태 매핑 |
| `labels` | Jira 라벨 |

**보고자(Reporter) 설정:**

Step 2에서 부모 티켓 확인 시, 보고자도 함께 질문합니다.
기본값은 Jira 인증 사용자(API 토큰 소유자)이며, 사용자가 별도 지정할 수 있습니다.

### Step 4: 필드 매핑

#### 이슈 타입 매핑

| beads type | Jira type |
|-----------|-----------|
| `epic` | Epic |
| `task` | Task |
| `bug` | Bug |
| `story` | Story |

#### 우선순위 매핑

| beads priority | Jira priority |
|---------------|---------------|
| 0 (P0) | Highest |
| 1 (P1) | High |
| 2 (P2) | Medium |
| 3 (P3) | Low |

#### 상태 매핑

| beads status | Jira status |
|-------------|-------------|
| `open` | To Do |
| `in_progress` | In Progress |
| `closed` | Done |

### Step 5: 사용자 확인

동기화 전에 매핑 결과를 사용자에게 보여주고 확인을 받습니다.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Jira 동기화 미리보기
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 beads ID:     {beads-id}
 부모 티켓:     {PROJ-123}
 제목:         {title}
 타입:         {issue_type} → {jira_type}
 우선순위:      P{n} → {jira_priority}
 라벨:         {labels}
 보고자:       {reporter}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 설명 미리보기:
 {description 첫 5줄}
 ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

사용자가 승인하면 다음 단계로 진행합니다.

### Step 6: Jira 이슈 생성

Atlassian MCP의 Jira 도구를 사용하여 이슈를 생성합니다.

**생성 시 포함할 정보:**
- **프로젝트**: 부모 티켓에서 추출한 프로젝트 키
- **부모 티켓**: Step 2에서 받은 부모 티켓 키
- **제목**: beads 이슈 제목
- **설명**: beads 이슈 설명 (Atlassian MCP가 마크다운을 ADF로 자동 변환)
- **이슈 타입**: 매핑된 Jira 타입
- **우선순위**: 매핑된 Jira 우선순위
- **라벨**: beads 라벨
- **보고자**: Step 2에서 확인한 보고자 (기본값: Jira 인증 사용자)

### Step 7: 완료 보고

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Jira 동기화 완료
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 beads ID:     {beads-id}
 Jira 티켓:    {PROJ-456}
 부모 티켓:    {PROJ-123}
 URL:          {jira-url}
 상태:         생성 완료
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 복수 이슈 동기화 시 결과 요약

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Jira 동기화 결과 요약
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 총 이슈:     {n}건
 성공:        {n}건
 실패:        {n}건

 | beads ID | Jira 티켓 | 제목 | 상태 |
 |----------|----------|------|------|
 | {id1}    | PROJ-456 | ... | 성공 |
 | {id2}    | PROJ-457 | ... | 성공 |
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 주의사항

- Jira 부모 티켓은 항상 사용자에게 확인합니다 (생략 불가)
- beads 이슈의 description(마크다운)은 Atlassian MCP를 통해 Jira ADF 형식으로 변환되어 전달됩니다
- Atlassian MCP가 연결되어 있지 않으면 에러 메시지를 표시합니다

## Troubleshooting

| 문제 | 원인 | 해결 방법 |
|------|------|----------|
| MCP 연결 실패 | Atlassian MCP 미설치 | Atlassian MCP 서버 설치 및 설정 확인 |
| 권한 오류 | Jira 접근 권한 부족 | Jira API 토큰 및 프로젝트 권한 확인 |
| 부모 티켓 없음 | 잘못된 티켓 키 입력 | 티켓 키 형식(PROJ-123) 재확인 |
| 타입 매핑 실패 | Jira 프로젝트에 해당 타입 없음 | 프로젝트 이슈 타입 설정 확인 |
