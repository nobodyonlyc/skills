# Agent Tool Mapping

This repo is driven by multiple agents (Claude Code, Codex, Antigravity). Skills and workflows refer to **capabilities** by a canonical name; each agent maps them to its own concrete tool. When a skill says "use the *ask-user* capability", use whichever of these your runtime exposes.

| Canonical capability | What it does | Claude Code | Codex / others |
|---|---|---|---|
| **ask-user** | Ask the user a question / get explicit confirmation before a gated step | `AskUserQuestion` | interactive prompt / `ask_question` |
| **spawn-subagents** | Run independent sub-tasks in parallel | `Agent` / `Task` tool | sub-agent / `invoke_subagent` |
| **generate-image** | Produce a mockup/asset image (optional) | image tool if available, else build a static HTML/CSS mockup | same fallback |

Rules:
- If your runtime lacks a capability (e.g. **generate-image**), use the documented fallback — never block on a missing tool.
- A "hard gate" in a skill means: you MUST use **ask-user** and receive explicit approval before continuing.
