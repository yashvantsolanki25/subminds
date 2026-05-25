# IBM Cloud CLI Setup Guide

## Prerequisites
- IBM Cloud account (sign up at https://cloud.ibm.com)
- Administrator access on your Windows machine

## Step 1: Install IBM Cloud CLI

### Option A: Manual Installation (Recommended if Application Control is blocking)
1. Download the installer from: https://github.com/IBM-Cloud/ibm-cloud-cli-release/releases
2. Download the latest `IBM_Cloud_CLI_x.x.x_windows_amd64.exe` file
3. Right-click the installer and select "Run as Administrator"
4. Follow the installation wizard
5. Restart your terminal/PowerShell

### Option B: PowerShell Script (Already attempted)
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex(New-Object Net.WebClient).DownloadString('https://clis.cloud.ibm.com/install/powershell')
```

### Verify Installation
```bash
ibmcloud --version
```

## Step 2: Login to IBM Cloud

```bash
ibmcloud login
```

Or if using SSO:
```bash
ibmcloud login --sso
```

Or with API key directly:
```bash
ibmcloud login --apikey YOUR_API_KEY
```

## Step 3: Target Your Region and Resource Group

```bash
# List available regions
ibmcloud regions

# Set target region (e.g., us-south)
ibmcloud target -r us-south

# List resource groups
ibmcloud resource groups

# Set resource group
ibmcloud target -g Default
```

## Step 4: Install Required Plugins

```bash
# Install Watson Machine Learning plugin
ibmcloud plugin install machine-learning

# Install watsonx plugin (if available)
ibmcloud plugin install watsonx
```

## Step 5: Create/Get API Key

### Create a new API Key:
```bash
ibmcloud iam api-key-create my-granite-api-key -d "API key for Granite AI project" --file api-key.json
```

This will create a file `api-key.json` with your API key. **Keep this secure!**

### Or list existing API keys:
```bash
ibmcloud iam api-keys
```

### Or get API key via IBM Cloud Console:
1. Go to https://cloud.ibm.com/iam/apikeys
2. Click "Create an IBM Cloud API key"
3. Give it a name (e.g., "granite-ai-key")
4. Click "Create"
5. **Copy and save the API key immediately** (you won't be able to see it again)

## Step 6: Get Project ID

### Method 1: Via CLI (for Watson Machine Learning)
```bash
# List all Watson Machine Learning instances
ibmcloud resource service-instances --service-name pm-20

# Get instance details
ibmcloud resource service-instance YOUR_INSTANCE_NAME --output json

# List projects (if using watsonx.ai)
ibmcloud watsonx project list
```

### Method 2: Via IBM Cloud Console
1. Go to https://dataplatform.cloud.ibm.com/projects
2. Select your project or create a new one
3. Click on "Manage" tab
4. Find "Project ID" in the project details
5. Copy the Project ID (format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)

### Method 3: Create a New Project
1. Go to https://dataplatform.cloud.ibm.com/projects
2. Click "New project"
3. Select "Create an empty project"
4. Enter project name and description
5. Select a storage service (or create new Cloud Object Storage)
6. Click "Create"
7. Copy the Project ID from the project settings

## Step 7: Configure Environment Variables

### For Windows PowerShell (Temporary - current session only):
```powershell
$env:IBM_CLOUD_API_KEY="your-api-key-here"
$env:IBM_PROJECT_ID="your-project-id-here"
```

### For Windows PowerShell (Permanent - user level):
```powershell
[System.Environment]::SetEnvironmentVariable("IBM_CLOUD_API_KEY", "your-api-key-here", "User")
[System.Environment]::SetEnvironmentVariable("IBM_PROJECT_ID", "your-project-id-here", "User")
```

### For .env file (Recommended for this project):
Create or update the `.env` file in your project root:
```
IBM_CLOUD_API_KEY=your-api-key-here
IBM_PROJECT_ID=your-project-id-here
```

## Step 8: Verify Configuration

### Test API Key:
```bash
ibmcloud login --apikey $env:IBM_CLOUD_API_KEY
```

### Test with Python:
```python
import os
from ibm_watson_machine_learning import APIClient

api_key = os.getenv('IBM_CLOUD_API_KEY')
project_id = os.getenv('IBM_PROJECT_ID')

credentials = {
    "url": "https://us-south.ml.cloud.ibm.com",
    "apikey": api_key
}

client = APIClient(credentials)
client.set.default_project(project_id)
print("Configuration successful!")
```

## Troubleshooting

### Application Control Policy Blocking
If you see "Application Control policy has blocked this file":
1. Contact your IT administrator to whitelist `ibmcloud.exe`
2. Or use IBM Cloud Console web interface for all operations
3. Or use the IBM Cloud API directly in your Python code

### API Key Issues
- Ensure the API key has proper permissions
- Check if the API key is expired
- Verify you're using the correct region

### Project ID Issues
- Ensure the project exists in your IBM Cloud account
- Verify you have access to the project
- Check if the project is in the correct region

## Additional Resources
- IBM Cloud CLI Documentation: https://cloud.ibm.com/docs/cli
- IBM watsonx.ai Documentation: https://dataplatform.cloud.ibm.com/docs/content/wsj/getting-started/welcome-main.html
- IBM Watson Machine Learning: https://cloud.ibm.com/catalog/services/watson-machine-learning

## Security Best Practices
1. Never commit API keys to version control
2. Use `.env` files and add them to `.gitignore`
3. Rotate API keys regularly
4. Use separate API keys for development and production
5. Set appropriate IAM permissions for API keys