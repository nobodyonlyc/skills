---
name: ship-deploy
description: Perform pre-flight checks, build the project, and run the deployment workflow for a target environment.
---

Deploy target: $ARGUMENTS (environment name, e.g., staging / production)

This skill guides the robust deployment of code. It replaces simple "run deploy" scripts with a structured pipeline: Pre-flight → Build → Deploy → Verify → Rollback (if necessary).

## References
Please follow the guidelines in these references carefully:
- **[Pre-Flight Checks](references/pre-flight-checks.md)**: Mandatory verification before any build/deploy steps.
- **[Deployment Targets](references/deployment-targets.md)**: Standard commands and abstractions for Docker, Vercel, AWS, etc.
- **[Rollback Runbook](references/rollback-runbook.md)**: Immediate steps to take if the deployment fails or verification fails.

## Examples
- **[Deploy Scenario](examples/deploy-scenario.md)**: An example of a deployment execution that hits an issue and rolls back.

## Workflow Phases
1. **Pre-flight Checks**: Execute the checklist in `references/pre-flight-checks.md`. Do not proceed if any check fails.
2. **Build**: Run the project's build command (e.g., `npm run build`, `cargo build --release`, `docker build`).
3. **Deploy**: Identify the correct deployment abstraction from `references/deployment-targets.md` and execute it. 
   - *Requirement*: Always show the deploy command to the user and ask for confirmation if deploying to `production`.
4. **Verify (Post-deploy)**: Run a health check (e.g., `curl https://target-url/health`) or a smoke test.
5. **Rollback (If needed)**: If the build, deploy, or verification steps fail, immediately trigger the procedures in `references/rollback-runbook.md`.
