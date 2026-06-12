# /harness-backlog

Turn the architecture **and every detailed SPEC** into a complete User-Story backlog in `.harness/features.json`. Act as a **Product Owner**.

> The #1 cause of a thin/incomplete backlog is reading only `docs/SYSTEM_ARCHITECTURE.md`. The real work items live in the per-component SPECs. Read them all, build an explicit inventory, and check coverage before showing the user.

## Step 1 — Read architecture AND all SPECs; build an inventory
Read `docs/SYSTEM_ARCHITECTURE.md` for structure, then **every** SPEC under `docs/spec/` (`frontend.md`, `backend.md`, `database.md`, `cli.md`, any tool SPEC). Build an explicit **inventory of every work item**:
1. **Bootstrap order / dependencies** (typically Database → Backend API → Frontend UI).
2. **FE** — every **screen** and major interaction in `frontend.md`.
3. **BE** — every **endpoint / service function** in `backend.md`.
4. **DB** — every **entity / migration** in `database.md`.
5. **Business functions** named in the BA / architecture (login, catalog, checkout, email dispatch, …).

## Step 2 — Draft User Stories
For each item, draft a US with:
1. **ID** — sequential (`F01`, `F02`, … or next free id).
2. **Title** — short, descriptive.
3. **Priority** — numeric; lower runs first; respect dependency order.
4. **Area** — `core` / `db` / `api` / `ui` / `batch` / `security`.
5. **User-visible behaviour** — what is observable when done.
6. **Verifications** — executable shell commands that prove it works non-interactively (`cargo test`, `pytest tests/test_auth.py`, `[ -f src/auth.rs ]`, …).

## Step 3 — Coverage check (mandatory, before showing the user)
Build a coverage table: each inventory item → the US that covers it. Any item with **no US is a gap** — add the missing story.
Then run an **independent PM coverage review**: spawn a subagent (Senior PM, read-only) that reads the SPECs + the drafted backlog and returns, in **one report**, every SPEC item (screen / endpoint / entity / business rule) that no US covers. Add **all** missing stories in a single pass; re-run the review at most once to confirm. Only a backlog that passes coverage proceeds.

## Step 4 — Present & get approval
Present the full proposed backlog as a Markdown table (ID, Title, Area, Behaviour, Verifications) and explain the dependency/sequence. **Ask the user for explicit approval.** Do **not** write anything until they approve.

## Step 5 — Persist (do not skip)
After approval, register **every** story:
```
./harness add <id> <title> --priority <p> --area <a> --behavior <b> --verifications <cmds...>
```
Then run `./harness status` to confirm all stories are present and sorted. The turn must not end with `.harness/features.json` still holding only the placeholder.
