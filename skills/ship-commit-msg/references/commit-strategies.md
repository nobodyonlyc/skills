# Commit Strategies

## When to Squash vs. Split

A good git history tells a story. One massive commit that does 5 different things is hard to review, hard to revert, and hard to understand.

### Split Commits (Atomic Commits)
If the staged diff contains multiple distinct, unrelated changes, you should suggest splitting them into multiple atomic commits.
**Examples of when to split:**
- A bug fix (`fix`) and a new feature (`feat`) in the same staging area.
- Fixing a typo in the documentation (`docs`) while refactoring a core module (`refactor`).
- Updating dependencies (`chore`) alongside a feature implementation.

**Action:** Recommend to the user: "I notice there are distinct changes here (a fix and a doc update). Would you like me to unstage and split them into two atomic commits, or commit them together?"

### Squash Commits
If the changes represent a single, cohesive unit of work, they belong in one commit.
**Examples of when to squash (or commit together):**
- Adding a function and its corresponding unit tests (`feat` or `fix` depending on context).
- Renaming a variable across 15 different files (`refactor`).

**Action:** Generate a single, comprehensive commit message that covers the cohesive unit.
