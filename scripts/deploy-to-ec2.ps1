# deploy-to-ec2.ps1
# Automated deployment script for SubMinds to AWS EC2

param(
    [string]$PemFile = "test.pem",
    [string]$EC2Host = "ec2-13-206-218-4.ap-south-1.compute.amazonaws.com",
    [string]$EC2User = "ubuntu"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SubMinds EC2 Deployment Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$SSH_CONNECTION = "${EC2User}@${EC2Host}"
$PROJECT_NAME = "subminds-may-2026"
$REMOTE_DIR = "/home/ubuntu/${PROJECT_NAME}"

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  PEM File: $PemFile" -ForegroundColor White
Write-Host "  EC2 Host: $EC2Host" -ForegroundColor White
Write-Host "  SSH User: $EC2User" -ForegroundColor White
Write-Host "  Remote Directory: $REMOTE_DIR" -ForegroundColor White
Write-Host ""

# Check if PEM file exists
if (-not (Test-Path $PemFile)) {
    Write-Host "✗ PEM file not found: $PemFile" -ForegroundColor Red
    Write-Host "Please ensure the PEM file is in the current directory or provide the correct path." -ForegroundColor Yellow
    exit 1
}
Write-Host "✓ PEM file found" -ForegroundColor Green

# Test SSH connection
Write-Host ""
Write-Host "Testing SSH connection..." -ForegroundColor Yellow
$testConnection = ssh -i $PemFile -o ConnectTimeout=10 -o StrictHostKeyChecking=no $SSH_CONNECTION "echo 'Connection successful'" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to connect to EC2 instance" -ForegroundColor Red
    Write-Host "Error: $testConnection" -ForegroundColor Red
    exit 1
}
Write-Host "✓ SSH connection successful" -ForegroundColor Green

# Create remote directory
Write-Host ""
Write-Host "Creating remote directory..." -ForegroundColor Yellow
ssh -i $PemFile $SSH_CONNECTION "mkdir -p $REMOTE_DIR"
Write-Host "✓ Remote directory ready" -ForegroundColor Green

# Copy project files
Write-Host ""
Write-Host "Copying project files to EC2..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor White

# Create list of files to copy (exclude unnecessary files)
$excludePatterns = @(
    "--exclude=.git",
    "--exclude=__pycache__",
    "--exclude=*.pyc",
    "--exclude=.venv",
    "--exclude=venv",
    "--exclude=node_modules",
    "--exclude=.env",
    "--exclude=*.log",
    "--exclude=data/raw/*",
    "--exclude=data/processed/*",
    "--exclude=data/models/*.h5",
    "--exclude=data/models/*.pkl",
    "--exclude=*.pem"
)

# Use rsync for efficient file transfer
$rsyncCommand = "rsync -avz -e `"ssh -i $PemFile`" $($excludePatterns -join ' ') ./ ${SSH_CONNECTION}:${REMOTE_DIR}/"
Invoke-Expression $rsyncCommand

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to copy files" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Files copied successfully" -ForegroundColor Green

# Copy .env file separately (with secure permissions)
Write-Host ""
Write-Host "Copying environment variables..." -ForegroundColor Yellow
scp -i $PemFile .env "${SSH_CONNECTION}:${REMOTE_DIR}/.env"
ssh -i $PemFile $SSH_CONNECTION "chmod 600 ${REMOTE_DIR}/.env"
Write-Host "✓ Environment variables copied" -ForegroundColor Green

# Install Docker and Docker Compose if needed
Write-Host ""
Write-Host "Checking Docker installation..." -ForegroundColor Yellow
$dockerCheck = ssh -i $PemFile $SSH_CONNECTION "docker --version 2>&1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker not found. Installing..." -ForegroundColor Yellow
    ssh -i $PemFile $SSH_CONNECTION @"
        sudo apt-get update
        sudo apt-get install -y docker.io
        sudo systemctl start docker
        sudo systemctl enable docker
        sudo usermod -aG docker ubuntu
"@
    Write-Host "✓ Docker installed" -ForegroundColor Green
} else {
    Write-Host "✓ Docker already installed" -ForegroundColor Green
}

# Check and install Docker Compose plugin
Write-Host "Checking Docker Compose..." -ForegroundColor Yellow
$composeCheck = ssh -i $PemFile $SSH_CONNECTION "docker compose version 2>&1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker Compose not found. Installing..." -ForegroundColor Yellow
    ssh -i $PemFile $SSH_CONNECTION @"
        sudo apt-get update
        sudo apt-get install -y docker-compose-plugin
"@
    Write-Host "✓ Docker Compose installed" -ForegroundColor Green
} else {
    Write-Host "✓ Docker Compose already installed" -ForegroundColor Green
}

# Build and start containers
Write-Host ""
Write-Host "Building and starting Docker containers..." -ForegroundColor Yellow
ssh -i $PemFile $SSH_CONNECTION @"
    cd $REMOTE_DIR
    sudo docker compose down 2>/dev/null || true
    sudo docker compose build
    sudo docker compose up -d
"@

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to start containers" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Containers started successfully" -ForegroundColor Green

# Check container status
Write-Host ""
Write-Host "Checking container status..." -ForegroundColor Yellow
ssh -i $PemFile $SSH_CONNECTION "cd $REMOTE_DIR && sudo docker compose ps"

# Show logs
Write-Host ""
Write-Host "Recent logs:" -ForegroundColor Yellow
ssh -i $PemFile $SSH_CONNECTION "cd $REMOTE_DIR && sudo docker compose logs --tail=20"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Deployment Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your application is now running on EC2!" -ForegroundColor Green
Write-Host ""
Write-Host "Access your application:" -ForegroundColor Yellow
Write-Host "  http://${EC2Host}:8000" -ForegroundColor White
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Yellow
Write-Host "  View logs:    ssh -i $PemFile $SSH_CONNECTION 'cd $REMOTE_DIR && sudo docker compose logs -f'" -ForegroundColor White
Write-Host "  Restart:      ssh -i $PemFile $SSH_CONNECTION 'cd $REMOTE_DIR && sudo docker compose restart'" -ForegroundColor White
Write-Host "  Stop:         ssh -i $PemFile $SSH_CONNECTION 'cd $REMOTE_DIR && sudo docker compose down'" -ForegroundColor White
Write-Host "  SSH access:   ssh -i $PemFile $SSH_CONNECTION" -ForegroundColor White
Write-Host ""
Write-Host "Security Group Configuration:" -ForegroundColor Yellow
Write-Host "  See: docs/AWS_SECURITY_GROUP_CONFIG.md" -ForegroundColor White
Write-Host ""

# Made with Bob
