# AWS EC2 Deployment Guide for SubMinds

Complete guide to deploy SubMinds application to your EC2 instance.

## 📋 Your EC2 Instance Details

- **Host**: `ec2-13-206-218-4.ap-south-1.compute.amazonaws.com`
- **User**: `ubuntu`
- **PEM File Location**: `C:\Users\Yashv\OneDrive\AWS Keys\test.pem`
- **Region**: `ap-south-1` (Mumbai)

## 🚀 Quick Deployment (One Command)

Run this command from your project directory:

```powershell
.\scripts\deploy-to-ec2.ps1 -PemFile "C:\Users\Yashv\OneDrive\AWS Keys\test.pem"
```

This will:
1. ✅ Test SSH connection
2. ✅ Copy all project files to EC2
3. ✅ Copy .env file with credentials
4. ✅ Install Docker & Docker Compose (if needed)
5. ✅ Build and start containers
6. ✅ Show application status

## 📝 Step-by-Step Manual Deployment

### Step 1: Test SSH Connection

```powershell
ssh -i "C:\Users\Yashv\OneDrive\AWS Keys\test.pem" ubuntu@ec2-13-206-218-4.ap-south-1.compute.amazonaws.com
```

If successful, you'll see the Ubuntu welcome message.

### Step 2: Configure Security Group

**Option A: Via AWS Console**
1. Go to AWS Console → EC2 → Security Groups
2. Find your instance's security group
3. Add these inbound rules:
   - Port 22 (SSH) - Your IP
   - Port 80 (HTTP) - 0.0.0.0/0
   - Port 443 (HTTPS) - 0.0.0.0/0
   - Port 8000 (Application) - 0.0.0.0/0
   - Port 8050 (Dashboard) - 0.0.0.0/0
   - Port 5432 (PostgreSQL) - Your IP only
   - Port 27017 (MongoDB) - Your IP only
   - Port 6379 (Redis) - Your IP only

**Option B: Via AWS CLI**
```powershell
# Get your security group ID first
aws ec2 describe-instances --filters "Name=dns-name,Values=ec2-13-206-218-4.ap-south-1.compute.amazonaws.com" --query "Reservations[0].Instances[0].SecurityGroups[0].GroupId"

# Then run the configuration script (see docs/AWS_SECURITY_GROUP_CONFIG.md)
```

### Step 3: Deploy Application

```powershell
# From your project directory
cd c:\Users\Yashv\Downloads\subminds-may-2026

# Run deployment script
.\scripts\deploy-to-ec2.ps1 -PemFile "C:\Users\Yashv\OneDrive\AWS Keys\test.pem"
```

### Step 4: Verify Deployment

After deployment completes, access your application:

- **Main Application**: http://ec2-13-206-218-4.ap-south-1.compute.amazonaws.com:8000
- **API Documentation**: http://ec2-13-206-218-4.ap-south-1.compute.amazonaws.com:8000/docs
- **Dashboard**: http://ec2-13-206-218-4.ap-south-1.compute.amazonaws.com:8050

## 🔧 Manual Commands (If Needed)

### Connect to EC2
```powershell
ssh -i "C:\Users\Yashv\OneDrive\AWS Keys\test.pem" ubuntu@ec2-13-206-218-4.ap-south-1.compute.amazonaws.com
```

### Check Docker Status
```bash
sudo docker ps
sudo docker-compose ps
```

### View Logs
```bash
cd /home/ubuntu/subminds-may-2026
sudo docker-compose logs -f
```

### Restart Application
```bash
cd /home/ubuntu/subminds-may-2026
sudo docker-compose restart
```

### Stop Application
```bash
cd /home/ubuntu/subminds-may-2026
sudo docker-compose down
```

### Start Application
```bash
cd /home/ubuntu/subminds-may-2026
sudo docker-compose up -d
```

### Rebuild Containers
```bash
cd /home/ubuntu/subminds-may-2026
sudo docker-compose down
sudo docker-compose build --no-cache
sudo docker-compose up -d
```

## 🔍 Troubleshooting

### Issue: Cannot connect via SSH

**Solution:**
```powershell
# Check PEM file permissions
icacls "C:\Users\Yashv\OneDrive\AWS Keys\test.pem"

# Fix permissions (run as Administrator)
icacls "C:\Users\Yashv\OneDrive\AWS Keys\test.pem" /inheritance:r
icacls "C:\Users\Yashv\OneDrive\AWS Keys\test.pem" /grant:r "$($env:USERNAME):(R)"
```

### Issue: Connection timeout

**Check:**
1. EC2 instance is running (AWS Console)
2. Security group allows port 22 from your IP
3. Network ACLs are not blocking traffic

### Issue: Application not accessible

**Check:**
1. Security group has port 8000 open
2. Docker containers are running: `sudo docker ps`
3. Application logs: `sudo docker-compose logs`

### Issue: Database connection errors

**Check:**
1. .env file is present: `cat /home/ubuntu/subminds-may-2026/.env`
2. Database containers are running: `sudo docker ps | grep postgres`
3. Database ports are accessible

## 📊 Monitoring

### Check Application Health
```bash
# From your PC
curl http://ec2-13-206-218-4.ap-south-1.compute.amazonaws.com:8000/health

# Or via browser
http://ec2-13-206-218-4.ap-south-1.compute.amazonaws.com:8000/docs
```

### Monitor Resource Usage
```bash
# SSH into EC2
ssh -i "C:\Users\Yashv\OneDrive\AWS Keys\test.pem" ubuntu@ec2-13-206-218-4.ap-south-1.compute.amazonaws.com

# Check CPU/Memory
htop

# Check disk space
df -h

# Check Docker stats
sudo docker stats
```

### View Application Logs
```bash
# Real-time logs
sudo docker-compose logs -f

# Last 100 lines
sudo docker-compose logs --tail=100

# Specific service
sudo docker-compose logs -f app
```

## 🔄 Update Application

When you make changes to your code:

```powershell
# From your PC, run deployment script again
.\scripts\deploy-to-ec2.ps1 -PemFile "C:\Users\Yashv\OneDrive\AWS Keys\test.pem"
```

Or manually:

```powershell
# Copy updated files
scp -i "C:\Users\Yashv\OneDrive\AWS Keys\test.pem" -r ./src ubuntu@ec2-13-206-218-4.ap-south-1.compute.amazonaws.com:/home/ubuntu/subminds-may-2026/

# SSH and restart
ssh -i "C:\Users\Yashv\OneDrive\AWS Keys\test.pem" ubuntu@ec2-13-206-218-4.ap-south-1.compute.amazonaws.com
cd /home/ubuntu/subminds-may-2026
sudo docker-compose restart
```

## 🔐 Security Checklist

- [ ] PEM file has restricted permissions
- [ ] Security group limits SSH to your IP
- [ ] Database ports not exposed to public
- [ ] .env file has secure permissions (600)
- [ ] Regular security updates: `sudo apt update && sudo apt upgrade`
- [ ] Firewall configured: `sudo ufw status`
- [ ] SSL certificate installed (for production)

## 📈 Performance Optimization

### Enable Swap (if needed)
```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Docker Cleanup
```bash
# Remove unused containers
sudo docker system prune -a

# Remove unused volumes
sudo docker volume prune
```

## 🆘 Emergency Commands

### Stop Everything
```bash
sudo docker-compose down
sudo systemctl stop docker
```

### Check System Status
```bash
sudo systemctl status docker
sudo journalctl -u docker -n 50
```

### Restart Docker
```bash
sudo systemctl restart docker
cd /home/ubuntu/subminds-may-2026
sudo docker-compose up -d
```

## 📞 Quick Reference

| Action | Command |
|--------|---------|
| Deploy | `.\scripts\deploy-to-ec2.ps1 -PemFile "C:\Users\Yashv\OneDrive\AWS Keys\test.pem"` |
| SSH | `ssh -i "C:\Users\Yashv\OneDrive\AWS Keys\test.pem" ubuntu@ec2-13-206-218-4.ap-south-1.compute.amazonaws.com` |
| Logs | `sudo docker-compose logs -f` |
| Restart | `sudo docker-compose restart` |
| Status | `sudo docker-compose ps` |
| Stop | `sudo docker-compose down` |
| Start | `sudo docker-compose up -d` |

## 🎯 Next Steps

1. ✅ Configure Security Group (see docs/AWS_SECURITY_GROUP_CONFIG.md)
2. ✅ Run deployment script
3. ✅ Verify application is accessible
4. ✅ Test all endpoints
5. ✅ Monitor logs for errors
6. ✅ Set up SSL certificate (for production)
7. ✅ Configure domain name (optional)
8. ✅ Set up monitoring/alerts

---

**Ready to deploy?** Run:
```powershell
.\scripts\deploy-to-ec2.ps1 -PemFile "C:\Users\Yashv\OneDrive\AWS Keys\test.pem"