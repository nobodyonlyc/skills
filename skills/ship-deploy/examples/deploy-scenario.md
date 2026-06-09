# Deploy Scenario Example

## Scenario: Deploying to Production (Docker)

1. **Pre-flight Checks**:
   - `git status` shows clean tree.
   - Branch is `main`.
   - `npm test` passes.
2. **Build**:
   - Runs `docker build -t my-app:v1.2.0 .`
   - Build succeeds.
3. **Deploy**:
   - Agent asks user: "Ready to deploy `my-app:v1.2.0` to production via docker-compose. Proceed? (y/n)"
   - User says "y".
   - Runs `docker-compose up -d`
4. **Verify**:
   - Agent runs `curl -f http://localhost:8080/health`
   - **Result**: `HTTP 500 Internal Server Error`
5. **Rollback Triggered**:
   - Agent immediately identifies failure.
   - Runs `docker-compose down` and modifies `docker-compose.yml` to revert to `v1.1.9`.
   - Runs `docker-compose up -d`.
   - Agent runs `curl -f http://localhost:8080/health`.
   - **Result**: `HTTP 200 OK`.
6. **Report**:
   - Agent reports: "Deployment of v1.2.0 failed health checks (HTTP 500). I have successfully rolled back to v1.1.9. The service is healthy. Please review the application logs to determine the cause of the crash."
