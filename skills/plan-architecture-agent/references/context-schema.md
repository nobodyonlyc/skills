# Context JSON Schema

When evaluating the system architecture, you MUST generate a `.harness/context.json` file in the project directory. This file acts as the machine-readable source of truth for the project's technical context.

## Schema Definition

Ensure the JSON adheres exactly to the structure below. Only include the `microservices` array if `architecture_pattern` is "Microservices".

```json
{
  "project_name": "string (e.g., 'E-Commerce Platform')",
  "user_role": "Developer | Non-Technical",
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
