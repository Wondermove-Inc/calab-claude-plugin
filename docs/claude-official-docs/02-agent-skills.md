# Agent Skills - Claude Code 공식 문서

> **출처**: https://code.claude.com/docs/en/skills

---

# Agent Skills

Create, manage, and share Skills to extend Claude's capabilities in Claude Code.

This guide shows you how to create, use, and manage Agent Skills in Claude Code. Skills are modular capabilities that extend Claude's functionality through organized folders containing instructions, scripts, and resources.

## Prerequisites

- Claude Code version 1.0 or later
- Basic familiarity with Claude Code

## What are Agent Skills?

Agent Skills package expertise into discoverable capabilities. Each Skill consists of a `SKILL.md` file with instructions that Claude reads when relevant, plus optional supporting files like scripts and templates.

**How Skills are invoked**: Skills are **model-invoked**—Claude autonomously decides when to use them based on your request and the Skill's description. This is different from slash commands, which are **user-invoked** (you explicitly type `/command` to trigger them).

**Benefits**:
- Extend Claude's capabilities for your specific workflows
- Share expertise across your team via git
- Reduce repetitive prompting
- Compose multiple Skills for complex tasks

## Create a Skill

Skills are stored as directories containing a `SKILL.md` file.

### Personal Skills

Personal Skills are available across all your projects. Store them in `~/.claude/skills/`:

```bash
mkdir -p ~/.claude/skills/my-skill-name
```

**Use personal Skills for**:
- Your individual workflows and preferences
- Experimental Skills you're developing
- Personal productivity tools

### Project Skills

Project Skills are shared with your team. Store them in `.claude/skills/` within your project:

```bash
mkdir -p .claude/skills/my-skill-name
```

**Use project Skills for**:
- Team workflows and conventions
- Project-specific expertise
- Shared utilities and scripts

Project Skills are checked into git and automatically available to team members.

### Plugin Skills

Skills can also come from Claude Code plugins. Plugins may bundle Skills that are automatically available when the plugin is installed.

## Write SKILL.md

Create a `SKILL.md` file with YAML frontmatter and Markdown content:

```markdown
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
---

# Your Skill Name

## Instructions
Provide clear, step-by-step guidance for Claude.

## Examples
Show concrete examples of using this Skill.
```

**Field requirements**:
- `name`: Must use lowercase letters, numbers, and hyphens only (max 64 characters)
- `description`: Brief description of what the Skill does and when to use it (max 1024 characters)

The `description` field is critical for Claude to discover when to use your Skill.

## Add supporting files

Create additional files alongside SKILL.md:

```
my-skill/
├── SKILL.md (required)
├── reference.md (optional documentation)
├── examples.md (optional examples)
├── scripts/
│   └── helper.py (optional utility)
└── templates/
    └── template.txt (optional template)
```

Reference these files from SKILL.md:

```markdown
For advanced usage, see [reference.md](reference.md).

Run the helper script:
```bash
python scripts/helper.py input.txt
```
```

Claude reads these files only when needed, using progressive disclosure to manage context efficiently.

## Restrict tool access with allowed-tools

Use the `allowed-tools` frontmatter field to limit which tools Claude can use when a Skill is active:

```markdown
---
name: safe-file-reader
description: Read files without making changes. Use when you need read-only file access.
allowed-tools: Read, Grep, Glob
---

# Safe File Reader

This Skill provides read-only file access.

## Instructions
1. Use Read to view file contents
2. Use Grep to search within files
3. Use Glob to find files by pattern
```

When this Skill is active, Claude can only use the specified tools without needing to ask for permission.

## View available Skills

Skills are automatically discovered by Claude from three sources:
- Personal Skills: `~/.claude/skills/`
- Project Skills: `.claude/skills/`
- Plugin Skills: bundled with installed plugins

**To view all available Skills**, ask Claude directly:

```
What Skills are available?
```

or

```
List all available Skills
```

**To inspect a specific Skill**:

```bash
# List personal Skills
ls ~/.claude/skills/

# List project Skills
ls .claude/skills/

# View a specific Skill's content
cat ~/.claude/skills/my-skill/SKILL.md
```

## Test a Skill

After creating a Skill, test it by asking questions that match your description.

**Example**: If your description mentions "PDF files":

```
Can you help me extract text from this PDF?
```

Claude autonomously decides to use your Skill if it matches the request.

## Debug a Skill

### Make description specific

**Too vague**:
```
description: Helps with documents
```

**Specific**:
```
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

### Verify file path

**Personal Skills**: `~/.claude/skills/skill-name/SKILL.md`
**Project Skills**: `.claude/skills/skill-name/SKILL.md`

```bash
# Personal
ls ~/.claude/skills/my-skill/SKILL.md

# Project
ls .claude/skills/my-skill/SKILL.md
```

### Check YAML syntax

```bash
cat SKILL.md | head -n 10
```

Ensure:
- Opening `---` on line 1
- Closing `---` before Markdown content
- Valid YAML syntax (no tabs, correct indentation)

### View errors

Run Claude Code with debug mode:

```bash
claude --debug
```

## Share Skills with your team

**Recommended approach**: Distribute Skills through plugins.

You can also share Skills directly through project repositories:

### Step 1: Add Skill to your project

```bash
mkdir -p .claude/skills/team-skill
# Create SKILL.md
```

### Step 2: Commit to git

```bash
git add .claude/skills/
git commit -m "Add team Skill for PDF processing"
git push
```

### Step 3: Team members get Skills automatically

```bash
git pull
claude  # Skills are now available
```

## Update a Skill

Edit SKILL.md directly:

```bash
# Personal Skill
code ~/.claude/skills/my-skill/SKILL.md

# Project Skill
code .claude/skills/my-skill/SKILL.md
```

Changes take effect the next time you start Claude Code.

## Remove a Skill

Delete the Skill directory:

```bash
# Personal
rm -rf ~/.claude/skills/my-skill

# Project
rm -rf .claude/skills/my-skill
git commit -m "Remove unused Skill"
```

## Best practices

### Keep Skills focused

One Skill should address one capability:

**Focused**:
- "PDF form filling"
- "Excel data analysis"
- "Git commit messages"

**Too broad**:
- "Document processing" (split into separate Skills)
- "Data tools" (split by data type or operation)

### Write clear descriptions

Include specific triggers in your description:

**Clear**:
```
description: Analyze Excel spreadsheets, create pivot tables, and generate charts. Use when working with Excel files, spreadsheets, or analyzing tabular data in .xlsx format.
```

**Vague**:
```
description: For files
```

### Test with your team

Have teammates use Skills and provide feedback:
- Does the Skill activate when expected?
- Are the instructions clear?
- Are there missing examples or edge cases?

### Document Skill versions

Add a version history section to SKILL.md:

```markdown
# My Skill

## Version History
- v2.0.0 (2025-10-01): Breaking changes to API
- v1.1.0 (2025-09-15): Added new features
- v1.0.0 (2025-09-01): Initial release
```

## Troubleshooting

### Claude doesn't use my Skill

**Check**: Is the description specific enough?

**Too generic**:
```
description: Helps with data
```

**Specific**:
```
description: Analyze Excel spreadsheets, generate pivot tables, create charts. Use when working with Excel files, spreadsheets, or .xlsx files.
```

**Check**: Is the YAML valid?

```bash
cat .claude/skills/my-skill/SKILL.md | head -n 15
```

**Check**: Is the Skill in the correct location?

```bash
# Personal Skills
ls ~/.claude/skills/*/SKILL.md

# Project Skills
ls .claude/skills/*/SKILL.md
```

### Skill has errors

**Check**: Do scripts have execute permissions?

```bash
chmod +x .claude/skills/my-skill/scripts/*.py
```

**Check**: Are file paths correct?

**Correct**: `scripts/helper.py`
**Wrong**: `scripts\helper.py` (Windows style)

### Multiple Skills conflict

Be specific in descriptions to help Claude choose the right Skill:

```markdown
# Skill 1
description: Analyze sales data in Excel files and CRM exports. Use for sales reports, pipeline analysis, and revenue tracking.

# Skill 2
description: Analyze log files and system metrics data. Use for performance monitoring, debugging, and system diagnostics.
```

## Examples

### Simple Skill (single file)

```
commit-helper/
└── SKILL.md
```

```markdown
---
name: generating-commit-messages
description: Generates clear commit messages from git diffs. Use when writing commit messages or reviewing staged changes.
---

# Generating Commit Messages

## Instructions

1. Run `git diff --staged` to see changes
2. I'll suggest a commit message with:
   - Summary under 50 characters
   - Detailed description
   - Affected components

## Best practices
- Use present tense
- Explain what and why, not how
```

### Skill with tool permissions

```
code-reviewer/
└── SKILL.md
```

```markdown
---
name: code-reviewer
description: Review code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.
allowed-tools: Read, Grep, Glob
---

# Code Reviewer

## Review checklist

1. Code organization and structure
2. Error handling
3. Performance considerations
4. Security concerns
5. Test coverage

## Instructions

1. Read the target files using Read tool
2. Search for patterns using Grep
3. Find related files using Glob
4. Provide detailed feedback on code quality
```

### Multi-file Skill

```
pdf-processing/
├── SKILL.md
├── FORMS.md
├── REFERENCE.md
└── scripts/
    ├── fill_form.py
    └── validate.py
```

**SKILL.md**:

```markdown
---
name: pdf-processing
description: Extract text, fill forms, merge PDFs. Use when working with PDF files, forms, or document extraction. Requires pypdf and pdfplumber packages.
---

# PDF Processing

## Quick start

Extract text:
```python
import pdfplumber
with pdfplumber.open("doc.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

For form filling, see [FORMS.md](FORMS.md).
For detailed API reference, see [REFERENCE.md](REFERENCE.md).

## Requirements
Packages must be installed in your environment:
```bash
pip install pypdf pdfplumber
```
```

Claude loads additional files only when needed.

## Next steps

- [Authoring best practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [Agent Skills overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Use Skills in the Agent SDK](https://docs.claude.com/en/docs/agent-sdk/skills)
