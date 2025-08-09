# Deployment Guide - PWD Vision Works

## ภาพรวม
คู่มือการติดตั้งและ deploy ระบบ PWD Vision Works ในสภาพแวดล้อมการผลิต (Production)

## สถาปัตยกรรมระบบ

### 1. แผนภาพระบบ
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Edge Device   │    │  Control Server │    │   Cloud API     │
│  (Raspberry Pi) │◄──►│    (Ubuntu)     │◄──►│   (Optional)    │
│                 │    │                 │    │                 │
│ - Camera        │    │ - Database      │    │ - Analytics     │
│ - Hailo AI      │    │ - Web Interface │    │ - Backup        │
│ - Local Storage │    │ - API Gateway   │    │ - Monitoring    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 2. Components
- **Edge Device**: Raspberry Pi 4/5 + Hailo8 + Camera
- **Control Server**: Ubuntu Server + Database + Web UI
- **Cloud Integration**: Optional backup และ analytics

## การเตรียม Hardware

### 1. Raspberry Pi Setup
```bash
# อัปเดตระบบ
sudo apt update && sudo apt upgrade -y

# ติดตั้ง dependencies
sudo apt install -y \
    python3-pip \
    python3-venv \
    git \
    curl \
    htop \
    vim

# เปิดใช้งาน Camera และ SPI
sudo raspi-config
# Interface Options -> Camera -> Enable
# Interface Options -> SPI -> Enable
```

### 2. Hailo8 Installation
```bash
# ดาวน์โหลด Hailo Software Suite
cd /tmp
wget https://hailo.ai/developer-zone/software-downloads/hailort-4.15.0.tgz
tar -xzf hailort-4.15.0.tgz

# ติดตั้ง HailoRT
cd hailort-4.15.0
sudo ./install.sh

# ตรวจสอบการติดตั้ง
hailortcli fw-control identify
```

## การติดตั้ง PWD Library

### 1. Clone Repository
```bash
# สร้าง directory สำหรับ project
sudo mkdir -p /opt/pwd_vision
sudo chown $USER:$USER /opt/pwd_vision
cd /opt/pwd_vision

# Clone repository
git clone https://github.com/popwandee/pwd_library.git
cd pwd_library
```

### 2. Virtual Environment Setup
```bash
# สร้าง virtual environment
python3 -m venv venv
source venv/bin/activate

# อัปเกรด pip
pip install --upgrade pip

# ติดตั้ง dependencies
pip install -r requirements.txt
```

### 3. Configuration
```bash
# สร้างไฟล์ config
cp config/config.example.yaml config/config.yaml

# แก้ไข config ตามสภาพแวดล้อม
vim config/config.yaml
```

## การสร้างไฟล์ Config

### 1. System Configuration
```yaml
# config/config.yaml
system:
  name: "PWD Vision Edge Device"
  location: "Factory Floor A"
  device_id: "edge_001"
  log_level: "INFO"
  
camera:
  type: "picamera2"  # or "usb_camera"
  resolution: [1920, 1080]
  framerate: 30
  auto_start: true
  
hailo:
  model_path: "models/yolov8n.hef"
  confidence_threshold: 0.5
  nms_threshold: 0.4
  batch_size: 4
  
network:
  control_server: "http://192.168.1.100:8080"
  api_key: "your_api_key_here"
  heartbeat_interval: 30
  
storage:
  local_storage_path: "/opt/pwd_vision/data"
  max_storage_gb: 10
  cleanup_days: 7
```

### 2. Environment Variables
```bash
# สร้างไฟล์ .env
cat > .env << EOF
# Database
DATABASE_URL=postgresql://pwd_user:password@localhost:5432/pwd_vision

# API Keys
API_SECRET_KEY=your-secret-key-here
HAILO_LICENSE_KEY=your-hailo-license

# Monitoring
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000

# Security
ENCRYPTION_KEY=your-encryption-key
JWT_SECRET=your-jwt-secret
EOF
```

## Database Setup

### 1. PostgreSQL Installation
```bash
# ติดตั้ง PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# สร้าง database และ user
sudo -u postgres psql << EOF
CREATE DATABASE pwd_vision;
CREATE USER pwd_user WITH ENCRYPTED PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE pwd_vision TO pwd_user;
\q
EOF
```

### 2. Database Schema
```sql
-- migrations/001_initial_schema.sql
CREATE TABLE devices (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active',
    last_heartbeat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE detections (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(50) REFERENCES devices(device_id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    image_path VARCHAR(255),
    objects JSONB,
    confidence_avg FLOAT,
    processing_time_ms INTEGER
);

CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(50) REFERENCES devices(device_id),
    alert_type VARCHAR(50) NOT NULL,
    message TEXT,
    severity VARCHAR(20) DEFAULT 'info',
    resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## System Services

### 1. PWD Vision Service
```ini
# /etc/systemd/system/pwd-vision.service
[Unit]
Description=PWD Vision Works - AI Detection Service
After=network.target
Wants=network.target

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=/opt/pwd_vision/pwd_library
Environment=PATH=/opt/pwd_vision/pwd_library/venv/bin
ExecStart=/opt/pwd_vision/pwd_library/venv/bin/python -m pwd_library.main
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Security settings
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/pwd_vision

[Install]
WantedBy=multi-user.target
```

### 2. Web API Service
```ini
# /etc/systemd/system/pwd-api.service
[Unit]
Description=PWD Vision Works - Web API
After=network.target postgresql.service
Wants=network.target

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=/opt/pwd_vision/pwd_library
Environment=PATH=/opt/pwd_vision/pwd_library/venv/bin
ExecStart=/opt/pwd_vision/pwd_library/venv/bin/python -m pwd_library.api.server
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. Enable Services
```bash
# Reload systemd และ enable services
sudo systemctl daemon-reload
sudo systemctl enable pwd-vision.service
sudo systemctl enable pwd-api.service

# Start services
sudo systemctl start pwd-vision.service
sudo systemctl start pwd-api.service

# ตรวจสอบสถานะ
sudo systemctl status pwd-vision.service
sudo systemctl status pwd-api.service
```

## Nginx Reverse Proxy

### 1. Nginx Configuration
```nginx
# /etc/nginx/sites-available/pwd-vision
server {
    listen 80;
    server_name your-domain.com;

    # API endpoints
    location /api/ {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # WebSocket for real-time updates
    location /ws {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    # Static files
    location /static/ {
        alias /opt/pwd_vision/pwd_library/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Default route to web interface
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. SSL Setup (Optional)
```bash
# ติดตั้ง Certbot
sudo apt install -y certbot python3-certbot-nginx

# ขอ SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# เพิ่ม: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Docker Deployment (Alternative)

### 1. Dockerfile
```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libopencv-dev \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create user
RUN useradd --create-home --shell /bin/bash pwd_user

# Set working directory
WORKDIR /app
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .
RUN chown -R pwd_user:pwd_user /app

# Switch to non-root user
USER pwd_user

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Start application
CMD ["python", "-m", "pwd_library.main"]
```

### 2. Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  pwd-vision:
    build: .
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://pwd_user:password@db:5432/pwd_vision
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=pwd_vision
      - POSTGRES_USER=pwd_user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl/certs
    depends_on:
      - pwd-vision
    restart: unless-stopped

volumes:
  postgres_data:
```

## Monitoring และ Logging

### 1. System Monitoring
```bash
# ติดตั้ง monitoring tools
sudo apt install -y htop iotop nethogs

# ตั้งค่า log rotation
sudo vim /etc/logrotate.d/pwd-vision
```

### 2. Application Logging
```python
# pwd_library/utils/logging_config.py
import logging
import logging.handlers
import os

def setup_logging(log_level="INFO"):
    """ตั้งค่า logging สำหรับ application"""
    
    # สร้าง log directory
    log_dir = "/var/log/pwd-vision"
    os.makedirs(log_dir, exist_ok=True)
    
    # Root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        f"{log_dir}/pwd-vision.log",
        maxBytes=50*1024*1024,  # 50MB
        backupCount=5
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
```

## Security

### 1. Firewall Configuration
```bash
# ติดตั้งและตั้งค่า UFW
sudo apt install -y ufw

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH
sudo ufw allow ssh

# Allow HTTP/HTTPS
sudo ufw allow 80
sudo ufw allow 443

# Allow API port (internal network only)
sudo ufw allow from 192.168.1.0/24 to any port 8080

# Enable firewall
sudo ufw enable
```

### 2. API Security
```python
# pwd_library/api/security.py
from functools import wraps
import jwt
import os

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != os.getenv('API_SECRET_KEY'):
            return {'error': 'Invalid API key'}, 401
        return f(*args, **kwargs)
    return decorated_function
```

## Backup และ Recovery

### 1. Database Backup
```bash
#!/bin/bash
# scripts/backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups/pwd_vision"
mkdir -p $BACKUP_DIR

# Database backup
pg_dump pwd_vision > "$BACKUP_DIR/db_backup_$DATE.sql"

# Application data backup
tar -czf "$BACKUP_DIR/data_backup_$DATE.tar.gz" /opt/pwd_vision/data

# Models backup (if needed)
tar -czf "$BACKUP_DIR/models_backup_$DATE.tar.gz" /opt/pwd_vision/models

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

### 2. Automated Backup
```bash
# เพิ่มใน crontab
crontab -e

# Backup ทุกวันเวลา 2:00 AM
0 2 * * * /opt/pwd_vision/scripts/backup.sh
```

## Performance Tuning

### 1. System Optimization
```bash
# GPU memory split (Raspberry Pi)
echo "gpu_mem=256" | sudo tee -a /boot/config.txt

# CPU governor
echo "performance" | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor

# Swap optimization
echo "vm.swappiness=10" | sudo tee -a /etc/sysctl.conf
```

### 2. Database Optimization
```sql
-- postgresql.conf optimizations
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
```

## Troubleshooting

### 1. Common Issues
```bash
# ตรวจสอบ services
sudo systemctl status pwd-vision
sudo journalctl -u pwd-vision -f

# ตรวจสอบ logs
tail -f /var/log/pwd-vision/pwd-vision.log

# ตรวจสอบ resources
htop
df -h
free -h

# ตรวจสอบ network
netstat -tlnp
curl -I http://localhost:8080/health
```

### 2. Recovery Procedures
```bash
# Service recovery
sudo systemctl restart pwd-vision
sudo systemctl restart pwd-api

# Database recovery
sudo systemctl restart postgresql
psql pwd_vision < /opt/backups/pwd_vision/db_backup_latest.sql

# Complete system recovery
sudo reboot
```