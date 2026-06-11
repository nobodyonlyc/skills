# Agent Tool Mapping

This repo is driven by multiple agents (Claude Code, Codex, Antigravity). Skills and workflows refer to **capabilities** by a canonical name; each agent maps them to its own concrete tool. When a skill says "use the *ask-user* capability", use whichever of these your runtime exposes.

| Canonical capability | What it does | Claude Code | Codex / others |
|---|---|---|---|
| **ask-user** | Ask the user a question / get explicit confirmation before a gated step | `AskUserQuestion` (use its **options** for choices) | interactive prompt / `ask_question` with choices |

### ask-user: prefer click-select options
Whenever a question has a **discrete set of answers** — a yes/no confirmation, "which approach", "which method (HTML vs Figma)", "approve / revise the backlog", picking from a list — present them as **selectable options the user clicks**, using the runtime's structured option capability (in Claude Code, `AskUserQuestion` with an `options` array; mark the recommended one and label it `(recommended)`). Do **not** make the user type a free-text answer to a question that is really a choice.

Use free text only when the answer is genuinely open-ended (e.g. "describe your project idea", "what should this screen show"). When in doubt, offer the likely options **plus** an implicit "something else" — the runtime already lets the user type their own answer past the options.
| **spawn-subagents** | Run independent sub-tasks in parallel | `Agent` / `Task` tool | sub-agent / `invoke_subagent` |
| **generate-image** | Produce a mockup/asset image (optional) | image tool if available, else build a static HTML/CSS mockup | same fallback |

## Model-tier hint (cost optimization)
When spawning a subagent, pass a **model-tier** so mechanical work doesn't burn a strong model. Tiers are abstract (not model names, so they don't go stale and map across runtimes):

| Tier | Use for | Claude Code | Codex / others |
|---|---|---|---|
| **fast** | Mechanical, low-judgment steps: running tests/lint, file ops, commit messages, formatting reports | `Agent(model: "haiku")` | cheapest capable model |
| **strong** (default) | Judgment work: design, planning, code review, QA, security, orchestration | session model (`Agent` default) | default model |

Default tier per skill group is set in [skills/CATEGORIES.md](../skills/CATEGORIES.md). Rules:
- The orchestrator passes the tier when it spawns a subagent for a skill.
- **When in doubt, use `strong`.** Saving tokens must never weaken a review/test/verify gate — quality outranks cost (the loops are already capped for runaway protection, see [autonomy-mode](autonomy-mode.md) and the iteration caps).

Rules:
- If your runtime lacks a capability (e.g. **generate-image**), use the documented fallback — never block on a missing tool.
- A "hard gate" in a skill means: you MUST use **ask-user** and receive explicit approval before continuing — **unless** the run is in `auto` mode, where the gate becomes a logged decision (see [autonomy-mode](autonomy-mode.md)). The always-stop list in that doc overrides every mode.
