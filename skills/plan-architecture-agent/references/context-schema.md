# Context JSON Schema

When evaluating the system architecture, you MUST generate a `.harness/context.json` file in the project directory. This file acts as the machine-readable source of truth for the project's technical context.

## Schema Definition

Ensure the JSON adheres exactly to the structure below. Only include the `microservices` array if `architecture_pattern` is "Microservices".

```json
{
  "project_name": "string (e.g., 'E-Commerce Platform')",
  "user_role": "Developer | Non-Technical",
  "auto_advance": "boolean (optional) — autonomous US chaining; see Rules",
  "size": "Small | Medium | Enterprise",
  "platform": ["Web", "Mobile", "CLI", "API", "Background Job"],
  "techstack": {
    "frontend": ["Next.js", "TailwindCSS"],
    "backend": ["Node.js", "Express", "Prisma"],
    "database": ["PostgreSQL", "Redis"]
  },
  "architecture_pattern": "Monolithic | Microservices | Serverless",
  "microservices": [
    {
      "name": "string (e.g., 'auth-service')",
      "description": "string (brief purpose of the service)",
      "techstack": {
        "framework": "string (e.g., 'FastAPI')",
        "database": "string (e.g., 'MongoDB')"
      }
    }
  ]
}
```

## Rules
- Do not output trailing commas in the JSON.
- If the `architecture_pattern` is not Microservices, leave the `microservices` array empty (`[]`).
- Create the `.harness` directory if it does not exist before writing the file.

## `auto_advance` — US chaining between stories
Controls what happens after a User Story reaches `passing` during execution (Route 2). Three effective behaviors from `{unset, true, false}`:
- **Effective value:**
  - `auto_advance: true` → **ON** (chain continuously, no asking).
  - `auto_advance: false` → **OFF** (hard stop and hand back after each US).
  - **absent (default)** → **ON** for `user_role == "Non-Technical"`, **ASK** for `Developer`.
- **ASK (dev default):** after a US passes, the agent does **not** go idle — it presents an interactive choice (Claude Code `AskUserQuestion`; the tool's equivalent elsewhere): **[Run next US]** / **[Run several / all remaining]** (switch to continuous chaining) / **[Stop here]**. This lets the user run many US back-to-back without re-prompting, while never stalling silently. Choosing "Run several" may persist `auto_advance: true`.
- **When ON:** after a US reaches `passing` (all child-tasks verified), the agent immediately selects the next-highest-priority unfinished US and starts it **without waiting** — chaining until the backlog is exhausted. This still honours **WIP = 1** (one US at a time) and **never weakens `./harness verify`** — it only changes the human handoff *between* stories. See [route-2-us-execution.md](../../workflow-intake/references/route-2-us-execution.md).
- **Hard stops (always return control, even when ON):** the backlog is exhausted, a US/task is `blocked`, `./harness verify` fails and cannot be auto-resolved, or an irreversible/outward-facing action (deploy, release, destructive command) needs sign-off.
