# Shared Documentation

**Version:** 1.0.0  
**Last Updated:** 2024-08-16  
**Author:** AI Camera Team  
**Status:** Active

## Overview

เอกสารที่แชร์ระหว่าง Edge Device และ LPR Server สำหรับการพัฒนาร่วมกันและการใช้งานระบบ

## 📋 Documentation Index

### 🔧 Configuration & Setup
- **[Tailscale Setup](tailscale-setup.md)** - การตั้งค่า Tailscale VPN สำหรับการเชื่อมต่อระหว่าง Edge และ Server
- **[Tailscale ACLs](tailscale-acls.json)** - ไฟล์ ACLs configuration มาตรฐาน
- **[Tailscale ACLs Fixed](tailscale-acls-fixed.json)** - ไฟล์ ACLs ที่แก้ไขแล้วพร้อม SSH access

### 🏗️ Architecture & Communication
- **[Unified Communication Architecture](unified-communication-architecture.md)** - สถาปัตยกรรมการสื่อสารแบบรวมที่รองรับ WebSocket, REST API, MQTT, SFTP, rsync

### 📚 Development Guidelines
- **[Development Guidelines](development-guidelines.md)** - แนวทางการพัฒนาร่วมกันระหว่าง Edge และ Server

## 🎯 Quick Start

### สำหรับการตั้งค่าเครือข่าย
1. **[Tailscale Setup](tailscale-setup.md)** - ติดตั้งและตั้งค่า Tailscale VPN
2. **[Tailscale ACLs](tailscale-acls-fixed.json)** - กำหนดสิทธิ์การเข้าถึง

### สำหรับการพัฒนา
1. **[Development Guidelines](development-guidelines.md)** - อ่านแนวทางการพัฒนา
2. **[Unified Communication Architecture](unified-communication-architecture.md)** - เข้าใจสถาปัตยกรรมการสื่อสาร

## 🔗 Cross-References

### Edge Device Documentation
- **[Edge Project Overview](../edge/project-overview.md)** - ภาพรวมโปรเจค Edge
- **[Edge API Reference](../edge/api-reference.md)** - API documentation สำหรับ Edge
- **[Edge Dashboard Improvements](../edge/dashboard-improvements.md)** - การปรับปรุง dashboard

### Server Documentation
- **[Server Documentation](../server/README.md)** - เอกสาร LPR Server
- **[Server API Endpoints](../server/README.md#api-endpoints)** - API endpoints สำหรับ Server

## 🏗️ System Architecture

### Network Topology
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Edge Device   │    │   LPR Server    │    │  Development    │
│  (Raspberry Pi) │◄──►│   (Ubuntu)      │◄──►│   Machine       │
│   aicamera1     │    │   lprserver     │    │   dev-machine   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Tailscale     │
                    │   Network       │
                    └─────────────────┘
```

### Communication Protocols
- **WebSocket:** Real-time data streaming
- **REST API:** HTTP communication
- **MQTT:** Message queuing
- **SFTP:** Secure file transfer
- **rsync:** File synchronization

## 📊 Development Workflow

### Git Workflow
```
main
├── develop
│   ├── feature/edge-camera-improvements
│   ├── feature/server-api-enhancements
│   ├── feature/unified-communication
│   └── hotfix/critical-bug-fix
└── release/v1.3.1
```

### Code Standards
- **Python:** PEP 8 with Black formatter
- **Documentation:** Google-style docstrings
- **Testing:** 90%+ coverage requirement
- **API:** RESTful design with consistent response format

## 🔒 Security Considerations

### Network Security
- **Tailscale VPN** - เชื่อมต่อทุกเครื่องอย่างปลอดภัย
- **ACLs Configuration** - ควบคุมการเข้าถึงระหว่างเครื่อง
- **Firewall Rules** - ตั้งค่าความปลอดภัย

### Application Security
- **JWT Authentication** - สำหรับ API access
- **Data Validation** - ตรวจสอบข้อมูล input
- **Encryption** - เข้ารหัสข้อมูลที่สำคัญ

## 📈 Monitoring and Logging

### System Monitoring
- **Communication Metrics** - ติดตามประสิทธิภาพการสื่อสาร
- **Protocol Statistics** - สถิติการใช้ protocol ต่างๆ
- **Error Tracking** - ติดตาม errors และ exceptions

### Logging Standards
- **Structured Logging** - JSON format logs
- **Performance Monitoring** - ติดตาม execution time
- **Event Tracking** - บันทึก events ที่สำคัญ

## 🚀 Deployment

### Environment Configuration
```yaml
# communication_config.yaml
websocket:
  server_url: "ws://lprserver:8765"
  reconnect_attempts: 3
  reconnect_delay: 5

rest:
  base_url: "http://lprserver:8000"
  timeout: 30
  retry_attempts: 3

mqtt:
  broker_url: "lprserver"
  client_id: "aicamera-edge-001"
  username: "edge_user"
  password: "secure_password"

sftp:
  host: "lprserver"
  username: "edge_user"
  key_file: "/home/camuser/.ssh/id_rsa"
  remote_path: "/data/lpr_images"

rsync:
  remote_host: "lprserver"
  remote_user: "edge_user"
  remote_path: "/data/lpr_images"
  options: ["-azP", "--delete"]
```

### System Requirements
- **Edge Device:** Raspberry Pi 5 (ARM64), 4GB+ RAM
- **Server:** Ubuntu Server, 8GB+ RAM, PostgreSQL 14+
- **Network:** Stable internet connection for Tailscale

## 📚 References

### External Resources
- [Tailscale Documentation](https://tailscale.com/kb/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)

### Project Resources
- **[Main Project Documentation](../../../docs/README.md)** - เอกสารหลักของโปรเจค
- **[Installation Guides](../../../installation/)** - คู่มือการติดตั้ง
- **[Setup Guides](../../../setup/)** - คู่มือการตั้งค่า

---

**Note:** เอกสารนี้จะได้รับการอัปเดตเมื่อมีการเปลี่ยนแปลงในระบบหรือเพิ่มเอกสารใหม่
