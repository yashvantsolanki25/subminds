# AWS Security Group Configuration for SubMinds

This guide explains how to configure your EC2 Security Group to allow proper access to the SubMinds application.

## 🔒 Required Security Group Rules

### Inbound Rules

Configure the following inbound rules in your EC2 Security Group:

| Type | Protocol | Port Range | Source | Description |
|------|----------|------------|--------|-------------|
| SSH | TCP | 22 | Your IP/0.0.0.0/0 | SSH access for deployment |
| HTTP | TCP | 80 | 0.0.0.0/0 | HTTP web access |
| HTTPS | TCP | 443 | 0.0.0.0/0 | HTTPS web access (if using SSL) |
| Custom TCP | TCP | 8000 | 0.0.0.0/0 | FastAPI/Application server |
| Custom TCP | TCP | 8050 | 0.0.0.0/0 | Dash/Dashboard (if used) |
| Custom TCP | TCP | 5432 | Your IP | PostgreSQL (if external access needed) |
| Custom TCP | TCP | 27017 | Your IP | MongoDB (if external access needed) |
| Custom TCP | TCP | 6379 | Your IP | Redis (if external access needed) |
| Custom TCP | TCP | 3001 | Your IP | TORCS simulation port |

### Outbound Rules

| Type | Protocol | Port Range | Destination | Description |
|------|----------|------------|-------------|-------------|
| All traffic | All | All | 0.0.0.0/0 | Allow all outbound traffic |

## 🚀 Quick Setup via AWS Console

### Step 1: Navigate to Security Groups

1. Log in to AWS Console
2. Go to **EC2 Dashboard**
3. Click **Security Groups** in the left sidebar
4. Find your instance's security group (e.g., `launch-wizard-1`)

### Step 2: Add Inbound Rules

1. Select your security group
2. Click **Inbound rules** tab
3. Click **Edit inbound rules**
4. Click **Add rule** for each required port
5. Configure as shown in the table above
6. Click **Save rules**

## 🔧 Setup via AWS CLI

If you prefer command line, use these commands:

```bash
# Set your security group ID
SECURITY_GROUP_ID="sg-xxxxxxxxx"

# Add SSH access (port 22)
aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0

# Add HTTP access (port 80)
aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0

# Add HTTPS access (port 443)
aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0

# Add Application server (port 8000)
aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 8000 \
    --cidr 0.0.0.0/0

# Add Dashboard (port 8050)
aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 8050 \
    --cidr 0.0.0.0/0

# Add PostgreSQL (port 5432) - Restrict to your IP
aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 5432 \
    --cidr YOUR_IP/32

# Add MongoDB (port 27017) - Restrict to your IP
aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 27017 \
    --cidr YOUR_IP/32

# Add Redis (port 6379) - Restrict to your IP
aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 6379 \
    --cidr YOUR_IP/32

# Add TORCS simulation (port 3001) - Restrict to your IP
aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 3001 \
    --cidr YOUR_IP/32
```

## 🔐 Security Best Practices

### 1. Restrict SSH Access
Instead of `0.0.0.0/0`, use your specific IP:
```bash
# Get your current IP
curl ifconfig.me

# Use it in security group
# Source: YOUR_IP/32
```

### 2. Database Ports
**IMPORTANT**: Never expose database ports (5432, 27017, 6379) to `0.0.0.0/0`
- Only allow access from your IP or VPC
- Use VPC peering for production databases
- Consider using AWS RDS/DocumentDB/ElastiCache instead

### 3. Use HTTPS
- Install SSL certificate (Let's Encrypt)
- Redirect HTTP to HTTPS
- Close port 80 after SSL setup

### 4. Enable VPC Flow Logs
Monitor network traffic:
```bash
aws ec2 create-flow-logs \
    --resource-type VPC \
    --resource-ids vpc-xxxxxxxx \
    --traffic-type ALL \
    --log-destination-type cloud-watch-logs \
    --log-group-name /aws/vpc/flowlogs
```

## 📋 Automated Security Group Setup Script

Create a PowerShell script to automate security group configuration:

```powershell
# configure-security-group.ps1

$SECURITY_GROUP_ID = "sg-xxxxxxxxx"  # Replace with your SG ID
$YOUR_IP = (Invoke-WebRequest -Uri "https://api.ipify.org").Content

Write-Host "Configuring Security Group: $SECURITY_GROUP_ID" -ForegroundColor Cyan
Write-Host "Your IP: $YOUR_IP" -ForegroundColor Yellow

# Public access ports
$publicPorts = @(22, 80, 443, 8000, 8050)
foreach ($port in $publicPorts) {
    Write-Host "Adding rule for port $port..." -ForegroundColor Yellow
    aws ec2 authorize-security-group-ingress `
        --group-id $SECURITY_GROUP_ID `
        --protocol tcp `
        --port $port `
        --cidr 0.0.0.0/0
}

# Restricted access ports (your IP only)
$restrictedPorts = @(5432, 27017, 6379, 3001)
foreach ($port in $restrictedPorts) {
    Write-Host "Adding restricted rule for port $port..." -ForegroundColor Yellow
    aws ec2 authorize-security-group-ingress `
        --group-id $SECURITY_GROUP_ID `
        --protocol tcp `
        --port $port `
        --cidr "$YOUR_IP/32"
}

Write-Host "Security Group configured successfully!" -ForegroundColor Green
```

## 🔍 Verify Security Group Configuration

### Via AWS Console
1. Go to EC2 → Security Groups
2. Select your security group
3. Check **Inbound rules** tab
4. Verify all required ports are open

### Via AWS CLI
```bash
# List all inbound rules
aws ec2 describe-security-groups \
    --group-ids sg-xxxxxxxxx \
    --query 'SecurityGroups[0].IpPermissions'
```

### Test Connectivity
```bash
# Test SSH
ssh -i test.pem ubuntu@ec2-13-206-218-4.ap-south-1.compute.amazonaws.com

# Test HTTP
curl http://ec2-13-206-218-4.ap-south-1.compute.amazonaws.com:8000

# Test specific port
nc -zv ec2-13-206-218-4.ap-south-1.compute.amazonaws.com 8000
```

## 🌐 Application Access URLs

After configuration, access your application at:

- **Main Application**: http://ec2-13-206-218-4.ap-south-1.compute.amazonaws.com:8000
- **Dashboard**: http://ec2-13-206-218-4.ap-south-1.compute.amazonaws.com:8050
- **API Documentation**: http://ec2-13-206-218-4.ap-south-1.compute.amazonaws.com:8000/docs

## 🚨 Troubleshooting

### Cannot Connect to Application

1. **Check Security Group**
   ```bash
   aws ec2 describe-security-groups --group-ids sg-xxxxxxxxx
   ```

2. **Check if port is listening**
   ```bash
   ssh -i test.pem ubuntu@ec2-13-206-218-4.ap-south-1.compute.amazonaws.com
   sudo netstat -tlnp | grep 8000
   ```

3. **Check Docker containers**
   ```bash
   sudo docker-compose ps
   sudo docker-compose logs
   ```

4. **Check firewall on EC2**
   ```bash
   sudo ufw status
   # If active, allow ports:
   sudo ufw allow 8000
   sudo ufw allow 8050
   ```

### Connection Timeout

- Verify security group allows your IP
- Check if EC2 instance is running
- Verify VPC and subnet configuration
- Check Network ACLs

### Database Connection Issues

- Ensure database ports are open to your IP
- Check if databases are running in Docker
- Verify connection strings in .env file

## 📊 Port Usage Summary

| Port | Service | Access Level | Purpose |
|------|---------|--------------|---------|
| 22 | SSH | Public/Restricted | Server management |
| 80 | HTTP | Public | Web access |
| 443 | HTTPS | Public | Secure web access |
| 8000 | FastAPI | Public | Main application API |
| 8050 | Dash | Public | Dashboard interface |
| 5432 | PostgreSQL | Restricted | Database access |
| 27017 | MongoDB | Restricted | NoSQL database |
| 6379 | Redis | Restricted | Cache/Queue |
| 3001 | TORCS | Restricted | Simulation server |

## 🔄 Update Security Group

To modify existing rules:

```bash
# Remove a rule
aws ec2 revoke-security-group-ingress \
    --group-id sg-xxxxxxxxx \
    --protocol tcp \
    --port 8000 \
    --cidr 0.0.0.0/0

# Add updated rule
aws ec2 authorize-security-group-ingress \
    --group-id sg-xxxxxxxxx \
    --protocol tcp \
    --port 8000 \
    --cidr YOUR_NEW_IP/32
```

## 📚 Additional Resources

- [AWS Security Groups Documentation](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html)
- [AWS CLI Security Group Commands](https://docs.aws.amazon.com/cli/latest/reference/ec2/authorize-security-group-ingress.html)
- [VPC Best Practices](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-best-practices.html)

---

**Next Steps:**
1. Configure security group using one of the methods above
2. Run deployment script: `.\scripts\deploy-to-ec2.ps1`
3. Access your application at the URLs listed above
4. Monitor logs and performance