---
name: ship-deploy
description: Perform pre-flight checks, build the project, and run the deployment workflow for a target environment.
---

Deploy target: $ARGUMENTS (environment name, e.g. staging / production)

Pre-flight checks:

```bash
git status
git log --oneline -3
git diff --stat HEAD
```

Follow this deployment workflow:

1. **Guard rails** — Stop and warn if:
   - There are uncommitted changes
   - Current branch is not the expected deploy branch (main/master for prod)
   - Tests haven't passed (check CI status if `gh` is available)

2. **Build** — Run the project's build command (detect from package.json scripts, Makefile, or ask the user).

3. **Deploy** — Run the deploy command for the target environment. Show the command before executing and ask for confirmation if deploying to production.

4. **Verify** — After deploy, check health endpoint or run a smoke test if available.

5. **Report** — Summarize: what was deployed, from which commit, to which environment, and the verification result.

If no deploy script is found, ask the user for the deploy command before proceeding.
