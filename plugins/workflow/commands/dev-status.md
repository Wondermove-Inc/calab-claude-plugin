---
description: 개발 워크플로우 진행 상황을 확인합니다. 현재 단계, 완료된 문서, 태스크 상태를 보여줍니다.
allowed-tools: Read, Glob
---

# 워크플로우 상태 확인

## 목적

현재 개발 워크플로우의 진행 상황을 한눈에 파악합니다.

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
└── complete/                        ← worktree 완료 시 자동 이동
    └── {완료된-기능}/
```

## 실행 절차

### Step 1: 컨텍스트 로드

```
memory/CURRENT_CONTEXT.md 읽기
```

### Step 2: 문서 상태 확인

```
.claude/docs/active/{feature-name}/
├── 01-brainstorm.md     ← Phase 1: 브레인스토밍
├── 02-prd.md            ← Phase 2: PRD
├── 03-architecture.md   ← Phase 3: 아키텍처
├── 04-erd.md            ← Phase 3: ERD
├── 05-tasks.md          ← Phase 4: 태스크 분해
└── qa/                  ← Phase 6: QA (선택)
```

### Step 3: 상태 출력

```
============================================
 개발 워크플로우 상태
============================================

 현재 기능: {feature-name}
 작업 폴더: .claude/docs/active/{feature-name}/
 시작일: {시작일}

 워크플로우 진행 상황:

 Phase 1: Brainstorming     [완료]
 Phase 2: PRD              [완료]
 Phase 3: Design           [완료]
 Phase 4: Task Planning     [완료]
 Phase 5: Implementation    [진행 중]

 생성된 문서:
• [x] 01-brainstorm.md
• [x] 02-prd.md
• [x] 03-architecture.md
• [x] 04-erd.md
• [x] 05-tasks.md

 태스크 진행 상황:
• 총 태스크: 15개
• 완료: 8개 (53%)
• 진행 중: 2개
• 대기 중: 5개

┌──────────────────────────────────────────┐
│ ████████████████░░░░░░░░░░░░░░░  53%     │
└──────────────────────────────────────────┘

 현재 진행 중:
• TASK-009: UserProfile 컴포넌트 (80%)
• TASK-010: useProfile 훅 구현 (30%)

 다음 태스크:
• TASK-011: 프로필 수정 API
• TASK-012: 프로필 이미지 업로드

============================================

 사용 가능한 명령어:
• /dev build TASK-011  - 다음 태스크 구현
• /worktree            - 작업 트리 보기

============================================
```

### Step 4: 완료된 기능 확인

```
.claude/docs/complete/ 디렉토리에서 완료된 기능 목록 확인
```

### Step 5: 진행 중인 워크플로우 없을 경우

```
============================================
 개발 워크플로우 상태
============================================

 진행 중인 워크플로우가 없습니다.

 새 워크플로우 시작:
  /dev plan "기능 아이디어"

 완료된 기능:
• .claude/docs/complete/user-auth/
• .claude/docs/complete/payment/

 진행 중인 기능:
• (없음)

============================================
```

## 참조 파일

- `memory/CURRENT_CONTEXT.md` - 현재 컨텍스트
- `.claude-state/worktree.json` - 태스크 진행 상황
- `.claude/docs/active/` - 진행 중인 기능 폴더
- `.claude/docs/complete/` - 완료된 기능 폴더
