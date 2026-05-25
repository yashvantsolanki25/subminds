# GitHub Deployment Guide

Complete guide to push SubMinds to GitHub with automated releases and CI/CD.

---

## 📋 Prerequisites

- Git installed on your system
- GitHub account
- Repository created on GitHub (or will create during setup)

---

## 🚀 Step-by-Step Deployment

### Step 1: Initialize Git Repository

```bash
cd subminds-may-2026

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: SubMinds v1.0.0 - AI-powered subconscious decision analysis"
```

### Step 2: Create GitHub Repository

**Option A: Via GitHub Website**
1. Go to https://github.com/new
2. Repository name: `subminds-may-2026`
3. Description: "AI-powered subconscious decision analysis for F1 drivers using facial expressions and IBM Granite AI"
4. Choose: Public or Private
5. **DO NOT** initialize with README (we already have one)
6. Click "Create repository"

**Option B: Via GitHub CLI**
```bash
# Install GitHub CLI if not installed
# https://cli.github.com/

# Login
gh auth login

# Create repository
gh repo create subminds-may-2026 --public --source=. --remote=origin --description="AI-powered subconscious decision analysis for F1 drivers"
```

### Step 3: Connect Local to GitHub

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/subminds-may-2026.git

# Verify remote
git remote -v

# Set main branch
git branch -M main
```

### Step 4: Push to GitHub

```bash
# Push code
git push -u origin main
```

---

## 🏷️ Creating Releases with Tags

### Create Your First Release (v1.0.0)

```bash
# Create and push tag
git tag -a v1.0.0 -m "Release v1.0.0: Initial release with facial analysis and IBM Granite integration"
git push origin v1.0.0
```

**This will automatically:**
- ✅ Trigger GitHub Actions release workflow
- ✅ Create a GitHub Release with changelog
- ✅ Build and publish Docker image
- ✅ Generate release notes
- ✅ Attach build artifacts

### Create Subsequent Releases

```bash
# For bug fixes (1.0.0 -> 1.0.1)
git tag -a v1.0.1 -m "Release v1.0.1: Bug fixes and improvements"
git push origin v1.0.1

# For new features (1.0.1 -> 1.1.0)
git tag -a v1.1.0 -m "Release v1.1.0: Added art analysis module"
git push origin v1.1.0

# For major changes (1.1.0 -> 2.0.0)
git tag -a v2.0.0 -m "Release v2.0.0: Complete architecture redesign"
git push origin v2.0.0
```

### Semantic Versioning

Follow semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR** (v2.0.0): Breaking changes
- **MINOR** (v1.1.0): New features, backward compatible
- **PATCH** (v1.0.1): Bug fixes, backward compatible

---

## ⚙️ GitHub Actions Workflows

### 1. CI Workflow (`.github/workflows/ci.yml`)

**Triggers on:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

**What it does:**
- ✅ Tests on multiple OS (Ubuntu, Windows, macOS)
- ✅ Tests on multiple Python versions (3.9, 3.10, 3.11)
- ✅ Runs linting (flake8)
- ✅ Checks code formatting (black)
- ✅ Type checking (mypy)
- ✅ Runs tests with coverage
- ✅ Builds Docker image

### 2. Release Workflow (`.github/workflows/release.yml`)

**Triggers on:**
- Push of version tags (v*.*.*)

**What it does:**
- ✅ Creates GitHub Release
- ✅ Generates changelog
- ✅ Builds Python package
- ✅ Builds and pushes Docker image to GHCR
- ✅ Publishes to PyPI (if configured)

### 3. Docker Publish Workflow (`.github/workflows/docker-publish.yml`)

**Triggers on:**
- Push to `main` branch
- Version tags
- Pull requests

**What it does:**
- ✅ Builds Docker image
- ✅ Pushes to GitHub Container Registry
- ✅ Tags with version and latest

---

## 🔐 Setting Up Secrets

### Required Secrets

Go to: `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

1. **PYPI_API_TOKEN** (Optional - for PyPI publishing)
   - Get from: https://pypi.org/manage/account/token/
   - Used for: Publishing package to PyPI

2. **GITHUB_TOKEN** (Automatic)
   - Automatically provided by GitHub
   - Used for: Creating releases, pushing Docker images

### How to Add Secrets

```bash
# Via GitHub CLI
gh secret set PYPI_API_TOKEN

# Or via GitHub website:
# Repository → Settings → Secrets and variables → Actions → New repository secret
```

---

## 📦 Release Process Workflow

### Complete Release Workflow

```bash
# 1. Make changes
git add .
git commit -m "feat: Add new feature"

# 2. Push changes
git push origin main

# 3. Create release tag
git tag -a v1.1.0 -m "Release v1.1.0: New features"
git push origin v1.1.0

# 4. GitHub Actions automatically:
#    - Creates release
#    - Builds packages
#    - Publishes Docker image
#    - Generates changelog

# 5. Check release at:
#    https://github.com/YOUR_USERNAME/subminds-may-2026/releases
```

---

## 🐳 Using Published Docker Images

### Pull from GitHub Container Registry

```bash
# Pull latest
docker pull ghcr.io/YOUR_USERNAME/subminds-may-2026:latest

# Pull specific version
docker pull ghcr.io/YOUR_USERNAME/subminds-may-2026:v1.0.0

# Run
docker run -it --rm ghcr.io/YOUR_USERNAME/subminds-may-2026:latest
```

---

## 📊 Monitoring Workflows

### View Workflow Status

1. Go to your repository on GitHub
2. Click "Actions" tab
3. See all workflow runs

### Check Release Status

```bash
# Via GitHub CLI
gh run list

# View specific run
gh run view <run-id>

# Watch live
gh run watch
```

---

## 🔄 Updating Releases

### Update Existing Release

```bash
# Delete tag locally
git tag -d v1.0.0

# Delete tag remotely
git push origin :refs/tags/v1.0.0

# Create new tag
git tag -a v1.0.0 -m "Updated release notes"

# Push new tag
git push origin v1.0.0
```

### Create Pre-release

```bash
# Create pre-release tag
git tag -a v1.1.0-beta.1 -m "Beta release for testing"
git push origin v1.1.0-beta.1

# Mark as pre-release in GitHub UI
```

---

## 📝 Commit Message Conventions

Use conventional commits for better changelogs:

```bash
# Features
git commit -m "feat: Add art analysis module"

# Bug fixes
git commit -m "fix: Resolve camera initialization issue"

# Documentation
git commit -m "docs: Update installation guide"

# Performance
git commit -m "perf: Optimize facial detection algorithm"

# Refactoring
git commit -m "refactor: Restructure AI engine module"

# Tests
git commit -m "test: Add unit tests for emotion tracker"

# Chores
git commit -m "chore: Update dependencies"
```

---

## 🎯 Complete Example: First Deployment

```bash
# 1. Navigate to project
cd subminds-may-2026

# 2. Initialize git
git init
git add .
git commit -m "feat: Initial commit - SubMinds v1.0.0"

# 3. Create GitHub repository
gh repo create subminds-may-2026 --public --source=. --remote=origin

# 4. Push to GitHub
git push -u origin main

# 5. Create first release
git tag -a v1.0.0 -m "Release v1.0.0: Initial release

Features:
- Facial expression analysis with MediaPipe and DeepFace
- IBM Granite AI integration for pattern recognition
- Real-time emotion tracking
- Docker support
- Comprehensive documentation"

git push origin v1.0.0

# 6. Check release
gh release view v1.0.0

# 7. View in browser
gh repo view --web
```

---

## 🔍 Troubleshooting

### Issue: Workflow fails on first run

**Solution:**
- Check GitHub Actions tab for error details
- Ensure all required files are committed
- Verify Python version compatibility

### Issue: Docker image not published

**Solution:**
- Check if GITHUB_TOKEN has package write permissions
- Go to Settings → Actions → General → Workflow permissions
- Select "Read and write permissions"

### Issue: Release not created

**Solution:**
- Verify tag format matches `v*.*.*`
- Check workflow logs in Actions tab
- Ensure you pushed the tag: `git push origin v1.0.0`

### Issue: PyPI publishing fails

**Solution:**
- Add PYPI_API_TOKEN secret
- Or remove PyPI publishing step from workflow

---

## 📚 Additional Resources

### GitHub Documentation
- [GitHub Actions](https://docs.github.com/en/actions)
- [Creating Releases](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)

### Project Documentation
- [README.md](../README.md) - Project overview
- [QUICKSTART.md](../QUICKSTART.md) - Quick start guide
- [INSTALLATION.md](INSTALLATION.md) - Installation instructions

---

## ✅ Checklist

Before pushing to GitHub:

- [ ] All sensitive data removed from code
- [ ] `.env` file in `.gitignore`
- [ ] README.md updated
- [ ] Version number updated in `setup.py`
- [ ] All tests passing locally
- [ ] Documentation complete
- [ ] License file added (if needed)

After pushing:

- [ ] Repository created on GitHub
- [ ] Code pushed successfully
- [ ] First release tag created
- [ ] GitHub Actions workflows running
- [ ] Release published
- [ ] Docker image available

---

## 🎉 Success!

Your SubMinds project is now on GitHub with automated CI/CD!

**Next steps:**
1. Share your repository
2. Add collaborators
3. Create issues for future features
4. Set up project board
5. Enable discussions

**Repository URL:**
```
https://github.com/YOUR_USERNAME/subminds-may-2026
```

**Releases:**
```
https://github.com/YOUR_USERNAME/subminds-may-2026/releases
```

**Docker Images:**
```
ghcr.io/YOUR_USERNAME/subminds-may-2026
```

---

*Happy coding! 🚀*