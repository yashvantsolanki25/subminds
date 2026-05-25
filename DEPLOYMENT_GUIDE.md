# SubMinds Deployment Guide

## 🚀 Complete Deployment Setup

This guide covers the complete setup for deploying SubMinds to AWS EC2 using GitHub Actions.

## Prerequisites

1. **GitHub Account** with repository access
2. **Docker Hub Account** for container registry
3. **AWS Account** with EC2 instance
4. **IBM Cloud Account** for Granite AI

## 📋 Step-by-Step Setup

### 1. GitHub Secrets Configuration

Add the following secrets to your GitHub repository (Settings → Secrets and variables → Actions):

#### Docker Hub Credentials
```
DOCKER_USERNAME=your_dockerhub_username
DOCKER_PASSWORD=your_dockerhub_password_or_token
```

#### AWS Credentials
```
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1  # or your preferred region
```

#### EC2 Instance Details
```
EC2_HOST=your_ec2_public_ip_or_dns
EC2_USER=ubuntu  # or ec2-user for Amazon Linux
EC2_SSH_PRIVATE_KEY=your_private_key_content
```

To get your EC2 SSH private key content:
```bash
cat ~/.ssh/your-key.pem
# Copy the entire output including BEGIN and END lines
```

#### Application Secrets
```
IBM_CLOUD_API_KEY=your_ibm_cloud_api_key
IBM_PROJECT_ID=your_ibm_project_id
POSTGRES_PASSWORD=secure_postgres_password
MONGO_PASSWORD=secure_mongo_password
REDIS_PASSWORD=secure_redis_password
```

### 2. EC2 Instance Setup

#### Launch EC2 Instance
1. Go to AWS EC2 Console
2. Launch instance with:
   - **AMI**: Ubuntu 22.04 LTS
   - **Instance Type**: t3.medium or larger
   - **Storage**: 30GB minimum
   - **Security Group**: Configure ports (see below)

#### Security Group Configuration
Open the following ports:
- **22** (SSH) - Your IP only
- **80** (HTTP) - 0.0.0.0/0
- **443** (HTTPS) - 0.0.0.0/0
- **8000** (API) - 0.0.0.0/0
- **8050** (Dashboard) - 0.0.0.0/0

#### Connect to EC2 and Install Docker
```bash
# SSH into your instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version

# Logout and login again for group changes
exit
```

#### Create Project Directory
```bash
# SSH back in
ssh -i your-key.pem ubuntu@your-ec2-ip

# Create project directory
mkdir -p ~/subminds
cd ~/subminds

# Create necessary subdirectories
mkdir -p data/raw/video data/processed data/models data/art_samples logs config
```

### 3. Local Development Setup

#### Clone Repository
```bash
git clone https://github.com/yourusername/subminds-may-2026.git
cd subminds-may-2026
```

#### Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Configure Environment
```bash
cp .env.example .env
# Edit .env with your credentials
```

### 4. Deployment Process

#### Automatic Deployment (Recommended)
Push to main/master branch:
```bash
git add .
git commit -m "Deploy to production"
git push origin main
```

The GitHub Actions workflow will automatically:
1. Run code quality checks
2. Build Docker image
3. Push to Docker Hub
4. Deploy to EC2
5. Run health checks

#### Manual Deployment
If you need to deploy manually:

```bash
# On your local machine
docker build -t yourusername/subminds-app:latest .
docker push yourusername/subminds-app:latest

# On EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip
cd ~/subminds

# Pull and restart
docker-compose pull
docker-compose down
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs -f
```

### 5. Monitoring and Maintenance

#### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f subminds

# Last 100 lines
docker-compose logs --tail=100
```

#### Check Container Status
```bash
docker-compose ps
docker stats
```

#### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart subminds
```

#### Update Application
```bash
# Pull latest changes
docker-compose pull

# Recreate containers
docker-compose up -d --force-recreate
```

#### Backup Data
```bash
# Backup databases
docker-compose exec postgres pg_dump -U subminds subminds > backup_$(date +%Y%m%d).sql
docker-compose exec mongodb mongodump --out=/backup

# Backup volumes
docker run --rm -v subminds_postgres-data:/data -v $(pwd):/backup ubuntu tar czf /backup/postgres-backup.tar.gz /data
```

### 6. Troubleshooting

#### Container Won't Start
```bash
# Check logs
docker-compose logs subminds

# Check resource usage
docker stats

# Restart Docker daemon
sudo systemctl restart docker
```

#### Database Connection Issues
```bash
# Check database containers
docker-compose ps postgres mongodb redis

# Test database connections
docker-compose exec postgres psql -U subminds -d subminds -c "SELECT 1;"
docker-compose exec mongodb mongosh --eval "db.adminCommand('ping')"
docker-compose exec redis redis-cli ping
```

#### Port Already in Use
```bash
# Find process using port
sudo lsof -i :8000

# Kill process
sudo kill -9 <PID>
```

#### Out of Disk Space
```bash
# Clean up Docker
docker system prune -a --volumes

# Check disk usage
df -h
du -sh /var/lib/docker
```

### 7. Security Best Practices

1. **Use SSH Keys Only** - Disable password authentication
2. **Keep Secrets Secure** - Never commit .env files
3. **Regular Updates** - Keep system and Docker updated
4. **Firewall Rules** - Restrict access to necessary ports only
5. **SSL/TLS** - Use HTTPS in production (setup nginx reverse proxy)
6. **Backup Regularly** - Automate database backups
7. **Monitor Logs** - Set up log aggregation and alerts

### 8. Performance Optimization

#### Increase Docker Resources
Edit `/etc/docker/daemon.json`:
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2"
}
```

#### Database Tuning
For PostgreSQL, edit docker-compose.yml:
```yaml
postgres:
  environment:
    - POSTGRES_SHARED_BUFFERS=256MB
    - POSTGRES_EFFECTIVE_CACHE_SIZE=1GB
```

### 9. Scaling Considerations

#### Horizontal Scaling
Use Docker Swarm or Kubernetes for multi-instance deployment:
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml subminds
```

#### Load Balancing
Add nginx as reverse proxy:
```yaml
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf
```

### 10. CI/CD Pipeline Details

The GitHub Actions workflow includes:

1. **Code Quality Checks**
   - Black formatter
   - Flake8 linting
   - Pylint analysis

2. **Docker Build**
   - Multi-stage build
   - Layer caching
   - Security scanning

3. **Deployment**
   - Zero-downtime deployment
   - Health checks
   - Automatic rollback on failure

4. **Notifications**
   - Deployment status
   - Error alerts

## 🎯 Quick Commands Reference

```bash
# Deploy
git push origin main

# Check status
ssh ubuntu@ec2-ip "cd ~/subminds && docker-compose ps"

# View logs
ssh ubuntu@ec2-ip "cd ~/subminds && docker-compose logs -f --tail=50"

# Restart
ssh ubuntu@ec2-ip "cd ~/subminds && docker-compose restart"

# Update
ssh ubuntu@ec2-ip "cd ~/subminds && docker-compose pull && docker-compose up -d"

# Backup
ssh ubuntu@ec2-ip "cd ~/subminds && docker-compose exec postgres pg_dump -U subminds subminds > backup.sql"
```

## 📞 Support

For issues or questions:
1. Check logs: `docker-compose logs`
2. Review GitHub Actions workflow runs
3. Verify all secrets are correctly set
4. Ensure EC2 security groups are properly configured

## 🔄 Updates and Maintenance

- **Weekly**: Check for security updates
- **Monthly**: Review and optimize resource usage
- **Quarterly**: Update dependencies and Docker images
- **Annually**: Review and update security policies

---

**Made with Bob** 🤖