---
description: 작업 트리를 관리합니다. 태스크 시작, 진행, 완료를 실시간 추적합니다. 작업 상태, 진행률 확인에 사용합니다.
allowed-tools: Read, Write, Edit
argument-hint: [status | start <id> | done <id> | block <id> <reason>]
---

# /worktree - 작업 트리 관리

## 설명

현재 개발 중인 작업의 전체 트리를 표시하고 관리합니다.
작업 시작, 진행, 완료를 실시간으로 추적합니다.

## 폴더 구조

```
.claude/docs/
├── active/                          ← 진행 중인 기능
│   └── {feature-name}/
│       ├── 01-brainstorm.md
│       ├── 02-prd.md
│       ├── 03-architecture.md
│       ├── 04-erd.md
│       ├── 05-tasks.md
│       └── qa/
│
└── complete/                        ← 모든 태스크 완료 시 자동 이동
    └── {feature-name}/              ← active에서 이동됨
        ├── 01-brainstorm.md
        ├── 02-prd.md
        ├── 03-architecture.md
        ├── 04-erd.md
        ├── 05-tasks.md
        └── qa/
```

**자동 이동 조건:**
- 모든 태스크가 `done` 상태일 때
- `/worktree done` 명령으로 마지막 태스크 완료 시 자동 실행

## 사용법

```bash
/worktree                    # 현재 작업 트리 표시
/worktree status             # 상태 요약
/worktree start TASK-001     # 태스크 시작
/worktree done TASK-001      # 태스크 완료
/worktree block TASK-001 "사유"  # 블로커 등록
/worktree reset              # 트리 초기화
```

## 실행 절차

### 기본 모드: 작업 트리 표시

**Step 1**: `.claude-state/worktree.json` 읽기

**Step 2**: 트리 구조로 출력

```
============================================
 WORKTREE: 사용자 인증 시스템
============================================

 진행률: ████████░░░░░░░░░░░░ 40% (4/10)

┌─ Epic 1: 사용자 인증
│
├─┬─ Story 1.1: 회원가입
│ │
│ ├── ✅ TASK-001: User 테이블 마이그레이션
│ ├── ✅ TASK-002: RegisterDto 정의
│ ├── 🔄 TASK-003: AuthService.register() 구현  ← 현재 작업
│ ├── ⬚ TASK-004: AuthController 구현
│ └── ⬚ TASK-005: 회원가입 폼 컴포넌트
│
├─┬─ Story 1.2: 로그인
│ │
│ ├── ⬚ TASK-006: LoginDto 정의
│ ├── ⬚ TASK-007: AuthService.login() 구현
│ └── ⬚ TASK-008: 로그인 폼 컴포넌트
│
└─┬─ Story 1.3: 로그아웃
  │
  ├── ⬚ TASK-009: 로그아웃 로직
  └── ⬚ TASK-010: 세션 정리

============================================
 상태 범례: ✅ 완료 | 🔄 진행중 | 🚫 블로커 | ⬚ 대기
============================================
 현재 작업: TASK-003 AuthService.register() 구현
 예상 다음: TASK-004 AuthController 구현
============================================
```

### start 모드: 태스크 시작

```bash
/worktree start TASK-003
```

**동작**:
1. `worktree.json`에서 TASK-003 상태를 `in_progress`로 변경
2. 현재 작업(`current_task`)을 TASK-003으로 설정
3. 시작 시간 기록
4. CURRENT_CONTEXT.md 업데이트

**출력**:
```
============================================
🔄 태스크 시작: TASK-003
============================================

 태스크: AuthService.register() 구현
 우선순위: P0 (Critical)
 의존성: TASK-002 ✅

 Acceptance Criteria:
 - [ ] register() 메서드 구현
 - [ ] 이메일 중복 검사
 - [ ] 비밀번호 해싱
 - [ ] 사용자 생성 및 저장

 참조:
 • .claude/docs/active/{feature}/03-architecture.md
 • best-practices/nodejs.md

============================================
```

### done 모드: 태스크 완료

```bash
/worktree done TASK-003
```

**동작**:
1. TASK-003 상태를 `done`으로 변경
2. 완료 시간 기록
3. 다음 태스크로 `current_task` 이동
4. 진행률 업데이트
5. CURRENT_CONTEXT.md 업데이트
6. **모든 태스크 완료 시**: 기능 폴더를 `active/` → `complete/`로 이동

**출력**:
```
============================================
✅ 태스크 완료: TASK-003
============================================

 완료: AuthService.register() 구현
 소요 시간: 45분

 진행률 업데이트:
 이전: ████████░░░░░░░░░░░░ 30% (3/10)
 현재: ██████████░░░░░░░░░░ 40% (4/10)

 다음 태스크: TASK-004 AuthController 구현
 자동 시작할까요? (Y/n)

============================================
```

### 🎉 모든 태스크 완료 시: 자동 아카이브

마지막 태스크가 완료되면 자동으로 기능 폴더를 `complete/`로 이동:

```bash
/worktree done TASK-010  # 마지막 태스크
```

**자동 동작**:
1. 모든 태스크 `done` 상태 확인
2. 기능 폴더 이동:
   ```
   .claude/docs/active/{feature-name}/
   → .claude/docs/complete/{feature-name}/
   ```
3. worktree.json 업데이트 (status: "completed")
4. CURRENT_CONTEXT.md 초기화

**출력**:
```
============================================
🎉 기능 개발 완료: {feature-name}
============================================

 모든 태스크 완료!

 진행률: ████████████████████ 100% (10/10)

 📁 아카이브 완료:
 FROM: .claude/docs/active/{feature-name}/
 TO:   .claude/docs/complete/{feature-name}/

 생성된 문서:
 • 01-brainstorm.md
 • 02-prd.md
 • 03-architecture.md
 • 04-erd.md
 • 05-tasks.md
 • qa/

 다음 단계:
 • /workflow:process-plan [새 기능] - 새로운 기능 개발 시작
 • /qa - QA 진행 (선택)

============================================
```

### block 모드: 블로커 등록

```bash
/worktree block TASK-004 "외부 API 인증 키 대기 중"
```

**출력**:
```
============================================
🚫 블로커 등록: TASK-004
============================================

 태스크: AuthController 구현
 블로커: 외부 API 인증 키 대기 중
 등록 시간: 2024-01-15 14:30

 대체 작업 추천:
 • TASK-005: 회원가입 폼 컴포넌트 (의존성 없음)
 • TASK-006: LoginDto 정의 (의존성 없음)

============================================
```

### status 모드: 상태 요약

```bash
/worktree status
```

**출력**:
```
============================================
 WORKTREE STATUS
============================================

 프로젝트: 사용자 인증 시스템
 시작일: 2024-01-15

 진행률: ████████░░░░░░░░░░░░ 40%

 ┌──────────────────────────────────┐
 │ 완료    │ ████████     │ 4개    │
 │ 진행중  │ ██           │ 1개    │
 │ 블로커  │              │ 0개    │
 │ 대기    │ ██████████   │ 5개    │
 └──────────────────────────────────┘

 오늘 완료: 2개
 예상 남은 작업: 6개

============================================
```

## worktree.json 구조

```json
{
  "project": "사용자 인증 시스템",
  "feature_folder": ".claude/docs/active/user-auth/",
  "status": "in_progress",
  "created_at": "2024-01-15T09:00:00Z",
  "updated_at": "2024-01-15T14:30:00Z",
  "current_task": "TASK-003",
  "progress": {
    "total": 10,
    "done": 4,
    "in_progress": 1,
    "blocked": 0,
    "pending": 5,
    "percentage": 40
  },
  "epics": [
    {
      "id": "EPIC-1",
      "name": "사용자 인증",
      "stories": [
        {
          "id": "STORY-1.1",
          "name": "회원가입",
          "tasks": [
            {
              "id": "TASK-001",
              "name": "User 테이블 마이그레이션",
              "priority": "P0",
              "status": "done",
              "dependencies": [],
              "started_at": "2024-01-15T09:00:00Z",
              "completed_at": "2024-01-15T09:30:00Z"
            },
            {
              "id": "TASK-002",
              "name": "RegisterDto 정의",
              "priority": "P0",
              "status": "done",
              "dependencies": ["TASK-001"],
              "started_at": "2024-01-15T09:30:00Z",
              "completed_at": "2024-01-15T10:00:00Z"
            },
            {
              "id": "TASK-003",
              "name": "AuthService.register() 구현",
              "priority": "P0",
              "status": "in_progress",
              "dependencies": ["TASK-002"],
              "started_at": "2024-01-15T10:00:00Z",
              "acceptance_criteria": [
                "register() 메서드 구현",
                "이메일 중복 검사",
                "비밀번호 해싱",
                "사용자 생성 및 저장"
              ]
            }
          ]
        }
      ]
    }
  ],
  "blockers": [],
  "daily_log": [
    {
      "date": "2024-01-15",
      "completed": ["TASK-001", "TASK-002"],
      "started": ["TASK-003"]
    }
  ]
}
```

## work-tracker 스킬 연동

work-tracker 스킬이 다음 키워드 감지 시 자동으로 worktree 업데이트:

| 키워드 | 동작 |
|--------|------|
| "TASK-XXX 시작", "XXX 작업 시작" | worktree start |
| "TASK-XXX 완료", "XXX 구현 완료" | worktree done |
| "막혔다", "블로커", "대기 중" | worktree block |

## 자동 동기화

1. `/workflow:process-tasks` 실행 시 → `worktree.json` 자동 생성
2. `/workflow:process-build` 실행 시 → 해당 태스크 자동 시작
3. 태스크 완료 감지 시 → 자동으로 done 처리

## JIRA 연동

JIRA 연동이 활성화된 경우, Worktree 변경 시 JIRA에 자동 동기화됩니다.

### 자동 동기화 트리거

| Worktree 명령 | JIRA 동작 |
|--------------|-----------|
| `/worktree start TASK-001` | JIRA 이슈 → In Progress |
| `/worktree done TASK-001` | JIRA 이슈 → Done |
| `/worktree block TASK-001` | JIRA 이슈 → Blocked + 코멘트 |

### 설정

```json
// integrations/jira_config.json
{
  "jira": {
    "auto_sync": {
      "enabled": true,
      "on_task_start": true,
      "on_task_done": true,
      "on_blocker": true
    }
  }
}
```

### 연계 명령어

| 명령어 | 설명 |
|--------|------|
| `/jira-init` | JIRA 연동 초기화 |
| `/jira-push` | Worktree → JIRA |
| `/jira-pull` | JIRA → Worktree |
| `/jira-sync` | 양방향 동기화 |
| `/jira-status` | 연동 상태 확인 |

자세한 내용: jira 플러그인의 `skills/jira-integration/SKILL.md` 참조

## 참조

- `skills/work-tracker/SKILL.md` (workflow)
- jira 플러그인의 `skills/jira-integration/SKILL.md`
- `.claude-state/worktree.json`
- `.claude/docs/active/{feature}/05-tasks.md`
- `.claude/docs/complete/` - 완료된 기능 폴더
