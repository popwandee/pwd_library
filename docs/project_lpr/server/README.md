# LPR Server - Project Documentation

**Version:** 2.0.0  
**Last Updated:** 2024-08-16  
**Author:** AI Camera Team  
**Status:** Active Development

## Overview

LPR Server เป็นระบบประมวลผล License Plate Recognition ที่ทำงานบน Ubuntu Server สำหรับรับข้อมูลจาก Edge devices และประมวลผลผลลัพธ์ โดยใช้ Unified Communication Architecture

## System Architecture

### Server Platform (Ubuntu)
- **Hardware:** Ubuntu Server (x86_64 หรือ ARM64)
- **OS:** Ubuntu 22.04+/24.04 LTS
- **Database:** PostgreSQL 14+
- **Web Framework:** Flask + Flask-SocketIO
- **Frontend:** Bootstrap 5 + Chart.js
- **Communication:** Unified Communication Gateway

### Unified Communication Support
- **WebSocket:** Real-time data streaming
- **REST API:** CRUD operations และ configuration
- **MQTT:** Message queuing และ pub/sub
- **SFTP:** Secure file transfer
- **rsync:** File synchronization

## Key Features

### Core Functionality
- License Plate Recognition processing
- Database storage และ management
- Web-based dashboard
- RESTful API สำหรับ Edge communication
- Real-time data streaming via WebSocket
- User authentication และ authorization

### Advanced Features
- Unified Communication Gateway
- Protocol auto-selection
- Fallback mechanism
- Load balancing
- Performance monitoring
- Security encryption

## Project Structure

```
lpr_server/
├── api/                    # API endpoints
│   ├── rest/              # REST API endpoints
│   ├── websocket/         # WebSocket handlers
│   └── mqtt/              # MQTT subscribers
├── communication/          # Unified Communication Gateway
│   ├── gateway/           # Main gateway implementation
│   ├── protocols/         # Protocol implementations
│   ├── monitoring/        # Communication monitoring
│   └── security/          # Security management
├── database/               # Database models และ migrations
│   ├── models/            # SQLAlchemy models
│   ├── migrations/        # Database migrations
│   └── schemas/           # Pydantic schemas
├── frontend/               # Web dashboard
│   ├── templates/         # HTML templates
│   ├── static/            # CSS, JS, images
│   └── components/        # Reusable components
├── processing/             # LPR processing logic
│   ├── lpr/               # LPR algorithms
│   ├── image/             # Image processing
│   └── validation/        # Data validation
├── storage/                # File storage management
│   ├── sftp/              # SFTP server
│   ├── rsync/             # rsync configuration
│   └── cleanup/           # Storage cleanup
├── monitoring/             # System monitoring
│   ├── metrics/           # Performance metrics
│   ├── alerts/            # Alert system
│   └── dashboards/        # Monitoring dashboards
├── docs/                   # Documentation
├── tests/                  # Test suite
├── deployment/             # Deployment scripts
└── config/                 # Configuration files
```

## Technology Stack

### Backend
- **Python 3.10+**
- **Flask** - Web framework
- **Flask-SocketIO** - WebSocket support
- **SQLAlchemy** - Database ORM
- **PostgreSQL** - Database
- **Pydantic** - Data validation
- **Celery** - Task queue (optional)

### Communication
- **WebSocket** - Real-time communication
- **REST API** - HTTP communication
- **MQTT** - Message queuing
- **SFTP** - File transfer
- **rsync** - File synchronization

### Frontend
- **Bootstrap 5** - UI framework
- **Chart.js** - Data visualization
- **JavaScript** - Client-side logic
- **WebSocket** - Real-time updates

### Infrastructure
- **Nginx** - Reverse proxy
- **Gunicorn** - WSGI server
- **Mosquitto** - MQTT broker
- **Redis** - Caching และ session storage
- **Docker** - Containerization (optional)

## Development Status

### Completed Features
- [x] Project structure setup
- [x] Unified Communication Architecture design
- [x] Database schema planning
- [x] API endpoints specification
- [x] Security framework design

### In Progress
- [ ] Database schema implementation
- [ ] REST API endpoints development
- [ ] WebSocket integration
- [ ] MQTT broker setup
- [ ] SFTP server configuration

### Planned Features
- [ ] LPR processing integration
- [ ] Web dashboard development
- [ ] User authentication system
- [ ] Real-time data streaming
- [ ] Performance monitoring
- [ ] Security implementation
- [ ] File storage management
- [ ] Backup และ recovery system

### Documentation Needed
- [x] Installation guide
- [ ] API documentation
- [ ] Database schema documentation
- [ ] Deployment guide
- [ ] Monitoring guide
- [ ] Security guide
- [ ] Communication protocol guide

## Integration with Edge Devices

### Communication Protocols

#### 1. Real-time Communication
- **WebSocket:** สำหรับ real-time updates และ streaming
- **MQTT:** สำหรับ reliable message queuing และ pub/sub

#### 2. Request-Response Communication
- **REST API:** สำหรับ CRUD operations และ configuration

#### 3. File Transfer
- **SFTP:** สำหรับ secure file transfer
- **rsync:** สำหรับ efficient file synchronization

### Data Flow
1. Edge device captures image
2. AI processing on Edge
3. Results sent via Unified Communication Gateway
4. Server processes และ stores data
5. Dashboard updates in real-time
6. File transfer via SFTP/rsync

### Protocol Selection
- **Auto-selection:** ระบบเลือก protocol ที่เหมาะสมอัตโนมัติ
- **Priority-based:** เลือกตามความสำคัญของข้อมูล
- **Network-aware:** ปรับตามคุณภาพเครือข่าย
- **Fallback:** ใช้ protocol สำรองเมื่อหลักล้มเหลว

## Database Schema

### Core Tables
```sql
-- LPR Events
CREATE TABLE lpr_events (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(50) UNIQUE NOT NULL,
    edge_device_id VARCHAR(50) NOT NULL,
    license_plate VARCHAR(20),
    confidence DECIMAL(5,4),
    image_path VARCHAR(255),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Edge Devices
CREATE TABLE edge_devices (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(50) UNIQUE NOT NULL,
    hostname VARCHAR(100),
    ip_address INET,
    status VARCHAR(20) DEFAULT 'active',
    last_seen TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Communication Logs
CREATE TABLE communication_logs (
    id SERIAL PRIMARY KEY,
    protocol VARCHAR(20) NOT NULL,
    source VARCHAR(50) NOT NULL,
    destination VARCHAR(50) NOT NULL,
    message_type VARCHAR(50),
    success BOOLEAN,
    latency_ms INTEGER,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API Endpoints

### REST API
```python
# Health Check
GET /api/health

# LPR Events
GET /api/lpr/events
POST /api/lpr/events
GET /api/lpr/events/{event_id}
PUT /api/lpr/events/{event_id}
DELETE /api/lpr/events/{event_id}

# Edge Devices
GET /api/devices
GET /api/devices/{device_id}
POST /api/devices
PUT /api/devices/{device_id}

# Communication
GET /api/communication/stats
GET /api/communication/logs
```

### WebSocket Events
```python
# Connection Events
'connect'
'disconnect'

# LPR Events
'lpr_event_received'
'lpr_event_processed'
'lpr_event_error'

# System Events
'system_status'
'device_status'
'communication_status'
```

### MQTT Topics
```python
# LPR Data
'lpr/data/edge/{device_id}'
'lpr/data/processed'
'lpr/data/error'

# System Control
'system/control/{device_id}'
'system/status/{device_id}'

# File Transfer
'file/transfer/request'
'file/transfer/status'
```

## Security Implementation

### Authentication
- **JWT-based authentication**
- **API key authentication**
- **Role-based access control**

### Encryption
- **TLS/SSL for all communications**
- **Data encryption at rest**
- **Secure file transfer**

### Network Security
- **Tailscale VPN**
- **Firewall configuration**
- **Rate limiting**

## Monitoring และ Analytics

### Performance Metrics
- **API response times**
- **Database query performance**
- **Communication protocol statistics**
- **System resource usage**

### Alerting
- **Error rate monitoring**
- **System health checks**
- **Communication failures**
- **Storage capacity alerts**

## Deployment

### System Requirements
- **CPU:** 4+ cores
- **RAM:** 8GB+ (16GB recommended)
- **Storage:** 100GB+ SSD
- **Network:** Stable internet connection

### Environment Setup
```bash
# Install dependencies
sudo apt update
sudo apt install python3.10 python3.10-venv postgresql nginx

# Setup virtual environment
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure PostgreSQL
sudo -u postgres createdb lpr_server
sudo -u postgres createuser lpr_user

# Setup systemd service
sudo cp deployment/lpr-server.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable lpr-server
```

## Next Steps

### Phase 1: Core Infrastructure
1. **Database Setup** - ติดตั้งและ configure PostgreSQL
2. **API Development** - พัฒนา REST API endpoints
3. **Communication Gateway** - Implement Unified Communication Gateway
4. **Basic Frontend** - สร้าง web dashboard พื้นฐาน

### Phase 2: Advanced Features
1. **LPR Integration** - เชื่อมต่อ LPR processing
2. **Real-time Updates** - Implement WebSocket และ MQTT
3. **File Management** - Setup SFTP และ rsync
4. **Security Implementation** - เพิ่ม authentication และ encryption

### Phase 3: Production Ready
1. **Performance Optimization** - ปรับปรุงประสิทธิภาพ
2. **Monitoring Setup** - ติดตั้ง monitoring และ alerting
3. **Backup System** - สร้างระบบ backup และ recovery
4. **Documentation** - เขียนเอกสารครบถ้วน

---

**Note:** เอกสารนี้จะได้รับการอัปเดตตามความคืบหน้าของการพัฒนา LPR Server
