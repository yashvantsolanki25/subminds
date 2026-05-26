# SubMinds Desktop Application - Installation and Launch Script
# PowerShell Script for Windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SubMinds Desktop Application" -ForegroundColor Cyan
Write-Host "Installation and Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found!" -ForegroundColor Red
    Write-Host "Please install Python 3.9 or higher from https://www.python.org/" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Check if .env exists
Write-Host "Checking configuration..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Write-Host "⚠ .env file not found!" -ForegroundColor Yellow
    if (Test-Path ".env.example") {
        Write-Host "Creating .env from .env.example..." -ForegroundColor Yellow
        Copy-Item ".env.example" ".env"
        Write-Host "✓ .env file created" -ForegroundColor Green
        Write-Host ""
        Write-Host "IMPORTANT: Please edit .env file with your IBM Cloud credentials:" -ForegroundColor Yellow
        Write-Host "  1. Open .env file in a text editor" -ForegroundColor White
        Write-Host "  2. Add your IBM_CLOUD_API_KEY" -ForegroundColor White
        Write-Host "  3. Add your IBM_PROJECT_ID" -ForegroundColor White
        Write-Host "  4. Save the file" -ForegroundColor White
        Write-Host ""
        $continue = Read-Host "Have you configured .env? (y/n)"
        if ($continue -ne "y") {
            Write-Host "Please configure .env and run this script again." -ForegroundColor Yellow
            Read-Host "Press Enter to exit"
            exit 0
        }
    } else {
        Write-Host "✗ .env.example not found!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "✓ Configuration file found" -ForegroundColor Green
}

Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray
Write-Host ""

try {
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Ask to launch
$launch = Read-Host "Launch SubMinds Desktop Application now? (y/n)"
if ($launch -eq "y") {
    Write-Host ""
    Write-Host "Starting SubMinds Desktop Application..." -ForegroundColor Yellow
    Write-Host ""
    
    try {
        python subminds_desktop.py
    } catch {
        Write-Host ""
        Write-Host "✗ Application failed to start" -ForegroundColor Red
        Write-Host "Error: $_" -ForegroundColor Red
    }
} else {
    Write-Host ""
    Write-Host "To launch the application later, run:" -ForegroundColor Yellow
    Write-Host "  python subminds_desktop.py" -ForegroundColor White
    Write-Host "or double-click run_subminds.bat" -ForegroundColor White
}

Write-Host ""
Read-Host "Press Enter to exit"

# Made with Bob
