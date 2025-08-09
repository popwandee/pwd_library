เอกสาร Markdown สำหรับคำสั่ง `UFW (Uncomplicated Firewall)` บน Linux ที่ใช้ในการพัฒนาระบบ มีทั้งขั้นตอนการตั้งค่า ตรวจสอบ สั่งทำงาน/หยุด และการแก้ไขปัญหาเบื้องต้น เหมาะสำหรับใช้เป็น Cheat Sheet ในงาน DevOps หรือระบบ Embedded ได้เลย:

---

```markdown
# 🔐 UFW Firewall Command Cheat Sheet

## ⚙️ การตั้งค่าเริ่มต้น

- เปิดใช้งาน UFW:
  ```bash
  sudo ufw enable
  ```

- ปิดใช้งาน UFW:
  ```bash
  sudo ufw disable
  ```

- รีเซ็ตค่าทั้งหมด:
  ```bash
  sudo ufw reset
  ```

## 🚪 การจัดการ Rule

- อนุญาตพอร์ต:
  ```bash
  sudo ufw allow <port>
  # ตัวอย่าง: sudo ufw allow 22
  ```

- ปฏิเสธพอร์ต:
  ```bash
  sudo ufw deny <port>
  ```

- อนุญาต service โดยใช้ชื่อ:
  ```bash
  sudo ufw allow ssh
  ```

- อนุญาตเฉพาะ IP:
  ```bash
  sudo ufw allow from 192.168.1.100
  ```

- อนุญาตเฉพาะ IP ไปยังพอร์ต:
  ```bash
  sudo ufw allow from 192.168.1.100 to any port 22
  ```

- ลบ rule ที่ระบุ:
  ```bash
  sudo ufw delete allow <port>
  ```

## 🔍 การตรวจสอบสถานะ

- ตรวจสอบสถานะ:
  ```bash
  sudo ufw status
  ```

- แสดงสถานะโดยละเอียด:
  ```bash
  sudo ufw status verbose
  ```

## 🛑 การหยุด / ปิดการทำงาน

- ปิด UFW ทั้งระบบ:
  ```bash
  sudo ufw disable
  ```

- ปิด rule เฉพาะ:
  ```bash
  sudo ufw delete deny <port>
  ```

## 🧯 การแก้ไขปัญหาเบื้องต้น

### 🔄 เปลี่ยนค่า default policies

- ปรับให้ default เป็นปฏิเสธทุกอย่าง:
  ```bash
  sudo ufw default deny incoming
  ```

- อนุญาตให้ outgoing connections ได้:
  ```bash
  sudo ufw default allow outgoing
  ```

### 🚧 เปิด log เพื่อตรวจสอบปัญหา

- เปิด log:
  ```bash
  sudo ufw logging on
  ```

- ปิด log:
  ```bash
  sudo ufw logging off
  ```

- ตรวจสอบ log:
  ```bash
  sudo less /var/log/ufw.log
  ```

---

## 📌 เคล็ดลับเพิ่มเติม

- ใช้ `ufw app list` เพื่อตรวจสอบ services ที่รู้จัก
- ตั้ง rule เฉพาะ protocol เช่น:
  ```bash
  sudo ufw allow 443/tcp
  ```

- ใช้ `ufw reload` เพื่อโหลด config ใหม่

```

---
