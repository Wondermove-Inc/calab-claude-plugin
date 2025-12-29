# MCP (Model Context Protocol) - Claude Code 공식 문서

> **출처**: https://code.claude.com/docs/en/mcp

---

# Connect Claude Code to tools via MCP

Learn how to connect Claude Code to your tools with the Model Context Protocol.

Claude Code can connect to hundreds of external tools and data sources through the Model Context Protocol (MCP), an open source standard for AI-tool integrations. MCP servers give Claude Code access to your tools, databases, and APIs.

## What you can do with MCP

With MCP servers connected, you can ask Claude Code to:

- **Implement features from issue trackers**: "Add the feature described in JIRA issue ENG-4521 and create a PR on GitHub."
- **Analyze monitoring data**: "Check Sentry and Statsig to check the usage of the feature described in ENG-4521."
- **Query databases**: "Find emails of 10 random users who used feature ENG-4521, based on our PostgreSQL database."
- **Integrate designs**: "Update our standard email template based on the new Figma designs that were posted in Slack"
- **Automate workflows**: "Create Gmail drafts inviting these 10 users to a feedback session about the new feature."

## Installing MCP servers

### Option 1: Add a remote HTTP server

HTTP servers are the recommended option for connecting to remote MCP servers.

```bash
# Basic syntax
claude mcp add --transport http <name> <url>

# Real example: Connect to Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Example with Bearer token
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### Option 2: Add a remote SSE server

The SSE (Server-Sent Events) transport is deprecated. Use HTTP servers instead.

```bash
# Basic syntax
claude mcp add --transport sse <name> <url>

# Real example: Connect to Asana
claude mcp add --transport sse asana https://mcp.asana.com/sse

# Example with authentication header
claude mcp add --transport sse private-api https://api.company.com/sse \
  --header "X-API-Key: your-key-here"
```

### Option 3: Add a local stdio server

Stdio servers run as local processes on your machine.

```bash
# Basic syntax
claude mcp add --transport stdio <name> <command> [args...]

# Real example: Add Airtable server
claude mcp add --transport stdio airtable --env AIRTABLE_API_KEY=YOUR_KEY \
  -- npx -y airtable-mcp-server
```

**Understanding the "--" parameter:** The `--` (double dash) separates Claude's CLI flags from the command and arguments that get passed to the MCP server.

### Managing your servers

```bash
# List all configured servers
claude mcp list

# Get details for a specific server
claude mcp get github

# Remove a server
claude mcp remove github

# (within Claude Code) Check server status
/mcp
```

**Tips:**
- Use `--scope` flag: `local` (default), `project`, or `user`
- Set environment variables with `--env` flags
- Configure timeout using `MCP_TIMEOUT` environment variable
- Use `/mcp` to authenticate with remote servers requiring OAuth

**Windows Users**: On native Windows, local MCP servers require the `cmd /c` wrapper:

```bash
claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
```

### Plugin-provided MCP servers

Plugins can bundle MCP servers in `.mcp.json` at the plugin root or inline in `plugin.json`:

```json
{
  "database-tools": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
    "env": {
      "DB_URL": "${DB_URL}"
    }
  }
}
```

## MCP installation scopes

### Local scope

Local-scoped servers are stored in `~/.claude.json` under your project's path. Private to you, only accessible in the current project.

```bash
claude mcp add --transport http stripe https://mcp.stripe.com
claude mcp add --transport http stripe --scope local https://mcp.stripe.com
```

### Project scope

Project-scoped servers store configurations in `.mcp.json` at your project's root, designed to be checked into version control.

```bash
claude mcp add --transport http paypal --scope project https://mcp.paypal.com/mcp
```

Resulting `.mcp.json`:

```json
{
  "mcpServers": {
    "shared-server": {
      "command": "/path/to/server",
      "args": [],
      "env": {}
    }
  }
}
```

### User scope

User-scoped servers are stored in `~/.claude.json` and available across all projects.

```bash
claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic
```

### Environment variable expansion in .mcp.json

**Supported syntax:**
- `${VAR}` - Expands to the value of environment variable `VAR`
- `${VAR:-default}` - Expands to `VAR` if set, otherwise uses `default`

**Example:**

```json
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

## Practical examples

### Example: Monitor errors with Sentry

```bash
# 1. Add the Sentry MCP server
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# 2. Use /mcp to authenticate with your Sentry account
> /mcp

# 3. Debug production issues
> "What are the most common errors in the last 24 hours?"
> "Show me the stack trace for error ID abc123"
> "Which deployment introduced these new errors?"
```

### Example: Connect to GitHub for code reviews

```bash
# 1. Add the GitHub MCP server
claude mcp add --transport http github https://api.githubcopilot.com/mcp/

# 2. In Claude Code, authenticate if needed
> /mcp

# 3. Now you can ask Claude to work with GitHub
> "Review PR #456 and suggest improvements"
> "Create a new issue for the bug we just found"
> "Show me all open PRs assigned to me"
```

### Example: Query your PostgreSQL database

```bash
# 1. Add the database server with your connection string
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://readonly:password@db.company.com:5432/analytics"

# 2. Query your database naturally
> "What's our total revenue this month?"
> "Show me the schema for the orders table"
> "Find customers who haven't made a purchase in 90 days"
```

## Authenticate with remote MCP servers

Many cloud-based MCP servers require OAuth 2.0 authentication:

1. Add the server that requires authentication
2. Use `/mcp` within Claude Code
3. Follow the steps in your browser to login

**Tips:**
- Authentication tokens are stored securely and refreshed automatically
- Use "Clear authentication" in `/mcp` menu to revoke access

## Add MCP servers from JSON configuration

```bash
# Basic syntax
claude mcp add-json <name> '<json-config>'

# Example: Adding an HTTP server with JSON configuration
claude mcp add-json weather-api '{"type":"http","url":"https://api.weather.com/mcp","headers":{"Authorization":"Bearer token"}}'

# Example: Adding a stdio server with JSON configuration
claude mcp add-json local-weather '{"type":"stdio","command":"/path/to/weather-cli","args":["--api-key","abc123"],"env":{"CACHE_DIR":"/tmp"}}'
```

## Import MCP servers from Claude Desktop

```bash
# Import servers from Claude Desktop
claude mcp add-from-claude-desktop

# Verify the servers were imported
claude mcp list
```

This feature only works on macOS and Windows Subsystem for Linux (WSL).

## Use Claude Code as an MCP server

```bash
# Start Claude as a stdio MCP server
claude mcp serve
```

Claude Desktop configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

## MCP output limits and warnings

- **Output warning threshold**: 10,000 tokens
- **Default maximum**: 25,000 tokens
- **Configurable limit**: `MAX_MCP_OUTPUT_TOKENS` environment variable

```bash
# Set a higher limit for MCP tool outputs
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

## Use MCP resources

Reference resources using @ mentions:

```
> Can you analyze @github:issue://123 and suggest a fix?
> Please review the API documentation at @docs:file://api/authentication
> Compare @postgres:schema://users with @docs:file://database/user-model
```

## Use MCP prompts as slash commands

### Execute MCP prompts

```
# Discover available prompts
Type / to see all available commands

# Execute a prompt without arguments
> /mcp__github__list_prs

# Execute a prompt with arguments
> /mcp__github__pr_review 456
> /mcp__jira__create_issue "Bug in login flow" high
```

## Enterprise MCP configuration

### Option 1: Exclusive control with managed-mcp.json

Deploy `managed-mcp.json` to system-wide directories:
- macOS: `/Library/Application Support/ClaudeCode/managed-mcp.json`
- Linux and WSL: `/etc/claude-code/managed-mcp.json`
- Windows: `C:\Program Files\ClaudeCode\managed-mcp.json`

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "sentry": {
      "type": "http",
      "url": "https://mcp.sentry.dev/mcp"
    },
    "company-internal": {
      "type": "stdio",
      "command": "/usr/local/bin/company-mcp-server",
      "args": ["--config", "/etc/company/mcp-config.json"],
      "env": {
        "COMPANY_API_URL": "https://internal.company.com"
      }
    }
  }
}
```

### Option 2: Policy-based control with allowlists and denylists

```json
{
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverName": "sentry" },
    { "serverCommand": ["npx", "-y", "@modelcontextprotocol/server-filesystem"] },
    { "serverUrl": "https://mcp.company.com/*" },
    { "serverUrl": "https://*.internal.corp/*" }
  ],
  "deniedMcpServers": [
    { "serverName": "dangerous-server" },
    { "serverCommand": ["npx", "-y", "unapproved-package"] },
    { "serverUrl": "https://*.untrusted.com/*" }
  ]
}
```

### Restriction options

1. **By server name** (`serverName`): Matches the configured name
2. **By command** (`serverCommand`): Matches exact command and arguments
3. **By URL pattern** (`serverUrl`): Matches remote server URLs with wildcard support

### Allowlist behavior

- `undefined` (default): No restrictions
- Empty array `[]`: Complete lockdown
- List of entries: Users can only configure matching servers

### Denylist behavior

- `undefined` (default): No servers are blocked
- Empty array `[]`: No servers are blocked
- List of entries: Specified servers are explicitly blocked

**Note:** Denylist takes absolute precedence over allowlist.
