# Best Practices สำหรับการเขียน Python - PWD Vision Works

## Code Style และ Formatting

### 1. ใช้ PEP 8 Style Guide
- ใช้ 4 spaces สำหรับ indentation
- ชื่อ function และ variable ใช้ snake_case
- ชื่อ class ใช้ PascalCase  
- ชื่อ constant ใช้ UPPER_CASE

```python
# ✅ ถูกต้อง
def process_image_data(image_path: str) -> np.ndarray:
    """ประมวลผลข้อมูลภาพ"""
    pass

class ImageProcessor:
    MAX_WIDTH = 1920
    MAX_HEIGHT = 1080
    
# ❌ ไม่ถูกต้อง
def processImageData(imagePath):
    pass
```

### 2. Type Hints
ใช้ type hints เสมอเพื่อให้โค้ดชัดเจนและง่ายต่อการ maintain

```python
from typing import List, Dict, Optional, Union
import numpy as np

def detect_objects(image: np.ndarray, 
                  confidence_threshold: float = 0.5) -> List[Dict[str, Union[str, float]]]:
    """
    ตรวจจับวัตถุในภาพ
    
    Args:
        image: ภาพที่จะตรวจจับ
        confidence_threshold: ค่าความเชื่อมั่นขั้นต่ำ
        
    Returns:
        รายการของวัตถุที่ตรวจพบพร้อมข้อมูล
    """
    pass
```

## Documentation

### 1. Docstrings
ใช้ Google Style docstrings

```python
def resize_image(image: np.ndarray, width: int, height: int) -> np.ndarray:
    """ปรับขนาดภาพ
    
    Args:
        image: ภาพต้นฉบับ
        width: ความกว้างใหม่
        height: ความสูงใหม่
        
    Returns:
        ภาพที่ปรับขนาดแล้ว
        
    Raises:
        ValueError: หากขนาดไม่ถูกต้อง
        
    Example:
        >>> image = load_image("photo.jpg")
        >>> resized = resize_image(image, 640, 480)
    """
    pass
```

### 2. README Files
แต่ละโมดูลควรมี README.md อธิบายการใช้งาน

## Error Handling

### 1. ใช้ Specific Exceptions
```python
# ✅ ดี
try:
    result = process_hailo_model(model_path)
except FileNotFoundError:
    logger.error(f"ไม่พบไฟล์โมเดล: {model_path}")
    raise
except ModelLoadError:
    logger.error("ไม่สามารถโหลดโมเดล Hailo ได้")
    raise

# ❌ ไม่ดี
try:
    result = process_hailo_model(model_path)
except Exception as e:
    print(f"Error: {e}")
```

### 2. Logging
ใช้ logging module แทน print

```python
import logging

logger = logging.getLogger(__name__)

def process_camera_feed():
    logger.info("เริ่มการประมวลผลจากกล้อง")
    try:
        # process logic
        logger.debug("ประมวลผลเฟรมสำเร็จ")
    except Exception as e:
        logger.error(f"เกิดข้อผิดพลาดในการประมวลผล: {e}")
        raise
```

## Code Organization

### 1. โครงสร้างโมดูล
```
module_name/
├── __init__.py          # Exports หลัก
├── core.py             # ฟังก์ชันหลัก
├── utils.py            # ฟังก์ชันช่วย
├── exceptions.py       # Custom exceptions
└── tests/              # Unit tests
    └── test_core.py
```

### 2. Imports
```python
# Standard library imports
import os
import sys
from typing import List, Dict

# Third-party imports
import numpy as np
import cv2
from PIL import Image

# Local application imports
from ..utils import drawing_utils
from .exceptions import ModelLoadError
```

## Testing

### 1. Unit Tests
ใช้ pytest สำหรับเขียน tests

```python
import pytest
from pwd_library.camera import PiCameraManager

def test_camera_initialization():
    """ทดสอบการเริ่มต้นกล้อง"""
    camera = PiCameraManager()
    assert camera.is_ready()
    
def test_invalid_model_path():
    """ทดสอบการจัดการไฟล์โมเดลที่ไม่ถูกต้อง"""
    with pytest.raises(FileNotFoundError):
        process_hailo_model("/invalid/path")
```

## Performance

### 1. Memory Management
```python
# ✅ ดี - ใช้ context manager
def process_large_image(image_path: str):
    with Image.open(image_path) as img:
        # process image
        return processed_result

# ✅ ดี - ใช้ numpy arrays อย่างมีประสิทธิภาพ
def batch_process(images: List[np.ndarray]) -> List[np.ndarray]:
    # ประมวลผลทีละชุด
    batch_size = 32
    results = []
    
    for i in range(0, len(images), batch_size):
        batch = images[i:i+batch_size]
        batch_results = model.predict(np.stack(batch))
        results.extend(batch_results)
    
    return results
```

## Security

### 1. Input Validation
```python
def load_image(file_path: str) -> np.ndarray:
    """โหลดภาพพร้อม validation"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"ไม่พบไฟล์: {file_path}")
    
    # ตรวจสอบนามสกุลไฟล์
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    if not any(file_path.lower().endswith(ext) for ext in allowed_extensions):
        raise ValueError("รูปแบบไฟล์ไม่รองรับ")
    
    return cv2.imread(file_path)
```

### 2. ไม่ expose sensitive information
```python
# ✅ ดี
logger.info("การเชื่อมต่อ API สำเร็จ")

# ❌ ไม่ดี
logger.info(f"เชื่อมต่อด้วย API key: {api_key}")
```

## Git และ Version Control

### 1. Commit Messages
```
feat: เพิ่มฟีเจอร์ object detection ด้วย Hailo8
fix: แก้ไขปัญหา memory leak ใน camera module  
docs: อัปเดต API documentation
refactor: ปรับปรุงโครงสร้าง image processing
```

### 2. Branch Naming
```
feature/camera-streaming
bugfix/hailo-model-loading
hotfix/memory-leak-fix
release/v1.2.0
```

## Dependencies Management

### 1. Requirements
ใช้ requirements.txt พร้อม pin versions

```txt
numpy==1.21.0
opencv-python==4.5.3.56
Pillow>=8.3.0,<9.0.0
pytest>=6.0.0
```

### 2. Virtual Environment
```bash
# สร้าง virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# ติดตั้ง dependencies
pip install -r requirements.txt
```