# Quick Setup: Docker Hub Secrets for GitHub Actions

## 🔑 Step-by-Step Guide

### 1. Create Docker Hub Access Token
1. Go to https://hub.docker.com/
2. Login → Click your username → **Account Settings**
3. **Security** → **Access Tokens** → **New Access Token**
4. Name: `GitHub Actions - English PDF Analyzer`
5. Permissions: **Read, Write, Delete**
6. Click **Generate** and **COPY THE TOKEN** (you won't see it again!)

### 2. Add Secrets to GitHub
1. Go to your GitHub repository
2. **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

Add these two secrets:

| Secret Name | Value |
|------------|-------|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_PASSWORD` | The access token from step 1 |

### 3. Create and Push a Version Tag
```bash
# Commit your changes
git add .
git commit -m "Add GitHub Actions CI/CD"
git push origin main

# Create a version tag
git tag v1.0.0

# Push the tag (this triggers the workflow)
git push origin v1.0.0
```

### 4. Monitor the Build
- Go to **Actions** tab in your GitHub repo
- Watch the workflow run
- Your image will be pushed to `docker.io/YOUR_USERNAME/english-pdf-analyzer`

## 🚀 Using Your Published Image

```bash
docker pull YOUR_USERNAME/english-pdf-analyzer:latest
docker run -d -p 8080:8080 YOUR_USERNAME/english-pdf-analyzer:latest
```

## ⚠️ Security Notes
- ✅ Use access tokens (NOT your password)
- ✅ Store credentials in GitHub Secrets
- ❌ Never commit credentials to code
- ❌ Never share access tokens publicly

---

For detailed documentation, see [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md)


## ⚠️ Security Notes
- ✅ Use access tokens (NOT your password)
- ✅ Store credentials in GitHub Secrets
- ❌ Never commit credentials to code
- ❌ Never share access tokens publicly

---

For detailed documentation, see [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md)
