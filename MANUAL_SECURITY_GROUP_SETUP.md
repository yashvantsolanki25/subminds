# Manual Security Group Setup

The AWS CLI commands failed to add security group rules. Please configure manually:

## 🔧 Quick Setup via AWS Console

### Step 1: Go to Security Groups
1. Open AWS Console: https://console.aws.amazon.com/ec2/
2. Select region: **ap-south-1 (Mumbai)**
3. Click **Security Groups** in left sidebar
4. Find security group: **sg-052f7263ed40feaad**

### Step 2: Add Inbound Rules

Click **Edit inbound rules** and add these:

| Type | Protocol | Port | Source | Description |
|------|----------|------|--------|-------------|
| SSH | TCP | 22 | 0.0.0.0/0 | SSH access |
| HTTP | TCP | 80 | 0.0.0.0/0 | HTTP |
| HTTPS | TCP | 443 | 0.0.0.0/0 | HTTPS |
| Custom TCP | TCP | 8000 | 0.0.0.0/0 | SubMinds API |
| Custom TCP | TCP | 8050 | 0.0.0.0/0 | Dashboard |
| Custom TCP | TCP | 5432 | 43.241.193.247/32 | PostgreSQL (Your IP) |
| Custom TCP | TCP | 27017 | 43.241.193.247/32 | MongoDB (Your IP) |
| Custom TCP | TCP | 6379 | 43.241.193.247/32 | Redis (Your IP) |

### Step 3: Save Rules

Click **Save rules**

## ✅ After Configuration

Run the deployment:
```powershell
.\scripts\deploy-to-ec2-fixed.ps1
```

This will:
- Copy all files to EC2
- Install Docker Compose if needed
- Build and start containers
- Show you the application URL

## 🌐 Access Application

After deployment:
- http://ec2-13-206-218-4.ap-south-1.compute.amazonaws.com:8000
- http://ec2-13-206-218-4.ap-south-1.compute.amazonaws.com:8000/docs
- http://ec2-13-206-218-4.ap-south-1.compute.amazonaws.com:8050