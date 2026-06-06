Prototype request: $ARGUMENTS

This is a multi-agent rapid prototyping workflow. Spawn the following agents IN PARALLEL:

**Agent 1 — Stack researcher**: Scan the existing codebase for languages, frameworks, and libraries already in use. Find similar existing code that could be reused or adapted. Produce: (1) recommended tech stack for the prototype, (2) existing code snippets to reuse, (3) any gotchas or constraints from the current setup.

**Agent 2 — Interface designer**: Based on the prototype description, define the minimal interface: inputs, outputs, and the single core interaction. If it's a UI, sketch a rough layout in ASCII. If it's an API/CLI/library, define the function signatures or commands. Produce: a concrete interface spec (not implementation).

After both agents complete:

1. Present stack recommendation + interface spec to user. Confirm or adjust.
2. Build the prototype:
   - Single file if possible
   - Use the stack from Agent 1
   - Implement the interface from Agent 2
   - Hardcode anything that's not the core concern
3. Run it and show real output.
4. Handoff notes:
   - What's hardcoded / stubbed
   - What would need to change for production
   - Estimated effort to productionize (S/M/L/XL)
