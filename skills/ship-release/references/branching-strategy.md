# Branching Strategy for Releases

Before tagging, ensure you are on the correct branch based on the project's strategy. Ask the user if you are unsure.

## 1. Trunk-Based Development (Default)
All releases and tags happen directly on `main` (or `master`).
- **Flow**: Commits merge to `main` -> Tag on `main` -> Deploy.

## 2. Release Branches
Used for larger teams where `main` continues moving forward, but a specific version needs to be stabilized.
- **Format**: `release/vX.Y.Z` or `release/vX.Y`
- **Flow**: Branch off `main` -> QA -> Fixes -> Tag on `release/vX.Y` -> Merge back to `main`.

## 3. Hotfix Branches
Used when a critical bug exists in production, but `main` already contains unreleased features.
- **Format**: `hotfix/vX.Y.Z`
- **Flow**: Branch off the existing production tag (e.g., `git checkout -b hotfix/v1.2.1 v1.2.0`) -> Fix the bug -> Tag `v1.2.1` -> Deploy -> Merge hotfix back into `main`.
