# Development Process (NEW_DEVELOPMENT / MODIFICATION)

Unified process for feature development and modification.

---

## Plan Template (Copy to Plan Document)

Copy this entire block to your plan document's `## 3. Execution Process (MUST)` section:

```markdown
## 3. Execution Process (MUST)

This plan is **{NEW_DEVELOPMENT|MODIFICATION}** type.

Execute in the following order:

- [ ] 1. `planner-phase` → PRD detailing {+ change scope analysis for MODIFICATION}
- [ ] 2. `design` → Architecture design {+ impact analysis for MODIFICATION}
- [ ] 3. `planner-task` → Task decomposition
- [ ] 3.1 `task-validator` → Task validation (HARD GATE)
- [ ] 4. `dev-executor` → Implementation
- [ ] 5. `qa` → Testing and verification {+ regression tests for MODIFICATION}
- [ ] 6. Cleanup (archive plan documents)

Steps 1-3.1 proceed sequentially (output dependencies).
Step 4 (dev-executor): **Parallel execution REQUIRED** for independent TASKs.

### Agents Used

| Agent | Purpose | Background |
|-------|---------|------------|
| `planner-phase` | PRD detailing, PHASE decomposition | Yes |
| `design` | Architecture design, ERD | Yes |
| `planner-task` | Task decomposition | Yes |
| `task-validator` | Task validation (HARD GATE) | Yes |
| `dev-executor` | Implementation | Yes |
| `qa` | Testing and verification | Yes |

## Agent Execution Log

| Agent | agentId | Status | Timestamp | Purpose |
|-------|---------|--------|-----------|---------|
| planner-phase | - | pending | - | PRD detailing |
| design | - | pending | - | Architecture design |
| planner-task | - | pending | - | Task decomposition |
| task-validator | - | pending | - | Task validation |
| dev-executor | - | pending | - | Implementation |
| qa | - | pending | - | Test verification |
```

---

## When to Use

| Type | When to Use |
|------|-------------|
| **NEW_DEVELOPMENT** | New feature that doesn't exist in codebase |
| **MODIFICATION** | Changes to existing features, API updates, refactoring |

### Examples

| Request | Type |
|---------|------|
| "Add user authentication" | NEW_DEVELOPMENT |
| "Change login to use OAuth" | MODIFICATION |
| "Refactor database layer" | MODIFICATION |
| "Add new API endpoint" | NEW_DEVELOPMENT |

---

## Agent Roles

| Agent | Base Role | MODIFICATION Additions |
|-------|-----------|------------------------|
| `planner-phase` | PRD detailing, PHASE decomposition | + Change scope analysis, impact assessment |
| `design` | Architecture design, ERD | + Compatibility review with existing design |
| `planner-task` | Task decomposition, TDD workflow | + Include regression test tasks |
| `task-validator` | Task validation (HARD GATE) | + Verify regression test inclusion |
| `dev-executor` | Implementation | + Integration with existing code |
| `qa` | Testing and verification | + **Regression tests required** |

---

## Execution Pattern

```python
# Sequential steps (1-3.1): Output dependencies
Task(subagent_type="calab-plugin:planner-phase", prompt="...", run_in_background=True)
# Wait for completion...
Task(subagent_type="calab-plugin:design", prompt="...", run_in_background=True)
# Wait for completion...
Task(subagent_type="calab-plugin:planner-task", prompt="...", run_in_background=True)
# Wait for completion...
Task(subagent_type="calab-plugin:task-validator", prompt="...", run_in_background=True)
# Wait for completion...

# Step 4: TaskList 기반 dev-executor 병렬 실행
all_tasks = TaskList()

def is_executable(task):
    """Task가 실행 가능한지 확인 (pending + blockedBy 모두 completed)"""
    if task.status != "pending":
        return False
    if not task.blockedBy:
        return True
    for dep_id in task.blockedBy:
        dep = TaskGet(taskId=dep_id)
        if dep.status != "completed":
            return False
    return True

# 의존성 순서대로 실행 (루프)
while any(t.status == "pending" for t in all_tasks):
    executable = [t for t in all_tasks if is_executable(t)]
    if not executable:
        break

    # 병렬 실행
    agents = []
    for task in executable:
        agent = Task(
            subagent_type="calab-plugin:dev-executor",
            prompt=f"Execute task: {task.id}\n{task.description}",
            run_in_background=True
        )
        agents.append((task.id, agent))
        TaskUpdate(taskId=task.id, status="in_progress")

    # 모든 병렬 실행 완료 대기
    for task_id, agent in agents:
        TaskOutput(task_id=agent.agent_id, block=True, timeout=300000)
        TaskUpdate(taskId=task_id, status="completed")

# Step 5: QA
Task(subagent_type="calab-plugin:qa", prompt="...", run_in_background=True)
```

---

## Parallel Execution (MUST)

Independent TASKs at step 4 (dev-executor) MUST execute in parallel.

### TaskList 기반 병렬 실행

1. **TaskList() 조회**: Claude Code Task 목록 자동 획득
2. **is_executable() 판단**: `status == "pending"` AND `blockedBy` 모두 completed
3. **병렬 실행**: 실행 가능한 모든 Task를 동시에 `run_in_background=True`로 실행
4. **완료 대기 후 루프**: 완료 후 다음 실행 가능 Task 그룹으로 진행

---

## Common Rules

1. **TaskList 기반 병렬 실행**: `TaskList()` 조회 후 `blockedBy == []`인 Task들을 병렬 실행
2. **task-validator is HARD GATE**: Cannot proceed to next step if validation fails
3. **Code changes through Agents**: Direct Edit/Write in Main context is prohibited
4. **Task 상태 관리**: 실행 전 `in_progress`, 완료 후 `completed`로 TaskUpdate

---

## MUST: Agent Execution Guidelines

**Key Requirements**:
1. Use `run_in_background=True` for all agents
2. Log agentId to plan's Agent Execution Log after launch
3. Steps 1-3.1 sequential; Step 4 (dev-executor) uses TaskList-based parallel execution
