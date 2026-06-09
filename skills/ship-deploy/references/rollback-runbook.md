# Rollback Runbook

If a deployment fails during the build phase, deployment phase, or post-deploy health check, you must execute a rollback to restore service stability immediately.

## 1. Identify the Failure
- **Build Failure**: The new code never went live. No rollback required, but notify the user.
- **Deploy Failure (Partial)**: The service might be in an inconsistent state.
- **Health Check Failure**: The service is live but broken. Immediate rollback required.

## 2. Rollback Procedures by Target

### Vercel
Vercel keeps immutable deployments. To rollback, find the previous successful deployment URL and alias it to the main domain, or use the CLI:
```bash
npx vercel rollback
```

### Docker
If the new container fails to start or is unhealthy, revert to the previous image tag.
```bash
# Stop new container
docker stop app-name
# Start old container (assuming previous tag was known)
docker run -d --name app-name app-name:previous-tag
```

### Bare Metal / VPS
Revert the git commit and restart the service.
```bash
ssh user@server "cd /var/www/app && git checkout HEAD^1 && npm install && pm2 restart all"
```

## 3. Post-Rollback Actions
1. Verify the service is back online using the health check.
2. Generate a post-mortem summary for the user explaining what failed and confirming the rollback was successful.
