# Camera Management - PWD Vision Works

## ภาพรวม
คู่มือการจัดการกล้องสำหรับระบบ Computer Vision ครอบคลุมการใช้งาน Raspberry Pi Camera และ USB Camera

## รองรับกล้องประเภท

### 1. Raspberry Pi Camera Module
- Camera Module v2 (8MP)
- Camera Module v3 (12MP)  
- HQ Camera Module
- กล้อง NoIR สำหรับถ่ายในที่มืด

### 2. USB Cameras
- UVC (USB Video Class) compatible cameras
- Web cameras ทั่วไป
- Industrial cameras

## การติดตั้ง

### 1. Raspberry Pi Camera
```bash
# เปิดใช้งาน camera interface
sudo raspi-config
# Interfacing Options -> Camera -> Enable

# ตรวจสอบการเชื่อมต่อ
vcgencmd get_camera

# ติดตั้ง libcamera tools
sudo apt update
sudo apt install libcamera-apps
```

### 2. USB Camera
```bash
# ตรวจสอบกล้อง USB
lsusb | grep -i camera
v4l2-ctl --list-devices

# ติดตั้ง v4l-utils
sudo apt install v4l-utils
```

## การใช้งาน PiCamera2

### 1. การตั้งค่าเบื้องต้น
```python
from picamera2 import Picamera2
import cv2
import numpy as np

class PWDCameraManager:
    def __init__(self):
        self.picam2 = None
        self.is_initialized = False
        
    def initialize_camera(self, resolution=(1920, 1080)):
        """เริ่มต้นกล้อง Raspberry Pi"""
        try:
            self.picam2 = Picamera2()
            
            # ตั้งค่า configuration
            config = self.picam2.create_still_configuration(
                main={"size": resolution, "format": "RGB888"}
            )
            self.picam2.configure(config)
            
            self.picam2.start()
            self.is_initialized = True
            print(f"Camera initialized with resolution: {resolution}")
            
        except Exception as e:
            print(f"Failed to initialize camera: {e}")
            self.is_initialized = False
```

### 2. การจับภาพ
```python
def capture_image(self) -> np.ndarray:
    """จับภาพเดี่ยว"""
    if not self.is_initialized:
        raise RuntimeError("Camera not initialized")
        
    # Capture image
    image = self.picam2.capture_array()
    
    # Convert RGB to BGR for OpenCV
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    return image_bgr

def capture_to_file(self, filename: str):
    """บันทึกภาพลงไฟล์"""
    if not self.is_initialized:
        raise RuntimeError("Camera not initialized")
        
    self.picam2.capture_file(filename)
    print(f"Image saved to: {filename}")
```

### 3. Video Streaming
```python
def start_video_stream(self, resolution=(640, 480), framerate=30):
    """เริ่ม video streaming"""
    if not self.is_initialized:
        self.initialize_camera()
    
    # ตั้งค่า video configuration
    video_config = self.picam2.create_video_configuration(
        main={"size": resolution, "format": "RGB888"},
        controls={"FrameRate": framerate}
    )
    
    self.picam2.configure(video_config)
    self.picam2.start()

def get_frame(self) -> np.ndarray:
    """ดึงเฟรมจาก video stream"""
    frame = self.picam2.capture_array()
    return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
```

## การปรับแต่งกล้อง

### 1. การตั้งค่า Exposure และ ISO
```python
def set_camera_settings(self, exposure_time=None, iso=None, brightness=0.0):
    """ปรับแต่งการตั้งค่ากล้อง"""
    controls = {}
    
    if exposure_time:
        controls["ExposureTime"] = exposure_time  # microseconds
    
    if iso:
        controls["AnalogueGain"] = iso / 100.0  # Convert ISO to gain
        
    controls["Brightness"] = brightness  # -1.0 to 1.0
    
    self.picam2.set_controls(controls)

def enable_auto_focus(self):
    """เปิดใช้งาน autofocus (สำหรับกล้องที่รองรับ)"""
    self.picam2.set_controls({"AfMode": 2})  # Continuous autofocus
    
def set_manual_focus(self, focus_distance: float):
    """ตั้งค่า manual focus"""
    # focus_distance: 0.0 (infinity) to 1.0 (close)
    self.picam2.set_controls({
        "AfMode": 0,  # Manual
        "LensPosition": focus_distance
    })
```

### 2. White Balance และ Color
```python
def set_white_balance(self, mode="auto"):
    """ปรับ white balance"""
    wb_modes = {
        "auto": 0,
        "tungsten": 1,
        "fluorescent": 2,
        "indoor": 3,
        "daylight": 4,
        "cloudy": 5
    }
    
    if mode in wb_modes:
        self.picam2.set_controls({"AwbMode": wb_modes[mode]})

def adjust_color_gains(self, red_gain=1.0, blue_gain=1.0):
    """ปรับ color gains ด้วยตนเอง"""
    self.picam2.set_controls({
        "AwbMode": 0,  # Manual
        "ColourGains": [red_gain, blue_gain]
    })
```

## USB Camera Management

### 1. การใช้งาน OpenCV
```python
import cv2

class USBCameraManager:
    def __init__(self, device_id=0):
        self.device_id = device_id
        self.cap = None
        
    def initialize_camera(self, width=1920, height=1080, fps=30):
        """เริ่มต้นกล้อง USB"""
        self.cap = cv2.VideoCapture(self.device_id)
        
        # ตั้งค่าความละเอียดและ FPS
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open camera {self.device_id}")
            
    def get_frame(self) -> np.ndarray:
        """ดึงเฟรมจากกล้อง USB"""
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to capture frame")
        return frame
        
    def release(self):
        """ปิดกล้อง"""
        if self.cap:
            self.cap.release()
```

## การจัดการหลายกล้อง

### 1. Multi-Camera Setup
```python
class MultiCameraManager:
    def __init__(self):
        self.cameras = {}
        
    def add_camera(self, name: str, camera_type: str, config: dict):
        """เพิ่มกล้องในระบบ"""
        if camera_type == "pi_camera":
            camera = PWDCameraManager()
            camera.initialize_camera(**config)
        elif camera_type == "usb_camera":
            camera = USBCameraManager(**config)
            camera.initialize_camera()
        else:
            raise ValueError(f"Unsupported camera type: {camera_type}")
            
        self.cameras[name] = camera
        
    def capture_all(self) -> dict:
        """จับภาพจากกล้องทั้งหมด"""
        images = {}
        for name, camera in self.cameras.items():
            try:
                images[name] = camera.get_frame()
            except Exception as e:
                print(f"Failed to capture from {name}: {e}")
                
        return images
```

## Performance Optimization

### 1. การปรับแต่งประสิทธิภาพ
```python
def optimize_camera_settings(self):
    """ปรับแต่งเพื่อประสิทธิภาพสูงสุด"""
    # ลด noise processing
    self.picam2.set_controls({
        "NoiseReductionMode": 0,  # Off
        "Sharpness": 1.0
    })
    
    # ปรับ encoding quality
    encoder_config = {
        "quality": 95,
        "format": "MJPEG"  # สำหรับ streaming
    }

def enable_gpu_acceleration(self):
    """เปิดใช้งาน GPU acceleration"""
    # ใช้ H.264 hardware encoding
    self.picam2.start_and_capture_files(
        "output.h264",
        encoder="h264_v4l2m2m"
    )
```

### 2. Memory Management
```python
import gc

def efficient_capture_loop(self):
    """Loop การจับภาพที่ประหยัดหน่วยความจำ"""
    try:
        while True:
            # Capture frame
            frame = self.get_frame()
            
            # Process frame
            processed_frame = self.process_frame(frame)
            
            # Clean up
            del frame
            if gc.get_count()[0] > 700:
                gc.collect()
                
    except KeyboardInterrupt:
        self.cleanup()
        
def cleanup(self):
    """ทำความสะอาดทรัพยากร"""
    if hasattr(self, 'picam2') and self.picam2:
        self.picam2.stop()
    
    if hasattr(self, 'cap') and self.cap:
        self.cap.release()
```

## Error Handling

### 1. Custom Exceptions
```python
class CameraError(Exception):
    """Base exception สำหรับ camera operations"""
    pass

class CameraInitializationError(CameraError):
    """Exception สำหรับการเริ่มต้นกล้องผิดพลาด"""
    pass

class FrameCaptureError(CameraError):
    """Exception สำหรับการจับภาพผิดพลาด"""
    pass

def safe_camera_operation(self, operation):
    """ดำเนินการกล้องอย่างปลอดภัย"""
    try:
        return operation()
    except Exception as e:
        raise CameraError(f"Camera operation failed: {e}") from e
```

### 2. Health Monitoring
```python
import time

class CameraHealthMonitor:
    def __init__(self):
        self.frame_count = 0
        self.error_count = 0
        self.start_time = time.time()
        
    def log_frame_capture(self, success: bool = True):
        """บันทึกการจับภาพ"""
        self.frame_count += 1
        if not success:
            self.error_count += 1
            
    def get_stats(self) -> dict:
        """ดึงสถิติการทำงาน"""
        runtime = time.time() - self.start_time
        return {
            "total_frames": self.frame_count,
            "errors": self.error_count,
            "success_rate": (self.frame_count - self.error_count) / self.frame_count if self.frame_count > 0 else 0,
            "fps": self.frame_count / runtime if runtime > 0 else 0
        }
```

## Troubleshooting

### 1. ปัญหาที่พบบ่อย
```bash
# กล้องไม่ทำงาน
sudo modprobe bcm2835-v4l2

# ตรวจสอบ permissions
sudo usermod -a -G video $USER

# รีสตาร์ทกล้อง service
sudo systemctl restart camera
```

### 2. การ Debug
```python
def debug_camera_info(self):
    """แสดงข้อมูลกล้องเพื่อ debug"""
    if hasattr(self, 'picam2'):
        print("Pi Camera Properties:")
        print(f"Camera info: {self.picam2.camera_properties}")
        print(f"Available modes: {self.picam2.sensor_modes}")
    
    if hasattr(self, 'cap'):
        print("USB Camera Properties:")
        print(f"Width: {self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)}")
        print(f"Height: {self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
        print(f"FPS: {self.cap.get(cv2.CAP_PROP_FPS)}")
```