# Plugins Reference - Claude Code 공식 문서

> **출처**: https://code.claude.com/docs/en/plugins-reference

---

# Plugins reference

Complete technical reference for Claude Code plugin system, including schemas, CLI commands, and component specifications.

## Plugin components reference

### Commands

Plugins add custom slash commands that integrate seamlessly with Claude Code's command system.

**Location**: `commands/` directory in plugin root
**File format**: Markdown files with frontmatter

### Agents

Plugins can provide specialized subagents for specific tasks.

**Location**: `agents/` directory in plugin root
**File format**: Markdown files describing agent capabilities

**Agent structure**:

```markdown
---
description: What this agent specializes in
capabilities: ["task1", "task2", "task3"]
---

# Agent Name

Detailed description of the agent's role, expertise, and when Claude should invoke it.

## Capabilities
- Specific task the agent excels at
- Another specialized capability

## Context and examples
Provide examples of when this agent should be used.
```

### Skills

Plugins can provide Agent Skills that extend Claude's capabilities.

**Location**: `skills/` directory in plugin root
**File format**: Directories containing `SKILL.md` files with frontmatter

**Skill structure**:

```
skills/
├── pdf-processor/
│   ├── SKILL.md
│   ├── reference.md (optional)
│   └── scripts/ (optional)
└── code-reviewer/
    └── SKILL.md
```

### Hooks

Plugins can provide event handlers that respond to Claude Code events.

**Location**: `hooks/hooks.json` in plugin root, or inline in plugin.json

**Hook configuration**:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

**Available events**:
- `PreToolUse`: Before Claude uses any tool
- `PostToolUse`: After Claude successfully uses any tool
- `PostToolUseFailure`: After Claude tool execution fails
- `PermissionRequest`: When a permission dialog is shown
- `UserPromptSubmit`: When user submits a prompt
- `Notification`: When Claude Code sends notifications
- `Stop`: When Claude attempts to stop
- `SubagentStart`: When a subagent is started
- `SubagentStop`: When a subagent attempts to stop
- `SessionStart`: At the beginning of sessions
- `SessionEnd`: At the end of sessions
- `PreCompact`: Before conversation history is compacted

**Hook types**:
- `command`: Execute shell commands or scripts
- `prompt`: Evaluate a prompt with an LLM
- `agent`: Run an agentic verifier with tools

### MCP servers

Plugins can bundle Model Context Protocol (MCP) servers.

**Location**: `.mcp.json` in plugin root, or inline in plugin.json

```json
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    }
  }
}
```

### LSP servers

Plugins can provide Language Server Protocol (LSP) servers for code intelligence.

**Location**: `.lsp.json` in plugin root, or inline in `plugin.json`

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

**Required fields:**

| Field | Description |
| --- | --- |
| `command` | The LSP binary to execute (must be in PATH) |
| `extensionToLanguage` | Maps file extensions to language identifiers |

**Optional fields:**

| Field | Description |
| --- | --- |
| `args` | Command-line arguments |
| `transport` | `stdio` (default) or `socket` |
| `env` | Environment variables |
| `initializationOptions` | Options for server initialization |
| `settings` | Settings via `workspace/didChangeConfiguration` |
| `startupTimeout` | Max startup wait time (ms) |
| `shutdownTimeout` | Max shutdown wait time (ms) |
| `restartOnCrash` | Auto-restart on crash |
| `maxRestarts` | Max restart attempts |
| `loggingConfig` | Debug logging configuration |

**Available LSP plugins:**

| Plugin | Language server | Install command |
| --- | --- | --- |
| `pyright-lsp` | Pyright (Python) | `pip install pyright` or `npm install -g pyright` |
| `typescript-lsp` | TypeScript Language Server | `npm install -g typescript-language-server typescript` |
| `rust-lsp` | rust-analyzer | See rust-analyzer installation |

## Plugin installation scopes

| Scope | Settings file | Use case |
| --- | --- | --- |
| `user` | `~/.claude/settings.json` | Personal plugins (default) |
| `project` | `.claude/settings.json` | Team plugins via version control |
| `local` | `.claude/settings.local.json` | Project-specific, gitignored |
| `managed` | `managed-settings.json` | Enterprise-managed (read-only) |

## Plugin manifest schema

### Complete schema

```json
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json"
}
```

### Required fields

| Field | Type | Description | Example |
| --- | --- | --- | --- |
| `name` | string | Unique identifier (kebab-case) | `"deployment-tools"` |

### Metadata fields

| Field | Type | Description |
| --- | --- | --- |
| `version` | string | Semantic version |
| `description` | string | Brief explanation |
| `author` | object | Author information |
| `homepage` | string | Documentation URL |
| `repository` | string | Source code URL |
| `license` | string | License identifier |
| `keywords` | array | Discovery tags |

### Component path fields

| Field | Type | Description |
| --- | --- | --- |
| `commands` | string\|array | Command files/directories |
| `agents` | string\|array | Agent files |
| `skills` | string\|array | Skill directories |
| `hooks` | string\|object | Hook config path or inline |
| `mcpServers` | string\|object | MCP config path or inline |
| `outputStyles` | string\|array | Output style files/directories |
| `lspServers` | string\|object | LSP config |

### Path behavior rules

Custom paths supplement default directories—they don't replace them.

```json
{
  "commands": [
    "./specialized/deploy.md",
    "./utilities/batch-process.md"
  ],
  "agents": [
    "./custom-agents/reviewer.md",
    "./custom-agents/tester.md"
  ]
}
```

### Environment variables

**`${CLAUDE_PLUGIN_ROOT}`**: Absolute path to your plugin directory.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/process.sh"
          }
        ]
      }
    ]
  }
}
```

## Plugin caching and file resolution

### How plugin caching works

When you install a plugin, Claude Code copies the plugin files to a cache directory rather than using them in-place.

### Path traversal limitations

Plugins cannot reference files outside their copied directory structure. Paths like `../shared-utils` will not work.

### Working with external dependencies

**Option 1: Use symlinks**

```bash
# Inside your plugin directory
ln -s /path/to/shared-utils ./shared-utils
```

**Option 2: Restructure your marketplace**

Set the plugin path to a parent directory containing all required files.

## Plugin directory structure

### Standard plugin layout

```
enterprise-plugin/
├── .claude-plugin/           # Metadata directory
│   └── plugin.json          # Required: plugin manifest
├── commands/                 # Default command location
│   ├── status.md
│   └── logs.md
├── agents/                   # Default agent location
│   ├── security-reviewer.md
│   └── performance-tester.md
├── skills/                   # Agent Skills
│   └── code-reviewer/
│       └── SKILL.md
├── hooks/                    # Hook configurations
│   └── hooks.json
├── .mcp.json                # MCP server definitions
├── .lsp.json                # LSP server configurations
├── scripts/                 # Hook and utility scripts
│   ├── security-scan.sh
│   └── format-code.py
├── LICENSE
└── CHANGELOG.md
```

### File locations reference

| Component | Default Location | Purpose |
| --- | --- | --- |
| **Manifest** | `.claude-plugin/plugin.json` | Required metadata file |
| **Commands** | `commands/` | Slash command Markdown files |
| **Agents** | `agents/` | Subagent Markdown files |
| **Skills** | `skills/` | Agent Skills with SKILL.md files |
| **Hooks** | `hooks/hooks.json` | Hook configuration |
| **MCP servers** | `.mcp.json` | MCP server definitions |
| **LSP servers** | `.lsp.json` | Language server configurations |

## CLI commands reference

### plugin install

```bash
claude plugin install <plugin> [options]
```

**Options:**
- `-s, --scope <scope>`: Installation scope (`user`, `project`, `local`)

**Examples:**

```bash
# Install to user scope (default)
claude plugin install formatter@my-marketplace

# Install to project scope
claude plugin install formatter@my-marketplace --scope project
```

### plugin uninstall

```bash
claude plugin uninstall <plugin> [options]
```

**Aliases:** `remove`, `rm`

### plugin enable

```bash
claude plugin enable <plugin> [options]
```

### plugin disable

```bash
claude plugin disable <plugin> [options]
```

### plugin update

```bash
claude plugin update <plugin> [options]
```

## Debugging and development tools

### Debugging commands

```bash
claude --debug
```

Shows:
- Which plugins are being loaded
- Any errors in plugin manifests
- Command, agent, and hook registration
- MCP server initialization

### Common issues

| Issue | Cause | Solution |
| --- | --- | --- |
| Plugin not loading | Invalid `plugin.json` | Validate with `claude plugin validate` |
| Commands not appearing | Wrong directory structure | Ensure `commands/` at root |
| Hooks not firing | Script not executable | Run `chmod +x script.sh` |
| MCP server fails | Missing `${CLAUDE_PLUGIN_ROOT}` | Use variable for all paths |
| Path errors | Absolute paths used | Use relative paths starting with `./` |
| LSP error | Language server not installed | Install the binary |

### Example error messages

**Manifest validation errors**:
- `Invalid JSON syntax: Unexpected token }`: check for missing/extra commas
- `Plugin has an invalid manifest file`: required field is missing
- `Plugin has a corrupt manifest file`: JSON syntax error

**Plugin loading errors**:
- `Warning: No commands found`: command path contains no valid files
- `Plugin directory not found`: source path is incorrect
- `Plugin has conflicting manifests`: duplicate component definitions

### Hook troubleshooting

1. Check the script is executable: `chmod +x ./scripts/your-script.sh`
2. Verify the shebang line: `#!/bin/bash`
3. Check path uses `${CLAUDE_PLUGIN_ROOT}`
4. Test the script manually

### MCP server troubleshooting

1. Check the command exists and is executable
2. Verify all paths use `${CLAUDE_PLUGIN_ROOT}`
3. Check MCP server logs: `claude --debug`
4. Test the server manually

### Directory structure mistakes

Components must be at the plugin root, not inside `.claude-plugin/`:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json      ← Only manifest here
├── commands/            ← At root level
├── agents/              ← At root level
└── hooks/               ← At root level
```

## Version management

Follow semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward-compatible)
- **PATCH**: Bug fixes (backward-compatible)

**Best practices**:
- Start at `1.0.0` for first stable release
- Update version before distributing changes
- Document changes in `CHANGELOG.md`
- Use pre-release versions like `2.0.0-beta.1` for testing

## See also

- [Plugins](/docs/en/plugins) - Tutorials and practical usage
- [Plugin marketplaces](/docs/en/plugin-marketplaces) - Creating and managing marketplaces
- [Slash commands](/docs/en/slash-commands) - Command development
- [Subagents](/docs/en/sub-agents) - Agent configuration
- [Agent Skills](/docs/en/skills) - Extending Claude's capabilities
- [Hooks](/docs/en/hooks) - Event handling and automation
- [MCP](/docs/en/mcp) - External tool integration
