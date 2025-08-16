# Network Best Practices

**แนวปฏิบัติที่ดีสำหรับการจัดการเครือข่ายและการสื่อสารในโปรเจกต์ IoT**

## 🌐 **Network Architecture**

### **1. Multi-Machine Network Setup**

```
Development Environment:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Your Machine  │    │  Edge Device    │    │  Server Device  │
│   (Windows/Mac/ │◄──►│  (Raspberry Pi) │◄──►│   (Ubuntu)      │
│    Linux)       │    │  aicamera.git   │    │  [Tailscale IP] │
│   Cursor AI     │    │  [Tailscale IP] │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **2. Tailscale VPN Configuration**

```bash
# Install Tailscale on all devices
# Ubuntu Server
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --authkey YOUR_AUTH_KEY

# Raspberry Pi
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --authkey YOUR_AUTH_KEY

# Development Machine
# Download from https://tailscale.com/download
```

## 🔧 **Network Configuration**

### **1. Static IP Configuration**

**Ubuntu Server (`/etc/netplan/01-netcfg.yaml`):**
```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: false
      addresses:
        - 192.168.1.100/24
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
```

**Raspberry Pi (`/etc/dhcpcd.conf`):**
```bash
# Static IP configuration
interface eth0
static ip_address=192.168.1.200/24
static routers=192.168.1.1
static domain_name_servers=8.8.8.8 8.8.4.4

interface wlan0
static ip_address=192.168.1.201/24
static routers=192.168.1.1
static domain_name_servers=8.8.8.8 8.8.4.4
```

### **2. Firewall Configuration**

**Ubuntu Server (`ufw`):**
```bash
# Enable UFW
sudo ufw enable

# Allow SSH
sudo ufw allow ssh

# Allow Tailscale
sudo ufw allow in on tailscale0
sudo ufw allow out on tailscale0

# Allow application ports
sudo ufw allow 8000/tcp  # FastAPI
sudo ufw allow 5432/tcp  # PostgreSQL
sudo ufw allow 6379/tcp  # Redis
sudo ufw allow 1883/tcp  # MQTT
sudo ufw allow 8883/tcp  # MQTT over TLS

# Check status
sudo ufw status verbose
```

**Raspberry Pi (`iptables`):**
```bash
# Basic firewall rules
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 1883 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 8883 -j ACCEPT

# Save rules
sudo iptables-save > /etc/iptables/rules.v4
```

## 📡 **Communication Protocols**

### **1. MQTT Configuration**

**MQTT Client Implementation:**
```python
import paho.mqtt.client as mqtt
import json
import asyncio
from typing import Dict, Any, Callable
import logging

class MQTTClient:
    """MQTT client with connection management and retry logic"""
    
    def __init__(self, broker: str, port: int = 1883, client_id: str = None):
        self.broker = broker
        self.port = port
        self.client_id = client_id or f"client_{id(self)}"
        self.client = mqtt.Client(client_id=self.client_id)
        self.logger = logging.getLogger(__name__)
        self.connected = False
        self.message_handlers = {}
        
        # Setup callbacks
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        
    def _on_connect(self, client, userdata, flags, rc):
        """Handle connection events"""
        if rc == 0:
            self.connected = True
            self.logger.info(f"Connected to MQTT broker: {self.broker}")
        else:
            self.connected = False
            self.logger.error(f"Failed to connect to MQTT broker: {rc}")
    
    def _on_disconnect(self, client, userdata, rc):
        """Handle disconnection events"""
        self.connected = False
        self.logger.warning(f"Disconnected from MQTT broker: {rc}")
    
    def _on_message(self, client, userdata, msg):
        """Handle incoming messages"""
        topic = msg.topic
        payload = msg.payload.decode('utf-8')
        
        if topic in self.message_handlers:
            try:
                data = json.loads(payload)
                self.message_handlers[topic](data)
            except json.JSONDecodeError:
                self.logger.error(f"Invalid JSON payload: {payload}")
    
    async def connect(self, username: str = None, password: str = None):
        """Connect to MQTT broker with authentication"""
        if username and password:
            self.client.username_pw_set(username, password)
        
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            
            # Wait for connection
            for _ in range(10):
                if self.connected:
                    break
                await asyncio.sleep(0.5)
            
            if not self.connected:
                raise ConnectionError("Failed to connect to MQTT broker")
                
        except Exception as e:
            self.logger.error(f"Connection error: {e}")
            raise
    
    async def publish(self, topic: str, data: Dict[str, Any], qos: int = 1):
        """Publish message to topic"""
        if not self.connected:
            raise ConnectionError("Not connected to MQTT broker")
        
        try:
            payload = json.dumps(data)
            result = self.client.publish(topic, payload, qos=qos)
            
            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                raise Exception(f"Failed to publish: {result.rc}")
                
            self.logger.debug(f"Published to {topic}: {payload}")
            
        except Exception as e:
            self.logger.error(f"Publish error: {e}")
            raise
    
    def subscribe(self, topic: str, handler: Callable[[Dict[str, Any]], None]):
        """Subscribe to topic with message handler"""
        self.message_handlers[topic] = handler
        self.client.subscribe(topic)
        self.logger.info(f"Subscribed to topic: {topic}")
    
    async def disconnect(self):
        """Disconnect from MQTT broker"""
        if self.connected:
            self.client.loop_stop()
            self.client.disconnect()
            self.connected = False
            self.logger.info("Disconnected from MQTT broker")
```

### **2. HTTP/2 Configuration**

**FastAPI with HTTP/2 Support:**
```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import ssl
from typing import Dict, Any

app = FastAPI(
    title="LPR Server API",
    description="License Plate Recognition Server",
    version="3.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SSL configuration for HTTP/2
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(
    certfile="certs/server.crt",
    keyfile="certs/server.key"
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "3.0.0"}

@app.post("/api/v1/process")
async def process_image(data: Dict[str, Any]):
    """Process image data"""
    try:
        # Processing logic
        return {"status": "success", "result": "processed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        ssl_keyfile="certs/server.key",
        ssl_certfile="certs/server.crt",
        http="h2"
    )
```

## 🔄 **Connection Resilience**

### **1. Retry Logic Implementation**

```python
import asyncio
import aiohttp
from typing import Any, Callable, Optional
import logging

class NetworkManager:
    """Manages network connections with retry logic"""
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.logger = logging.getLogger(__name__)
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def request_with_retry(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> aiohttp.ClientResponse:
        """Make HTTP request with retry logic"""
        for attempt in range(self.max_retries):
            try:
                if not self.session:
                    raise RuntimeError("Session not initialized")
                
                async with self.session.request(method, url, **kwargs) as response:
                    response.raise_for_status()
                    return response
                    
            except Exception as e:
                self.logger.warning(
                    f"Request failed (attempt {attempt + 1}/{self.max_retries}): {e}"
                )
                
                if attempt == self.max_retries - 1:
                    raise e
                
                # Exponential backoff
                delay = self.base_delay * (2 ** attempt)
                await asyncio.sleep(delay)
        
        raise RuntimeError("Max retries exceeded")
    
    async def send_data_to_server(self, data: Dict[str, Any]) -> bool:
        """Send data to server with retry logic"""
        try:
            async with self.request_with_retry(
                "POST",
                "https://server:8000/api/v1/data",
                json=data
            ) as response:
                result = await response.json()
                return result.get("status") == "success"
                
        except Exception as e:
            self.logger.error(f"Failed to send data: {e}")
            return False
```

### **2. Circuit Breaker Pattern**

```python
import asyncio
from enum import Enum
from typing import Callable, Any
import time

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    """Circuit breaker pattern implementation"""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: type = Exception
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection"""
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
            
        except self.expected_exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        """Handle successful execution"""
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def _on_failure(self):
        """Handle failed execution"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
```

## 📊 **Network Monitoring**

### **1. Connection Health Monitoring**

```python
import asyncio
import aiohttp
import psutil
from typing import Dict, Any
import logging

class NetworkMonitor:
    """Monitors network connectivity and performance"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.endpoints = [
            "https://server:8000/health",
            "mqtt://broker:1883",
            "https://api.github.com"
        ]
    
    async def check_connectivity(self) -> Dict[str, Any]:
        """Check connectivity to all endpoints"""
        results = {}
        
        for endpoint in self.endpoints:
            try:
                start_time = asyncio.get_event_loop().time()
                
                if endpoint.startswith("https://"):
                    async with aiohttp.ClientSession() as session:
                        async with session.get(endpoint, timeout=5) as response:
                            response.raise_for_status()
                            latency = (asyncio.get_event_loop().time() - start_time) * 1000
                            results[endpoint] = {
                                "status": "connected",
                                "latency_ms": round(latency, 2)
                            }
                
                elif endpoint.startswith("mqtt://"):
                    # MQTT connectivity check
                    results[endpoint] = {
                        "status": "connected",
                        "latency_ms": 0
                    }
                    
            except Exception as e:
                results[endpoint] = {
                    "status": "failed",
                    "error": str(e)
                }
        
        return results
    
    def get_network_stats(self) -> Dict[str, Any]:
        """Get network interface statistics"""
        stats = {}
        
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == psutil.AF_INET:
                    stats[interface] = {
                        "ip": addr.address,
                        "netmask": addr.netmask
                    }
        
        return stats
    
    async def monitor_network(self, interval: int = 60):
        """Continuous network monitoring"""
        while True:
            try:
                connectivity = await self.check_connectivity()
                network_stats = self.get_network_stats()
                
                self.logger.info(f"Connectivity: {connectivity}")
                self.logger.info(f"Network stats: {network_stats}")
                
                # Check for issues
                failed_endpoints = [
                    endpoint for endpoint, result in connectivity.items()
                    if result["status"] == "failed"
                ]
                
                if failed_endpoints:
                    self.logger.warning(f"Failed endpoints: {failed_endpoints}")
                
            except Exception as e:
                self.logger.error(f"Network monitoring error: {e}")
            
            await asyncio.sleep(interval)
```

### **2. Network Diagnostics**

```bash
#!/bin/bash
# scripts/network_diagnostics.sh

echo "=== Network Diagnostics ==="

# Check Tailscale status
echo "1. Tailscale Status:"
tailscale status

# Check network interfaces
echo -e "\n2. Network Interfaces:"
ip addr show

# Check routing table
echo -e "\n3. Routing Table:"
ip route show

# Check DNS resolution
echo -e "\n4. DNS Resolution:"
nslookup google.com

# Check connectivity to devices
echo -e "\n5. Connectivity Test:"
ping -c 3 192.168.1.100  # Server
ping -c 3 192.168.1.200  # Edge device

# Check open ports
echo -e "\n6. Open Ports:"
ss -tuln

# Check firewall status
echo -e "\n7. Firewall Status:"
sudo ufw status

echo -e "\n=== Diagnostics Complete ==="
```

## 🔒 **Network Security**

### **1. SSL/TLS Configuration**

```python
import ssl
import certifi
from typing import Optional

def create_ssl_context(
    cert_file: Optional[str] = None,
    key_file: Optional[str] = None,
    ca_file: Optional[str] = None
) -> ssl.SSLContext:
    """Create SSL context for secure connections"""
    
    context = ssl.create_default_context(
        purpose=ssl.Purpose.SERVER_AUTH,
        cafile=ca_file or certifi.where()
    )
    
    if cert_file and key_file:
        context.load_cert_chain(certfile=cert_file, keyfile=key_file)
    
    # Security settings
    context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20')
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    
    return context
```

### **2. Network Access Control**

```python
from typing import List, Set
import ipaddress

class NetworkAccessControl:
    """Network access control for security"""
    
    def __init__(self, allowed_networks: List[str]):
        self.allowed_networks = [
            ipaddress.ip_network(network) for network in allowed_networks
        ]
    
    def is_allowed(self, ip_address: str) -> bool:
        """Check if IP address is allowed"""
        try:
            ip = ipaddress.ip_address(ip_address)
            return any(ip in network for network in self.allowed_networks)
        except ValueError:
            return False
    
    def add_allowed_network(self, network: str):
        """Add allowed network"""
        self.allowed_networks.append(ipaddress.ip_network(network))
    
    def remove_allowed_network(self, network: str):
        """Remove allowed network"""
        network_obj = ipaddress.ip_network(network)
        self.allowed_networks = [
            net for net in self.allowed_networks if net != network_obj
        ]
```

---

**Last Updated**: December 2024  
**Version**: 2.0.0
