# Skill Categories

Skills are stored **flat** (one directory per skill, so `/skill-name` discovery works across Claude Code, Codex, and Antigravity). Grouping is encoded in the **name prefix** — this file is the index.

| Group | Prefix | Skills |
|---|---|---|
| **Workflows** — multi-agent orchestrators (entry points) | `workflow-` | workflow-intake, workflow-bootstrap, workflow-onboard, workflow-feature, workflow-bugfix, workflow-prototype, workflow-qa, workflow-release-prep, workflow-review-deep |
| **Planning** — turn an idea into spec, backlog, and skeleton | `plan-` | plan-architecture-agent, plan-us-backlog-generator, plan-project-skeleton-generator |
| **Development** — write the code, by component type | `dev-` | dev-be-developer, dev-fe-developer, dev-cli-tool-developer, dev-batch-developer, dev-db-designer |
| **Quality** — review, test, and harden changes | `check-` | check-code-review, check-security-review, check-pr-review, check-qa, check-test-gen, check-refactor |
| **Delivery** — commit, PR, release, deploy, package | `ship-` | ship-commit-msg, ship-pr-create, ship-deploy, ship-release, ship-mcp-build |
| **Core** — everyday single-agent dev tasks | `core-` | core-explain, core-fix, core-feature, core-prototype, core-file-ops |

## Notes
- The prefix is **classification only** — every skill still runs independently via `/skill-name`.
- Workflows drive the leaf skills; each `workflow-*/SKILL.md` lists the skills it uses and links to them.
- Tool-capability names used inside skills (ask-user, spawn-subagents, generate-image) are mapped per agent in [../resources/agent-tool-mapping.md](../resources/agent-tool-mapping.md).
