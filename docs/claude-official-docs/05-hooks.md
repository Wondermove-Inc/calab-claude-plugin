# Hooks - Claude Code 공식 문서

> **출처**: https://code.claude.com/docs/en/hooks-guide

---

# Get started with Claude Code hooks

Learn how to customize and extend Claude Code's behavior by registering shell commands.

Claude Code hooks are user-defined shell commands that execute at various points in Claude Code's lifecycle. Hooks provide deterministic control over Claude Code's behavior, ensuring certain actions always happen rather than relying on the LLM to choose to run them.

## Example use cases

- **Notifications**: Customize how you get notified when Claude Code is awaiting your input
- **Automatic formatting**: Run `prettier` on .ts files, `gofmt` on .go files after every file edit
- **Logging**: Track and count all executed commands for compliance or debugging
- **Feedback**: Provide automated feedback when Claude Code produces code that does not follow your codebase conventions
- **Custom permissions**: Block modifications to production files or sensitive directories

> **Security Warning**: You must consider the security implication of hooks as they run automatically during the agent loop with your current environment's credentials. Always review your hooks implementation before registering them.

## Hook Events Overview

| Event | Description |
| --- | --- |
| **PreToolUse** | Runs before tool calls (can block them) |
| **PermissionRequest** | Runs when a permission dialog is shown (can allow or deny) |
| **PostToolUse** | Runs after tool calls complete |
| **UserPromptSubmit** | Runs when the user submits a prompt, before Claude processes it |
| **Notification** | Runs when Claude Code sends notifications |
| **Stop** | Runs when Claude Code finishes responding |
| **SubagentStop** | Runs when subagent tasks complete |
| **PreCompact** | Runs before Claude Code is about to run a compact operation |
| **SessionStart** | Runs when Claude Code starts a new session or resumes an existing session |
| **SessionEnd** | Runs when Claude Code session ends |

## Quickstart

### Prerequisites

Install `jq` for JSON processing in the command line.

### Step 1: Open hooks configuration

Run the `/hooks` slash command and select the `PreToolUse` hook event.

### Step 2: Add a matcher

Select `+ Add new matcher...` and type `Bash` to run your hook only on Bash tool calls.

You can use `*` to match all tools.

### Step 3: Add the hook

Select `+ Add new hook...` and enter this command:

```bash
jq -r '"\(.tool_input.command) - \(.tool_input.description // "No description")"' >> ~/.claude/bash-command-log.txt
```

### Step 4: Save your configuration

Select `User settings` since you're logging to your home directory. Press `Esc` to return to the REPL.

### Step 5: Verify your hook

Run `/hooks` again or check `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"\\(.tool_input.command) - \\(.tool_input.description // \"No description\")\"' >> ~/.claude/bash-command-log.txt"
          }
        ]
      }
    ]
  }
}
```

### Step 6: Test your hook

Ask Claude to run a simple command like `ls` and check your log file:

```bash
cat ~/.claude/bash-command-log.txt
```

You should see entries like:

```
ls - Lists files and directories
```

## More Examples

### Code Formatting Hook

Automatically format TypeScript files after editing:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | { read file_path; if echo \"$file_path\" | grep -q '\\.ts$'; then npx prettier --write \"$file_path\"; fi; }"
          }
        ]
      }
    ]
  }
}
```

### Markdown Formatting Hook

Automatically fix missing language tags and formatting issues in markdown files:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/markdown_formatter.py"
          }
        ]
      }
    ]
  }
}
```

Create `.claude/hooks/markdown_formatter.py`:

```python
#!/usr/bin/env python3
"""
Markdown formatter for Claude Code output.
Fixes missing language tags and spacing issues while preserving code content.
"""

import json
import sys
import re
import os

def detect_language(code):
    """Best-effort language detection from code content."""
    s = code.strip()

    # JSON detection
    if re.search(r'^\s*[{\[]', s):
        try:
            json.loads(s)
            return 'json'
        except:
            pass

    # Python detection
    if re.search(r'^\s*def\s+\w+\s*\(', s, re.M) or \
       re.search(r'^\s*(import|from)\s+\w+', s, re.M):
        return 'python'

    # JavaScript detection
    if re.search(r'\b(function\s+\w+\s*\(|const\s+\w+\s*=)', s) or \
       re.search(r'=>|console\.(log|error)', s):
        return 'javascript'

    # Bash detection
    if re.search(r'^#!.*\b(bash|sh)\b', s, re.M) or \
       re.search(r'\b(if|then|fi|for|in|do|done)\b', s):
        return 'bash'

    # SQL detection
    if re.search(r'\b(SELECT|INSERT|UPDATE|DELETE|CREATE)\s+', s, re.I):
        return 'sql'

    return 'text'

def format_markdown(content):
    """Format markdown content with language detection."""
    # Fix unlabeled code fences
    def add_lang_to_fence(match):
        indent, info, body, closing = match.groups()
        if not info.strip():
            lang = detect_language(body)
            return f"{indent}```{lang}\n{body}{closing}\n"
        return match.group(0)

    fence_pattern = r'(?ms)^([ \t]{0,3})```([^\n]*)\n(.*?)(\n\1```)\s*$'
    content = re.sub(fence_pattern, add_lang_to_fence, content)

    # Fix excessive blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content.rstrip() + '\n'

# Main execution
try:
    input_data = json.load(sys.stdin)
    file_path = input_data.get('tool_input', {}).get('file_path', '')

    if not file_path.endswith(('.md', '.mdx')):
        sys.exit(0)  # Not a markdown file

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        formatted = format_markdown(content)

        if formatted != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(formatted)
            print(f"✓ Fixed markdown formatting in {file_path}")

except Exception as e:
    print(f"Error formatting markdown: {e}", file=sys.stderr)
    sys.exit(1)
```

Make the script executable:

```bash
chmod +x .claude/hooks/markdown_formatter.py
```

### Custom Notification Hook

Get desktop notifications when Claude needs input:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Awaiting your input'"
          }
        ]
      }
    ]
  }
}
```

### File Protection Hook

Block edits to sensitive files:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -c \"import json, sys; data=json.load(sys.stdin); path=data.get('tool_input',{}).get('file_path',''); sys.exit(2 if any(p in path for p in ['.env', 'package-lock.json', '.git/']) else 0)\""
          }
        ]
      }
    ]
  }
}
```

## Hook Types

### Command hooks

Execute shell commands or scripts:

```json
{
  "type": "command",
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
}
```

### Prompt hooks

Evaluate a prompt with an LLM:

```json
{
  "type": "prompt",
  "prompt": "Analyze the following code change and provide feedback: $ARGUMENTS"
}
```

### Agent hooks

Run an agentic verifier with tools for complex verification tasks:

```json
{
  "type": "agent",
  "prompt": "Verify that the code changes follow our security guidelines"
}
```

## Available Events

| Event | When it runs | Can block? |
| --- | --- | --- |
| `PreToolUse` | Before tool calls | Yes (exit code 2) |
| `PermissionRequest` | When permission dialog shown | Yes |
| `PostToolUse` | After tool calls complete | No |
| `PostToolUseFailure` | After tool execution fails | No |
| `UserPromptSubmit` | When user submits prompt | No |
| `Notification` | When sending notifications | No |
| `Stop` | When Claude finishes responding | No |
| `SubagentStart` | When subagent starts | No |
| `SubagentStop` | When subagent completes | No |
| `SessionStart` | At session beginning | No |
| `SessionEnd` | At session end | No |
| `PreCompact` | Before conversation compacting | No |

## Blocking with exit codes

For `PreToolUse` hooks, use exit codes to control behavior:
- **Exit code 0**: Allow the tool to run
- **Exit code 2**: Block the tool execution
- **Other exit codes**: Log error but allow tool to run

## Learn more

- [Hooks reference](/docs/en/hooks) - Complete reference documentation
- [Security Considerations](/docs/en/hooks#security-considerations) - Security best practices
- [Debugging](/docs/en/hooks#debugging) - Troubleshooting techniques
