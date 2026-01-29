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
| `/dev-build` 시작 시 | 1. worktree.json 읽기 → 2. status를 "in_progress"로 Edit → 3. started_at 추가 |
| `/dev-build` 완료 시 | 1. worktree.json 읽기 → 2. status를 "done"으로 Edit → 3. completed_at 추가 → 4. progress 업데이트 |
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

## 🔐 Worktree 무결성 검증 (W3 Fix)

> **"Validate before trust"** - worktree.json 데이터 무결성 보장

### Worktree 체크섬 검증

```python
import hashlib
import json
from datetime import datetime

def calculate_worktree_checksum(worktree):
    """Worktree 상태 체크섬 계산"""
    # 변동성 필드 제외한 핵심 상태만 해시
    core_state = {
        "epics": worktree.get("epics", []),
        "progress": worktree.get("progress", {}),
        "current_task": worktree.get("current_task")
    }
    state_json = json.dumps(core_state, sort_keys=True)
    return hashlib.sha256(state_json.encode()).hexdigest()[:16]


def save_worktree_with_integrity(worktree):
    """무결성 메타데이터 포함하여 저장"""
    worktree["_integrity"] = {
        "checksum": calculate_worktree_checksum(worktree),
        "updated_at": datetime.now().isoformat(),
        "version": worktree.get("_integrity", {}).get("version", 0) + 1
    }
    save_to_file(".claude-state/worktree.json", worktree)


def validate_worktree_integrity(worktree):
    """Worktree 무결성 검증"""
    integrity = worktree.get("_integrity", {})

    if not integrity:
        return {
            "valid": False,
            "error": "NO_INTEGRITY_METADATA",
            "action": "regenerate_checksum"
        }

    stored_checksum = integrity.get("checksum")
    calculated_checksum = calculate_worktree_checksum(worktree)

    if stored_checksum != calculated_checksum:
        return {
            "valid": False,
            "error": "CHECKSUM_MISMATCH",
            "stored": stored_checksum,
            "calculated": calculated_checksum,
            "action": "investigate_corruption"
        }

    # 타임스탬프 검증 (24시간 이상 미업데이트 경고)
    updated_at = integrity.get("updated_at")
    if updated_at:
        last_update = datetime.fromisoformat(updated_at)
        if (datetime.now() - last_update).total_seconds() > 86400:
            return {
                "valid": True,
                "warning": "STALE_DATA",
                "last_update": updated_at,
                "action": "consider_refresh"
            }

    return {"valid": True, "checksum": stored_checksum}
```

### Worktree JSON 형식 (무결성 포함)

```json
{
  "_integrity": {
    "checksum": "a1b2c3d4e5f67890",
    "updated_at": "2024-01-15T10:30:00Z",
    "version": 42
  },
  "current_task": "TASK-003",
  "epics": [...],
  "progress": {
    "done": 5,
    "in_progress": 1,
    "pending": 4,
    "percentage": 50
  }
}
```

### 무결성 검증 시점

| 시점 | 액션 | 실패 시 |
|------|------|--------|
| **세션 시작** | 체크섬 검증 | checkpoint.json에서 복구 |
| **worktree 로드** | 체크섬 검증 | 경고 후 재계산 |
| **worktree 저장** | 체크섬 갱신 | - |
| **/restore 실행** | 3중 채널 교차 검증 | 가장 최신 버전 사용 |

### 무결성 오류 출력

```
============================================
[WORKTREE INTEGRITY] 무결성 검증 결과
============================================

⚠️ 체크섬 불일치 감지!

• 저장된 체크섬: a1b2c3d4e5f67890
• 계산된 체크섬: x9y8z7w6v5u43210

🔍 가능한 원인:
1. 외부 도구에 의한 직접 수정
2. 비정상 세션 종료
3. 동시 접근 충돌

🔧 복구 옵션:
1. checkpoint.json에서 복원 (권장)
2. 현재 상태 기준 체크섬 재계산
3. 수동 검토 후 수정

============================================
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

## State Handoff Pattern (2025 Best Practice)

> **"Reliable state transfer with checksum validation and redundancy"** - AI Agent Handoff Pattern

### 상태 전달 신뢰성 보장

세션 간 상태 전달 시 데이터 무결성을 보장하기 위한 체크섬 검증 및 중복 채널 패턴.

### 중복 저장 채널 (Redundancy Channels)

| 우선순위 | 채널 | 파일 | 용도 |
|---------|------|------|------|
| **Primary** | 구조화된 핸드오프 | `.claude-state/checkpoint.json` | 상세 체크포인트 |
| **Secondary** | 상태 JSON | `.claude-state/worktree.json` | 작업 트리 상태 |
| **Tertiary** | 사람 읽기용 저널 | `.claude/memory/CURRENT_CONTEXT.md` | 비상 복구용 |

### 체크섬 검증 프로토콜

```python
def create_checkpoint_with_checksum(state):
    """체크섬 포함 체크포인트 생성"""
    import hashlib
    import json

    checkpoint = {
        "timestamp": datetime.now().isoformat(),
        "state": state,
        "version": "1.0"
    }

    # 상태 해시 계산
    state_json = json.dumps(state, sort_keys=True)
    checkpoint["checksum"] = hashlib.sha256(state_json.encode()).hexdigest()[:16]

    return checkpoint


def validate_checkpoint(checkpoint):
    """체크포인트 무결성 검증"""
    import hashlib
    import json

    state_json = json.dumps(checkpoint["state"], sort_keys=True)
    calculated = hashlib.sha256(state_json.encode()).hexdigest()[:16]

    return calculated == checkpoint.get("checksum")
```

### 체크포인트 JSON 형식

```json
{
  "timestamp": "2024-01-15T10:00:00Z",
  "version": "1.0",
  "checksum": "a1b2c3d4e5f67890",
  "state": {
    "current_task": "TASK-003",
    "progress": {
      "done": 2,
      "in_progress": 1,
      "pending": 5,
      "percentage": 25
    },
    "work_stack": [
      {
        "task_id": "TASK-003",
        "status": "in_progress",
        "started_at": "2024-01-15T09:30:00Z",
        "context": "사용자 인증 로직 구현 중"
      }
    ],
    "recent_files": [
      "src/auth/login.ts",
      "src/services/auth.ts"
    ],
    "next_steps": [
      "토큰 검증 로직 구현",
      "에러 핸들링 추가"
    ],
    "important_notes": "JWT 라이브러리 사용, 환경변수 SECRET_KEY 필요"
  }
}
```

### 복구 시 검증 절차

```python
def restore_state():
    """상태 복구 with 체크섬 검증"""

    channels = [
        ".claude-state/checkpoint.json",      # Primary
        ".claude-state/worktree.json",        # Secondary
        ".claude/memory/CURRENT_CONTEXT.md"   # Tertiary
    ]

    for channel in channels:
        try:
            checkpoint = read_file(channel)

            if channel.endswith('.json'):
                if validate_checkpoint(checkpoint):
                    return {
                        "status": "success",
                        "source": channel,
                        "state": checkpoint["state"],
                        "checksum_valid": True
                    }
                else:
                    log_warning(f"Checksum mismatch in {channel}")
                    continue

            else:
                # Markdown 파일은 파싱 후 사용
                return {
                    "status": "degraded",
                    "source": channel,
                    "state": parse_markdown_context(checkpoint),
                    "checksum_valid": None
                }

        except Exception as e:
            log_error(f"Failed to read {channel}: {e}")
            continue

    return {
        "status": "failed",
        "reason": "All recovery channels exhausted"
    }
```

### 복구 결과 출력

```
============================================
[STATE RECOVERY] 상태 복구 완료
============================================

📁 복구 소스: .claude-state/checkpoint.json
✅ 체크섬 검증: 통과 (a1b2c3d4e5f67890)

📊 복구된 상태:
• 현재 태스크: TASK-003
• 진행률: 25% (2/8 완료)
• 마지막 작업: 2024-01-15T09:30:00Z

📋 다음 단계:
1. 토큰 검증 로직 구현
2. 에러 핸들링 추가

============================================
```

## Graceful Degradation (우아한 성능 저하)

> **"Prioritize recovery based on business impact"** - 비즈니스 영향도 기반 복구

### 복구 우선순위

| 우선순위 | 영역 | 실패 시 영향 | 복구 전략 |
|---------|------|-------------|----------|
| **P0** | 작업 컨텍스트 | 진행 상황 유실 | 3중 백업 복구 |
| **P1** | Worktree 상태 | 진행률 오류 | 마지막 커밋 기준 재계산 |
| **P2** | 규칙 캐시 | 규칙 적용 지연 | 런타임 재로드 |
| **P3** | 베스트 프랙티스 | 품질 저하 가능 | 기본 규칙 폴백 |

### 성능 저하 모드

```python
def determine_degradation_level(failures):
    """장애 수준에 따른 성능 저하 모드 결정"""

    if "checkpoint" in failures and "worktree" in failures:
        return {
            "level": "CRITICAL",
            "mode": "manual_recovery",
            "message": "수동 복구 필요 - 사용자에게 /restore 안내"
        }

    if "checkpoint" in failures:
        return {
            "level": "DEGRADED",
            "mode": "worktree_only",
            "message": "체크포인트 불가 - Worktree 기반 진행"
        }

    if "rules" in failures:
        return {
            "level": "LIMITED",
            "mode": "default_rules",
            "message": "프로젝트 규칙 로드 실패 - 기본 규칙 적용"
        }

    return {
        "level": "NORMAL",
        "mode": "full_operation",
        "message": None
    }
```

## 🔒 Deadlock Prevention (데드락 방지)

> **"Cycle detection at task creation"** - Task 생성 시 순환 의존성 감지

### 의존성 검증 (Task 생성 전 필수)

새 Task 생성 시 반드시 의존성 그래프를 검증합니다:

```python
def validate_task_dependencies(new_task_id, depends_on, worktree):
    """Task 의존성 유효성 검사"""

    # 1. 기존 의존성 그래프 구축
    graph = {}
    for epic in worktree["epics"]:
        for story in epic["stories"]:
            for task in story["tasks"]:
                graph[task["id"]] = task.get("depends_on", [])

    # 2. 새 Task 추가
    graph[new_task_id] = depends_on

    # 3. 순환 의존성 검사 (DFS)
    def has_cycle(node, visited, rec_stack):
        visited.add(node)
        rec_stack.add(node)

        for dep in graph.get(node, []):
            if dep not in visited:
                if has_cycle(dep, visited, rec_stack):
                    return True
            elif dep in rec_stack:
                return True

        rec_stack.remove(node)
        return False

    visited, rec_stack = set(), set()
    for node in graph:
        if node not in visited:
            if has_cycle(node, visited, rec_stack):
                return {
                    "valid": False,
                    "error": "CIRCULAR_DEPENDENCY",
                    "suggestion": "의존성 구조 재검토 필요"
                }

    return {"valid": True}
```

### 데드락 방지 체크리스트

Task 생성 시:
- [ ] 순환 의존성 없음 확인
- [ ] 상호 대기(mutual wait) 가능성 없음
- [ ] 의존성 체인 깊이 5단계 이하
- [ ] 모든 의존 Task가 존재함

## ⏱️ Heartbeat & Timeout (하트비트 모니터링)

> **"Release stale tasks automatically"** - 오래된 Task 자동 해제

### 하트비트 프로토콜

진행 중인 Task의 활성 상태를 추적합니다:

```python
TIMEOUT_THRESHOLDS = {
    "inner_loop": 300,      # 5분 (코드 수정)
    "middle_loop": 1800,    # 30분 (Task 구현)
    "outer_loop": 7200,     # 2시간 (설계/계획)
}

def check_task_heartbeat(worktree):
    """Stale Task 감지 및 처리"""

    stale_tasks = []
    now = datetime.now()

    for epic in worktree["epics"]:
        for story in epic["stories"]:
            for task in story["tasks"]:
                if task["status"] == "in_progress":
                    last_beat = parse_datetime(task.get("last_heartbeat", task.get("started_at")))
                    loop_type = determine_loop_type(task)
                    timeout = TIMEOUT_THRESHOLDS[loop_type]

                    elapsed = (now - last_beat).total_seconds()
                    if elapsed > timeout:
                        stale_tasks.append({
                            "task_id": task["id"],
                            "elapsed_seconds": elapsed,
                            "timeout": timeout,
                            "action": "release"
                        })

    return stale_tasks


def release_stale_task(task_id, worktree):
    """Stale Task 해제 - 재시도 가능 상태로 변경"""

    # Task 상태 업데이트
    task["status"] = "pending"  # 다시 pending으로
    task["release_reason"] = "heartbeat_timeout"
    task["release_time"] = datetime.now().isoformat()
    task.pop("started_at", None)

    return {"released": True, "task_id": task_id}
```

### Worktree에 하트비트 기록

```json
{
  "current_task": "TASK-003",
  "epics": [...],
  "heartbeat_tracking": {
    "enabled": true,
    "check_interval_seconds": 60,
    "last_check": "2024-01-15T10:30:00Z"
  },
  "stale_releases": [
    {
      "task_id": "TASK-002",
      "released_at": "2024-01-15T09:00:00Z",
      "reason": "heartbeat_timeout",
      "elapsed_seconds": 3600
    }
  ]
}
```

### Task 시작 시 하트비트 시작

```python
def start_task_with_heartbeat(task_id):
    """Task 시작 시 하트비트 초기화"""

    task = get_task(task_id)
    task["status"] = "in_progress"
    task["started_at"] = datetime.now().isoformat()
    task["last_heartbeat"] = datetime.now().isoformat()

    # Worktree 업데이트
    update_worktree(task)

    return task
```

### 하트비트 갱신 시점

다음 시점에 하트비트를 갱신합니다:
- 파일 수정 완료 시
- 빌드/테스트 실행 후
- 사용자 응답 후
- 체크포인트 저장 시

## 🔗 Request ID Correlation (요청 추적)

> **"You can't fix what you don't trace"** - 2025 SRE Best Practice

### Request ID 생성 규칙

모든 에이전트 호출과 작업에 고유 ID를 부여하여 추적합니다:

```python
import uuid
from datetime import datetime

def generate_request_id(prefix="REQ"):
    """고유 요청 ID 생성"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    short_uuid = str(uuid.uuid4())[:8]
    return f"{prefix}-{timestamp}-{short_uuid}"

# 예시: REQ-20240115103045-a1b2c3d4
```

### Request ID 유형

| Prefix | 용도 | 예시 |
|--------|------|------|
| `REQ` | 일반 요청 | `REQ-20240115103045-a1b2c3d4` |
| `TSK` | Task 작업 | `TSK-001-20240115103045-a1b2c3d4` |
| `AGT` | 에이전트 호출 | `AGT-validator-20240115103045-a1b2c3d4` |
| `ERR` | 오류 추적 | `ERR-build-20240115103045-a1b2c3d4` |

### 로그 형식

```json
{
  "request_id": "TSK-003-20240115103045-a1b2c3d4",
  "timestamp": "2024-01-15T10:30:45Z",
  "severity": "INFO",
  "task_id": "TASK-003",
  "agent": "dev-executor",
  "operation": "file_edit",
  "file": "src/auth/login.ts",
  "latency_ms": 234,
  "success": true,
  "parent_request_id": "REQ-20240115103000-xyz12345"
}
```

### 분산 추적 체인

```
[REQ-xxx] 사용자 요청: "로그인 기능 구현해줘"
    │
    ├── [AGT-planner-xxx] planner-phase 호출
    │       └── 결과: PRD 생성
    │
    ├── [AGT-executor-xxx] dev-executor 호출
    │       ├── [TSK-001-xxx] 타입 정의
    │       ├── [TSK-002-xxx] API 구현
    │       └── [TSK-003-xxx] 테스트 작성
    │
    └── [AGT-validator-xxx] validator 호출
            └── [ERR-type-xxx] 타입 오류 발생
                    └── [AGT-reinforcer-xxx] reinforcer 호출
```

### Correlation 저장 위치

```
.claude-state/
├── request-log.jsonl     # 요청 로그 (JSON Lines 형식)
├── correlation-index.json # 요청 ID 인덱스
└── error-traces/         # 오류별 상세 추적
    └── ERR-xxx.json
```

### 오류 추적 활용

```
============================================
[ERROR TRACE] 오류 추적 정보
============================================

🔍 오류 ID: ERR-build-20240115103045-a1b2c3d4

📋 추적 체인:
REQ-20240115103000-xyz12345 (최초 요청)
  └── AGT-executor-20240115103010-abc (dev-executor)
        └── TSK-003-20240115103020-def (TASK-003)
              └── ERR-build-20240115103045-a1b2c3d4 ← 오류 발생

📊 컨텍스트:
• 작업: TASK-003 - AuthService 구현
• 파일: src/services/auth.ts:45
• 에이전트: dev-executor

🔄 관련 요청:
• 이전: TSK-002-xxx (성공)
• 현재: TSK-003-xxx (실패)
• 의존: TSK-001-xxx

============================================
```

## 참조 파일
- `.claude/memory/CURRENT_CONTEXT.md` - 현재 작업 상태
- `.claude-state/checkpoint.json` - 체크포인트 (체크섬 포함)
- `.claude-state/worktree.json` - 작업 트리 상태
- `.claude/memory/WORK_HISTORY.md` - 작업 히스토리
- `.claude-state/request-log.jsonl` - 요청 로그
- `commands/worktree.md` - Worktree 명령어
