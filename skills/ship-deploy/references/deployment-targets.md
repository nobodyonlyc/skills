# Deployment Targets

Identify the project's infrastructure and use the appropriate deployment strategy.

## 1. Vercel (Next.js, Frontend Apps)
**Build & Deploy Command:**
```bash
# Staging/Preview
npx vercel --build-env NODE_ENV=development

# Production
npx vercel --prod
```
*Note*: Vercel handles builds automatically in the cloud, but triggering from CLI requires these commands.

## 2. Docker / Containerized Apps
**Build Command:**
```bash
docker build -t app-name:latest .
```
**Deploy Command (e.g., Docker Compose):**
```bash
docker-compose up -d --build
```
*Note*: For remote registries, ensure `docker login` and `docker push` are executed before triggering the remote server update.

## 3. AWS (S3/CloudFront) - Static Sites
**Build Command:**
```bash
npm run build
```
**Deploy Command:**
```bash
aws s3 sync ./dist s3://your-bucket-name --delete
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

## 4. Bare Metal / VPS (SSH + Git Pull)
**Deploy Command:**
```bash
ssh user@server.ip "cd /var/www/app && git pull origin main && npm install && pm2 restart all"
```
