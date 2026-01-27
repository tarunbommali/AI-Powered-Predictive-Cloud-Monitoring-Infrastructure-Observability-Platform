# Quick Start Guide

Get the Cloud Monitoring System up and running in 5 minutes!

## Prerequisites

- Docker & Docker Compose installed
- At least one EC2 instance with Node Exporter running

## Steps

### 1. Configure Backend

```bash
cd backend
cp .env.example .env
nano .env  # Edit with your settings
```

**Minimum required changes:**
- Generate a new `SECRET_KEY`
- Configure `SMTP_USER` and `SMTP_PASSWORD` for email alerts (optional)

### 2. Configure Prometheus

Edit `monitoring/prometheus/prometheus.yml` and add your EC2 instances:

```yaml
scrape_configs:
  - job_name: 'node-exporter'
    static_configs:
      - targets:
          - '10.0.1.100:9100'  # Replace with your EC2 IP
```

### 3. Start Services

```bash
# From project root
./setup.sh

# Or manually:
docker-compose up -d
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API Docs**: http://localhost:8000/api/docs
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/admin)

### 5. Register and Login

1. Go to http://localhost:3000
2. Click "Register" tab
3. Create an account
4. Login with your credentials

### 6. Add Instances

1. Navigate to "Instances" page
2. Click "Add Instance"
3. Fill in EC2 instance details:
   - Name: Any descriptive name
   - Instance ID: AWS instance ID
   - IP Address: Private or public IP
   - Port: 9100 (Node Exporter default)
   - Region: AWS region
   - Instance Type: e.g., t3.medium

### 7. View Metrics

- Go to "Dashboard" to see overview
- Go to "Metrics" for detailed charts
- Go to "Alerts" to see triggered alerts

## Troubleshooting

**Cannot connect to EC2 instances:**
- Verify Node Exporter is running on EC2: `curl http://localhost:9100/metrics`
- Check security groups allow port 9100
- Verify IP address is correct in Prometheus config

**Frontend not loading:**
- Check if backend is running: `curl http://localhost:8000/api/health`
- Check Docker logs: `docker-compose logs frontend`

**No metrics showing:**
- Wait 15-30 seconds for initial scrape
- Check Prometheus targets: http://localhost:9090/targets
- Verify instances are added in the UI

## Next Steps

- Configure email alerts in `backend/.env`
- Import Grafana dashboard from `monitoring/grafana/dashboards/`
- Set up SSL/TLS for production
- Configure backups

For detailed documentation, see [README.md](README.md) and [DEPLOYMENT.md](DEPLOYMENT.md).
