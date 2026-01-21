---
name: work-tracker
description: 작업 진행 상태를 추적하고 관리합니다. 새 작업 시작, 작업 전환, 완료, 다음 단계, 이제, 그 다음 키워드 사용 시 자동 활성화. 맥락 유실 방지에 필수입니다.
allowed-tools: Read, Write, Edit
---

# Work Tracker Skill

## 목적
진행 중인 작업의 상태를 추적하여 컨텍스트 유실을 방지합니다.
**Worktree와 연동하여 실시간 작업 트리를 관리합니다.**

## 🚨 CRITICAL: 작업 기록 의무

**모든 응답에서 작업 내용을 상세히 기록해야 합니다.**

Hook은 파일 변경만 감지할 수 있고, Claude가 실제로 무슨 작업을 했는지는 Claude 자신만 알 수 있습니다.
따라서 **Claude가 직접** 다음 파일들을 업데이트해야 합니다:

| 파일 | 기록 시점 | 기록 내용 |
|------|----------|----------|
| `CURRENT_CONTEXT.md` | 작업 시작/완료 시 | 무엇을, 왜, 결과 |
| `WORK_HISTORY.md` | 의미 있는 작업 완료 시 | 상세 작업 내역 |
| `worktree.json` | 태스크 상태 변경 시 | 진행률, 상태 |

### 기록해야 할 정보 (6W1H)

1. **What (무엇을)**: 수행한 작업의 구체적 내용
2. **Why (왜)**: 이 작업을 수행한 이유/목적
3. **How (어떻게)**: 해결 방법, 사용한 기술
4. **Where (어디서)**: 변경된 파일 목록
5. **Result (결과)**: 성공/실패, 발견한 문제
6. **Next (다음)**: 후속 작업, 남은 TODO
7. **Progress (진행률)**: 전체 중 현재 위치

### 기록 형식 예시

```markdown
## 작업 스택 (위에서 아래로 진입 순서)

- [17:30] **[문제해결]** Memory 기록 품질 개선
  - **목적**: Memory에 기록되는 내용이 허접해서 작업 추적 불가
  - **원인**: Hook이 파일 변경만 감지, Claude 작업 내용 모름
  - **해결**: work-tracker 스킬에 상세 기록 의무 추가
  - **변경**: SKILL.md, CLAUDE.md
  - **결과**: ✅ Claude가 직접 상세 기록하도록 규칙 강화
  - **다음**: 실제 작업에서 테스트 필요
```

## 활성화 조건
다음 상황에서 이 스킬이 자동으로 활성화됩니다:
- 새로운 작업/기능 구현 시작 시
- "다음", "그 다음", "이제", "그러면" 등 작업 전환 키워드 사용 시
- 하위 작업으로 진입할 때
- "완료", "끝", "다 했어" 등 완료 키워드 사용 시
- 상위 작업으로 복귀할 때
- 긴 대화 후 방향 확인 필요 시

## 작업 관리 프로토콜

### 새 작업 시작 시

1. **현재 상태 확인**
   - `.claude/memory/CURRENT_CONTEXT.md` 읽기
   - 기존 작업 스택 확인

2. **작업 스택 업데이트**
   - 새 작업을 스택 최상단에 추가
   - 상태를 "[진행중]"으로 설정
   - 작업 목표와 예상 단계 기록

3. **파일 업데이트**
   ```markdown
   ## 작업 스택
   1. **[진행중]** [새 작업]
      - 상태: 시작
      - 다음 단계: [첫 번째 할 일]
   2. **[대기]** [이전 작업]
      - 현재 작업 완료 후 복귀 예정
   ```

### 작업 완료 시

> 🚨 **CRITICAL**: 아래 검증을 거치지 않고 완료 처리하지 마세요!

**1. 완료 검증 (필수 - 건너뛰기 금지)**
   - Acceptance Criteria 각 항목 검증
   - 기능 동작 테스트
   - 엣지 케이스 처리 확인
   - 코드 품질 검증

**검증 결과 출력 (필수):**
```
[TASK 완료 검증] TASK-XXX
━━━━━━━━━━━━━━━━━━━━━━━
✅ AC1: {조건} - 충족
✅ AC2: {조건} - 충족
❌ AC3: {조건} - 미충족 → 추가 구현 필요
━━━━━━━━━━━━━━━━━━━━━━━
결과: ❌ 미충족 항목 있음 - 완료 불가
```

**❌ 미충족 시: 현재 Task 계속 진행, 다음 Task 이동 금지**
**✅ 모두 충족 시: 아래 완료 처리 진행**

**2. 완료 처리 (검증 통과 후)**
   - 완료된 작업을 "최근 완료" 섹션으로 이동
   - 완료 시간 기록

**3. 스택 업데이트**
   - 스택에서 완료된 작업 제거
   - 다음 작업(있다면)을 "[진행중]"으로 변경

**4. 상위 작업 복귀**
   - 대기 중이던 상위 작업 컨텍스트 복원
   - 다음 단계 안내

### 작업 중단/전환 시

1. **현재 상태 상세 기록**
   - 어디까지 진행했는지
   - 어떤 파일을 수정했는지
   - 발생한 이슈가 있는지

2. **"다음 단계" 명확히 작성**
   - 재개 시 바로 시작할 수 있도록

3. **주의사항 기록**
   - 기억해야 할 컨텍스트
   - 관련 파일 경로

## 맥락 이탈 감지

다음 상황에서 경고 발생:
- 현재 작업과 무관한 요청 감지
- 작업 스택이 너무 깊어질 때 (3단계 이상)
- 상위 목표와 일치하지 않는 방향

```
[CONTEXT CHECK] 작업 방향 확인

현재 목표: [원래 목표]
현재 요청: [지금 하려는 것]

이 작업이 현재 목표와 관련이 있나요?
- 예: 계속 진행
- 아니오: 현재 작업 저장 후 새 작업으로 전환
```

## 체크포인트 생성

중요 진행 시점에서 `.claude-state/checkpoint.json` 자동 업데이트:

```json
{
  "timestamp": "ISO-8601 형식",
  "current_task": "현재 작업 설명",
  "progress": "진행 상황 요약",
  "next_steps": ["다음 단계 1", "다음 단계 2"],
  "important_files": ["수정한 파일 1", "수정한 파일 2"],
  "notes": "특이사항"
}
```

## 🚨 Worktree 연동 (필수 - 직접 수정)

> **CRITICAL**: Hook은 worktree.json을 자동 업데이트하지 않습니다!
> **Claude가 Edit 도구로 직접 수정해야 합니다.**

### Worktree 업데이트 의무

다음 상황에서 **반드시 Edit 도구로 `.claude-state/worktree.json` 직접 수정**:

| 상황 | 즉시 수행할 작업 |
|------|-----------------|
| `/workflow:process-build` 시작 시 | 1. worktree.json 읽기 → 2. status를 "in_progress"로 Edit → 3. started_at 추가 |
| `/workflow:process-build` 완료 시 | 1. worktree.json 읽기 → 2. status를 "done"으로 Edit → 3. completed_at 추가 → 4. progress 업데이트 |
| "TASK-XXX 시작" 언급 시 | 즉시 status → "in_progress" Edit |
| "TASK-XXX 완료" 언급 시 | 즉시 status → "done" Edit |
| "블로커", "막힘" 언급 시 | 즉시 status → "blocked" Edit |

### 업데이트 실행 절차

**Step 1**: worktree.json 파일 읽기
```
Read: .claude-state/worktree.json
```

**Step 2**: 해당 태스크 찾기 (epics[].stories[].tasks[] 구조)

**Step 3**: Edit 도구로 status 변경
```
Edit: .claude-state/worktree.json
old_string: "status": "pending"
new_string: "status": "in_progress"
```

**Step 4**: 시간 필드 추가
```
started_at: "2024-01-15T10:00:00Z"  (시작 시)
completed_at: "2024-01-15T11:00:00Z"  (완료 시)
```

**Step 5**: progress 필드 업데이트
```json
"progress": {
  "done": 5,
  "in_progress": 1,
  "pending": 4,
  "percentage": 50
}
```

### 작업 시작 시 Worktree 업데이트

```json
{
  "current_task": "TASK-003",
  "epics[].stories[].tasks[id=TASK-003]": {
    "status": "in_progress",
    "started_at": "2024-01-15T10:00:00Z"
  },
  "progress": {
    "in_progress": 1
  }
}
```

### 작업 완료 시 Worktree 업데이트

```json
{
  "current_task": "TASK-004",  // 다음 태스크로 이동
  "epics[].stories[].tasks[id=TASK-003]": {
    "status": "done",
    "completed_at": "2024-01-15T11:00:00Z"
  },
  "progress": {
    "done": 4,
    "in_progress": 1,
    "percentage": 40
  },
  "daily_log": [{
    "date": "2024-01-15",
    "completed": ["TASK-003"]
  }]
}
```

### Worktree 표시 트리거

다음 상황에서 Worktree 트리 자동 출력:

1. **세션 시작 시** - 현재 진행 상황 요약
2. **태스크 완료 시** - 진행률 업데이트 및 다음 태스크 안내
3. **긴 대화 후** - 현재 위치 확인
4. **사용자가 "/worktree" 요청 시**

### Worktree 출력 형식

```
┌─ Epic 1: 사용자 인증
│
├─┬─ Story 1.1: 회원가입
│ ├── ✅ TASK-001: User 테이블 마이그레이션
│ ├── ✅ TASK-002: RegisterDto 정의
│ ├── 🔄 TASK-003: AuthService.register()  ← 현재
│ └── ⬚ TASK-004: AuthController 구현
│
└─ 진행률: ████████░░░░ 40%
```

## 참조 파일
- `.claude/memory/CURRENT_CONTEXT.md` - 현재 작업 상태
- `.claude-state/checkpoint.json` - 체크포인트
- `.claude-state/worktree.json` - 작업 트리 상태
- `.claude/memory/WORK_HISTORY.md` - 작업 히스토리
- `commands/worktree.md` - Worktree 명령어
