---
description: 개발 워크플로우 진행 상황을 확인합니다. 현재 단계, 완료된 문서, 태스크 상태를 보여줍니다.
allowed-tools: Read, Glob
---

# 워크플로우 상태 확인

## 목적

현재 개발 워크플로우의 진행 상황을 한눈에 파악합니다.

## 실행 절차

### Step 1: 컨텍스트 로드

```
.claude/memory/CURRENT_CONTEXT.md 읽기
```

### Step 2: 문서 상태 확인

```
docs/prd/{feature}/ - brainstorm.md, prd.md
docs/architecture/ - system-architecture.md, erd.md, api-spec.md
docs/tasks/{feature}/ - tasks.md, progress.md
```

### Step 3: 상태 출력

```
============================================
 개발 워크플로우 상태
============================================

 현재 기능: {feature-name}
 시작일: {시작일}

 워크플로우 진행 상황:

 Phase 1: Brainstorming     [완료]
 Phase 2: PRD              [완료]
 Phase 3: Architecture      [완료]
 Phase 4: Task Planning     [완료]
 Phase 5: Implementation    [진행 중]

 생성된 문서:
• [x] docs/prd/{feature}/brainstorm.md
• [x] docs/prd/{feature}/prd.md
• [x] docs/architecture/system-architecture.md
• [x] docs/architecture/erd.md
• [x] docs/architecture/api-spec.md
• [x] docs/tasks/{feature}/tasks.md

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
• /dev-implement TASK-011  - 다음 태스크 구현
• /dev-tasks              - 태스크 목록 보기

============================================
```

### Step 4: 진행 중인 워크플로우 없을 경우

```
============================================
 개발 워크플로우 상태
============================================

 진행 중인 워크플로우가 없습니다.

 새 워크플로우 시작:
  /dev-start "기능 아이디어"

 기존 문서:
• docs/prd/user-auth/ (완료)
• docs/prd/payment/ (진행 중)

============================================
```

## 참조 파일

- `.claude/memory/CURRENT_CONTEXT.md` - 현재 컨텍스트
- `docs/tasks/{feature}/progress.md` - 진행 상황
