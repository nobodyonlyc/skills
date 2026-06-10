# Branch-per-Feature Convention (team development)

When multiple people or agents share one harness repo, each feature is developed on its own branch so checkpoints never collide on `master` and work integrates through review.

## Branch naming
`feat/<feature_id>` — e.g. `feat/F30`, `feat/F24-T2`. One branch per feature or child-task.

## Starting work on a branch
```bash
./harness start F30 --assignee alice --branch
```
- `--branch` creates `feat/F30` (or checks it out if it already exists) and records the branch name on the feature row (visible in `.harness/features.json`).
- `--assignee` sets the owner; WIP=1 is enforced **per assignee**, so teammates each hold one active feature concurrently.
- Both flags are optional. Omitting them keeps the single-developer flow: work on the current branch, global WIP=1.

## During development
- Phase checkpoints (`harness verify`, phase-boundary commits) land on `feat/<id>`.
- `harness verify` skips its auto-checkpoint if the index already holds unrelated staged changes, so it never sweeps a teammate's work into your commit.

## Integration
- When the feature is `passing`, open a PR from `feat/<id>` into the integration branch via [ship-pr-create](../skills/ship-pr-create/SKILL.md).
- Do **not** merge directly to `master`/`main` without the review gate ([workflow-review-deep](../skills/workflow-review-deep/SKILL.md) for deeper passes).

## Conflict avoidance
- `.harness/features.json` is the one shared file every branch touches. It is sorted deterministically (priority, then id) so diffs are minimal; see [state-merge-convention](state-merge-convention.md) for the conflict-resolution rule.
- Keep each feature's code changes inside its own scope (WIP=1) to minimize cross-branch overlap.
