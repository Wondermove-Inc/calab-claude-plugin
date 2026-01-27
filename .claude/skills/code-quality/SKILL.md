---
# 원본: claude-monitoring-main
# 적용: calab-claude-plugin v2.3.0+
name: code-quality
description: 코드 품질 분석 및 개선. 코드 스멜 탐지, 리팩토링 가이드, 아키텍처 검토를 수행합니다.
allowed-tools:
  - Read
  - Grep
  - Glob
  - LSP
  - mcp__plugin_serena_serena__get_symbols_overview
  - mcp__plugin_serena_serena__find_symbol
  - mcp__plugin_serena_serena__find_referencing_symbols
---

# Code Quality

Analyze and improve code quality through systematic review, refactoring guidance, and best practice enforcement.

## Code Smells Detection

### Common Code Smells

```
  Smell          Description
  ─────────────  ─────────────────────────────────────────────────
  Long Method    Method doing too much (>50 lines)
  Large Class    Class with too many responsibilities
  Duplicate Code Copy-pasted logic
  Dead Code      Unused code
  Magic Numbers  Unexplained literals
  Deep Nesting   Too many indentation levels (>3)
  God Object     Object that knows/does too much
  Feature Envy   Method using other class's data excessively
  ─────────────  ─────────────────────────────────────────────────
```

### Detection Workflow

1. Analyze code structure using `get_symbols_overview`
2. Check for common patterns with Grep
3. Measure complexity metrics
4. Report findings with file:line locations

## Refactoring Patterns

### Extract Method

**Before**:
```typescript
function processOrder(order) {
  // validate
  if (!order.items) throw new Error('No items');
  if (!order.customer) throw new Error('No customer');

  // calculate total
  let total = 0;
  for (const item of order.items) {
    total += item.price * item.quantity;
  }

  // apply discount
  if (order.customer.isPremium) {
    total *= 0.9;
  }

  return total;
}
```

**After**:
```typescript
function processOrder(order) {
  validateOrder(order);
  const total = calculateTotal(order.items);
  return applyDiscount(total, order.customer);
}
```

### Replace Magic Numbers

**Before**:
```typescript
if (user.age >= 18) {
  if (order.total > 10000) {
    discount = order.total * 0.1;
  }
}
```

**After**:
```typescript
const ADULT_AGE = 18;
const DISCOUNT_THRESHOLD = 10000;
const DISCOUNT_RATE = 0.1;

if (user.age >= ADULT_AGE) {
  if (order.total > DISCOUNT_THRESHOLD) {
    discount = order.total * DISCOUNT_RATE;
  }
}
```

### Reduce Nesting

**Before**:
```typescript
function process(data) {
  if (data) {
    if (data.valid) {
      if (data.items.length > 0) {
        return data.items.map(item => item.value);
      }
    }
  }
  return [];
}
```

**After**:
```typescript
function process(data) {
  if (!data?.valid) return [];
  if (data.items.length === 0) return [];
  return data.items.map(item => item.value);
}
```

## Quality Metrics

### Complexity Thresholds

```
  Metric                   Good   Warning  Critical
  ───────────────────────  ─────  ───────  ────────
  Cyclomatic Complexity    < 10   10-20    > 20
  Lines per Function       < 50   50-100   > 100
  Parameters per Function  < 4    4-6      > 6
  Nesting Depth            < 3    3-5      > 5
  ───────────────────────  ─────  ───────  ────────
```

### Coverage Targets

```
  Type       Minimum  Recommended
  ─────────  ───────  ───────────
  Statement  70%      85%
  Branch     60%      80%
  Function   80%      90%
  ─────────  ───────  ───────────
```

## When to Use

Use this skill when you need to:

```
  Scenario                Primary Tool              When to Use
  ──────────────────────  ────────────────────────  ──────────────────────────────────────────
  Code smell detection    Grep + patterns           Find Long Method, Magic Numbers, Nesting
  Structure analysis      get_symbols_overview      Understand file/class organization
  Impact before refactor  find_referencing_symbols  Check what will break
  Dependency check        LSP findReferences        Trace symbol usage across codebase
  Architecture violation  Grep + layer patterns     Detect layer violations
  Duplicate code          Grep multiline            Find copy-pasted blocks
  ──────────────────────  ────────────────────────  ──────────────────────────────────────────
```

### Tool Selection Guide

```
  Task                      Best Tool                Alternative
  ────────────────────────  ───────────────────────  ─────────────────────────
  Find function usages      LSP findReferences       find_referencing_symbols
  Analyze file structure    get_symbols_overview     LSP documentSymbol
  Detect code patterns      Grep with regex          search_for_pattern
  Check import dependencies Grep "import|require"    get_symbols_overview
  Measure complexity        Read + count lines       -
  ────────────────────────  ───────────────────────  ─────────────────────────
```

### When NOT to Use

- Simple typo fixes → Edit directly
- Single-line changes → No analysis needed
- Already know exact location → Read directly

## Tools & Integration

### Serena Plugin
- `find_symbol` - Locate code for analysis
- `get_symbols_overview` - Structure analysis
- `find_referencing_symbols` - Impact analysis before refactoring

### LSP
- `findReferences` - Find all usages before changing
- `goToDefinition` - Navigate to implementation

### Grep/Glob
- Pattern-based code smell detection
- Find duplicate code blocks

## Plugin Integration

### code-review Plugin

Use `code-review@claude-plugins-official` for comprehensive code review:

```
  When                     How
  ───────────────────────  ───────────────────────────────────
  After completing feature Invoke /code-review skill
  PR review needed         Use plugin for systematic review
  Quality gate check       Run before commit
  ───────────────────────  ───────────────────────────────────
```

Invocation:
- Skill: `code-review:code-review`
- Focus: bugs, security, code quality, conventions

## Workflows

### Quality Audit

1. Read file content
2. Analyze structure and complexity with `get_symbols_overview`
3. Check for code smells using pattern matching
4. Measure metrics against thresholds
5. Provide improvement suggestions with priorities

### Refactoring Session

1. Analyze current implementation
2. Use `find_referencing_symbols` for impact analysis
3. Identify refactoring opportunities
4. Apply appropriate patterns
5. Verify tests still pass
6. Document changes

### Technical Debt Assessment

1. Scan codebase for issues using Grep patterns
2. Categorize by severity (Critical/Warning/Info)
3. Estimate effort to fix
4. Prioritize by impact
5. Create remediation plan

## Architecture Quality

### Architecture Smells

```
  Smell                Description
  ───────────────────  ───────────────────────────────────────────
  Layer Violation      Inner layer depends on outer layer
  Boundary Leak        Entity exposed outside Application
  Circular Dependency  Modules depend on each other
  God Module           Module with too many responsibilities
  Skip Layer           Controller directly calls Domain
  Framework Coupling   Domain depends on framework
  ───────────────────  ───────────────────────────────────────────
```

### Layer Dependency Rules

```
[Infrastructure] → [Adapters] → [Application] → [Domain]
     outer            ↓              ↓           inner
                  (inward only)
```

```
  Layer           May Depend On          Must NOT Depend On
  ──────────────  ─────────────────────  ─────────────────────────────────────────
  Domain          Nothing                Application, Adapters, Infrastructure
  Application     Domain                 Adapters, Infrastructure
  Adapters        Application, Domain    Infrastructure
  Infrastructure  All layers             -
  ──────────────  ─────────────────────  ─────────────────────────────────────────
```

### Architecture Anti-Patterns

**Domain Layer Violations:**
- ORM annotations in Domain entities
- HTTP Request/Response objects in Domain
- Framework dependencies in Domain

**Application Layer Violations:**
- Direct DB query execution
- HTTP request/response handling
- UI formatting logic

**Boundary Violations:**
- Entity passed directly to Controller
- ORM model used as API response
- Framework objects passed to inner layers

### Architecture Review Workflow

1. Identify layer structure using `get_symbols_overview`
2. Check dependency directions with `find_referencing_symbols`
3. Detect anti-patterns using Grep
4. Report violations with file:line locations
5. Suggest remediation steps

### Architecture Quality Gate

Checklist for architecture review:

- [ ] Domain layer has no external dependencies
- [ ] Application doesn't reference Infrastructure directly
- [ ] Data crossing boundaries uses DTOs
- [ ] External dependencies abstracted via interfaces
- [ ] No framework annotations in Domain entities

**Detailed Reference**: See [wm/rules/guide-clean-architecture.md](../wm/rules/policies/guide-clean-architecture.md)
