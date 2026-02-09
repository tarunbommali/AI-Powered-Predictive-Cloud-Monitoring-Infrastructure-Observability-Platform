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


###how to run docker and all
PS D:\Likhitha\Cloud-Monitoring-System> python
>> 
Python 3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import sqlite3
>>> from passlib.context import CryptContext
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'passlib'
>>> from datetime import datetime
>>> 
>>> # Connect to DB
>>> conn = sqlite3.connect("monitoring.db")
>>> cursor = conn.cursor()
>>> 
>>> # Hashing setup
>>> pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'CryptContext' is not defined
>>>
>>> # User details
>>> email = "newadmin@example.com"
>>> username = "newadmin"
>>> full_name = "New Admin"
>>> password = "newadmin@123"
>>>
>>> # Hash the password
>>> hashed_password = pwd_context.hash(password)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'pwd_context' is not defined
>>>
>>> # User flags
>>> is_active = 1
>>> is_admin = 1
>>> created_at = datetime.utcnow().isoformat()
>>>
>>> # Insert user
>>> cursor.execute("""
... INSERT INTO users (email, username, full_name, hashed_password, is_active, is_admin, created_at)
... VALUES (?, ?, ?, ?, ?, ?, ?)
... """, (email, username, full_name, hashed_password, is_active, is_admin, created_at))
Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
NameError: name 'hashed_password' is not defined
>>>
>>> # Commit & close
>>> conn.commit()
>>> conn.close()
>>>
>>> print("New admin user created successfully!")
New admin user created successfully!
>>> exit()
PS D:\Likhitha\Cloud-Monitoring-System> sqlite3 monitoring.db
sqlite3 : The term 'sqlite3' is not recognized as the name of a cmdlet, 
function, script file, or operable program. Check the spelling of the name, or  
if a path was included, verify that the path is correct and try again.
At line:1 char:1
+ sqlite3 monitoring.db
+ ~~~~~~~
    + CategoryInfo          : ObjectNotFound: (sqlite3:String) [], CommandNotF  
   oundException
    + FullyQualifiedErrorId : CommandNotFoundException

PS D:\Likhitha\Cloud-Monitoring-System> SELECT * FROM users;
Select-Object : A positional parameter cannot be found that accepts argument 
'FROM'.
At line:1 char:1
+ SELECT * FROM users;
+ ~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgument: (:) [Select-Object], ParameterB  
   indingException
    + FullyQualifiedErrorId : PositionalParameterNotFound,Microsoft.PowerShell  
   .Commands.SelectObjectCommand

PS D:\Likhitha\Cloud-Monitoring-System> .exit
.exit : The term '.exit' is not recognized as the name of a cmdlet, function, 
script file, or operable program. Check the spelling of the name, or if a path  
was included, verify that the path is correct and try again.
At line:1 char:1
+ .exit
+ ~~~~~
    + CategoryInfo          : ObjectNotFound: (.exit:String) [], CommandNotFou  
   ndException
    + FullyQualifiedErrorId : CommandNotFoundException

PS D:\Likhitha\Cloud-Monitoring-System> docker exec -it f5b1f982e4b8 bash
appuser@f5b1f982e4b8:/app$ 
appuser@f5b1f982e4b8:/app$ docker exec -it f5b1f982e4b8 bash
bash: docker: command not found
appuser@f5b1f982e4b8:/app$ sqlite3 monitoring.db
.tables
SELECT * FROM users;
.exit
SQLite version 3.46.1 2024-08-13 09:16:08
Enter ".help" for usage hints.
sqlite> python
   ...> exit()
   ...> exit
   ...> clear
Program interrupted.
bash: .tables: command not found
bash: SELECT: command not found
bash: .exit: command not found
appuser@f5b1f982e4b8:/app$ python
Python 3.11.14 (main, Jan 13 2026, 03:12:14) [GCC 14.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import sqlite3
>>> from passlib.context import CryptContext
>>> from datetime import datetime
>>>
>>> # Connect to DB
>>> conn = sqlite3.connect("monitoring.db")
>>> cursor = conn.cursor()
>>>
>>> # Password hashing setup
>>> pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")     
>>>
>>> # New user details
>>> email = "newadmin@example.com"
>>> username = "newadmin"
>>> full_name = "New Admin"
>>> password = "newadmin@123"
>>>
>>> # Hash password
>>> hashed_password = pwd_context.hash(password)
>>> 
>>> # Flags
>>> is_active = 1
>>> is_admin = 1
>>> created_at = datetime.utcnow().isoformat()
>>>
>>> # Insert user
>>> cursor.execute("""
... INSERT INTO users (email, username, full_name, hashed_password, is_active, is_admin, created_at)
... VALUES (?, ?, ?, ?, ?, ?, ?)
... """, (email, username, full_name, hashed_password, is_active, is_admin, created_at))
<sqlite3.Cursor object at 0x735ba63797c0>
>>>
>>> conn.commit()
>>> conn.close()
>>> 
>>> print("New admin user created successfully!")
New admin user created successfully!
>>> exit()
appuser@f5b1f982e4b8:/app$ docker exec -it f5b1f982e4b8 bash
bash: docker: command not found
appuser@f5b1f982e4b8:/app$ sqlite3 monitoring.db
SELECT * FROM users;
.exit
SQLite version 3.46.1 2024-08-13 09:16:08
Enter ".help" for usage hints.
sqlite>



1)docker-compose up -d
## 🤝 Contributing
