Markdown ที่รวบรวมคำสั่ง Linux ด้าน Network ที่ใช้ในการพัฒนาระบบ ครอบคลุมทั้งการตั้งค่า ตรวจสอบ หยุดการทำงาน และแก้ไขปัญหาเบื้องต้น เหมาะสำหรับใช้ในการดูแลระบบเครือข่ายหรือ Embedded Networking:

---

```markdown
# 🌐 Linux Networking Command Cheat Sheet

## 🛠️ การตั้งค่าเริ่มต้น (Network Configuration)

- ตรวจสอบ IP และ interface:
  ```bash
  ip a
  ip link show
  ```

- ตั้งค่า IP แบบ static:
  ```bash
  sudo ip addr add 192.168.1.100/24 dev eth0
  sudo ip route add default via 192.168.1.1
  ```

- เปิด/ปิด interface:
  ```bash
  sudo ip link set eth0 up
  sudo ip link set eth0 down
  ```

- ตรวจสอบ DNS:
  ```bash
  cat /etc/resolv.conf
  ```

## 🔍 การตรวจสอบการทำงาน (Network Diagnostics)

- ตรวจสอบการเชื่อมต่อ:
  ```bash
  ping <ip-or-host>
  ```

- ตรวจสอบ routing table:
  ```bash
  ip route
  ```

- ตรวจสอบ port ที่เปิด:
  ```bash
  sudo netstat -tuln
  sudo ss -tuln
  ```

- ตรวจสอบการใช้งานเครือข่าย:
  ```bash
  iftop         # ต้องติดตั้งเพิ่ม
  nload         # เครื่องมือดู traffic แบบกราฟ
  ```

## ▶️🛑 การควบคุม Network Service

- เริ่ม/หยุด Network Manager:
  ```bash
  sudo systemctl start NetworkManager
  sudo systemctl stop NetworkManager
  ```

- ตรวจสอบสถานะ:
  ```bash
  sudo systemctl status NetworkManager
  ```

- รีสตาร์ทการตั้งค่า network:
  ```bash
  sudo systemctl restart networking
  ```

## 🧯 การแก้ไขปัญหาเบื้องต้น

### ❌ เชื่อมต่อ Network ไม่ได้

- ตรวจสอบ interface ถูกเปิดหรือไม่:
  ```bash
  ip link show
  ```

- ตรวจสอบ IP config:
  ```bash
  ip a
  ```

- ตรวจสอบ gateway:
  ```bash
  ip route show
  ```

- ตรวจสอบ DNS:
  ```bash
  ping 8.8.8.8
  ping google.com
  ```

### 🔌 DHCP ไม่ทำงาน

- สั่งขอ IP ใหม่:
  ```bash
  sudo dhclient -v eth0
  ```

- ตรวจสอบ log:
  ```bash
  journalctl -u NetworkManager
  ```

### 🔒 Firewall บล็อกการเชื่อมต่อ

- ปิดชั่วคราวเพื่อตรวจสอบ:
  ```bash
  sudo ufw disable
  ```

- ตรวจสอบ rule ที่อาจบล็อก port:
  ```bash
  sudo ufw status
  ```

---

## 📌 เคล็ดลับเพิ่มเติม

- ใช้ `nmcli` สำหรับจัดการ Network Manager ด้วย CLI  
- ใช้ `tcpdump` หรือ `wireshark` เพื่อวิเคราะห์ packet  
- ตั้ง static IP ผ่าน `netplan` หรือ `interfaces` แล้วแต่ distro

```

---

วางแผนเพิ่มส่วน VPN, Wi-Fi, Network bridge ,การตั้งค่า IP จาก Python script 