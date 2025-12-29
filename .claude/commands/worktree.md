---
description: 작업 트리를 관리합니다. 태스크 시작, 진행, 완료를 실시간 추적합니다. 작업 상태, 진행률 확인에 사용합니다.
allowed-tools: Read, Write, Edit
argument-hint: [status | start <id> | done <id> | block <id> <reason>]
---

# /worktree - 작업 트리 관리

## 설명

현재 개발 중인 작업의 전체 트리를 표시하고 관리합니다.
작업 시작, 진행, 완료를 실시간으로 추적합니다.

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
 • docs/architecture/api-spec.md
 • .claude/best-practices/nodejs.md

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

1. `/dev-tasks` 실행 시 → `worktree.json` 자동 생성
2. `/dev build` 실행 시 → 해당 태스크 자동 시작
3. 태스크 완료 감지 시 → 자동으로 done 처리

## 참조

- `.claude/skills/work-tracker/SKILL.md`
- `.claude-state/worktree.json`
- `docs/tasks/{feature}/tasks.md`
