# PWD Vision Works - Library

**Utilities library for Computer Vision and AI projects**

เป็น library รวบรวมเครื่องมือและฟังก์ชั่นสำหรับการพัฒนาระบบ Computer Vision และ AI ที่ใช้งานง่าย มีประสิทธิภาพสูง และเหมาะสำหรับการใช้งานในสภาพแวดล้อมการผลิต (Production)

## 🌟 Features

- 📷 **Camera Management**: รองรับ Raspberry Pi Camera และ USB Camera
- 🚀 **Hailo8 AI Integration**: ประมวลผล AI ด้วย Hailo8 accelerator
- 🖼️ **Image Processing**: เครื่องมือประมวลผลภาพที่ครบครัน
- 📊 **Graph Utilities**: เครื่องมือสำหรับการวิเคราะห์และแสดงผลกราฟ
- 🛠️ **Drawing Utilities**: เครื่องมือสำหรับการวาดและแสดงผลบนภาพ
- 📚 **Knowledge Base**: รวบรวมความรู้และ best practices

## 🏗️ Project Structure

```
pwd_library/
├── 📁 camera/                    # Camera management
│   ├── __init__.py              
│   └── picamera2_cm3.py         # Raspberry Pi Camera Manager
├── 📁 dev-knowledge-base/       # Documentation & guides
│   ├── 📁 ai_vision/            # AI/Vision best practices
│   ├── 📁 camera/               # Camera management guides
│   ├── 📁 deployment/           # Deployment guides
│   ├── 📁 python/               # Python best practices
│   └── 📁 [other topics]/
├── 📁 graph/                    # Graph utilities
│   └── graph_utils.py
├── 📁 hailo/                    # Hailo AI processor
│   ├── coco.txt                 # COCO class names
│   └── detect.py                # Detection utilities
├── 📁 image_processing/         # Image processing tools
│   ├── __init__.py
│   ├── preprocessor.py          # Image preprocessing
│   └── postprocessor.py         # Results post-processing
├── 📁 model/                    # AI model management
│   ├── __init__.py
│   └── hailo8_processor.py      # Hailo8 processor
├── 📁 utils/                    # Common utilities
│   ├── __init__.py
│   ├── drawing_utils.py         # Drawing and visualization
│   └── exceptions.py            # Custom exceptions
├── 📄 README.md
└── 📄 LICENSE
```

## 🚀 Installation

### การติดตั้งแบบ Submodule (แนะนำ)

เพิ่ม PWD Library เป็น Git Submodule ในโปรเจกต์ของคุณ:

```bash
# เพิ่ม submodule
git submodule add https://github.com/popwandee/pwd_library.git

จากเอกสารที่แนบมาและข้อมูลเพิ่มเติมที่ค้นหามา ผมได้รวบรวมคำสั่งและแนวทางปฏิบัติที่จำเป็นในการพัฒนาโปรแกรม โดยจัดทำในรูปแบบไฟล์ `.md` เพื่อให้ง่ายต่อการใช้งาน ดังนี้ครับ

# คู่มือการพัฒนาและจัดการระบบ

## 1\. คำสั่ง Git ที่จำเป็น

คู่มือนี้รวบรวมคำสั่ง Git ขั้นพื้นฐานสำหรับการจัดการ Repository ของคุณ

### การตั้งค่า Git Repository

  * **ตั้งค่าโปรเจกต์ใหม่:** ใช้คำสั่งนี้ในโฟลเดอร์โปรเจกต์ของคุณเพื่อสร้าง Git Repository ใหม่
    ```bash
    git init
    ```
  * **เพิ่มไฟล์เข้าสู่ Staging Area:** เตรียมไฟล์ที่แก้ไขเพื่อทำการ commit
    ```bash
    git add .
    ```
  * **บันทึกการเปลี่ยนแปลง:** สร้าง commit เพื่อบันทึกการเปลี่ยนแปลงใน History
    ```bash
    git commit -m "ข้อความอธิบายการเปลี่ยนแปลง"
    ```
  * **เชื่อมต่อกับ Remote Repository:** ตั้งค่า Remote Repository (เช่น GitHub)
    ```bash
    git remote add origin <URL ของ Remote Repository>
    ```
  * **Push โค้ดขึ้น Remote:** ส่งโค้ดที่ commit แล้วขึ้นไปยัง Remote Repository
    ```bash
    git push -u origin main
    ```

### การจัดการ Branch

  * **สร้างและสลับไป Branch ใหม่:** สร้าง Branch ใหม่และสลับไปใช้งานทันที
    ```bash
    git switch -c <ชื่อ branch>
    ```
    หรือ
    ```bash
    git checkout -b <ชื่อ branch>
    ```
  * **สลับไป Branch ที่มีอยู่แล้ว:**
    ```bash
    git checkout <ชื่อ branch>
    ```
  * **ดู Branch ทั้งหมด:**
    ```bash
    git branch
    ```
  * **รวมโค้ดจากอีก Branch หนึ่ง:** รวมโค้ดจาก Branch ปัจจุบันเข้ากับ Branch อื่น
    ```bash
    git merge <ชื่อ branch ที่จะนำมารวม>
    ```

### การแก้ไขปัญหา Conflict

เมื่อเกิด `Merge Conflict` Git จะหยุดการ Merge และแจ้งว่ามีไฟล์ที่เกิดความขัดแย้ง

  * **ตรวจสอบสถานะ:** ใช้คำสั่งนี้เพื่อดูว่ามีไฟล์ใดที่เกิด Conflict
    ```bash
    git status
    ```
  * **การแก้ไข Conflict:** เมื่อเปิดไฟล์ที่มีปัญหา จะเห็นโค้ดที่มีเครื่องหมาย `<<<<<<<`, `=======`, และ `>>>>>>>` คุณต้องเลือกว่าจะใช้โค้ดส่วนไหนหรือแก้ไขใหม่ทั้งหมด
  * **ยกเลิกการ Merge:** หากไม่ต้องการแก้ไข Conflict สามารถยกเลิกการ Merge ได้ด้วยคำสั่ง
    ```bash
    git merge --abort
    ```
  * **ยืนยันการแก้ไข:** หลังจากแก้ไขไฟล์ที่มี Conflict แล้ว ให้ `add` และ `commit` เพื่อยืนยันว่าแก้ไขเสร็จสิ้น
    ```bash
    git add .
    git commit -m "Resolve merge conflict"
    ```

## 2\. คำสั่งสำหรับ Systemd

### `systemctl`

`systemctl` เป็นคำสั่งหลักสำหรับจัดการบริการ (services) และหน่วย (units) ต่างๆ ในระบบ Linux ที่ใช้ `systemd`

| คำสั่ง | คำอธิบาย |
| :--- | :--- |
| `systemctl start <ชื่อ service>` | เริ่มการทำงานของ Service นั้น |
| `systemctl stop <ชื่อ service>` | หยุดการทำงานของ Service นั้น |
| `systemctl restart <ชื่อ service>` | Restart Service |
| `systemctl reload <ชื่อ service>` | Reload Service โดยไม่ต้องหยุดการทำงาน (ถ้า Service รองรับ) |
| `systemctl status <ชื่อ service>` | แสดงสถานะปัจจุบันของ Service นั้นอย่างละเอียด |
| `systemctl enable <ชื่อ service>` | กำหนดให้ Service เริ่มทำงานอัตโนมัติเมื่อ Boot เครื่อง |
| `systemctl disable <ชื่อ service>` | ยกเลิกการเริ่มทำงานอัตโนมัติของ Service นั้น |
| `systemctl is-active <ชื่อ service>` | ตรวจสอบว่า Service กำลังทำงานหรือไม่ |
| `systemctl is-enabled <ชื่อ service>` | ตรวจสอบว่า Service ถูกตั้งค่าให้เริ่มอัตโนมัติหรือไม่ |

### `journalctl`

`journalctl` ใช้สำหรับดู Log ของระบบที่จัดการโดย `systemd`

  * **ดู Log ทั้งหมด:** แสดง Log ทั้งหมดในระบบ
    ```bash
    journalctl
    ```
  * **ดู Log ของ Service เฉพาะ:** ดู Log ของ Service ที่ต้องการ
    ```bash
    journalctl -u <ชื่อ service>
    ```
  * **ดู Log แบบ Real-time:** แสดง Log ที่เข้ามาใหม่แบบต่อเนื่องเหมือนคำสั่ง `tail -f`
    ```bash
    journalctl -f
    ```
  * **ดู Log ตั้งแต่เวลาที่กำหนด:**
    ```bash
    journalctl --since "YYYY-MM-DD HH:MM:SS"
    ```
  * **จัดการ Log:** ตรวจสอบขนาดของ Log และลบ Log เก่าเพื่อประหยัดพื้นที่
    ```bash
    journalctl --disk-usage
    sudo journalctl --vacuum-size=1G
    ```

## 3\. แนวทางปฏิบัติที่ดีในการ Config Nginx, Gunicorn และ Systemd

### Nginx (Reverse Proxy)

Nginx ทำหน้าที่เป็น Reverse Proxy เพื่อรับ Request จากผู้ใช้และส่งต่อไปยัง Gunicorn ช่วยเพิ่มประสิทธิภาพและความปลอดภัย

  * **ตัวอย่างไฟล์ `server block` ของ Nginx**
    ```nginx
    server {
        listen 80;
        server_name your_domain.com www.your_domain.com;

        location / {
            include proxy_params;
            proxy_pass http://unix:/run/gunicorn.sock; # ส่ง Request ไปยัง Gunicorn ผ่าน Unix socket
        }
    }
    ```
  * **แนวทางปฏิบัติ:**
      * ใช้ Nginx ในการจัดการ Request ที่เข้ามาทั้งหมด
      * ใช้ Nginx ในการ Serve ไฟล์ Static เพื่อลดภาระของ Gunicorn
      * ตั้งค่า `proxy_set_header` เพื่อให้ Gunicorn ทราบข้อมูล Request ที่ถูกต้อง เช่น `X-Forwarded-Proto` สำหรับ HTTPS
      * ตรวจสอบความถูกต้องของ Configuration ด้วย `sudo nginx -t` และ `sudo systemctl restart nginx` หลังจากการแก้ไข

### Gunicorn (Application Server)

Gunicorn ทำหน้าที่รันโปรแกรม Python ของคุณใน Production Environment

  * **แนวทางปฏิบัติ:**
      * ใช้ Gunicorn ร่วมกับ Nginx
      * ตั้งค่า Gunicorn ให้ทำงานใน Background โดยใช้ `systemd`
      * ใช้ Unix Socket (`/run/gunicorn.sock`) เพื่อให้ Nginx และ Gunicorn สื่อสารกันอย่างรวดเร็วและปลอดภัย

### Systemd (Configuration)

การใช้ `systemd` ในการจัดการ Gunicorn เป็นวิธีที่แนะนำเพื่อให้แอปพลิเคชันทำงานได้อย่างเสถียร

  * **ตัวอย่างไฟล์ `gunicorn.socket`:**
    ```ini
    [Unit]
    Description=gunicorn socket for my app

    [Socket]
    ListenStream=/run/gunicorn.sock

    [Install]
    WantedBy=sockets.target
    ```
  * **ตัวอย่างไฟล์ `gunicorn.service`:**
    ```ini
    [Unit]
    Description=Gunicorn service for my app
    After=network.target

    [Service]
    User=your_username
    Group=www-data
    WorkingDirectory=/path/to/your/app
    ExecStart=/path/to/your/venv/bin/gunicorn --workers 3 --bind unix:/run/gunicorn.sock wsgi:app
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```
  * **แนวทางปฏิบัติ:**
      * ใช้ `systemctl daemon-reload` เพื่อโหลดไฟล์ Configuration ใหม่หลังจากแก้ไข
      * ใช้ `systemctl enable --now gunicorn.socket gunicorn.service` เพื่อเริ่มและเปิดใช้งานบริการทันที
      * ตรวจสอบสถานะด้วย `systemctl status gunicorn.service`
      * ตั้งค่า `User` และ `Group` ให้เหมาะสมเพื่อความปลอดภัย
      * กำหนด `WorkingDirectory` ให้ถูกต้องเพื่อให้ Gunicorn หาไฟล์โปรเจกต์เจอ


การเขียนโค้ดตามแนวทางปฏิบัติที่ดีเป็นสิ่งสำคัญที่จะช่วยให้โค้ดอ่านง่าย บำรุงรักษาง่าย และทำงานร่วมกับผู้อื่นได้อย่างมีประสิทธิภาพ 

-----

### 1\. แนวทางปฏิบัติที่ดีสำหรับการเขียนโค้ด Python ตามมาตรฐาน PEP 8

**PEP 8 (Python Enhancement Proposal 8)** คือแนวทางในการเขียนโค้ด Python ที่ทุกคนในชุมชน Python ยอมรับและใช้เป็นมาตรฐาน เพื่อให้โค้ดมีความสอดคล้องกันและอ่านง่ายขึ้นมากครับ

**หลักการสำคัญของ PEP 8:**

  * **การเว้นวรรค (Indentation):** ใช้ 4 Space ในการเว้นวรรคแต่ละระดับ **ไม่ใช้ Tab**

    ```python
    # ถูกต้อง
    def my_function():
        x = 1
        if x == 1:
            print("Hello")

    # ผิด (ใช้ 2 space)
    def my_function():
      x = 1
    ```

  * **ความยาวบรรทัด:** จำกัดความยาวบรรทัดไม่เกิน 79 ตัวอักษร เพื่อให้โค้ดดูง่ายบนหน้าจอขนาดเล็ก

    ```python
    # ถูกต้อง (ตัดบรรทัดโดยใช้ \ หรือในวงเล็บ)
    long_variable_name = "This is a very long string that needs " \
                         "to be broken into multiple lines."

    def long_function(param_1, param_2,
                      param_3, param_4):
        pass
    ```

  * **การเว้นบรรทัดเปล่า:**

      * เว้น 2 บรรทัดเปล่าระหว่าง Class และ Function ระดับบนสุด (Top-level)
      * เว้น 1 บรรทัดเปล่าระหว่าง method ภายใน Class

    <!-- end list -->

    ```python
    # เว้น 2 บรรทัดระหว่าง class และ function
    class MyClass:
        pass


    def my_function():
        pass
    ```

  * **การตั้งชื่อ (Naming Conventions):**

      * **ตัวแปรและฟังก์ชัน:** ใช้ `snake_case` (ตัวพิมพ์เล็กคั่นด้วยขีดล่าง) เช่น `my_variable`, `calculate_total()`
      * **คลาส (Class):** ใช้ `PascalCase` หรือ `CamelCase` (ตัวอักษรตัวแรกของแต่ละคำเป็นตัวใหญ่) เช่น `MyClass`
      * **ค่าคงที่ (Constants):** ใช้ `ALL_CAPS` (ตัวพิมพ์ใหญ่ทั้งหมดคั่นด้วยขีดล่าง) เช่น `MAX_SIZE`

  * **การใช้เว้นวรรครอบตัวดำเนินการ (Operators):**

      * เว้น 1 ช่องว่างรอบๆ ตัวดำเนินการ เช่น `=`, `+`, `-`, `*`

    <!-- end list -->

    ```python
    # ถูกต้อง
    x = 1 + 2

    # ผิด
    x=1+2
    ```

**เครื่องมือช่วยตรวจสอบ:**

  * **`flake8`:** เป็นเครื่องมือที่ใช้ตรวจสอบโค้ดตามมาตรฐาน PEP 8 และอื่นๆ
  * **`autopep8`:** เป็นเครื่องมือที่แก้ไขโค้ดของคุณให้เป็นไปตาม PEP 8 โดยอัตโนมัติ

-----

### 2\. การ Import แบบ Absolute Imports

**Absolute Imports** คือการอ้างอิงโมดูลหรือแพ็กเกจจาก root directory ของโปรเจกต์ของคุณ ซึ่งเป็นวิธีที่แนะนำเพราะทำให้โค้ดมีความชัดเจนและไม่สับสนเมื่อต้องจัดการกับโครงสร้างไฟล์ที่ซับซ้อน

**ตัวอย่างโครงสร้างโปรเจกต์:**

```
my_project/
├── main.py
├── package_a/
│   ├── __init__.py
│   ├── module_1.py
│   └── sub_package_a/
│       ├── __init__.py
│       └── module_2.py
└── package_b/
    ├── __init__.py
    └── module_3.py
```

**ตัวอย่างการ Import แบบ Absolute:**
ถ้าคุณต้องการ import `do_something()` จาก `module_2.py` ไปใช้ใน `main.py`

```python
# ในไฟล์ my_project/main.py
from package_a.sub_package_a.module_2 import do_something

def main():
    do_something()

if __name__ == "__main__":
    main()
```

การ Import แบบนี้จะเริ่มจากชื่อแพ็กเกจหลัก `package_a` เสมอ ทำให้คุณทราบทันทีว่าโค้ดที่เรียกใช้มาจากที่ใด

-----

### 3\. การนำเข้า Git Repository อื่นเข้ามาเป็นส่วนหนึ่งใน Repository ของเรา

การนำโค้ดจาก Git Repository อื่นเข้ามาเป็นส่วนหนึ่งของโปรเจกต์เรา มักทำได้ด้วยวิธี **Git Submodule** ซึ่งเป็นการผูก Repository ภายนอกเข้ากับโปรเจกต์หลักของเรา โดยจะยังคงสถานะเป็น Repository แยกต่างหาก

#### แนวทางการใช้ Git Submodule

**ขั้นตอนที่ 1: การเพิ่ม Submodule**
ใช้คำสั่ง `git submodule add` เพื่อเพิ่ม Repository ที่ต้องการเข้ามาในโปรเจกต์ของคุณ
สมมติว่าคุณต้องการเพิ่มไลบรารีชื่อ `my-utility` เข้ามาในโฟลเดอร์ `vendor/`

```bash
git submodule add https://github.com/user/my-utility.git vendor/my-utility
```

คำสั่งนี้จะ:

1.  Clone `my-utility` Repository เข้ามาในโฟลเดอร์ `vendor/my-utility`
2.  เพิ่มไฟล์ `.gitmodules` ที่จะเก็บข้อมูลของ Submodule
3.  เพิ่มโฟลเดอร์ `vendor/my-utility` เข้ามาใน Git Index ของโปรเจกต์หลัก

**ขั้นตอนที่ 2: Clone Repository ที่มี Submodule**
หากมีผู้อื่น `git clone` โปรเจกต์หลักของคุณไป พวกเขาจะต้องใช้คำสั่งเพิ่มเติมเพื่อดึงโค้ดของ Submodule เข้ามาด้วย

```bash
# Clone โปรเจกต์หลัก
git clone https://github.com/popwandee/your-project.git

# Initialise และ Update submodule
cd your-project
git submodule update --init --recursive
```

  * `--init` ใช้สำหรับ Initialise Submodule ที่ยังไม่ถูกโหลดเข้ามา
  * `--recursive` ใช้สำหรับกรณีที่ Submodule นั้นมี Submodule ซ้อนอยู่ข้างในอีกที

**ข้อดีของ Git Submodule:**

  * สามารถรันและแก้ไขโค้ดใน Submodule ได้เหมือนกับเป็น Git Repository ปกติ
  * โค้ดของ Submodule จะแยกจากโค้ดของโปรเจกต์หลัก ทำให้จัดการการเปลี่ยนแปลงได้ง่าย

**ข้อควรระวัง:**

  * เมื่อทำการ Commit ใน Submodule และต้องการให้โปรเจกต์หลักอ้างอิงถึง Commit ล่าสุดนั้น ต้อง `git add` และ `git commit` ในโปรเจกต์หลักอีกครั้ง เพื่อบันทึกการเปลี่ยนแปลงของ Submodule
# อัปเดต submodules
git submodule update --init --recursive
```

### การติดตั้ง Dependencies

```bash
# ติดตั้ง Python dependencies
pip install -r requirements.txt

# สำหรับ Raspberry Pi Camera
sudo apt install libcamera-apps python3-picamera2

# สำหรับ Hailo8 (ดูคู่มือใน dev-knowledge-base/ai_vision/)
# Download และติดตั้ง HailoRT จาก hailo.ai
```

## 💡 Quick Start

### 1. การจัดการกล้อง

```python
from pwd_library.camera.picamera2_cm3 import PiCameraManager

# เริ่มต้นกล้อง
with PiCameraManager() as camera:
    # เริ่มต้นกล้อง
    camera.initialize_camera(resolution=(1920, 1080), framerate=30)
    
    # จับภาพ
    image = camera.capture_image()
    
    # บันทึกภาพ
    camera.capture_to_file("captured_image.jpg")
    
    # เริ่ม video streaming
    camera.start_video_stream(resolution=(640, 480))
    frame = camera.get_frame()
```

### 2. AI Processing ด้วย Hailo8

```python
from pwd_library.model.hailo8_processor import Hailo8Processor
from pwd_library.image_processing.preprocessor import ImagePreprocessor
import cv2

# เริ่มต้น processor
with Hailo8Processor("models/yolov8n.hef") as processor:
    # อ่านภาพ
    image = cv2.imread("input.jpg")
    
    # ทำ inference
    results = processor.predict(image)
    
    # แสดงผลลัพธ์
    for detection in results:
        print(f"Object: {detection['class']}, Confidence: {detection['confidence']}")
```

### 3. Image Processing

```python
from pwd_library.image_processing.preprocessor import ImagePreprocessor
import cv2

# สร้าง preprocessor
preprocessor = ImagePreprocessor(target_size=(640, 640))

# อ่านภาพ
image = cv2.imread("input.jpg")

# Preprocess ภาพ
resized = preprocessor.resize_with_padding(image)
normalized = preprocessor.normalize(resized, method="imagenet")

# หรือใช้ preprocess แบบเฉพาะสำหรับ model
processed = preprocessor.preprocess_for_model(image, model_type="yolo")
```

### 4. Drawing และ Visualization

```python
from pwd_library.utils.drawing_utils import draw_detections
import cv2

# วาดผลการตรวจจับ
image_with_boxes = draw_detections(image, results)

# แสดงผล
cv2.imshow("Detections", image_with_boxes)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## 📋 Requirements

### System Requirements
- **Python**: 3.8+
- **OS**: Ubuntu 20.04+ / Raspberry Pi OS
- **Hardware**: Raspberry Pi 4/5 (สำหรับ camera และ edge computing)

### Python Dependencies
```
opencv-python>=4.5.0
numpy>=1.21.0
pillow>=8.3.0
picamera2  # สำหรับ Raspberry Pi Camera
hailo-platform  # สำหรับ Hailo8 AI
```

### Hardware Support
- **Cameras**: 
  - Raspberry Pi Camera Module v2/v3
  - USB UVC compatible cameras
  - Industrial cameras
- **AI Accelerators**: 
  - Hailo8 AI processor
  - Support for other accelerators (coming soon)

## 📚 Documentation

### Best Practices Guides
- [Python Best Practices](dev-knowledge-base/python/best_practices.md)
- [Hailo AI Best Practices](dev-knowledge-base/ai_vision/hailo_best_practices.md)
- [Camera Management](dev-knowledge-base/camera/camera_management.md)
- [Deployment Guide](dev-knowledge-base/deployment/deployment_guide.md)

### Technical References
- [Linux Commands](dev-knowledge-base/linux_commands/)
- [Network Configuration](dev-knowledge-base/network/)
- [Docker Usage](dev-knowledge-base/docker/)
- [Database Management](dev-knowledge-base/sql/)

## 🔧 Configuration

สร้างไฟล์ `config.yaml` สำหรับการตั้งค่าระบบ:

```yaml
# config.yaml
system:
  name: "PWD Vision System"
  log_level: "INFO"
  
camera:
  type: "picamera2"
  resolution: [1920, 1080]
  framerate: 30
  
hailo:
  model_path: "models/yolov8n.hef"
  confidence_threshold: 0.5
  nms_threshold: 0.4
  
image_processing:
  target_size: [640, 640]
  normalization: "imagenet"
```

## 🚀 Advanced Usage

### Multi-Camera Setup

```python
from pwd_library.camera.picamera2_cm3 import MultiCameraManager

# จัดการหลายกล้อง
camera_manager = MultiCameraManager()

# เพิ่มกล้อง
camera_manager.add_camera("main", "pi_camera", {"resolution": (1920, 1080)})
camera_manager.add_camera("side", "usb_camera", {"device_id": 1})

# จับภาพจากทุกกล้อง
images = camera_manager.capture_all()
```

### Batch Processing

```python
from pwd_library.image_processing.preprocessor import ImagePreprocessor

preprocessor = ImagePreprocessor()

# ประมวลผล batch
images = [cv2.imread(f"image_{i}.jpg") for i in range(10)]
batch = preprocessor.preprocess_batch(images, normalize_method="zero_one")

# Batch inference
results = processor.batch_predict(images)
```

### Performance Monitoring

```python
from pwd_library.model.hailo8_processor import HailoHealthMonitor

# ติดตามประสิทธิภาพ
monitor = HailoHealthMonitor()

# หลังจาก inference แต่ละครั้ง
monitor.log_inference(success=True, inference_time=0.05)

# ดูสถิติ
stats = monitor.get_stats()
print(f"FPS: {stats['avg_fps']:.2f}, Success Rate: {stats['success_rate']:.2%}")
```

## 🐛 Error Handling

```python
from pwd_library.utils.exceptions import CameraError, InferenceError, handle_exception

try:
    # Your code here
    result = processor.predict(image)
except InferenceError as e:
    logger.error(f"Inference failed: {e.message} (Code: {e.error_code})")
    result = handle_exception(e, default_return=[])
```

## 🧪 Testing

```bash
# รันการทดสอบ
python -m pytest tests/

# ทดสอบกล้อง
python -c "
from pwd_library.camera.picamera2_cm3 import detect_available_cameras
cameras = detect_available_cameras()
print(f'Found {len(cameras)} camera(s)')
"

# ทดสอบ Hailo device
python -c "
from pwd_library.model.hailo8_processor import detect_hailo_devices
devices = detect_hailo_devices()
print(f'Found {len(devices)} Hailo device(s)')
"
```

## 📈 Performance Tips

### สำหรับ Raspberry Pi
```python
# เพิ่มประสิทธิภาพกล้อง
camera.optimize_for_performance()

# ตั้งค่า GPU memory
# ใน /boot/config.txt: gpu_mem=256

# ใช้ threading สำหรับ real-time processing
import threading
from concurrent.futures import ThreadPoolExecutor
```

### สำหรับ AI Inference
```python
# ใช้ batch processing
batch_size = 4
results = processor.batch_predict(images[:batch_size])

# Memory management
with processor.inference_context():
    result = processor.predict(image)
```

## 🤝 Contributing

เรายินดีรับการร่วมพัฒนา! กรุณาอ่าน guidelines ใน:
- [Python Best Practices](dev-knowledge-base/python/best_practices.md)
- [Git Guidelines](dev-knowledge-base/git/common_command.md)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Contact

- **Documentation**: [dev-knowledge-base/](dev-knowledge-base/)
- **Issues**: สร้าง GitHub issue
- **Email**: contact@pwdvisionworks.com
- **Website**: https://pwdvisionworks.com

## 🔄 Changelog

### v1.0.0 (Current)
- ✅ Raspberry Pi Camera support
- ✅ Hailo8 AI integration
- ✅ Image processing pipeline
- ✅ Comprehensive documentation
- ✅ Error handling system
- ✅ Performance monitoring

### Upcoming Features
- 🚧 Web interface สำหรับ monitoring
- 🚧 Cloud integration
- 🚧 Additional AI model support
- 🚧 Mobile app connectivity

---

**PWD Vision Works** - Making Computer Vision Accessible
