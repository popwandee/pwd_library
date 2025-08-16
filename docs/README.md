# PWD Library - Documentation

**Version:** 2.0.0  
**Last Updated:** 2024-08-16  
**Author:** PWD Library Team  
**Status:** Active

## Overview

PWD Library เป็นคลังความรู้และเอกสารทั่วไปสำหรับการพัฒนา Edge AI systems โดยเฉพาะสำหรับ Raspberry Pi และ Hailo AI accelerator

## 📁 Documentation Structure

```
docs/
├── installation/                # คู่มือการติดตั้ง
│   ├── README.md               # Installation Overview
│   ├── edge/                   # Edge Device Installation
│   │   └── README.md           # Raspberry Pi + Hailo Setup
│   ├── server/                 # Server Installation
│   │   └── README.md           # Ubuntu Server Setup
│   └── dev/                    # Development Machine Installation
│       └── README.md           # Windows/Mac/Linux Dev Setup
├── setup/                      # การตั้งค่าและ Configuration
│   ├── README.md               # Setup Overview
│   ├── tailscale/              # Tailscale VPN Setup
│   │   └── README.md           # Complete Tailscale Guide
│   ├── websocket/              # WebSocket Setup
│   │   └── README.md           # (To be created)
│   ├── rest-api/               # REST API Setup
│   │   └── README.md           # (To be created)
│   ├── mqtt/                   # MQTT Setup
│   │   └── README.md           # (To be created)
│   └── security/               # Security Setup
│       └── README.md           # (To be created)
├── guides/                     # คู่มือทั่วไป
│   ├── installation.md         # General Installation Guide
│   └── development.md          # Development Guide
├── reference/                  # เอกสารอ้างอิงทั่วไป
│   └── tailscale-acls-reference.md # Tailscale ACLs Reference
├── monitoring/                 # การติดตามระบบทั่วไป
│   └── monitoring.md           # System Monitoring Guide
├── deployment/                 # การ deploy ทั่วไป
│   └── tailscale-setup.sh      # Tailscale Setup Script
├── projects/                   # Project-specific documentation
│   ├── ai_camera/              # AI Camera project docs
│   └── lpr_server/             # LPR Server project docs
├── development/                # Development tools & practices
│   ├── cursor/                 # Cursor AI documentation
│   ├── git/                    # Git workflow & practices
│   └── docker/                 # Docker & deployment
├── knowledge/                  # Technical knowledge base
│   ├── hardware/               # Hardware & sensors
│   ├── ai_vision/              # AI & computer vision
│   ├── network/                # Network & communication
│   └── system/                 # System administration
├── tutorials/                  # Tutorials & examples
│   ├── getting_started/        # Getting started guides
│   ├── examples/               # Code examples
│   └── best_practices/         # Best practices
├── camera/                     # Camera-related documentation
├── docker/                     # Docker documentation
├── gstreamer/                  # GStreamer documentation
├── hailo_ai_vision/            # Hailo AI Vision documentation
├── images/                     # Documentation images
├── linux_commands/             # Linux commands reference
├── network/                    # Network documentation
├── picamer2/                   # PiCamera2 documentation
├── python/                     # Python documentation
├── rpicam/                     # RPi Camera documentation
├── sql/                        # SQL documentation
└── README.md                   # This file
```

## 🚀 Quick Start

### For New Users
1. **[Installation Overview](installation/README.md)** - เริ่มต้นที่นี่เพื่อเข้าใจการติดตั้ง
2. **[Edge Device Installation](installation/edge/README.md)** - ติดตั้ง Raspberry Pi + Hailo
3. **[Server Installation](installation/server/README.md)** - ติดตั้ง Ubuntu Server
4. **[Development Setup](installation/dev/README.md)** - ตั้งค่าเครื่องพัฒนา

### For Setup and Configuration
1. **[Setup Overview](setup/README.md)** - ภาพรวมการตั้งค่าทุกเทคโนโลยี
2. **[Tailscale Setup](setup/tailscale/README.md)** - ตั้งค่า Tailscale VPN
3. **[WebSocket Setup](setup/websocket/README.md)** - ตั้งค่า WebSocket (รอสร้าง)
4. **[REST API Setup](setup/rest-api/README.md)** - ตั้งค่า REST API (รอสร้าง)
5. **[MQTT Setup](setup/mqtt/README.md)** - ตั้งค่า MQTT (รอสร้าง)
6. **[Security Setup](setup/security/README.md)** - ตั้งค่าความปลอดภัย (รอสร้าง)

### For General Knowledge
1. **[General Installation Guide](guides/installation.md)** - คู่มือการติดตั้งทั่วไป
2. **[Development Guide](guides/development.md)** - แนวทางการพัฒนา
3. **[Tailscale ACLs Reference](reference/tailscale-acls-reference.md)** - อ้างอิง ACLs
4. **[System Monitoring Guide](monitoring/monitoring.md)** - การติดตามระบบ
5. **[Tailscale Setup Script](deployment/tailscale-setup.sh)** - สคริปต์ตั้งค่า Tailscale

## 📋 Documentation Categories

### 🔧 Installation Guides
คู่มือการติดตั้งแยกตาม platform และ use case

- **[Installation Overview](installation/README.md)** - ภาพรวมการติดตั้งทุก platform
- **[Edge Device Installation](installation/edge/README.md)** - Raspberry Pi + Hailo setup
- **[Server Installation](installation/server/README.md)** - Ubuntu Server setup
- **[Development Installation](installation/dev/README.md)** - Development machine setup

### ⚙️ Setup and Configuration
คู่มือการตั้งค่าและ configuration สำหรับเทคโนโลยีต่างๆ

- **[Setup Overview](setup/README.md)** - ภาพรวมการตั้งค่าทุกเทคโนโลยี
- **[Tailscale Setup](setup/tailscale/README.md)** - การตั้งค่า Tailscale VPN
- **[WebSocket Setup](setup/websocket/README.md)** - การตั้งค่า WebSocket communication
- **[REST API Setup](setup/rest-api/README.md)** - การตั้งค่า REST API
- **[MQTT Setup](setup/mqtt/README.md)** - การตั้งค่า MQTT messaging
- **[Security Setup](setup/security/README.md)** - การตั้งค่าความปลอดภัย

### 🎯 Project-Specific Documentation
เอกสารเฉพาะโปรเจค

- **[AI Camera Project](projects/ai_camera/)** - เอกสารเฉพาะโปรเจค AI Camera
- **[LPR Server Project](projects/lpr_server/)** - เอกสารเฉพาะโปรเจค LPR Server

### 🛠️ Development Tools & Practices
เครื่องมือการพัฒนาและแนวทางปฏิบัติ

- **[Cursor AI Development](development/cursor/)** - คู่มือการใช้งาน Cursor AI
- **[Git Workflow](development/git/)** - แนวทางการใช้งาน Git
- **[Docker & Deployment](development/docker/)** - การใช้งาน Docker และการ Deploy

### 🔧 Technical Knowledge Base
ความรู้ทางเทคนิค

- **[Hardware & Sensors](knowledge/hardware/)** - ข้อมูลฮาร์ดแวร์และเซ็นเซอร์
- **[AI & Computer Vision](knowledge/ai_vision/)** - ความรู้ด้าน AI และ Computer Vision
- **[Network & Communication](knowledge/network/)** - โปรโตคอลการสื่อสารและเครือข่าย
- **[System Administration](knowledge/system/)** - การจัดการระบบและ Linux

### 📖 Tutorials & Examples
คู่มือและตัวอย่าง

- **[Getting Started](tutorials/getting_started/)** - คู่มือเริ่มต้นใช้งาน
- **[Code Examples](tutorials/examples/)** - ตัวอย่างโค้ดและการใช้งาน
- **[Best Practices](tutorials/best_practices/)** - แนวปฏิบัติที่ดี

### 📚 General Guides
คู่มือทั่วไปสำหรับการพัฒนาและใช้งาน

- **[General Installation Guide](guides/installation.md)** - คู่มือการติดตั้งทั่วไป
- **[Development Guide](guides/development.md)** - แนวทางการพัฒนา

### 🔍 Reference Documentation
เอกสารอ้างอิงทางเทคนิค

- **[Tailscale ACLs Reference](reference/tailscale-acls-reference.md)** - อ้างอิง ACLs configuration
- **[Hailo World](001_hailo_world.md)** - Getting started with Hailo
- **[Object Detection](002_object_detection.md)** - Object detection with Hailo
- **[Simplified Object Detection](003_simplified_object_detection.md)** - Simplified approach
- **[Segmentation Example](004_segmentation_example.md)** - Image segmentation
- **[Docker Guide](005_docker.md)** - Docker usage

### 📊 Monitoring and Operations
การติดตามและจัดการระบบ

- **[System Monitoring Guide](monitoring/monitoring.md)** - การติดตามระบบทั่วไป
- **[Tailscale Setup Script](deployment/tailscale-setup.sh)** - สคริปต์ตั้งค่า Tailscale

### 🚀 Deployment
การ deploy และการจัดการระบบ

- **[Deployment Guide](deployment/)** - คู่มือการ deploy
- **[Docker Documentation](docker/)** - Docker deployment
- **[Git Documentation](git/)** - Version control

### 📷 Camera and Vision
การใช้งานกล้องและ computer vision

- **[Camera Documentation](camera/)** - Camera setup and usage
- **[PiCamera2 Documentation](picamer2/)** - PiCamera2 usage
- **[RPi Camera Documentation](rpicam/)** - RPi Camera documentation
- **[GStreamer Documentation](gstreamer/)** - GStreamer pipeline

### 🤖 AI and Machine Learning
AI และ machine learning

- **[Hailo AI Vision](hailo_ai_vision/)** - Hailo AI Vision documentation
- **[Basic Pipelines](basic-pipelines.md)** - Basic AI pipelines
- **[Model Performance Testing](HowToTestModelPerformance.md)** - Testing model performance
- **[Retraining Example](retraining-example.md)** - Model retraining

### 💻 Development Tools
เครื่องมือการพัฒนา

- **[Python Documentation](python/)** - Python development
- **[Linux Commands](linux_commands/)** - Linux command reference
- **[Network Documentation](network/)** - Network configuration
- **[SQL Documentation](sql/)** - Database operations

## 🔗 Cross-References

### Project-Specific Documentation
- **[AI Camera Edge System Documentation](../../docs/README.md)** - เอกสารเฉพาะโปรเจค

### External Resources
- [Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/)
- [Hailo TAPPAS Documentation](https://hailo.ai/developer-zone/)
- [Tailscale Documentation](https://tailscale.com/kb/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Ubuntu Documentation](https://ubuntu.com/tutorials)

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

## 📝 Contributing

### Guidelines
1. **Version Control:** ทุกเอกสารต้องมี version และวันที่อัปเดต
2. **Structure:** ใช้โครงสร้างที่กำหนดไว้
3. **Language:** ใช้ภาษาไทยสำหรับคำอธิบาย ภาษาอังกฤษสำหรับ code
4. **Format:** ใช้ Markdown format
5. **Links:** เชื่อมโยงเอกสารที่เกี่ยวข้อง

### Template for New Documents
```markdown
# Document Title

**Version:** X.X.X  
**Last Updated:** YYYY-MM-DD  
**Author:** Author Name  
**Category:** Category Name  
**Status:** Active/Draft/Deprecated

## Table of Contents

1. [Section 1](#section-1)
2. [Section 2](#section-2)

## Section 1

Content here...

## Section 2

Content here...

## References

- [Reference 1](link1)
- [Reference 2](link2)

---

**Note:** Additional notes or warnings
```

## 🔄 Documentation Maintenance

### การอัพเดทเอกสาร
- เอกสารจะถูกอัพเดทเมื่อมีการเปลี่ยนแปลงในโค้ด
- ใช้ [Git Workflow](development/git/01_workflow.md) สำหรับการอัพเดท
- ทดสอบเอกสารก่อนเผยแพร่

### การแจ้งปัญหา
- หากพบข้อผิดพลาดในเอกสาร กรุณาแจ้งผ่าน Issue
- ใช้ template "Documentation Bug" สำหรับรายงานปัญหา

## 📞 Support

- **Technical Issues**: ดู [Troubleshooting Guide](reference/troubleshooting/01_common_issues.md)
- **Development Questions**: อ่าน [Development FAQ](reference/faq/01_development.md)
- **Hardware Issues**: ดู [Hardware Troubleshooting](knowledge/hardware/05_troubleshooting.md)

## 📚 References

### Official Documentation
- [Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/)
- [Hailo TAPPAS Documentation](https://hailo.ai/developer-zone/)
- [Tailscale Documentation](https://tailscale.com/kb/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Ubuntu Documentation](https://ubuntu.com/tutorials)

### Community Resources
- [Raspberry Pi Forums](https://www.raspberrypi.org/forums/)
- [Hailo Community](https://hailo.ai/community/)
- [Tailscale Community](https://tailscale.com/community/)

---

**Note:** เอกสารนี้เป็นคลังความรู้ทั่วไปสำหรับการพัฒนา Edge AI systems
