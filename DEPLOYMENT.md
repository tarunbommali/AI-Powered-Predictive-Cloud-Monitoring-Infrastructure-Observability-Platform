# Deployment Guide

This guide covers deploying the Cloud Monitoring System to production environments.

## Table of Contents

1. [AWS EC2 Deployment](#aws-ec2-deployment)
2. [Docker Production Setup](#docker-production-setup)
3. [Security Configuration](#security-configuration)
4. [SSL/TLS Setup](#ssltls-setup)
5. [Monitoring Production](#monitoring-production)

## AWS EC2 Deployment

### Prerequisites

- AWS Account with EC2 access
- At least 2 EC2 instances:
  - 1 for the monitoring stack (t3.medium recommended)
  - 1+ for applications being monitored

### Step 1: Launch Monitoring Server

```bash
# Launch EC2 instance (Ubuntu 22.04 LTS recommended)
# Instance type: t3.medium or larger
# Storage: 30GB+ SSD
# Security Group: Allow ports 22, 80, 443, 8000, 9090, 3000, 3001

# Connect to instance
ssh -i your-key.pem ubuntu@your-instance-ip
```

### Step 2: Install Docker

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login again
exit
```

### Step 3: Deploy Application

```bash
# Clone repository
git clone <your-repo-url>
cd cloud-monitoring-system

# Configure environment
cp backend/.env.example backend/.env
nano backend/.env  # Edit configuration

# Update Prometheus targets
nano monitoring/prometheus/prometheus.yml
# Add your EC2 instance IPs

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Verify all services are running
docker-compose ps
```

### Step 4: Configure Target Instances

On each EC2 instance to monitor:

```bash
# Install Node Exporter
wget https://github.com/prometheus/node_exporter/releases/download/v1.7.0/node_exporter-1.7.0.linux-amd64.tar.gz
tar xvfz node_exporter-1.7.0.linux-amd64.tar.gz
sudo mv node_exporter-1.7.0.linux-amd64/node_exporter /usr/local/bin/

# Create user
sudo useradd --no-create-home --shell /bin/false node_exporter

# Create systemd service
sudo tee /etc/systemd/system/node_exporter.service << EOF
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
EOF

# Start service
sudo systemctl daemon-reload
sudo systemctl start node_exporter
sudo systemctl enable node_exporter

# Verify
sudo systemctl status node_exporter
curl http://localhost:9100/metrics
```

## Docker Production Setup

### Environment Variables

Create `.env` file with production values:

```env
# Production Database
DATABASE_URL=postgresql://prod_user:secure_password@postgres:5432/monitoring

# Security
SECRET_KEY=<generate-strong-random-key>
DEBUG=False

# Email Configuration
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=<your-sendgrid-api-key>
ALERT_EMAIL_FROM=alerts@yourdomain.com
ALERT_EMAIL_TO=ops@yourdomain.com

# Grafana
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=<strong-password>
GRAFANA_ROOT_URL=https://grafana.yourdomain.com
```

### Generate Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Production Docker Compose

Use `docker-compose.prod.yml` for production:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Security Configuration

### 1. Firewall Setup (UFW)

```bash
# Enable UFW
sudo ufw enable

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow monitoring access (restrict to your IP)
sudo ufw allow from YOUR_IP to any port 9090  # Prometheus
sudo ufw allow from YOUR_IP to any port 3001  # Grafana

# Check status
sudo ufw status
```

### 2. Security Groups (AWS)

Configure EC2 Security Groups:

**Monitoring Server:**
- SSH (22): Your IP only
- HTTP (80): 0.0.0.0/0
- HTTPS (443): 0.0.0.0/0
- Prometheus (9090): Your IP / VPC only
- Grafana (3001): Your IP / VPC only

**Target Instances:**
- Node Exporter (9100): Monitoring Server IP only

### 3. Application Security

```bash
# Change default passwords
# Update backend/.env:
SECRET_KEY=<strong-random-key>

# Update docker-compose.prod.yml:
POSTGRES_PASSWORD=<strong-password>
GRAFANA_ADMIN_PASSWORD=<strong-password>
```

### 4. Database Security

```bash
# Backup PostgreSQL
docker exec monitoring-postgres-prod pg_dump -U monitoring_user monitoring > backup.sql

# Restore
docker exec -i monitoring-postgres-prod psql -U monitoring_user monitoring < backup.sql
```

## SSL/TLS Setup

### Option 1: Let's Encrypt (Recommended)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

### Option 2: Nginx as Reverse Proxy

Create `nginx/nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:80;
    }

    upstream grafana {
        server grafana:3000;
    }

    server {
        listen 80;
        server_name yourdomain.com;
        
        # Redirect to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name yourdomain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Backend API
        location /api {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Grafana
        location /grafana/ {
            proxy_pass http://grafana/;
            proxy_set_header Host $host;
        }
    }
}
```

## Monitoring Production

### Health Checks

```bash
# API Health
curl http://localhost:8000/api/health

# Prometheus Health
curl http://localhost:9090/-/healthy

# Check all services
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f prometheus
```

### Automated Backups

Create backup script `backup.sh`:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Backup database
docker exec monitoring-postgres-prod pg_dump -U monitoring_user monitoring > $BACKUP_DIR/db_$DATE.sql

# Backup Prometheus data
docker exec monitoring-prometheus-prod tar czf /tmp/prometheus_$DATE.tar.gz /prometheus
docker cp monitoring-prometheus-prod:/tmp/prometheus_$DATE.tar.gz $BACKUP_DIR/

# Backup Grafana
docker exec monitoring-grafana-prod tar czf /tmp/grafana_$DATE.tar.gz /var/lib/grafana
docker cp monitoring-grafana-prod:/tmp/grafana_$DATE.tar.gz $BACKUP_DIR/

# Remove old backups (keep 7 days)
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

Add to crontab:
```bash
# Run daily at 2 AM
0 2 * * * /path/to/backup.sh
```

### Monitoring Metrics

Key metrics to monitor:

1. **System Resources**
   - CPU usage < 80%
   - Memory usage < 85%
   - Disk usage < 90%

2. **Application Health**
   - API response time < 500ms
   - Error rate < 1%
   - Uptime > 99.9%

3. **Database**
   - Connection pool usage
   - Query performance
   - Database size

### Scaling Considerations

**Horizontal Scaling:**
```bash
# Scale backend instances
docker-compose up -d --scale backend=3

# Add load balancer
# Update nginx configuration
```

**Vertical Scaling:**
- Upgrade EC2 instance type
- Increase container resource limits
- Optimize database queries

## Maintenance

### Update Application

```bash
# Pull latest changes
git pull

# Rebuild containers
docker-compose -f docker-compose.prod.yml build

# Restart services
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose logs -f
```

### Database Migrations

```bash
# Run migrations
docker exec monitoring-backend-prod alembic upgrade head

# Rollback if needed
docker exec monitoring-backend-prod alembic downgrade -1
```

### Clean Up

```bash
# Remove unused containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Full cleanup
docker system prune -a
```

## Troubleshooting Production

### High CPU Usage

```bash
# Check container resource usage
docker stats

# Identify processes
docker exec monitoring-backend-prod top

# Check logs for errors
docker-compose logs --tail=100 backend
```

### Memory Leaks

```bash
# Monitor memory over time
watch -n 5 docker stats

# Restart specific service
docker-compose restart backend

# Check for zombie processes
docker exec monitoring-backend-prod ps aux
```

### Database Issues

```bash
# Check database connections
docker exec monitoring-postgres-prod psql -U monitoring_user -c "SELECT * FROM pg_stat_activity;"

# Vacuum database
docker exec monitoring-postgres-prod psql -U monitoring_user -c "VACUUM ANALYZE;"

# Check database size
docker exec monitoring-postgres-prod psql -U monitoring_user -c "SELECT pg_size_pretty(pg_database_size('monitoring'));"
```

## Best Practices

1. **Always use HTTPS in production**
2. **Regular backups** (database, configuration, Prometheus data)
3. **Monitor your monitoring system**
4. **Keep secrets in environment variables**
5. **Use strong passwords**
6. **Update regularly** (security patches)
7. **Set up log rotation**
8. **Implement rate limiting**
9. **Use a CDN** for static assets
10. **Document your setup**

## Support

For production support:
- Email: ops@yourdomain.com
- Slack: #monitoring-support
- On-call: PagerDuty integration
