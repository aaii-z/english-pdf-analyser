# GitHub Actions CI/CD Setup Guide

This guide explains how to set up GitHub Actions for automatic Docker image builds and pushes to Docker Hub.

## Overview

The GitHub Actions workflow (`.github/workflows/docker-build.yml`) automatically:
- Builds the Docker image when you push a version tag (e.g., `v1.0.0`)
- Pushes the image to Docker Hub with semantic version tags
- Uses GitHub Actions cache to speed up builds

## Setting Up Docker Hub Credentials

### Step 1: Create a Docker Hub Access Token

1. Log in to [Docker Hub](https://hub.docker.com/)
2. Click on your username in the top right → **Account Settings**
3. Go to **Security** → **Access Tokens**
4. Click **New Access Token**
5. Give it a description (e.g., "GitHub Actions - PDF Analyzer")
6. Set permissions to **Read, Write, Delete**
7. Click **Generate**
8. **IMPORTANT**: Copy the token immediately - you won't be able to see it again!

### Step 2: Add Secrets to GitHub Repository

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add two secrets:

   **Secret 1:**
   - Name: `DOCKER_USERNAME`
   - Value: Your Docker Hub username (e.g., `yourusername`)
   
   **Secret 2:**
   - Name: `DOCKER_PASSWORD`
   - Value: The access token you generated in Step 1

### Step 3: Update the Workflow (if needed)

The workflow uses `${{ secrets.DOCKER_USERNAME }}/english-pdf-analyzer` as the image name. This means your image will be pushed to:
```
docker.io/yourusername/english-pdf-analyzer
```

If you want a different image name, edit `.github/workflows/docker-build.yml` and change the `images` field in the metadata step.

## How the Workflow Works

### Triggers
- **Git tags**: Builds and pushes the image when you create a version tag (e.g., `v1.0.0`, `v2.1.3`)

### Tags
The workflow automatically creates multiple tags based on your git tag:
- `latest` - Always points to the latest version
- `1.0.0` - Full semantic version (from tag `v1.0.0`)
- `1.0` - Major.minor version
- `1` - Major version only

### Example Tags
After pushing tag `v1.0.0`, you'll get:
```
yourusername/english-pdf-analyzer:latest
yourusername/english-pdf-analyzer:1.0.0
yourusername/english-pdf-analyzer:1.0
yourusername/english-pdf-analyzer:1
```

### How to Create and Push a Tag
```bash
# Create a tag
git tag v1.0.0

# Push the tag to GitHub
git push origin v1.0.0

# The workflow will automatically trigger and build/push the image
```

## Using the Published Image

Once the workflow runs successfully, anyone can pull and run your image:

```bash
# Pull the latest version
docker pull yourusername/english-pdf-analyzer:latest

# Run the container
docker run -d -p 8080:8080 yourusername/english-pdf-analyzer:latest
```

## Security Best Practices

✅ **DO:**
- Use Docker Hub access tokens (not your password)
- Set minimal required permissions on tokens
- Use GitHub Secrets for credentials
- Rotate tokens periodically

❌ **DON'T:**
- Commit credentials to the repository
- Share access tokens publicly
- Use your Docker Hub password directly

## Monitoring Builds

1. Go to your GitHub repository
2. Click the **Actions** tab
3. You'll see all workflow runs
4. Click on a run to see detailed logs

## Troubleshooting

### Build fails with "unauthorized" error
- Check that `DOCKER_USERNAME` and `DOCKER_PASSWORD` secrets are set correctly
- Verify the access token hasn't expired
- Ensure the token has write permissions

### Image not appearing on Docker Hub
- Verify you pushed a version tag (e.g., `v1.0.0`), not just a regular commit
- Check that the tag follows the format `v*.*.*`
- Check the Actions logs for errors

### Build is slow
- The workflow uses GitHub Actions cache to speed up subsequent builds
- First build will be slower, subsequent builds should be faster

## Optional: Adding Tests

You can extend the workflow to run tests before building:

```yaml
- name: Run tests
  run: |
    python -m pytest tests/
```

Add this step before the "Build and push Docker image" step.

## Next Steps

1. Set up the Docker Hub secrets as described above
2. Push your code to GitHub
3. Create and push a version tag (e.g., `git tag v1.0.0 && git push origin v1.0.0`)
4. The workflow will automatically run
5. Check the Actions tab to monitor progress
6. Once complete, your image will be available on Docker Hub!
