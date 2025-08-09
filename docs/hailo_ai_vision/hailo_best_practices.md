# Hailo AI Processor - Best Practices

## ภาพรวม
คู่มือการใช้งาน Hailo8 AI processor อย่างมีประสิทธิภาพสำหรับงาน Computer Vision

## การติดตั้งและการตั้งค่า

### 1. ข้อกำหนดระบบ
```bash
# Ubuntu 20.04+ / Raspberry Pi OS
sudo apt update
sudo apt install python3-dev python3-pip
```

### 2. การติดตั้ง Hailo Software Suite
```bash
# ติดตั้ง HailoRT
wget https://hailo.ai/developer-zone/software-downloads/
# ทำตามขั้นตอนการติดตั้งจากเอกสารทางการ
```

## โครงสร้างโมเดล

### 1. รูปแบบไฟล์โมเดล
- `.hef` - Hailo Executable Format (โมเดลที่คอมไพล์แล้ว)
- `.onnx` - Open Neural Network Exchange (ก่อนการคอมไพล์)

### 2. การจัดการโมเดล
```python
from pathlib import Path

class HailoModelManager:
    def __init__(self, model_dir: str = "models/"):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(exist_ok=True)
        
    def load_model(self, model_name: str) -> "HailoModel":
        """โหลดโมเดล Hailo"""
        model_path = self.model_dir / f"{model_name}.hef"
        
        if not model_path.exists():
            raise FileNotFoundError(f"ไม่พบโมเดล: {model_path}")
            
        return HailoModel(model_path)
```

## การประมวลผลภาพ

### 1. Pre-processing Pipeline
```python
import numpy as np
import cv2
from typing import Tuple

def preprocess_image(image: np.ndarray, 
                    target_size: Tuple[int, int] = (640, 640),
                    normalize: bool = True) -> np.ndarray:
    """
    เตรียมภาพสำหรับโมเดล Hailo
    
    Args:
        image: ภาพต้นฉบับ (BGR format)
        target_size: ขนาดเป้าหมาย (width, height)
        normalize: ปรับค่าพิกเซลเป็น 0-1
        
    Returns:
        ภาพที่เตรียมแล้ว
    """
    # Resize while maintaining aspect ratio
    h, w = image.shape[:2]
    scale = min(target_size[0]/w, target_size[1]/h)
    new_w, new_h = int(w*scale), int(h*scale)
    
    resized = cv2.resize(image, (new_w, new_h))
    
    # Pad to target size
    padded = np.zeros((target_size[1], target_size[0], 3), dtype=np.uint8)
    y_offset = (target_size[1] - new_h) // 2
    x_offset = (target_size[0] - new_w) // 2
    padded[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
    
    if normalize:
        padded = padded.astype(np.float32) / 255.0
        
    return padded
```

### 2. Batch Processing
```python
def batch_inference(model: "HailoModel", 
                   images: List[np.ndarray],
                   batch_size: int = 8) -> List[np.ndarray]:
    """ประมวลผลภาพเป็นชุด เพื่อประสิทธิภาพสูงสุด"""
    results = []
    
    for i in range(0, len(images), batch_size):
        batch = images[i:i+batch_size]
        
        # Preprocess batch
        processed_batch = [preprocess_image(img) for img in batch]
        batch_input = np.stack(processed_batch)
        
        # Inference
        batch_output = model.predict(batch_input)
        results.extend(batch_output)
        
    return results
```

## การจัดการหน่วยความจำ

### 1. Memory Pool
```python
import gc
from contextlib import contextmanager

@contextmanager
def hailo_inference_context():
    """Context manager สำหรับการจัดการหน่วยความจำ"""
    try:
        # Pre-allocate buffers
        yield
    finally:
        # Cleanup
        gc.collect()

# การใช้งาน
with hailo_inference_context():
    results = model.predict(batch_images)
```

### 2. การใช้งาน GPU Memory
```python
def optimize_memory_usage():
    """เพิ่มประสิทธิภาพการใช้หน่วยความจำ"""
    # ใช้ memory mapping สำหรับไฟล์ขนาดใหญ่
    # จำกัดขนาด batch ตามหน่วยความจำที่มี
    # ใช้ data generator แทนการโหลดข้อมูลทั้งหมด
    pass
```

## Performance Optimization

### 1. Threading และ Multiprocessing
```python
import threading
import queue
from concurrent.futures import ThreadPoolExecutor

class HailoInferenceEngine:
    def __init__(self, model_path: str, num_threads: int = 4):
        self.model = HailoModel(model_path)
        self.num_threads = num_threads
        self.input_queue = queue.Queue(maxsize=100)
        self.output_queue = queue.Queue()
        
    def start_inference_threads(self):
        """เริ่ม inference threads"""
        self.executor = ThreadPoolExecutor(max_workers=self.num_threads)
        for _ in range(self.num_threads):
            self.executor.submit(self._inference_worker)
            
    def _inference_worker(self):
        """Worker thread สำหรับ inference"""
        while True:
            try:
                image = self.input_queue.get(timeout=1)
                result = self.model.predict(image)
                self.output_queue.put(result)
                self.input_queue.task_done()
            except queue.Empty:
                break
```

### 2. Profiling และ Benchmarking
```python
import time
from functools import wraps

def benchmark_inference(func):
    """Decorator สำหรับวัดประสิทธิภาพ"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

@benchmark_inference
def run_inference(model, image):
    return model.predict(image)
```

## Error Handling

### 1. Custom Exceptions
```python
class HailoError(Exception):
    """Base exception สำหรับ Hailo operations"""
    pass

class ModelLoadError(HailoError):
    """Exception สำหรับการโหลดโมเดลผิดพลาด"""
    pass

class InferenceError(HailoError):
    """Exception สำหรับการ inference ผิดพลาด"""
    pass

def safe_inference(model, image):
    """Inference พร้อม error handling"""
    try:
        return model.predict(image)
    except Exception as e:
        raise InferenceError(f"Inference failed: {e}") from e
```

### 2. Health Monitoring
```python
class HailoHealthMonitor:
    def __init__(self):
        self.inference_count = 0
        self.error_count = 0
        self.start_time = time.time()
        
    def log_inference(self, success: bool = True):
        """บันทึกข้อมูล inference"""
        self.inference_count += 1
        if not success:
            self.error_count += 1
            
    def get_stats(self) -> dict:
        """ดึงสถิติการทำงาน"""
        runtime = time.time() - self.start_time
        return {
            "total_inferences": self.inference_count,
            "errors": self.error_count,
            "success_rate": (self.inference_count - self.error_count) / self.inference_count,
            "fps": self.inference_count / runtime
        }
```

## Deployment

### 1. Docker Configuration
```dockerfile
FROM ubuntu:20.04

# ติดตั้ง dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libopencv-dev

# Copy Hailo software
COPY hailo-sw/ /opt/hailo/

# Copy application
COPY pwd_library/ /app/pwd_library/
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

CMD ["python3", "-m", "pwd_library.hailo.detect"]
```

### 2. System Service
```ini
# /etc/systemd/system/hailo-vision.service
[Unit]
Description=PWD Vision Works - Hailo AI Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/pwd_library
ExecStart=/usr/bin/python3 -m pwd_library.hailo.detect
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## การทดสอบ

### 1. Unit Tests
```python
import pytest
import numpy as np

class TestHailoProcessor:
    def test_model_loading(self):
        """ทดสอบการโหลดโมเดล"""
        processor = HailoProcessor("models/yolov5.hef")
        assert processor.is_loaded()
        
    def test_inference(self):
        """ทดสอบการ inference"""
        image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
        results = processor.detect(image)
        assert len(results) >= 0
        
    def test_batch_processing(self):
        """ทดสอบการประมวลผลแบบ batch"""
        images = [np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8) 
                 for _ in range(10)]
        results = processor.batch_detect(images)
        assert len(results) == len(images)
```

## การติดตาม (Monitoring)

### 1. Logging
```python
import logging
import sys

def setup_hailo_logging():
    """ตั้งค่า logging สำหรับ Hailo operations"""
    logger = logging.getLogger('hailo')
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
```

### 2. Metrics Collection
```python
from dataclasses import dataclass
from typing import Dict

@dataclass
class InferenceMetrics:
    fps: float
    avg_latency: float
    memory_usage: float
    cpu_usage: float
    
def collect_metrics() -> InferenceMetrics:
    """เก็บข้อมูล metrics ของระบบ"""
    # Implementation for collecting system metrics
    pass
```