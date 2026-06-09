# Release Prep Scenario Example

## 1. Audit Phase (Parallel)
- **Agent 1 (Changelog)**: Drafts v1.2.0 changelog with 2 new features and 3 fixes.
- **Agent 2 (Health Check)**: Tests pass, but discovers `packages/ui/package.json` is at `1.1.9` while `packages/core/package.json` is at `1.2.0-beta.1`. **BLOCKER**.
- **Agent 3 (Audit)**: Finds a `Moderate` severity advisory in `axios`. **Non-blocker**.

## 2. Resolve Blockers
- **Agent**: "I found a version mismatch between packages in the monorepo. I will align them to `1.1.9` before proceeding."
- **User**: "Go ahead."
- Agent aligns versions. Blocker resolved.

## 3. Apply Release
- **Agent**: "The calculated next version is `1.2.0`. Here is the proposed CHANGELOG. Shall I commit and tag?"
- **User**: "Yes."
- Agent bumps versions to `1.2.0`, updates `CHANGELOG.md`, commits, and tags `v1.2.0`.
- **Agent**: "Tagged v1.2.0 locally. Shall I push to remote?"
- **User**: "Yes."
- Agent pushes the tag.

## 4. Staging Validation
- Agent uses `ship-deploy` to push `v1.2.0` to the Vercel staging environment.
- Health check returns `200 OK`.
- **Agent**: "Staging deployment successful. The release is ready for production. Here is your draft announcement..."
