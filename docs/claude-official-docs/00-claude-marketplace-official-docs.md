# Claude Code Plugin Marketplace 공식 문서

> **출처**: https://code.claude.com/docs/en/discover-plugins, https://code.claude.com/docs/en/plugin-marketplaces, https://github.com/anthropics/claude-plugins-official

---

## 목차

1. [개요](#개요)
2. [플러그인 마켓플레이스 발견 및 설치](#플러그인-마켓플레이스-발견-및-설치)
3. [플러그인 마켓플레이스 생성 및 배포](#플러그인-마켓플레이스-생성-및-배포)
4. [공식 플러그인 디렉토리 구조](#공식-플러그인-디렉토리-구조)

---

## 개요

**Claude Code Plugin Marketplace**는 Anthropic의 Claude Code에서 플러그인을 검색, 설치, 공유할 수 있는 시스템입니다. 플러그인은 커스텀 명령어, 에이전트, 훅, MCP 서버 등을 통해 Claude Code를 확장합니다.

---

# Part 1: Discover and install prebuilt plugins through marketplaces

Find and install plugins from marketplaces to extend Claude Code with new commands, agents, and capabilities.

Plugins extend Claude Code with custom commands, agents, hooks, and MCP servers. Plugin marketplaces are catalogs that help you discover and install these extensions without building them yourself.

## How marketplaces work

A marketplace is a catalog of plugins that someone else has created and shared. Using a marketplace is a two-step process:

1. **Add the marketplace**: This registers the catalog with Claude Code so you can browse what's available. No plugins are installed yet.
2. **Install individual plugins**: Browse the catalog and install the plugins you want.

Think of it like adding an app store: adding the store gives you access to browse its collection, but you still choose which apps to download individually.

## Official Anthropic marketplace

The official Anthropic marketplace (`claude-plugins-official`) is automatically installed when you start Claude Code. You can browse its plugins immediately by running `/plugin` and going to the **Discover** tab. To install a plugin from the official marketplace:

```
/plugin install plugin-name@claude-plugins-official
```

## Try it: add the demo marketplace

Anthropic also maintains a [demo plugins marketplace](https://github.com/anthropics/claude-code/tree/main/plugins) with example plugins that show what's possible with the plugin system. Unlike the official marketplace, you need to add this one manually.

### Step 1: Add the marketplace

From within Claude Code, run the `plugin marketplace add` command for the `anthropics/claude-code` marketplace:

```
/plugin marketplace add anthropics/claude-code
```

This downloads the marketplace catalog and makes its plugins available to you.

### Step 2: Browse available plugins

Run `/plugin` to open the plugin manager. This opens a tabbed interface with four tabs you can cycle through using **Tab** (or **Shift+Tab** to go backward):

- **Discover**: browse available plugins from all your marketplaces
- **Installed**: view and manage your installed plugins
- **Marketplaces**: add, remove, or update your added marketplaces
- **Errors**: view any plugin loading errors

Go to the **Discover** tab to see plugins from the marketplace you just added.

### Step 3: Install a plugin

Select a plugin to view its details, then choose an installation scope:

- **User scope**: install for yourself across all projects
- **Project scope**: install for all collaborators on this repository
- **Local scope**: install for yourself in this repository only

For example, select **commit-commands** (a plugin that adds git workflow commands) and install it to your user scope. You can also install directly from the command line:

```
/plugin install commit-commands@anthropics-claude-code
```

### Step 4: Use your new plugin

After installing, the plugin's commands are immediately available. Plugin commands are namespaced by the plugin name, so **commit-commands** provides commands like `/commit-commands:commit`. Try it out by making a change to a file and running:

```
/commit-commands:commit
```

This stages your changes, generates a commit message, and creates the commit.

## Add marketplaces

Use the `/plugin marketplace add` command to add marketplaces from different sources.

**Shortcuts**: You can use `/plugin market` instead of `/plugin marketplace`, and `rm` instead of `remove`.

- **GitHub repositories**: `owner/repo` format (for example, `anthropics/claude-code`)
- **Git URLs**: any git repository URL (GitLab, Bitbucket, self-hosted)
- **Local paths**: directories or direct paths to `marketplace.json` files
- **Remote URLs**: direct URLs to hosted `marketplace.json` files

### Add from GitHub

Add a GitHub repository that contains a `.claude-plugin/marketplace.json` file using the `owner/repo` format:

```
/plugin marketplace add anthropics/claude-code
```

### Add from other Git hosts

Add any git repository by providing the full URL:

Using HTTPS:
```
/plugin marketplace add https://gitlab.com/company/plugins.git
```

Using SSH:
```
/plugin marketplace add git@gitlab.com:company/plugins.git
```

To add a specific branch or tag, append `#` followed by the ref:
```
/plugin marketplace add https://gitlab.com/company/plugins.git#v1.0.0
```

### Add from local paths

Add a local directory that contains a `.claude-plugin/marketplace.json` file:

```
/plugin marketplace add ./my-marketplace
```

You can also add a direct path to a `marketplace.json` file:

```
/plugin marketplace add ./path/to/marketplace.json
```

Or add a remote `marketplace.json` file via URL:

```
/plugin marketplace add https://example.com/marketplace.json
```

## Install plugins

Once you've added marketplaces, you can install plugins directly (installs to user scope by default):

```
/plugin install plugin-name@marketplace-name
```

To choose a different installation scope, use the interactive UI: run `/plugin`, go to the **Discover** tab, and press **Enter** on a plugin. You'll see options for:

- **User scope** (default): install for yourself across all projects
- **Project scope**: install for all collaborators on this repository (adds to `.claude/settings.json`)
- **Local scope**: install for yourself in this repository only (not shared with collaborators)

> **Warning**: Make sure you trust a plugin before installing it. Anthropic does not control what MCP servers, files, or other software are included in plugins and cannot verify that they work as intended.

## Manage installed plugins

Run `/plugin` and go to the **Installed** tab to view, enable, disable, or uninstall your plugins.

Disable a plugin without uninstalling:
```
/plugin disable plugin-name@marketplace-name
```

Re-enable a disabled plugin:
```
/plugin enable plugin-name@marketplace-name
```

Completely remove a plugin:
```
/plugin uninstall plugin-name@marketplace-name
```

The `--scope` option lets you target a specific scope with CLI commands:
```
claude plugin install formatter@your-org --scope project
claude plugin uninstall formatter@your-org --scope project
```

## Manage marketplaces

### Use the interactive interface

Run `/plugin` and go to the **Marketplaces** tab to:

- View all your added marketplaces with their sources and status
- Add new marketplaces
- Update marketplace listings to fetch the latest plugins
- Remove marketplaces you no longer need

### Use CLI commands

List all configured marketplaces:
```
/plugin marketplace list
```

Refresh plugin listings from a marketplace:
```
/plugin marketplace update marketplace-name
```

Remove a marketplace:
```
/plugin marketplace remove marketplace-name
```

> **Note**: Removing a marketplace will uninstall any plugins you installed from it.

### Configure auto-updates

Claude Code can automatically update marketplaces and their installed plugins at startup. Toggle auto-update for individual marketplaces through the UI:

1. Run `/plugin` to open the plugin manager
2. Select **Marketplaces**
3. Choose a marketplace from the list
4. Select **Enable auto-update** or **Disable auto-update**

Official Anthropic marketplaces have auto-update enabled by default. Third-party and local development marketplaces have auto-update disabled by default.

## Configure team marketplaces

Team admins can set up automatic marketplace installation for projects by adding marketplace configuration to `.claude/settings.json`. When team members trust the repository folder, Claude Code prompts them to install these marketplaces and plugins.

## Troubleshooting

### /plugin command not recognized

If you see "unknown command" or the `/plugin` command doesn't appear:

1. **Check your version**: Run `claude --version`. Plugins require version 1.0.33 or later.
2. **Update Claude Code**:
   - **Homebrew**: `brew upgrade claude-code`
   - **npm**: `npm update -g @anthropic-ai/claude-code`
   - **Native installer**: Re-run the install command
3. **Restart Claude Code**: After updating, restart your terminal and run `claude` again.

### Common issues

- **Marketplace not loading**: Verify the URL is accessible and that `.claude-plugin/marketplace.json` exists at the path
- **Plugin installation failures**: Check that plugin source URLs are accessible and repositories are public (or you have access)
- **Files not found after installation**: Plugins are copied to a cache, so paths referencing files outside the plugin directory won't work

---

# Part 2: Create and distribute a plugin marketplace

Build and host plugin marketplaces to distribute Claude Code extensions across teams and communities.

A plugin marketplace is a catalog that lets you distribute plugins to others. Marketplaces provide centralized discovery, version tracking, automatic updates, and support for multiple source types.

## Overview

Creating and distributing a marketplace involves:

1. **Creating plugins**: build one or more plugins with commands, agents, hooks, MCP servers, or LSP servers.
2. **Creating a marketplace file**: define a `marketplace.json` that lists your plugins and where to find them.
3. **Host the marketplace**: push to GitHub, GitLab, or another git host.
4. **Share with users**: users add your marketplace with `/plugin marketplace add` and install individual plugins.

## Walkthrough: create a local marketplace

This example creates a marketplace with one plugin: a `/review` command for code reviews.

### Step 1: Create the directory structure

```bash
mkdir -p my-marketplace/.claude-plugin
mkdir -p my-marketplace/plugins/review-plugin/.claude-plugin
mkdir -p my-marketplace/plugins/review-plugin/commands
```

### Step 2: Create the plugin command

Create a Markdown file that defines what the `/review` command does.

**my-marketplace/plugins/review-plugin/commands/review.md**
```markdown
Review the code I've selected or the recent changes for:
- Potential bugs or edge cases
- Security concerns
- Performance issues
- Readability improvements

Be concise and actionable.
```

### Step 3: Create the plugin manifest

**my-marketplace/plugins/review-plugin/.claude-plugin/plugin.json**
```json
{
  "name": "review-plugin",
  "description": "Adds a /review command for quick code reviews",
  "version": "1.0.0"
}
```

### Step 4: Create the marketplace file

**my-marketplace/.claude-plugin/marketplace.json**
```json
{
  "name": "my-plugins",
  "owner": {
    "name": "Your Name"
  },
  "plugins": [
    {
      "name": "review-plugin",
      "source": "./plugins/review-plugin",
      "description": "Adds a /review command for quick code reviews"
    }
  ]
}
```

### Step 5: Add and install

```
/plugin marketplace add ./my-marketplace
/plugin install review-plugin@my-plugins
```

### Step 6: Try it out

Select some code in your editor and run your new command:
```
/review
```

## Create the marketplace file

Create `.claude-plugin/marketplace.json` in your repository root.

```json
{
  "name": "company-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@example.com"
  },
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "description": "Automatic code formatting on save",
      "version": "2.1.0",
      "author": {
        "name": "DevTools Team"
      }
    },
    {
      "name": "deployment-tools",
      "source": {
        "source": "github",
        "repo": "company/deploy-plugin"
      },
      "description": "Deployment automation tools"
    }
  ]
}
```

## Marketplace schema

### Required fields

| Field | Type | Description | Example |
| --- | --- | --- | --- |
| `name` | string | Marketplace identifier (kebab-case, no spaces) | `"acme-tools"` |
| `owner` | object | Marketplace maintainer information | |
| `plugins` | array | List of available plugins | |

**Reserved names**: The following marketplace names are reserved for official Anthropic use:
- `claude-code-marketplace`
- `claude-code-plugins`
- `claude-plugins-official`
- `anthropic-marketplace`
- `anthropic-plugins`
- `agent-skills`
- `life-sciences`

### Owner fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string | Yes | Name of the maintainer or team |
| `email` | string | No | Contact email for the maintainer |

### Optional metadata

| Field | Type | Description |
| --- | --- | --- |
| `metadata.description` | string | Brief marketplace description |
| `metadata.version` | string | Marketplace version |
| `metadata.pluginRoot` | string | Base directory for relative plugin source paths |

## Plugin entries

### Required fields

| Field | Type | Description |
| --- | --- | --- |
| `name` | string | Plugin identifier (kebab-case, no spaces) |
| `source` | string\|object | Where to fetch the plugin from |

### Optional plugin fields

| Field | Type | Description |
| --- | --- | --- |
| `description` | string | Brief plugin description |
| `version` | string | Plugin version |
| `author` | object | Plugin author information |
| `homepage` | string | Plugin homepage or documentation URL |
| `repository` | string | Source code repository URL |
| `license` | string | SPDX license identifier |
| `keywords` | array | Tags for plugin discovery |
| `category` | string | Plugin category |
| `tags` | array | Tags for searchability |
| `strict` | boolean | Controls whether plugins need their own `plugin.json` file |
| `commands` | string\|array | Custom paths to command files or directories |
| `agents` | string\|array | Custom paths to agent files |
| `hooks` | string\|object | Custom hooks configuration |
| `mcpServers` | string\|object | MCP server configurations |
| `lspServers` | string\|object | LSP server configurations |

## Plugin sources

### Relative paths
```json
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```

### GitHub repositories
```json
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  }
}
```

### Git repositories
```json
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

### Advanced plugin entries

```json
{
  "name": "enterprise-tools",
  "source": {
    "source": "github",
    "repo": "company/enterprise-plugin"
  },
  "description": "Enterprise workflow automation tools",
  "version": "2.1.0",
  "author": {
    "name": "Enterprise Team",
    "email": "enterprise@example.com"
  },
  "homepage": "https://docs.example.com/plugins/enterprise-tools",
  "repository": "https://github.com/company/enterprise-plugin",
  "license": "MIT",
  "keywords": ["enterprise", "workflow", "automation"],
  "category": "productivity",
  "commands": [
    "./commands/core/",
    "./commands/enterprise/",
    "./commands/experimental/preview.md"
  ],
  "agents": ["./agents/security-reviewer.md", "./agents/compliance-checker.md"],
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
          }
        ]
      }
    ]
  },
  "mcpServers": {
    "enterprise-db": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  },
  "strict": false
}
```

## Host and distribute marketplaces

### Host on GitHub (recommended)

1. **Create a repository**: Set up a new repository for your marketplace
2. **Add marketplace file**: Create `.claude-plugin/marketplace.json` with your plugin definitions
3. **Share with teams**: Users add your marketplace with `/plugin marketplace add owner/repo`

### Host on other git services

Any git hosting service works (GitLab, Bitbucket, self-hosted servers):

```
/plugin marketplace add https://gitlab.com/company/plugins.git
```

### Test locally before distribution

```
/plugin marketplace add ./my-local-marketplace
/plugin install test-plugin@my-local-marketplace
```

### Require marketplaces for your team

Add your marketplace to `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

You can also specify which plugins should be enabled by default:

```json
{
  "enabledPlugins": {
    "code-formatter@company-tools": true,
    "deployment-tools@company-tools": true
  }
}
```

## Enterprise marketplace restrictions

For organizations requiring strict control over plugin sources, use `strictKnownMarketplaces` in managed settings:

| Value | Behavior |
| --- | --- |
| Undefined (default) | No restrictions. Users can add any marketplace |
| Empty array `[]` | Complete lockdown. Users cannot add any new marketplaces |
| List of sources | Users can only add marketplaces that match the allowlist exactly |

### Disable all marketplace additions

```json
{
  "strictKnownMarketplaces": []
}
```

### Allow specific marketplaces only

```json
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json"
    }
  ]
}
```

## Validation and testing

Validate your marketplace JSON syntax:

```bash
claude plugin validate .
```

Or from within Claude Code:

```
/plugin validate .
```

## Troubleshooting

### Marketplace not loading

**Solutions**:
- Verify the marketplace URL is accessible
- Check that `.claude-plugin/marketplace.json` exists at the specified path
- Ensure JSON syntax is valid using `claude plugin validate` or `/plugin validate`
- For private repositories, confirm you have access permissions

### Marketplace validation errors

| Error | Cause | Solution |
| --- | --- | --- |
| `File not found: .claude-plugin/marketplace.json` | Missing manifest | Create `.claude-plugin/marketplace.json` with required fields |
| `Invalid JSON syntax: Unexpected token...` | JSON syntax error | Check for missing commas, extra commas, or unquoted strings |
| `Duplicate plugin name "x" found in marketplace` | Two plugins share the same name | Give each plugin a unique `name` value |
| `plugins[0].source: Path traversal not allowed` | Source path contains `..` | Use paths relative to marketplace root without `..` |

### Plugin installation failures

**Solutions**:
- Verify plugin source URLs are accessible
- Check that plugin directories contain required files
- For GitHub sources, ensure repositories are public or you have access
- Test plugin sources manually by cloning/downloading

### Files not found after installation

**Cause**: Plugins are copied to a cache directory. Paths that reference files outside the plugin's directory won't work.

**Solutions**: Use symlinks or restructure your marketplace so shared directories are inside the plugin source path.

---

# Part 3: Claude Code Plugins Directory (Official GitHub)

> **Source**: https://github.com/anthropics/claude-plugins-official

A curated directory of high-quality plugins for Claude Code.

> **⚠️ Important:** Make sure you trust a plugin before installing, updating, or using it. Anthropic does not control what MCP servers, files, or other software are included in plugins and cannot verify that they will work as intended or that they won't change. See each plugin's homepage for more information.

## Structure

- **`/plugins`** - Internal plugins developed and maintained by Anthropic
- **`/external_plugins`** - Third-party plugins from partners and the community

## Installation

Plugins can be installed directly from this marketplace via Claude Code's plugin system.

To install, run:
```
/plugin install {plugin-name}@claude-plugin-directory
```

or browse for the plugin in `/plugin > Discover`

## Contributing

### Internal Plugins

Internal plugins are developed by Anthropic team members. See `/plugins/example-plugin` for a reference implementation.

### External Plugins

Third-party partners can submit plugins for inclusion in the marketplace. External plugins must meet quality and security standards for approval.

## Plugin Structure

Each plugin follows a standard structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json       # Plugin metadata (required)
├── .mcp.json             # MCP server configuration (optional)
├── commands/             # Slash commands (optional)
├── agents/               # Agent definitions (optional)
├── skills/               # Skill definitions (optional)
└── README.md             # Documentation
```

For more information on developing Claude Code plugins, see the [official documentation](https://code.claude.com/docs/en/plugins).

---

## 관련 링크

- [Claude Code 공식 문서](https://code.claude.com/docs/en/overview)
- [플러그인 생성 가이드](https://code.claude.com/docs/en/plugins)
- [플러그인 레퍼런스](https://code.claude.com/docs/en/plugins-reference)
- [공식 플러그인 GitHub](https://github.com/anthropics/claude-plugins-official)
