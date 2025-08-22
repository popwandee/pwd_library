รวมคำสั่ง Linux ที่เกี่ยวข้องกับ `systemd` สำหรับการบริหารจัดการ service อย่างครบถ้วน เหมาะใช้เป็น cheat sheet ระหว่างการพัฒนาระบบหรือ debug ระบบที่ใช้ service-based architecture:

---

```markdown
# ⚙️ Linux Systemd Service Management Cheat Sheet

## 📦 การสร้าง Service

1. 📁 สร้างไฟล์ service
   ```bash
   sudo nano /etc/systemd/system/<service_name>.service
   ```

2. 📝 ตัวอย่างเนื้อหาไฟล์ `.service`
   ```ini
   [Unit]
   Description=My Custom Service
   After=network.target

   [Service]
   ExecStart=/usr/bin/python3 /path/to/script.py
   Restart=always
   User=root

   [Install]
   WantedBy=multi-user.target
   ```

3. 🚀 โหลด service เข้าระบบ
   ```bash
   sudo systemctl daemon-reexec
   sudo systemctl daemon-reload
   ```

4. ✅ เปิดใช้งานให้รันอัตโนมัติเมื่อบูต
   ```bash
   sudo systemctl enable <service_name>
   ```

---

## 🔍 การตรวจสอบสถานะ

- `systemctl status <service_name>`  
  ดูสถานะการทำงานของ service

- `journalctl -u <service_name>`  
  ดู log ที่เกี่ยวข้องกับ service

- `systemctl list-units --type=service`  
  แสดงรายการ service ที่ทำงานอยู่

- `sudo systemctl is-active <service_name>`  
  ตรวจสอบว่า service ทำงานอยู่หรือไม่

---

## ▶️🛑 คำสั่งควบคุม Service

- `sudo systemctl start <service_name>`  
  เริ่ม service

- `sudo systemctl stop <service_name>`  
  หยุด service

- `sudo systemctl restart <service_name>`  
  เริ่มใหม่ (เหมาะสำหรับ reload config)

- `sudo systemctl reload <service_name>`  
  ส่งสัญญาณให้ service reload config โดยไม่ restart

- `sudo systemctl disable <service_name>`  
  ยกเลิกการทำงานอัตโนมัติเมื่อบูต

---

## 🧯 การแก้ไขปัญหาเบื้องต้น

### ❌ Service ไม่ทำงาน

- ตรวจสอบ log:
  ```bash
  journalctl -xe
  ```

- ตรวจสอบสิทธิ์ไฟล์:
  ```bash
  ls -l /path/to/script.py
  ```

- ตรวจสอบ syntax ของ unit file:
  ```bash
  sudo systemd-analyze verify /etc/systemd/system/<service_name>.service
  ```

### ♻️ Service ไม่ reload หลังแก้ config

- สั่ง reload daemon:
  ```bash
  sudo systemctl daemon-reload
  ```

### 🕒 Service ทำงานช้า / Timeout

- เพิ่ม timeout ใน section `[Service]`:
  ```ini
  TimeoutStartSec=30
  TimeoutStopSec=15
  ```

---

## 📌 เคล็ดลับเพิ่มเติม

- ใช้ `Restart=on-failure` เพื่อให้ systemd พยายาม restart เมื่อ error
- ใช้ `Environment=` เพื่อกำหนดตัวแปรให้ process  
  เช่น `Environment="MODE=production"`
- ใช้ `ExecStop=` หากต้องการควบคุมวิธีหยุด service

```
You can list and filter systemd services on a Raspberry Pi (running Raspberry Pi OS), Debian, or Ubuntu using the systemctl command. Here are the commands to list all services and to display only the enabled and active ones.
List All Services
To list all loaded services on your system, regardless of their state, use the list-units subcommand with the --type=service option.
systemctl list-units --type=service

The output will show columns for the unit's name, whether its configuration is loaded, its high-level activation state (ACTIVE), and its low-level activation state (SUB).
Display Enabled Services
Enabled services are those configured to start automatically at boot. To list these, use list-unit-files with the --state=enabled option.
systemctl list-unit-files --type=service --state=enabled

The output will show the unit file's name and its state, which should be enabled for all listed services.
Display Active/Running Services
Active services are currently running. To display them, use the list-units subcommand with the --state=active option.
systemctl list-units --type=service --state=active

This command shows units in an active state. To be more specific and only list services that are actively running, you can use the --state=running option.
systemctl list-units --type=service --state=running

The output for these commands will show the UNIT name, LOAD status, ACTIVE status, SUB status (e.g., running or exited), and a brief description.

---
