# Quick Deployment Setup for SubMinds

## 🚀 Your Docker Hub Credentials

**Username**: `yashvant25`
**Token**: `dckr_pat_h6frDFxLLipfNZUZl2cXlhF0dKw`

⚠️ **IMPORTANT**: Never commit these credentials to your repository!

## Step 1: Add GitHub Secrets

Go to your GitHub repository: https://github.com/yashvant25/subminds

1. Click **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add each secret below:

### Required Secrets

```
DOCKER_USERNAME = yashvant25
DOCKER_PASSWORD = dckr_pat_h6frDFxLLipfNZUZl2cXlhF0dKw

# AWS Credentials (get from AWS Console)
AWS_ACCESS_KEY_ID = your_aws_access_key
AWS_SECRET_ACCESS_KEY = your_aws_secret_key
AWS_REGION = us-east-1

# EC2 Details (get from AWS EC2 Console)
EC2_HOST = your_ec2_public_ip
EC2_USER = ubuntu
EC2_SSH_PRIVATE_KEY = your_private_key_content

# Application Secrets
IBM_CLOUD_API_KEY = your_ibm_api_key
IBM_PROJECT_ID = your_ibm_project_id
POSTGRES_PASSWORD = generate_secure_password
MONGO_PASSWORD = generate_secure_password
REDIS_PASSWORD = generate_secure_password
```

## Step 2: Generate Secure Passwords

Run this in your terminal:

```bash
# Generate secure passwords
echo "POSTGRES_PASSWORD=$(openssl rand -base64 32)"
echo "MONGO_PASSWORD=$(openssl rand -base64 32)"
echo "REDIS_PASSWORD=$(openssl rand -base64 32)"
```

## Step 3: Setup EC2 Instance

### Launch EC2 Instance
1. Go to AWS EC2 Console
2. Click "Launch Instance"
3. Choose **Ubuntu 22.04 LTS**
4. Instance type: **t3.medium** (minimum)
5. Create or select key pair
6. Configure Security Group:
   - SSH (22) - Your IP
   - HTTP (80) - Anywhere
   - HTTPS (443) - Anywhere
   - Custom TCP (8000) - Anywhere
   - Custom TCP (8050) - Anywhere

### Install Docker on EC2

```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify
docker --version
docker-compose --version

# Create project directory
mkdir -p ~/subminds
cd ~/subminds

# Logout and login again
exit
```

## Step 4: Get Your EC2 SSH Private Key

```bash
# On your local machine
cat ~/.ssh/your-ec2-key.pem
```

Copy the ENTIRE output (including BEGIN and END lines) and add it as `EC2_SSH_PRIVATE_KEY` secret.

## Step 5: Deploy

### Option A: Automatic Deployment (Recommended)

```bash
# Push to GitHub
git add .
git commit -m "Initial deployment"
git push origin main
```

The GitHub Actions workflow will automatically deploy to EC2!

### Option B: Manual Deployment

```bash
# Build and push Docker image
docker build -t yashvant25/subminds:latest .
docker push yashvant25/subminds:latest

# On EC2
ssh -i your-key.pem ubuntu@your-ec2-ip
cd ~/subminds

# Create .env file
cat > .env << EOF
IBM_CLOUD_API_KEY=your_key
IBM_PROJECT_ID=your_project_id
POSTGRES_PASSWORD=your_password
MONGO_PASSWORD=your_password
REDIS_PASSWORD=your_password
POSTGRES_USER=subminds
MONGO_USER=subminds
DEBUG=False
LOG_LEVEL=INFO
EOF

# Copy docker-compose.yml from your repo
# Then run:
docker-compose up -d
```

## Step 6: Verify Deployment

```bash
# Check running containers
ssh ubuntu@your-ec2-ip "cd ~/subminds && docker-compose ps"

# View logs
ssh ubuntu@your-ec2-ip "cd ~/subminds && docker-compose logs -f"

# Test API
curl http://your-ec2-ip:8000
```

## Step 7: Access Your Application

- **API**: http://your-ec2-ip:8000
- **Dashboard**: http://your-ec2-ip:8050

## Troubleshooting

### Docker Login Failed
```bash
echo "dckr_pat_h6frDFxLLipfNZUZl2cXlhF0dKw" | docker login -u yashvant25 --password-stdin
```

### Container Won't Start
```bash
docker-compose logs subminds
docker-compose restart
```

### Port Already in Use
```bash
sudo lsof -i :8000
sudo kill -9 <PID>
```

## Security Checklist

- [ ] Added all secrets to GitHub (not in code!)
- [ ] EC2 security group configured
- [ ] SSH key permissions set to 600
- [ ] Strong passwords generated
- [ ] .env file not committed to git
- [ ] Docker Hub token used (not password)

## Quick Commands

```bash
# View logs
ssh ubuntu@ec2-ip "cd ~/subminds && docker-compose logs -f --tail=50"

# Restart services
ssh ubuntu@ec2-ip "cd ~/subminds && docker-compose restart"

# Update deployment
git push origin main  # Automatic deployment via GitHub Actions

# Manual update
ssh ubuntu@ec2-ip "cd ~/subminds && docker-compose pull && docker-compose up -d"
```

## Next Steps

1. ✅ Add all GitHub secrets
2. ✅ Setup EC2 instance
3. ✅ Push code to GitHub
4. ✅ Verify deployment
5. ✅ Test application
6. ✅ Setup monitoring
7. ✅ Configure SSL/HTTPS (optional)

---

**Made with Bob** 🤖

**REMEMBER**: Keep your credentials secure! Never commit them to your repository.