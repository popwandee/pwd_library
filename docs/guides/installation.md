# Raspberry Pi + Hailo Edge AI Installation Guide

**Version:** 1.0.0  
**Last Updated:** 2024-08-16  
**Author:** Edge AI Team  
**Category:** Setup & Installation  
**Status:** Active

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [System Requirements](#system-requirements)
3. [Installation Steps](#installation-steps)
4. [Configuration](#configuration)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

### Hardware Requirements
- **Raspberry Pi 5** (ARM64) สำหรับ Edge device
- **Hailo-8 AI accelerator** พร้อม USB cable
- **PiCamera2** หรือ USB camera
- **MicroSD card** (32GB+ recommended)
- **Power supply** (5V/3A recommended)

### Software Requirements
- **Raspberry Pi OS (Brookwarm)** - Debian-based
- **Python 3.10+**
- **Git**
- **Internet connection** สำหรับการติดตั้ง

## System Requirements

### Minimum Requirements
- **CPU:** ARM64 compatible
- **RAM:** 4GB
- **Storage:** 16GB free space
- **Network:** Ethernet หรือ WiFi

### Recommended Requirements
- **CPU:** ARM64 compatible
- **RAM:** 8GB
- **Storage:** 32GB+ SSD
- **Network:** Gigabit Ethernet

## Installation Steps

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
    cmake \
    pkg-config \
    libopencv-dev \
    libatlas-base-dev \
    libhdf5-dev \
    libhdf5-serial-dev \
    libatlas-base-dev \
    libjasper-dev \
    libqtcore4 \
    libqtgui4 \
    libqt4-test \
    libgstreamer1.0-0 \
    libgstreamer-plugins-base1.0-0 \
    libgtk-3-0 \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libatlas-base-dev \
    gfortran \
    libhdf5-dev \
    libhdf5-serial-dev \
    libhdf5-103 \
    libqtgui4 \
    libqtwebkit4 \
    libqt4-test \
    python3-pyqt5 \
    libgtk-3-dev \
    libcanberra-gtk3-module \
    libcanberra-gtk-module
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
python3 -m venv venv_hailo

# Activate virtual environment
source venv_hailo/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

### Step 4: Install Hailo TAPPAS

```bash
# Setup Hailo environment
source setup_env.sh

# Verify TAPPAS installation
pkg-config --modversion hailo-tappas-core
```

### Step 5: Install Python Dependencies

```bash
# Install requirements
pip install -r requirements.txt

# Install additional dependencies if needed
pip install opencv-python-headless
pip install picamera2
```

### Step 6: Configure Camera

```bash
# Enable camera interface
sudo raspi-config nonint do_camera 0

# Enable I2C interface (if needed)
sudo raspi-config nonint do_i2c 0

# Reboot to apply changes
sudo reboot
```

### Step 7: Setup Systemd Service

```bash
# Copy service file
sudo cp systemd_service/your_service.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable your_service.service
```

## Configuration

### Environment Configuration

สร้างไฟล์ `.env` ในโฟลเดอร์หลัก:

```bash
# Application Configuration
FLASK_ENV=production
FLASK_APP=your_app.wsgi:app
PYTHONPATH=/path/to/your/project

# Camera Configuration
CAMERA_DEVICE=/dev/video0
CAMERA_RESOLUTION=1920x1080
CAMERA_FPS=30

# AI Configuration
AI_MODEL_PATH=resources/models/
AI_CONFIDENCE_THRESHOLD=0.5

# Network Configuration
WEBSOCKET_PORT=8765
HTTP_PORT=5000

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/your_app.log
```

### Camera Configuration

ตรวจสอบการตั้งค่ากล้อง:

```bash
# Check camera devices
ls -la /dev/video*

# Test camera with v4l2-ctl
v4l2-ctl --list-devices

# Check camera capabilities
v4l2-ctl --device=/dev/video0 --list-formats-ext
```

### Network Configuration

```bash
# Configure static IP (optional)
sudo tee -a /etc/dhcpcd.conf <<EOF
interface eth0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=8.8.8.8 8.8.4.4
EOF
```

## Verification

### Step 1: Verify Installation

```bash
# Check Python environment
python3 --version
pip list | grep -E "(opencv|hailo|flask)"

# Check Hailo TAPPAS
pkg-config --modversion hailo-tappas-core

# Check camera
vcgencmd get_camera
```

### Step 2: Test Camera

```bash
# Test camera capture
python3 -c "
from picamera2 import Picamera2
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())
picam2.start()
print('Camera test successful')
picam2.stop()
"
```

### Step 3: Test AI Models

```bash
# Test Hailo device
hailortcli fw-control identify

# Test model loading (if models are available)
python3 -c "
import hailo_platform
print('Hailo platform test successful')
"
```

### Step 4: Test Web Interface

```bash
# Start application
sudo systemctl start your_service

# Check service status
sudo systemctl status your_service

# Test web interface
curl http://localhost:5000/health
```

## Troubleshooting

### Common Issues

#### 1. Camera Not Found
```bash
# Check camera interface
sudo raspi-config nonint do_camera 0

# Check device permissions
sudo usermod -a -G video $USER

# Reboot system
sudo reboot
```

#### 2. Hailo Device Not Detected
```bash
# Check USB connection
lsusb | grep Hailo

# Check device permissions
sudo usermod -a -G dialout $USER

# Restart Hailo service
sudo systemctl restart hailo-fw-updater
```

#### 3. Python Import Errors
```bash
# Activate virtual environment
source venv_hailo/bin/activate

# Reinstall packages
pip install --force-reinstall -r requirements.txt

# Check Python path
echo $PYTHONPATH
```

#### 4. Service Not Starting
```bash
# Check service logs
sudo journalctl -u your_service -f

# Check file permissions
ls -la /path/to/your/project/

# Check environment variables
sudo systemctl show your_service
```

### Diagnostic Commands

```bash
# System information
uname -a
cat /etc/os-release

# Hardware information
vcgencmd get_mem gpu
vcgencmd get_mem arm

# Network information
ip addr show
ip route show

# Process information
ps aux | grep python
ps aux | grep hailo

# Log files
tail -f logs/your_app.log
sudo journalctl -f
```

## Post-Installation

### Performance Optimization

```bash
# Disable unnecessary services
sudo systemctl disable bluetooth
sudo systemctl disable avahi-daemon

# Optimize GPU memory
echo 'gpu_mem=128' | sudo tee -a /boot/config.txt

# Optimize CPU governor
echo 'GOVERNOR=performance' | sudo tee -a /etc/default/cpufrequtils
```

### Security Hardening

```bash
# Update firewall rules
sudo ufw allow 22/tcp
sudo ufw allow 5000/tcp
sudo ufw allow 8765/tcp
sudo ufw enable

# Disable password authentication for SSH
sudo sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart ssh
```

### Monitoring Setup

```bash
# Install monitoring tools
sudo apt install -y htop iotop nethogs

# Setup log rotation
sudo tee /etc/logrotate.d/your_app <<EOF
/path/to/your/project/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 $USER $USER
}
EOF
```

## References

- [Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/)
- [Hailo TAPPAS Documentation](https://hailo.ai/developer-zone/)
- [PiCamera2 Documentation](https://picamera2.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Note:** เอกสารนี้เป็นแนวทางทั่วไปสำหรับการติดตั้ง Raspberry Pi + Hailo Edge AI system
