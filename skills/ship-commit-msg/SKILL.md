---
name: ship-commit-msg
description: Generate a structured, clean, and concise git commit message based on staged changes following Conventional Commits format.
---

Generate a commit message based on the current workspace state.

```bash
git status
git diff --staged
git diff
git log --oneline -5
```

## Ground Rules
- **Use Conventional Commits**: Every commit MUST follow the `type(scope): description` format.
- **Base on staged changes**: The primary focus of the commit message must be the output of `git diff --staged`.
- **Breaking Changes**: Must be explicitly noted in the footer.
- **Do not commit automatically**: Present the command (`git commit -m "..."`) and let the user execute it.

## References
Please follow the guidelines in these references carefully:
- **[Conventional Commits Specification](references/conventional-commits.md)**: Format rules, types, and scope definition.
- **[Commit Strategies](references/commit-strategies.md)**: When to squash vs. split commits.

## Examples
- **[Commit Examples](examples/commit-examples.md)**: See examples of well-structured commit messages.

## Workflow Phases
1. **Analyze Diff**: Read the staged changes and determine the core intent of the modification.
2. **Determine Strategy**: Using `references/commit-strategies.md`, decide if the changes should be split into multiple commits or kept as one. If multiple, ask the user before writing the messages.
3. **Draft Message**: Write the commit message(s) strictly adhering to `references/conventional-commits.md`.
4. **Present to User**: Present the proposed message along with the executable command:
   ```bash
   git commit -m "type(scope): description" -m "body details..."
   ```
   Ask the user for approval or adjustments before they run it.
