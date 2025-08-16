# Cursor AI Development Basics

**คู่มือการใช้งาน Cursor AI สำหรับการพัฒนาโปรเจกต์ IoT แบบ Multi-Machine**

> **หมายเหตุ**: เอกสารนี้เป็นส่วนหนึ่งของ [Cursor AI Development Documentation](./README.md)

## 🎯 **Overview**

คู่มือนี้ครอบคลุมการใช้งาน Cursor AI สำหรับการพัฒนาโปรเจกต์ IoT ที่มี Edge Device (Raspberry Pi) และ Server Device (Ubuntu) เชื่อมต่อผ่าน Tailscale VPN

## 🏗️ **Development Architecture**

```
Development Environment:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Your Machine  │    │  Edge Device    │    │  Server Device  │
│   (Windows/Mac/ │◄──►│  (Raspberry Pi) │◄──►│   (Ubuntu)      │
│    Linux)       │    │  aicamera.git   │    │  lprserver_v3.git│
│   Cursor AI     │    │  [Tailscale IP] │    │  [Tailscale IP] │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## ⚙️ **Cursor Configuration**

### **1. Basic Settings Setup**

สร้างไฟล์ `~/.config/Cursor/User/settings.json`:

```json
{
  "workbench.colorTheme": "Default Dark+",
  "editor.fontSize": 14,
  "terminal.integrated.fontSize": 12,
  
  // Network and Connection Settings
  "http.proxySupport": "off",
  "http.proxyStrictSSL": false,
  "http.maxConcurrentRequests": 1,
  "http.maxRedirects": 5,
  
  // Cursor AI Settings
  "cursor.ai.enableTelemetry": false,
  "cursor.ai.enableAnalytics": false,
  "cursor.ai.enableCrashReporting": false,
  
  // Environment Variables
  "terminal.integrated.env.linux": {
    "DISABLE_HTTP2": "1",
    "CURL_VERBOSE": "0"
  },
  "terminal.integrated.env.osx": {
    "DISABLE_HTTP2": "1",
    "CURL_VERBOSE": "0"
  },
  "terminal.integrated.env.windows": {
    "DISABLE_HTTP2": "1",
    "CURL_VERBOSE": "0"
  },
  
  // Git Settings
  "git.enableSmartCommit": true,
  "git.autofetch": true,
  "git.confirmSync": false,
  
  // File Settings
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  
  // Python Settings
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.terminal.activateEnvironment": true,
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black"
}
```

### **2. Project-Specific Configuration**

**สำหรับ aicamera.git (.cursorrules):**
```json
{
  "name": "AI Camera Edge Development",
  "description": "Edge AI camera system with real-time processing for Raspberry Pi Bookworm",
  "rules": [
    "Focus on resource-constrained environments (Raspberry Pi 4/5)",
    "Optimize for low power consumption and thermal management",
    "Use lightweight libraries suitable for ARM64 architecture",
    "Implement efficient image processing pipelines with memory optimization",
    "Use async/await for non-blocking operations",
    "Implement robust error handling for hardware failures",
    "Use local caching for offline operation",
    "Implement graceful degradation when network is unavailable",
    "Optimize for real-time performance with minimal latency",
    "Use hardware acceleration when available (GPU, VPU)"
  ],
  "technologies": [
    "Python 3.9+",
    "OpenCV (opencv-python-headless)",
    "NumPy",
    "Paho-MQTT",
    "Picamera2",
    "Asyncio",
    "RPi.GPIO",
    "Adafruit CircuitPython libraries",
    "Pillow (PIL)",
    "Pydantic for data validation"
  ],
  "hardware": [
    "Raspberry Pi 4/5",
    "Raspberry Pi Camera Module v2/v3",
    "Hailo8 AI accelerator (optional)",
    "DHT22/AM2302 sensors",
    "PIR motion sensors"
  ],
  "architecture": {
    "pattern": "Event-driven with async processing",
    "communication": "MQTT for sensor data, HTTP for commands",
    "storage": "Local SQLite for caching, remote PostgreSQL for persistence"
  }
}
```

**สำหรับ lprserver_v3.git (.cursorrules):**
```json
{
  "name": "LPR Server Backend Development",
  "description": "License Plate Recognition server with API and database management",
  "rules": [
    "Design scalable microservices architecture with clear separation of concerns",
    "Implement RESTful APIs with proper authentication and authorization",
    "Use containerization (Docker) for deployment and scaling",
    "Focus on security and data privacy with input validation",
    "Implement comprehensive logging and monitoring",
    "Use connection pooling for database operations",
    "Implement caching strategies for performance optimization",
    "Design for horizontal scaling and load balancing",
    "Use message queues for async processing",
    "Implement proper error handling and circuit breakers"
  ],
  "technologies": [
    "Python 3.9+",
    "FastAPI",
    "SQLAlchemy",
    "PostgreSQL",
    "Redis",
    "Docker",
    "Pydantic",
    "Alembic for migrations",
    "Celery for background tasks",
    "JWT for authentication"
  ],
  "infrastructure": [
    "Ubuntu Server 20.04+",
    "Docker & Docker Compose",
    "Nginx reverse proxy",
    "PostgreSQL database",
    "Redis cache",
    "Tailscale VPN"
  ],
  "architecture": {
    "pattern": "Layered architecture with dependency injection",
    "communication": "REST API, WebSocket for real-time updates",
    "storage": "PostgreSQL for main data, Redis for caching"
  }
}
```

## 🌐 **Tailscale Network Setup**

### **1. Network Configuration**

```bash
# Check Tailscale status
tailscale status

# Get device IPs
tailscale ip -4

# Test connectivity
ping [edge-device-tailscale-ip]
ping [server-device-tailscale-ip]
```

### **2. SSH Configuration**

สร้างไฟล์ `~/.ssh/config`:

```bash
Host edge-device
    HostName [edge-tailscale-ip]
    User pi
    Port 22
    IdentityFile ~/.ssh/id_rsa
    StrictHostKeyChecking no

Host server-device
    HostName [server-tailscale-ip]
    User ubuntu
    Port 22
    IdentityFile ~/.ssh/id_rsa
    StrictHostKeyChecking no
```

## 🚀 **Development Workflow**

### **1. Project Setup**

```bash
# Create project structure
mkdir ~/iot-projects
cd ~/iot-projects

# Clone repositories
git clone https://github.com/your-username/aicamera.git
git clone https://github.com/your-username/lprserver_v3.git

# Create virtual environments
cd aicamera && python3 -m venv venv
cd ../lprserver_v3 && python3 -m venv venv

# Install dependencies for Edge project
cd aicamera
source venv/bin/activate
pip install -r requirements.txt

# Install dependencies for Server project
cd ../lprserver_v3
source venv/bin/activate
pip install -r requirements.txt
```

### **2. Multi-Instance Cursor Setup**

```bash
# Open multiple Cursor instances for different projects
cursor ~/iot-projects/aicamera/  # Edge development
cursor ~/iot-projects/lprserver_v3/  # Server development

# Or use workspace files
cd ~/iot-projects
cursor aicamera.code-workspace
cursor lprserver_v3.code-workspace
```

### **3. Workspace Configuration**

**aicamera.code-workspace:**
```json
{
  "folders": [
    {
      "name": "AI Camera Edge",
      "path": "./aicamera"
    },
    {
      "name": "Shared Tools",
      "path": "./shared-tools"
    }
  ],
  "settings": {
    "python.defaultInterpreterPath": "./aicamera/venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "files.exclude": {
      "**/__pycache__": true,
      "**/*.pyc": true,
      "**/.pytest_cache": true
    }
  },
  "extensions": {
    "recommendations": [
      "ms-python.python",
      "ms-python.flake8",
      "ms-python.black-formatter"
    ]
  }
}
```

**lprserver_v3.code-workspace:**
```json
{
  "folders": [
    {
      "name": "LPR Server",
      "path": "./lprserver_v3"
    },
    {
      "name": "Shared Tools",
      "path": "./shared-tools"
    }
  ],
  "settings": {
    "python.defaultInterpreterPath": "./lprserver_v3/venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "files.exclude": {
      "**/__pycache__": true,
      "**/*.pyc": true,
      "**/.pytest_cache": true,
      "**/node_modules": true
    }
  },
  "extensions": {
    "recommendations": [
      "ms-python.python",
      "ms-python.flake8",
      "ms-python.black-formatter",
      "ms-vscode.vscode-json",
      "redhat.vscode-yaml"
    ]
  }
}
```

### **4. Environment Variables**

สร้างไฟล์ `.env.development`:

```bash
# Tailscale Network Configuration
EDGE_DEVICE_IP=100.64.0.1
SERVER_DEVICE_IP=100.64.0.2

# Edge Device Configuration
EDGE_MQTT_BROKER=$SERVER_DEVICE_IP
EDGE_MQTT_PORT=1883
EDGE_DEVICE_ID=ai_camera_001

# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
SERVER_DATABASE_URL=postgresql://user:pass@$SERVER_DEVICE_IP:5432/lpr_db
```

### **5. Development Scripts**

สร้างไฟล์ `scripts/dev-workflow.sh`:

```bash
#!/bin/bash

PROJECTS_DIR="$HOME/iot-projects"
AICAMERA_DIR="$PROJECTS_DIR/aicamera"
LPRSERVER_DIR="$PROJECTS_DIR/lprserver_v3"

# Load environment variables
source .env.development

case "$1" in
    "sync")
        echo "Syncing repositories..."
        cd "$AICAMERA_DIR" && git pull origin main
        cd "$LPRSERVER_DIR" && git pull origin main
        ;;
    "deploy-edge")
        echo "Deploying to edge device..."
        rsync -avz --exclude='venv' --exclude='__pycache__' "$AICAMERA_DIR/" "pi@$EDGE_DEVICE_IP:/opt/aicamera/"
        ;;
    "deploy-server")
        echo "Deploying to server device..."
        rsync -avz --exclude='venv' --exclude='__pycache__' "$LPRSERVER_DIR/" "ubuntu@$SERVER_DEVICE_IP:/opt/lprserver/"
        ;;
    *)
        echo "Usage: $0 {sync|deploy-edge|deploy-server}"
        exit 1
        ;;
esac
```

## 🛠️ **Cursor AI Best Practices**

### **1. Effective Prompting**

```markdown
# Good prompts for IoT development:

"Create a Python class for MQTT communication with error handling and reconnection logic"

"Implement an async image processing pipeline for Raspberry Pi camera with memory optimization"

"Design a FastAPI endpoint for receiving sensor data with validation and database storage"

"Create a Docker Compose setup for the LPR server with PostgreSQL and Redis"
```

### **2. Code Organization**

```python
# Recommended structure for edge devices:
edge_project/
├── src/
│   ├── sensors/
│   ├── communication/
│   ├── processing/
│   └── utils/
├── config/
├── tests/
├── requirements.txt
└── main.py

# Recommended structure for server:
server_project/
├── app/
│   ├── api/
│   ├── models/
│   ├── services/
│   └── utils/
├── migrations/
├── tests/
├── requirements.txt
└── main.py
```

### **3. Error Handling Patterns**

```python
# Edge device error handling
import asyncio
import logging
from typing import Optional

class EdgeDevice:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.retry_count = 0
        self.max_retries = 3
    
    async def safe_operation(self, operation, *args, **kwargs):
        """Execute operation with retry logic"""
        for attempt in range(self.max_retries):
            try:
                return await operation(*args, **kwargs)
            except Exception as e:
                self.logger.error(f"Operation failed (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise
```

## 🔧 **Troubleshooting**

### **1. Connection Issues**

```bash
# Test Tailscale connectivity
tailscale ping [device-ip]

# Check SSH connection
ssh -v [device-name]

# Test network ports
telnet [device-ip] 22
telnet [device-ip] 8000

# Check Tailscale status
tailscale status
tailscale ip -4
```

### **2. Cursor AI Issues**

```bash
# Reset Cursor settings
rm -rf ~/.config/Cursor/User/workspaceStorage
rm -rf ~/.config/Cursor/User/globalStorage

# Clear Cursor cache
rm -rf ~/.cache/Cursor

# Fix NGHTTP2_INTERNAL_ERROR
# Add to ~/.config/Cursor/User/settings.json:
{
  "http.proxySupport": "off",
  "http.proxyStrictSSL": false,
  "terminal.integrated.env.linux": {
    "DISABLE_HTTP2": "1"
  }
}
```

### **3. Development Environment Issues**

```bash
# Recreate virtual environments
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Check Python paths
which python
python -c "import sys; print(sys.path)"

# Fix permission issues
sudo chown -R $USER:$USER ~/iot-projects
chmod +x scripts/*.sh
```

### **4. Network and VPN Issues**

```bash
# Reset network stack (Ubuntu)
sudo systemctl restart NetworkManager
sudo systemd-resolve --flush-caches

# Reset network stack (Windows)
ipconfig /flushdns
netsh winsock reset

# Test VPN connectivity
tailscale ping [device-ip]
ping [device-ip]
```

### **5. Multi-Instance Issues**

```bash
# Check if multiple Cursor instances are running
ps aux | grep cursor

# Kill all Cursor processes if needed
pkill -f cursor

# Restart with specific workspace
cursor --new-window ~/iot-projects/aicamera/
cursor --new-window ~/iot-projects/lprserver_v3/
```

## 🚀 **Advanced Cursor Features**

### **1. AI Chat Commands**

```markdown
# Effective prompts for IoT development:

"Create a Python class for MQTT communication with automatic reconnection and exponential backoff"

"Implement an async image processing pipeline for Raspberry Pi camera with memory optimization and error handling"

"Design a FastAPI endpoint for receiving sensor data with Pydantic validation and database storage"

"Create a Docker Compose setup for the LPR server with PostgreSQL, Redis, and Nginx reverse proxy"

"Implement a health monitoring system for edge devices with CPU, memory, and network checks"

"Create a circuit breaker pattern for external service calls in Python"

"Design a caching strategy using Redis for API responses with TTL and invalidation"
```

### **2. Code Generation Templates**

```python
# Edge Device Template
# Use this prompt: "Generate a complete edge device class with sensor management, MQTT communication, and error handling"

class EdgeDevice:
    def __init__(self, device_id: str, config: dict):
        self.device_id = device_id
        self.config = config
        self.logger = logging.getLogger(f"edge.{device_id}")
        self.mqtt_client = None
        self.sensors = {}
        self.health_monitor = HealthMonitor()
    
    async def initialize(self):
        """Initialize device components"""
        await self._setup_sensors()
        await self._setup_mqtt()
        await self._start_monitoring()
    
    async def _setup_sensors(self):
        """Setup sensor interfaces"""
        # Implementation
        pass
    
    async def _setup_mqtt(self):
        """Setup MQTT communication"""
        # Implementation
        pass
    
    async def _start_monitoring(self):
        """Start health monitoring"""
        # Implementation
        pass
```

### **3. Debugging with Cursor AI**

```python
# Use these prompts for debugging:

"Debug this MQTT connection issue: [paste error message]"

"Analyze this performance bottleneck in the image processing pipeline"

"Find memory leaks in this async code"

"Optimize this database query for better performance"

"Review this code for security vulnerabilities"
```

## 📚 **Additional Resources**

- [Cursor AI Documentation](https://cursor.sh/docs)
- [Tailscale Documentation](https://tailscale.com/kb/)
- [Raspberry Pi Development](https://www.raspberrypi.org/documentation/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MQTT Protocol Guide](https://mqtt.org/documentation)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## 🔄 **Development Workflow Summary**

1. **Setup**: Configure Cursor settings and project structure
2. **Development**: Use multiple Cursor instances for Edge and Server
3. **Testing**: Implement automated tests and health checks
4. **Deployment**: Use scripts to deploy to Edge and Server devices
5. **Monitoring**: Monitor system health and performance
6. **Iteration**: Continuously improve based on feedback

---

**Next Steps**: อ่าน [Best Practices](./02_best_practices.md) สำหรับแนวปฏิบัติที่ดีในการพัฒนา
