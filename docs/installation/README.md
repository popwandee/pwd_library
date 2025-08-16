# Installation Guide - Overview

**Version:** 1.0.0  
**Last Updated:** 2024-08-16  
**Author:** Edge AI Team  
**Category:** Installation  
**Status:** Active

## Overview

คู่มือการติดตั้งสำหรับระบบ Edge AI ที่ครอบคลุมการติดตั้งบนเครื่องต่างๆ และการตั้งค่าที่จำเป็น

## 📋 Installation Categories

### Platform-Specific Installation
- **[Edge Device Installation](edge/README.md)** - การติดตั้งบน Raspberry Pi + Hailo
- **[Server Installation](server/README.md)** - การติดตั้งบน Ubuntu Server
- **[Development Machine Installation](dev/README.md)** - การติดตั้งบนเครื่องพัฒนา

### Setup and Configuration
- **[Tailscale Setup](../setup/tailscale/README.md)** - การตั้งค่า Tailscale VPN
- **[WebSocket Setup](../setup/websocket/README.md)** - การตั้งค่า WebSocket communication
- **[REST API Setup](../setup/rest-api/README.md)** - การตั้งค่า REST API
- **[MQTT Setup](../setup/mqtt/README.md)** - การตั้งค่า MQTT messaging
- **[Security Setup](../setup/security/README.md)** - การตั้งค่าความปลอดภัย

## 🚀 Quick Start

### For New Users
1. **Edge Device**: เริ่มจาก [Edge Installation](edge/README.md)
2. **Server**: ตามด้วย [Server Installation](server/README.md)
3. **Development**: ตั้งค่า [Development Environment](dev/README.md)

### For Existing Users
1. **Tailscale**: ตั้งค่า [Tailscale VPN](../setup/tailscale/README.md)
2. **Communication**: ตั้งค่า [WebSocket](../setup/websocket/README.md) และ [REST API](../setup/rest-api/README.md)
3. **Security**: ตรวจสอบ [Security Configuration](../setup/security/README.md)

## 📊 System Requirements

### Edge Device (Raspberry Pi 5)
- **Hardware:** Raspberry Pi 5 (ARM64)
- **OS:** Raspberry Pi OS (Brookwarm)
- **RAM:** 4GB+ (8GB recommended)
- **Storage:** 32GB+ microSD card
- **AI Accelerator:** Hailo-8

### Server (Ubuntu)
- **Hardware:** Ubuntu Server
- **OS:** Ubuntu 22.04+/24.04 LTS
- **RAM:** 8GB+ (16GB recommended)
- **Storage:** 100GB+ SSD
- **Database:** PostgreSQL

### Development Machine
- **OS:** Windows 10/11, macOS, หรือ Linux
- **RAM:** 8GB+ (16GB recommended)
- **Storage:** 50GB+ free space
- **Tools:** Git, Python 3.10+, IDE

## 🔧 Prerequisites

### Common Requirements
- **Internet Connection** - สำหรับการดาวน์โหลดและติดตั้ง
- **Git** - สำหรับ version control
- **SSH Access** - สำหรับการเข้าถึง remote machines
- **Tailscale Account** - สำหรับ VPN connectivity

### Platform-Specific Requirements
- **Edge:** Hailo TAPPAS, PiCamera2
- **Server:** PostgreSQL, Nginx, Docker (optional)
- **Development:** VS Code/PyCharm, Postman

## 📝 Installation Checklist

### Edge Device
- [ ] System preparation
- [ ] Python environment setup
- [ ] Hailo TAPPAS installation
- [ ] Camera configuration
- [ ] Service setup
- [ ] Network configuration

### Server
- [ ] System preparation
- [ ] Database installation
- [ ] Web framework setup
- [ ] Service configuration
- [ ] Security hardening
- [ ] Monitoring setup

### Development Machine
- [ ] Development tools installation
- [ ] Python environment setup
- [ ] IDE configuration
- [ ] Git setup
- [ ] Testing tools setup

## 🔗 Cross-Platform Setup

### Network Configuration
- **Tailscale VPN** - เชื่อมต่อทุกเครื่องเข้าด้วยกัน
- **Firewall Rules** - ตั้งค่าความปลอดภัย
- **DNS Configuration** - การตั้งค่า hostname resolution

### Communication Setup
- **REST API** - HTTP communication
- **WebSocket** - Real-time communication
- **MQTT** - Lightweight messaging

### Security Configuration
- **Authentication** - User authentication
- **Authorization** - Access control
- **Encryption** - Data encryption
- **Monitoring** - Security monitoring

## 🛠️ Troubleshooting

### Common Issues
- **Network Connectivity** - ตรวจสอบ Tailscale status
- **Service Startup** - ตรวจสอบ systemd services
- **Permission Issues** - ตรวจสอบ file permissions
- **Dependency Conflicts** - ตรวจสอบ Python packages

### Platform-Specific Issues
- **Edge:** Camera detection, Hailo device issues
- **Server:** Database connection, service conflicts
- **Development:** IDE configuration, environment issues

## 📚 References

### Official Documentation
- [Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/)
- [Ubuntu Documentation](https://ubuntu.com/tutorials)
- [Hailo TAPPAS Documentation](https://hailo.ai/developer-zone/)
- [Tailscale Documentation](https://tailscale.com/kb/)

### Community Resources
- [Raspberry Pi Forums](https://www.raspberrypi.org/forums/)
- [Ubuntu Forums](https://ubuntuforums.org/)
- [Stack Overflow](https://stackoverflow.com/)

---

**Note:** เอกสารนี้เป็น overview สำหรับการติดตั้งระบบ Edge AI
