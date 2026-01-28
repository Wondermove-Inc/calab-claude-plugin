# /dev --status - 상태 확인

> **워크플로우 진행 상황 표시**

## 사용법

```bash
/dev --status              # 현재 진행 상황
/dev --status [기능명]     # 특정 기능 상태
```

---

## 실행 절차

### Step 1: 컨텍스트 로드

```
로드 파일:
1. .claude/memory/CURRENT_CONTEXT.md
2. .claude-state/worktree.json
3. .claude/docs/active/ 스캔
4. .claude/docs/complete/ 스캔
```

### Step 2: 문서 상태 확인

```
각 Phase별 문서 존재 여부 확인:

Phase 1 (Plan):
- [ ] 01-brainstorm.md
- [ ] 02-prd.md

Phase 2 (Design):
- [ ] 03-architecture.md
- [ ] 04-erd.md

Phase 3 (Tasks):
- [ ] 05-tasks.md
- [ ] worktree.json

Phase 4 (Build):
- [ ] 소스 코드 변경

Phase 5 (QA):
- [ ] qa/plan.md
- [ ] qa/report.md
```

### Step 3: 진행률 계산

```
worktree.json에서:
- total: 전체 태스크
- done: 완료된 태스크
- in_progress: 진행 중
- blocked: 차단됨
- pending: 대기 중

percentage = (done / total) * 100
```

---

## 출력 형식

```
============================================
 DEV STATUS: {기능명}
============================================

 📍 현재 단계: {Phase 이름}

 📋 워크플로우 진행:

 ┌────────────────────────────────────────┐
 │ Phase 1: Plan                          │
 │   ├── 01-brainstorm.md        [✓]     │
 │   └── 02-prd.md               [✓]     │
 │                                        │
 │ Phase 2: Design                        │
 │   ├── 03-architecture.md      [✓]     │
 │   └── 04-erd.md               [✓]     │
 │                                        │
 │ Phase 3: Tasks                         │
 │   ├── 05-tasks.md             [✓]     │
 │   └── worktree.json           [✓]     │
 │                                        │
 │ Phase 4: Build                         │
 │   └── 진행률                  [40%]    │
 │                                        │
 │ Phase 5: QA                            │
 │   ├── qa/plan.md              [ ]     │
 │   └── qa/report.md            [ ]     │
 └────────────────────────────────────────┘

 📊 태스크 진행률:

 ████████░░░░░░░░░░░░ 40% (4/10)

 ┌──────────────────────────────────┐
 │ 완료    │ ████████     │ 4개    │
 │ 진행중  │ ██           │ 1개    │
 │ 블로커  │              │ 0개    │
 │ 대기    │ ██████████   │ 5개    │
 └──────────────────────────────────┘

 🔄 현재 작업:
 • TASK-005: AuthService.register() 구현

 ⏭️ 다음 작업:
 • TASK-006: AuthController 구현

 🚫 블로커: (있는 경우)
 • TASK-008: 외부 API 인증 키 대기 중

============================================
 명령어 안내:
 • 태스크 시작: /dev --build TASK-005
 • 트리 확인: /worktree
 • 진행 저장: /save
============================================
```

---

## 활성 프로젝트 목록

여러 기능이 진행 중인 경우:

```
============================================
 ACTIVE PROJECTS
============================================

 📁 .claude/docs/active/

 1. user-auth/
    • 진행률: 40% (4/10 tasks)
    • 현재: TASK-005
    • 단계: Build

 2. notification-system/
    • 진행률: 0% (0/8 tasks)
    • 현재: -
    • 단계: Design

============================================
 특정 프로젝트 상태: /dev --status user-auth
============================================
```

---

## 완료된 프로젝트

```
============================================
 COMPLETED PROJECTS
============================================

 📁 .claude/docs/complete/

 1. login-feature/
    • 완료일: 2024-01-10
    • 태스크: 12개

 2. profile-page/
    • 완료일: 2024-01-08
    • 태스크: 8개

============================================
```

---

## 다음 단계 안내

| 현재 상태 | 권장 명령어 |
|----------|------------|
| Plan 미완료 | `/dev --plan {기능}` |
| Design 미완료 | `/dev --design {기능}` |
| Tasks 미완료 | `/dev --tasks {기능}` |
| Build 진행중 | `/dev --build {TASK-ID}` |
| 전체 완료 | `/qa` |
