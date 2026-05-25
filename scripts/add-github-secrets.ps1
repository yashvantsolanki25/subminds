# add-github-secrets.ps1
# Script to add all environment variables as GitHub Secrets

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  GitHub Secrets Setup for SubMinds" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if GitHub CLI is installed
Write-Host "Checking for GitHub CLI..." -ForegroundColor Yellow
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "✗ GitHub CLI is not installed." -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install GitHub CLI first:" -ForegroundColor Yellow
    Write-Host "  winget install GitHub.cli" -ForegroundColor White
    Write-Host ""
    Write-Host "Or download from: https://cli.github.com/" -ForegroundColor White
    exit 1
}
Write-Host "✓ GitHub CLI is installed" -ForegroundColor Green
Write-Host ""

# Check if authenticated
Write-Host "Checking GitHub authentication..." -ForegroundColor Yellow
$authStatus = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Not authenticated with GitHub" -ForegroundColor Red
    Write-Host ""
    Write-Host "Running authentication process..." -ForegroundColor Yellow
    gh auth login
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Authentication failed" -ForegroundColor Red
        exit 1
    }
}
Write-Host "✓ Authenticated with GitHub" -ForegroundColor Green
Write-Host ""

# Define secrets from .env file
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

# Confirm before proceeding
Write-Host "This script will add the following secrets to your GitHub repository:" -ForegroundColor Yellow
Write-Host ""
foreach ($key in $secrets.Keys) {
    Write-Host "  - $key" -ForegroundColor White
}
Write-Host ""
Write-Host "WARNING: This will overwrite any existing secrets with the same names!" -ForegroundColor Red
Write-Host ""
$confirmation = Read-Host "Do you want to continue? (yes/no)"

if ($confirmation -ne "yes" -and $confirmation -ne "y") {
    Write-Host "Operation cancelled by user." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Adding secrets to GitHub repository..." -ForegroundColor Cyan
Write-Host ""

$successCount = 0
$failCount = 0

foreach ($key in $secrets.Keys) {
    Write-Host "Adding secret: $key" -NoNewline
    $value = $secrets[$key]
    
    # Add secret using GitHub CLI
    $output = gh secret set $key -b "$value" 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✓" -ForegroundColor Green
        $successCount++
    } else {
        Write-Host " ✗" -ForegroundColor Red
        Write-Host "  Error: $output" -ForegroundColor Red
        $failCount++
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Successfully added: $successCount secrets" -ForegroundColor Green
Write-Host "Failed: $failCount secrets" -ForegroundColor $(if ($failCount -gt 0) { "Red" } else { "Green" })
Write-Host ""

if ($successCount -eq $secrets.Count) {
    Write-Host "✓ All secrets have been successfully added to GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Verify secrets in GitHub: Settings → Secrets and variables → Actions" -ForegroundColor White
    Write-Host "2. Update your GitHub Actions workflows to use these secrets" -ForegroundColor White
    Write-Host "3. Test your CI/CD pipeline" -ForegroundColor White
} else {
    Write-Host "⚠ Some secrets failed to add. Please check the errors above." -ForegroundColor Yellow
    Write-Host "You may need to add them manually via GitHub web interface." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "For more information, see: docs/GITHUB_SECRETS_SETUP.md" -ForegroundColor Cyan
Write-Host ""

# Made with Bob
