# Phase 3 — Verification & Checkpoint

**Skills used:** `harness cli`

After the QA pass is complete and blockers are either fixed or deferred, you must sync the state with the Harness environment manager.

## 1. Verify Feature
Run the harness verify command to ensure the feature satisfies the system's baseline checks.
```bash
./harness verify
```
*If this fails, the feature is NOT done. You must fix the verification errors or escalate to the user.*

## 2. Stop Session
Once verification passes (or if the user explicitly wants to stop with known issues), checkpoint the progress so the next session can continue smoothly.
```bash
./harness session stop
```

## 3. Clean up
Remove any temporary test files, coverage reports, or debug logs generated during Phase 1.
```bash
./harness clean
```

**STOP.** Do not start new work after Phase 3.
