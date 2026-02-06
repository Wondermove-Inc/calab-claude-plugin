# Tasks Phase - 에이전트 호출 프롬프트

> **planner-task 에이전트 호출 시 사용되는 프롬프트 템플릿**

---

## 에이전트 호출

```python
Task(
    subagent_type="calab-plugin:planner-task",
    description="Task 분해",
    prompt="""
## Role
태스크 분해 및 워크플로우 설계 전문가

## Goal
'{feature_name}' 기능을 Epic → Story → Task로 분해

## Input (필수)
- PRD: .claude/docs/active/{feature_name}/02-PRD.md
- 아키텍처: .claude/docs/active/{feature_name}/03-architecture.md

## Output (필수)
**반드시 생성해야 할 파일:**
1. .claude/docs/active/{feature_name}/05-tasks.md
2. .claude-state/worktree.json

## Workflow
1. 02-PRD.md, 03-architecture.md 읽기
2. Epic 정의 (릴리스 단위)
3. Story 분해 (사용자 관점)
4. Task 분해 (개발자 작업 단위, 2-4시간)
5. 각 Task에 Acceptance Criteria 정의
6. 의존성 분석
7. 우선순위 할당 (P0/P1/P2/P3)
8. worktree.json 생성
9. 완료 보고

## Constraints
- 05-tasks.md 파일명 필수
- worktree.json 필수 생성
- 모든 Task에 AC 3-5개 필수
- TASK-{3자리} 형식 (TASK-001, TASK-002...)
- 의존성 그래프 포함

## Template
references/tasks.md 참조
"""
)
```

---

## Data Flow

### Input (이전 단계에서)
| 소스 | 데이터 |
|------|--------|
| /dev --plan | .claude/docs/active/{feature}/02-PRD.md |
| /dev --design | .claude/docs/active/{feature}/03-architecture.md |

### Output (다음 단계로)
| 산출물 | 다음 단계 |
|--------|----------|
| .claude/docs/active/{feature}/05-tasks.md | /dev --build |
| .claude-state/worktree.json | /dev --build |

---

## Worktree Schema

```json
{
  "project": "{feature_name}",
  "feature_folder": ".claude/docs/active/{feature_name}/",
  "status": "in_progress",
  "current_task": "TASK-001",
  "progress": {
    "total": 10,
    "done": 0,
    "in_progress": 0,
    "pending": 10,
    "percentage": 0
  },
  "epics": [
    {
      "id": "EPIC-001",
      "name": "Epic Name",
      "stories": [
        {
          "id": "STORY-001",
          "name": "Story Name",
          "tasks": [
            {
              "id": "TASK-001",
              "name": "Task Name",
              "status": "pending",
              "priority": "P0",
              "dependencies": [],
              "acceptance_criteria": ["AC1", "AC2", "AC3"]
            }
          ]
        }
      ]
    }
  ]
}
```

---

## 검증

산출물 검증은 `post_skill_artifact_check.py`에서 수행:
- 패턴: `{docs}/*/05-tasks.md`
- 필수: Yes
- 미생성 시: Exit Code 2 (차단)
