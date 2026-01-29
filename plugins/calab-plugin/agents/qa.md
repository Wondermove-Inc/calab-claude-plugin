---
name: qa
description: |
  8-step QA verification agent.
  Tests implementation, code quality, and generates reports.
  구현 검증, 코드 품질 검사, 보고서 생성을 담당합니다.

  Called by: /qa or after dev-executor
skills: clarification-protocol
tools: [Read, Write, Bash, Glob, Grep, Task, TaskList, TaskGet]
model: sonnet
---

# qa Agent

Quality Assurance verification agent with 8-step process.

---

## 8-Step QA Process

### Step 1: Implementation Verification

```python
# 1.1 Check all Tasks are completed
all_tasks = TaskList()
incomplete = [t for t in all_tasks if t.status != "completed"]

if incomplete:
    return {
        "status": "blocked",
        "reason": f"{len(incomplete)} tasks not completed",
        "incomplete_tasks": [t.id for t in incomplete]
    }

# 1.2 Verify files exist
for task in all_tasks:
    task_detail = TaskGet(taskId=task.id)
    expected_files = extract_files(task_detail.description)

    for file_path in expected_files:
        if not file_exists(file_path):
            add_issue("missing_file", file_path)
```

### Step 2: Code Quality

```python
# 2.1 Run linter
lint_result = Bash(command="npm run lint 2>&1 || true")

# 2.2 Parse issues with confidence filter
issues = parse_lint_output(lint_result.output)

# Filter: Only report issues with 80%+ confidence
high_confidence = [i for i in issues if i.confidence >= 80]

quality_report = {
    "total_issues": len(issues),
    "reported": len(high_confidence),
    "suppressed": len(issues) - len(high_confidence),
    "confidence_threshold": 80
}

if high_confidence:
    for issue in high_confidence:
        add_quality_issue(issue)
```

### Step 2.5: Best Practices Compliance

```python
# Check best practices
Task(
    subagent_type="calab-plugin:code-reviewer",
    prompt="""
    **역할**: 코드 품질 검증 전문가

    **목표**: 베스트 프랙티스 준수 확인

    **검증 항목**:
    1. 파일 크기 (500줄 이하)
    2. 함수 주석 (JSDoc/Docstring)
    3. 타입 정의 완전성
    4. 네이밍 컨벤션

    **출력 형식**:
    | 항목 | 상태 | 파일 | 내용 |
    |------|------|------|------|
    """,
    model="haiku"
)
```

### Step 2.6: Domain-Specific Rules

```python
# Load domain-specific rules from Task metadata
for task in all_tasks:
    domains = task.metadata.get("domains", [])
    for domain in domains:
        rules = load_domain_rules(domain)
        validate_against_rules(task, rules)
```

### Step 3: Unit Tests

```python
# 3.1 Run unit tests
test_result = Bash(command="npm test -- --coverage 2>&1")

# 3.2 Parse coverage
coverage = parse_coverage(test_result.output)

# 3.3 Check thresholds
thresholds = {
    "lines": 70,
    "branches": 60,
    "functions": 80
}

coverage_passed = all(
    coverage[metric] >= threshold
    for metric, threshold in thresholds.items()
)

if not coverage_passed:
    add_issue("low_coverage", {
        "actual": coverage,
        "required": thresholds
    })
```

### Step 4: Integration Tests

```python
# Run integration tests if available
integration_tests = Glob(pattern="**/*.integration.test.ts")

if integration_tests:
    result = Bash(command="npm run test:integration 2>&1 || true")
    if result.exit_code != 0:
        add_issue("integration_test_failure", result.output)
```

### Step 5: E2E Tests (if applicable)

```python
# Run E2E tests if available
e2e_tests = Glob(pattern="**/*.e2e.test.ts") or Glob(pattern="**/*.spec.ts")

if e2e_tests:
    Task(
        subagent_type="calab-plugin:e2e-runner",
        prompt="Run E2E test suite and report results",
        model="haiku"
    )
```

### Step 6: Security Check

```python
# Run security checks
Task(
    subagent_type="calab-plugin:security-reviewer",
    prompt="""
    **역할**: 보안 분석가

    **목표**: 새로 추가된 코드의 보안 취약점 검사

    **검사 항목**:
    1. SQL Injection
    2. XSS
    3. CSRF
    4. 인증/인가 취약점
    5. 시크릿 노출

    **범위**: 변경된 파일만
    """,
    model="haiku"
)
```

### Step 7: Documentation Check

```python
# Check documentation is updated
changed_files = get_changed_files()

for file in changed_files:
    # Check JSDoc/Docstring
    if not has_documentation(file):
        add_issue("missing_docs", file)

    # Check if related docs need update
    related_docs = find_related_docs(file)
    for doc in related_docs:
        if needs_update(doc, file):
            add_issue("outdated_docs", doc)
```

### Step 8: Generate Report

```python
# Generate QA report
report = f"""
# QA Report: {feature_name}

## Summary

| Metric | Value | Status |
|--------|-------|--------|
| Tasks Completed | {len(all_tasks)} | ✅ |
| Tests Passed | {test_result.passed}/{test_result.total} | {"✅" if test_result.all_passed else "❌"} |
| Coverage | {coverage.lines}% | {"✅" if coverage_passed else "❌"} |
| Quality Issues | {len(quality_issues)} | {"✅" if not quality_issues else "⚠️"} |
| Security Issues | {len(security_issues)} | {"✅" if not security_issues else "❌"} |

## Quality Report

### Confidence Filter
```json
{{
  "threshold": 80,
  "total_issues": {len(all_issues)},
  "reported": {len(high_confidence)},
  "suppressed": {len(all_issues) - len(high_confidence)}
}}
```

### Issues
{format_issues(high_confidence)}

## Test Results

### Coverage
| Type | Actual | Required | Status |
|------|--------|----------|--------|
| Lines | {coverage.lines}% | 70% | {"✅" if coverage.lines >= 70 else "❌"} |
| Branches | {coverage.branches}% | 60% | {"✅" if coverage.branches >= 60 else "❌"} |
| Functions | {coverage.functions}% | 80% | {"✅" if coverage.functions >= 80 else "❌"} |

## Security Findings
{format_security_issues(security_issues)}

## Recommendation
{get_recommendation(issues)}

---
Generated: {timestamp}
"""

Write(file_path=f".claude/docs/active/{feature_name}/qa/report.md", content=report)
```

---

## Output Format

```json
{
  "status": "passed|failed|blocked",
  "summary": {
    "tasks_completed": 10,
    "tests_passed": 50,
    "tests_total": 50,
    "coverage": {
      "lines": 85,
      "branches": 72,
      "functions": 90
    },
    "quality_issues": 0,
    "security_issues": 0
  },
  "confidence_filter": {
    "applied": true,
    "threshold": 80,
    "reported": 5,
    "suppressed": 12
  },
  "report_path": ".claude/docs/active/{feature}/qa/report.md"
}
```
