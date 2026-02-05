> **Behavioral rules for Claude Code that guarantee consistent development quality in every situation.**

---

## Table of Contents

1. [Plugin Overview](#plugin-overview)
2. [Core Principles (5 Rules)](#core-principles-5-rules)
3. [Agent Guide](#agent-guide)
4. [Verification & Reinforcement](#verification--reinforcement)
5. [Skills](#skills)
6. [Workflows](#workflows)
7. [Quality Rules](#quality-rules)
8. [Session Management](#session-management)

---

## Plugin Overview

### Composition

```
17 Skills (10 active + 7 passive) + 23 Agents + 26 Hooks
```

| Area | Automation |
|------|-----------|
| **Development Workflow** | Plan → Discuss → Design → Tasks → Build (Wave parallelism) |
| **Code Quality** | Best practices, 500-line limit, mandatory comments |
| **Problem Solving** | 5 Whys, RCA, hypothesis-driven debugging |
| **Work Tracking** | Worktree progress + phase roadmap management |

### Skill Structure

| Type | Skills | Role |
|------|--------|------|
| **Active (Core)** | dev, solve, onboard | Development / Problem solving / Onboarding |
| **Active (Utility)** | docs, security, research, jira, refactor, e2e, guard | Docs / Security / Research / JIRA / Refactoring / E2E / Rule enforcement |
| **Passive** | best-practices, code-quality, tdd-workflow, project-rules, work-tracker, clarification-protocol, skill-completion-rules | Auto-loaded |

---

## Core Principles (5 Rules)

### 1. Zero Hallucination

```
❌ Never guess about unread code
✅ Read the file first, then respond
✅ If uncertain, acknowledge "needs verification"
```

### 2. 100% Agent Utilization

| Task | Agent |
|------|-------|
| Codebase exploration | `Explore` |
| Code review | `calab-plugin:code-reviewer` |
| Security audit | `calab-plugin:security-reviewer` |
| Completeness validation | `calab-plugin:validator` |
| Web research | `calab-plugin:web-researcher` |

### 3. Mandatory Task Completion Verification

> **Do not proceed to the next Task until AC is 100% satisfied.**

- [ ] AC 100% satisfied
- [ ] Functional behavior confirmed
- [ ] Edge cases handled
- [ ] Code quality (500 lines max, comments, types)

### 4. User Checkpoint Classification

| Type | Frequency | Handling |
|------|-----------|---------|
| **human-verify** | 90% | Concise summary + auto-proceed option |
| **decision** | 9% | Trade-off analysis + recommended option |
| **human-action** | 1% | Step-by-step guide + wait for completion |

> If you can decide on your own, don't ask. Only ask when the cost of reversal is high.

### 5. Context Preservation (50% Budget Rule)

- `.claude/memory/CURRENT_CONTEXT.md` — Current work state
- `.claude/memory/PROJECT_RULES.md` — Project rules

| Usage | Quality | Action |
|-------|---------|--------|
| **0-30%** | PEAK | Optimal zone |
| **30-50%** | GOOD | Target completion zone |
| **50-70%** | DEGRADING | Efficiency mode — omissions may occur |
| **70%+** | POOR | Immediate isolation — save checkpoint |

---

## Agent Guide

### Namespace Convention

| Type | Invocation | Example |
|------|-----------|---------|
| **Built-in** | No prefix | `subagent_type="Explore"` |
| **Plugin** | `calab-plugin:` required | `subagent_type="calab-plugin:validator"` |

### Built-in Agents (3)

| Agent | Role |
|-------|------|
| **Explore** | Codebase exploration |
| **Plan** | Implementation planning |
| **general-purpose** | General-purpose tasks |

### Plugin Agents (23)

| Agent | Role |
|-------|------|
| `code-reviewer` | Code quality review |
| `security-reviewer` | Security vulnerability analysis |
| `validator` | Completeness / AC verification |
| `reinforcer` | Remediation of validation failures |
| `build-error-resolver` | Build error resolution |
| `root-cause-finder` | Root cause analysis |
| `bug-fixer` | TDD-based bug fixing |
| `planner-phase` | PRD and phase decomposition |
| `planner-task` | Task breakdown (TDD) |
| `design` | Architecture / ERD design |
| `dev-executor` | TDD implementation execution |
| `qa` | 8-stage QA verification |
| `web-researcher` | Web search and collection |
| `deep-researcher` | Deep research and synthesis |
| `doc-updater` | Automatic documentation updates |
| `docs-generator` | Code-based documentation generation |
| `project-onboarder` | Project onboarding |
| `project-guardian` | Rule compliance enforcement |
| `jira-connector` | Bidirectional JIRA synchronization |
| `refactor-cleaner` | Dead code cleanup |
| `e2e-runner` | E2E test execution |
| `task-validator` | Task breakdown validation |
| `dev-workflow` | Development workflow orchestration |

### Prompt Required 7 Elements (RGOSWOC)

| Element | Description |
|---------|------------|
| **R**ole | Role definition |
| **G**oal | Achievement target |
| **O**bjective | Specific objectives |
| **S**cope | Work scope |
| **W**orkflow | Execution sequence |
| **O**utput | Output format |
| **C**onstraints | Constraints |

### 6-Element Task Specification (Specificity Test)

> **"Can another Claude instance execute this without asking questions?"**

| Element | Description |
|---------|------------|
| **What** | What to implement (specific functionality) |
| **How** | Implementation method (technology, patterns) |
| **Avoid + WHY** | Prohibitions + reasoning |
| **Verify** | Verification commands |
| **Done** | Completion criteria (AC) |
| **Files** | Files to create / modify |

### Structured Returns (Inter-Agent Communication)

> All verification/review agents return text + structured JSON results.

| Agent | Result Values |
|-------|--------------|
| `validator` | `passed\|warning\|failed\|critical` + `confidence_score` |
| `code-reviewer` | `passed\|needs_improvement\|failed` + `issues[]` |
| `security-reviewer` | `clean\|warning\|vulnerable\|critical` + `findings[]` |
| `dev-executor` | `success\|failure\|needs_clarification` + `deviations[]` |

### Deviation Rules (dev-executor Auto-Fix)

| Auto-fix (no confirmation) | User confirmation required |
|---------------------------|---------------------------|
| Bug / type error fixes | Architecture changes |
| Security vulnerability fixes | Public API changes |
| Missing error handling / validation | Scope creep |
| Dependency / import fixes | Deleting existing files / functions |
| Broken test fixes | |

### Parallel vs Sequential Execution

| Scenario | Execution |
|----------|-----------|
| Independent investigations | **Parallel** |
| Output feeds next stage | **Sequential** |
| File modification tasks | **Sequential** (conflict prevention) |
| Tasks within a Wave | **Parallel** (Fresh Context) |

### Fresh Context Pattern

> **The orchestrator manages only task definitions. It never reads implementation code directly.**

| Item | Rule |
|------|------|
| Orchestrator | Reads only task definitions + worktree.json |
| Executor | Runs independently with fresh 200k context |
| Never pass | Previous task implementation results or history |

### Wave-Based Parallel Execution

```
Wave 1: [TASK-001] [TASK-002]  ← Parallel (no dependencies)
Wave 2: [TASK-003]             ← After Wave 1 completes
Wave 3: [TASK-004] [TASK-005]  ← After Wave 2 completes
```

### Model Profile Management

| Profile | Description | Cost |
|---------|------------|------|
| **quality** | All stages use Opus | 100% |
| **balanced** | Planning uses Opus + execution uses Sonnet (recommended) | ~60% |
| **budget** | All stages use Haiku/Sonnet | ~30% |

Configuration: `.claude/settings/model-profile.json`

---

## Verification & Reinforcement

### Mandatory Verification Chain

```
Implementation → Validator (3-Level + Goal-Backward) → (on failure) Reinforcer → Validator (re-verify)
```

| Step | Agent | Role |
|------|-------|------|
| 1 | Implementation agent | Write code |
| 2 | `validator` | AC / completeness verification **mandatory** (3-Level Artifact + Goal-Backward) |
| 3 | `code-reviewer` | Quality review |
| 4 | `security-reviewer` | Security audit (API / auth) |
| 5 | `reinforcer` | Level-specific remediation (on failure) |
| 6 | `validator` | Re-verification **mandatory** |

### 3-Level Artifact Verification

| Level | Checks | Confidence Impact |
|-------|--------|-------------------|
| **L1: Existence** | File / function existence | Baseline |
| **L2: Substantive** | AC implementation, error handling, type definitions | Medium |
| **L3: Wired** | Import connections, router registration, test linkage | High |

### Goal-Backward Verification

```
User Goal → Observable Truth → Code Artifact → Key Link (reverse trace)
```

### Confidence-Based Escalation

| Confidence | Action |
|-----------|--------|
| 90%+ | Proceed to next Task |
| 70-89% | Invoke reinforcer |
| 50-69% | User confirmation |
| <50% | Escalate to `/solve` |

### Plan Checker Loop

> During task breakdown, planner-task self-verifies (max 3 rounds), then task-validator performs final validation.

```
planner-task → self_verify (3 rounds) → task-validator (final)
```

### Verification Bypass Prohibited

| Scenario | Required Agent |
|----------|---------------|
| New file creation | `code-reviewer` |
| API endpoint | `code-reviewer` + `security-reviewer` |
| Auth / authorization logic | `security-reviewer` |
| Task completion | `validator` |

---

## Skills

### Core Skills (3)

| Skill | Command | Role |
|-------|---------|------|
| **dev** | `/dev --plan/--discuss/--design/--tasks/--build/--roadmap` | Development workflow |
| **solve** | `/solve --5whys/--rca/--hypothesis` | Problem solving |
| **onboard** | `/onboard` | Project analysis |

### Passive Skills (7)

| Skill | Trigger |
|-------|---------|
| `best-practices` | Technology keywords |
| `code-quality` | Code generation / modification |
| `tdd-workflow` | `--tdd`, test keywords |
| `project-rules` | All code writing |
| `work-tracker` | Source file modification |
| `clarification-protocol` | Subagent execution |
| `skill-completion-rules` | Active skill completion |

### Workflow Integration

```
/onboard → /dev --plan → --discuss → --design → --tasks → --build → QA
               (ROADMAP)  (optional)               (Wave)   (Wave parallel)
                                                                ↓
                                                          On failure → /solve
```

### solve ↔ dev Transition Criteria

| Scenario | Transition |
|----------|-----------|
| New feature needed | `/dev --plan` |
| 3+ modules affected | `/dev --design` |
| Simple code fix | Resolve within `/solve` |
| Build errors 3+ times | `/solve --5whys` |

---

## Workflows

### New Project

```bash
/onboard   # Project analysis
```

### Feature Development

```bash
/dev --plan [feature]         # PRD authoring + ROADMAP.md generation
/dev --discuss                # Resolve gray areas (optional)
/dev --design                 # Architecture design
/dev --tasks                  # Task breakdown (Wave assignment)
/dev --build --all            # Wave parallel execution
/dev --build TASK-001         # Single task execution
/dev --roadmap complete 1     # Complete phase → next phase
/dev --roadmap milestone "v1.0.0"  # Create milestone
```

### Problem Solving

```bash
/solve [error message]   # Auto-selects methodology
/solve --5whys           # 5 Whys analysis
/solve --rca             # Root Cause Analysis
```

---

## Quality Rules

### Code Quality

| Item | Standard |
|------|----------|
| File size | 500 lines max |
| Function comments | Required on all functions |
| Type definitions | 100% coverage |

### Test Coverage

| Item | Minimum | Recommended |
|------|---------|-------------|
| Lines | 70% | 80% |
| Branches | 60% | 70% |
| Functions | 80% | 90% |

---

## Session Management

### State Files

| File | Purpose |
|------|---------|
| `.claude-state/checkpoint.json` | Detailed state |
| `.claude-state/worktree.json` | Work tree (includes Wave / Phase) |
| `.claude/docs/active/{feature}/ROADMAP.md` | Phase roadmap |
| `.claude/memory/CURRENT_CONTEXT.md` | Emergency recovery |

### Recovery Priority

```
1. checkpoint.json → 2. worktree.json → 3. CURRENT_CONTEXT.md → 4. /onboard
```

### Automatic Behaviors

| Trigger | Action |
|---------|--------|
| Code writing | Quality check |
| File modification | Worktree update |
| Session start | Context guidance + log rotation |
| Compact | Checkpoint save |
| Build error | Invoke `build-error-resolver` |

---

## Mandatory Artifacts

### Per-Skill Artifacts

| Skill | Artifact | Path |
|-------|----------|------|
| `/dev --plan` | PRD + ROADMAP | `.claude/docs/active/{feature}/01-PRD.md`, `ROADMAP.md` |
| `/dev --discuss` | Implementation decisions | `.claude/docs/active/{feature}/00-CONTEXT.md` |
| `/dev --design` | Architecture | `.claude/docs/active/{feature}/02-architecture.md` |
| `/dev --tasks` | Task list | `.claude/docs/active/{feature}/03-tasks.md` |
| `/solve` | Resolution report | `.claude/problem-solving/resolved/{id}/report.md` |
| `/onboard` | Context documents | `.claude/project-context/` |

### Per-Agent Artifacts

| Agent | Artifact |
|-------|----------|
| `validator` | `.claude/docs/active/{feature}/validation-report.md` |
| `reinforcer` | `.claude/docs/active/{feature}/reinforcer-report.md` |
| `build-error-resolver` | `.claude/docs/active/{feature}/build-error-report.md` |

> **Failure to produce artifacts is treated as task failure.**

---

## Command Reference

### Core Skills

| Command | Options |
|---------|---------|
| `/dev` | `--plan`, `--discuss`, `--design`, `--tasks`, `--build [ID\|--wave N\|--all]`, `--roadmap [add\|insert\|remove\|complete\|milestone]`, `--status` |
| `/solve` | `--5whys`, `--rca`, `--hypothesis`, `--log`, `--report` |
| `/onboard` | `--quick`, `--full`, `--phase N`, `--skip-domain` |

### Utility Skills

| Command | Options | Purpose |
|---------|---------|---------|
| `/docs` | `--api`, `--component`, `--guide` | Documentation generation |
| `/security` | `--owasp`, `--secrets`, `--deps` | Security scanning |
| `/research` | `--deep`, `--compare` | Web research |
| `/jira` | `--sync`, `--create`, `--update` | JIRA integration |
| `/refactor` | `--dead-code`, `--duplicates`, `--imports` | Refactoring |
| `/e2e` | `--run`, `--debug`, `--record` | E2E testing |
| `/guard` | `--rules`, `--context`, `--full` | Rule enforcement |

### Agent Invocation

```bash
"Run a quality check with code-reviewer"
"Run a security scan with security-reviewer"
"Research this with web-researcher"
```

---

## Skill Autocomplete (Link Setup)

To show plugin skills in `/` tab-completion:

```bash
# Run from the repository root
./link-skills.sh
```

Result: Creates `~/.claude/skills/calab-*` symlinks

```bash
/calab-dev --plan feature-name     # Development workflow
/calab-solve error-message         # Problem solving
/calab-docs --api src/api/         # Documentation generation
```

Remove: `./link-skills.sh --remove`
