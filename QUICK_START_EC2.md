# 🚀 Quick Start - Deploy SubMinds to EC2

## ✅ Prerequisites Check

Your EC2 instance is ready:
- ✅ SSH connection working
- ✅ Docker installed (v29.5.2)
- ⚠️ Docker Compose needs installation (script will handle this)

## 🎯 Deploy in 2 Steps

### Step 1: Configure Security Group (One-time setup)

```powershell
.\scripts\configure-security-group.ps1
```

This will automatically:
- Find your EC2 instance security group
- Open required ports (8000, 8050, 80, 443, 22)
- Restrict database ports to your IP only

### Step 2: Deploy Application

```powershell
.\DEPLOY_NOW.ps1
```

This will:
- Copy all files to EC2
- Install Docker Compose if needed
- Copy .env file with your credentials
- Build and start all containers
- Show you the application URL

## 🌐 Access Your Application

After deployment:
- **Main API**: http://ec2-13-206-218-4.ap-south-1.compute.amazonaws.com:8000
- **API Docs**: http://ec2-13-206-218-4.ap-south-1.compute.amazonaws.com:8000/docs
- **Dashboard**: http://ec2-13-206-218-4.ap-south-1.compute.amazonaws.com:8050

## 📊 What Gets Deployed

Your EC2 instance will run:
- **SubMinds Application** (Port 8000, 8050)
- **PostgreSQL Database** (Port 5432)
- **MongoDB Database** (Port 27017)
- **Redis Cache** (Port 6379)

All using your credentials from `.env` file:
- IBM Cloud API Key: `XRNJls6GZurytauCdeC1T0sTIRMyViF9KvSDvCM86MSC`
- IBM Project ID: `c01ebe61-c1ef-4f7d-9706-2da1b4c01fcf`
- Database credentials: `subminds / abcd@1234`

## 🔧 Useful Commands

### View Logs
```powershell
ssh -i "C:\Users\Yashv\OneDrive\AWS Keys\test.pem" ubuntu@ec2-13-206-218-4.ap-south-1.compute.amazonaws.com "cd /home/ubuntu/subminds-may-2026 && sudo docker compose logs -f"
```

### Restart Application
```powershell
ssh -i "C:\Users\Yashv\OneDrive\AWS Keys\test.pem" ubuntu@ec2-13-206-218-4.ap-south-1.compute.amazonaws.com "cd /home/ubuntu/subminds-may-2026 && sudo docker compose restart"
```

### Check Status
```powershell
ssh -i "C:\Users\Yashv\OneDrive\AWS Keys\test.pem" ubuntu@ec2-13-206-218-4.ap-south-1.compute.amazonaws.com "cd /home/ubuntu/subminds-may-2026 && sudo docker compose ps"
```

### SSH into EC2
```powershell
ssh -i "C:\Users\Yashv\OneDrive\AWS Keys\test.pem" ubuntu@ec2-13-206-218-4.ap-south-1.compute.amazonaws.com
```

## 🔄 Update Application

When you make code changes:

```powershell
.\DEPLOY_NOW.ps1
```

The script will:
1. Copy updated files
2. Rebuild containers
3. Restart application

## 🆘 Troubleshooting

### Cannot connect to EC2
```powershell
# Test connection
ssh -i "C:\Users\Yashv\OneDrive\AWS Keys\test.pem" ubuntu@ec2-13-206-218-4.ap-south-1.compute.amazonaws.com

# If fails, check:
# 1. EC2 instance is running (AWS Console)
# 2. Security group allows port 22
# 3. PEM file permissions are correct
```

### Application not accessible
```powershell
# Check if containers are running
ssh -i "C:\Users\Yashv\OneDrive\AWS Keys\test.pem" ubuntu@ec2-13-206-218-4.ap-south-1.compute.amazonaws.com "sudo docker ps"

# Check logs
ssh -i "C:\Users\Yashv\OneDrive\AWS Keys\test.pem" ubuntu@ec2-13-206-218-4.ap-south-1.compute.amazonaws.com "cd /home/ubuntu/subminds-may-2026 && sudo docker compose logs"
```

### Security group issues
```powershell
# Re-run security group configuration
.\scripts\configure-security-group.ps1
```

## 📚 Additional Documentation

- **Complete Deployment Guide**: `AWS_EC2_DEPLOYMENT_GUIDE.md`
- **Security Group Details**: `docs/AWS_SECURITY_GROUP_CONFIG.md`
- **GitHub Secrets Setup**: `GITHUB_SECRETS_QUICK_GUIDE.md`

## 🎉 That's It!

You're ready to deploy. Just run:

```powershell
# Step 1: Configure security (one-time)
.\scripts\configure-security-group.ps1

# Step 2: Deploy
.\DEPLOY_NOW.ps1
```

Your SubMinds application will be live in minutes! 🚀