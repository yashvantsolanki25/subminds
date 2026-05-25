# SubMinds GitHub Deployment Script
# This script will push your code and create the first release

Write-Host "🚀 SubMinds GitHub Deployment Script" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "README.md")) {
    Write-Host "❌ Error: Please run this script from the subminds-may-2026 directory" -ForegroundColor Red
    exit 1
}

# Step 1: Accept GitHub SSH key
Write-Host "📝 Step 1: Accepting GitHub SSH key..." -ForegroundColor Yellow
$response = Read-Host "Do you trust GitHub's SSH key? Type 'yes' to continue"
if ($response -ne "yes") {
    Write-Host "❌ Deployment cancelled" -ForegroundColor Red
    exit 1
}

# Step 2: Push to GitHub
Write-Host ""
Write-Host "📤 Step 2: Pushing code to GitHub..." -ForegroundColor Yellow
git push -u origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to push to GitHub" -ForegroundColor Red
    Write-Host "Please manually run: git push -u origin main" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Code pushed successfully!" -ForegroundColor Green

# Step 3: Create release tag
Write-Host ""
Write-Host "🏷️  Step 3: Creating release tag v1.0.0..." -ForegroundColor Yellow

$tagMessage = @"
Release v1.0.0: Initial Release

🎯 Features:
- Facial expression analysis with MediaPipe and DeepFace
- IBM Granite AI integration for pattern recognition
- Real-time emotion tracking and stress detection
- TORCS racing simulator integration
- Docker containerization support
- Comprehensive documentation and guides
- GitHub Actions CI/CD workflows

📦 Components:
- Facial Analysis Module
- AI Engine with IBM Granite
- Emotion Tracker
- Configuration System
- Docker Setup
- Complete Documentation

🚀 Ready for production use!
"@

git tag -a v1.0.0 -m $tagMessage

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create tag" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Tag v1.0.0 created!" -ForegroundColor Green

# Step 4: Push tag
Write-Host ""
Write-Host "📤 Step 4: Pushing release tag..." -ForegroundColor Yellow
git push origin v1.0.0

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to push tag" -ForegroundColor Red
    Write-Host "Please manually run: git push origin v1.0.0" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Release tag pushed successfully!" -ForegroundColor Green

# Success message
Write-Host ""
Write-Host "🎉 Deployment Complete!" -ForegroundColor Green
Write-Host "======================" -ForegroundColor Green
Write-Host ""
Write-Host "✅ Code pushed to GitHub" -ForegroundColor Green
Write-Host "✅ Release v1.0.0 created" -ForegroundColor Green
Write-Host "✅ GitHub Actions workflows triggered" -ForegroundColor Green
Write-Host ""
Write-Host "🔗 View your repository:" -ForegroundColor Cyan
Write-Host "   https://github.com/yashvantsolanki25/subminds-may-2026" -ForegroundColor White
Write-Host ""
Write-Host "🔗 View releases:" -ForegroundColor Cyan
Write-Host "   https://github.com/yashvantsolanki25/subminds-may-2026/releases" -ForegroundColor White
Write-Host ""
Write-Host "🔗 View GitHub Actions:" -ForegroundColor Cyan
Write-Host "   https://github.com/yashvantsolanki25/subminds-may-2026/actions" -ForegroundColor White
Write-Host ""
Write-Host "📦 Docker images will be available at:" -ForegroundColor Cyan
Write-Host "   ghcr.io/yashvantsolanki25/subminds-may-2026:latest" -ForegroundColor White
Write-Host "   ghcr.io/yashvantsolanki25/subminds-may-2026:v1.0.0" -ForegroundColor White
Write-Host ""
Write-Host "⏳ GitHub Actions is now building and publishing your release..." -ForegroundColor Yellow
Write-Host "   This may take 5-10 minutes to complete." -ForegroundColor Yellow
Write-Host ""

# Made with Bob
