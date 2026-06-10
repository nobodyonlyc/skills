# Feature-State Merge Convention (team development)

`.harness/features.json` is the one file every feature branch touches, so it is the most likely merge-conflict point. These rules keep conflicts rare and mechanical to resolve.

## Why conflicts stay small
- **Deterministic order**: the CLI serializes features sorted by `priority ASC, id ASC`, and each feature's verification list is sorted by insertion id. The same database always produces byte-identical JSON, so diffs reflect real changes only — not reordering noise.
- **Read-only commands don't write**: `status` and `resume` never call sync-out, so simply viewing state never touches the file.
- **One feature per branch (WIP=1)**: each branch typically adds/edits a single feature block, so two branches rarely touch the same lines.

## Resolving a conflict in features.json
A conflict here is almost always two branches adding *different* features, or editing *different* features' status. Resolve by keeping **both** sides:

1. Take the union of all `features[]` entries from both sides. Each `id` is unique, so there is no true overwrite — keep every distinct id.
2. If the **same id** was edited on both sides (e.g. status changed), prefer the entry with the more advanced status (`passing` > `blocked`/`in_progress` > `not_started`); if still unclear, ask the feature's `assignee`.
3. Re-run any harness command (e.g. `./harness status`) — it imports the merged JSON, then the next state-mutating command rewrites it in canonical sorted order, normalizing whitespace.
4. Commit the normalized file.

Never hand-resolve by deleting one side's features to make the conflict disappear — that silently drops backlog items.

## Priority collisions
Two features may share a `priority`; `id` breaks the tie deterministically. To force a specific order, give them distinct priorities. Child-tasks already do this via `parent_priority * 100 + n` (see [task-convention](task-convention.md)).
