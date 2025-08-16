# Development Best Practices

**แนวปฏิบัติที่ดีสำหรับการพัฒนาโปรเจกต์ IoT แบบ Multi-Machine**

## 🎯 **Core Development Principles**

### **1. Separation of Concerns**
- แยก Edge และ Server development ให้ชัดเจน
- ใช้ .cursorrules ที่เหมาะสมสำหรับแต่ละโปรเจกต์
- จัดการ dependencies แยกกัน

### **2. Code Organization**
- ใช้โครงสร้างโปรเจกต์ที่เป็นมาตรฐาน
- แยก business logic จาก infrastructure code
- ใช้ dependency injection pattern

### **3. Development Efficiency**
- ใช้ templates และ snippets
- Automate deployment และ testing
- Maintain consistent code style

## 🏗️ **Project Structure Best Practices**

### **1. Repository Organization**

```
iot-projects/
├── aicamera/                    # Edge Device Repository
│   ├── src/
│   │   ├── sensors/            # Sensor interfaces (DHT22, PIR, etc.)
│   │   ├── communication/      # MQTT, HTTP clients
│   │   ├── processing/         # Image processing pipeline
│   │   ├── ai/                 # AI model integration (Hailo8, etc.)
│   │   └── utils/              # Common utilities
│   ├── config/
│   │   ├── device_config.yaml  # Device-specific config
│   │   ├── network_config.yaml # Network settings
│   │   └── ai_config.yaml      # AI model configuration
│   ├── tests/
│   │   ├── unit/              # Unit tests
│   │   ├── integration/       # Integration tests
│   │   └── hardware/          # Hardware tests
│   ├── scripts/
│   │   ├── deploy.sh          # Deployment script
│   │   ├── monitor.sh         # Health monitoring
│   │   ├── setup.sh           # Initial setup
│   │   └── backup.sh          # Backup and restore
│   ├── docs/                  # Project documentation
│   ├── requirements.txt
│   ├── .cursorrules           # Edge-specific rules
│   ├── Dockerfile             # Container for testing
│   └── README.md
│
├── lprserver_v3/               # Server Repository
│   ├── app/
│   │   ├── api/               # FastAPI routes
│   │   │   ├── v1/           # API versioning
│   │   │   └── health/       # Health check endpoints
│   │   ├── models/            # Database models
│   │   ├── services/          # Business logic
│   │   ├── utils/             # Common utilities
│   │   └── middleware/        # Custom middleware
│   ├── migrations/            # Database migrations
│   ├── tests/
│   │   ├── unit/             # Unit tests
│   │   ├── integration/      # Integration tests
│   │   └── e2e/              # End-to-end tests
│   ├── docker/               # Docker configuration
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   └── nginx/            # Nginx configuration
│   ├── scripts/
│   │   ├── deploy.sh         # Deployment script
│   │   ├── migrate.sh        # Database migration
│   │   └── backup.sh         # Database backup
│   ├── docs/                 # API documentation
│   ├── requirements.txt
│   ├── .cursorrules          # Server-specific rules
│   └── README.md
│
└── shared-tools/              # Shared Development Tools
    ├── templates/             # Code templates
    │   ├── edge/             # Edge device templates
    │   ├── server/           # Server templates
    │   └── docker/           # Docker templates
    ├── scripts/              # Common scripts
    │   ├── setup-env.sh      # Environment setup
    │   ├── sync-repos.sh     # Repository synchronization
    │   └── health-check.sh   # System health checks
    ├── docs/                 # Shared documentation
    │   ├── api/              # API documentation
    │   ├── deployment/       # Deployment guides
    │   └── troubleshooting/  # Troubleshooting guides
    └── config/               # Shared configuration
        ├── logging.yaml      # Logging configuration
        └── monitoring.yaml   # Monitoring configuration
```

## 📝 **Code Quality Best Practices**

### **1. Python Code Standards**

```python
# Use type hints for all functions
from typing import Optional, List, Dict, Any
import logging
from dataclasses import dataclass

@dataclass
class SensorData:
    """Data class for sensor readings"""
    temperature: float
    humidity: float
    timestamp: str

class SensorManager:
    """Manages sensor operations with proper error handling"""
    
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    async def read_sensor(self) -> Optional[SensorData]:
        """Read sensor data with error handling"""
        try:
            # Sensor reading logic
            return SensorData(
                temperature=25.5,
                humidity=60.0,
                timestamp="2024-01-01T12:00:00Z"
            )
        except Exception as e:
            self.logger.error(f"Failed to read sensor: {e}")
            return None
```

### **2. Error Handling Patterns**

```python
import asyncio
from functools import wraps
from typing import Callable, Any

def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """Decorator for retry logic"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    await asyncio.sleep(delay * (2 ** attempt))
            return None
        return wrapper
    return decorator

@retry_on_failure(max_retries=3)
async def send_data_to_server(data: Dict[str, Any]) -> bool:
    """Send data to server with retry logic"""
    # Implementation
    pass
```

### **3. Configuration Management**

```python
import os
from pathlib import Path
from typing import Dict, Any
import yaml

class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
```

## 🧪 **Testing Best Practices**

### **1. Test Structure**

```python
# tests/test_sensor_manager.py
import pytest
from unittest.mock import Mock, patch
from src.sensors.sensor_manager import SensorManager

class TestSensorManager:
    """Test cases for SensorManager"""
    
    @pytest.fixture
    def sensor_manager(self):
        """Create SensorManager instance for testing"""
        config = {"sensor_type": "DHT22", "pin": 4}
        return SensorManager(config)
    
    @pytest.mark.asyncio
    async def test_read_sensor_success(self, sensor_manager):
        """Test successful sensor reading"""
        with patch('src.sensors.sensor_manager.DHT22') as mock_dht:
            mock_dht.return_value.temperature = 25.5
            mock_dht.return_value.humidity = 60.0
            
            result = await sensor_manager.read_sensor()
            
            assert result is not None
            assert result.temperature == 25.5
            assert result.humidity == 60.0
    
    @pytest.mark.asyncio
    async def test_read_sensor_failure(self, sensor_manager):
        """Test sensor reading failure"""
        with patch('src.sensors.sensor_manager.DHT22') as mock_dht:
            mock_dht.side_effect = Exception("Sensor error")
            
            result = await sensor_manager.read_sensor()
            
            assert result is None
```

### **2. Integration Testing**

```python
# tests/integration/test_mqtt_communication.py
import pytest
import asyncio
from src.communication.mqtt_client import MQTTClient

class TestMQTTCommunication:
    """Integration tests for MQTT communication"""
    
    @pytest.mark.asyncio
    async def test_mqtt_publish_subscribe(self):
        """Test MQTT publish and subscribe functionality"""
        client = MQTTClient("test_broker", 1883)
        
        # Test publish
        await client.publish("test/topic", "test_message")
        
        # Test subscribe
        received_messages = []
        await client.subscribe("test/topic", lambda msg: received_messages.append(msg))
        
        # Wait for message processing
        await asyncio.sleep(1)
        
        assert len(received_messages) > 0
```

## 🔧 **Development Workflow**

### **1. Pre-commit Hooks**

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
  
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

### **2. Development Scripts**

```bash
#!/bin/bash
# scripts/dev-setup.sh

echo "Setting up development environment..."

# Create virtual environments
python -m venv aicamera/venv
python -m venv lprserver_v3/venv

# Install dependencies
source aicamera/venv/bin/activate
pip install -r aicamera/requirements.txt

source lprserver_v3/venv/bin/activate
pip install -r lprserver_v3/requirements.txt

# Install pre-commit hooks
pre-commit install

echo "Development environment setup complete!"
```

## 📊 **Performance Optimization**

### **1. Memory Management**

```python
import gc
import psutil
import asyncio
from typing import List

class PerformanceOptimizer:
    """Optimizes performance for resource-constrained environments"""
    
    def __init__(self):
        self.process = psutil.Process()
    
    def get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        return self.process.memory_info().rss / 1024 / 1024
    
    def optimize_memory(self):
        """Optimize memory usage"""
        # Force garbage collection
        gc.collect()
        
        # Log memory usage
        memory_mb = self.get_memory_usage()
        print(f"Memory usage: {memory_mb:.2f} MB")
    
    async def monitor_performance(self, interval: int = 60):
        """Monitor performance metrics"""
        while True:
            self.optimize_memory()
            await asyncio.sleep(interval)
```

### **2. Async Processing**

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, Any

class AsyncProcessor:
    """Handles async processing with thread pool"""
    
    def __init__(self, max_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def process_batch(self, items: List[Any]) -> List[Any]:
        """Process items in parallel"""
        loop = asyncio.get_event_loop()
        
        # Process items in thread pool
        tasks = [
            loop.run_in_executor(self.executor, self._process_item, item)
            for item in items
        ]
        
        results = await asyncio.gather(*tasks)
        return results
    
    def _process_item(self, item: Any) -> Any:
        """Process individual item (CPU-intensive)"""
        # CPU-intensive processing
        return item * 2
```

## 🔍 **Debugging Best Practices**

### **1. Structured Logging**

```python
import logging
import json
from datetime import datetime
from typing import Dict, Any

class StructuredLogger:
    """Structured logging for better debugging"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.setup_logging()
    
    def setup_logging(self):
        """Setup structured logging"""
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_event(self, event: str, data: Dict[str, Any], level: str = "info"):
        """Log structured event"""
        log_data = {
            "event": event,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }
        
        log_message = json.dumps(log_data)
        
        if level == "error":
            self.logger.error(log_message)
        elif level == "warning":
            self.logger.warning(log_message)
        else:
            self.logger.info(log_message)
```

### **2. Debug Configuration**

```python
# config/debug_config.py
import os
from typing import Dict, Any

class DebugConfig:
    """Debug configuration for development"""
    
    @staticmethod
    def get_debug_settings() -> Dict[str, Any]:
        """Get debug settings based on environment"""
        is_debug = os.getenv("DEBUG", "false").lower() == "true"
        
        return {
            "debug": is_debug,
            "log_level": "DEBUG" if is_debug else "INFO",
            "enable_profiling": is_debug,
            "enable_tracing": is_debug,
            "max_log_size": "10MB" if is_debug else "1MB"
        }
```

---

**Last Updated**: December 2024  
**Version**: 2.0.0
