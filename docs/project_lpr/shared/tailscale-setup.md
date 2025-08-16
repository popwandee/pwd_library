# Tailscale Setup Guide

**Version:** 2.0.0  
**Last Updated:** 2024-08-16  
**Author:** AI Camera Team  
**Status:** Active

## Overview

คู่มือการตั้งค่า Tailscale VPN สำหรับระบบ AI Camera Edge System เพื่อเชื่อมต่อ Edge devices, LPR Server, และ Development machines อย่างปลอดภัย

## 🏗️ Architecture Overview

### Network Topology
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Edge Device   │    │   LPR Server    │    │  Development    │
│  (Raspberry Pi) │◄──►│   (Ubuntu)      │◄──►│   Machine       │
│   aicamera1     │    │   lprserver     │    │   dev-machine   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Tailscale     │
                    │   Network       │
                    └─────────────────┘
```

### Communication Protocols
- **WebSocket:** Real-time data streaming
- **REST API:** HTTP communication
- **MQTT:** Message queuing
- **SFTP:** Secure file transfer
- **rsync:** File synchronization

## 📋 Prerequisites

### Requirements
- **Tailscale Account** - สมัครที่ [tailscale.com](https://tailscale.com)
- **Admin/Sudo Access** - สำหรับการติดตั้งบนทุกเครื่อง
- **Stable Internet Connection** - สำหรับการเชื่อมต่อ Tailscale
- **Unique Hostnames** - hostname ที่ไม่ซ้ำกันสำหรับแต่ละเครื่อง

### Hardware Requirements
- **Edge Device:** Raspberry Pi 5 (ARM64)
- **Server:** Ubuntu Server (x86_64 หรือ ARM64)
- **Development:** Windows/macOS/Linux

## 🚀 Installation

### Edge Device (Raspberry Pi)

#### 1. Install Tailscale
```bash
# Add Tailscale repository
curl -fsSL https://pkgs.tailscale.com/stable/raspbian/bullseye.noarmor.gpg | sudo tee /usr/share/keyrings/tailscale-archive-keyring.gpg >/dev/null
curl -fsSL https://pkgs.tailscale.com/stable/raspbian/bullseye.tailscale-keyring.list | sudo tee /etc/apt/sources.list.d/tailscale.list

# Update package list
sudo apt update

# Install Tailscale
sudo apt install tailscale
```

#### 2. Configure Hostname
```bash
# Set unique hostname
sudo hostnamectl set-hostname aicamera1

# Update /etc/hosts
echo "127.0.1.1 aicamera1" | sudo tee -a /etc/hosts
```

#### 3. Start Tailscale
```bash
# Start Tailscale with tags
sudo tailscale up --advertise-tags=tag:edge --hostname=aicamera1 --accept-dns=false

# Verify connection
tailscale status
```

#### 4. Auto-connect Service
```bash
# Create auto-connect script
sudo tee /usr/local/bin/tailscale-autoconnect.sh << 'EOF'
#!/bin/bash
if ! tailscale status | grep -q "Connected"; then
    sudo tailscale up --advertise-tags=tag:edge --hostname=aicamera1 --accept-dns=false
fi
EOF

# Make executable
sudo chmod +x /usr/local/bin/tailscale-autoconnect.sh

# Create systemd service
sudo tee /etc/systemd/system/tailscale-autoconnect.service << EOF
[Unit]
Description=Tailscale Auto-Connect
After=network.target
Wants=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/tailscale-autoconnect.sh
User=root

[Install]
WantedBy=multi-user.target
EOF

# Create timer
sudo tee /etc/systemd/system/tailscale-autoconnect.timer << EOF
[Unit]
Description=Run Tailscale Auto-Connect every 5 minutes
Requires=tailscale-autoconnect.service

[Timer]
OnBootSec=1min
OnUnitActiveSec=5min
Unit=tailscale-autoconnect.service

[Install]
WantedBy=timers.target
EOF

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable tailscale-autoconnect.timer
sudo systemctl start tailscale-autoconnect.timer
```

### LPR Server (Ubuntu)

#### 1. Install Tailscale
```bash
# Add Tailscale repository
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/jammy.noarmor.gpg | sudo tee /usr/share/keyrings/tailscale-archive-keyring.gpg >/dev/null
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/jammy.tailscale-keyring.list | sudo tee /etc/apt/sources.list.d/tailscale.list

# Update package list
sudo apt update

# Install Tailscale
sudo apt install tailscale
```

#### 2. Configure Hostname
```bash
# Set unique hostname
sudo hostnamectl set-hostname lprserver

# Update /etc/hosts
echo "127.0.1.1 lprserver" | sudo tee -a /etc/hosts
```

#### 3. Start Tailscale
```bash
# Start Tailscale with tags
sudo tailscale up --advertise-tags=tag:server --hostname=lprserver --accept-dns=false

# Verify connection
tailscale status
```

#### 4. Auto-connect Service
```bash
# Create auto-connect script
sudo tee /usr/local/bin/tailscale-autoconnect.sh << 'EOF'
#!/bin/bash
if ! tailscale status | grep -q "Connected"; then
    sudo tailscale up --advertise-tags=tag:server --hostname=lprserver --accept-dns=false
fi
EOF

# Make executable
sudo chmod +x /usr/local/bin/tailscale-autoconnect.sh

# Create systemd service (same as Edge device)
sudo tee /etc/systemd/system/tailscale-autoconnect.service << EOF
[Unit]
Description=Tailscale Auto-Connect
After=network.target
Wants=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/tailscale-autoconnect.sh
User=root

[Install]
WantedBy=multi-user.target
EOF

# Create timer
sudo tee /etc/systemd/system/tailscale-autoconnect.timer << EOF
[Unit]
Description=Run Tailscale Auto-Connect every 5 minutes
Requires=tailscale-autoconnect.service

[Timer]
OnBootSec=1min
OnUnitActiveSec=5min
Unit=tailscale-autoconnect.service

[Install]
WantedBy=timers.target
EOF

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable tailscale-autoconnect.timer
sudo systemctl start tailscale-autoconnect.timer
```

### Development Machine

#### Windows
1. Download Tailscale from [tailscale.com](https://tailscale.com/download/windows)
2. Install and run
3. Login with your Tailscale account
4. Set hostname to `dev-windows` (or unique name)

#### macOS
```bash
# Install via Homebrew
brew install tailscale

# Start Tailscale
sudo tailscale up --advertise-tags=tag:dev --hostname=dev-macos --accept-dns=false
```

#### Linux
```bash
# Install Tailscale
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/jammy.noarmor.gpg | sudo tee /usr/share/keyrings/tailscale-archive-keyring.gpg >/dev/null
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/jammy.tailscale-keyring.list | sudo tee /etc/apt/sources.list.d/tailscale.list
sudo apt update
sudo apt install tailscale

# Start Tailscale
sudo tailscale up --advertise-tags=tag:dev --hostname=dev-linux --accept-dns=false
```

## 🔧 Configuration

### ACLs Configuration

#### Basic ACLs
```json
{
  "tagOwners": {
    "tag:edge": ["email@gmail.com"],
    "tag:server": ["email@gmail.com"],
    "tag:dev": ["email@gmail.com"]
  },
  "acls": [
    {
      "action": "accept",
      "src": ["tag:edge"],
      "dst": ["tag:server:*"]
    },
    {
      "action": "accept",
      "src": ["tag:server"],
      "dst": ["tag:edge:*"]
    },
    {
      "action": "accept",
      "src": ["tag:server"],
      "dst": ["tag:dev:*"]
    },
    {
      "action": "accept",
      "src": ["tag:dev"],
      "dst": ["tag:server:*"]
    },
    {
      "action": "accept",
      "src": ["tag:edge"],
      "dst": ["tag:dev:*"]
    },
    {
      "action": "accept",
      "src": ["tag:dev"],
      "dst": ["tag:edge:*"]
    }
  ],
  "hosts": {
    "aicamera1": "100.xx.xx.xx",
    "lprserver": "100.xx.xx.xx",
    "dev-machine": "100.xx.xx.xx"
  }
}
```

#### Advanced ACLs with SSH
```json
{
  "tagOwners": {
    "tag:edge": ["email@gmail.com"],
    "tag:server": ["email@gmail.com"],
    "tag:dev": ["email@gmail.com"]
  },
  "groups": {
    "group:ai-camera-team": ["email1@gmail.com", "email2@gmail.com"]
  },
  "acls": [
    {
      "action": "accept",
      "src": ["tag:edge"],
      "dst": ["tag:server:*"]
    },
    {
      "action": "accept",
      "src": ["tag:server"],
      "dst": ["tag:edge:*"]
    },
    {
      "action": "accept",
      "src": ["tag:server"],
      "dst": ["tag:dev:*"]
    },
    {
      "action": "accept",
      "src": ["tag:dev"],
      "dst": ["tag:server:*"]
    },
    {
      "action": "accept",
      "src": ["tag:edge"],
      "dst": ["tag:dev:*"]
    },
    {
      "action": "accept",
      "src": ["tag:dev"],
      "dst": ["tag:edge:*"]
    }
  ],
  "ssh": [
    {
      "action": "accept",
      "src": ["group:ai-camera-team"],
      "dst": ["aicamera1:22", "lprserver:22"],
      "users": ["camuser", "ubuntu"]
    }
  ],
  "hosts": {
    "aicamera1": "100.xx.xx.xx",
    "lprserver": "100.xx.xx.xx",
    "dev-machine": "100.xx.xx.xx"
  }
}
```

### Communication Ports

#### Required Ports
```bash
# WebSocket
8765 - WebSocket server (Edge to Server)

# REST API
8000 - REST API server (Server)
8001 - REST API server (Edge)

# MQTT
1883 - MQTT broker (Server)
8883 - MQTT broker (TLS)

# SFTP
22 - SSH/SFTP

# rsync
22 - SSH (for rsync)

# Health Check
8080 - Health check endpoint
```

#### Firewall Configuration
```bash
# Edge Device (Raspberry Pi)
sudo ufw allow 8001/tcp  # REST API
sudo ufw allow 8765/tcp  # WebSocket
sudo ufw allow 22/tcp    # SSH/SFTP

# LPR Server (Ubuntu)
sudo ufw allow 8000/tcp  # REST API
sudo ufw allow 8765/tcp  # WebSocket
sudo ufw allow 1883/tcp  # MQTT
sudo ufw allow 8883/tcp  # MQTT TLS
sudo ufw allow 22/tcp    # SSH/SFTP
sudo ufw allow 8080/tcp  # Health check
```

## 🔍 Verification

### Connection Test
```bash
# Test connectivity between devices
tailscale ping aicamera1
tailscale ping lprserver
tailscale ping dev-machine

# Test specific ports
nc -zv aicamera1 8001  # Edge REST API
nc -zv lprserver 8000  # Server REST API
nc -zv lprserver 1883  # MQTT broker
```

### Status Check
```bash
# Check Tailscale status
tailscale status

# Check service status
sudo systemctl status tailscaled
sudo systemctl status tailscale-autoconnect.timer

# Check logs
sudo journalctl -u tailscaled -f
sudo journalctl -u tailscale-autoconnect.service -f
```

## 🔄 Integration with Unified Communication

### Protocol Selection
Tailscale VPN รองรับการสื่อสารแบบ Unified Communication Architecture:

#### 1. Real-time Communication
- **WebSocket:** `ws://aicamera1:8765` → `ws://lprserver:8765`
- **MQTT:** `mqtt://lprserver:1883`

#### 2. Request-Response Communication
- **REST API:** `http://aicamera1:8001` → `http://lprserver:8000`

#### 3. File Transfer
- **SFTP:** `sftp://aicamera1` → `sftp://lprserver`
- **rsync:** `rsync://aicamera1` → `rsync://lprserver`

### Configuration Integration
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
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Connection Issues
```bash
# Check Tailscale status
tailscale status

# Restart Tailscale
sudo systemctl restart tailscaled

# Re-authenticate
sudo tailscale up --authkey=YOUR_AUTH_KEY
```

#### 2. Hostname Issues
```bash
# Check hostname
hostname

# Set hostname
sudo hostnamectl set-hostname aicamera1

# Update /etc/hosts
echo "127.0.1.1 aicamera1" | sudo tee -a /etc/hosts
```

#### 3. ACLs Issues
```bash
# Check ACLs in Tailscale Admin Console
# Verify tag assignments
# Check hostname mappings
```

#### 4. Port Issues
```bash
# Check if ports are open
sudo netstat -tlnp | grep :8000
sudo netstat -tlnp | grep :8765
sudo netstat -tlnp | grep :1883

# Check firewall
sudo ufw status
```

### Diagnostic Commands
```bash
# Network diagnostics
tailscale ping lprserver
tailscale status --json

# Service diagnostics
sudo systemctl status tailscaled
sudo journalctl -u tailscaled -n 50

# Connection test
curl -I http://lprserver:8000/health
nc -zv lprserver 8765
```

## 📊 Monitoring

### Health Checks
```bash
# Create health check script
sudo tee /usr/local/bin/tailscale-health-check.sh << 'EOF'
#!/bin/bash
if ! tailscale status | grep -q "Connected"; then
    echo "Tailscale not connected"
    exit 1
fi

if ! tailscale ping lprserver >/dev/null 2>&1; then
    echo "Cannot ping lprserver"
    exit 1
fi

echo "Tailscale health check passed"
exit 0
EOF

sudo chmod +x /usr/local/bin/tailscale-health-check.sh
```

### Logging
```bash
# Enable detailed logging
sudo tailscale up --verbose=1

# Monitor logs
sudo journalctl -u tailscaled -f
sudo journalctl -u tailscale-autoconnect.service -f
```

## 🔒 Security

### Best Practices
1. **Use ACLs** - กำหนดสิทธิ์การเข้าถึงอย่างชัดเจน
2. **Tag-based Access** - ใช้ tags แทน IP addresses
3. **Regular Updates** - อัปเดต Tailscale เป็นประจำ
4. **Monitor Logs** - ติดตาม logs อย่างสม่ำเสมอ
5. **Backup Configuration** - สำรอง configuration

### Security Checklist
- [ ] ACLs configured properly
- [ ] Hostnames are unique
- [ ] Firewall rules configured
- [ ] Services running with proper permissions
- [ ] Logs being monitored
- [ ] Regular updates scheduled

## 📚 References

### Related Documentation
- **[Unified Communication Architecture](unified-communication-architecture.md)** - สถาปัตยกรรมการสื่อสารแบบรวม
- **[Edge Project Overview](../edge/project-overview.md)** - ภาพรวมโปรเจค Edge
- **[Server Documentation](../server/README.md)** - เอกสาร LPR Server

### External Resources
- [Tailscale Documentation](https://tailscale.com/kb/)
- [Tailscale ACLs Reference](https://tailscale.com/kb/1018/acls/)
- [Tailscale SSH](https://tailscale.com/kb/1193/tailscale-ssh/)

---

**Note:** เอกสารนี้จะได้รับการอัปเดตเมื่อมีการเปลี่ยนแปลงในระบบหรือ configuration
