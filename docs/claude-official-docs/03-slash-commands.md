# Slash Commands - Claude Code 공식 문서

> **출처**: https://code.claude.com/docs/en/slash-commands

---

# Slash commands

Control Claude's behavior during an interactive session with slash commands.

## Built-in slash commands

| Command | Purpose |
| --- | --- |
| `/add-dir` | Add additional working directories |
| `/agents` | Manage custom AI subagents for specialized tasks |
| `/bashes` | List and manage background tasks |
| `/bug` | Report bugs (sends conversation to Anthropic) |
| `/clear` | Clear conversation history |
| `/compact [instructions]` | Compact conversation with optional focus instructions |
| `/config` | Open the Settings interface (Config tab) |
| `/context` | Visualize current context usage as a colored grid |
| `/cost` | Show token usage statistics |
| `/doctor` | Checks the health of your Claude Code installation |
| `/exit` | Exit the REPL |
| `/export [filename]` | Export the current conversation to a file or clipboard |
| `/help` | Get usage help |
| `/hooks` | Manage hook configurations for tool events |
| `/ide` | Manage IDE integrations and show status |
| `/init` | Initialize project with `CLAUDE.md` guide |
| `/install-github-app` | Set up Claude GitHub Actions for a repository |
| `/login` | Switch Anthropic accounts |
| `/logout` | Sign out from your Anthropic account |
| `/mcp` | Manage MCP server connections and OAuth authentication |
| `/memory` | Edit `CLAUDE.md` memory files |
| `/model` | Select or change the AI model |
| `/output-style [style]` | Set the output style directly or from a selection menu |
| `/permissions` | View or update permissions |
| `/plugin` | Manage Claude Code plugins |
| `/pr-comments` | View pull request comments |
| `/privacy-settings` | View and update your privacy settings |
| `/release-notes` | View release notes |
| `/rename` | Rename the current session for easier identification |
| `/resume [session]` | Resume a conversation by ID or name |
| `/review` | Request code review |
| `/rewind` | Rewind the conversation and/or code |
| `/sandbox` | Enable sandboxed bash tool with filesystem and network isolation |
| `/security-review` | Complete a security review of pending changes |
| `/stats` | Visualize daily usage, session history, streaks, and model preferences |
| `/status` | Open the Settings interface (Status tab) |
| `/statusline` | Set up Claude Code's status line UI |
| `/terminal-setup` | Install Shift+Enter key binding for newlines |
| `/todos` | List current TODO items |
| `/usage` | Show plan usage limits and rate limit status |
| `/vim` | Enter vim mode for alternating insert and command modes |

## Custom slash commands

Custom slash commands allow you to define frequently used prompts as Markdown files that Claude Code can execute.

### Syntax

```
/<command-name> [arguments]
```

### Command types

#### Project commands

Commands stored in your repository and shared with your team.

**Location**: `.claude/commands/`

```bash
# Create a project command
mkdir -p .claude/commands
echo "Analyze this code for performance issues and suggest optimizations:" > .claude/commands/optimize.md
```

#### Personal commands

Commands available across all your projects.

**Location**: `~/.claude/commands/`

```bash
# Create a personal command
mkdir -p ~/.claude/commands
echo "Review this code for security vulnerabilities:" > ~/.claude/commands/security-review.md
```

### Features

#### Namespacing

Use subdirectories to group related commands:
- `.claude/commands/frontend/component.md` creates `/component` with description "(project:frontend)"
- `~/.claude/commands/component.md` creates `/component` with description "(user)"

#### Arguments

##### All arguments with `$ARGUMENTS`

```markdown
# Command definition
echo 'Fix issue #$ARGUMENTS following our coding standards' > .claude/commands/fix-issue.md

# Usage
> /fix-issue 123 high-priority
# $ARGUMENTS becomes: "123 high-priority"
```

##### Individual arguments with `$1`, `$2`, etc.

```markdown
# Command definition
echo 'Review PR #$1 with priority $2 and assign to $3' > .claude/commands/review-pr.md

# Usage
> /review-pr 456 high alice
# $1 becomes "456", $2 becomes "high", $3 becomes "alice"
```

#### Bash command execution

Execute bash commands before the slash command runs using the `!` prefix:

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

## Context
- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task
Based on the above changes, create a single git commit.
```

#### File references

Include file contents using the `@` prefix:

```markdown
# Reference a specific file
Review the implementation in @src/utils/helpers.js

# Reference multiple files
Compare @src/old-version.js with @src/new-version.js
```

#### Thinking mode

Slash commands can trigger extended thinking by including extended thinking keywords.

### Frontmatter

| Frontmatter | Purpose | Default |
| --- | --- | --- |
| `allowed-tools` | List of tools the command can use | Inherits from the conversation |
| `argument-hint` | The arguments expected for the slash command | None |
| `description` | Brief description of the command | Uses the first line from the prompt |
| `model` | Specific model string | Inherits from the conversation |
| `disable-model-invocation` | Whether to prevent SlashCommand tool from calling this command | false |

Example:

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
argument-hint: [message]
description: Create a git commit
model: claude-3-5-haiku-20241022
---

Create a git commit with message: $ARGUMENTS
```

## Plugin commands

Plugins can provide custom slash commands that integrate seamlessly with Claude Code.

### How plugin commands work

- **Namespaced**: Commands use the format `/plugin-name:command-name`
- **Automatically available**: Once a plugin is installed, its commands appear in `/help`
- **Fully integrated**: Support all command features

### Invocation patterns

```
# Direct command (when no conflicts)
/command-name

# Plugin-prefixed (when needed for disambiguation)
/plugin-name:command-name

# With arguments
/command-name arg1 arg2
```

## MCP slash commands

MCP servers can expose prompts as slash commands.

### Command format

```
/mcp__<server>__<prompt> [arguments]
```

### Features

#### Dynamic discovery

MCP commands are automatically available when:
- An MCP server is connected and active
- The server exposes prompts through the MCP protocol

#### Arguments

```
# Without arguments
> /mcp__github__list_prs

# With arguments
> /mcp__github__pr_review 456
> /mcp__jira__create_issue "Bug title" high
```

### Managing MCP connections

Use `/mcp` to:
- View all configured MCP servers
- Check connection status
- Authenticate with OAuth-enabled servers
- Clear authentication tokens
- View available tools and prompts

### MCP permissions and wildcards

```
# Approve all tools from an MCP server
mcp__github
mcp__github__*

# Approve specific tools
mcp__github__get_issue
mcp__github__list_issues
```

## SlashCommand tool

The `SlashCommand` tool allows Claude to execute custom slash commands programmatically.

### Disable SlashCommand tool

```
/permissions
# Add to deny rules: SlashCommand
```

### Disable specific commands only

Add `disable-model-invocation: true` to the command's frontmatter.

### SlashCommand permission rules

- **Exact match**: `SlashCommand:/commit`
- **Prefix match**: `SlashCommand:/review-pr:*`

### Character budget limit

- **Default limit**: 15,000 characters
- **Custom limit**: Set via `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable

## Skills vs slash commands

### Use slash commands for

**Quick, frequently used prompts**:
- Simple prompt snippets you use often
- Quick reminders or templates
- Frequently used instructions that fit in one file

**Examples**:
- `/review` → "Review this code for bugs and suggest improvements"
- `/explain` → "Explain this code in simple terms"
- `/optimize` → "Analyze this code for performance issues"

### Use Skills for

**Comprehensive capabilities with structure**:
- Complex workflows with multiple steps
- Capabilities requiring scripts or utilities
- Knowledge organized across multiple files
- Team workflows you want to standardize

**Examples**:
- PDF processing Skill with form-filling scripts and validation
- Data analysis Skill with reference docs for different data types
- Documentation Skill with style guides and templates

### Key differences

| Aspect | Slash Commands | Agent Skills |
| --- | --- | --- |
| **Complexity** | Simple prompts | Complex capabilities |
| **Structure** | Single .md file | Directory with SKILL.md + resources |
| **Discovery** | Explicit invocation (`/command`) | Automatic (based on context) |
| **Files** | One file only | Multiple files, scripts, templates |
| **Scope** | Project or personal | Project or personal |
| **Sharing** | Via git | Via git |

### Example comparison

**As a slash command**:

```markdown
# .claude/commands/review.md
Review this code for:
- Security vulnerabilities
- Performance issues
- Code style violations
```

Usage: `/review` (manual invocation)

**As a Skill**:

```
.claude/skills/code-review/
├── SKILL.md (overview and workflows)
├── SECURITY.md (security checklist)
├── PERFORMANCE.md (performance patterns)
├── STYLE.md (style guide reference)
└── scripts/
    └── run-linters.sh
```

Usage: "Can you review this code?" (automatic discovery)

### When to use each

**Use slash commands**:
- You invoke the same prompt repeatedly
- The prompt fits in a single file
- You want explicit control over when it runs

**Use Skills**:
- Claude should discover the capability automatically
- Multiple files or scripts are needed
- Complex workflows with validation steps
- Team needs standardized, detailed guidance

## See also

- [Plugins](/docs/en/plugins)
- [Identity and Access Management](/docs/en/iam)
- [Interactive mode](/docs/en/interactive-mode)
- [CLI reference](/docs/en/cli-reference)
- [Settings](/docs/en/settings)
- [Memory management](/docs/en/memory)
