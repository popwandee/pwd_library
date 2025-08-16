# Server Installation Guide

**Version:** 1.0.0  
**Last Updated:** 2024-08-16  
**Author:** Edge AI Team  
**Category:** Installation - Server  
**Status:** Active

## Overview

คู่มือการติดตั้งสำหรับ Server ที่ใช้ Ubuntu สำหรับระบบ LPR (License Plate Recognition)

## 📋 Prerequisites

### Hardware Requirements
- **Ubuntu Server** - x86_64 หรือ ARM64
- **RAM:** 8GB+ (16GB recommended)
- **Storage:** 100GB+ SSD
- **Network:** Gigabit Ethernet
- **CPU:** 4+ cores (8+ cores recommended)

### Software Requirements
- **Ubuntu 22.04+/24.04 LTS**
- **Python 3.10+**
- **Git**
- **PostgreSQL 14+**
- **Nginx**
- **Docker** (optional)

## 🚀 Installation Steps

### Step 1: System Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y \
    python3-pip \
    python3-venv \
    git \
    curl \
    wget \
    htop \
    vim \
    build-essential \
    python3-dev \
    libpq-dev \
    nginx \
    postgresql \
    postgresql-contrib \
    redis-server \
    supervisor \
    certbot \
    python3-certbot-nginx
```

### Step 2: Clone Repository

```bash
# Clone your project repository
git clone <your-repository-url>
cd <your-project-directory>

# Initialize submodules (if any)
git submodule update --init --recursive
```

### Step 3: Setup Python Environment

```bash
# Create virtual environment
python3 -m venv venv_server

# Activate virtual environment
source venv_server/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

### Step 4: Install Python Dependencies

```bash
# Install requirements
pip install -r requirements.txt

# Install additional dependencies
pip install flask
pip install flask-socketio
pip install sqlalchemy
pip install psycopg2-binary
pip install redis
pip install gunicorn
pip install eventlet
```

### Step 5: Setup PostgreSQL Database

```bash
# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database user
sudo -u postgres createuser --interactive
# Enter name of role to add: lpr_user
# Shall the new role be a superuser? (y/n) n
# Shall the new role be allowed to create databases? (y/n) y
# Shall the new role be allowed to create more new roles? (y/n) n

# Create database
sudo -u postgres createdb lpr_database

# Set password for user
sudo -u postgres psql
postgres=# ALTER USER lpr_user WITH PASSWORD 'your_secure_password';
postgres=# \q
```

### Step 6: Setup Redis (for caching and sessions)

```bash
# Start Redis service
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Test Redis connection
redis-cli ping
# Should return: PONG
```

### Step 7: Setup Nginx

```bash
# Create Nginx configuration
sudo tee /etc/nginx/sites-available/lpr-server <<EOF
server {
    listen 80;
    server_name your-server-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /socket.io {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static {
        alias /path/to/your/project/static;
        expires 30d;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/lpr-server /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

### Step 8: Setup Systemd Service

```bash
# Create service file
sudo tee /etc/systemd/system/lpr-server.service <<EOF
[Unit]
Description=LPR Server
After=network.target postgresql.service redis-server.service

[Service]
Type=notify
User=ubuntu
Group=ubuntu
WorkingDirectory=/path/to/your/project
Environment=PATH=/path/to/your/project/venv_server/bin
Environment=FLASK_ENV=production
Environment=FLASK_APP=server_app.wsgi:app
ExecStart=/path/to/your/project/venv_server/bin/gunicorn --config gunicorn_config.py server_app.wsgi:app
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable lpr-server.service
```

## ⚙️ Configuration

### Environment Configuration

สร้างไฟล์ `.env` ในโฟลเดอร์หลัก:

```bash
# Application Configuration
FLASK_ENV=production
FLASK_APP=server_app.wsgi:app
PYTHONPATH=/path/to/your/project

# Database Configuration
DATABASE_URL=postgresql://lpr_user:your_secure_password@localhost:5432/lpr_database
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=

# Network Configuration
HTTP_PORT=8000
WEBSOCKET_PORT=8765
ALLOWED_HOSTS=your-server-domain.com,localhost

# Security Configuration
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key
CORS_ORIGINS=http://localhost:3000,https://your-frontend-domain.com

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/server_app.log

# Performance Configuration
MAX_WORKERS=4
THREADS_PER_WORKER=2
WORKER_TIMEOUT=120

# Edge Device Configuration
EDGE_DEVICES=aicamera1,aicamera2
EDGE_COMMUNICATION_TIMEOUT=30
```

### Database Configuration

```bash
# PostgreSQL configuration
sudo nano /etc/postgresql/14/main/postgresql.conf

# Add/modify these settings:
max_connections = 100
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB

# Restart PostgreSQL
sudo systemctl restart postgresql
```

### Nginx Configuration

```bash
# SSL Configuration (if using HTTPS)
sudo certbot --nginx -d your-server-domain.com

# Rate limiting
sudo tee /etc/nginx/conf.d/rate-limiting.conf <<EOF
limit_req_zone \$binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone \$binary_remote_addr zone=login:10m rate=1r/s;

server {
    # ... existing configuration ...
    
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://127.0.0.1:8000;
    }
    
    location /auth/login {
        limit_req zone=login burst=5 nodelay;
        proxy_pass http://127.0.0.1:8000;
    }
}
EOF
```

## 🔧 Verification

### Step 1: Verify Installation

```bash
# Check Python environment
python3 --version
pip list | grep -E "(flask|sqlalchemy|psycopg2)"

# Check PostgreSQL
sudo systemctl status postgresql
psql -U lpr_user -d lpr_database -c "SELECT version();"

# Check Redis
sudo systemctl status redis-server
redis-cli ping
```

### Step 2: Test Database Connection

```bash
# Test database connection
python3 -c "
import psycopg2
conn = psycopg2.connect('postgresql://lpr_user:your_secure_password@localhost:5432/lpr_database')
print('Database connection successful')
conn.close()
"
```

### Step 3: Test Web Interface

```bash
# Start application
sudo systemctl start lpr-server

# Check service status
sudo systemctl status lpr-server

# Test web interface
curl http://localhost:8000/health
```

### Step 4: Test Communication

```bash
# Test WebSocket
python3 -c "
import websocket
ws = websocket.create_connection('ws://localhost:8765')
print('WebSocket test successful')
ws.close()
"

# Test REST API
curl http://localhost:8000/api/health
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check database connection
sudo -u postgres psql -c "\l"

# Check user permissions
sudo -u postgres psql -c "\du"

# Check PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-14-main.log
```

#### 2. Nginx Issues
```bash
# Check Nginx status
sudo systemctl status nginx

# Check Nginx configuration
sudo nginx -t

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

#### 3. Application Issues
```bash
# Check service status
sudo systemctl status lpr-server

# Check service logs
sudo journalctl -u lpr-server -f

# Check application logs
tail -f logs/server_app.log
```

#### 4. Memory Issues
```bash
# Check memory usage
free -h

# Check swap usage
swapon --show

# Check process memory usage
ps aux --sort=-%mem | head -10
```

### Diagnostic Commands

```bash
# System information
uname -a
cat /etc/os-release

# Hardware information
lscpu
free -h
df -h

# Network information
ip addr show
netstat -tlnp

# Process information
ps aux | grep python
ps aux | grep nginx
ps aux | grep postgres

# Log files
tail -f logs/server_app.log
sudo journalctl -f
```

## 📊 Performance Monitoring

### System Monitoring

```bash
# CPU usage
htop
top

# Memory usage
free -h
cat /proc/meminfo

# Disk usage
df -h
iotop

# Network usage
iftop
nethogs
```

### Application Monitoring

```bash
# Service status
sudo systemctl status lpr-server

# Service logs
sudo journalctl -u lpr-server -f

# Application logs
tail -f logs/server_app.log

# Performance metrics
curl http://localhost:8000/metrics
```

### Database Monitoring

```bash
# Database connections
sudo -u postgres psql -c "SELECT count(*) FROM pg_stat_activity;"

# Database performance
sudo -u postgres psql -c "SELECT * FROM pg_stat_database;"

# Slow queries
sudo -u postgres psql -c "SELECT query, mean_time FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;"
```

## 🔒 Security Configuration

### Firewall Setup

```bash
# Install UFW
sudo apt install ufw

# Configure firewall rules
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow in on tailscale0
sudo ufw allow out on tailscale0

# Enable firewall
sudo ufw enable
```

### SSL/TLS Configuration

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-server-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Database Security

```bash
# PostgreSQL security configuration
sudo nano /etc/postgresql/14/main/pg_hba.conf

# Add/modify these lines:
local   all             postgres                                peer
local   all             all                                     md5
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5

# Restart PostgreSQL
sudo systemctl restart postgresql
```

## 📚 References

- [Ubuntu Documentation](https://ubuntu.com/tutorials)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Note:** เอกสารนี้เป็นคู่มือการติดตั้งสำหรับ Server
