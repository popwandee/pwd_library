# Edge Device Installation Guide

**Version:** 1.0.0  
**Last Updated:** 2024-08-16  
**Author:** Edge AI Team  
**Category:** Installation - Edge Device  
**Status:** Active

## Overview

คู่มือการติดตั้งสำหรับ Edge Device ที่ใช้ Raspberry Pi 5 พร้อม Hailo-8 AI accelerator

## 📋 Prerequisites

### Hardware Requirements
- **Raspberry Pi 5** (ARM64) - 4GB+ RAM (8GB recommended)
- **Hailo-8 AI accelerator** พร้อม USB cable
- **PiCamera2** หรือ USB camera
- **MicroSD card** (32GB+ recommended)
- **Power supply** (5V/3A recommended)
- **Cooling solution** (fan หรือ heatsink)

### Software Requirements
- **Raspberry Pi OS (Brookwarm)** - Debian-based
- **Python 3.10+**
- **Git**
- **Internet connection** สำหรับการติดตั้ง

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

# Check Hailo device
hailortcli fw-control identify
```

### Step 5: Install Python Dependencies

```bash
# Install requirements
pip install -r requirements.txt

# Install additional dependencies
pip install opencv-python-headless
pip install picamera2
pip install flask
pip install flask-socketio
pip install gunicorn
```

### Step 6: Configure Camera

```bash
# Enable camera interface
sudo raspi-config nonint do_camera 0

# Enable I2C interface (if needed)
sudo raspi-config nonint do_i2c 0

# Check camera devices
ls -la /dev/video*

# Test camera
vcgencmd get_camera

# Reboot to apply changes
sudo reboot
```

### Step 7: Setup Systemd Service

```bash
# Copy service file
sudo cp systemd_service/your_edge_service.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable your_edge_service.service
```

## ⚙️ Configuration

### Environment Configuration

สร้างไฟล์ `.env` ในโฟลเดอร์หลัก:

```bash
# Application Configuration
FLASK_ENV=production
FLASK_APP=edge_app.wsgi:app
PYTHONPATH=/path/to/your/edge/project

# Camera Configuration
CAMERA_DEVICE=/dev/video0
CAMERA_RESOLUTION=1920x1080
CAMERA_FPS=30

# AI Configuration
AI_MODEL_PATH=resources/models/
AI_CONFIDENCE_THRESHOLD=0.5
HAILO_DEVICE_ID=0

# Network Configuration
WEBSOCKET_PORT=8765
HTTP_PORT=5000
SERVER_HOST=lprserver
SERVER_PORT=8000

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/edge_app.log

# Performance Configuration
MAX_WORKERS=1
THREADS_PER_WORKER=4
```

### Camera Configuration

```bash
# Check camera capabilities
v4l2-ctl --device=/dev/video0 --list-formats-ext

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

### Performance Optimization

```bash
# Disable unnecessary services
sudo systemctl disable bluetooth
sudo systemctl disable avahi-daemon

# Optimize GPU memory
echo 'gpu_mem=128' | sudo tee -a /boot/config.txt

# Optimize CPU governor
echo 'GOVERNOR=performance' | sudo tee -a /etc/default/cpufrequtils

# Increase swap space (if needed)
sudo dphys-swapfile swapoff
sudo sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=2048/' /etc/dphys-swapfile
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

## 🔧 Verification

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

### Step 2: Test AI Models

```bash
# Test Hailo device
hailortcli fw-control identify

# Test model loading
python3 -c "
import hailo_platform
print('Hailo platform test successful')
"
```

### Step 3: Test Web Interface

```bash
# Start application
sudo systemctl start your_edge_service

# Check service status
sudo systemctl status your_edge_service

# Test web interface
curl http://localhost:5000/health
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
curl http://localhost:5000/api/camera/status
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Camera Not Found
```bash
# Check camera interface
sudo raspi-config nonint do_camera 0

# Check device permissions
sudo usermod -a -G video $USER

# Check camera devices
ls -la /dev/video*

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

# Check Hailo device
hailortcli fw-control identify
```

#### 3. High Temperature
```bash
# Check temperature
vcgencmd measure_temp

# Check thermal throttling
vcgencmd get_throttled

# Solutions:
# - Improve ventilation
# - Add cooling fan
# - Reduce CPU load
```

#### 4. Memory Issues
```bash
# Check memory usage
free -h

# Check memory pressure
cat /proc/pressure/memory

# Solutions:
# - Increase swap space
# - Optimize application memory usage
# - Reduce concurrent processes
```

### Diagnostic Commands

```bash
# System information
uname -a
cat /etc/os-release

# Hardware information
vcgencmd get_mem gpu
vcgencmd get_mem arm
vcgencmd measure_temp

# Network information
ip addr show
ip route show

# Process information
ps aux | grep python
ps aux | grep hailo

# Log files
tail -f logs/edge_app.log
sudo journalctl -f
```

## 📊 Performance Monitoring

### System Monitoring

```bash
# CPU usage
htop
top -p $(pgrep -d',' python)

# Memory usage
free -h
cat /proc/meminfo

# Temperature monitoring
watch -n 5 vcgencmd measure_temp

# Storage usage
df -h
du -sh /path/to/your/project/*
```

### Application Monitoring

```bash
# Service status
sudo systemctl status your_edge_service

# Service logs
sudo journalctl -u your_edge_service -f

# Application logs
tail -f logs/edge_app.log

# Performance metrics
curl http://localhost:5000/metrics
```

## 🔒 Security Configuration

### Firewall Setup

```bash
# Install UFW
sudo apt install ufw

# Configure firewall rules
sudo ufw allow 22/tcp
sudo ufw allow 5000/tcp
sudo ufw allow 8765/tcp
sudo ufw allow in on tailscale0
sudo ufw allow out on tailscale0

# Enable firewall
sudo ufw enable
```

### SSH Security

```bash
# Disable password authentication
sudo sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

# Restart SSH service
sudo systemctl restart ssh
```

## 📚 References

- [Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/)
- [Hailo TAPPAS Documentation](https://hailo.ai/developer-zone/)
- [PiCamera2 Documentation](https://picamera2.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Note:** เอกสารนี้เป็นคู่มือการติดตั้งสำหรับ Edge Device
