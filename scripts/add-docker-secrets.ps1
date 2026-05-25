# Add Docker Hub Secrets to GitHub Actions
# This script helps you add Docker Hub credentials to GitHub repository secrets

param(
    [Parameter(Mandatory=$false)]
    [string]$RepoOwner = "yashvant25",
    
    [Parameter(Mandatory=$false)]
    [string]$RepoName = "subminds",
    
    [Parameter(Mandatory=$false)]
    [string]$DockerUsername = "yashvant25",
    
    [Parameter(Mandatory=$false)]
    [string]$DockerToken = "dckr_pat_h6frDFxLLipfNZUZl2cXlhF0dKw"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GitHub Actions Secrets Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if GitHub CLI is installed
$ghInstalled = Get-Command gh -ErrorAction SilentlyContinue

if (-not $ghInstalled) {
    Write-Host "❌ GitHub CLI (gh) is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install GitHub CLI:" -ForegroundColor Yellow
    Write-Host "  Windows: winget install --id GitHub.cli" -ForegroundColor White
    Write-Host "  Or download from: https://cli.github.com/" -ForegroundColor White
    Write-Host ""
    Write-Host "After installation, run: gh auth login" -ForegroundColor Yellow
    Write-Host ""
    
    # Show manual instructions
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "MANUAL SETUP INSTRUCTIONS" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Go to: https://github.com/$RepoOwner/$RepoName/settings/secrets/actions" -ForegroundColor White
    Write-Host ""
    Write-Host "2. Click 'New repository secret'" -ForegroundColor White
    Write-Host ""
    Write-Host "3. Add these secrets:" -ForegroundColor White
    Write-Host ""
    Write-Host "   Name: DOCKER_USERNAME" -ForegroundColor Green
    Write-Host "   Value: $DockerUsername" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   Name: DOCKER_PASSWORD" -ForegroundColor Green
    Write-Host "   Value: $DockerToken" -ForegroundColor Yellow
    Write-Host ""
    
    exit 1
}

# Check if authenticated
Write-Host "Checking GitHub authentication..." -ForegroundColor Yellow
$authStatus = gh auth status 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Not authenticated with GitHub!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please run: gh auth login" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

Write-Host "✅ GitHub CLI authenticated" -ForegroundColor Green
Write-Host ""

# Add Docker secrets
Write-Host "Adding Docker Hub secrets to GitHub repository..." -ForegroundColor Yellow
Write-Host ""

try {
    # Add DOCKER_USERNAME
    Write-Host "Adding DOCKER_USERNAME..." -ForegroundColor Cyan
    $dockerUsernameEncoded = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($DockerUsername))
    gh secret set DOCKER_USERNAME --body $DockerUsername --repo "$RepoOwner/$RepoName"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ DOCKER_USERNAME added successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to add DOCKER_USERNAME" -ForegroundColor Red
    }
    
    # Add DOCKER_PASSWORD
    Write-Host "Adding DOCKER_PASSWORD..." -ForegroundColor Cyan
    gh secret set DOCKER_PASSWORD --body $DockerToken --repo "$RepoOwner/$RepoName"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ DOCKER_PASSWORD added successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to add DOCKER_PASSWORD" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "✅ Docker secrets added successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    # List all secrets
    Write-Host "Current repository secrets:" -ForegroundColor Yellow
    gh secret list --repo "$RepoOwner/$RepoName"
    Write-Host ""
    
} catch {
    Write-Host "❌ Error adding secrets: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please add secrets manually:" -ForegroundColor Yellow
    Write-Host "https://github.com/$RepoOwner/$RepoName/settings/secrets/actions" -ForegroundColor White
    Write-Host ""
    exit 1
}

# Show remaining secrets to add
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "REMAINING SECRETS TO ADD" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "You still need to add these secrets manually:" -ForegroundColor Yellow
Write-Host ""
Write-Host "AWS Credentials:" -ForegroundColor Cyan
Write-Host "  - AWS_ACCESS_KEY_ID" -ForegroundColor White
Write-Host "  - AWS_SECRET_ACCESS_KEY" -ForegroundColor White
Write-Host "  - AWS_REGION (e.g., us-east-1)" -ForegroundColor White
Write-Host ""
Write-Host "EC2 Instance:" -ForegroundColor Cyan
Write-Host "  - EC2_HOST (your EC2 public IP)" -ForegroundColor White
Write-Host "  - EC2_USER (ubuntu or ec2-user)" -ForegroundColor White
Write-Host "  - EC2_SSH_PRIVATE_KEY (your .pem file content)" -ForegroundColor White
Write-Host ""
Write-Host "Application:" -ForegroundColor Cyan
Write-Host "  - IBM_CLOUD_API_KEY" -ForegroundColor White
Write-Host "  - IBM_PROJECT_ID" -ForegroundColor White
Write-Host "  - POSTGRES_PASSWORD" -ForegroundColor White
Write-Host "  - MONGO_PASSWORD" -ForegroundColor White
Write-Host "  - REDIS_PASSWORD" -ForegroundColor White
Write-Host ""
Write-Host "Add them at: https://github.com/$RepoOwner/$RepoName/settings/secrets/actions" -ForegroundColor Green
Write-Host ""

# Generate secure passwords
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GENERATE SECURE PASSWORDS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Run these commands to generate secure passwords:" -ForegroundColor Yellow
Write-Host ""
Write-Host "PowerShell:" -ForegroundColor Cyan
Write-Host '  $bytes = New-Object Byte[] 32' -ForegroundColor White
Write-Host '  [Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)' -ForegroundColor White
Write-Host '  [Convert]::ToBase64String($bytes)' -ForegroundColor White
Write-Host ""
Write-Host "Or use online generator: https://passwordsgenerator.net/" -ForegroundColor White
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "NEXT STEPS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. ✅ Docker secrets added" -ForegroundColor Green
Write-Host "2. ⏳ Add remaining secrets manually" -ForegroundColor Yellow
Write-Host "3. ⏳ Setup EC2 instance" -ForegroundColor Yellow
Write-Host "4. ⏳ Push code to GitHub" -ForegroundColor Yellow
Write-Host "5. ⏳ Verify deployment" -ForegroundColor Yellow
Write-Host ""
Write-Host "See QUICK_DEPLOYMENT_SETUP.md for detailed instructions" -ForegroundColor Cyan
Write-Host ""

# Made with Bob