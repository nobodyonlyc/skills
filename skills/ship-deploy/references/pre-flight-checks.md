# Pre-Flight Checks

Before triggering any build or deployment process, the following checks MUST be executed and pass. If any check fails, abort the deployment and notify the user.

## 1. Git State Check
The working directory must be clean. No uncommitted changes should be deployed.
```bash
git status --porcelain
```
*Expected: Empty output.*

## 2. Branch Check
Ensure you are deploying from the correct branch.
- **Production**: Should usually be `main` or `master`.
- **Staging**: Should usually be `staging`, `dev`, or a specific feature branch.

## 3. Test Suite Verification
Run the project's fast test suite to ensure no obvious regressions were introduced locally right before deployment.
```bash
# e.g., npm test, cargo test, pytest
```
*If tests fail, ABORT deploy.*

## 4. Environment Variable Check
Ensure the necessary secrets/env vars for the target environment are available locally (if deploying from local) or configured in the CI/CD pipeline.
Check `.env` files or CLI tools (`vercel env ls`, `aws configure list`).
