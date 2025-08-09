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

### การติดตั้งแบบ Submodule

เพิ่ม PWD Library เป็น Git Submodule ในโปรเจกต์ของคุณ:

```bash
# เพิ่ม submodule
git submodule add https://github.com/popwandee/pwd_library.git

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
