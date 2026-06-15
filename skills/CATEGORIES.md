# Skill Categories

Skills are stored **flat** (one directory per skill: `skills/<name>/SKILL.md`). Grouping is encoded in the **name prefix** — this file is the index. Invocation differs per tool: **Claude Code** loads them as the `harness` plugin (`harness:<name>`); **Codex** reads `skills/<name>/SKILL.md` by path; **Antigravity** uses the `.agent/` workflows (`/harness-*`).

| Group | Prefix | Default model-tier | Skills |
|---|---|---|---|
| **Workflows** — multi-agent orchestrators (entry points) | `workflow-` | strong | workflow-intake, workflow-bootstrap, workflow-onboard, workflow-feature, workflow-bugfix, workflow-prototype, workflow-qa, workflow-release-prep, workflow-review-deep |
| **Planning** — turn an idea into spec, backlog, and skeleton | `plan-` | strong | plan-architecture-agent, plan-us-backlog-generator, plan-project-skeleton-generator |
| **Development** — write the code, by component type | `dev-` | strong | dev-be-developer, dev-fe-developer, dev-cli-tool-developer, dev-batch-developer, dev-db-designer, dev-go-developer, dev-js-ts-developer, dev-design-patterns, dev-system-design, dev-detailed-design |
| **Quality** — review, test, and harden changes | `check-` | strong | check-code-review, check-security-review, check-pr-review, check-qa, check-test-gen, check-refactor |
| **Delivery** — commit, PR, release, deploy, package | `ship-` | **fast** (except ship-release/ship-deploy → strong) | ship-commit-msg, ship-pr-create, ship-deploy, ship-release, ship-mcp-build |
| **Core** — everyday single-agent dev tasks | `core-` | **fast** for core-file-ops; strong for core-explain/core-explore/core-fix/core-feature/core-prototype | core-explain, core-explore, core-fix, core-feature, core-prototype, core-file-ops |

## Notes
- The prefix is **classification only** — every skill still runs independently (Claude Code: `harness:<name>`; Codex: by file path; Antigravity: `.agent/` workflows).
- Workflows drive the leaf skills; each `workflow-*/SKILL.md` lists the skills it uses and links to them.
- Tool-capability names used inside skills (ask-user, spawn-subagents, generate-image) are mapped per agent in [../resources/agent-tool-mapping.md](../resources/agent-tool-mapping.md).
- **Model-tier** (`fast` / `strong`) tells an orchestrator which model to spawn a skill's subagent on; see the model-tier section in [agent-tool-mapping.md](../resources/agent-tool-mapping.md). `strong` is the safe default — only the mechanical skills above default to `fast`, and any judgment step escalates to `strong` when in doubt.
