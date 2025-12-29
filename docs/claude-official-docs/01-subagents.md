# Subagents - Claude Code 공식 문서

> **출처**: https://code.claude.com/docs/en/sub-agents

---

# Subagents

Create and use specialized AI subagents in Claude Code for task-specific workflows and improved context management.

## What are subagents?

Subagents are specialized AI assistants that Claude can invoke for specific tasks. They provide focused expertise and maintain their own context, making them ideal for complex workflows.

## Key benefits

### Context preservation
Subagents maintain their own conversation context, preventing the main thread from becoming cluttered with task-specific details.

### Specialized expertise
Each subagent can be configured with specific prompts, tools, and capabilities for particular tasks.

### Reusability
Once created, subagents can be invoked repeatedly across different conversations and projects.

### Flexible permissions
Subagents can have their own tool permissions and permission modes.

## Quick start

1. Open the subagents interface: `/agents`
2. Select 'Create New Agent'
3. Define the subagent: Press `e` to edit
4. Save and use: `> Use the code-reviewer subagent to check my recent changes`

## Subagent configuration

### File locations

| Type | Location | Scope | Priority |
| --- | --- | --- | --- |
| **Project subagents** | `.claude/agents/` | Available in current project | Highest |
| **User subagents** | `~/.claude/agents/` | Available across all projects | Lower |

### Plugin agents

Plugins can provide subagents in their `agents/` directory. Plugin agents appear in `/agents` alongside user and project agents.

### CLI-based configuration

Use `--agents` flag to define subagents dynamically:

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

### File format

```markdown
---
name: your-sub-agent-name
description: Description of when this subagent should be invoked
tools: tool1, tool2, tool3 # Optional - inherits all tools if omitted
model: sonnet # Optional - specify model alias or 'inherit'
permissionMode: default # Optional - permission mode for the subagent
skills: skill1, skill2 # Optional - skills to auto-load
---

Your subagent's system prompt goes here. This can be multiple paragraphs
and should clearly define the subagent's role, capabilities, and approach
to solving problems.

Include specific instructions, best practices, and any constraints
the subagent should follow.
```

#### Configuration fields

| Field | Required | Description |
| --- | --- | --- |
| `name` | Yes | Unique identifier using lowercase letters and hyphens |
| `description` | Yes | Natural language description of the subagent's purpose |
| `tools` | No | Comma-separated list of specific tools. If omitted, inherits all tools from the main thread |
| `model` | No | Model to use: `sonnet`, `opus`, `haiku`, or `'inherit'` |
| `permissionMode` | No | Valid values: `default`, `acceptEdits`, `bypassPermissions`, `plan`, `ignore` |
| `skills` | No | Comma-separated list of skill names to auto-load |

### Model selection

- `sonnet` - Default, balanced performance
- `opus` - More capable, for complex tasks
- `haiku` - Faster, for simple tasks
- `'inherit'` - Use the main conversation's model

### Available tools

View available tools in `/agents`. If `tools` field is omitted, the subagent inherits all tools from the parent.

## Managing subagents

### Using the /agents command (Recommended)

Use `/agents` to create, edit, and manage subagents interactively.

### Direct file management

```bash
# Create a project subagent
mkdir -p .claude/agents
echo '---
name: test-runner
description: Use proactively to run tests and fix failures
---

You are a test automation expert. When you see code changes, proactively run the appropriate tests. If tests fail, analyze the failures and fix them while preserving the original test intent.' > .claude/agents/test-runner.md

# Create a user subagent
mkdir -p ~/.claude/agents
# ... create subagent file
```

## Using subagents effectively

### Automatic delegation

Claude automatically invokes subagents based on their `description` field when the task context matches.

### Explicit invocation

```
> Use the test-runner subagent to fix failing tests
> Have the code-reviewer subagent look at my recent changes
> Ask the debugger subagent to investigate this error
```

## Built-in subagents

### General-purpose subagent

Used for complex, multi-step tasks that require searching and modifying code.

```
User: Find all the places where we handle authentication and update them to use the new token format

Claude: [Invokes general-purpose subagent]
[Agent searches for auth-related code across codebase]
[Agent reads and analyzes multiple files]
[Agent makes necessary edits]
[Returns detailed writeup of changes made]
```

### Plan subagent

Used in plan mode to explore the codebase and design implementation approaches.

### Explore subagent

Fast agent specialized for exploring codebases:

```
User: Where are errors from the client handled?

Claude: [Invokes Explore subagent with "medium" thoroughness]
[Explore uses Grep to search for error handling patterns]
[Explore uses Read to examine promising files]
[Returns findings with absolute file paths]
Claude: Client errors are handled in src/services/process.ts:712...
```

## Example subagents

### Code reviewer

```markdown
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

### Debugger

```markdown
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.
```

### Data scientist

```markdown
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.
```

## Best practices

1. **Write clear descriptions**: The description field determines when Claude invokes the subagent
2. **Limit tool access**: Only grant tools the subagent actually needs
3. **Keep prompts focused**: Each subagent should have a clear, specific purpose
4. **Test iteratively**: Refine prompts based on actual usage patterns

## Advanced usage

### Chaining subagents

```
> First use the code-analyzer subagent to find performance issues, then use the optimizer subagent to fix them
```

### Dynamic subagent selection

Claude uses the `description` field to automatically select appropriate subagents for tasks.

### Resumable subagents

Subagents can be resumed using their `agentId`. The conversation is saved to `agent-{agentId}.jsonl`.

```
> Use the code-analyzer agent to start reviewing the authentication module

[Agent completes initial analysis and returns agentId: "abc123"]
```

```
> Resume agent abc123 and now analyze the authorization logic as well

[Agent continues with full context from previous conversation]
```

Use the `resume` parameter in the Task tool to continue a previous agent execution:

```json
{
  "description": "Continue analysis",
  "prompt": "Now examine the error handling patterns",
  "subagent_type": "code-analyzer",
  "resume": "abc123"
}
```

## Performance considerations

- Subagents start fresh contexts, so provide necessary information in the invocation
- Consider using haiku model for simple, repetitive tasks
- Use specific tool lists to reduce overhead

## Related documentation

- [Agent Skills](/docs/en/skills)
- [Plugins](/docs/en/plugins)
- [Hooks](/docs/en/hooks)
