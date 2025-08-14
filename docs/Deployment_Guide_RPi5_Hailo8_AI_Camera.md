## Deployment Guide: ติดตั้งระบบ AI Camera (ALPR) บน Raspberry Pi 5 + Camera Module 3 + Hailo 8/8L

เอกสารนี้เป็นแนวทางแบบ End-to-End สำหรับการติดตั้งฮาร์ดแวร์และซอฟต์แวร์บน Raspberry Pi 5 เพื่อใช้งานระบบ AI Camera (ALPR) เวอร์ชัน 1.3

---

### 1) ฮาร์ดแวร์ที่ต้องใช้ (Bill of Materials)
- Raspberry Pi 5 (รุ่น RAM 8GB แนะนำ)
- Raspberry Pi Camera Module 3 (หรือ High-Quality Camera)
- Hailo 8/8L (AI HAT+ 26 TOPs หรือ AI KIT – M.2 M-Key)
- ฮีตซิงก์/พัดลมระบายความร้อน (แนะนำ Active Cooler)
- microSD Card (>= 32GB, Class 10/UHS-I)
- สาย/อะแดปเตอร์ไฟ 5V/5A สำหรับ RPi5

> [diagram/screenshot: การประกอบฮาร์ดแวร์]

---

### 2) ขั้นตอนติดตั้งฮาร์ดแวร์
1. ปิดเครื่อง/ถอดไฟ Raspberry Pi 5
2. ติดตั้ง Camera Module 3 กับพอร์ตกล้องตามคู่มือ Raspberry Pi (ตรวจสายให้แน่น)
3. ติดตั้ง Hailo AI HAT+ ให้แน่นหนา (หรือเสียบโมดูล M.2 กับ HAT ที่รองรับ)
4. ติดตั้งฮีตซิงก์/พัดลม
5. เสียบ microSD Card ที่แฟลช OS แล้ว
6. จ่ายไฟและเปิดเครื่อง

> [screenshot: จุดเชื่อมต่อสายกล้อง/ตำแหน่ง HAT]

---

### 3) เตรียมระบบปฏิบัติการ
- แนะนำ Raspberry Pi OS (64-bit) เวอร์ชันล่าสุด
- ตั้งค่า `raspi-config` เบื้องต้น: ภูมิภาค, SSH, กล้อง, และ PCIe Gen3

ตั้งค่า PCIe Gen3 (หากใช้ M.2 HAT):
```bash
sudo raspi-config
# 6 Advanced Options → A8 PCIe Speed → Enable Gen3 → Reboot
```

---

### 4) ติดตั้งไดรเวอร์/ซอฟต์แวร์ Hailo
ติดตั้ง Hailo all-in-one packages:
```bash
sudo apt update
sudo apt install -y hailo-all
sudo reboot
```

ตรวจสอบอุปกรณ์ Hailo:
```bash
hailortcli fw-control identify
```

ตรวจสอบ GStreamer/TAPPAS Core:
```bash
gst-inspect-1.0 hailotools
gst-inspect-1.0 hailo
```

ทดสอบ rpicam-apps:
```bash
sudo apt install -y rpicam-apps
rpicam-hello -t 10s
```

> [screenshot: เอาต์พุต hailortcli identify]

---

### 5) เตรียมโปรเจกต์ซอฟต์แวร์ AI Camera
โครงสร้างโปรเจกต์ (ตำแหน่งเริ่มต้น): `/home/camuser/aicamera`

ติดตั้ง dependencies และ environment:
```bash
cd /home/camuser/aicamera
source setup_env.sh
pip install -r v1_3/requirements.txt
```

ตั้งค่าไฟล์แวดล้อมสำหรับโปรดักชัน:
```bash
cat > v1_3/.env.production << 'EOF'
SECRET_KEY=change_me
# ปล่อยว่างเพื่อ offline mode หรือกำหนด URL เซิร์ฟเวอร์ WS
WEBSOCKET_SERVER_URL=
AICAMERA_ID=1
CHECKPOINT_ID=1
EOF
```

ตำแหน่งโมเดล Hailo และทรัพยากร:
- โฟลเดอร์ `resources/` เก็บ .hef (Hailo Executable Files)
- ตั้งค่าชื่อโมเดลใน `v1_3/src/core/config.py`

---

### 6) การรันระบบสำหรับทดสอบ (Development)
```bash
python3 v1_3/src/app.py
# เปิดเบราว์เซอร์ไปที่ http://<host>/ เพื่อตรวจภาพ/ควบคุม/ตรวจจับ/สุขภาพระบบ
```

---

### 7) การติดตั้งเป็นบริการ (Production)
ส่วนนี้อ้างอิง Nginx + Gunicorn + Systemd

ตัวอย่าง service (ไฟล์มีในโปรเจกต์): `/home/camuser/aicamera/aicamera_v1.3_fixed.service`

ติดตั้ง/เริ่มต้นบริการ:
```bash
sudo systemctl daemon-reload
sudo systemctl enable aicamera_v1.3
sudo systemctl start aicamera_v1.3
sudo journalctl -u aicamera_v1.3 -f
```

ตรวจสอบเว็บผ่าน Nginx (ตัวอย่าง):
```bash
sudo nginx -t && sudo systemctl reload nginx
```

> [screenshot: systemctl status aicamera_v1.3]

---

### 8) การอัปเดต/บำรุงรักษา
- อัปเดตไลบรารี: `source setup_env.sh && pip install -r v1_3/requirements.txt --upgrade`
- รีสตาร์ตบริการ: `sudo systemctl restart aicamera_v1.3`
- ตรวจสุขภาพ: เข้า `/health/system` หรือดู log ใน `logs/` และ `journalctl`
- ล้างข้อมูลเก่า: ใช้เมทอด `cleanup_old_records()` ใน `DatabaseManager`

การสำรองข้อมูล:
- สำรองไฟล์ `db/lpr_data.db` และโฟลเดอร์ `captured_images/`

---

### 9) การแก้ปัญหาเบื้องต้น (Troubleshooting)
- กล้องไม่สตาร์ต: ตรวจสิทธิ์/รีเซ็ตโมดูลกล้อง (ภายใน `CameraHandler` มีฟังก์ชันช่วย kill process ที่ใช้ `/dev/video*`)
- โมเดลไม่โหลด: ตรวจ `degirum` และไฟล์ `.hef` ใน `resources/` และชื่อโมเดลใน `config.py`
- พอร์ต/ซ็อกเก็ต: ตรวจ `/tmp/aicamera.sock`, Nginx config, Gunicorn config
- นำทางไม่เจอไฟล์เทมเพลต: ตรวจพาธ `template_folder`/`static_folder` ใน `app.py`

---

### 10) ภาคผนวก (Appendix)
- โครงสร้างโปรเจกต์: ดู `v1_3/ARCHITECTURE.md`
- มาตรฐานตัวแปร/หน้าจอ: `v1_3/VARIABLE_MANAGEMENT.md`
- เอกสารการติดตั้ง Hailo เพิ่มเติม: เอกสารอย่างเป็นทางการของ HailoRT/TAPPAS
- ตัวอย่างคำสั่งทดสอบ rpicam-apps: ดู `README.md` (root)

พื้นที่สำหรับแนบภาพหน้าจอการติดตั้ง/ผลการทดสอบ:
- [screenshot: hailortcli identify]
- [screenshot: rpicam-hello]
- [screenshot: หน้า Dashboard หลังติดตั้ง]


