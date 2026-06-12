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

## `auto_advance` — autonomous US chaining
Controls whether the agent stops for human confirmation between User Stories during execution (Route 2).
- **Effective value:** `auto_advance` if present; otherwise it **defaults to `true` when `user_role` is `Non-Technical`**, and `false` for `Developer`. Set it explicitly to override the default either way (e.g. a dev who wants hands-off runs sets `true`; a non-tech user who wants to review each US sets `false`).
- **When ON:** after a US reaches `passing` (all child-tasks verified), the agent immediately selects the next-highest-priority unfinished US and starts it **without waiting** for the user to say "run the next one" — and keeps chaining until the backlog is exhausted. This still honours **WIP = 1** (one US at a time) and **never weakens `./harness verify`** — it only removes the human handoff *between* stories. See [route-2-us-execution.md](../../workflow-intake/references/route-2-us-execution.md).
- **Hard stops (always return control, even when ON):** the backlog is exhausted, a US/task is `blocked`, `./harness verify` fails and cannot be auto-resolved, or an irreversible/outward-facing action (deploy, release, destructive command) needs sign-off.
