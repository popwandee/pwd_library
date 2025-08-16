# Development Guidelines

**Version:** 1.0.0  
**Last Updated:** 2024-08-16  
**Author:** AI Camera Team  
**Status:** Active

## Overview

แนวทางการพัฒนาร่วมกันระหว่าง Edge Device และ LPR Server เพื่อให้การพัฒนาเป็นระบบและสอดคล้องกัน

## 🏗️ Development Architecture

### Project Structure
```
aicamera/                    # Main project repository
├── v1_3/                   # Edge device application
├── docs/                   # Project documentation
├── pwd_library/            # Shared knowledge base
└── lpr_server/             # LPR Server application (separate repo)

pwd_library/docs/project_lpr/
├── edge/                   # Edge-specific documentation
├── server/                 # Server-specific documentation
└── shared/                 # Shared documentation
```

### Communication Flow
```
Edge Device (v1_3) ←→ Unified Communication Gateway ←→ LPR Server
     │                           │                           │
     ├── WebSocket              ├── REST API                ├── Database
     ├── REST API               ├── MQTT                    ├── Web Dashboard
     ├── MQTT                   ├── SFTP                    └── Processing
     ├── SFTP                   └── rsync
     └── rsync
```

## 📋 Development Standards

### Code Standards

#### Python Code Style
```python
# Follow PEP 8 with Black formatter
# Use Google-style docstrings
# Maximum line length: 88 characters

def process_lpr_data(image_data: bytes, metadata: dict) -> dict:
    """Process LPR data from edge device.
    
    Args:
        image_data: Raw image data in bytes
        metadata: Additional metadata dictionary
        
    Returns:
        Processed LPR results dictionary
        
    Raises:
        ValueError: If image_data is empty
        ProcessingError: If LPR processing fails
    """
    if not image_data:
        raise ValueError("Image data cannot be empty")
    
    try:
        # Process image data
        result = lpr_processor.process(image_data)
        
        # Add metadata
        result.update(metadata)
        
        return result
    except Exception as e:
        raise ProcessingError(f"LPR processing failed: {e}")
```

#### Configuration Management
```python
# Use dataclasses for configuration
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class CommunicationConfig:
    """Configuration for communication protocols."""
    websocket_url: str
    rest_api_url: str
    mqtt_broker: str
    sftp_host: str
    rsync_host: str
    
    # Optional settings
    timeout: int = 30
    retry_attempts: int = 3
    enable_ssl: bool = True

# Load from YAML/JSON files
def load_config(config_path: str) -> CommunicationConfig:
    """Load configuration from file."""
    with open(config_path, 'r') as f:
        config_data = yaml.safe_load(f)
    return CommunicationConfig(**config_data)
```

#### Error Handling
```python
# Use custom exception classes
class CommunicationError(Exception):
    """Base exception for communication errors."""
    pass

class ProtocolError(CommunicationError):
    """Exception for protocol-specific errors."""
    pass

class ConnectionError(CommunicationError):
    """Exception for connection errors."""
    pass

# Consistent error handling
def send_data(data: dict, protocol: str = 'auto') -> bool:
    """Send data using specified protocol."""
    try:
        if protocol == 'websocket':
            return websocket_client.send(data)
        elif protocol == 'rest':
            return rest_client.post(data)
        elif protocol == 'mqtt':
            return mqtt_client.publish(data)
        else:
            raise ProtocolError(f"Unsupported protocol: {protocol}")
    except Exception as e:
        logger.error(f"Failed to send data via {protocol}: {e}")
        raise CommunicationError(f"Data transmission failed: {e}")
```

### API Standards

#### REST API Design
```python
# Consistent endpoint structure
# Edge Device API (v1_3)
GET    /api/v1/health                    # Health check
GET    /api/v1/system/info              # System information
POST   /api/v1/camera/start             # Start camera
POST   /api/v1/camera/stop              # Stop camera
GET    /api/v1/camera/status            # Camera status
POST   /api/v1/lpr/process              # Process LPR
GET    /api/v1/lpr/results              # Get LPR results
POST   /api/v1/communication/test       # Test communication

# LPR Server API
GET    /api/v1/health                   # Health check
GET    /api/v1/events                   # List LPR events
POST   /api/v1/events                   # Create LPR event
GET    /api/v1/events/{event_id}        # Get specific event
PUT    /api/v1/events/{event_id}        # Update event
DELETE /api/v1/events/{event_id}        # Delete event
GET    /api/v1/devices                  # List edge devices
GET    /api/v1/devices/{device_id}      # Get device info
GET    /api/v1/communication/stats      # Communication statistics
```

#### Response Format
```python
# Standard response format
{
    "success": True,
    "data": {
        # Response data
    },
    "message": "Operation completed successfully",
    "timestamp": "2024-08-16T10:30:00Z",
    "request_id": "req_123456789"
}

# Error response format
{
    "success": False,
    "error": {
        "code": "INVALID_INPUT",
        "message": "Invalid input parameters",
        "details": {
            "field": "image_data",
            "issue": "Image data is required"
        }
    },
    "timestamp": "2024-08-16T10:30:00Z",
    "request_id": "req_123456789"
}
```

#### WebSocket Events
```python
# Standard WebSocket event format
{
    "event": "lpr_result",
    "data": {
        "event_id": "evt_123456789",
        "license_plate": "ABC1234",
        "confidence": 0.95,
        "timestamp": "2024-08-16T10:30:00Z"
    },
    "source": "edge_device",
    "target": "lpr_server"
}

# Event types
EVENT_TYPES = {
    # System events
    'system_status': 'System status update',
    'device_connected': 'Device connected',
    'device_disconnected': 'Device disconnected',
    
    # Camera events
    'camera_started': 'Camera started',
    'camera_stopped': 'Camera stopped',
    'frame_captured': 'Frame captured',
    
    # LPR events
    'lpr_processing': 'LPR processing started',
    'lpr_result': 'LPR result available',
    'lpr_error': 'LPR processing error',
    
    # Communication events
    'communication_status': 'Communication status',
    'protocol_changed': 'Protocol changed',
    'connection_lost': 'Connection lost'
}
```

### Database Standards

#### Schema Design
```sql
-- Consistent naming conventions
-- Use snake_case for table and column names
-- Use plural for table names
-- Use singular for column names

-- Edge device events
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

-- Communication logs
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

-- Indexes for performance
CREATE INDEX idx_lpr_events_device_id ON lpr_events(edge_device_id);
CREATE INDEX idx_lpr_events_created_at ON lpr_events(created_at);
CREATE INDEX idx_comm_logs_protocol ON communication_logs(protocol);
CREATE INDEX idx_comm_logs_created_at ON communication_logs(created_at);
```

#### Data Validation
```python
# Use Pydantic for data validation
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime

class LPREvent(BaseModel):
    """LPR event data model."""
    event_id: str = Field(..., min_length=1, max_length=50)
    edge_device_id: str = Field(..., min_length=1, max_length=50)
    license_plate: Optional[str] = Field(None, max_length=20)
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    image_path: Optional[str] = Field(None, max_length=255)
    metadata: Optional[Dict[str, Any]] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator('event_id')
    def validate_event_id(cls, v):
        if not v.startswith('evt_'):
            raise ValueError('Event ID must start with "evt_"')
        return v
    
    @validator('edge_device_id')
    def validate_device_id(cls, v):
        if not v.startswith('edge_'):
            raise ValueError('Device ID must start with "edge_"')
        return v

class CommunicationLog(BaseModel):
    """Communication log data model."""
    protocol: str = Field(..., regex='^(websocket|rest|mqtt|sftp|rsync)$')
    source: str = Field(..., min_length=1, max_length=50)
    destination: str = Field(..., min_length=1, max_length=50)
    message_type: Optional[str] = Field(None, max_length=50)
    success: bool
    latency_ms: Optional[int] = Field(None, ge=0)
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## 🔄 Development Workflow

### Git Workflow

#### Branch Strategy
```
main
├── develop
│   ├── feature/edge-camera-improvements
│   ├── feature/server-api-enhancements
│   ├── feature/unified-communication
│   └── hotfix/critical-bug-fix
└── release/v1.3.1
```

#### Commit Message Format
```bash
# Format: <type>(<scope>): <description>
# Types: feat, fix, docs, style, refactor, test, chore

# Examples:
feat(edge): add camera auto-focus capability
fix(server): resolve database connection timeout
docs(shared): update communication protocol guide
style(edge): format code with black
refactor(server): improve API response handling
test(edge): add unit tests for LPR processing
chore(shared): update dependencies
```

#### Pull Request Process
1. **Create Feature Branch** - จาก develop branch
2. **Develop Feature** - พัฒนาฟีเจอร์ตาม requirements
3. **Write Tests** - เขียน unit tests และ integration tests
4. **Update Documentation** - อัปเดตเอกสารที่เกี่ยวข้อง
5. **Create Pull Request** - สร้าง PR ไปยัง develop
6. **Code Review** - ทีม review code
7. **Address Feedback** - แก้ไขตาม feedback
8. **Merge** - merge เมื่อ approved

### Testing Standards

#### Unit Tests
```python
# Use pytest for unit testing
import pytest
from unittest.mock import Mock, patch
from src.communication import UnifiedCommunicationGateway

class TestUnifiedCommunicationGateway:
    """Test cases for UnifiedCommunicationGateway."""
    
    @pytest.fixture
    def gateway(self):
        """Create gateway instance for testing."""
        config = Mock()
        config.websocket.server_url = "ws://test:8765"
        config.rest.base_url = "http://test:8000"
        return UnifiedCommunicationGateway(config)
    
    def test_send_metadata_websocket_success(self, gateway):
        """Test successful metadata sending via WebSocket."""
        with patch.object(gateway.websocket_client, 'send') as mock_send:
            mock_send.return_value = CommunicationResult(success=True)
            
            result = gateway.send_metadata({"test": "data"}, protocol='websocket')
            
            assert result.success is True
            mock_send.assert_called_once_with({"test": "data"})
    
    def test_send_metadata_auto_selection(self, gateway):
        """Test automatic protocol selection."""
        with patch.object(gateway.protocol_selector, 'select_metadata_protocol') as mock_select:
            mock_select.return_value = 'rest'
            
            gateway.send_metadata({"test": "data"})
            
            mock_select.assert_called_once_with({"test": "data"}, 'normal')
```

#### Integration Tests
```python
# Test communication between Edge and Server
import pytest
import requests
import websocket
from src.test_utils import TestServer, TestEdge

class TestEdgeServerCommunication:
    """Integration tests for Edge-Server communication."""
    
    @pytest.fixture
    def test_server(self):
        """Start test server."""
        server = TestServer()
        server.start()
        yield server
        server.stop()
    
    @pytest.fixture
    def test_edge(self):
        """Start test edge device."""
        edge = TestEdge()
        edge.start()
        yield edge
        edge.stop()
    
    def test_rest_api_communication(self, test_server, test_edge):
        """Test REST API communication."""
        # Send test data from edge to server
        response = test_edge.send_rest_data({
            "event_id": "evt_test_001",
            "license_plate": "TEST123",
            "confidence": 0.95
        })
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        
        # Verify data received by server
        events = test_server.get_events()
        assert len(events) == 1
        assert events[0]["event_id"] == "evt_test_001"
    
    def test_websocket_communication(self, test_server, test_edge):
        """Test WebSocket communication."""
        # Connect WebSocket
        ws = test_edge.connect_websocket()
        
        # Send test event
        test_edge.send_websocket_event("lpr_result", {
            "event_id": "evt_test_002",
            "license_plate": "TEST456"
        })
        
        # Verify event received by server
        received_events = test_server.get_websocket_events()
        assert len(received_events) == 1
        assert received_events[0]["event"] == "lpr_result"
```

### Documentation Standards

#### Code Documentation
```python
def process_lpr_image(image_data: bytes, config: LPRConfig) -> LPRResult:
    """Process license plate recognition on image data.
    
    This function performs license plate recognition on the provided image
    data using the specified configuration. It supports multiple AI models
    and can handle various image formats.
    
    Args:
        image_data: Raw image data in bytes. Supports JPEG, PNG formats.
        config: LPR configuration including model selection and parameters.
        
    Returns:
        LPRResult object containing recognition results and metadata.
        
    Raises:
        ValueError: If image_data is empty or invalid format.
        ModelNotFoundError: If specified AI model is not available.
        ProcessingError: If LPR processing fails due to technical issues.
        
    Example:
        >>> config = LPRConfig(model="hailo_yolo", confidence_threshold=0.8)
        >>> result = process_lpr_image(image_bytes, config)
        >>> print(f"Detected: {result.license_plate}")
        Detected: ABC1234
    """
    # Implementation details...
```

#### API Documentation
```python
# Use OpenAPI/Swagger for API documentation
from flask_restx import Api, Resource, fields

api = Api(
    title='AI Camera Edge API',
    version='1.0',
    description='API for AI Camera Edge Device'
)

# Define models
lpr_event_model = api.model('LPREvent', {
    'event_id': fields.String(required=True, description='Unique event ID'),
    'license_plate': fields.String(description='Detected license plate'),
    'confidence': fields.Float(description='Detection confidence (0-1)'),
    'image_path': fields.String(description='Path to captured image'),
    'metadata': fields.Raw(description='Additional metadata')
})

@api.route('/api/v1/lpr/process')
class LPRProcess(Resource):
    @api.doc('process_lpr_image')
    @api.expect(lpr_event_model)
    @api.marshal_with(lpr_event_model, code=201)
    def post(self):
        """Process LPR image and return results."""
        # Implementation...
```

## 🔧 Development Tools

### Required Tools
- **Python 3.10+** - Programming language
- **Git** - Version control
- **Docker** - Containerization (optional)
- **VS Code/Cursor** - IDE
- **Black** - Code formatter
- **Pylint** - Code linter
- **Pytest** - Testing framework

### Development Environment Setup
```bash
# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Setup database (for server development)
sudo -u postgres createdb aicamera_dev
sudo -u postgres createuser aicamera_dev

# Run tests
pytest tests/

# Format code
black src/
isort src/

# Lint code
pylint src/
```

### Configuration Management
```yaml
# config/development.yaml
environment: development
debug: true

communication:
  websocket:
    server_url: "ws://localhost:8765"
    reconnect_attempts: 3
  rest:
    base_url: "http://localhost:8000"
    timeout: 30
  mqtt:
    broker_url: "localhost"
    client_id: "dev_edge_001"

database:
  host: "localhost"
  port: 5432
  name: "aicamera_dev"
  user: "aicamera_dev"

logging:
  level: "DEBUG"
  file: "logs/dev.log"
```

## 📊 Monitoring and Debugging

### Logging Standards
```python
import logging
import json
from datetime import datetime

# Structured logging
class StructuredLogger:
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
    
    def log_event(self, event_type: str, data: dict, level: str = "INFO"):
        """Log structured event."""
        log_data = {
            "event_type": event_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        getattr(self.logger, level.lower())(
            f"Event: {event_type}",
            extra={"extra": json.dumps(log_data)}
        )

# Usage
logger = StructuredLogger("edge_device")
logger.log_event("lpr_processing", {
    "event_id": "evt_123",
    "image_size": 1024000,
    "processing_time": 1.5
})
```

### Performance Monitoring
```python
import time
import functools
from typing import Callable, Any

def monitor_performance(func: Callable) -> Callable:
    """Decorator to monitor function performance."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Log performance metrics
            logger.info(f"Function {func.__name__} executed in {execution_time:.3f}s")
            
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Function {func.__name__} failed after {execution_time:.3f}s: {e}")
            raise
    
    return wrapper

# Usage
@monitor_performance
def process_lpr_image(image_data: bytes) -> dict:
    """Process LPR image with performance monitoring."""
    # Implementation...
```

## 🔒 Security Guidelines

### Authentication and Authorization
```python
# JWT-based authentication
import jwt
from functools import wraps
from flask import request, jsonify

def require_auth(f):
    """Decorator to require JWT authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({"error": "No token provided"}), 401
        
        try:
            # Remove 'Bearer ' prefix
            token = token.split(' ')[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user = payload
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        
        return f(*args, **kwargs)
    
    return decorated

# Usage
@app.route('/api/v1/events')
@require_auth
def get_events():
    """Get events (requires authentication)."""
    # Implementation...
```

### Data Validation and Sanitization
```python
from pydantic import BaseModel, validator
import re

class UserInput(BaseModel):
    """User input with validation and sanitization."""
    event_id: str
    license_plate: Optional[str] = None
    
    @validator('event_id')
    def validate_event_id(cls, v):
        # Only allow alphanumeric and underscore
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Event ID contains invalid characters')
        return v
    
    @validator('license_plate')
    def validate_license_plate(cls, v):
        if v is not None:
            # Remove any potentially dangerous characters
            v = re.sub(r'[<>"\']', '', v)
            if len(v) > 20:
                raise ValueError('License plate too long')
        return v
```

## 📚 References

### Related Documentation
- **[Unified Communication Architecture](unified-communication-architecture.md)** - สถาปัตยกรรมการสื่อสารแบบรวม
- **[Tailscale Setup](tailscale-setup.md)** - การตั้งค่า Tailscale VPN
- **[Edge Project Overview](../edge/project-overview.md)** - ภาพรวมโปรเจค Edge
- **[Server Documentation](../server/README.md)** - เอกสาร LPR Server

### External Resources
- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Pytest Documentation](https://docs.pytest.org/)

---

**Note:** แนวทางการพัฒนานี้จะได้รับการอัปเดตตามความต้องการและ feedback จากทีม
