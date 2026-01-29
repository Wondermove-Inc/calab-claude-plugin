---
name: task-validator
description: |
  Validates Task decomposition against PHASE planning.
  Ensures planner-phase output is correctly reflected in planner-task output.
  Task 분해가 PHASE 계획과 일치하는지 검증합니다.

  Called by: /dev workflow after planner-task
skills: project-rules, clarification-protocol
tools: [Read, Glob, Grep, TaskList, TaskGet]
model: sonnet
---

# task-validator Agent

Validation agent for Task decomposition quality assurance.

Ensures that:
1. All PHASEs from planner-phase have corresponding Tasks
2. PRD objectives are reflected in Tasks
3. Task ordering respects PHASE dependencies
4. Clean Architecture layer order is maintained
5. Task completeness (required fields present)

---

## Workflow

### 1. Load Context

```python
# 1. Read PRD document
prd = Read(f".claude/plans/{feature_name}.md")
# Extract: PHASE list, PRD objectives, dependencies

# 2. Load Tasks via TaskList
all_tasks = TaskList()

# 3. Feature filtering
feature_tasks = [
    task for task in all_tasks
    if task.metadata.get("feature") == feature_name
]

# 4. Group by PHASE
tasks_by_phase = {}
for task in feature_tasks:
    phase = task.metadata.get("phase")
    if phase not in tasks_by_phase:
        tasks_by_phase[phase] = []
    tasks_by_phase[phase].append(task)
```

### 2. Validation Checks

#### Check 1: PHASE Coverage

```python
# Verify all PHASEs have corresponding Tasks
affected_phases = []

expected_phases = [phase.number for phase in prd.phases]
covered_phases = set(
    task.metadata.get("phase")
    for task in feature_tasks
    if task.metadata.get("phase")
)

for phase_num in expected_phases:
    if phase_num not in covered_phases:
        affected_phases.append(phase_num)
        add_issue("phase_missing", phase_num)

# Track for clarification
if affected_phases:
    clarification_data["affected_phases"] = sorted(affected_phases)
```

**Pass Criteria**:
- Every PHASE in PRD has corresponding Tasks
- Each PHASE has at least one Task
- Tasks have required metadata (phase, tdd_stage, layer)

#### Check 2: PRD Objective Mapping

```python
# Verify PRD objectives are reflected in Tasks
missing_objectives = []

for objective in prd.objectives:
    found = False

    for task in feature_tasks:
        task_detail = TaskGet(taskId=task.id)
        if objective_matches(task_detail.description, objective):
            found = True
            break

    if not found:
        missing_objectives.append(objective)
        add_issue("objective_not_covered", objective)

if missing_objectives:
    clarification_data["missing_objectives"] = missing_objectives
```

**Pass Criteria**:
- Each PRD objective maps to at least one Task
- Task descriptions reference objectives they fulfill

#### Check 3: Dependency Order

```python
# Verify Task order respects dependencies
circular_deps = []
order_violations = []

for task in feature_tasks:
    task_detail = TaskGet(taskId=task.id)
    blocked_by = task_detail.blockedBy or []

    for dep_id in blocked_by:
        dep = TaskGet(taskId=dep_id)

        # Check for circular dependencies
        if has_circular_dependency(task.id, dep_id):
            circular_deps.append((task.id, dep_id))

        # Check layer order (Clean Architecture)
        if violates_layer_order(task, dep):
            order_violations.append({
                "task": task.id,
                "dependency": dep_id,
                "reason": "Layer order violation"
            })

if circular_deps:
    add_issue("circular_dependency", circular_deps)
if order_violations:
    add_issue("layer_order_violation", order_violations)
```

**Pass Criteria**:
- No circular dependencies
- Dependencies follow Clean Architecture layer order

#### Check 4: Task Completeness

```python
# Verify each Task has required fields
incomplete_tasks = []

required_fields = [
    "subject",
    "description",
    "acceptance_criteria",
    "tdd_stage",
    "layer"
]

for task in feature_tasks:
    task_detail = TaskGet(taskId=task.id)
    missing_fields = []

    for field in required_fields:
        if not has_field(task_detail, field):
            missing_fields.append(field)

    if missing_fields:
        incomplete_tasks.append({
            "task_id": task.id,
            "missing": missing_fields
        })

if incomplete_tasks:
    add_issue("incomplete_task", incomplete_tasks)
```

**Pass Criteria**:
- All Tasks have required fields populated
- Acceptance criteria are testable

### 3. Validation Result

```python
if issues:
    # HARD GATE: Cannot proceed if validation fails
    return {
        "status": "validation_failed",
        "issues": issues,
        "needs_clarification": True,
        "clarification_type": "validation_failure",
        "clarification_data": {
            "question": f"Task 검증에서 {len(issues)}개의 문제가 발견되었습니다. 어떻게 진행할까요?",
            "header": "검증 실패",
            "options": [
                {"value": "fix_auto", "label": "자동 수정 (권장)", "description": "planner-task 재실행"},
                {"value": "proceed", "label": "무시하고 진행", "description": "문제를 나중에 처리"},
                {"value": "manual", "label": "수동 수정", "description": "직접 Task 수정"}
            ],
            "affected_phases": affected_phases
        }
    }

return {
    "status": "validation_passed",
    "checks": {
        "phase_coverage": "passed",
        "objective_mapping": "passed",
        "dependency_order": "passed",
        "task_completeness": "passed"
    },
    "task_count": len(feature_tasks),
    "phase_count": len(tasks_by_phase)
}
```

---

## Validation Summary Report

```markdown
## Task Validation Report

### Summary
- **Feature**: {feature_name}
- **Total Tasks**: {count}
- **PHASEs Covered**: {phase_count}
- **Status**: {PASSED|FAILED}

### Check Results

| Check | Status | Details |
|-------|--------|---------|
| PHASE Coverage | ✅/❌ | {details} |
| Objective Mapping | ✅/❌ | {details} |
| Dependency Order | ✅/❌ | {details} |
| Task Completeness | ✅/❌ | {details} |

### Issues Found
{list of issues if any}

### Recommendation
{next steps}
```
