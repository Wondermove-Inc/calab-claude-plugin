---
name: planner-task
description: |
  Decomposes PHASEs into individual Tasks with TDD workflow.
  Tactical planning: How to implement each PHASE.
  PHASE를 개별 Task로 분해하고 TDD 워크플로우를 적용합니다.

  Called by: /dev --tasks
skills: clarification-protocol
tools: [Read, Write, Glob, Grep, TaskCreate, TaskUpdate, TaskList, Task]
model: sonnet
---

# planner-task Agent

Task decomposition agent for TDD workflow setup.

---

## Workflow

### 1. Load Context

```python
# 1. Read PRD with PHASE definitions
prd = Read(f".claude/plans/{feature_name}.md")

# 2. Read Design document if exists
design = Read(f".claude/plans/{feature_name}-DESIGN.md")

# 3. Analyze existing patterns
Task(
    subagent_type="Explore",
    prompt="Find test patterns: *.test.ts, *.spec.ts",
    model="haiku"
)
```

### 2. Generate Task List

For each PHASE, create Tasks using TaskCreate:

```python
for phase in prd.phases:
    # Create Tasks for this PHASE
    for task_def in decompose_phase(phase):
        TaskCreate(
            subject=f"[{phase.number}] {task_def.name}",
            description=f"""
## Task: {task_def.name}

**PHASE**: {phase.number} - {phase.name}
**Type**: {task_def.type}  # domain/application/adapters/infrastructure

### Acceptance Criteria
{task_def.acceptance_criteria}

### TDD Stage
- RED: Write failing tests first
- GREEN: Implement to pass tests
- REFACTOR: Clean up code

### Files to Create/Modify
{task_def.files}

### Dependencies
{task_def.dependencies}
            """,
            activeForm=f"구현 중: {task_def.name}",
            metadata={
                "feature": feature_name,
                "phase": phase.number,
                "layer": task_def.layer,
                "tdd_stage": "RED"
            }
        )

    # Set up dependencies
    for task in phase_tasks:
        if task.dependencies:
            TaskUpdate(
                taskId=task.id,
                addBlockedBy=task.dependencies
            )
```

### 3. Task Structure Template

Each Task document should contain:

```markdown
## Task: {TASK-ID}

**PHASE**: {phase_number} - {phase_name}
**Layer**: {domain|application|adapters|infrastructure}
**Status**: pending

### Acceptance Criteria

- [ ] AC1: {specific, testable criteria}
- [ ] AC2: {specific, testable criteria}

### TDD Workflow

#### RED Phase (Write Failing Tests)
- [ ] Create test file: `src/{path}/__tests__/{name}.test.ts`
- [ ] Write test cases for AC1, AC2
- [ ] Verify tests FAIL

#### GREEN Phase (Implement)
- [ ] Create implementation: `src/{path}/{name}.ts`
- [ ] Write minimum code to pass tests
- [ ] Verify tests PASS

#### REFACTOR Phase (Clean Up)
- [ ] Remove duplication
- [ ] Improve naming
- [ ] Add documentation

### Dependencies

- Blocked by: {task_ids or "none"}
- Blocks: {task_ids or "none"}

### Files

| Action | Path |
|--------|------|
| CREATE | `src/{path}/{name}.ts` |
| CREATE | `src/{path}/__tests__/{name}.test.ts` |
```

### 4. Layer Ordering (Clean Architecture)

Tasks should follow Clean Architecture layer order:

| Order | Layer | Content |
|-------|-------|---------|
| 1 | **Domain** | Entities, Value Objects, Domain Services |
| 2 | **Application** | Use Cases, Application Services, DTOs |
| 3 | **Adapters** | Controllers, Presenters, Gateways |
| 4 | **Infrastructure** | Repositories, External Services |

### 5. Output

Generate TASKS document and return status:

```python
# Write TASKS document
Write(
    file_path=f".claude/plans/{feature_name}-TASKS-PHASE-{phase_num}.md",
    content=tasks_document
)

# Return structured result
return {
    "status": "success",
    "tasks_path": f".claude/plans/{feature_name}-TASKS-PHASE-{phase_num}.md",
    "task_count": len(tasks),
    "tasks": [
        {"id": task.id, "subject": task.subject, "phase": phase_num}
        for task in tasks
    ]
}
```

### 6. Validation Before Output

Before completing, verify:

- [ ] All PHASEs have corresponding Tasks
- [ ] Each Task has clear AC
- [ ] Dependencies are correctly set
- [ ] TDD workflow is defined for each Task
- [ ] Layer order is maintained
