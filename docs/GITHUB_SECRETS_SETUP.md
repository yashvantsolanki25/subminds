# GitHub Secrets Setup Guide

This guide explains how to add your environment variables to GitHub Secrets for secure CI/CD deployment.

## 🔐 Why Use GitHub Secrets?

GitHub Secrets allow you to store sensitive information (API keys, passwords, tokens) securely in your repository. These secrets are:
- Encrypted and only exposed to GitHub Actions workflows
- Never visible in logs or to unauthorized users
- Essential for secure CI/CD pipelines

## 📋 Secrets to Add

Based on your `.env` file, you need to add the following secrets:

### IBM Cloud Credentials
- `IBM_CLOUD_API_KEY` - Your IBM Cloud API key for Granite AI access
- `IBM_PROJECT_ID` - Your IBM Watson Studio project ID

### Database Credentials
- `POSTGRES_HOST` - PostgreSQL host address
- `POSTGRES_USER` - PostgreSQL username
- `POSTGRES_PASSWORD` - PostgreSQL password
- `MONGO_HOST` - MongoDB host address
- `MONGO_USER` - MongoDB username
- `MONGO_PASSWORD` - MongoDB password
- `REDIS_HOST` - Redis host address
- `REDIS_PASSWORD` - Redis password

### Application Settings
- `DEBUG` - Debug mode flag (True/False)
- `LOG_LEVEL` - Logging level (INFO, DEBUG, WARNING, ERROR)

## 🚀 How to Add Secrets to GitHub

### Method 1: Using GitHub Web Interface (Recommended)

1. **Navigate to Your Repository**
   - Go to https://github.com/YOUR_USERNAME/YOUR_REPO_NAME

2. **Access Settings**
   - Click on **Settings** tab (top right of repository page)
   - You need admin access to the repository

3. **Navigate to Secrets**
   - In the left sidebar, click **Secrets and variables**
   - Click **Actions**

4. **Add New Secret**
   - Click **New repository secret** button
   - Enter the secret name (e.g., `IBM_CLOUD_API_KEY`)
   - Paste the secret value
   - Click **Add secret**

5. **Repeat for All Secrets**
   - Add each secret from the list above
   - Use EXACT names as shown (case-sensitive)

### Method 2: Using GitHub CLI

If you have GitHub CLI installed, you can add secrets via command line:

```bash
# Install GitHub CLI first (if not installed)
# Windows: winget install GitHub.cli
# Mac: brew install gh
# Linux: See https://github.com/cli/cli#installation

# Login to GitHub
gh auth login

# Add secrets one by one
gh secret set IBM_CLOUD_API_KEY -b "XRNJls6GZurytauCdeC1T0sTIRMyViF9KvSDvCM86MSC"
gh secret set IBM_PROJECT_ID -b "c01ebe61-c1ef-4f7d-9706-2da1b4c01fcf"
gh secret set POSTGRES_HOST -b "localhost"
gh secret set POSTGRES_USER -b "subminds"
gh secret set POSTGRES_PASSWORD -b "abcd@1234"
gh secret set MONGO_HOST -b "localhost"
gh secret set MONGO_USER -b "subminds"
gh secret set MONGO_PASSWORD -b "abcd@1234"
gh secret set REDIS_HOST -b "localhost"
gh secret set REDIS_PASSWORD -b "abcd@1234"
gh secret set DEBUG -b "True"
gh secret set LOG_LEVEL -b "INFO"
```

### Method 3: Bulk Import Using PowerShell Script

Create a PowerShell script to add all secrets at once:

```powershell
# add-github-secrets.ps1

# Ensure GitHub CLI is installed and authenticated
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Error "GitHub CLI is not installed. Install it first: winget install GitHub.cli"
    exit 1
}

# Check if authenticated
$authStatus = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Not authenticated. Running gh auth login..."
    gh auth login
}

# Define secrets
$secrets = @{
    "IBM_CLOUD_API_KEY" = "XRNJls6GZurytauCdeC1T0sTIRMyViF9KvSDvCM86MSC"
    "IBM_PROJECT_ID" = "c01ebe61-c1ef-4f7d-9706-2da1b4c01fcf"
    "POSTGRES_HOST" = "localhost"
    "POSTGRES_USER" = "subminds"
    "POSTGRES_PASSWORD" = "abcd@1234"
    "MONGO_HOST" = "localhost"
    "MONGO_USER" = "subminds"
    "MONGO_PASSWORD" = "abcd@1234"
    "REDIS_HOST" = "localhost"
    "REDIS_PASSWORD" = "abcd@1234"
    "DEBUG" = "True"
    "LOG_LEVEL" = "INFO"
}

# Add each secret
Write-Host "Adding secrets to GitHub repository..."
foreach ($key in $secrets.Keys) {
    Write-Host "Adding secret: $key"
    $value = $secrets[$key]
    gh secret set $key -b "$value"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Successfully added $key" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to add $key" -ForegroundColor Red
    }
}

Write-Host "`nAll secrets have been processed!" -ForegroundColor Cyan
```

Save this as `scripts/add-github-secrets.ps1` and run:
```powershell
cd c:/Users/Yashv/Downloads/subminds-may-2026
.\scripts\add-github-secrets.ps1
```

## 🔍 Verify Secrets Were Added

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. You should see all your secrets listed (values are hidden)

## 📝 Using Secrets in GitHub Actions

Once secrets are added, use them in your workflow files:

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run tests
        env:
          IBM_CLOUD_API_KEY: ${{ secrets.IBM_CLOUD_API_KEY }}
          IBM_PROJECT_ID: ${{ secrets.IBM_PROJECT_ID }}
          POSTGRES_HOST: ${{ secrets.POSTGRES_HOST }}
          POSTGRES_USER: ${{ secrets.POSTGRES_USER }}
          POSTGRES_PASSWORD: ${{ secrets.POSTGRES_PASSWORD }}
          MONGO_HOST: ${{ secrets.MONGO_HOST }}
          MONGO_USER: ${{ secrets.MONGO_USER }}
          MONGO_PASSWORD: ${{ secrets.MONGO_PASSWORD }}
          REDIS_HOST: ${{ secrets.REDIS_HOST }}
          REDIS_PASSWORD: ${{ secrets.REDIS_PASSWORD }}
          DEBUG: ${{ secrets.DEBUG }}
          LOG_LEVEL: ${{ secrets.LOG_LEVEL }}
        run: |
          python -m pytest tests/
      
      - name: Deploy
        env:
          IBM_CLOUD_API_KEY: ${{ secrets.IBM_CLOUD_API_KEY }}
        run: |
          # Your deployment commands here
          echo "Deploying to production..."
```

## ⚠️ Important Security Notes

1. **Never commit `.env` files** - They're already in `.gitignore`
2. **Rotate credentials regularly** - Update secrets periodically
3. **Use different credentials for production** - Don't use localhost values in production
4. **Limit secret access** - Only give access to necessary workflows
5. **Audit secret usage** - Review which workflows use which secrets

## 🔄 Updating Secrets

To update a secret:
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click on the secret name
3. Click **Update secret**
4. Enter new value and save

Or use GitHub CLI:
```bash
gh secret set SECRET_NAME -b "new_value"
```

## 🗑️ Deleting Secrets

To delete a secret:
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click on the secret name
3. Click **Remove secret**

Or use GitHub CLI:
```bash
gh secret remove SECRET_NAME
```

## 📚 Additional Resources

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [Best Practices for Secrets Management](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)

## 🆘 Troubleshooting

### "gh: command not found"
Install GitHub CLI:
```powershell
winget install GitHub.cli
```

### "Authentication required"
Login to GitHub:
```bash
gh auth login
```

### "Permission denied"
Ensure you have admin access to the repository.

### Secrets not working in workflows
- Check secret names match exactly (case-sensitive)
- Verify workflow has access to secrets
- Check if repository is private (secrets work differently in public repos)

---

**Next Steps:**
1. Choose your preferred method (Web UI, CLI, or PowerShell script)
2. Add all secrets to your GitHub repository
3. Verify secrets are added correctly
4. Update your GitHub Actions workflows to use these secrets
5. Test your CI/CD pipeline
