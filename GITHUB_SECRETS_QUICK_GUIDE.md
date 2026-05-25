# GitHub Secrets - Quick Reference Guide

## 🚀 Quick Setup (3 Methods)

### Method 1: Automated PowerShell Script (Easiest)

```powershell
# Run this command in PowerShell
.\scripts\add-github-secrets.ps1
```

This will automatically add all secrets from your `.env` file to GitHub.

### Method 2: GitHub CLI (Command Line)

```bash
# Install GitHub CLI (if not installed)
winget install GitHub.cli

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

### Method 3: GitHub Web Interface (Manual)

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret:
   - Name: `IBM_CLOUD_API_KEY`
   - Value: `XRNJls6GZurytauCdeC1T0sTIRMyViF9KvSDvCM86MSC`
5. Repeat for all 11 secrets

## 📋 Secrets List

| Secret Name | Description | Example Value |
|------------|-------------|---------------|
| `IBM_CLOUD_API_KEY` | IBM Cloud API Key | `XRNJls6GZurytauCdeC1T0sTIRMyViF9KvSDvCM86MSC` |
| `IBM_PROJECT_ID` | IBM Watson Studio Project ID | `c01ebe61-c1ef-4f7d-9706-2da1b4c01fcf` |
| `POSTGRES_HOST` | PostgreSQL Host | `localhost` |
| `POSTGRES_USER` | PostgreSQL Username | `subminds` |
| `POSTGRES_PASSWORD` | PostgreSQL Password | `abcd@1234` |
| `MONGO_HOST` | MongoDB Host | `localhost` |
| `MONGO_USER` | MongoDB Username | `subminds` |
| `MONGO_PASSWORD` | MongoDB Password | `abcd@1234` |
| `REDIS_HOST` | Redis Host | `localhost` |
| `REDIS_PASSWORD` | Redis Password | `abcd@1234` |
| `DEBUG` | Debug Mode | `True` |
| `LOG_LEVEL` | Logging Level | `INFO` |

## ✅ Verify Secrets

After adding secrets, verify them:

```bash
# List all secrets (names only, values are hidden)
gh secret list
```

Or check on GitHub:
- Go to **Settings** → **Secrets and variables** → **Actions**
- You should see all 11 secrets listed

## 🔧 Using Secrets in GitHub Actions

Your secrets are automatically available in the CI/CD workflow (`.github/workflows/ci-cd.yml`):

```yaml
env:
  IBM_CLOUD_API_KEY: ${{ secrets.IBM_CLOUD_API_KEY }}
  IBM_PROJECT_ID: ${{ secrets.IBM_PROJECT_ID }}
  # ... other secrets
```

## 📝 Important Notes

1. **Security**: Never commit `.env` file (already in `.gitignore`)
2. **Production**: Use different credentials for production environments
3. **Updates**: To update a secret, run the script again or use `gh secret set`
4. **Access**: Only repository admins can view/edit secrets

## 🆘 Troubleshooting

### GitHub CLI not found
```powershell
winget install GitHub.cli
```

### Not authenticated
```bash
gh auth login
```

### Permission denied
- Ensure you have admin access to the repository
- Check if you're logged into the correct GitHub account

## 📚 Full Documentation

For detailed instructions, see:
- **Complete Guide**: `docs/GITHUB_SECRETS_SETUP.md`
- **GitHub Actions Workflow**: `.github/workflows/ci-cd.yml`

## 🎯 Next Steps

1. ✅ Add secrets to GitHub (use Method 1 for easiest setup)
2. ✅ Verify secrets are added correctly
3. ✅ Push your code to GitHub
4. ✅ GitHub Actions will automatically run using these secrets
5. ✅ Monitor your CI/CD pipeline in the Actions tab

---

**Ready to add secrets?** Run: `.\scripts\add-github-secrets.ps1`