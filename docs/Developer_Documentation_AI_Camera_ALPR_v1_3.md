## Developer Documentation – AI Camera (ALPR) v1.3

เอกสารนี้ช่วยนักพัฒนาใหม่ทำความเข้าใจระบบอย่างรวดเร็ว ครอบคลุมภาพรวมสถาปัตยกรรม โครงสร้างโค้ด เวิร์กโฟลว์การทำงาน จุดขยายระบบ การดีบัก/ทดสอบ และแนวปฏิบัติที่ดี

---

### 1) สถาปัตยกรรมโดยสรุป
- รูปแบบ: DI + Service Layer + Flask Blueprints + Absolute Imports
- Auto-Startup: `camera → detection → health → websocket_sender`
- Health Monitoring ครอบคลุม Camera/Disk/CPU-RAM/Models/EasyOCR/DB/Network
- Offline-first WebSocket Sender

อ่านรายละเอียดเชิงลึก: `v1_3/ARCHITECTURE.md`

---

### 2) โครงสร้างโปรเจกต์หลัก
```
/home/camuser/aicamera
├─ v1_3/
│  ├─ src/
│  │  ├─ app.py                 # Flask app (dev runtime & orchestration)
│  │  ├─ wsgi.py                # WSGI entry (gunicorn)
│  │  ├─ core/
│  │  │  ├─ config.py           # ค่าคอนฟิกหลัก + auto-start flags
│  │  │  ├─ dependency_container.py # DI container + service registry
│  │  │  └─ utils/
│  │  │     ├─ import_helper.py # Absolute import paths + validation
│  │  │     └─ logging_config.py
│  │  ├─ components/
│  │  │  ├─ camera_handler.py   # Picamera2 (Singleton, thread-safe)
│  │  │  ├─ detection_processor.py # โหลดโมเดล/ตรวจจับ/ครอป/วาดกรอบ
│  │  │  ├─ database_manager.py # SQLite schema/CRUD/logs
│  │  │  └─ health_monitor.py   # Checks & logs
│  │  ├─ services/
│  │  │  ├─ camera_manager.py   # ควบคุมกล้องระดับสูง + auto-start
│  │  │  ├─ detection_manager.py# วงจรตรวจจับ + สถิติ + interval
│  │  │  ├─ video_streaming.py  # (ถูกรวมใช้ใน blueprints)
│  │  │  └─ websocket_sender.py # ส่งผล/สุขภาพ (online/offline)
│  │  └─ web/blueprints/        # UI/REST/SocketIO
│  │     ├─ main.py camera.py detection.py streaming.py health.py websocket.py
│  ├─ ARCHITECTURE.md VARIABLE_MANAGEMENT.md DETECTION_RESULTS_IMPLEMENTATION.md
│  └─ requirements.txt
├─ resources/                   # โมเดล Hailo (.hef)
├─ db/ logs/ captured_images/
└─ aicamera_v1.3_fixed.service  # systemd service
```

---

### 3) เวิร์กโฟลว์หลักของระบบ
1. Startup: `wsgi.py → app.create_app()`
2. Import paths + validate imports → โหลดคอนฟิก → สร้าง DI container → สร้าง SocketIO → ลงทะเบียน Blueprints
3. Initialize services ตามลำดับ (camera → detection → health → websocket)
4. ผู้ใช้โต้ตอบผ่าน UI/REST/SocketIO → เรียกใช้ service → ใช้ component → เข้าถึงฮาร์ดแวร์/โมเดล/ฐานข้อมูล

แผนภาพการไหล: ดู `ARCHITECTURE.md` (Dependency Flow, Startup Sequence)

---

### 4) จุดขยายระบบ (Extensibility)
เพิ่ม Component ใหม่:
1) สร้างไฟล์ใน `v1_3/src/components/your_component.py`
2) ลงทะเบียนใน DI: เพิ่มใน `DependencyContainer._register_default_services()`
3) (ถ้าต้องมี UI/REST) สร้าง Blueprint ใหม่ใน `v1_3/src/web/blueprints/`
4) ลงทะเบียน blueprint ใน `web/blueprints/__init__.py`

เพิ่ม Service ใหม่:
1) สร้างไฟล์ใน `v1_3/src/services/your_service.py`
2) ลงทะเบียนใน DI + ระบุ dependencies ที่ต้องการ (เช่น `database_manager`, `logger`)
3) ใช้ใน blueprint หรือ orchestration ตามเหมาะสม

ขยายฐานข้อมูล:
1) เพิ่มคอลัมน์/ตารางใน `DatabaseManager._create_tables()`
2) เพิ่มเมทอด query ใหม่ (รองรับ pagination/filter/sort)
3) อัปเดตเอกสารและหน้า UI (หากต้องแสดงผล)

---

### 5) แนวปฏิบัติการเขียนโค้ด (Coding Standards)
- ใช้ Absolute Imports (`from v1_3.src...`)
- แยก business logic ไว้ที่ Service, งาน IO/ฮาร์ดแวร์ไว้ใน Component
- สร้างเมทอดสถานะ/สุขภาพให้ทุกคอมโพเนนต์ที่สำคัญ (`get_status()`, `get_health_status()`)
- ใช้ logging อย่างสม่ำเสมอ และคืนค่าที่ serializable สำหรับ API
- ป้องกันข้อผิดพลาดด้าน frame/attribute ตามแนวทางใน `ARCHITECTURE.md`/`VARIABLE_MANAGEMENT.md`

---

### 6) การทดสอบ (Testing)
หัวข้อที่ควรมี Unit/Integration Tests:
- Camera Handler: singleton/thread-safe, start/stop, capture frame, metadata
- Detection Processor: validate frame, load models, detect vehicle/plate, OCR
- Detection Manager: วงจรตรวจจับ, สถิติ, interval, readiness camera
- Database Manager: schema, CRUD, pagination, marking sent, logs
- Health Monitor/Service: checks ค่าต่างๆ และโครงสร้างผลลัพธ์
- Blueprints: เสถียรภาพของ API/WS events และโครงสร้าง response

สคริปต์/ตัวอย่างทดสอบ: ดู `v1_3/README.md` และ tests ภายในโครงการ

---

### 7) การดีบักและ Troubleshooting
- Web ไม่ขึ้น: ตรวจ gunicorn/nginx config, permission, socket `/tmp/aicamera.sock`
- ImportError: เรียก `validate_imports()` และตรวจพาธ `setup_import_paths()`
- กล้องชนทรัพยากร: ใช้เมทอดใน `CameraHandler` ที่ช่วยปล่อย `/dev/video*`/`/dev/media*`
- โมเดลโหลดล้มเหลว: ตรวจ `degirum`, พาธ `resources/`, คีย์ใน `config.py`
- ผลตรวจจับว่าง: ตรวจ `DETECTION_INTERVAL`, readiness ของกล้อง, thresholds และแสง

---

### 8) ค่าคอนฟิกสำคัญ (Config Quick Reference)
- เส้นทาง: `BASE_DIR`, `DATABASE_PATH`, `IMAGE_SAVE_DIR`
- กล้อง: `DEFAULT_RESOLUTION`, `DEFAULT_FRAMERATE`, ฯลฯ
- ตรวจจับ: `DETECTION_INTERVAL`, `CONFIDENCE_THRESHOLD`, `PLATE_CONFIDENCE_THRESHOLD`
- Auto-start: `AUTO_START_CAMERA`, `AUTO_START_DETECTION`, `AUTO_START_HEALTH_MONITOR`, `AUTO_START_WEBSOCKET_SENDER`
- WebSocket: `WEBSOCKET_SERVER_URL`, `SENDER_INTERVAL`, `HEALTH_SENDER_INTERVAL`

---

### 9) แนวทางรีวิวโค้ด (Code Review Checklist)
- แยกความรับผิดชอบชัดเจน (Service vs Component)
- ปลอดภัยต่อเธรด/ฮาร์ดแวร์กล้อง (เรียกผ่าน manager/handler เท่านั้น)
- จัดการข้อผิดพลาดและบันทึก log ครอบคลุมเส้นทางสำคัญ
- คืนค่า JSON-serializable เสมอใน API/WS
- อัปเดตเอกสาร (README/ARCHITECTURE/VARIABLE_MANAGEMENT) เมื่อมีการเปลี่ยนแปลง

---

### 10) Roadmap/งานที่แนะนำในอนาคต
- ปรับปรุง OCR (โมเดลเฉพาะภาษาไทย/เขต)
- เพิ่มระบบสิทธิ์ผู้ใช้และการตรวจสอบการเข้าถึง
- เพิ่มหน้า Analytics (กราฟแนวโน้ม ตรวจจับตามช่วงเวลา ฯลฯ)
- เพิ่ม Integration กับระบบภายนอก (REST/WebSocket/MQTT)

---

### 11) ภาคผนวก
- เอกสารอ้างอิงภายใน: `ARCHITECTURE.md`, `VARIABLE_MANAGEMENT.md`, `DETECTION_RESULTS_IMPLEMENTATION.md`
- สคริปต์สภาพแวดล้อม: `setup_env.sh`, `install.sh`
- ตัวอย่าง Systemd: `aicamera_v1.3_fixed.service`


