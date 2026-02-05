# Roadmap Phase Management

> **Phase 단위 로드맵 관리 - 추가/삽입/삭제/완료/마일스톤**

---

## ROADMAP.md 파일 형식

### 경로: `.claude/docs/active/{feature}/ROADMAP.md`

```markdown
# Roadmap: {feature-name}

## 프로젝트 정보
- **이름**: {feature-name}
- **버전**: v{major}.{minor}.{patch}
- **시작일**: {YYYY-MM-DD}
- **현재 Phase**: {N}

## Phase 목록

### Phase 1: {제목} ✅ (완료)
- **완료일**: {YYYY-MM-DD}
- {항목 1}
- {항목 2}

### Phase 2: {제목} 🚧 (진행 중)
- {항목 1}
- {항목 2}

### Phase 3: {제목} 📋 (예정)
- {항목 1}
- {항목 2}

## 마일스톤 히스토리
| 버전 | Phase | 완료일 | 태그 |
|------|-------|--------|------|
| v1.0.0 | Phase 1 | 2026-02-01 | release/v1.0.0 |
```

### 상태 아이콘

| 상태 | 아이콘 | 설명 |
|------|--------|------|
| 완료 | ✅ | 모든 항목 구현 + 검증 완료 |
| 진행 중 | 🚧 | 현재 활성 Phase |
| 예정 | 📋 | 아직 시작 안 함 |
| 긴급 삽입 | 🔴 | insert로 추가된 긴급 Phase |

---

## Phase 관리 커맨드

### 1. `--roadmap` (상태 조회)

```python
# ROADMAP.md 읽어서 현재 상태 출력
roadmap = Read(f".claude/docs/active/{feature}/ROADMAP.md")

# 출력 형식
"""
[ROADMAP] {feature-name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase 1: 기본 인증          ✅ 완료
Phase 2: 소셜 로그인        🚧 진행 중 (3/5 Task)
Phase 3: 2FA               📋 예정
Phase 4: 권한 관리          📋 예정
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
진행률: 1/4 Phase 완료 (25%)
"""
```

### 2. `--roadmap add "{제목}"` (Phase 추가)

마지막에 새 Phase를 추가합니다.

```python
def add_phase(feature, title, items):
    """새 Phase를 로드맵 마지막에 추가"""
    roadmap = read_roadmap(feature)

    new_phase_num = len(roadmap.phases) + 1
    roadmap.phases.append({
        "number": new_phase_num,
        "title": title,
        "status": "planned",  # 📋
        "items": items
    })

    save_roadmap(feature, roadmap)
    return f"Phase {new_phase_num}: {title} 추가 완료"
```

### 3. `--roadmap insert [N] "{제목}"` (긴급 Phase 삽입)

Phase N 앞에 긴급 작업을 삽입합니다. 이후 Phase 번호가 자동으로 밀립니다.

```python
def insert_phase(feature, position, title, items):
    """Phase N 위치에 긴급 Phase 삽입"""
    roadmap = read_roadmap(feature)

    # 유효성 검증
    if position < 1 or position > len(roadmap.phases) + 1:
        raise Error(f"유효하지 않은 위치: {position}")

    # 완료된 Phase 앞에 삽입 금지
    for phase in roadmap.phases:
        if phase.number < position and phase.status == "completed":
            if position <= phase.number:
                raise Error("완료된 Phase 앞에 삽입 불가")

    # 삽입 + 번호 재할당
    new_phase = {
        "number": position,
        "title": title,
        "status": "planned",
        "items": items,
        "urgent": True  # 🔴 표시
    }

    roadmap.phases.insert(position - 1, new_phase)
    renumber_phases(roadmap)

    # worktree.json 업데이트 (Task의 phase 번호 조정)
    update_worktree_phase_numbers(feature, position)

    save_roadmap(feature, roadmap)
    return f"Phase {position}: {title} 삽입 완료 (긴급)"
```

### 4. `--roadmap remove [N]` (Phase 삭제)

예정 상태의 Phase만 삭제 가능합니다.

```python
def remove_phase(feature, phase_num):
    """Phase N 삭제 (예정 상태만 가능)"""
    roadmap = read_roadmap(feature)
    phase = find_phase(roadmap, phase_num)

    # 안전 검증
    if phase.status == "completed":
        raise Error("완료된 Phase는 삭제 불가")
    if phase.status == "in_progress":
        # 사용자 확인 필수
        confirm = AskUserQuestion(
            questions=[{
                "question": f"Phase {phase_num} '{phase.title}'은 진행 중입니다. 정말 삭제할까요?",
                "header": "Phase 삭제",
                "options": [
                    {"label": "삭제", "description": "Phase와 관련 Task 모두 삭제"},
                    {"label": "취소", "description": "삭제하지 않음"}
                ],
                "multiSelect": False
            }]
        )
        if confirm == "취소":
            return "삭제 취소됨"

    roadmap.phases.remove(phase)
    renumber_phases(roadmap)
    save_roadmap(feature, roadmap)
    return f"Phase {phase_num}: {phase.title} 삭제 완료"
```

### 5. `--roadmap complete [N]` (Phase 완료)

Phase를 완료 처리하고 다음 Phase를 활성화합니다.

```python
def complete_phase(feature, phase_num):
    """Phase N 완료 처리 + 다음 Phase 활성화"""
    roadmap = read_roadmap(feature)
    phase = find_phase(roadmap, phase_num)

    # 1. Phase 내 모든 Task 완료 확인
    worktree = load_json(".claude-state/worktree.json")
    phase_tasks = [t for t in worktree["tasks"] if t.get("phase") == phase_num]
    incomplete = [t for t in phase_tasks if t["status"] != "done"]

    if incomplete:
        raise Error(
            f"미완료 Task {len(incomplete)}개: "
            + ", ".join(t["id"] for t in incomplete)
        )

    # 2. Phase 완료 표시
    phase.status = "completed"
    phase.completed_date = datetime.now().strftime("%Y-%m-%d")

    # 3. 다음 Phase 활성화
    next_phase = find_phase(roadmap, phase_num + 1)
    if next_phase:
        next_phase.status = "in_progress"
        roadmap.current_phase = phase_num + 1

    # 4. 산출물 아카이빙
    archive_phase_docs(feature, phase_num)

    save_roadmap(feature, roadmap)
    return f"Phase {phase_num} 완료! → Phase {phase_num + 1} 활성화"
```

### 6. `--roadmap milestone "{버전}"` (마일스톤 생성)

현재 완료된 Phase까지 마일스톤으로 기록합니다.

```python
def create_milestone(feature, version):
    """마일스톤 생성 + Git 태그"""
    roadmap = read_roadmap(feature)

    # 1. 완료된 Phase 확인
    completed = [p for p in roadmap.phases if p.status == "completed"]
    if not completed:
        raise Error("완료된 Phase가 없습니다")

    latest_completed = completed[-1]

    # 2. 마일스톤 히스토리에 추가
    roadmap.milestones.append({
        "version": version,
        "phase": f"Phase {latest_completed.number}",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "tag": f"release/{version}"
    })

    # 3. Git 태그 생성 (사용자 확인 후)
    confirm = AskUserQuestion(
        questions=[{
            "question": f"Git 태그 'release/{version}'를 생성할까요?",
            "header": "Git 태그",
            "options": [
                {"label": "생성", "description": f"release/{version} 태그 생성"},
                {"label": "건너뛰기", "description": "태그 없이 마일스톤만 기록"}
            ],
            "multiSelect": False
        }]
    )

    if confirm == "생성":
        Bash(f'git tag -a "release/{version}" -m "Milestone: Phase {latest_completed.number} - {latest_completed.title}"')

    # 4. 완료 Phase 문서 아카이빙
    archive_dir = f".claude/docs/archived/{feature}/{version}"
    move_completed_docs(feature, archive_dir)

    save_roadmap(feature, roadmap)
    return f"마일스톤 {version} 생성 완료 (Phase {latest_completed.number}까지)"
```

---

## Phase와 워크플로우 연동

### Phase → Tasks 매핑

```json
// worktree.json 확장
{
  "feature": "user-auth",
  "current_phase": 2,
  "total_phases": 4,
  "phases": [
    {
      "number": 1,
      "title": "기본 인증",
      "status": "completed"
    },
    {
      "number": 2,
      "title": "소셜 로그인",
      "status": "in_progress"
    }
  ],
  "tasks": [
    {
      "id": "TASK-001",
      "phase": 1,
      "wave": 1,
      "status": "done"
    },
    {
      "id": "TASK-004",
      "phase": 2,
      "wave": 1,
      "status": "in_progress"
    }
  ]
}
```

### Phase 완료 → 다음 Phase 전환 흐름

```
Phase N의 모든 Task 완료
    ↓
validator 검증 (Phase 단위)
    ↓
--roadmap complete N
    ↓
Phase N ✅ 완료 표시
    ↓
Phase N+1 🚧 활성화
    ↓
--tasks (Phase N+1 Task 분해)
    ↓
--build --all (Wave 실행)
```

---

## 초기화

### `--plan` 단계에서 ROADMAP.md 생성

```python
def init_roadmap(feature, prd):
    """PRD 기반으로 초기 ROADMAP.md 생성"""
    phases = extract_phases_from_prd(prd)

    roadmap = {
        "name": feature,
        "version": "v0.1.0",
        "start_date": datetime.now().strftime("%Y-%m-%d"),
        "current_phase": 1,
        "phases": phases,
        "milestones": []
    }

    # Phase 1을 자동 활성화
    roadmap["phases"][0]["status"] = "in_progress"

    Write(
        f".claude/docs/active/{feature}/ROADMAP.md",
        render_roadmap_md(roadmap)
    )
```

### PRD에서 Phase 추출 기준

| 기준 | 설명 |
|------|------|
| Epic 단위 | PRD의 Epic이 Phase에 매핑 |
| 의존성 순서 | 선행 기능 → 후행 기능 순서 |
| 사용자 가치 | MVP → 확장 순서 |

---

## 안전 규칙

| 규칙 | 설명 |
|------|------|
| 완료 Phase 삭제 금지 | 이미 완료된 Phase는 삭제할 수 없음 |
| 진행 중 Phase 삭제 시 확인 | AskUserQuestion으로 사용자 확인 필수 |
| 삽입 시 번호 자동 조정 | 이후 Phase/Task 번호 자동 재할당 |
| 마일스톤 Git 태그 확인 | 사용자 승인 후에만 태그 생성 |
| Phase 완료 전 Task 검증 | 미완료 Task 있으면 완료 불가 |
