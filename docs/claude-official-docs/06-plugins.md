# Plugins - Claude Code 공식 문서

> **출처**: https://code.claude.com/docs/en/plugins

---

# Create plugins

Create custom plugins to extend Claude Code with slash commands, agents, hooks, Skills, and MCP servers.

Plugins let you extend Claude Code with custom functionality that can be shared across projects and teams.

## When to use plugins vs standalone configuration

| Approach | Slash command names | Best for |
| --- | --- | --- |
| **Standalone** (`.claude/` directory) | `/hello` | Personal workflows, project-specific customizations, quick experiments |
| **Plugins** (directories with `.claude-plugin/plugin.json`) | `/plugin-name:hello` | Sharing with teammates, distributing to community, versioned releases, reusable across projects |

**Use standalone configuration when**:
- You're customizing Claude Code for a single project
- The configuration is personal and doesn't need to be shared
- You're experimenting before packaging

**Use plugins when**:
- You want to share functionality with your team or community
- You need the same commands across multiple projects
- You want version control and easy updates
- You're distributing through a marketplace

## Quickstart

### Prerequisites

- Claude Code installed and authenticated
- Claude Code version 1.0.33 or later

### Create your first plugin

#### Step 1: Create the plugin directory

```bash
mkdir my-first-plugin
```

#### Step 2: Create the plugin manifest

```bash
mkdir my-first-plugin/.claude-plugin
```

Create `my-first-plugin/.claude-plugin/plugin.json`:

```json
{
  "name": "my-first-plugin",
  "description": "A greeting plugin to learn the basics",
  "version": "1.0.0",
  "author": {
    "name": "Your Name"
  }
}
```

| Field | Purpose |
| --- | --- |
| `name` | Unique identifier and slash command namespace |
| `description` | Shown in the plugin manager |
| `version` | Track releases using semantic versioning |
| `author` | Optional, helpful for attribution |

#### Step 3: Add a slash command

```bash
mkdir my-first-plugin/commands
```

Create `my-first-plugin/commands/hello.md`:

```markdown
---
description: Greet the user with a friendly message
---

# Hello Command

Greet the user warmly and ask how you can help them today.
```

#### Step 4: Test your plugin

```bash
claude --plugin-dir ./my-first-plugin
```

Then run:

```
/my-first-plugin:hello
```

#### Step 5: Add slash command arguments

Update `hello.md`:

```markdown
---
description: Greet the user with a personalized message
---

# Hello Command

Greet the user named "$ARGUMENTS" warmly and ask how you can help them today. Make the greeting personal and encouraging.
```

Test with:

```
/my-first-plugin:hello Alex
```

## Plugin structure overview

| Directory | Location | Purpose |
| --- | --- | --- |
| `.claude-plugin/` | Plugin root | Contains only `plugin.json` manifest (required) |
| `commands/` | Plugin root | Slash commands as Markdown files |
| `agents/` | Plugin root | Custom agent definitions |
| `skills/` | Plugin root | Agent Skills with `SKILL.md` files |
| `hooks/` | Plugin root | Event handlers in `hooks.json` |
| `.mcp.json` | Plugin root | MCP server configurations |
| `.lsp.json` | Plugin root | LSP server configurations |

**Important**: Don't put `commands/`, `agents/`, `skills/`, or `hooks/` inside the `.claude-plugin/` directory. Only `plugin.json` goes inside `.claude-plugin/`.

## Develop more complex plugins

### Add Skills to your plugin

Create a `skills/` directory at your plugin root and add Skill folders with `SKILL.md` files.

### Add LSP servers to your plugin

Add an `.lsp.json` file to your plugin:

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

### Organize complex plugins

```
enterprise-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── core/
│   │   └── status.md
│   └── deploy/
│       └── production.md
├── agents/
│   ├── reviewer.md
│   └── tester.md
├── skills/
│   └── code-review/
│       └── SKILL.md
├── hooks/
│   └── hooks.json
├── .mcp.json
└── scripts/
    └── validate.sh
```

### Test your plugins locally

```bash
# Load single plugin
claude --plugin-dir ./my-plugin

# Load multiple plugins
claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two
```

### Debug plugin issues

1. **Check the structure**: Ensure directories are at the plugin root, not inside `.claude-plugin/`
2. **Test components individually**: Check each command, agent, and hook separately
3. **Use validation tools**: `claude plugin validate .` or `/plugin validate`

### Share your plugins

1. **Add documentation**: Include a `README.md`
2. **Version your plugin**: Use semantic versioning
3. **Create or use a marketplace**: Distribute through plugin marketplaces
4. **Test with others**: Have team members test before wider distribution

## Convert existing configurations to plugins

### Migration steps

#### Step 1: Create the plugin structure

```bash
mkdir -p my-plugin/.claude-plugin
```

Create `my-plugin/.claude-plugin/plugin.json`:

```json
{
  "name": "my-plugin",
  "description": "Migrated from standalone configuration",
  "version": "1.0.0"
}
```

#### Step 2: Copy your existing files

```bash
# Copy commands
cp -r .claude/commands my-plugin/

# Copy agents (if any)
cp -r .claude/agents my-plugin/

# Copy skills (if any)
cp -r .claude/skills my-plugin/
```

#### Step 3: Migrate hooks

Create `my-plugin/hooks/hooks.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": "npm run lint:fix $FILE" }]
      }
    ]
  }
}
```

#### Step 4: Test your migrated plugin

```bash
claude --plugin-dir ./my-plugin
```

### What changes when migrating

| Standalone (`.claude/`) | Plugin |
| --- | --- |
| Only available in one project | Can be shared via marketplaces |
| Files in `.claude/commands/` | Files in `plugin-name/commands/` |
| Hooks in `settings.json` | Hooks in `hooks/hooks.json` |
| Must manually copy to share | Install with `/plugin install` |

## Plugin manifest fields

### Required fields

| Field | Type | Description |
| --- | --- | --- |
| `name` | string | Unique identifier (kebab-case) |

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
| `lspServers` | string\|object | LSP config path or inline |

## Environment variables

**`${CLAUDE_PLUGIN_ROOT}`**: Absolute path to your plugin directory. Use this in hooks, MCP servers, and scripts:

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

## Next steps

### For plugin users
- [Discover and install plugins](/docs/en/discover-plugins)
- [Configure team marketplaces](/docs/en/discover-plugins#configure-team-marketplaces)

### For plugin developers
- [Create and distribute a marketplace](/docs/en/plugin-marketplaces)
- [Plugins reference](/docs/en/plugins-reference)
- [Slash commands](/docs/en/slash-commands)
- [Subagents](/docs/en/sub-agents)
- [Agent Skills](/docs/en/skills)
- [Hooks](/docs/en/hooks)
- [MCP](/docs/en/mcp)
