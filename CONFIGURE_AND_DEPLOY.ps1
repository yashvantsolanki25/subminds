# CONFIGURE_AND_DEPLOY.ps1
# Complete setup: Configure security group and deploy application

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SubMinds Complete Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$INSTANCE_ID = "i-0f6d969c603357328"
$EC2_HOST = "ec2-13-206-218-4.ap-south-1.compute.amazonaws.com"
$PEM_FILE = "C:\Users\Yashv\OneDrive\AWS Keys\test.pem"
$REGION = "ap-south-1"

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  Instance ID: $INSTANCE_ID" -ForegroundColor White
Write-Host "  EC2 Host: $EC2_HOST" -ForegroundColor White
Write-Host "  Region: $REGION" -ForegroundColor White
Write-Host ""

# Step 1: Get Security Group ID
Write-Host "Step 1: Getting Security Group..." -ForegroundColor Cyan
$SECURITY_GROUP_ID = aws ec2 describe-instances --region $REGION --instance-ids $INSTANCE_ID --query "Reservations[0].Instances[0].SecurityGroups[0].GroupId" --output text 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "X Failed to get security group" -ForegroundColor Red
    Write-Host "Error: $SECURITY_GROUP_ID" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please ensure AWS CLI is configured:" -ForegroundColor Yellow
    Write-Host "  aws configure" -ForegroundColor White
    exit 1
}

Write-Host "OK Security Group ID: $SECURITY_GROUP_ID" -ForegroundColor Green
Write-Host ""

# Step 2: Get Your IP
Write-Host "Step 2: Getting your IP address..." -ForegroundColor Cyan
try {
    $YOUR_IP = (Invoke-WebRequest -Uri "https://api.ipify.org" -UseBasicParsing).Content.Trim()
    Write-Host "OK Your IP: $YOUR_IP" -ForegroundColor Green
}
catch {
    Write-Host "Warning: Could not detect IP automatically" -ForegroundColor Yellow
    $YOUR_IP = Read-Host "Please enter your IP address"
}
Write-Host ""

# Step 3: Configure Security Group
Write-Host "Step 3: Configuring Security Group..." -ForegroundColor Cyan
Write-Host ""

function Add-SGRule {
    param([string]$Port, [string]$Cidr, [string]$Desc)
    Write-Host "  Adding: Port $Port from $Cidr" -NoNewline
    $result = aws ec2 authorize-security-group-ingress --region $REGION --group-id $SECURITY_GROUP_ID --protocol tcp --port $Port --cidr $Cidr --description "$Desc" 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host " OK" -ForegroundColor Green
    }
    elseif ($result -like "*already exists*") {
        Write-Host " (exists)" -ForegroundColor Yellow
    }
    else {
        Write-Host " X" -ForegroundColor Red
    }
}

Write-Host "Public Access:" -ForegroundColor Yellow
Add-SGRule -Port 22 -Cidr "0.0.0.0/0" -Desc "SSH"
Add-SGRule -Port 80 -Cidr "0.0.0.0/0" -Desc "HTTP"
Add-SGRule -Port 443 -Cidr "0.0.0.0/0" -Desc "HTTPS"
Add-SGRule -Port 8000 -Cidr "0.0.0.0/0" -Desc "SubMinds API"
Add-SGRule -Port 8050 -Cidr "0.0.0.0/0" -Desc "SubMinds Dashboard"

Write-Host ""
Write-Host "Restricted Access (Your IP):" -ForegroundColor Yellow
Add-SGRule -Port 5432 -Cidr "$YOUR_IP/32" -Desc "PostgreSQL"
Add-SGRule -Port 27017 -Cidr "$YOUR_IP/32" -Desc "MongoDB"
Add-SGRule -Port 6379 -Cidr "$YOUR_IP/32" -Desc "Redis"

Write-Host ""
Write-Host "OK Security Group Configured!" -ForegroundColor Green
Write-Host ""

# Step 4: Test SSH Connection
Write-Host "Step 4: Testing SSH Connection..." -ForegroundColor Cyan
$sshTest = ssh -i $PEM_FILE -o ConnectTimeout=10 -o StrictHostKeyChecking=no ubuntu@$EC2_HOST "echo 'OK'" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "X SSH connection failed" -ForegroundColor Red
    Write-Host "Error: $sshTest" -ForegroundColor Red
    exit 1
}
Write-Host "OK SSH connection successful" -ForegroundColor Green
Write-Host ""

# Step 5: Deploy Application
Write-Host "Step 5: Deploying Application..." -ForegroundColor Cyan
Write-Host ""
Write-Host "This will:" -ForegroundColor Yellow
Write-Host "  1. Clone/copy project to EC2" -ForegroundColor White
Write-Host "  2. Install Docker Compose if needed" -ForegroundColor White
Write-Host "  3. Copy .env file with credentials" -ForegroundColor White
Write-Host "  4. Build and start containers" -ForegroundColor White
Write-Host ""

$confirmation = Read-Host "Continue with deployment? (yes/no)"
if ($confirmation -ne "yes" -and $confirmation -ne "y") {
    Write-Host "Deployment cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
& ".\scripts\deploy-to-ec2.ps1" -PemFile $PEM_FILE -EC2Host $EC2_HOST -EC2User "ubuntu"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  Setup Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your SubMinds application is now running!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Access URLs:" -ForegroundColor Yellow
    Write-Host "  Main API:  http://$EC2_HOST:8000" -ForegroundColor Cyan
    Write-Host "  API Docs:  http://$EC2_HOST:8000/docs" -ForegroundColor Cyan
    Write-Host "  Dashboard: http://$EC2_HOST:8050" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Useful Commands:" -ForegroundColor Yellow
    Write-Host "  View logs:  ssh -i `"$PEM_FILE`" ubuntu@$EC2_HOST 'cd /home/ubuntu/subminds-may-2026 && sudo docker compose logs -f'" -ForegroundColor White
    Write-Host "  Restart:    ssh -i `"$PEM_FILE`" ubuntu@$EC2_HOST 'cd /home/ubuntu/subminds-may-2026 && sudo docker compose restart'" -ForegroundColor White
    Write-Host "  SSH:        ssh -i `"$PEM_FILE`" ubuntu@$EC2_HOST" -ForegroundColor White
    Write-Host ""
}
else {
    Write-Host ""
    Write-Host "X Deployment failed. Check errors above." -ForegroundColor Red
    Write-Host ""
}

# Made with Bob
