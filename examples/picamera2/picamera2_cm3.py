"""
PWD Vision Works - Raspberry Pi Camera Manager
สำหรับจัดการกล้อง Raspberry Pi Camera Module ทุกรุ่น

Author: PWD Vision Works
Version: 1.0.0
"""

import time
import logging
from typing import Optional, Tuple, Dict, Any
from pathlib import Path
import numpy as np
import cv2

try:
    from picamera2 import Picamera2
    PICAMERA2_AVAILABLE = True
except ImportError:
    PICAMERA2_AVAILABLE = False
    logging.warning("picamera2 not available. Please install: pip install picamera2")

from ..utils.exceptions import CameraError, CameraInitializationError, FrameCaptureError

logger = logging.getLogger(__name__)


class PiCameraManager:
    """
    จัดการ Raspberry Pi Camera Module
    รองรับ Camera v2, v3, HQ Camera และ NoIR
    """
    
    def __init__(self, camera_num: int = 0):
        """
        เริ่มต้น PiCameraManager
        
        Args:
            camera_num: หมายเลขกล้อง (0 สำหรับกล้องหลัก)
        """
        if not PICAMERA2_AVAILABLE:
            raise ImportError("picamera2 library not available")
            
        self.camera_num = camera_num
        self.picam2: Optional[Picamera2] = None
        self.is_initialized = False
        self.current_config = None
        
        # Default settings
        self.default_resolution = (1920, 1080)
        self.default_framerate = 30
        
        logger.info(f"PiCameraManager initialized for camera {camera_num}")
    
    def initialize_camera(self, 
                         resolution: Tuple[int, int] = None,
                         framerate: int = None,
                         format: str = "RGB888") -> bool:
        """
        เริ่มต้นกล้อง Raspberry Pi
        
        Args:
            resolution: ความละเอียดกล้อง (width, height)
            framerate: อัตราเฟรม
            format: รูปแบบสี (RGB888, BGR888, YUV420)
            
        Returns:
            True หากเริ่มต้นสำเร็จ
            
        Raises:
            CameraInitializationError: หากไม่สามารถเริ่มต้นกล้องได้
        """
        try:
            if self.is_initialized:
                logger.warning("Camera already initialized")
                return True
                
            # ใช้ค่า default หากไม่ได้กำหนด
            resolution = resolution or self.default_resolution
            framerate = framerate or self.default_framerate
            
            logger.info(f"Initializing camera with resolution {resolution}, fps {framerate}")
            
            # สร้าง Picamera2 instance
            self.picam2 = Picamera2(self.camera_num)
            
            # ตั้งค่า configuration
            config = self.picam2.create_still_configuration(
                main={"size": resolution, "format": format},
                controls={"FrameRate": framerate}
            )
            
            self.picam2.configure(config)
            self.current_config = config
            
            # เริ่มต้นกล้อง
            self.picam2.start()
            self.is_initialized = True
            
            # รอให้กล้องเริ่มต้นเสร็จ
            time.sleep(2)
            
            logger.info("Camera initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize camera: {e}")
            self.is_initialized = False
            raise CameraInitializationError(f"Camera initialization failed: {e}") from e
    
    def capture_image(self) -> np.ndarray:
        """
        จับภาพเดี่ยว
        
        Returns:
            numpy array ของภาพ (BGR format สำหรับ OpenCV)
            
        Raises:
            FrameCaptureError: หากไม่สามารถจับภาพได้
        """
        if not self.is_initialized:
            raise FrameCaptureError("Camera not initialized")
        
        try:
            # จับภาพ
            image = self.picam2.capture_array()
            
            # แปลงจาก RGB เป็น BGR สำหรับ OpenCV
            if len(image.shape) == 3 and image.shape[2] == 3:
                image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            else:
                image_bgr = image
                
            logger.debug(f"Captured image shape: {image_bgr.shape}")
            return image_bgr
            
        except Exception as e:
            logger.error(f"Failed to capture image: {e}")
            raise FrameCaptureError(f"Image capture failed: {e}") from e
    
    def capture_to_file(self, filename: str) -> bool:
        """
        บันทึกภาพลงไฟล์
        
        Args:
            filename: ชื่อไฟล์ที่ต้องการบันทึก
            
        Returns:
            True หากบันทึกสำเร็จ
        """
        if not self.is_initialized:
            raise FrameCaptureError("Camera not initialized")
            
        try:
            # สร้าง directory หากยังไม่มี
            Path(filename).parent.mkdir(parents=True, exist_ok=True)
            
            self.picam2.capture_file(filename)
            logger.info(f"Image saved to: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save image to {filename}: {e}")
            return False
    
    def start_video_stream(self, 
                          resolution: Tuple[int, int] = (640, 480),
                          framerate: int = 30) -> bool:
        """
        เริ่ม video streaming
        
        Args:
            resolution: ความละเอียดสำหรับ streaming
            framerate: อัตราเฟรม
            
        Returns:
            True หากเริ่ม streaming สำเร็จ
        """
        try:
            if not self.is_initialized:
                logger.info("Camera not initialized, initializing for video stream")
                self.initialize_camera()
                
            # หยุด current session ถ้ามี
            if self.is_initialized:
                self.picam2.stop()
            
            # ตั้งค่า video configuration
            video_config = self.picam2.create_video_configuration(
                main={"size": resolution, "format": "RGB888"},
                controls={"FrameRate": framerate}
            )
            
            self.picam2.configure(video_config)
            self.current_config = video_config
            self.picam2.start()
            
            logger.info(f"Video stream started: {resolution} @ {framerate}fps")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start video stream: {e}")
            return False
    
    def get_frame(self) -> np.ndarray:
        """
        ดึงเฟรมจาก video stream
        
        Returns:
            numpy array ของเฟรม (BGR format)
        """
        if not self.is_initialized:
            raise FrameCaptureError("Camera not initialized or not in video mode")
            
        try:
            frame = self.picam2.capture_array()
            
            # แปลงสีสำหรับ OpenCV
            if len(frame.shape) == 3 and frame.shape[2] == 3:
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            else:
                frame_bgr = frame
                
            return frame_bgr
            
        except Exception as e:
            logger.error(f"Failed to get frame: {e}")
            raise FrameCaptureError(f"Frame capture failed: {e}") from e
    
    def set_camera_controls(self, **controls) -> bool:
        """
        ตั้งค่า camera controls
        
        Args:
            **controls: camera control parameters
            
        Returns:
            True หากตั้งค่าสำเร็จ
            
        Example:
            set_camera_controls(
                ExposureTime=10000,  # microseconds
                AnalogueGain=2.0,
                Brightness=0.1
            )
        """
        if not self.is_initialized:
            logger.warning("Camera not initialized")
            return False
            
        try:
            self.picam2.set_controls(controls)
            logger.info(f"Camera controls set: {controls}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to set camera controls: {e}")
            return False
    
    def set_exposure_settings(self, 
                             exposure_time: Optional[int] = None,
                             iso: Optional[int] = None,
                             brightness: float = 0.0) -> bool:
        """
        ตั้งค่า exposure และ ISO
        
        Args:
            exposure_time: เวลา exposure ในไมโครวินาที
            iso: ค่า ISO (จะแปลงเป็น AnalogueGain)
            brightness: ค่าความสว่าง (-1.0 ถึง 1.0)
        """
        controls = {}
        
        if exposure_time is not None:
            controls["ExposureTime"] = exposure_time
            
        if iso is not None:
            # แปลง ISO เป็น AnalogueGain
            controls["AnalogueGain"] = iso / 100.0
            
        controls["Brightness"] = brightness
        
        return self.set_camera_controls(**controls)
    
    def set_white_balance(self, mode: str = "auto") -> bool:
        """
        ปรับ white balance
        
        Args:
            mode: โหมด white balance 
                  ("auto", "tungsten", "fluorescent", "indoor", "daylight", "cloudy")
        """
        wb_modes = {
            "auto": 0,
            "tungsten": 1,
            "fluorescent": 2,
            "indoor": 3,
            "daylight": 4,
            "cloudy": 5
        }
        
        if mode not in wb_modes:
            logger.error(f"Invalid white balance mode: {mode}")
            return False
            
        return self.set_camera_controls(AwbMode=wb_modes[mode])
    
    def set_focus(self, mode: str = "auto", distance: Optional[float] = None) -> bool:
        """
        ตั้งค่า focus (สำหรับกล้องที่รองรับ)
        
        Args:
            mode: โหมด focus ("auto", "manual")
            distance: ระยะ focus (0.0-1.0) สำหรับ manual mode
        """
        if mode == "auto":
            return self.set_camera_controls(AfMode=2)  # Continuous autofocus
        elif mode == "manual" and distance is not None:
            controls = {
                "AfMode": 0,  # Manual
                "LensPosition": distance
            }
            return self.set_camera_controls(**controls)
        else:
            logger.error("Invalid focus settings")
            return False
    
    def get_camera_properties(self) -> Dict[str, Any]:
        """
        ดึงข้อมูลคุณสมบัติของกล้อง
        
        Returns:
            Dictionary ของคุณสมบัติกล้อง
        """
        if not self.picam2:
            return {}
            
        try:
            properties = {
                "camera_properties": dict(self.picam2.camera_properties),
                "sensor_modes": self.picam2.sensor_modes,
                "current_config": self.current_config,
                "is_initialized": self.is_initialized
            }
            return properties
        except Exception as e:
            logger.error(f"Failed to get camera properties: {e}")
            return {}
    
    def optimize_for_performance(self) -> bool:
        """
        ปรับแต่งเพื่อประสิทธิภาพสูงสุด
        """
        try:
            # ลด noise processing
            controls = {
                "NoiseReductionMode": 0,  # Off
                "Sharpness": 1.0,
                "ScalerCrop": (0, 0, 1920, 1080)  # Full sensor
            }
            
            return self.set_camera_controls(**controls)
            
        except Exception as e:
            logger.error(f"Failed to optimize camera: {e}")
            return False
    
    def cleanup(self) -> None:
        """
        ทำความสะอาดทรัพยากร
        """
        try:
            if self.picam2 and self.is_initialized:
                self.picam2.stop()
                logger.info("Camera stopped and cleaned up")
                
            self.is_initialized = False
            self.picam2 = None
            self.current_config = None
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()
    
    def __del__(self):
        """Destructor"""
        self.cleanup()


class CameraHealthMonitor:
    """
    ติดตามสุขภาพของระบบกล้อง
    """
    
    def __init__(self):
        self.frame_count = 0
        self.error_count = 0
        self.start_time = time.time()
        self.last_fps_check = time.time()
        self.fps_window = []
        
    def log_frame_capture(self, success: bool = True) -> None:
        """
        บันทึกการจับภาพ
        
        Args:
            success: True หากจับภาพสำเร็จ
        """
        self.frame_count += 1
        
        if not success:
            self.error_count += 1
            
        # คำนวณ FPS
        current_time = time.time()
        self.fps_window.append(current_time)
        
        # เก็บข้อมูล FPS ในช่วง 5 วินาทีที่ผ่านมา
        self.fps_window = [t for t in self.fps_window if current_time - t <= 5.0]
    
    def get_stats(self) -> Dict[str, float]:
        """
        ดึงสถิติการทำงาน
        
        Returns:
            Dictionary ของสถิติ
        """
        runtime = time.time() - self.start_time
        current_fps = len(self.fps_window) / 5.0 if len(self.fps_window) > 0 else 0.0
        
        success_rate = 0.0
        if self.frame_count > 0:
            success_rate = (self.frame_count - self.error_count) / self.frame_count
            
        avg_fps = self.frame_count / runtime if runtime > 0 else 0.0
        
        return {
            "total_frames": self.frame_count,
            "errors": self.error_count,
            "success_rate": success_rate,
            "avg_fps": avg_fps,
            "current_fps": current_fps,
            "runtime_seconds": runtime
        }
    
    def reset_stats(self) -> None:
        """รีเซ็ตสถิติ"""
        self.frame_count = 0
        self.error_count = 0
        self.start_time = time.time()
        self.fps_window = []


# Utility functions
def detect_available_cameras() -> list:
    """
    ตรวจจับกล้องที่มีอยู่ในระบบ
    
    Returns:
        รายการของกล้องที่พบ
    """
    available_cameras = []
    
    if not PICAMERA2_AVAILABLE:
        logger.warning("picamera2 not available")
        return available_cameras
    
    try:
        # ลองสร้าง Picamera2 เพื่อดูว่ามีกล้องหรือไม่
        for i in range(3):  # ตรวจสอบกล้องสูงสุด 3 ตัว
            try:
                with Picamera2(i) as picam2:
                    camera_info = {
                        "index": i,
                        "properties": dict(picam2.camera_properties)
                    }
                    available_cameras.append(camera_info)
            except:
                break  # หยุดเมื่อไม่พบกล้อง
                
    except Exception as e:
        logger.error(f"Error detecting cameras: {e}")
    
    logger.info(f"Found {len(available_cameras)} camera(s)")
    return available_cameras


def capture_test_image(camera_manager: PiCameraManager, 
                      filename: str = "test_image.jpg") -> bool:
    """
    ทดสอบการจับภาพ
    
    Args:
        camera_manager: instance ของ PiCameraManager
        filename: ชื่อไฟล์ทดสอบ
        
    Returns:
        True หากทดสอบสำเร็จ
    """
    try:
        if not camera_manager.is_initialized:
            camera_manager.initialize_camera()
            
        image = camera_manager.capture_image()
        
        if image is not None and image.size > 0:
            cv2.imwrite(filename, image)
            logger.info(f"Test image saved: {filename}")
            return True
        else:
            logger.error("Captured image is empty")
            return False
            
    except Exception as e:
        logger.error(f"Camera test failed: {e}")
        return False