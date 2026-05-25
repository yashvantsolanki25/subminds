# IBM Cloud Setup Script for SubMinds Project
# This script helps configure IBM Cloud credentials for the Granite AI integration

Write-Host "=== IBM Cloud Setup for SubMinds ===" -ForegroundColor Cyan
Write-Host ""

# Check if IBM Cloud CLI is installed
Write-Host "Checking IBM Cloud CLI installation..." -ForegroundColor Yellow
try {
    $version = ibmcloud --version 2>&1
    Write-Host "✓ IBM Cloud CLI is installed: $version" -ForegroundColor Green
} catch {
    Write-Host "✗ IBM Cloud CLI is not installed or not accessible" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install IBM Cloud CLI first:" -ForegroundColor Yellow
    Write-Host "1. Visit: https://github.com/IBM-Cloud/ibm-cloud-cli-release/releases" -ForegroundColor White
    Write-Host "2. Download the latest Windows installer" -ForegroundColor White
    Write-Host "3. Run as Administrator and restart your terminal" -ForegroundColor White
    Write-Host ""
    Write-Host "Or follow the guide: docs/IBM_CLOUD_CLI_SETUP.md" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "=== Step 1: Login to IBM Cloud ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Choose login method:" -ForegroundColor Yellow
Write-Host "1. Interactive login (default)" -ForegroundColor White
Write-Host "2. SSO login" -ForegroundColor White
Write-Host "3. API key login (if you already have one)" -ForegroundColor White
Write-Host "4. Skip (already logged in)" -ForegroundColor White
Write-Host ""

$loginChoice = Read-Host "Enter choice (1-4)"

switch ($loginChoice) {
    "1" {
        Write-Host "Logging in to IBM Cloud..." -ForegroundColor Yellow
        ibmcloud login
    }
    "2" {
        Write-Host "Logging in with SSO..." -ForegroundColor Yellow
        ibmcloud login --sso
    }
    "3" {
        $apiKey = Read-Host "Enter your API key" -AsSecureString
        $apiKeyPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($apiKey))
        ibmcloud login --apikey $apiKeyPlain
    }
    "4" {
        Write-Host "Skipping login..." -ForegroundColor Yellow
    }
    default {
        Write-Host "Logging in to IBM Cloud..." -ForegroundColor Yellow
        ibmcloud login
    }
}

Write-Host ""
Write-Host "=== Step 2: Set Target Region ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Available regions:" -ForegroundColor Yellow
ibmcloud regions

Write-Host ""
$region = Read-Host "Enter region (e.g., us-south, eu-gb, jp-tok) [default: us-south]"
if ([string]::IsNullOrWhiteSpace($region)) {
    $region = "us-south"
}

ibmcloud target -r $region

Write-Host ""
Write-Host "=== Step 3: Set Resource Group ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Available resource groups:" -ForegroundColor Yellow
ibmcloud resource groups

Write-Host ""
$resourceGroup = Read-Host "Enter resource group [default: Default]"
if ([string]::IsNullOrWhiteSpace($resourceGroup)) {
    $resourceGroup = "Default"
}

ibmcloud target -g $resourceGroup

Write-Host ""
Write-Host "=== Step 4: Create or Use Existing API Key ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Choose option:" -ForegroundColor Yellow
Write-Host "1. Create new API key" -ForegroundColor White
Write-Host "2. Use existing API key (enter manually)" -ForegroundColor White
Write-Host "3. List existing API keys" -ForegroundColor White
Write-Host ""

$apiKeyChoice = Read-Host "Enter choice (1-3)"

$IBM_CLOUD_API_KEY = ""

switch ($apiKeyChoice) {
    "1" {
        $keyName = Read-Host "Enter API key name [default: subminds-granite-key]"
        if ([string]::IsNullOrWhiteSpace($keyName)) {
            $keyName = "subminds-granite-key"
        }
        
        Write-Host "Creating API key..." -ForegroundColor Yellow
        $keyFile = Join-Path $PSScriptRoot "..\api-key.json"
        ibmcloud iam api-key-create $keyName -d "API key for SubMinds Granite AI project" --file $keyFile
        
        if (Test-Path $keyFile) {
            $keyData = Get-Content $keyFile | ConvertFrom-Json
            $IBM_CLOUD_API_KEY = $keyData.apikey
            Write-Host "✓ API key created and saved to: $keyFile" -ForegroundColor Green
            Write-Host "⚠ Keep this file secure and do not commit it to version control!" -ForegroundColor Red
        }
    }
    "2" {
        $IBM_CLOUD_API_KEY = Read-Host "Enter your IBM Cloud API key"
    }
    "3" {
        Write-Host "Existing API keys:" -ForegroundColor Yellow
        ibmcloud iam api-keys
        Write-Host ""
        $IBM_CLOUD_API_KEY = Read-Host "Enter the API key you want to use"
    }
    default {
        Write-Host "Invalid choice. Please run the script again." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "=== Step 5: Get Project ID ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "To get your Project ID:" -ForegroundColor Yellow
Write-Host "1. Go to: https://dataplatform.cloud.ibm.com/projects" -ForegroundColor White
Write-Host "2. Select your project (or create a new one)" -ForegroundColor White
Write-Host "3. Click 'Manage' tab" -ForegroundColor White
Write-Host "4. Copy the Project ID" -ForegroundColor White
Write-Host ""
Write-Host "Or create a new project:" -ForegroundColor Yellow
Write-Host "1. Click 'New project' -> 'Create an empty project'" -ForegroundColor White
Write-Host "2. Enter name and description" -ForegroundColor White
Write-Host "3. Select or create Cloud Object Storage" -ForegroundColor White
Write-Host "4. Copy the Project ID from settings" -ForegroundColor White
Write-Host ""

$IBM_PROJECT_ID = Read-Host "Enter your IBM Project ID"

Write-Host ""
Write-Host "=== Step 6: Save Configuration ===" -ForegroundColor Cyan
Write-Host ""

# Check if .env file exists
$envFile = Join-Path $PSScriptRoot "..\.env"
$envExampleFile = Join-Path $PSScriptRoot "..\.env.example"

if (Test-Path $envFile) {
    Write-Host "⚠ .env file already exists" -ForegroundColor Yellow
    $overwrite = Read-Host "Do you want to update IBM credentials in existing .env? (y/n)"
    
    if ($overwrite -eq "y" -or $overwrite -eq "Y") {
        # Read existing .env
        $envContent = Get-Content $envFile -Raw
        
        # Update IBM credentials
        $envContent = $envContent -replace "IBM_CLOUD_API_KEY=.*", "IBM_CLOUD_API_KEY=$IBM_CLOUD_API_KEY"
        $envContent = $envContent -replace "IBM_PROJECT_ID=.*", "IBM_PROJECT_ID=$IBM_PROJECT_ID"
        
        # Save updated .env
        Set-Content -Path $envFile -Value $envContent -NoNewline
        Write-Host "✓ Updated IBM credentials in .env file" -ForegroundColor Green
    }
} else {
    # Copy from .env.example and update
    if (Test-Path $envExampleFile) {
        Copy-Item $envExampleFile $envFile
        
        # Update IBM credentials
        $envContent = Get-Content $envFile -Raw
        $envContent = $envContent -replace "IBM_CLOUD_API_KEY=your_ibm_cloud_api_key_here", "IBM_CLOUD_API_KEY=$IBM_CLOUD_API_KEY"
        $envContent = $envContent -replace "IBM_PROJECT_ID=your_ibm_project_id_here", "IBM_PROJECT_ID=$IBM_PROJECT_ID"
        
        Set-Content -Path $envFile -Value $envContent -NoNewline
        Write-Host "✓ Created .env file with IBM credentials" -ForegroundColor Green
    } else {
        Write-Host "✗ .env.example not found. Creating new .env file..." -ForegroundColor Yellow
        $newEnvContent = @"
# IBM Cloud Credentials
IBM_CLOUD_API_KEY=$IBM_CLOUD_API_KEY
IBM_PROJECT_ID=$IBM_PROJECT_ID
"@
        Set-Content -Path $envFile -Value $newEnvContent
        Write-Host "✓ Created .env file with IBM credentials" -ForegroundColor Green
    }
}

# Also set environment variables for current session
$env:IBM_CLOUD_API_KEY = $IBM_CLOUD_API_KEY
$env:IBM_PROJECT_ID = $IBM_PROJECT_ID

Write-Host ""
Write-Host "=== Configuration Complete! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Your IBM Cloud credentials have been configured:" -ForegroundColor Cyan
Write-Host "✓ API Key: $($IBM_CLOUD_API_KEY.Substring(0, 10))..." -ForegroundColor Green
Write-Host "✓ Project ID: $IBM_PROJECT_ID" -ForegroundColor Green
Write-Host "✓ Region: $region" -ForegroundColor Green
Write-Host "✓ Resource Group: $resourceGroup" -ForegroundColor Green
Write-Host ""
Write-Host "Environment variables set for current session." -ForegroundColor Yellow
Write-Host "To set permanently, run:" -ForegroundColor Yellow
Write-Host '[System.Environment]::SetEnvironmentVariable("IBM_CLOUD_API_KEY", "' + $IBM_CLOUD_API_KEY + '", "User")' -ForegroundColor White
Write-Host '[System.Environment]::SetEnvironmentVariable("IBM_PROJECT_ID", "' + $IBM_PROJECT_ID + '", "User")' -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Test the configuration: python -c 'from src.ai_engine.granite_client import GraniteClient; print(\"OK\")'" -ForegroundColor White
Write-Host "2. Run the application: docker-compose up" -ForegroundColor White
Write-Host "3. Check docs/IBM_CLOUD_CLI_SETUP.md for more information" -ForegroundColor White
Write-Host ""

# Made with Bob
