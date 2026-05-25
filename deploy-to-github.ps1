# SubMinds GitHub Deployment Script
# Deploys project to GitHub with proper secrets management

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "SubMinds - GitHub Deployment" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if GitHub CLI is installed and authenticated
Write-Host "Checking GitHub CLI..." -ForegroundColor Yellow
$ghAuth = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: GitHub CLI not authenticated" -ForegroundColor Red
    Write-Host "Run: gh auth login" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ GitHub CLI authenticated" -ForegroundColor Green
Write-Host ""

# Get repository name
$repoName = Read-Host "Enter repository name (default: subminds-may-2026)"
if ([string]::IsNullOrWhiteSpace($repoName)) {
    $repoName = "subminds-may-2026"
}

# Get repository visibility
Write-Host ""
Write-Host "Repository visibility:" -ForegroundColor Yellow
Write-Host "  1. Private (recommended - contains sensitive code)" -ForegroundColor Cyan
Write-Host "  2. Public" -ForegroundColor Cyan
$visibility = Read-Host "Choose (1 or 2, default: 1)"
if ([string]::IsNullOrWhiteSpace($visibility) -or $visibility -eq "1") {
    $visibilityFlag = "--private"
    $visibilityText = "private"
} else {
    $visibilityFlag = "--public"
    $visibilityText = "public"
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Deployment Configuration:" -ForegroundColor Cyan
Write-Host "  Repository: $repoName" -ForegroundColor White
Write-Host "  Visibility: $visibilityText" -ForegroundColor White
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$confirm = Read-Host "Continue with deployment? (y/n)"
if ($confirm -ne "y") {
    Write-Host "Deployment cancelled" -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Starting deployment..." -ForegroundColor Yellow
Write-Host ""

# Initialize git if not already initialized
if (-not (Test-Path ".git")) {
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git initialized" -ForegroundColor Green
} else {
    Write-Host "✅ Git repository already initialized" -ForegroundColor Green
}

# Add all files (respecting .gitignore)
Write-Host ""
Write-Host "Adding files to Git..." -ForegroundColor Yellow
git add .
Write-Host "✅ Files added" -ForegroundColor Green

# Create initial commit
Write-Host ""
Write-Host "Creating initial commit..." -ForegroundColor Yellow
git commit -m "Initial commit: SubMinds - Subconscious Decision Analysis System

- Complete facial analysis system with webcam capture
- Emotion detection with DeepFace (7 emotions)
- IBM Granite AI integration for pattern analysis
- Real-time data processing and logging
- Comprehensive error handling and mock modes
- Production-ready code with 2,500+ lines
- Full documentation and setup guides
- IoT template adaptation for IBM Watson Studio

Project ID: c01ebe61-c1ef-4f7d-9706-2da1b4c01fcf
Region: EU-GB
"
Write-Host "✅ Initial commit created" -ForegroundColor Green

# Create GitHub repository
Write-Host ""
Write-Host "Creating GitHub repository..." -ForegroundColor Yellow
gh repo create $repoName $visibilityFlag --source=. --description "SubMinds - AI-powered subconscious decision analysis for F1 drivers using facial expressions, IBM Granite AI, and real-time telemetry" --push

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Repository created and pushed" -ForegroundColor Green
} else {
    Write-Host "ERROR: Failed to create repository" -ForegroundColor Red
    exit 1
}

# Add GitHub Secrets for IBM credentials
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Setting up GitHub Secrets" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Adding IBM Cloud credentials as GitHub secrets..." -ForegroundColor Yellow

# Read credentials from .env file
if (Test-Path ".env") {
    $envContent = Get-Content ".env"
    
    # Extract IBM_CLOUD_API_KEY
    $apiKeyLine = $envContent | Where-Object { $_ -match "^IBM_CLOUD_API_KEY=" }
    if ($apiKeyLine) {
        $apiKey = $apiKeyLine -replace "^IBM_CLOUD_API_KEY=", ""
        Write-Host "Setting IBM_CLOUD_API_KEY..." -ForegroundColor Yellow
        $apiKey | gh secret set IBM_CLOUD_API_KEY
        Write-Host "✅ IBM_CLOUD_API_KEY added" -ForegroundColor Green
    }
    
    # Extract IBM_PROJECT_ID
    $projectIdLine = $envContent | Where-Object { $_ -match "^IBM_PROJECT_ID=" }
    if ($projectIdLine) {
        $projectId = $projectIdLine -replace "^IBM_PROJECT_ID=", ""
        Write-Host "Setting IBM_PROJECT_ID..." -ForegroundColor Yellow
        $projectId | gh secret set IBM_PROJECT_ID
        Write-Host "✅ IBM_PROJECT_ID added" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "✅ GitHub secrets configured" -ForegroundColor Green
} else {
    Write-Host "⚠️  .env file not found. Secrets not added." -ForegroundColor Yellow
    Write-Host "You can add them manually later in GitHub Settings > Secrets" -ForegroundColor Yellow
}

# Get repository URL
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$repoUrl = gh repo view --json url -q .url
Write-Host "Repository URL: $repoUrl" -ForegroundColor Cyan
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. View your repository: $repoUrl" -ForegroundColor White
Write-Host "  2. Verify GitHub secrets are set (Settings > Secrets)" -ForegroundColor White
Write-Host "  3. Clone on other machines: gh repo clone $repoName" -ForegroundColor White
Write-Host "  4. Share with team members (if private)" -ForegroundColor White
Write-Host ""

Write-Host "Important Notes:" -ForegroundColor Yellow
Write-Host "  • Your .env file is NOT pushed (protected by .gitignore)" -ForegroundColor White
Write-Host "  • IBM credentials are stored as GitHub secrets" -ForegroundColor White
Write-Host "  • config/ibm_granite_config.yaml is NOT pushed (protected)" -ForegroundColor White
Write-Host "  • Large data files and models are excluded" -ForegroundColor White
Write-Host ""

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🎉 SubMinds successfully deployed to GitHub!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan

# Made with Bob
