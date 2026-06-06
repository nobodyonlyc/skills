# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This repo is a curated library of Claude Code skills, agents, and workflows. Skills are slash commands (`/skill-name`) loaded from `.claude/commands/`.

## Structure

```
.claude/
  commands/       ← All skills (slash commands) as .md files
  settings.json   ← Harness config: permissions, hooks
hooks/            ← Shell scripts used by hooks
CLAUDE.md
```

## How Skills Work

Each `.md` file in `.claude/commands/` becomes a `/skill-name` slash command. File content is injected as the opening message. `$ARGUMENTS` receives anything typed after the command name.

**Key patterns:**
- **Context gathering** — bash blocks at the top gather state before Claude reasons
- **Arguments** — `$ARGUMENTS` for parameters (e.g. `/deploy staging`, `/fix login broken`)
- **Decision points** — always confirm before irreversible actions (push, deploy, release)
- **Agents** — instruct Claude to use the `Agent` tool to spawn parallel subagents

## Writing Great Skills

1. Gather context first with bash blocks — don't ask Claude to guess
2. Specify exact output format — table, bullet list, severity levels
3. Gate irreversible actions behind explicit user confirmation
4. Keep each skill single-purpose; use workflows for multi-step orchestration

## Hooks

| Hook | Trigger | Script |
|---|---|---|
| git-guard | PreToolUse(Bash) | Blocks force-push to main/master |
| notify | Stop | Desktop/terminal notification when Claude finishes |

Hook scripts are in `hooks/`. Add/remove hooks by editing `.claude/settings.json`.

## Available Skills

### Git & Code Quality
| Command | Description |
|---|---|
| `/commit-msg` | Analyze staged changes, propose conventional commit message |
| `/pr-create` | Draft and create a PR with title, summary, test plan |
| `/pr-review [PR#]` | Review a PR diff — bugs, security, suggestions |
| `/code-review [path]` | Review current changes or a specific file |
| `/security-review [path]` | OWASP-focused security audit of changes |

### Development
| Command | Description |
|---|---|
| `/fix <bug description>` | Root-cause a bug and apply minimal fix |
| `/feature <description>` | Plan and implement a feature |
| `/refactor <target>` | Identify code smells and refactor safely |
| `/explain <file or function>` | Plain-language explanation of complex code |
| `/test-gen <file>` | Generate tests following project conventions |

### Deploy & Release
| Command | Description |
|---|---|
| `/deploy <environment>` | Pre-flight checks, build, deploy, verify |
| `/release [major\|minor\|patch]` | Changelog, version bump, tag, push |

### Workflows (Multi-Agent)
| Command | Description |
|---|---|
| `/workflow-feature <description>` | Parallel requirements + test planning, then implement |
| `/workflow-bugfix <bug>` | Parallel root-cause + impact analysis, then fix |
| `/workflow-review-deep [PR#]` | One agent per file for thorough parallel review |
| `/workflow-release-prep [version]` | Parallel changelog + health check + dep audit |
