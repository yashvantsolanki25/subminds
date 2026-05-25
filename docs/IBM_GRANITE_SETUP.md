# IBM Granite AI Setup Guide

This guide will help you set up IBM Granite AI for the SubMinds project.

## Prerequisites

- IBM Cloud account
- Credit card for IBM Cloud (free tier available)
- Basic understanding of API keys

---

## Step 1: Create IBM Cloud Account

1. Go to [IBM Cloud](https://cloud.ibm.com/registration)
2. Sign up for a free account
3. Verify your email address
4. Complete account setup

---

## Step 2: Create Watson Machine Learning Service

1. **Log in to IBM Cloud Console**
   - Go to https://cloud.ibm.com
   - Click "Log in"

2. **Create Watson Machine Learning Service**
   - Click "Catalog" in the top menu
   - Search for "Watson Machine Learning"
   - Click on "Watson Machine Learning"
   - Select a plan:
     - **Lite Plan**: Free (limited usage)
     - **Standard Plan**: Pay-as-you-go
   - Choose a region (e.g., Dallas, London, Frankfurt)
   - Click "Create"

3. **Wait for Service Provisioning**
   - This may take 1-2 minutes
   - You'll see a success message when ready

---

## Step 3: Get API Credentials

1. **Navigate to Service Credentials**
   - Go to your Watson ML service dashboard
   - Click "Service credentials" in the left menu
   - Click "New credential"
   - Give it a name (e.g., "subminds-credentials")
   - Click "Add"

2. **Copy Credentials**
   - Click "View credentials" on the newly created credential
   - You'll see JSON with:
     ```json
     {
       "apikey": "YOUR_API_KEY_HERE",
       "url": "https://us-south.ml.cloud.ibm.com",
       ...
     }
     ```
   - **IMPORTANT**: Copy and save these credentials securely!

---

## Step 4: Create Watson Studio Project

1. **Go to Watson Studio**
   - From IBM Cloud dashboard, click "Resource list"
   - Find your Watson ML service
   - Click "Launch in Watson Studio"

2. **Create New Project**
   - Click "Create a project"
   - Select "Create an empty project"
   - Give it a name: "SubMinds"
   - Add a description (optional)
   - Click "Create"

3. **Get Project ID**
   - Once created, click on the project
   - Click "Manage" tab
   - Copy the "Project ID" (you'll need this)

---

## Step 5: Configure SubMinds Project

1. **Copy Environment Template**
   ```bash
   cd subminds-may-2026
   cp .env.example .env
   ```

2. **Edit .env File**
   ```bash
   nano .env  # or use your preferred editor
   ```

3. **Add Your Credentials**
   ```env
   # IBM Cloud Credentials
   IBM_CLOUD_API_KEY=your_api_key_from_step_3
   IBM_PROJECT_ID=your_project_id_from_step_4
   
   # Database Credentials
   POSTGRES_PASSWORD=your_secure_password
   MONGO_PASSWORD=your_secure_password
   ```

4. **Save and Close**
   - Press `Ctrl+X`, then `Y`, then `Enter` (in nano)

---

## Step 6: Verify Configuration

1. **Test IBM Granite Connection**
   ```bash
   python -c "from src.ai_engine import GraniteAIClient; client = GraniteAIClient(); print('✓ Connection successful!')"
   ```

2. **Expected Output**
   ```
   INFO - Initializing IBM Granite AI Client
   INFO - Configuration loaded successfully
   INFO - IBM Granite model initialized: ibm/granite-13b-chat-v2
   ✓ Connection successful!
   ```

---

## Step 7: Understanding Usage Limits

### Free Tier (Lite Plan)
- **Capacity Units**: 20 per month
- **API Calls**: Limited
- **Best for**: Development and testing

### Standard Plan
- **Pay-as-you-go**: Based on usage
- **Pricing**: ~$0.50 per 1000 tokens
- **Best for**: Production use

### Monitor Usage
1. Go to IBM Cloud dashboard
2. Click "Billing and usage"
3. View "Usage" tab
4. Monitor Watson ML consumption

---

## Step 8: Security Best Practices

### ✅ DO:
- Store credentials in `.env` file (never commit to git)
- Use environment variables for sensitive data
- Rotate API keys regularly
- Use separate keys for dev/prod
- Enable MFA on IBM Cloud account

### ❌ DON'T:
- Commit `.env` file to version control
- Share API keys in chat/email
- Use production keys in development
- Hard-code credentials in source code
- Leave unused services running

---

## Troubleshooting

### Error: "Authentication failed"
**Solution**: 
- Verify API key is correct
- Check if service is active in IBM Cloud
- Ensure no extra spaces in `.env` file

### Error: "Project not found"
**Solution**:
- Verify Project ID is correct
- Ensure project exists in Watson Studio
- Check if you have access permissions

### Error: "Rate limit exceeded"
**Solution**:
- Wait for rate limit to reset (usually 1 minute)
- Upgrade to Standard plan for higher limits
- Implement request caching in your code

### Error: "Model not available"
**Solution**:
- Check if Granite model is available in your region
- Try different model ID
- Contact IBM support

---

## Alternative: Using IBM watsonx.ai

If you prefer using watsonx.ai instead of Watson ML:

1. **Go to watsonx.ai**
   - Visit https://www.ibm.com/watsonx
   - Sign up for watsonx.ai

2. **Create Deployment Space**
   - Create a new deployment space
   - Deploy Granite model

3. **Update Configuration**
   ```yaml
   # config/ibm_granite_config.yaml
   ibm_granite:
     url: "https://us-south.ml.cloud.ibm.com"
     model:
       id: "ibm/granite-13b-chat-v2"
   ```

---

## Getting Help

### IBM Cloud Support
- **Documentation**: https://cloud.ibm.com/docs
- **Community**: https://community.ibm.com
- **Support Tickets**: IBM Cloud Console → Support

### SubMinds Project
- Check `README.md` for project documentation
- Review `SOLUTION.md` for architecture details
- See `IMPLEMENTATION_GUIDE.md` for code examples

---

## Next Steps

After setup is complete:

1. ✅ Test the connection (Step 6)
2. ✅ Run the simulation: `python scripts/run_simulation.py`
3. ✅ Monitor usage in IBM Cloud dashboard
4. ✅ Start developing your AI models

---

## Cost Estimation

### Development (Lite Plan)
- **Cost**: FREE
- **Usage**: 20 CU/month
- **Suitable for**: Testing, small projects

### Production (Standard Plan)
- **Estimated Cost**: $50-200/month
- **Depends on**:
  - Number of API calls
  - Token usage
  - Model complexity

### Tips to Reduce Costs
1. Implement response caching
2. Batch requests when possible
3. Use rate limiting
4. Monitor usage regularly
5. Optimize prompts for efficiency

---

**🎉 Congratulations! Your IBM Granite AI is now set up and ready to use!**

For questions or issues, refer to the troubleshooting section or contact IBM support.