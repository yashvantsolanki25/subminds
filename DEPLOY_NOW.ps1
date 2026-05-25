# DEPLOY_NOW.ps1
# Quick deployment script - Just run this!

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SubMinds Quick Deploy to EC2" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$PEM_FILE = "C:\Users\Yashv\OneDrive\AWS Keys\test.pem"
$EC2_HOST = "ec2-13-206-218-4.ap-south-1.compute.amazonaws.com"

# Check if PEM file exists
if (-not (Test-Path $PEM_FILE)) {
    Write-Host "✗ PEM file not found at: $PEM_FILE" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please update the PEM_FILE path in this script or place test.pem in:" -ForegroundColor Yellow
    Write-Host "  C:\Users\Yashv\OneDrive\AWS Keys\" -ForegroundColor White
    exit 1
}

Write-Host "✓ PEM file found" -ForegroundColor Green
Write-Host "✓ Target: $EC2_HOST" -ForegroundColor Green
Write-Host ""

# Run deployment
Write-Host "Starting deployment..." -ForegroundColor Yellow
Write-Host ""

& ".\scripts\deploy-to-ec2.ps1" -PemFile $PEM_FILE -EC2Host $EC2_HOST -EC2User "ubuntu"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  🎉 Deployment Successful!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Access your application at:" -ForegroundColor Yellow
    Write-Host "  http://$EC2_HOST:8000" -ForegroundColor Cyan
    Write-Host "  http://$EC2_HOST:8000/docs" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  ✗ Deployment Failed" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Check the error messages above." -ForegroundColor Yellow
    Write-Host "See AWS_EC2_DEPLOYMENT_GUIDE.md for troubleshooting." -ForegroundColor Yellow
    Write-Host ""
}

# Made with Bob
