# Security Best Practices

**แนวปฏิบัติที่ดีสำหรับความปลอดภัยในการพัฒนาโปรเจกต์ IoT**

## 🔒 **Security Architecture**

### **1. Multi-Layer Security Model**

```
┌─────────────────────────────────────┐
│           Application Layer         │
│  ┌─────────────────────────────────┐ │
│  │      Authentication & Auth      │ │
│  │      Rate Limiting & DDoS       │ │
│  │      Input Validation           │ │
│  └─────────────────────────────────┘ │
├─────────────────────────────────────┤
│           Transport Layer           │
│  ┌─────────────────────────────────┐ │
│  │      TLS/SSL Encryption         │ │
│  │      Certificate Management     │ │
│  │      Secure Protocols           │ │
│  └─────────────────────────────────┘ │
├─────────────────────────────────────┤
│           Network Layer             │
│  ┌─────────────────────────────────┐ │
│  │      Firewall Configuration     │ │
│  │      VPN (Tailscale)            │ │
│  │      Network Segmentation       │ │
│  └─────────────────────────────────┘ │
├─────────────────────────────────────┤
│           Device Layer              │
│  ┌─────────────────────────────────┐ │
│  │      Secure Boot                │ │
│  │      Access Control             │ │
│  │      Physical Security          │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

### **2. Security Zones**

```
Internet
    │
    ▼
┌─────────────┐
│   Firewall  │
└─────────────┘
    │
    ▼
┌─────────────┐    ┌─────────────┐
│   Server    │    │   Edge      │
│   Zone      │    │   Zone      │
│             │    │             │
│ • API       │    │ • Sensors   │
│ • Database  │    │ • Camera    │
│ • Cache     │    │ • Processing│
└─────────────┘    └─────────────┘
    │                   │
    └───────┬───────────┘
            │
        ┌─────────────┐
        │   VPN       │
        │  (Tailscale)│
        └─────────────┘
```

## 🔐 **Authentication & Authorization**

### **1. JWT Implementation**

```python
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class SecurityManager:
    """Manages authentication and authorization"""
    
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.pwd_context = pwd_context
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash password"""
        return self.pwd_context.hash(password)
    
    def create_access_token(
        self,
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

# Security dependency
security = HTTPBearer()
security_manager = SecurityManager()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Get current authenticated user"""
    token = credentials.credentials
    payload = security_manager.verify_token(token)
    return payload
```

### **2. Role-Based Access Control (RBAC)**

```python
from enum import Enum
from typing import List, Set
from functools import wraps

class UserRole(Enum):
    ADMIN = "admin"
    OPERATOR = "operator"
    VIEWER = "viewer"

class Permission(Enum):
    READ_SENSORS = "read_sensors"
    WRITE_SENSORS = "write_sensors"
    READ_LOGS = "read_logs"
    WRITE_LOGS = "write_logs"
    MANAGE_USERS = "manage_users"
    MANAGE_SYSTEM = "manage_system"

class RBACManager:
    """Role-based access control manager"""
    
    def __init__(self):
        self.role_permissions = {
            UserRole.ADMIN: {
                Permission.READ_SENSORS,
                Permission.WRITE_SENSORS,
                Permission.READ_LOGS,
                Permission.WRITE_LOGS,
                Permission.MANAGE_USERS,
                Permission.MANAGE_SYSTEM
            },
            UserRole.OPERATOR: {
                Permission.READ_SENSORS,
                Permission.WRITE_SENSORS,
                Permission.READ_LOGS
            },
            UserRole.VIEWER: {
                Permission.READ_SENSORS,
                Permission.READ_LOGS
            }
        }
    
    def has_permission(self, user_role: UserRole, permission: Permission) -> bool:
        """Check if user has specific permission"""
        return permission in self.role_permissions.get(user_role, set())
    
    def require_permission(self, permission: Permission):
        """Decorator to require specific permission"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Get user from context (implement based on your auth system)
                user_role = kwargs.get('user_role', UserRole.VIEWER)
                
                if not self.has_permission(user_role, permission):
                    raise HTTPException(
                        status_code=403,
                        detail=f"Insufficient permissions for {permission.value}"
                    )
                
                return await func(*args, **kwargs)
            return wrapper
        return decorator

# Usage example
rbac_manager = RBACManager()

@rbac_manager.require_permission(Permission.READ_SENSORS)
async def get_sensor_data(user_role: UserRole = UserRole.VIEWER):
    """Get sensor data (requires READ_SENSORS permission)"""
    return {"sensor_data": "example"}
```

## 🛡️ **Input Validation & Sanitization**

### **1. Pydantic Models for Validation**

```python
from pydantic import BaseModel, validator, Field
from typing import Optional, List
import re

class SensorData(BaseModel):
    """Validated sensor data model"""
    
    temperature: float = Field(..., ge=-50, le=100)
    humidity: float = Field(..., ge=0, le=100)
    timestamp: str = Field(..., regex=r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$')
    sensor_id: str = Field(..., min_length=1, max_length=50)
    location: Optional[str] = Field(None, max_length=100)
    
    @validator('sensor_id')
    def validate_sensor_id(cls, v):
        """Validate sensor ID format"""
        if not re.match(r'^[A-Za-z0-9_-]+$', v):
            raise ValueError('Sensor ID must contain only alphanumeric characters, hyphens, and underscores')
        return v
    
    @validator('location')
    def validate_location(cls, v):
        """Validate location format"""
        if v is not None:
            # Remove potentially dangerous characters
            v = re.sub(r'[<>"\']', '', v)
        return v

class ImageData(BaseModel):
    """Validated image data model"""
    
    image_data: str = Field(..., min_length=100)  # Base64 encoded
    format: str = Field(..., regex=r'^(jpeg|png|jpg)$')
    size_bytes: int = Field(..., ge=1024, le=10*1024*1024)  # 1KB to 10MB
    
    @validator('image_data')
    def validate_image_data(cls, v):
        """Validate base64 image data"""
        import base64
        try:
            # Check if it's valid base64
            base64.b64decode(v)
            return v
        except Exception:
            raise ValueError('Invalid base64 image data')

class APIRequest(BaseModel):
    """Validated API request model"""
    
    endpoint: str = Field(..., regex=r'^/api/v[0-9]+/[a-zA-Z0-9/_-]+$')
    method: str = Field(..., regex=r'^(GET|POST|PUT|DELETE)$')
    headers: Optional[Dict[str, str]] = Field(default_factory=dict)
    body: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    @validator('headers')
    def validate_headers(cls, v):
        """Validate and sanitize headers"""
        sanitized = {}
        for key, value in v.items():
            # Remove potentially dangerous headers
            if key.lower() not in ['host', 'content-length', 'transfer-encoding']:
                # Sanitize header values
                sanitized[key] = re.sub(r'[<>"\']', '', str(value))
        return sanitized
```

### **2. SQL Injection Prevention**

```python
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from typing import Dict, Any, List
import logging

class SecureDatabaseManager:
    """Secure database operations with SQL injection prevention"""
    
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.logger = logging.getLogger(__name__)
    
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
    
    def execute_query_safely(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute query safely using parameterized statements"""
        try:
            with self.get_session() as session:
                # Use parameterized query to prevent SQL injection
                result = session.execute(text(query), params or {})
                return [dict(row) for row in result]
        except Exception as e:
            self.logger.error(f"Database query error: {e}")
            raise
    
    def insert_data_safely(self, table: str, data: Dict[str, Any]) -> bool:
        """Insert data safely"""
        try:
            # Build parameterized insert query
            columns = ', '.join(data.keys())
            placeholders = ', '.join([f':{key}' for key in data.keys()])
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
            with self.get_session() as session:
                session.execute(text(query), data)
                session.commit()
                return True
        except Exception as e:
            self.logger.error(f"Database insert error: {e}")
            return False
    
    def update_data_safely(self, table: str, data: Dict[str, Any], condition: str, params: Dict[str, Any]) -> bool:
        """Update data safely"""
        try:
            # Build parameterized update query
            set_clause = ', '.join([f"{key} = :{key}" for key in data.keys()])
            query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
            
            # Combine parameters
            all_params = {**data, **params}
            
            with self.get_session() as session:
                session.execute(text(query), all_params)
                session.commit()
                return True
        except Exception as e:
            self.logger.error(f"Database update error: {e}")
            return False

# Usage example
db_manager = SecureDatabaseManager("postgresql://user:pass@localhost/db")

# Safe query execution
users = db_manager.execute_query_safely(
    "SELECT * FROM users WHERE role = :role",
    {"role": "admin"}
)

# Safe data insertion
success = db_manager.insert_data_safely(
    "sensor_data",
    {
        "temperature": 25.5,
        "humidity": 60.0,
        "timestamp": "2024-01-01T12:00:00Z"
    }
)
```

## 🚫 **Rate Limiting & DDoS Protection**

### **1. Rate Limiting Implementation**

```python
import time
import asyncio
from collections import defaultdict
from typing import Dict, Tuple
import logging

class RateLimiter:
    """Rate limiting implementation"""
    
    def __init__(self, requests_per_minute: int = 60, requests_per_hour: int = 1000):
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.minute_requests = defaultdict(list)
        self.hour_requests = defaultdict(list)
        self.logger = logging.getLogger(__name__)
    
    def is_allowed(self, client_id: str) -> Tuple[bool, Dict[str, int]]:
        """Check if request is allowed"""
        current_time = time.time()
        
        # Clean old requests
        self._clean_old_requests(current_time)
        
        # Check minute limit
        minute_count = len(self.minute_requests[client_id])
        if minute_count >= self.requests_per_minute:
            return False, {
                "minute_remaining": 0,
                "hour_remaining": self.requests_per_hour - len(self.hour_requests[client_id])
            }
        
        # Check hour limit
        hour_count = len(self.hour_requests[client_id])
        if hour_count >= self.requests_per_hour:
            return False, {
                "minute_remaining": self.requests_per_minute - minute_count,
                "hour_remaining": 0
            }
        
        # Add current request
        self.minute_requests[client_id].append(current_time)
        self.hour_requests[client_id].append(current_time)
        
        return True, {
            "minute_remaining": self.requests_per_minute - minute_count - 1,
            "hour_remaining": self.requests_per_hour - hour_count - 1
        }
    
    def _clean_old_requests(self, current_time: float):
        """Clean old requests from tracking"""
        # Clean minute requests (older than 60 seconds)
        for client_id in list(self.minute_requests.keys()):
            self.minute_requests[client_id] = [
                req_time for req_time in self.minute_requests[client_id]
                if current_time - req_time < 60
            ]
            if not self.minute_requests[client_id]:
                del self.minute_requests[client_id]
        
        # Clean hour requests (older than 3600 seconds)
        for client_id in list(self.hour_requests.keys()):
            self.hour_requests[client_id] = [
                req_time for req_time in self.hour_requests[client_id]
                if current_time - req_time < 3600
            ]
            if not self.hour_requests[client_id]:
                del self.hour_requests[client_id]

class DDoSProtection:
    """DDoS protection with multiple detection methods"""
    
    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.suspicious_ips = set()
        self.blocked_ips = set()
        self.request_patterns = defaultdict(list)
        self.logger = logging.getLogger(__name__)
    
    def check_request(self, client_ip: str, request_data: Dict[str, Any]) -> bool:
        """Check if request should be allowed"""
        # Check if IP is blocked
        if client_ip in self.blocked_ips:
            self.logger.warning(f"Blocked IP attempted access: {client_ip}")
            return False
        
        # Check rate limiting
        allowed, limits = self.rate_limiter.is_allowed(client_ip)
        if not allowed:
            self.logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            self.suspicious_ips.add(client_ip)
            return False
        
        # Check for suspicious patterns
        if self._is_suspicious_pattern(client_ip, request_data):
            self.logger.warning(f"Suspicious pattern detected for IP: {client_ip}")
            self.suspicious_ips.add(client_ip)
            return False
        
        # Check suspicious IP count
        if len(self.suspicious_ips) > 10:
            self._block_suspicious_ips()
        
        return True
    
    def _is_suspicious_pattern(self, client_ip: str, request_data: Dict[str, Any]) -> bool:
        """Detect suspicious request patterns"""
        current_time = time.time()
        
        # Track request patterns
        self.request_patterns[client_ip].append({
            'time': current_time,
            'endpoint': request_data.get('endpoint', ''),
            'method': request_data.get('method', ''),
            'user_agent': request_data.get('user_agent', '')
        })
        
        # Clean old patterns
        self.request_patterns[client_ip] = [
            pattern for pattern in self.request_patterns[client_ip]
            if current_time - pattern['time'] < 300  # 5 minutes
        ]
        
        patterns = self.request_patterns[client_ip]
        
        # Check for rapid requests to same endpoint
        if len(patterns) > 50:
            endpoint_counts = defaultdict(int)
            for pattern in patterns:
                endpoint_counts[pattern['endpoint']] += 1
            
            for endpoint, count in endpoint_counts.items():
                if count > 20:  # More than 20 requests to same endpoint
                    return True
        
        # Check for missing or suspicious user agent
        suspicious_user_agents = ['', 'curl', 'wget', 'python-requests']
        for pattern in patterns:
            if pattern['user_agent'] in suspicious_user_agents:
                return True
        
        return False
    
    def _block_suspicious_ips(self):
        """Block suspicious IPs"""
        for ip in self.suspicious_ips:
            self.blocked_ips.add(ip)
            self.logger.warning(f"Blocked suspicious IP: {ip}")
        
        self.suspicious_ips.clear()
```

### **2. FastAPI Middleware Integration**

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import time
from typing import Callable

class SecurityMiddleware:
    """Security middleware for FastAPI"""
    
    def __init__(self, app: FastAPI):
        self.app = app
        self.ddos_protection = DDoSProtection()
        self.security_manager = SecurityManager()
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            
            # Get client IP
            client_ip = request.client.host
            
            # Check DDoS protection
            request_data = {
                'endpoint': request.url.path,
                'method': request.method,
                'user_agent': request.headers.get('user-agent', '')
            }
            
            if not self.ddos_protection.check_request(client_ip, request_data):
                return JSONResponse(
                    status_code=429,
                    content={"error": "Too many requests"}
                )
            
            # Add security headers
            async def send_with_headers(message):
                if message["type"] == "http.response.start":
                    message["headers"].extend([
                        (b"X-Content-Type-Options", b"nosniff"),
                        (b"X-Frame-Options", b"DENY"),
                        (b"X-XSS-Protection", b"1; mode=block"),
                        (b"Strict-Transport-Security", b"max-age=31536000; includeSubDomains"),
                        (b"Content-Security-Policy", b"default-src 'self'"),
                        (b"Referrer-Policy", b"strict-origin-when-cross-origin")
                    ])
                await send(message)
            
            await self.app(scope, receive, send_with_headers)
        else:
            await self.app(scope, receive, send)

# Usage in FastAPI app
app = FastAPI()
app.add_middleware(SecurityMiddleware)
```

## 🔐 **Encryption & Key Management**

### **1. Encryption Utilities**

```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import base64
import os
from typing import Optional

class EncryptionManager:
    """Manages encryption and decryption operations"""
    
    def __init__(self, key_file: str = "encryption.key"):
        self.key_file = key_file
        self.key = self._load_or_generate_key()
        self.cipher_suite = Fernet(self.key)
    
    def _load_or_generate_key(self) -> bytes:
        """Load existing key or generate new one"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            return key
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt string data"""
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        return base64.b64encode(encrypted_data).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt string data"""
        encrypted_bytes = base64.b64decode(encrypted_data.encode())
        decrypted_data = self.cipher_suite.decrypt(encrypted_bytes)
        return decrypted_data.decode()
    
    def encrypt_file(self, input_file: str, output_file: str):
        """Encrypt file"""
        with open(input_file, 'rb') as f:
            data = f.read()
        
        encrypted_data = self.cipher_suite.encrypt(data)
        
        with open(output_file, 'wb') as f:
            f.write(encrypted_data)
    
    def decrypt_file(self, input_file: str, output_file: str):
        """Decrypt file"""
        with open(input_file, 'rb') as f:
            encrypted_data = f.read()
        
        decrypted_data = self.cipher_suite.decrypt(encrypted_data)
        
        with open(output_file, 'wb') as f:
            f.write(decrypted_data)

class KeyManager:
    """Manages cryptographic keys"""
    
    def __init__(self, key_directory: str = "keys"):
        self.key_directory = key_directory
        os.makedirs(key_directory, exist_ok=True)
    
    def generate_rsa_key_pair(self, key_name: str, key_size: int = 2048):
        """Generate RSA key pair"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size
        )
        public_key = private_key.public_key()
        
        # Save private key
        private_key_path = os.path.join(self.key_directory, f"{key_name}_private.pem")
        with open(private_key_path, 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        # Save public key
        public_key_path = os.path.join(self.key_directory, f"{key_name}_public.pem")
        with open(public_key_path, 'wb') as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        
        return private_key_path, public_key_path
    
    def load_private_key(self, key_path: str):
        """Load private key from file"""
        with open(key_path, 'rb') as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None
            )
        return private_key
    
    def load_public_key(self, key_path: str):
        """Load public key from file"""
        with open(key_path, 'rb') as f:
            public_key = serialization.load_pem_public_key(f.read())
        return public_key

# Usage example
encryption_manager = EncryptionManager()
key_manager = KeyManager()

# Encrypt sensitive data
sensitive_data = "password123"
encrypted = encryption_manager.encrypt_data(sensitive_data)
decrypted = encryption_manager.decrypt_data(encrypted)

# Generate key pair
private_key_path, public_key_path = key_manager.generate_rsa_key_pair("server")
```

## 📊 **Security Monitoring**

### **1. Security Event Logging**

```python
import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
import hashlib

class SecurityLogger:
    """Security event logging"""
    
    def __init__(self, log_file: str = "security.log"):
        self.logger = logging.getLogger("security")
        self.logger.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
    
    def log_security_event(
        self,
        event_type: str,
        details: Dict[str, Any],
        severity: str = "INFO",
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None
    ):
        """Log security event"""
        event_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "severity": severity,
            "user_id": user_id,
            "ip_address": ip_address,
            "details": details,
            "hash": self._generate_event_hash(event_type, details)
        }
        
        log_message = json.dumps(event_data)
        
        if severity == "ERROR":
            self.logger.error(log_message)
        elif severity == "WARNING":
            self.logger.warning(log_message)
        else:
            self.logger.info(log_message)
    
    def _generate_event_hash(self, event_type: str, details: Dict[str, Any]) -> str:
        """Generate hash for event data"""
        data_string = f"{event_type}:{json.dumps(details, sort_keys=True)}"
        return hashlib.sha256(data_string.encode()).hexdigest()
    
    def log_login_attempt(self, user_id: str, ip_address: str, success: bool):
        """Log login attempt"""
        self.log_security_event(
            event_type="login_attempt",
            details={
                "user_id": user_id,
                "ip_address": ip_address,
                "success": success
            },
            severity="WARNING" if not success else "INFO",
            user_id=user_id,
            ip_address=ip_address
        )
    
    def log_api_access(self, endpoint: str, method: str, user_id: str, ip_address: str):
        """Log API access"""
        self.log_security_event(
            event_type="api_access",
            details={
                "endpoint": endpoint,
                "method": method
            },
            user_id=user_id,
            ip_address=ip_address
        )
    
    def log_security_violation(self, violation_type: str, details: Dict[str, Any], ip_address: str):
        """Log security violation"""
        self.log_security_event(
            event_type="security_violation",
            details={
                "violation_type": violation_type,
                **details
            },
            severity="ERROR",
            ip_address=ip_address
        )

# Usage example
security_logger = SecurityLogger()

# Log security events
security_logger.log_login_attempt("user123", "192.168.1.100", True)
security_logger.log_api_access("/api/v1/sensors", "GET", "user123", "192.168.1.100")
security_logger.log_security_violation("rate_limit_exceeded", {"requests": 100}, "192.168.1.100")
```

---

**Last Updated**: December 2024  
**Version**: 2.0.0
