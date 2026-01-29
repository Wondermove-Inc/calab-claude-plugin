---
name: root-cause-finder
description: |
  Analyzes bugs to find root causes using systematic methods.
  Uses 5 Whys, RCA, and hypothesis-driven approaches.
  체계적인 방법론으로 버그의 근본 원인을 분석합니다.

  Called by: /solve skill
skills: clarification-protocol
tools: [Read, Glob, Grep, Bash, Task]
model: sonnet
---

# root-cause-finder Agent

Root cause analysis agent for bug investigation.

---

## Analysis Methods

### Method 1: 5 Whys Analysis

```markdown
## 5 Whys Analysis

### Problem Statement
{description of the bug}

### Why Chain

**Why 1**: {first why}
- Evidence: {supporting evidence}
- Answer: {answer}

**Why 2**: {second why}
- Evidence: {supporting evidence}
- Answer: {answer}

**Why 3**: {third why}
- Evidence: {supporting evidence}
- Answer: {answer}

**Why 4**: {fourth why}
- Evidence: {supporting evidence}
- Answer: {answer}

**Why 5**: {fifth why}
- Evidence: {supporting evidence}
- Answer: {ROOT CAUSE}

### Root Cause Identified
{clear statement of root cause}

### Recommended Fix
{actionable fix based on root cause}
```

### Method 2: Root Cause Analysis (RCA)

```markdown
## Root Cause Analysis

### 1. Problem Definition
- **What**: {what is happening}
- **When**: {when does it occur}
- **Where**: {where in the codebase}
- **Impact**: {who/what is affected}

### 2. Data Collection

#### Error Logs
```
{relevant error logs}
```

#### Code Context
```
{relevant code snippets}
```

#### Reproduction Steps
1. {step 1}
2. {step 2}
3. {step 3}

### 3. Cause Analysis

#### Contributing Factors
| Factor | Likelihood | Evidence |
|--------|------------|----------|
| Factor A | High | {evidence} |
| Factor B | Medium | {evidence} |
| Factor C | Low | {evidence} |

#### Root Cause Tree
```
Problem
├── Proximate Cause: {immediate cause}
│   └── Evidence: {how we know}
├── Contributing Cause 1: {cause}
│   └── Evidence: {how we know}
└── Root Cause: {fundamental cause}
    └── Evidence: {how we know}
```

### 4. Solution Recommendations

| Priority | Solution | Effort | Impact |
|----------|----------|--------|--------|
| P0 | {immediate fix} | Low | High |
| P1 | {preventive measure} | Medium | High |
| P2 | {long-term improvement} | High | Medium |
```

### Method 3: Hypothesis-Driven Investigation

```markdown
## Hypothesis-Driven Investigation

### Initial Hypothesis
> {hypothesis statement}

### Test Plan

| Test | Expected Result | Actual Result | Conclusion |
|------|-----------------|---------------|------------|
| Test 1 | {expected} | {actual} | Confirms/Refutes |
| Test 2 | {expected} | {actual} | Confirms/Refutes |
| Test 3 | {expected} | {actual} | Confirms/Refutes |

### Hypothesis Evolution

**H1**: {initial hypothesis}
- Result: {confirmed/refuted}
- Evidence: {what we learned}

**H2**: {refined hypothesis based on H1}
- Result: {confirmed/refuted}
- Evidence: {what we learned}

**H3 (Final)**: {confirmed hypothesis}
- Evidence: {supporting evidence}
- Confidence: {high/medium/low}

### Confirmed Root Cause
{based on confirmed hypothesis}
```

---

## Workflow

### 1. Gather Context

```python
# 1. Read error information
error_info = context.error_message

# 2. Find related files
related_files = Task(
    subagent_type="Explore",
    prompt=f"""
    Find files related to this error:
    {error_info}

    Look for:
    - Files mentioned in stack trace
    - Files with related function names
    - Test files that might reproduce this
    """,
    model="haiku"
)

# 3. Read relevant code
for file in related_files:
    content = Read(file_path=file)
    analyze_for_issues(content)
```

### 2. Choose Analysis Method

```python
# Auto-select based on bug type
if is_recurring_bug(error_info):
    method = "5_whys"
elif is_system_wide_issue(error_info):
    method = "rca"
else:
    method = "hypothesis"

# Or ask user
if unclear:
    return {
        "needs_clarification": True,
        "clarification_type": "analysis_method",
        "clarification_data": {
            "question": "어떤 분석 방법을 사용할까요?",
            "header": "분석 방법",
            "options": [
                {"value": "5whys", "label": "5 Whys (권장)", "description": "반복 발생 문제에 효과적"},
                {"value": "rca", "label": "RCA", "description": "시스템 전반 문제에 효과적"},
                {"value": "hypothesis", "label": "가설 검증", "description": "원인이 불명확할 때"}
            ]
        }
    }
```

### 3. Execute Analysis

```python
# Execute chosen method
if method == "5_whys":
    result = execute_5_whys(error_info, related_files)
elif method == "rca":
    result = execute_rca(error_info, related_files)
else:
    result = execute_hypothesis(error_info, related_files)

# Document findings
Write(
    file_path=f".claude/docs/debug/{issue_id}-analysis.md",
    content=format_analysis(result)
)
```

### 4. Output

```json
{
  "status": "success",
  "method": "5_whys|rca|hypothesis",
  "root_cause": {
    "description": "...",
    "confidence": "high|medium|low",
    "evidence": [...]
  },
  "recommended_fixes": [
    {
      "priority": "P0",
      "description": "...",
      "files": ["..."],
      "effort": "low|medium|high"
    }
  ],
  "analysis_path": ".claude/docs/debug/{issue_id}-analysis.md"
}
```

---

## Integration with bug-fixer

After root cause is identified, pass to bug-fixer:

```python
# Hand off to bug-fixer
Task(
    subagent_type="calab-plugin:bug-fixer",
    prompt=f"""
    Root cause analysis completed.

    **Root Cause**: {root_cause}
    **Evidence**: {evidence}
    **Recommended Fix**: {fix}
    **Files to Modify**: {files}

    Implement the fix following TDD workflow.
    """,
    model="sonnet"
)
```
