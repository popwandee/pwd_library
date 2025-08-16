# Unified Communication Architecture

**Version:** 1.0.0  
**Last Updated:** 2024-08-16  
**Author:** AI Camera Team  
**Status:** Active

## Overview

Unified Communication Architecture สำหรับ AI Camera Edge System ที่รองรับการสื่อสารแบบหลากหลาย protocol และการส่งไฟล์แบบ flexible

## 🏗️ Architecture Overview

### System Components
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Edge Device   │    │ Unified Comm    │    │   LPR Server    │
│  (Raspberry Pi) │◄──►│   Gateway       │◄──►│   (Ubuntu)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │ Communication   │
                    │   Protocols     │
                    └─────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
    ┌─────────┐            ┌─────────┐            ┌─────────┐
    │WebSocket│            │ REST API│            │  MQTT   │
    └─────────┘            └─────────┘            └─────────┘
         │                       │                       │
    ┌─────────┐            ┌─────────┐            ┌─────────┐
    │  SFTP   │            │ rsync   │            │ Mosquitto│
    └─────────┘            └─────────┘            └─────────┘
```

### Communication Protocols

#### 1. Real-time Communication
- **WebSocket**: สำหรับ real-time updates และ streaming
- **MQTT**: สำหรับ reliable message queuing และ pub/sub

#### 2. Request-Response Communication
- **REST API**: สำหรับ CRUD operations และ configuration

#### 3. File Transfer
- **SFTP**: สำหรับ secure file transfer
- **rsync**: สำหรับ efficient file synchronization

## 🔧 Implementation Details

### Unified Communication Gateway

#### Core Interface
```python
class UnifiedCommunicationGateway:
    def __init__(self, config):
        self.config = config
        self.websocket_client = WebSocketClient(config.websocket)
        self.rest_client = RESTClient(config.rest)
        self.mqtt_client = MQTTClient(config.mqtt)
        self.sftp_client = SFTPClient(config.sftp)
        self.rsync_client = RSyncClient(config.rsync)
        
        # Protocol selection strategies
        self.protocol_selector = ProtocolSelector(config)
        self.fallback_manager = FallbackManager(config)
    
    def send_metadata(self, data, protocol='auto', priority='normal'):
        """Send metadata using specified or auto-selected protocol"""
        try:
            if protocol == 'auto':
                protocol = self.protocol_selector.select_metadata_protocol(data, priority)
            
            result = self._send_via_protocol(data, protocol)
            
            if not result.success and self.fallback_manager.has_fallback(protocol):
                fallback_protocol = self.fallback_manager.get_fallback(protocol)
                result = self._send_via_protocol(data, fallback_protocol)
            
            return result
        except Exception as e:
            logger.error(f"Failed to send metadata: {e}")
            return CommunicationResult(success=False, error=str(e))
    
    def send_file(self, file_path, protocol='auto', priority='normal'):
        """Send file using specified or auto-selected protocol"""
        try:
            if protocol == 'auto':
                protocol = self.protocol_selector.select_file_protocol(file_path, priority)
            
            result = self._send_file_via_protocol(file_path, protocol)
            
            if not result.success and self.fallback_manager.has_fallback(protocol):
                fallback_protocol = self.fallback_manager.get_fallback(protocol)
                result = self._send_file_via_protocol(file_path, fallback_protocol)
            
            return result
        except Exception as e:
            logger.error(f"Failed to send file: {e}")
            return CommunicationResult(success=False, error=str(e))
    
    def _send_via_protocol(self, data, protocol):
        """Send data via specific protocol"""
        if protocol == 'websocket':
            return self.websocket_client.send(data)
        elif protocol == 'rest':
            return self.rest_client.post(data)
        elif protocol == 'mqtt':
            return self.mqtt_client.publish(data)
        else:
            raise ValueError(f"Unsupported protocol: {protocol}")
    
    def _send_file_via_protocol(self, file_path, protocol):
        """Send file via specific protocol"""
        if protocol == 'sftp':
            return self.sftp_client.upload(file_path)
        elif protocol == 'rsync':
            return self.rsync_client.sync(file_path)
        else:
            raise ValueError(f"Unsupported file protocol: {protocol}")
```

#### Protocol Selection Logic
```python
class ProtocolSelector:
    def __init__(self, config):
        self.config = config
        self.network_monitor = NetworkMonitor()
    
    def select_metadata_protocol(self, data, priority='normal'):
        """Auto-select communication protocol for metadata"""
        data_size = len(str(data))
        network_quality = self.network_monitor.get_quality()
        
        # Priority-based selection
        if priority == 'high':
            if network_quality == 'good':
                return 'websocket'  # Fastest for high priority
            else:
                return 'mqtt'  # Most reliable for high priority
        
        # Size-based selection
        if data_size < 1024:  # Small data
            if network_quality == 'good':
                return 'websocket'
            else:
                return 'rest'
        elif data_size < 10000:  # Medium data
            return 'rest'
        else:  # Large data
            return 'mqtt'
    
    def select_file_protocol(self, file_path, priority='normal'):
        """Auto-select file transfer protocol"""
        file_size = os.path.getsize(file_path)
        network_quality = self.network_monitor.get_quality()
        
        # Priority-based selection
        if priority == 'high':
            return 'sftp'  # More reliable for high priority
        
        # Size-based selection
        if file_size < 1024 * 1024:  # < 1MB
            if network_quality == 'good':
                return 'sftp'
            else:
                return 'rsync'
        else:  # >= 1MB
            return 'rsync'  # More efficient for large files
```

#### Fallback Management
```python
class FallbackManager:
    def __init__(self, config):
        self.fallback_map = {
            'websocket': ['rest', 'mqtt'],
            'rest': ['mqtt', 'websocket'],
            'mqtt': ['rest', 'websocket'],
            'sftp': ['rsync'],
            'rsync': ['sftp']
        }
    
    def has_fallback(self, protocol):
        """Check if protocol has fallback options"""
        return protocol in self.fallback_map
    
    def get_fallback(self, protocol):
        """Get primary fallback protocol"""
        if self.has_fallback(protocol):
            return self.fallback_map[protocol][0]
        return None
    
    def get_all_fallbacks(self, protocol):
        """Get all fallback protocols"""
        return self.fallback_map.get(protocol, [])
```

### Protocol Implementations

#### 1. WebSocket Client
```python
class WebSocketClient:
    def __init__(self, config):
        self.server_url = config.server_url
        self.connection = None
        self.reconnect_attempts = config.reconnect_attempts
        self.reconnect_delay = config.reconnect_delay
    
    def connect(self):
        """Establish WebSocket connection"""
        try:
            self.connection = websocket.create_connection(
                self.server_url,
                timeout=30
            )
            return True
        except Exception as e:
            logger.error(f"WebSocket connection failed: {e}")
            return False
    
    def send(self, data):
        """Send data via WebSocket"""
        if not self.connection:
            if not self.connect():
                return CommunicationResult(success=False, error="Connection failed")
        
        try:
            self.connection.send(json.dumps(data))
            return CommunicationResult(success=True)
        except Exception as e:
            logger.error(f"WebSocket send failed: {e}")
            # Try to reconnect
            if self._reconnect():
                return self.send(data)
            return CommunicationResult(success=False, error=str(e))
    
    def _reconnect(self):
        """Attempt to reconnect"""
        for attempt in range(self.reconnect_attempts):
            try:
                time.sleep(self.reconnect_delay * (attempt + 1))
                self.connection = websocket.create_connection(self.server_url)
                return True
            except Exception as e:
                logger.warning(f"Reconnect attempt {attempt + 1} failed: {e}")
        return False
```

#### 2. REST API Client
```python
class RESTClient:
    def __init__(self, config):
        self.base_url = config.base_url
        self.timeout = config.timeout
        self.retry_attempts = config.retry_attempts
        self.session = requests.Session()
        
        # Configure session
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'AI-Camera-Edge/1.0'
        })
    
    def post(self, data, endpoint='/api/lpr/data'):
        """Send data via REST API"""
        for attempt in range(self.retry_attempts):
            try:
                response = self.session.post(
                    f"{self.base_url}{endpoint}",
                    json=data,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    return CommunicationResult(success=True, data=response.json())
                else:
                    logger.warning(f"REST API returned {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                logger.warning(f"REST API attempt {attempt + 1} failed: {e}")
                if attempt < self.retry_attempts - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        
        return CommunicationResult(success=False, error="All retry attempts failed")
```

#### 3. MQTT Client
```python
class MQTTClient:
    def __init__(self, config):
        self.broker_url = config.broker_url
        self.client_id = config.client_id
        self.username = config.username
        self.password = config.password
        self.client = mqtt.Client(client_id=self.client_id)
        
        # Configure client
        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)
        
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_publish = self._on_publish
    
    def connect(self):
        """Connect to MQTT broker"""
        try:
            self.client.connect(self.broker_url, 1883, 60)
            self.client.loop_start()
            return True
        except Exception as e:
            logger.error(f"MQTT connection failed: {e}")
            return False
    
    def publish(self, data, topic='lpr/data', qos=1):
        """Publish data to MQTT topic"""
        try:
            if not self.client.is_connected():
                if not self.connect():
                    return CommunicationResult(success=False, error="Connection failed")
            
            result = self.client.publish(topic, json.dumps(data), qos=qos)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                return CommunicationResult(success=True)
            else:
                return CommunicationResult(success=False, error=f"Publish failed: {result.rc}")
                
        except Exception as e:
            logger.error(f"MQTT publish failed: {e}")
            return CommunicationResult(success=False, error=str(e))
    
    def _on_connect(self, client, userdata, flags, rc):
        """MQTT connection callback"""
        if rc == 0:
            logger.info("MQTT connected successfully")
        else:
            logger.error(f"MQTT connection failed with code: {rc}")
    
    def _on_disconnect(self, client, userdata, rc):
        """MQTT disconnection callback"""
        logger.warning(f"MQTT disconnected with code: {rc}")
    
    def _on_publish(self, client, userdata, mid):
        """MQTT publish callback"""
        logger.debug(f"MQTT message published with ID: {mid}")
```

#### 4. SFTP Client
```python
class SFTPClient:
    def __init__(self, config):
        self.host = config.host
        self.username = config.username
        self.password = config.password
        self.key_file = config.key_file
        self.remote_path = config.remote_path
    
    def upload(self, local_path, remote_path=None):
        """Upload file via SFTP"""
        transport = None
        try:
            # Create transport
            transport = paramiko.Transport((self.host, 22))
            
            # Authenticate
            if self.key_file:
                transport.connect(username=self.username, key_filename=self.key_file)
            else:
                transport.connect(username=self.username, password=self.password)
            
            # Create SFTP client
            sftp = paramiko.SFTPClient.from_transport(transport)
            
            # Determine remote path
            if remote_path is None:
                remote_path = os.path.join(self.remote_path, os.path.basename(local_path))
            
            # Upload file
            sftp.put(local_path, remote_path)
            
            # Close connections
            sftp.close()
            transport.close()
            
            return CommunicationResult(success=True)
            
        except Exception as e:
            logger.error(f"SFTP upload failed: {e}")
            if transport:
                transport.close()
            return CommunicationResult(success=False, error=str(e))
```

#### 5. rsync Client
```python
class RSyncClient:
    def __init__(self, config):
        self.remote_host = config.remote_host
        self.remote_user = config.remote_user
        self.remote_path = config.remote_path
        self.options = config.options or ['-azP']
    
    def sync(self, local_path):
        """Sync file via rsync"""
        try:
            # Build rsync command
            cmd = ['rsync'] + self.options + [
                local_path,
                f"{self.remote_user}@{self.remote_host}:{self.remote_path}"
            ]
            
            # Execute rsync
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode == 0:
                return CommunicationResult(success=True)
            else:
                logger.error(f"rsync failed: {result.stderr}")
                return CommunicationResult(success=False, error=result.stderr)
                
        except subprocess.TimeoutExpired:
            logger.error("rsync timeout")
            return CommunicationResult(success=False, error="Timeout")
        except Exception as e:
            logger.error(f"rsync sync failed: {e}")
            return CommunicationResult(success=False, error=str(e))
```

### Configuration Management

#### Configuration Structure
```python
@dataclass
class CommunicationConfig:
    # WebSocket configuration
    websocket: WebSocketConfig
    
    # REST API configuration
    rest: RESTConfig
    
    # MQTT configuration
    mqtt: MQTTConfig
    
    # SFTP configuration
    sftp: SFTPConfig
    
    # rsync configuration
    rsync: RSyncConfig
    
    # Protocol selection configuration
    protocol_selection: ProtocolSelectionConfig
    
    # Fallback configuration
    fallback: FallbackConfig

@dataclass
class WebSocketConfig:
    server_url: str
    reconnect_attempts: int = 3
    reconnect_delay: int = 5

@dataclass
class RESTConfig:
    base_url: str
    timeout: int = 30
    retry_attempts: int = 3

@dataclass
class MQTTConfig:
    broker_url: str
    client_id: str
    username: str = None
    password: str = None

@dataclass
class SFTPConfig:
    host: str
    username: str
    password: str = None
    key_file: str = None
    remote_path: str = "/data/lpr_images"

@dataclass
class RSyncConfig:
    remote_host: str
    remote_user: str
    remote_path: str = "/data/lpr_images"
    options: List[str] = None
```

#### Configuration Loading
```python
def load_communication_config(config_path: str) -> CommunicationConfig:
    """Load communication configuration from file"""
    with open(config_path, 'r') as f:
        config_data = yaml.safe_load(f)
    
    return CommunicationConfig(
        websocket=WebSocketConfig(**config_data['websocket']),
        rest=RESTConfig(**config_data['rest']),
        mqtt=MQTTConfig(**config_data['mqtt']),
        sftp=SFTPConfig(**config_data['sftp']),
        rsync=RSyncConfig(**config_data['rsync']),
        protocol_selection=ProtocolSelectionConfig(**config_data['protocol_selection']),
        fallback=FallbackConfig(**config_data['fallback'])
    )
```

### Monitoring and Logging

#### Communication Monitoring
```python
class CommunicationMonitor:
    def __init__(self):
        self.metrics = {
            'websocket': {'success': 0, 'failure': 0, 'latency': []},
            'rest': {'success': 0, 'failure': 0, 'latency': []},
            'mqtt': {'success': 0, 'failure': 0, 'latency': []},
            'sftp': {'success': 0, 'failure': 0, 'latency': []},
            'rsync': {'success': 0, 'failure': 0, 'latency': []}
        }
    
    def record_communication(self, protocol: str, success: bool, latency: float):
        """Record communication metrics"""
        if protocol in self.metrics:
            if success:
                self.metrics[protocol]['success'] += 1
            else:
                self.metrics[protocol]['failure'] += 1
            
            self.metrics[protocol]['latency'].append(latency)
    
    def get_protocol_stats(self, protocol: str) -> Dict:
        """Get statistics for specific protocol"""
        if protocol in self.metrics:
            stats = self.metrics[protocol]
            total = stats['success'] + stats['failure']
            success_rate = stats['success'] / total if total > 0 else 0
            avg_latency = sum(stats['latency']) / len(stats['latency']) if stats['latency'] else 0
            
            return {
                'success_rate': success_rate,
                'total_attempts': total,
                'average_latency': avg_latency
            }
        return {}
    
    def get_overall_stats(self) -> Dict:
        """Get overall communication statistics"""
        return {
            protocol: self.get_protocol_stats(protocol)
            for protocol in self.metrics.keys()
        }
```

## 📊 Performance Optimization

### Protocol Selection Strategies

#### 1. Network Quality-Based Selection
```python
class NetworkMonitor:
    def __init__(self):
        self.quality_history = []
        self.max_history = 100
    
    def get_quality(self) -> str:
        """Get current network quality"""
        if not self.quality_history:
            return 'unknown'
        
        recent_quality = self.quality_history[-10:]  # Last 10 measurements
        avg_latency = sum(q['latency'] for q in recent_quality) / len(recent_quality)
        avg_loss = sum(q['packet_loss'] for q in recent_quality) / len(recent_quality)
        
        if avg_latency < 50 and avg_loss < 0.01:
            return 'excellent'
        elif avg_latency < 100 and avg_loss < 0.05:
            return 'good'
        elif avg_latency < 200 and avg_loss < 0.1:
            return 'fair'
        else:
            return 'poor'
    
    def measure_quality(self):
        """Measure current network quality"""
        # Measure latency to server
        latency = self._measure_latency()
        
        # Measure packet loss
        packet_loss = self._measure_packet_loss()
        
        quality = {
            'timestamp': time.time(),
            'latency': latency,
            'packet_loss': packet_loss
        }
        
        self.quality_history.append(quality)
        
        # Keep only recent history
        if len(self.quality_history) > self.max_history:
            self.quality_history.pop(0)
    
    def _measure_latency(self) -> float:
        """Measure network latency"""
        # Implementation depends on target server
        pass
    
    def _measure_packet_loss(self) -> float:
        """Measure packet loss rate"""
        # Implementation depends on target server
        pass
```

#### 2. Load Balancing
```python
class LoadBalancer:
    def __init__(self, protocols: List[str]):
        self.protocols = protocols
        self.usage_count = {protocol: 0 for protocol in protocols}
    
    def select_protocol(self, data_size: int, priority: str) -> str:
        """Select protocol based on load balancing"""
        # For high priority, prefer fastest protocol
        if priority == 'high':
            return self._get_fastest_protocol(data_size)
        
        # For normal priority, use round-robin
        return self._get_next_protocol()
    
    def _get_fastest_protocol(self, data_size: int) -> str:
        """Get fastest protocol for given data size"""
        if data_size < 1024:
            return 'websocket'
        elif data_size < 10000:
            return 'rest'
        else:
            return 'mqtt'
    
    def _get_next_protocol(self) -> str:
        """Get next protocol using round-robin"""
        min_usage = min(self.usage_count.values())
        candidates = [p for p, count in self.usage_count.items() if count == min_usage]
        
        selected = candidates[0]
        self.usage_count[selected] += 1
        
        return selected
```

## 🔒 Security Considerations

### Authentication and Authorization
```python
class SecurityManager:
    def __init__(self, config):
        self.config = config
        self.jwt_secret = config.jwt_secret
        self.api_keys = config.api_keys
    
    def authenticate_request(self, request_data: Dict) -> bool:
        """Authenticate communication request"""
        # Check API key
        api_key = request_data.get('api_key')
        if api_key not in self.api_keys:
            return False
        
        # Check JWT token if present
        jwt_token = request_data.get('jwt_token')
        if jwt_token and not self._verify_jwt(jwt_token):
            return False
        
        return True
    
    def _verify_jwt(self, token: str) -> bool:
        """Verify JWT token"""
        try:
            jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            return True
        except jwt.InvalidTokenError:
            return False
```

### Encryption
```python
class EncryptionManager:
    def __init__(self, config):
        self.encryption_key = config.encryption_key
    
    def encrypt_data(self, data: Dict) -> str:
        """Encrypt sensitive data"""
        json_data = json.dumps(data)
        cipher = AES.new(self.encryption_key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(json_data.encode())
        
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode()
    
    def decrypt_data(self, encrypted_data: str) -> Dict:
        """Decrypt sensitive data"""
        data = base64.b64decode(encrypted_data.encode())
        nonce = data[:12]
        tag = data[12:28]
        ciphertext = data[28:]
        
        cipher = AES.new(self.encryption_key, AES.MODE_GCM, nonce=nonce)
        json_data = cipher.decrypt_and_verify(ciphertext, tag)
        
        return json.loads(json_data.decode())
```

## 📈 Monitoring and Analytics

### Real-time Monitoring
```python
class CommunicationDashboard:
    def __init__(self):
        self.monitor = CommunicationMonitor()
        self.network_monitor = NetworkMonitor()
    
    def get_dashboard_data(self) -> Dict:
        """Get data for communication dashboard"""
        return {
            'protocol_stats': self.monitor.get_overall_stats(),
            'network_quality': self.network_monitor.get_quality(),
            'active_connections': self._get_active_connections(),
            'recent_errors': self._get_recent_errors()
        }
    
    def _get_active_connections(self) -> Dict:
        """Get count of active connections by protocol"""
        # Implementation depends on specific protocols
        pass
    
    def _get_recent_errors(self) -> List:
        """Get recent communication errors"""
        # Implementation depends on logging system
        pass
```

## 🚀 Deployment and Configuration

### Environment Configuration
```yaml
# communication_config.yaml
websocket:
  server_url: "ws://lprserver:8765"
  reconnect_attempts: 3
  reconnect_delay: 5

rest:
  base_url: "http://lprserver:8000"
  timeout: 30
  retry_attempts: 3

mqtt:
  broker_url: "lprserver"
  client_id: "aicamera-edge-001"
  username: "edge_user"
  password: "secure_password"

sftp:
  host: "lprserver"
  username: "edge_user"
  key_file: "/home/camuser/.ssh/id_rsa"
  remote_path: "/data/lpr_images"

rsync:
  remote_host: "lprserver"
  remote_user: "edge_user"
  remote_path: "/data/lpr_images"
  options: ["-azP", "--delete"]

protocol_selection:
  auto_select: true
  priority_based: true
  network_aware: true

fallback:
  enabled: true
  max_attempts: 3
```

### Systemd Service Configuration
```ini
# /etc/systemd/system/unified-communication.service
[Unit]
Description=Unified Communication Gateway
After=network.target
Wants=network.target

[Service]
Type=simple
User=camuser
Group=camuser
WorkingDirectory=/home/camuser/aicamera
Environment=PATH=/home/camuser/aicamera/venv_hailo/bin
ExecStart=/home/camuser/aicamera/venv_hailo/bin/python unified_communication.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

**Note:** Unified Communication Architecture นี้รองรับการขยายระบบและเพิ่ม protocol ใหม่ได้ในอนาคต
