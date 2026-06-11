# Example — Bootstrapping a small task-tracker SaaS

Input: `/workflow-bootstrap a simple team task tracker with auth and a REST API`

## Phase 1 — architecture-agent
The interview classifies the user as **Dev**, small project. Decisions captured:
- Stack: TypeScript + Fastify, PostgreSQL, React (Vite) frontend, Docker Compose for local.
- Auth: email/password + JWT.

Output written: `docs/SYSTEM_ARCHITECTURE.md` with stack, a 4-table data model (`users`, `teams`, `tasks`, `memberships`), and a roadmap of 6 epics.

## Phase 2 — BA & per-component SPECs
`docs/BA.md` captures goals, the two personas (team admin, member), the core journeys, and out-of-scope items. A follow-up question clarifies invite flow. Then per-component SPECs are written and confirmed: `docs/spec/frontend.md` (screens: login, team list, board), `docs/spec/backend.md` (auth + teams + tasks endpoints), `docs/spec/database.md` (the 4 tables). These are what the backlog reads next.

## Phase 3 — backlog (main agent) + skeleton (subagent)
The **us-backlog-generator runs in the main agent** (so it can ask the user and run `./harness add`). It reads the architecture **and** the `docs/spec/*` SPECs, drafts 11 User Stories, and presents:

| ID  | Story                                   | Priority |
|-----|-----------------------------------------|----------|
| F01 | Project setup & CI                      | 1        |
| F02 | User signup/login (JWT)                 | 2        |
| F03 | Create & list teams                     | 3        |
| ... | ...                                     | ...      |

User approves → `./harness add` populates `.harness/features.json`.

In parallel, **Subagent B (project-skeleton-generator)** scaffolds `apps/api`, `apps/web`, `docker-compose.yml`, `.env.example`, and a smoke test that boots the API and hits `/health`. It consults [dev-db-designer](../../dev-db-designer/SKILL.md) to emit the initial migration for the 4 tables.

## Phase 4 — common design phase (UI project)
Basic DB design confirmed. `docs/spec/design-system.md` is established and approved (minimal/professional, token block). Then [workflow-prototype](../../workflow-prototype/SKILL.md) renders the login, team-list, and board screens as HTML/CSS using those tokens; browser preview → one round of feedback → approved. Design-phase artifacts are committed before any feature work.

## Phase 5 — verify & handoff
```
$ ./init.sh        # installs deps, runs baseline smoke test → PASS
$ ./harness status # prints the 11-feature backlog
```
STOP. Agent reports: "Bootstrap complete. Pick one feature (WIP=1) to start — F01 is highest priority." No feature code is written.
