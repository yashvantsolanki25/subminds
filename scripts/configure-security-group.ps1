# configure-security-group.ps1
# Automatically configure AWS Security Group for SubMinds

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AWS Security Group Configuration" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if AWS CLI is installed
Write-Host "Checking for AWS CLI..." -ForegroundColor Yellow
if (-not (Get-Command aws -ErrorAction SilentlyContinue)) {
    Write-Host "✗ AWS CLI is not installed." -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install AWS CLI first:" -ForegroundColor Yellow
    Write-Host "  Download from: https://aws.amazon.com/cli/" -ForegroundColor White
    Write-Host "  Or run: msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi" -ForegroundColor White
    exit 1
}
Write-Host "✓ AWS CLI is installed" -ForegroundColor Green

# Check AWS credentials
Write-Host "Checking AWS credentials..." -ForegroundColor Yellow
$awsCheck = aws sts get-caller-identity 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ AWS credentials not configured" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please configure AWS CLI first:" -ForegroundColor Yellow
    Write-Host "  aws configure" -ForegroundColor White
    exit 1
}
Write-Host "✓ AWS credentials configured" -ForegroundColor Green
Write-Host ""

# Get EC2 instance details
$EC2_HOST = "ec2-13-206-218-4.ap-south-1.compute.amazonaws.com"
Write-Host "Getting security group for: $EC2_HOST" -ForegroundColor Yellow

$instanceInfo = aws ec2 describe-instances `
    --region ap-south-1 `
    --filters "Name=dns-name,Values=$EC2_HOST" `
    --query "Reservations[0].Instances[0].[InstanceId,SecurityGroups[0].GroupId]" `
    --output text 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to get instance information" -ForegroundColor Red
    Write-Host "Error: $instanceInfo" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please ensure:" -ForegroundColor Yellow
    Write-Host "  1. AWS CLI is configured with correct region (ap-south-1)" -ForegroundColor White
    Write-Host "  2. You have permissions to describe EC2 instances" -ForegroundColor White
    Write-Host "  3. The EC2 instance exists and is running" -ForegroundColor White
    exit 1
}

$INSTANCE_ID, $SECURITY_GROUP_ID = $instanceInfo -split '\s+'
Write-Host "✓ Instance ID: $INSTANCE_ID" -ForegroundColor Green
Write-Host "✓ Security Group ID: $SECURITY_GROUP_ID" -ForegroundColor Green
Write-Host ""

# Get your current IP
Write-Host "Getting your current IP address..." -ForegroundColor Yellow
try {
    $YOUR_IP = (Invoke-WebRequest -Uri "https://api.ipify.org" -UseBasicParsing).Content.Trim()
    Write-Host "✓ Your IP: $YOUR_IP" -ForegroundColor Green
} catch {
    Write-Host "⚠ Could not detect your IP automatically" -ForegroundColor Yellow
    $YOUR_IP = Read-Host "Please enter your IP address"
}
Write-Host ""

# Confirm before proceeding
Write-Host "This script will configure the following ports:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Public Access (0.0.0.0/0):" -ForegroundColor Cyan
Write-Host "  - Port 22 (SSH)" -ForegroundColor White
Write-Host "  - Port 80 (HTTP)" -ForegroundColor White
Write-Host "  - Port 443 (HTTPS)" -ForegroundColor White
Write-Host "  - Port 8000 (Application API)" -ForegroundColor White
Write-Host "  - Port 8050 (Dashboard)" -ForegroundColor White
Write-Host ""
Write-Host "Restricted Access (Your IP: $YOUR_IP/32):" -ForegroundColor Cyan
Write-Host "  - Port 5432 (PostgreSQL)" -ForegroundColor White
Write-Host "  - Port 27017 (MongoDB)" -ForegroundColor White
Write-Host "  - Port 6379 (Redis)" -ForegroundColor White
Write-Host ""
$confirmation = Read-Host "Do you want to continue? (yes/no)"

if ($confirmation -ne "yes" -and $confirmation -ne "y") {
    Write-Host "Operation cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Configuring security group rules..." -ForegroundColor Cyan
Write-Host ""

# Function to add security group rule
function Add-SecurityGroupRule {
    param(
        [string]$Port,
        [string]$Cidr,
        [string]$Description
    )
    
    Write-Host "Adding rule: Port $Port from $Cidr - $Description" -NoNewline
    
    $result = aws ec2 authorize-security-group-ingress `
        --region ap-south-1 `
        --group-id $SECURITY_GROUP_ID `
        --protocol tcp `
        --port $Port `
        --cidr $Cidr `
        --description "$Description" 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✓" -ForegroundColor Green
        return $true
    } elseif ($result -like "*already exists*") {
        Write-Host " (already exists)" -ForegroundColor Yellow
        return $true
    } else {
        Write-Host " ✗" -ForegroundColor Red
        Write-Host "  Error: $result" -ForegroundColor Red
        return $false
    }
}

# Add public access rules
Write-Host "Public Access Rules:" -ForegroundColor Cyan
Add-SecurityGroupRule -Port 22 -Cidr "0.0.0.0/0" -Description "SSH access"
Add-SecurityGroupRule -Port 80 -Cidr "0.0.0.0/0" -Description "HTTP web access"
Add-SecurityGroupRule -Port 443 -Cidr "0.0.0.0/0" -Description "HTTPS web access"
Add-SecurityGroupRule -Port 8000 -Cidr "0.0.0.0/0" -Description "SubMinds Application API"
Add-SecurityGroupRule -Port 8050 -Cidr "0.0.0.0/0" -Description "SubMinds Dashboard"

Write-Host ""
Write-Host "Restricted Access Rules (Your IP only):" -ForegroundColor Cyan
Add-SecurityGroupRule -Port 5432 -Cidr "$YOUR_IP/32" -Description "PostgreSQL database"
Add-SecurityGroupRule -Port 27017 -Cidr "$YOUR_IP/32" -Description "MongoDB database"
Add-SecurityGroupRule -Port 6379 -Cidr "$YOUR_IP/32" -Description "Redis cache"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Security Group Configured!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your EC2 instance is now configured with the following access:" -ForegroundColor Yellow
Write-Host ""
Write-Host "✓ Public access to application (ports 8000, 8050)" -ForegroundColor Green
Write-Host "✓ SSH access (port 22)" -ForegroundColor Green
Write-Host "✓ Database access restricted to your IP ($YOUR_IP)" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Run deployment: .\DEPLOY_NOW.ps1" -ForegroundColor White
Write-Host "2. Access application: http://$EC2_HOST:8000" -ForegroundColor White
Write-Host ""
Write-Host "Security Note:" -ForegroundColor Yellow
Write-Host "If your IP changes, run this script again to update database access." -ForegroundColor White
Write-Host ""

# Made with Bob
