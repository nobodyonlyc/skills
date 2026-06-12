# Common design phase (Routes 1 & 3)

Runs after analysis and **before** per-US execution. Produces the shared artifacts the US implementations build on: a basic DB design, an approved **design system**, and an approved mock UI. Reused by [Route 1](route-1-new-project.md) and Route 3.

## 1. Basic DB design
From the BA and the tech-stack SPEC, drive [dev-db-designer](../../dev-db-designer/SKILL.md) to produce a **basic schema** (core entities, relationships, key constraints) under `docs/spec/database.md` / migration stubs. Keep it foundational — full per-feature schema work happens inside each US.

## 2. Design system (establish FIRST, if the project has a UI)
Before drawing any screen, decide the project's visual language once and persist it to **`docs/spec/design-system.md`** (committed). This is the single source of truth every later prototype — the initial mock **and** each per-US screen — reads and reuses, so the UI stays consistent instead of each prototype reinventing its own look.

**Offer concrete directions, don't default.** Present **2–3 distinct style directions** (e.g. *minimal/editorial* · *warm/friendly* · *bold/high-contrast* · *data-heavy/dashboard*), each with a one-line feel and a **sample `:root` token preview** (accent hue, font pairing, radius/shadow), and let the user pick via **ask-user** (click-select). Defaulting to "generic blue + Inter" is the main cause of bland prototypes — see the [design-system reference](../../core-prototype/references/design-system.md).

`docs/spec/design-system.md` must capture (tuned to the chosen direction):
- **Style direction** — the chosen feel, in a sentence.
- **Color palette** incl. **semantic roles** (success/warning/danger/info) and a focus-ring color; **typography** — a heading+body **font pairing** and a real **type scale** (not two sizes); **spacing scale** (4/8pt); **breakpoints**; **radius/elevation** scale; **motion** tokens; and **component conventions** (button/input/card styles).
- A copy-pasteable **`:root { … }` CSS custom-property block** holding the actual token values (all categories above), so an HTML/CSS prototype can drop it straight in.

Get explicit **ask-user** approval of the design system **before** generating screens.

## 3. Mock UI
If the project has a UI, generate the **mock UI** from the FE SPEC via [workflow-prototype](../../workflow-prototype/SKILL.md) (UI only — no backend/DB), **styled with the approved `docs/spec/design-system.md` tokens**:
- It renders **every screen + function** in `docs/spec/frontend.md`.
- Method: standalone **HTML/CSS/JS**, or **Figma via an MCP connector** if the SPEC requires it.
- Mandatory preview — **browser** for HTML/CSS/JS, or the **MCP tool** for Figma — then iterate: present → feedback → regenerate/extend → re-preview, until the user approves every screen. Feedback that changes the look updates `design-system.md` so it stays the source of truth.

## Gates
- **ask-user** approval is required for the DB design, the **design system**, and the mock UI before leaving this phase; on feedback, redo that artifact.
- **Hook-enforced:** for a UI project (`docs/spec/frontend.md` exists), `hooks/harness-phase-guard.sh` blocks `./harness start` and app-code edits until **both** `docs/spec/design-system.md` and `prototype/*.html` exist. This is the mechanical backstop for the common failure where the agent jumps from the backlog straight to US execution and skips the prototype. The backlog itself (`./harness add`) is *not* blocked — only US execution.
- Record each artifact as a harness task where useful ([task-convention](../../../resources/task-convention.md)).
- **Commit the design-phase artifacts before starting the first US** (a phase checkpoint: `git add docs/spec docs/SYSTEM_ARCHITECTURE.md prototype && git commit -m "design phase"`). Otherwise the first US's `harness verify` checkpoint sweeps these shared artifacts into a commit labelled for that single feature.

→ Once all are approved and committed, proceed to per-US execution via [Route 2](route-2-us-execution.md).
