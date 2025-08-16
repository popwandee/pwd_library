# Setup and Configuration Guide - Overview

**Version:** 1.0.0  
**Last Updated:** 2024-08-16  
**Author:** Edge AI Team  
**Category:** Setup & Configuration  
**Status:** Active

## Overview

คู่มือการตั้งค่าและ configuration สำหรับระบบ Edge AI ที่ครอบคลุมการตั้งค่าทุกเทคโนโลยีที่จำเป็น

## 📋 Setup Categories

### Network and Security
- **[Tailscale Setup](tailscale/README.md)** - การตั้งค่า Tailscale VPN
- **[Security Setup](security/README.md)** - การตั้งค่าความปลอดภัย

### Communication Protocols
- **[WebSocket Setup](websocket/README.md)** - การตั้งค่า WebSocket communication
- **[REST API Setup](rest-api/README.md)** - การตั้งค่า REST API
- **[MQTT Setup](mqtt/README.md)** - การตั้งค่า MQTT messaging

## 🚀 Quick Start

### For New Setup
1. **Network**: เริ่มจาก [Tailscale Setup](tailscale/README.md)
2. **Security**: ตั้งค่า [Security Configuration](security/README.md)
3. **Communication**: ตั้งค่า [REST API](rest-api/README.md) และ [WebSocket](websocket/README.md)
4. **Messaging**: ตั้งค่า [MQTT](mqtt/README.md) (ถ้าจำเป็น)

### For Existing Setup
1. **Verify Network**: ตรวจสอบ [Tailscale Configuration](tailscale/README.md)
2. **Update Security**: อัปเดต [Security Settings](security/README.md)
3. **Test Communication**: ทดสอบ [REST API](rest-api/README.md) และ [WebSocket](websocket/README.md)

## 📊 System Architecture

### Network Layer
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Edge      │    │   Server    │    │   Dev       │
│  Device     │    │             │    │  Machine    │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    ┌─────────────┐
                    │  Tailscale  │
                    │     VPN     │
                    └─────────────┘
```

### Communication Layer
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Edge      │    │   Server    │    │   Dev       │
│  Device     │    │             │    │  Machine    │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       ├─── REST API ──────┤                   │
       ├─── WebSocket ─────┤                   │
       └─── MQTT ──────────┘                   │
```

## 🔧 Prerequisites

### Common Requirements
- **Tailscale Account** - สำหรับ VPN connectivity
- **Network Access** - สำหรับการติดตั้งและ configuration
- **Admin/Sudo Access** - สำหรับการตั้งค่าระบบ
- **Domain Names** - สำหรับ SSL certificates (optional)

### Platform-Specific Requirements
- **Edge:** Hailo TAPPAS, PiCamera2
- **Server:** PostgreSQL, Nginx, Redis
- **Development:** Python 3.10+, Git, IDE

## 📝 Setup Checklist

### Network Setup
- [ ] Tailscale installation
- [ ] Hostname configuration
- [ ] ACLs setup
- [ ] DNS configuration
- [ ] Firewall rules

### Security Setup
- [ ] SSL/TLS certificates
- [ ] Authentication system
- [ ] Authorization rules
- [ ] Encryption configuration
- [ ] Security monitoring

### Communication Setup
- [ ] REST API endpoints
- [ ] WebSocket connections
- [ ] MQTT broker (if needed)
- [ ] Rate limiting
- [ ] Error handling

## 🔗 Cross-Platform Configuration

### Environment Variables
```bash
# Common Environment Variables
TAILSCALE_HOSTNAME=<device-name>
TAILSCALE_AUTH_KEY=<auth-key>
SERVER_HOST=<server-hostname>
EDGE_HOST=<edge-hostname>

# REST API Configuration
API_BASE_URL=http://<server-host>:8000/api
API_TIMEOUT=30
API_RETRY_ATTEMPTS=3

# WebSocket Configuration
WS_URL=ws://<server-host>:8765
WS_RECONNECT_INTERVAL=5
WS_MAX_RECONNECT_ATTEMPTS=10

# MQTT Configuration (if used)
MQTT_BROKER=<mqtt-broker-host>
MQTT_PORT=1883
MQTT_USERNAME=<username>
MQTT_PASSWORD=<password>

# Security Configuration
SECRET_KEY=<secret-key>
JWT_SECRET_KEY=<jwt-secret>
CORS_ORIGINS=<allowed-origins>
```

### Configuration Files

#### Tailscale Configuration
```bash
# /etc/systemd/system/tailscale-autoconnect.service
[Unit]
Description=Tailscale Auto-Connect
After=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/bin/tailscale up --authkey=YOUR_AUTH_KEY --hostname=HOSTNAME
```

#### WebSocket Configuration
```python
# websocket_config.py
WEBSOCKET_CONFIG = {
    'host': '0.0.0.0',
    'port': 8765,
    'cors_origins': ['*'],
    'ping_interval': 25,
    'ping_timeout': 10,
    'max_connections': 100
}
```

#### REST API Configuration
```python
# api_config.py
API_CONFIG = {
    'host': '0.0.0.0',
    'port': 8000,
    'debug': False,
    'threaded': True,
    'rate_limit': '100/minute',
    'cors_origins': ['*']
}
```

## 🛠️ Troubleshooting

### Common Issues

#### Network Connectivity
- **Tailscale not connecting**: ตรวจสอบ auth key และ ACLs
- **Hostname resolution**: ตรวจสอบ DNS configuration
- **Firewall blocking**: ตรวจสอบ firewall rules

#### Communication Issues
- **REST API timeout**: ตรวจสอบ network latency และ timeout settings
- **WebSocket disconnection**: ตรวจสอบ ping/pong settings
- **MQTT connection lost**: ตรวจสอบ broker configuration

#### Security Issues
- **SSL certificate errors**: ตรวจสอบ certificate validity
- **Authentication failures**: ตรวจสอบ credentials และ JWT tokens
- **CORS errors**: ตรวจสอบ CORS configuration

### Diagnostic Commands

```bash
# Network diagnostics
ping <hostname>
nslookup <hostname>
traceroute <hostname>

# Tailscale diagnostics
tailscale status
tailscale ping <hostname>
tailscale netcheck

# Service diagnostics
sudo systemctl status <service-name>
sudo journalctl -u <service-name> -f

# Port diagnostics
netstat -tlnp
ss -tlnp
```

## 📊 Monitoring

### Network Monitoring
```bash
# Monitor Tailscale status
watch -n 5 tailscale status

# Monitor network connectivity
watch -n 10 ping -c 1 <hostname>

# Monitor service status
watch -n 5 systemctl status <service-name>
```

### Communication Monitoring
```bash
# Monitor REST API
curl -f http://<hostname>:8000/health

# Monitor WebSocket
python3 -c "
import websocket
ws = websocket.create_connection('ws://<hostname>:8765')
print('WebSocket connected')
ws.close()
"

# Monitor MQTT (if used)
mosquitto_pub -h <broker> -t test/topic -m "test message"
```

## 🔒 Security Best Practices

### Network Security
- ใช้ Tailscale ACLs อย่างเหมาะสม
- เปิดใช้งาน firewall rules
- ใช้ strong authentication
- ตรวจสอบ logs เป็นประจำ

### Communication Security
- ใช้ HTTPS สำหรับ REST API
- ใช้ WSS สำหรับ WebSocket
- ใช้ TLS สำหรับ MQTT
- ตรวจสอบ rate limiting

### Data Security
- เข้ารหัสข้อมูลที่สำคัญ
- ใช้ secure key management
- ตรวจสอบ access logs
- อัปเดต security patches

## 📚 References

### Official Documentation
- [Tailscale Documentation](https://tailscale.com/kb/)
- [WebSocket Documentation](https://websockets.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MQTT Documentation](https://mqtt.org/documentation)

### Best Practices
- [Network Security Best Practices](https://www.nist.gov/cyberframework)
- [API Security Best Practices](https://owasp.org/www-project-api-security/)
- [WebSocket Security](https://websocket.org/echo.html)

---

**Note:** เอกสารนี้เป็น overview สำหรับการตั้งค่าและ configuration ระบบ Edge AI
