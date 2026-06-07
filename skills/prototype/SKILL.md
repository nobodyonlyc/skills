---
name: prototype
description: Rapidly prototype a new feature or design concept, focusing on speed and minimal functionality for feedback.
---

Prototype to build: $ARGUMENTS

```bash
git log --oneline -3
ls -la
find . -name "package.json" -o -name "pyproject.toml" -o -name "go.mod" | head -3
```

Build a working prototype as fast as possible. Optimize for **speed and clarity**, not production quality.

## Ground rules

- **No over-engineering** — no abstraction layers, no config systems, no plugin architectures unless the prototype itself is about those things
- **Hardcode values** — use hardcoded URLs, credentials (non-prod), magic numbers freely; leave TODOs for the real implementation
- **Single file preferred** — put everything in one file unless the language makes that impractical
- **Real dependencies** — use existing libraries; don't reimplement what npm/pip/go already has
- **No tests** — unless the prototype IS a testing tool

## Workflow

1. **Confirm the goal** — one sentence: what should the prototype do? What's the success condition?
2. **Pick the simplest stack** — plain Node/Python/bash script, not a full framework
3. **Build it** — write the code, run it, show output
4. **Demonstrate** — run the prototype and show real output, not just "it compiled"
5. **Handoff notes** — bullet list of shortcuts taken that would need fixing before production

If the prototype doesn't work on first run, fix it — don't hand over broken code.
