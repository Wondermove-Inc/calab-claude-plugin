---
name: worktree
description: |
  작업 트리를 관리합니다. 태스크 시작, 진행, 완료를 실시간 추적합니다. 작업 상태, 진행률 확인에 사용합니다.
  USE WHEN: 작업 트리, worktree, 태스크 상태, task status, 진행률, progress,
  뭐 남았어, 얼마나 했어, 진행 상황, 현황,
  태스크, task, 시작, start, 완료, done, complete,
  블로킹, blocking, 차단,
  몇 퍼센트, 몇개 남았어, 다음 작업
argument-hint: "[status | start <id> | done <id> | block <id> <reason>]"
allowed-tools: [Read, Write, Edit]
---

# /worktree - 작업 트리 관리

> **태스크 진행 상태 추적 및 관리**

## 사용법

```bash
/worktree                    # 현재 작업 트리 표시
/worktree status             # 상태 요약
/worktree start TASK-001     # 태스크 시작
/worktree done TASK-001      # 태스크 완료
/worktree block TASK-001 "사유"  # 블로커 등록
/worktree reset              # 트리 초기화
```

## 폴더 구조

```
.claude/docs/
├── active/                          # 진행 중인 기능
│   └── {feature-name}/
│       ├── 01-brainstorm.md
│       ├── 02-prd.md
│       ├── 03-architecture.md
│       ├── 04-erd.md
│       ├── 05-tasks.md
│       └── qa/
│
└── complete/                        # 모든 태스크 완료 시 자동 이동
    └── {feature-name}/
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
└─┬─ Story 1.2: 로그인
  │
  ├── ⬚ TASK-006: LoginDto 정의
  └── ⬚ TASK-007: AuthService.login() 구현

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

### done 모드: 태스크 완료

```bash
/worktree done TASK-003
```

**동작**:
1. TASK-003 상태를 `done`으로 변경
2. 완료 시간 기록
3. 다음 태스크로 `current_task` 이동
4. 진행률 업데이트
5. **모든 태스크 완료 시**: 기능 폴더를 `active/` → `complete/`로 이동

### block 모드: 블로커 등록

```bash
/worktree block TASK-004 "외부 API 인증 키 대기 중"
```

### status 모드: 상태 요약

```bash
/worktree status
```

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

============================================
```

## worktree.json 구조

```json
{
  "project": "사용자 인증 시스템",
  "feature_folder": ".claude/docs/active/user-auth/",
  "status": "in_progress",
  "current_task": "TASK-003",
  "progress": {
    "total": 10,
    "done": 4,
    "in_progress": 1,
    "blocked": 0,
    "pending": 5,
    "percentage": 40
  },
  "epics": [...]
}
```

## JIRA 연동

JIRA 연동이 활성화된 경우, Worktree 변경 시 JIRA에 자동 동기화됩니다.

| Worktree 명령 | JIRA 동작 |
|--------------|-----------|
| `/worktree start TASK-001` | JIRA 이슈 → In Progress |
| `/worktree done TASK-001` | JIRA 이슈 → Done |
| `/worktree block TASK-001` | JIRA 이슈 → Blocked + 코멘트 |

## 참조

- `skills/work-tracker/SKILL.md`
- `skills/jira-integration/SKILL.md`
- `.claude-state/worktree.json`
