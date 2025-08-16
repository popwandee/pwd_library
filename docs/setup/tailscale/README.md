# Tailscale Setup Guide

**Version:** 1.0.0  
**Last Updated:** 2024-08-16  
**Author:** Edge AI Team  
**Category:** Setup - Tailscale  
**Status:** Active

## Overview

คู่มือการตั้งค่า Tailscale VPN สำหรับระบบ Edge AI เพื่อเชื่อมต่อ Edge devices, Server, และ Development machines อย่างปลอดภัย

## 📋 Prerequisites

### Requirements
- **Tailscale Account** - สมัครที่ [tailscale.com](https://tailscale.com)
- **Admin/Sudo Access** - สำหรับการติดตั้งบนทุกเครื่อง
- **Network Access** - สำหรับการดาวน์โหลดและติดตั้ง
- **Unique Hostnames** - สำหรับแต่ละเครื่อง

### Hostname Convention
- **Edge Devices:** `aicamera1`, `aicamera2`, etc.
- **Server:** `lprserver`, `lpr-server1`, etc.
- **Development:** `dev-windows`, `dev-mac`, `dev-linux`, etc.

## 🚀 Installation Steps

### Step 1: Install Tailscale

#### Ubuntu/Debian (Server & Edge)
```bash
# Add Tailscale repository
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/jammy.noarmor.gpg | sudo tee /usr/share/keyrings/tailscale-archive-keyring.gpg >/dev/null
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/jammy.tailscale-keyring.list | sudo tee /etc/apt/sources.list.d/tailscale.list

# Install Tailscale
sudo apt update
sudo apt install tailscale

# Start Tailscale
sudo systemctl start tailscaled
sudo systemctl enable tailscaled
```

#### Raspberry Pi OS (Edge)
```bash
# Add Tailscale repository
curl -fsSL https://pkgs.tailscale.com/stable/raspbian/bullseye.noarmor.gpg | sudo tee /usr/share/keyrings/tailscale-archive-keyring.gpg >/dev/null
curl -fsSL https://pkgs.tailscale.com/stable/raspbian/bullseye.tailscale-keyring.list | sudo tee /etc/apt/sources.list.d/tailscale.list

# Install Tailscale
sudo apt update
sudo apt install tailscale

# Start Tailscale
sudo systemctl start tailscaled
sudo systemctl enable tailscaled
```

#### Windows (Development)
```bash
# Download from tailscale.com
# หรือใช้ winget
winget install Tailscale.Tailscale

# หรือใช้ Chocolatey
choco install tailscale
```

#### macOS (Development)
```bash
# Install with Homebrew
brew install tailscale

# หรือดาวน์โหลดจาก tailscale.com
```

### Step 2: Configure Hostname

#### Linux (Server & Edge)
```bash
# Set hostname
sudo hostnamectl set-hostname <your-hostname>
echo "<your-hostname>" | sudo tee /etc/hostname

# Update hosts file
echo "127.0.1.1 <your-hostname>" | sudo tee -a /etc/hosts

# Reboot to apply changes
sudo reboot
```

#### Windows (Development)
```powershell
# Set hostname
Rename-Computer -NewName "<your-hostname>" -Restart
```

#### macOS (Development)
```bash
# Set hostname
sudo scutil --set HostName "<your-hostname>"
sudo scutil --set LocalHostName "<your-hostname>"
sudo scutil --set ComputerName "<your-hostname>"
```

### Step 3: Get Auth Key

```bash
# Get auth key from Tailscale Admin Console
# ไปที่ https://login.tailscale.com/admin/settings/keys
# สร้าง auth key และคัดลอกมา

# หรือใช้ command line (if available)
tailscale up --auth-key=YOUR_AUTH_KEY
```

### Step 4: Connect to Tailscale

```bash
# Connect with auth key
sudo tailscale up --auth-key=YOUR_AUTH_KEY --hostname=<your-hostname>

# หรือ connect interactively
sudo tailscale up --hostname=<your-hostname>
```

### Step 5: Verify Connection

```bash
# Check Tailscale status
tailscale status

# Check IP address
tailscale ip

# Test connectivity
tailscale ping <other-hostname>
```

## ⚙️ Configuration

### Auto-Connect Service

สร้างไฟล์ service สำหรับ auto-connect:

```bash
# Create auto-connect service
sudo tee /etc/systemd/system/tailscale-autoconnect.service > /dev/null <<EOF
[Unit]
Description=Tailscale Auto-Connect
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/bin/tailscale up --authkey=YOUR_AUTH_KEY --hostname=HOSTNAME --advertise-tags=tag:edge
ExecStop=/usr/bin/tailscale down
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF

# Enable service
sudo systemctl enable tailscale-autoconnect.service
sudo systemctl start tailscale-autoconnect.service
```

### Environment Configuration

สร้างไฟล์ `.env` สำหรับ Tailscale configuration:

```bash
# Tailscale Configuration
TAILSCALE_HOSTNAME=<your-hostname>
TAILSCALE_AUTH_KEY=<your-auth-key>
TAILSCALE_TAGS=tag:edge,tag:server,tag:dev

# Network Configuration
SERVER_HOST=lprserver
EDGE_HOST=aicamera1
DEV_HOST=dev-linux
```

### ACLs Configuration

ตั้งค่า ACLs ใน Tailscale Admin Console:

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
      "src": ["tag:dev"],
      "dst": ["tag:edge:*", "tag:server:*"]
    }
  ],
  "ssh": [
    {
      "action": "accept",
      "src": ["tag:dev"],
      "dst": ["aicamera1:22"],
      "users": ["camuser"]
    },
    {
      "action": "accept",
      "src": ["tag:dev"],
      "dst": ["lprserver:22"],
      "users": ["ubuntu"]
    }
  ],
  "hosts": {
    "aicamera1": "100.xx.xx.xx",
    "lprserver": "100.xx.xx.xx",
    "dev-windows": "100.xx.xx.xx",
    "dev-mac": "100.xx.xx.xx",
    "dev-linux": "100.xx.xx.xx"
  }
}
```

## 🔧 Verification

### Step 1: Check Installation

```bash
# Check Tailscale installation
tailscale --version

# Check service status
sudo systemctl status tailscaled
sudo systemctl status tailscale-autoconnect

# Check hostname
hostname
hostnamectl
```

### Step 2: Check Connection

```bash
# Check Tailscale status
tailscale status

# Check IP address
tailscale ip

# Check routes
tailscale netcheck
```

### Step 3: Test Connectivity

```bash
# Test ping to other devices
tailscale ping aicamera1
tailscale ping lprserver
tailscale ping dev-linux

# Test DNS resolution
nslookup aicamera1
nslookup lprserver
```

### Step 4: Test SSH Access

```bash
# Test SSH to Edge device
ssh camuser@aicamera1

# Test SSH to Server
ssh ubuntu@lprserver

# Test SSH with specific user
ssh -l camuser aicamera1
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Tailscale Not Starting
```bash
# Check service status
sudo systemctl status tailscaled

# Check logs
sudo journalctl -u tailscaled -f

# Restart service
sudo systemctl restart tailscaled
```

#### 2. Connection Issues
```bash
# Check Tailscale status
tailscale status

# Check network connectivity
tailscale netcheck

# Restart Tailscale
sudo tailscale down
sudo tailscale up --auth-key=YOUR_AUTH_KEY
```

#### 3. Hostname Issues
```bash
# Check hostname
hostname
hostnamectl

# Check hosts file
cat /etc/hosts

# Check DNS resolution
nslookup <hostname>
```

#### 4. ACLs Issues
```bash
# Check ACLs in Admin Console
# ไปที่ https://login.tailscale.com/admin/acls

# Check device tags
tailscale status --json | jq '.Peer[] | {Hostname: .HostName, Tags: .Tags}'
```

### Diagnostic Commands

```bash
# System information
uname -a
cat /etc/os-release

# Network information
ip addr show
ip route show

# Tailscale information
tailscale status --json
tailscale netcheck --json

# Service information
sudo systemctl status tailscaled
sudo journalctl -u tailscaled --no-pager
```

## 📊 Monitoring

### Health Check Script

สร้างสคริปต์ health check:

```bash
#!/bin/bash
# /usr/local/bin/tailscale-health-check.sh

HOSTNAME=$(hostname)
LOG_FILE="/var/log/tailscale-health.log"

# Check Tailscale status
if ! tailscale status > /dev/null 2>&1; then
    echo "$(date): Tailscale not running on $HOSTNAME" >> $LOG_FILE
    sudo systemctl restart tailscaled
    exit 1
fi

# Check connectivity to other devices
for device in aicamera1 lprserver; do
    if ! tailscale ping -c 1 $device > /dev/null 2>&1; then
        echo "$(date): Cannot ping $device from $HOSTNAME" >> $LOG_FILE
    fi
done

echo "$(date): Tailscale health check passed on $HOSTNAME" >> $LOG_FILE
```

### Cron Job

```bash
# Add to crontab
sudo crontab -e

# Add this line to run every 5 minutes
*/5 * * * * /usr/local/bin/tailscale-health-check.sh
```

### Monitoring Commands

```bash
# Monitor Tailscale status
watch -n 5 tailscale status

# Monitor connectivity
watch -n 10 'tailscale ping -c 1 aicamera1 && tailscale ping -c 1 lprserver'

# Monitor logs
tail -f /var/log/tailscale-health.log
sudo journalctl -u tailscaled -f
```

## 🔒 Security Configuration

### Firewall Rules

```bash
# Install UFW
sudo apt install ufw

# Configure firewall rules
sudo ufw allow 22/tcp
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

### Access Control

```bash
# Set up user groups
sudo usermod -a -G sudo camuser
sudo usermod -a -G sudo ubuntu

# Configure sudo access
echo "camuser ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/camuser
echo "ubuntu ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/ubuntu
```

## 📚 References

### Official Documentation
- [Tailscale Documentation](https://tailscale.com/kb/)
- [Tailscale ACLs](https://tailscale.com/kb/1018/acls/)
- [Tailscale SSH](https://tailscale.com/kb/1193/tailscale-ssh/)

### Best Practices
- [Network Security Best Practices](https://www.nist.gov/cyberframework)
- [SSH Security Best Practices](https://www.ssh.com/academy/ssh/security)

---

**Note:** เอกสารนี้เป็นคู่มือการตั้งค่า Tailscale สำหรับระบบ Edge AI
