**Markdown** ที่รวบรวมคำสั่งสำหรับใช้กับ **Picamera2** และ **rpicam-apps** ซึ่งเป็นเครื่องมือยอดนิยมในการควบคุมกล้องของ Raspberry Pi รุ่นใหม่ ๆ โดยครอบคลุมทั้งการติดตั้ง การใช้งาน และการแก้ปัญหาเบื้องต้น เหมาะสำหรับนักพัฒนาระบบภาพจากกล้องบนบอร์ด Raspberry Pi 📸🐍

---

```markdown
# 📷 คู่มือ Picamera2 และ rpicam-apps สำหรับการพัฒนาระบบด้วยกล้อง Raspberry Pi

## 🛠️ การติดตั้งพื้นฐาน

### 📦 ติดตั้ง Picamera2
```bash
sudo apt update
sudo apt install -y python3-picamera2 python3-libcamera libcamera-apps
```

### 📦 ติดตั้ง rpicam-apps
```bash
sudo apt install -y rpicam-apps
```

---

## ⚙️ ตั้งค่าเบื้องต้น

### ตรวจสอบกล้องว่าเชื่อมต่อถูกต้อง
```bash
libcamera-hello
```

### ตรวจสอบอุปกรณ์ที่เชื่อมต่อ
```bash
libcamera-hello --list-cameras
```

### ใช้ Picamera2 ใน Python
```python
from picamera2 import Picamera2
picam2 = Picamera2()
picam2.start()
image = picam2.capture_array()
```

---

## 📸 ใช้งาน rpicam-apps

### แสดงภาพจากกล้อง
```bash
libcamera-hello
```

### ถ่ายภาพนิ่ง
```bash
libcamera-jpeg -o image.jpg
```

### บันทึกวิดีโอ
```bash
libcamera-vid -t 10000 -o video.h264
```

### ถ่ายภาพแบบ RAW และ YUV
```bash
libcamera-raw -o image.raw
libcamera-yuv -o image.yuv
```

---

## 🧪 ตรวจสอบและทดสอบการทำงาน

### ทดสอบด้วย Picamera2 บน Python
```python
from picamera2 import Picamera2, Preview
picam2 = Picamera2()
picam2.start_preview(Preview.QT)
picam2.start()
```

### ตรวจสอบเวอร์ชันและ dependencies
```bash
apt list --installed | grep libcamera
pip list | grep picamera2
```

---

## 🩺 แก้ไขปัญหาเบื้องต้น

### ปัญหากล้องไม่แสดงภาพ
- ตรวจสอบการเชื่อมต่อของกล้อง
- ตรวจสอบว่ากล้องเปิดใช้งานใน `/boot/config.txt`:
  ```bash
  sudo nano /boot/config.txt
  ```
  เพิ่มบรรทัด:
  ```
  start_x=1
  gpu_mem=128
  ```

### ปัญหา libcamera error
- อัพเดตแพ็กเกจ:
  ```bash
  sudo apt update && sudo apt upgrade
  ```
- ตรวจสอบว่ามีการใช้ Raspberry Pi OS เวอร์ชันล่าสุด

---

## 📚 แหล่งอ้างอิงและการเรียนรู้เพิ่มเติม
- [libcamera Documentation](https://www.linaro.org/)
- [Picamera2 GitHub](https://github.com/raspberrypi/picamera2)
- [rpicam-apps GitHub](https://github.com/raspberrypi/rpicam-apps)

```

---
