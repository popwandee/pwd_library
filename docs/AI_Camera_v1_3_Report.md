## เอกสารสรุปรายงานการพัฒนา: AI Camera v1.3 (Raspberry Pi 5 + Camera Module 3 + Hailo 8)

### ข้อมูลโครงการ
- ชื่อระบบ: AI Camera v1.3 – Edge AI License Plate Recognition (LPR)
- แพลตฟอร์ม: Raspberry Pi 5 + Camera Module 3 + Hailo 8/8L
- สแต็กหลัก: Flask, Gunicorn, Nginx, SQLite, Picamera2, DeGirum/HailoRT, Flask-SocketIO
- ตำแหน่งโปรเจกต์: `/home/camuser/aicamera` (ไดเรกทอรีเวอร์ชันหลัก `v1_3`)

---

### 1) แนวคิดในการออกแบบสถาปัตยกรรม
- **Dependency Injection (DI)**: จัดการ dependency ของ services และ components ผ่าน `v1_3/src/core/dependency_container.py` ลดการเชื่อมโยงแน่น (coupling) และทำให้ทดสอบง่าย
- **Service Layer**: แยก business logic ออกจากส่วนควบคุมฮาร์ดแวร์/IO เพื่อความเป็นระเบียบและบำรุงรักษาง่าย
- **Flask Blueprints**: แยก Web UI/REST/WebSocket ตามโดเมนงาน (`main`, `camera`, `detection`, `streaming`, `health`, `websocket`)
- **Absolute Imports**: ใช้ `v1_3.src.*` เพื่อความชัดเจน ลด circular import และรองรับการ refactor (`core/utils/import_helper.py`)
- **Auto-Startup Sequence**: ลำดับเริ่มทำงานอัตโนมัติ `camera → detection → health → websocket_sender` (กำหนดใน `core/config.py` และ orchestration ใน `app.py`)
- **Health Monitoring**: ตรวจสุขภาพกล้อง, ทรัพยากรระบบ, เครือข่าย, สถานะโมเดล, ฐานข้อมูล พร้อมบันทึกผลใน DB
- **Offline-first WebSocket**: หากไม่กำหนด `WEBSOCKET_SERVER_URL` ระบบ sender ทำงานแบบ offline และส่งย้อนหลังเมื่อเชื่อมต่อได้
- **Thread-safe Camera Singleton**: ป้องกันการชนทรัพยากรกล้อง ด้วย single instance + locking ที่ `CameraHandler`

---

### 2) โครงสร้างระบบ (สรุปภาพรวม)
- Runtime: Nginx → Gunicorn → Flask (`v1_3/src/wsgi.py` → `v1_3/src/app.py`)
- DI container ประกอบบริการหลัก: `camera_manager`, `detection_manager`, `health_service`, `websocket_sender`, `database_manager`
- ฐานข้อมูล: SQLite (`/home/camuser/aicamera/db/lpr_data.db`)
- กล้อง: Picamera2 (จ่ายเฟรมให้ pipeline ตรวจจับ)
- AI: โมเดลตรวจจับยานพาหนะ/ป้ายทะเบียน/ OCR ผ่าน DeGirum/Hailo (`DetectionProcessor`)
- ส่งผลตรวจจับ: WebSocket (ออนไลน์/ออฟไลน์)

โฟลเดอร์สำคัญ:
- `v1_3/src/core`: `config.py`, `dependency_container.py`, `utils/*`
- `v1_3/src/components`: `camera_handler.py`, `detection_processor.py`, `database_manager.py`, `health_monitor.py`
- `v1_3/src/services`: `camera_manager.py`, `detection_manager.py`, `video_streaming.py`, `websocket_sender.py`
- `v1_3/src/web/blueprints`: `main.py`, `camera.py`, `detection.py`, `streaming.py`, `health.py`, `websocket.py`
- ทรัพยากร: โมเดล `resources/`, รูปที่จับ `captured_images/`, ล็อก `logs/`

---

### 3) องค์ประกอบสำคัญในระบบ
- `CameraHandler` (Singleton): ควบคุม Picamera2, ตั้งค่า/อ่านค่ากล้อง, จับภาพ, สถานะ, บันทึกวิดีโอ
- `CameraManager`: จัดการอายุการใช้งาน/สตรีมมิ่ง, สถานะ, อัปเดตคอนฟิก, auto-start
- `DetectionProcessor`: โหลดโมเดล, ตรวจสอบเฟรม, ตรวจจับยานพาหนะ/ป้ายทะเบียน, OCR, วาดกรอบ/ครอป, เซฟรูป
- `DetectionManager`: ลูปตรวจจับเต็มกระบวนการ, สถิติ, จัดช่วงเวลา (`DETECTION_INTERVAL`)
- `DatabaseManager`: สคีมา/คอนเนกชัน/บันทึกผลตรวจจับและล็อกกิจกรรม sender/health
- `HealthMonitor` + `HealthService`: ตรวจสุขภาพรวม (กล้อง/ทรัพยากร/โมเดล/DB/เครือข่าย) + บันทึกลง DB + APIs
- `WebSocketSender`: ส่งข้อมูล `detection_results`, `health_checks`; มี auto-retry และ offline mode
- `Blueprints`: REST/หน้าเว็บ/SocketIO events สำหรับ UI และควบคุมระบบ

---

### 4) การพัฒนาระบบ (แนวทาง/มาตรฐาน)
- Environment
  - ใช้ `setup_env.sh` เพื่อตรวจ/เปิดใช้งานสภาพแวดล้อม Hailo/TAPPAS และ virtualenv
  - ติดตั้ง Python deps: `requirements.txt` (root) และ `v1_3/requirements.txt`
- Absolute Imports
  - เรียก `setup_import_paths()` ก่อน import, ตรวจด้วย `validate_imports()` ตอนเริ่มระบบ
- มาตรฐานตัวแปร/โครงสร้าง Response
  - อ้างอิง `v1_3/VARIABLE_MANAGEMENT.md` (success/error/status/health/WS)
- Logging: โฟลเดอร์ `logs/` ถูกสร้างอัตโนมัติจาก `config.py`
- ทดสอบ/ดีบัก: ใช้ endpoints `/camera/*`, `/detection/*`, `/health/*`, `/websocket/*` และดู `journalctl`/ไฟล์ log
- ขยายฟีเจอร์
  - เพิ่มไฟล์ใน `components/` หรือ `services/` → ลงทะเบียน DI → เพิ่ม blueprint/route (ถ้าจำเป็น) → อัปเดตเอกสาร

---

### 5) คำแนะนำและคู่มือในการใช้งาน
ข้อกำหนดระบบ:
- Raspberry Pi 5 (ARM64), Camera Module 3, Hailo 8/8L
- Python 3.11+, Picamera2, Nginx, Gunicorn

เริ่มต้นใช้งานแบบพัฒนา:
```bash
cd /home/camuser/aicamera
source setup_env.sh
pip install -r v1_3/requirements.txt
python3 v1_3/src/app.py
```

ติดตั้งเป็นบริการระบบ (systemd + gunicorn + nginx):
```bash
sudo systemctl daemon-reload
sudo systemctl enable aicamera_v1.3
sudo systemctl start aicamera_v1.3
sudo journalctl -u aicamera_v1.3 -f
```

การเข้าถึงระบบ (ผ่าน Nginx):
- หน้า Dashboard: `http://<host>/`
- สตรีมวิดีโอ: `/camera/video_feed`, `/camera/video_feed_lores`
- สถานะระบบ: `/health/system`, `/camera/status`, `/detection/status`, `/websocket/status`

API พื้นฐาน:
- กล้อง: `POST /camera/start`, `POST /camera/stop`, `GET/POST /camera/config`
- ตรวจจับ: `POST /detection/start`, `POST /detection/stop`, `GET /detection/statistics`, `POST /detection/process_frame`
- ผลล่าสุด: `GET /detection/results/recent`
- เฮลธ์: `GET /health/system`, `GET /health/logs`, `POST /health/monitor/start`, `POST /health/monitor/stop`
- WebSocket สถานะรวม: `GET /websocket/status`

โหมดออฟไลน์:
- ปล่อยว่าง `WEBSOCKET_SERVER_URL` (ใน `v1_3/.env.production`) → sender ทำงานแบบ offline และส่งย้อนหลังเมื่อออนไลน์

---

### 6) คำแนะนำและคู่มือในการพัฒนาต่อยอด
- เพิ่มคอมโพเนนต์/บริการใหม่: สร้างคลาส → ลงทะเบียนใน DI → เพิ่ม blueprint/route → อัปเดต import validation/เอกสาร
- ขยายฐานข้อมูล: เพิ่มตาราง/อินเด็กซ์ใน `DatabaseManager._create_tables()` + เมทอด query/report
- เพิ่ม Health Check: เสริมเมทอดใน `HealthMonitor` และแสดงผ่าน `/health/*`/SocketIO
- ปรับประสิทธิภาพ: ปรับ `DETECTION_INTERVAL`, thresholds และค่ากล้อง (`DEFAULT_RESOLUTION`, `DEFAULT_FRAMERATE`)
- UI/Frontend: ปรับ `web/templates` และ `web/static/js/*` ตามมาตรฐานตัวแปร

---

### 7) การบำรุงรักษา
- เฝ้าระวัง: `/health/system`, events ผ่าน SocketIO, โลกระบบใน `logs/` และ `journalctl`
- ทำความสะอาดข้อมูล: ใช้ `DatabaseManager.cleanup_old_records(days_to_keep=30)` ลดขนาด DB
- แบ็กอัป: สำรอง `db/lpr_data.db` และ `captured_images/`
- อัปเดตแพ็กเกจ: `source setup_env.sh && pip install -r v1_3/requirements.txt --upgrade` แล้ว restart service
- ความปลอดภัย: เก็บ `SECRET_KEY`, URL ภายนอกใน `.env.production`; ใช้ Unix socket ระหว่าง Nginx↔Gunicorn

---

### 8) แนวทางแก้ปัญหาเบื้องต้น (Troubleshooting)
- กล้องไม่สตาร์ต: ตรวจสิทธิ์อุปกรณ์, ปลดกระบวนการที่จับ `/dev/video*`/`/dev/media*` (มีใน `CameraHandler`)
- ImportError `v1_3.*`: ตรวจ `setup_import_paths()`/`validate_imports()` และโครงสร้างไดเรกทอรี
- โมเดลโหลดไม่ได้: ตรวจ `degirum` และไฟล์ใน `resources/`, ค่าคอนฟิกใน `core/config.py`
- เซอร์วิสล้มเหลว: ตรวจ `journalctl -u aicamera_v1.3 -f`, ไฟล์ log, สถานะ socket, สิทธิ์ไฟล์

---

### 9) ค่าคอนฟิกหลัก (อ้างอิง `v1_3/src/core/config.py`)
- เส้นทาง: `BASE_DIR=/home/camuser/aicamera`, `DATABASE_PATH=db/lpr_data.db`, `IMAGE_SAVE_DIR=captured_images/`
- ออโต้สตาร์ต: `AUTO_START_CAMERA`, `AUTO_START_STREAMING`, `AUTO_START_DETECTION`, `AUTO_START_HEALTH_MONITOR`, `AUTO_START_WEBSOCKET_SENDER`
- โมเดล/ออปชัน: `VEHICLE_DETECTION_MODEL`, `LICENSE_PLATE_DETECTION_MODEL`, `LICENSE_PLATE_OCR_MODEL`, `EASYOCR_LANGUAGES`
- จังหวะการทำงาน: `DETECTION_INTERVAL`, `CONFIDENCE_THRESHOLD`, `PLATE_CONFIDENCE_THRESHOLD`
- WebSocket: `WEBSOCKET_SERVER_URL`, `SENDER_INTERVAL`, `HEALTH_SENDER_INTERVAL`

---

### 10) อ้างอิงไฟล์/เอกสารที่เกี่ยวข้อง
- สถาปัตยกรรม: `v1_3/ARCHITECTURE.md`
- มาตรฐานตัวแปร/UI: `v1_3/VARIABLE_MANAGEMENT.md`
- หน้าผลตรวจจับ: `v1_3/DETECTION_RESULTS_IMPLEMENTATION.md`
- คู่มือฮาร์ดแวร์/ติดตั้ง: `README.md` (root) และตัวอย่าง rpicam-apps
- เดโม/คลาวด์: `v1_3_demo/`

---

อัปเดตล่าสุด: สร้างโดยอัตโนมัติจากซอร์สโค้ดในไดเรกทอรี `v1_3` บนเครื่องเมื่อวันที่สร้างไฟล์นี้


