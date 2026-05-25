# deploy-to-ec2-fixed.ps1
# Fixed deployment script for Windows to EC2

param(
    [string]$PemFile = "C:\Users\Yashv\OneDrive\AWS Keys\test.pem",
    [string]$EC2Host = "ec2-13-206-218-4.ap-south-1.compute.amazonaws.com",
    [string]$EC2User = "ubuntu"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SubMinds EC2 Deployment (Fixed)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$SSH_CONNECTION = "${EC2User}@${EC2Host}"
$PROJECT_NAME = "subminds-may-2026"
$REMOTE_DIR = "/home/ubuntu/${PROJECT_NAME}"

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  PEM File: $PemFile" -ForegroundColor White
Write-Host "  EC2 Host: $EC2Host" -ForegroundColor White
Write-Host "  Remote Directory: $REMOTE_DIR" -ForegroundColor White
Write-Host ""

# Test SSH connection
Write-Host "Testing SSH connection..." -ForegroundColor Yellow
$testConnection = ssh -i $PemFile -o ConnectTimeout=10 -o StrictHostKeyChecking=no $SSH_CONNECTION "echo 'OK'" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "X Failed to connect to EC2" -ForegroundColor Red
    exit 1
}
Write-Host "OK SSH connection successful" -ForegroundColor Green
Write-Host ""

# Create remote directory
Write-Host "Creating remote directory..." -ForegroundColor Yellow
ssh -i $PemFile $SSH_CONNECTION "mkdir -p $REMOTE_DIR"
Write-Host "OK Remote directory ready" -ForegroundColor Green
Write-Host ""

# Copy files using SCP (works on Windows)
Write-Host "Copying project files to EC2..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor White

# Create a temporary archive
$tempZip = "$env:TEMP\subminds-deploy.zip"
Write-Host "Creating archive..." -ForegroundColor Yellow

# Compress files (excluding unnecessary ones)
$excludePatterns = @('*.pyc', '__pycache__', '.git', '.venv', 'venv', 'node_modules', '*.log', 'data/raw/*', 'data/processed/*', '*.pem')
Compress-Archive -Path @(
    "src",
    "config",
    "scripts",
    "docs",
    "requirements.txt",
    "setup.py",
    "Dockerfile",
    "docker-compose.yml",
    "README.md"
) -DestinationPath $tempZip -Force

# Copy archive to EC2
Write-Host "Uploading archive..." -ForegroundColor Yellow
scp -i $PemFile $tempZip "${SSH_CONNECTION}:${REMOTE_DIR}/project.zip"

# Extract on EC2
Write-Host "Extracting files on EC2..." -ForegroundColor Yellow
ssh -i $PemFile $SSH_CONNECTION "cd $REMOTE_DIR && unzip -o project.zip && rm project.zip"

# Clean up local temp file
Remove-Item $tempZip -Force

Write-Host "OK Files copied successfully" -ForegroundColor Green
Write-Host ""

# Copy .env file separately
Write-Host "Copying environment variables..." -ForegroundColor Yellow
scp -i $PemFile .env "${SSH_CONNECTION}:${REMOTE_DIR}/.env"
ssh -i $PemFile $SSH_CONNECTION "chmod 600 ${REMOTE_DIR}/.env"
Write-Host "OK Environment variables copied" -ForegroundColor Green
Write-Host ""

# Install Docker Compose plugin if needed
Write-Host "Checking Docker Compose..." -ForegroundColor Yellow
$composeCheck = ssh -i $PemFile $SSH_CONNECTION "docker compose version" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing Docker Compose..." -ForegroundColor Yellow
    ssh -i $PemFile $SSH_CONNECTION "sudo apt-get update && sudo apt-get install -y docker-compose-plugin"
    Write-Host "OK Docker Compose installed" -ForegroundColor Green
} else {
    Write-Host "OK Docker Compose already installed" -ForegroundColor Green
}
Write-Host ""

# Build and start containers
Write-Host "Building and starting Docker containers..." -ForegroundColor Yellow
ssh -i $PemFile $SSH_CONNECTION @"
cd $REMOTE_DIR
sudo docker compose down 2>/dev/null || true
sudo docker compose build
sudo docker compose up -d
"@

if ($LASTEXITCODE -ne 0) {
    Write-Host "X Failed to start containers" -ForegroundColor Red
    Write-Host ""
    Write-Host "Checking logs..." -ForegroundColor Yellow
    ssh -i $PemFile $SSH_CONNECTION "cd $REMOTE_DIR && sudo docker compose logs"
    exit 1
}
Write-Host "OK Containers started successfully" -ForegroundColor Green
Write-Host ""

# Check container status
Write-Host "Checking container status..." -ForegroundColor Yellow
ssh -i $PemFile $SSH_CONNECTION "cd $REMOTE_DIR && sudo docker compose ps"
Write-Host ""

# Show recent logs
Write-Host "Recent logs:" -ForegroundColor Yellow
ssh -i $PemFile $SSH_CONNECTION "cd $REMOTE_DIR && sudo docker compose logs --tail=20"
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "  Deployment Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your application is now running on EC2!" -ForegroundColor Green
Write-Host ""
Write-Host "Access your application:" -ForegroundColor Yellow
Write-Host "  http://${EC2Host}:8000" -ForegroundColor Cyan
Write-Host "  http://${EC2Host}:8000/docs" -ForegroundColor Cyan
Write-Host "  http://${EC2Host}:8050" -ForegroundColor Cyan
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Yellow
Write-Host "  View logs:  ssh -i `"$PemFile`" $SSH_CONNECTION 'cd $REMOTE_DIR && sudo docker compose logs -f'" -ForegroundColor White
Write-Host "  Restart:    ssh -i `"$PemFile`" $SSH_CONNECTION 'cd $REMOTE_DIR && sudo docker compose restart'" -ForegroundColor White
Write-Host "  Stop:       ssh -i `"$PemFile`" $SSH_CONNECTION 'cd $REMOTE_DIR && sudo docker compose down'" -ForegroundColor White
Write-Host "  SSH:        ssh -i `"$PemFile`" $SSH_CONNECTION" -ForegroundColor White
Write-Host ""

# Made with Bob
