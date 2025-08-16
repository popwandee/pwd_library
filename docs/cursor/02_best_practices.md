# Cursor AI Development Best Practices

**แนวปฏิบัติที่ดีในการใช้ Cursor AI สำหรับการพัฒนาโปรเจกต์ IoT แบบ Multi-Machine**

## 🎯 **Core Principles**

### **1. Separation of Concerns**
- แยก Edge และ Server development ให้ชัดเจน
- ใช้ .cursorrules ที่เหมาะสมสำหรับแต่ละโปรเจกต์
- จัดการ dependencies แยกกัน

### **2. Network Resilience**
- ออกแบบระบบให้ทำงานได้แม้ network มีปัญหา
- ใช้ local caching และ buffering
- Implement retry logic และ circuit breakers

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

### **2. Configuration Management**

**Edge Device Configuration (aicamera/config/device_config.yaml):**
```yaml
device:
  id: "ai_camera_001"
  name: "Raspberry Pi Camera"
  location: "entrance_gate"
  
hardware:
  camera:
    resolution: [1920, 1080]
    framerate: 30
    sensor_mode: 3
  
  sensors:
    temperature:
      enabled: true
      pin: 4
      sampling_rate: 60  # seconds
    
    motion:
      enabled: true
      pin: 17
      sensitivity: 0.5

network:
  mqtt:
    broker: "192.168.1.10"  # Server Tailscale IP
    port: 1883
    keepalive: 60
    reconnect_delay: 5
  
  http:
    server_url: "http://192.168.1.10:8000"
    timeout: 30
    retry_attempts: 3

processing:
  image_quality: 85
  max_file_size: "10MB"
  storage_path: "/opt/aicamera/storage"
  
logging:
  level: "INFO"
  file: "/var/log/aicamera/app.log"
  max_size: "10MB"
  backup_count: 5
```

**Server Configuration (lprserver_v3/config/server_config.yaml):**
```yaml
server:
  host: "0.0.0.0"
  port: 8000
  workers: 4
  timeout: 30

database:
  url: "postgresql://user:pass@localhost:5432/lpr_db"
  pool_size: 20
  max_overflow: 30
  echo: false

redis:
  url: "redis://localhost:6379"
  max_connections: 20

mqtt:
  broker: "localhost"
  port: 1883
  topics:
    sensor_data: "sensor/data"
    commands: "device/commands"
    status: "device/status"

security:
  jwt_secret: "your-secret-key"
  jwt_expire_minutes: 60
  cors_origins: ["*"]

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "/var/log/lprserver/app.log"
```

## 🚀 **Development Workflow Best Practices**

### **1. Git Workflow**

```bash
# Feature Branch Workflow
git checkout -b feature/edge-mqtt-improvement
# Develop and test
git add .
git commit -m "feat: improve MQTT reconnection logic with exponential backoff"
git push origin feature/edge-mqtt-improvement
# Create Pull Request

# Hotfix Workflow
git checkout -b hotfix/critical-security-fix
# Fix and test
git add .
git commit -m "fix: patch critical security vulnerability in API endpoint"
git push origin hotfix/critical-security-fix
```

### **2. Environment Management**

```bash
# Create environment-specific files
# .env.development
# .env.staging
# .env.production

# Load environment in scripts
#!/bin/bash
ENV=${1:-development}
source .env.$ENV

echo "Using environment: $ENV"
echo "Edge device IP: $EDGE_DEVICE_IP"
echo "Server device IP: $SERVER_DEVICE_IP"
```

### **3. Automated Testing**

```python
# tests/test_edge_communication.py
import pytest
import asyncio
from unittest.mock import Mock, patch
from src.communication.mqtt_client import MQTTClient

@pytest.mark.asyncio
async def test_mqtt_reconnection():
    """Test MQTT client reconnection logic"""
    client = MQTTClient("test-broker", 1883)
    
    # Mock connection failure
    with patch.object(client, '_connect', side_effect=Exception("Connection failed")):
        with pytest.raises(Exception):
            await client.connect()
    
    # Verify retry logic
    assert client.retry_count > 0

@pytest.mark.asyncio
async def test_sensor_data_processing():
    """Test sensor data processing pipeline"""
    # Test implementation
    pass
```

## 🛠️ **Code Quality Best Practices**

### **1. Edge Device Code Patterns**

```python
# src/communication/mqtt_client.py
import asyncio
import logging
from typing import Optional, Callable
from paho.mqtt import client as mqtt_client

class MQTTClient:
    """Robust MQTT client with reconnection logic"""
    
    def __init__(self, broker: str, port: int = 1883):
        self.broker = broker
        self.port = port
        self.client = mqtt_client.Client()
        self.logger = logging.getLogger(__name__)
        self.connected = False
        self.retry_count = 0
        self.max_retries = 5
        
    async def connect(self) -> bool:
        """Connect with retry logic"""
        for attempt in range(self.max_retries):
            try:
                result = self.client.connect(self.broker, self.port)
                if result == mqtt_client.MQTT_ERR_SUCCESS:
                    self.connected = True
                    self.retry_count = 0
                    self.logger.info("MQTT connected successfully")
                    return True
            except Exception as e:
                self.logger.error(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        self.logger.error("Failed to connect after all retries")
        return False
    
    async def publish(self, topic: str, message: str, qos: int = 1) -> bool:
        """Publish message with error handling"""
        if not self.connected:
            if not await self.connect():
                return False
        
        try:
            result = self.client.publish(topic, message, qos)
            return result.rc == mqtt_client.MQTT_ERR_SUCCESS
        except Exception as e:
            self.logger.error(f"Publish failed: {e}")
            self.connected = False
            return False
```

### **2. Server Code Patterns**

```python
# app/api/endpoints/sensor_data.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.sensor_data import SensorData
from app.schemas.sensor_data import SensorDataCreate, SensorDataResponse
from app.services.sensor_service import SensorService
from app.database import get_db

router = APIRouter()

@router.post("/sensor-data", response_model=SensorDataResponse)
async def create_sensor_data(
    data: SensorDataCreate,
    db: Session = Depends(get_db),
    sensor_service: SensorService = Depends()
):
    """Create new sensor data entry"""
    try:
        result = await sensor_service.create_sensor_data(db, data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sensor-data/{device_id}", response_model=List[SensorDataResponse])
async def get_device_data(
    device_id: str,
    limit: int = 100,
    db: Session = Depends(get_db),
    sensor_service: SensorService = Depends()
):
    """Get sensor data for specific device"""
    try:
        data = await sensor_service.get_device_data(db, device_id, limit)
        return data
    except Exception as e:
        raise HTTPException(status_code=404, detail="Device not found")
```

### **3. Error Handling Patterns**

```python
# app/utils/error_handlers.py
import logging
from functools import wraps
from typing import Callable, Any
from fastapi import HTTPException

logger = logging.getLogger(__name__)

def handle_errors(func: Callable) -> Callable:
    """Decorator for consistent error handling"""
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    return wrapper

class CircuitBreaker:
    """Circuit breaker pattern for external service calls"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    async def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.state == "OPEN":
            if self._should_attempt_reset():
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        """Handle successful call"""
        self.failure_count = 0
        self.state = "CLOSED"
    
    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
    
    def _should_attempt_reset(self) -> bool:
        """Check if circuit breaker should attempt reset"""
        if self.last_failure_time is None:
            return True
        return time.time() - self.last_failure_time >= self.timeout
```

## 🔧 **Deployment Best Practices**

### **1. Edge Device Deployment**

```bash
#!/bin/bash
# scripts/deploy_edge.sh

set -e

DEVICE_IP=${1:-$EDGE_DEVICE_IP}
PROJECT_DIR="/opt/aicamera"

echo "Deploying to edge device: $DEVICE_IP"

# Create backup
ssh pi@$DEVICE_IP "sudo cp -r $PROJECT_DIR ${PROJECT_DIR}_backup_$(date +%Y%m%d_%H%M%S)"

# Sync code
rsync -avz --exclude='venv' --exclude='__pycache__' --exclude='*.log' \
    ./aicamera/ pi@$DEVICE_IP:$PROJECT_DIR/

# Install dependencies
ssh pi@$DEVICE_IP "cd $PROJECT_DIR && source venv/bin/activate && pip install -r requirements.txt"

# Update configuration
ssh pi@$DEVICE_IP "sudo cp $PROJECT_DIR/config/device_config.yaml /etc/aicamera/"

# Restart service
ssh pi@$DEVICE_IP "sudo systemctl restart aicamera"

# Verify deployment
ssh pi@$DEVICE_IP "sudo systemctl status aicamera"
echo "Edge deployment completed successfully!"
```

### **2. Server Deployment**

```yaml
# docker-compose.yml
version: '3.8'

services:
  lprserver:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/lpr_db
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  postgres:
    image: postgres:13
    environment:
      - POSTGRES_DB=lpr_db
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:6-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

## 📊 **Monitoring and Logging Best Practices**

### **1. Health Monitoring**

```python
# src/monitoring/health_check.py
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any

class HealthMonitor:
    """Health monitoring for edge devices"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.health_status = {
            "status": "healthy",
            "last_check": None,
            "components": {}
        }
    
    async def check_system_health(self) -> Dict[str, Any]:
        """Comprehensive health check"""
        checks = {
            "cpu_usage": await self._check_cpu_usage(),
            "memory_usage": await self._check_memory_usage(),
            "disk_usage": await self._check_disk_usage(),
            "network_connectivity": await self._check_network(),
            "sensor_status": await self._check_sensors(),
            "mqtt_connection": await self._check_mqtt()
        }
        
        # Update overall status
        failed_checks = [k for k, v in checks.items() if not v["healthy"]]
        self.health_status["status"] = "unhealthy" if failed_checks else "healthy"
        self.health_status["last_check"] = datetime.now()
        self.health_status["components"] = checks
        
        return self.health_status
    
    async def _check_cpu_usage(self) -> Dict[str, Any]:
        """Check CPU usage"""
        try:
            # Implementation for CPU check
            return {"healthy": True, "value": "25%", "threshold": "80%"}
        except Exception as e:
            return {"healthy": False, "error": str(e)}
    
    async def _check_memory_usage(self) -> Dict[str, Any]:
        """Check memory usage"""
        try:
            # Implementation for memory check
            return {"healthy": True, "value": "512MB", "threshold": "1GB"}
        except Exception as e:
            return {"healthy": False, "error": str(e)}
```

### **2. Structured Logging**

```python
# app/utils/logging.py
import logging
import json
from datetime import datetime
from typing import Any, Dict

class StructuredLogger:
    """Structured logging for better monitoring"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Add JSON formatter
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
            '"logger": "%(name)s", "message": "%(message)s", '
            '"extra": %(extra)s}'
        )
        
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def info(self, message: str, extra: Dict[str, Any] = None):
        """Log info message with structured data"""
        self.logger.info(message, extra={"extra": json.dumps(extra or {})})
    
    def error(self, message: str, extra: Dict[str, Any] = None):
        """Log error message with structured data"""
        self.logger.error(message, extra={"extra": json.dumps(extra or {})})
    
    def log_api_request(self, method: str, path: str, status_code: int, 
                       duration: float, user_id: str = None):
        """Log API request details"""
        extra = {
            "type": "api_request",
            "method": method,
            "path": path,
            "status_code": status_code,
            "duration_ms": round(duration * 1000, 2),
            "user_id": user_id
        }
        self.info(f"API Request: {method} {path} - {status_code}", extra)
```

## 🔒 **Security Best Practices**

### **1. Authentication and Authorization**

```python
# app/security/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

security = HTTPBearer()

class AuthService:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
    
    def create_access_token(self, data: dict) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> dict:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user"""
    auth_service = AuthService("your-secret-key")
    payload = auth_service.verify_token(credentials.credentials)
    return payload
```

### **2. Input Validation**

```python
# app/schemas/validation.py
from pydantic import BaseModel, validator, Field
from typing import Optional
import re

class SensorDataCreate(BaseModel):
    device_id: str = Field(..., min_length=1, max_length=50)
    temperature: float = Field(..., ge=-50, le=100)
    humidity: float = Field(..., ge=0, le=100)
    timestamp: str
    
    @validator('device_id')
    def validate_device_id(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Device ID must contain only alphanumeric characters, hyphens, and underscores')
        return v
    
    @validator('timestamp')
    def validate_timestamp(cls, v):
        try:
            datetime.fromisoformat(v.replace('Z', '+00:00'))
            return v
        except ValueError:
            raise ValueError('Invalid timestamp format')
```

## 📈 **Performance Best Practices**

### **1. Database Optimization**

```python
# app/database/optimization.py
from sqlalchemy import create_engine, Index, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from sqlalchemy import event

# Database connection pooling with monitoring
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False,  # Set to True for debugging
    pool_timeout=30
)

# Create indexes for better performance
Index('idx_sensor_data_device_timestamp', 'device_id', 'timestamp')
Index('idx_sensor_data_timestamp', 'timestamp')
Index('idx_sensor_data_device_status', 'device_id', 'status')

# Database monitoring
@event.listens_for(engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())

@event.listens_for(engine, "after_cursor_execute")
def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop(-1)
    if total > 1.0:  # Log slow queries
        logger.warning(f"Slow query detected: {total:.2f}s - {statement[:100]}")

# Connection health check
def check_db_health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False
```

### **2. Edge Device Performance**

```python
# src/optimization/performance.py
import psutil
import asyncio
from typing import Dict, Any

class PerformanceOptimizer:
    """Performance optimization for edge devices"""
    
    def __init__(self):
        self.memory_threshold = 0.8  # 80% memory usage
        self.cpu_threshold = 0.7     # 70% CPU usage
        self.temp_threshold = 70     # 70°C temperature
    
    async def optimize_system(self) -> Dict[str, Any]:
        """Apply performance optimizations"""
        optimizations = {}
        
        # Memory optimization
        if psutil.virtual_memory().percent > self.memory_threshold * 100:
            optimizations['memory'] = await self._optimize_memory()
        
        # CPU optimization
        if psutil.cpu_percent() > self.cpu_threshold * 100:
            optimizations['cpu'] = await self._optimize_cpu()
        
        # Temperature optimization
        temp = self._get_cpu_temperature()
        if temp > self.temp_threshold:
            optimizations['temperature'] = await self._optimize_temperature()
        
        return optimizations
    
    async def _optimize_memory(self) -> Dict[str, Any]:
        """Optimize memory usage"""
        import gc
        gc.collect()  # Force garbage collection
        
        # Clear image cache if available
        if hasattr(self, 'image_cache'):
            self.image_cache.clear()
        
        return {"action": "garbage_collection", "memory_freed": "variable"}
    
    async def _optimize_cpu(self) -> Dict[str, Any]:
        """Optimize CPU usage"""
        # Reduce processing frequency
        return {"action": "reduce_processing_frequency", "new_interval": "5s"}
    
    async def _optimize_temperature(self) -> Dict[str, Any]:
        """Optimize for temperature"""
        # Reduce CPU frequency
        return {"action": "reduce_cpu_frequency", "new_freq": "1.2GHz"}
    
    def _get_cpu_temperature(self) -> float:
        """Get CPU temperature"""
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp = float(f.read()) / 1000.0
            return temp
        except:
            return 0.0
```

### **2. Caching Strategy**

```python
# app/services/cache_service.py
import redis
import json
from typing import Any, Optional
from functools import wraps

class CacheService:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = self.redis.get(key)
            return json.loads(value) if value else None
        except Exception:
            return None
    
    def set(self, key: str, value: Any, expire: int = 3600):
        """Set value in cache"""
        try:
            self.redis.setex(key, expire, json.dumps(value))
        except Exception:
            pass  # Fail silently for cache operations
    
    def delete(self, key: str):
        """Delete value from cache"""
        try:
            self.redis.delete(key)
        except Exception:
            pass

def cache_result(expire: int = 3600):
    """Decorator for caching function results"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_service = CacheService("redis://localhost:6379")
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached_result = cache_service.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            cache_service.set(cache_key, result, expire)
            return result
        return wrapper
    return decorator
```

## 🔄 **Modern Development Practices**

### **1. CI/CD Pipeline**

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test-edge:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r aicamera/requirements.txt
          pip install pytest pytest-asyncio
      - name: Run tests
        run: |
          cd aicamera
          pytest tests/ -v

  test-server:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:6-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r lprserver_v3/requirements.txt
          pip install pytest pytest-asyncio
      - name: Run tests
        run: |
          cd lprserver_v3
          pytest tests/ -v

  deploy-edge:
    needs: [test-edge]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Edge Device
        run: |
          echo "Deploying to edge device..."
          # Add deployment logic here

  deploy-server:
    needs: [test-server]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Server
        run: |
          echo "Deploying to server..."
          # Add deployment logic here
```

### **2. Infrastructure as Code**

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  lprserver:
    build: 
      context: .
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/lpr_db
      - REDIS_URL=redis://redis:6379
      - ENVIRONMENT=production
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./logs:/app/logs
      - ./uploads:/app/uploads
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  postgres:
    image: postgres:13
    environment:
      - POSTGRES_DB=lpr_db
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d lpr_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:6-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./docker/nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./docker/nginx/ssl:/etc/nginx/ssl
    depends_on:
      - lprserver
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### **3. Monitoring and Observability**

```python
# app/monitoring/prometheus_metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import FastAPI
import time

# Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Number of active connections')
DB_CONNECTION_POOL = Gauge('db_connection_pool_size', 'Database connection pool size')

class MetricsMiddleware:
    def __init__(self, app: FastAPI):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope['type'] == 'http':
            start_time = time.time()
            
            async def send_wrapper(message):
                if message['type'] == 'http.response.start':
                    duration = time.time() - start_time
                    REQUEST_DURATION.observe(duration)
                    REQUEST_COUNT.labels(
                        method=scope['method'],
                        endpoint=scope['path'],
                        status=message['status']
                    ).inc()
                await send(message)
            
            await self.app(scope, receive, send_wrapper)
        else:
            await self.app(scope, receive, send)

# Health check endpoint
@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

## 🛡️ **Security Best Practices (Updated)**

### **1. Advanced Authentication**

```python
# app/security/advanced_auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

class AdvancedAuthService:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
        self.refresh_token_expire_days = 7
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def create_tokens(self, data: dict) -> dict:
        access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
        refresh_token_expires = timedelta(days=self.refresh_token_expire_days)
        
        access_token = self._create_token(data, access_token_expires)
        refresh_token = self._create_token(data, refresh_token_expires)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    def _create_token(self, data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire, "jti": secrets.token_urlsafe()})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
```

### **2. Rate Limiting and DDoS Protection**

```python
# app/security/rate_limiting.py
from fastapi import HTTPException, Request
import time
from collections import defaultdict
import asyncio

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)
    
    async def check_rate_limit(self, request: Request, client_id: str):
        now = time.time()
        minute_ago = now - 60
        
        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if req_time > minute_ago
        ]
        
        # Check rate limit
        if len(self.requests[client_id]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later."
            )
        
        # Add current request
        self.requests[client_id].append(now)

# Usage in middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_id = request.client.host
    await rate_limiter.check_rate_limit(request, client_id)
    response = await call_next(request)
    return response
```

---

**Next Steps**: อ่าน [IoT Development Guide](03_iot_development.md) สำหรับการพัฒนา Edge devices
