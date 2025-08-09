"""
PWD Vision Works - Hailo8 AI Processor
สำหรับจัดการ Hailo8 AI accelerator และการประมวลผล inference

Author: PWD Vision Works
Version: 1.0.0
"""

import time
import logging
import gc
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, Union
from contextlib import contextmanager
import numpy as np

try:
    import hailo_platform as hailo
    HAILO_AVAILABLE = True
except ImportError:
    HAILO_AVAILABLE = False
    logging.warning("Hailo platform not available. Please install HailoRT")

from ..utils.exceptions import HailoError, ModelLoadError, InferenceError
from ..image_processing.preprocessor import ImagePreprocessor
from ..image_processing.postprocessor import ImagePostprocessor

logger = logging.getLogger(__name__)


class HailoModelManager:
    """
    จัดการโมเดล Hailo และการโหลด
    """
    
    def __init__(self, model_dir: str = "models/"):
        """
        เริ่มต้น HailoModelManager
        
        Args:
            model_dir: ไดเรกทอรีที่เก็บโมเดล
        """
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(exist_ok=True, parents=True)
        self.loaded_models = {}
        
        logger.info(f"HailoModelManager initialized with model directory: {self.model_dir}")
    
    def list_available_models(self) -> List[str]:
        """
        แสดงรายการโมเดลที่มีอยู่
        
        Returns:
            รายการชื่อไฟล์โมเดล .hef
        """
        hef_files = list(self.model_dir.glob("*.hef"))
        model_names = [f.stem for f in hef_files]
        
        logger.info(f"Found {len(model_names)} model(s): {model_names}")
        return model_names
    
    def get_model_path(self, model_name: str) -> Path:
        """
        ดึงพาธของโมเดล
        
        Args:
            model_name: ชื่อโมเดล (ไม่ต้องมี .hef)
            
        Returns:
            พาธของไฟล์โมเดล
            
        Raises:
            FileNotFoundError: หากไม่พบโมเดล
        """
        if not model_name.endswith('.hef'):
            model_name = f"{model_name}.hef"
            
        model_path = self.model_dir / model_name
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")
            
        return model_path
    
    def validate_model(self, model_path: Path) -> Dict[str, Any]:
        """
        ตรวจสอบความถูกต้องของโมเดล
        
        Args:
            model_path: พาธของโมเดล
            
        Returns:
            ข้อมูลโมเดล
        """
        try:
            # ตรวจสอบไฟล์
            if not model_path.exists():
                raise FileNotFoundError(f"Model file not found: {model_path}")
            
            if model_path.stat().st_size == 0:
                raise ValueError(f"Model file is empty: {model_path}")
            
            # TODO: เพิ่มการตรวจสอบ metadata ของโมเดล Hailo
            model_info = {
                "path": str(model_path),
                "size_bytes": model_path.stat().st_size,
                "name": model_path.stem,
                "valid": True
            }
            
            logger.info(f"Model validated: {model_path.stem}")
            return model_info
            
        except Exception as e:
            logger.error(f"Model validation failed: {e}")
            raise ModelLoadError(f"Model validation failed: {e}") from e


class Hailo8Processor:
    """
    ประมวลผล AI ด้วย Hailo8 accelerator
    """
    
    def __init__(self, model_path: str, batch_size: int = 1):
        """
        เริ่มต้น Hailo8Processor
        
        Args:
            model_path: พาธของโมเดล .hef
            batch_size: ขนาด batch สำหรับการประมวลผล
        """
        if not HAILO_AVAILABLE:
            raise ImportError("Hailo platform not available")
            
        self.model_path = Path(model_path)
        self.batch_size = batch_size
        self.model = None
        self.network_group = None
        self.input_vstream_params = None
        self.output_vstream_params = None
        self.input_vstreams = None
        self.output_vstreams = None
        
        # Performance metrics
        self.inference_count = 0
        self.total_inference_time = 0.0
        self.error_count = 0
        
        # Preprocessor และ Postprocessor
        self.preprocessor = ImagePreprocessor()
        self.postprocessor = ImagePostprocessor()
        
        logger.info(f"Hailo8Processor initialized with model: {self.model_path}")
    
    def load_model(self) -> bool:
        """
        โหลดโมเดล Hailo
        
        Returns:
            True หากโหลดสำเร็จ
            
        Raises:
            ModelLoadError: หากไม่สามารถโหลดโมเดลได้
        """
        try:
            if not self.model_path.exists():
                raise FileNotFoundError(f"Model not found: {self.model_path}")
            
            logger.info(f"Loading Hailo model: {self.model_path}")
            
            # สร้าง VDevice
            params = hailo.VDevice.create_params()
            params.device_count = 1
            
            with hailo.VDevice(params) as device:
                # อ่านโมเดล HEF
                hef = hailo.HEF(str(self.model_path))
                
                # สร้าง network group
                configure_params = hailo.ConfigureParams.create_from_hef(hef, interface=hailo.Interface.PCIe)
                self.network_group = device.configure(hef, configure_params)[0]
                
                # ตั้งค่า input/output streams
                self.input_vstream_params = hailo.InputVStreamParams.make_from_network_group(
                    self.network_group, quantized=False, format_type=hailo.FormatType.FLOAT32)
                self.output_vstream_params = hailo.OutputVStreamParams.make_from_network_group(
                    self.network_group, quantized=False, format_type=hailo.FormatType.FLOAT32)
                
                logger.info("Hailo model loaded successfully")
                return True
                
        except Exception as e:
            logger.error(f"Failed to load Hailo model: {e}")
            raise ModelLoadError(f"Model load failed: {e}") from e
    
    def preprocess_image(self, image: np.ndarray, target_size: Tuple[int, int] = (640, 640)) -> np.ndarray:
        """
        เตรียมภาพสำหรับ inference
        
        Args:
            image: ภาพต้นฉบับ (BGR format)
            target_size: ขนาดเป้าหมาย (width, height)
            
        Returns:
            ภาพที่เตรียมแล้ว
        """
        try:
            # ใช้ preprocessor
            processed_image = self.preprocessor.resize_with_padding(image, target_size)
            processed_image = self.preprocessor.normalize(processed_image)
            
            # แปลงเป็น format ที่ Hailo ต้องการ
            if len(processed_image.shape) == 3:
                processed_image = np.expand_dims(processed_image, axis=0)  # Add batch dimension
            
            return processed_image.astype(np.float32)
            
        except Exception as e:
            logger.error(f"Preprocessing failed: {e}")
            raise InferenceError(f"Preprocessing failed: {e}") from e
    
    @contextmanager
    def inference_context(self):
        """
        Context manager สำหรับการจัดการหน่วยความจำระหว่าง inference
        """
        try:
            yield
        finally:
            # ทำความสะอาดหน่วยความจำ
            gc.collect()
    
    def predict(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        ทำการ inference บนภาพเดี่ยว
        
        Args:
            image: ภาพ input (BGR format)
            
        Returns:
            ผลการ inference
            
        Raises:
            InferenceError: หากการ inference ผิดพลาด
        """
        if self.network_group is None:
            raise InferenceError("Model not loaded")
        
        try:
            with self.inference_context():
                start_time = time.perf_counter()
                
                # Preprocessing
                processed_image = self.preprocess_image(image)
                
                # Create input/output streams
                with hailo.InputVStreams(self.network_group, self.input_vstream_params) as input_vstreams:
                    with hailo.OutputVStreams(self.network_group, self.output_vstream_params) as output_vstreams:
                        
                        # ส่งข้อมูลเข้า network
                        input_data = {input_vstreams[0].name: processed_image}
                        
                        # Run inference
                        output_data = self.network_group.wait_for_async_ready(input_data, timeout_ms=1000)
                        
                        # Post-processing
                        results = self.postprocess_output(output_data, image.shape[:2])
                        
                        # Update metrics
                        inference_time = time.perf_counter() - start_time
                        self.inference_count += 1
                        self.total_inference_time += inference_time
                        
                        logger.debug(f"Inference completed in {inference_time:.4f}s")
                        return results
                        
        except Exception as e:
            self.error_count += 1
            logger.error(f"Inference failed: {e}")
            raise InferenceError(f"Inference failed: {e}") from e
    
    def batch_predict(self, images: List[np.ndarray]) -> List[List[Dict[str, Any]]]:
        """
        ทำการ inference แบบ batch
        
        Args:
            images: รายการภาพ
            
        Returns:
            ผลการ inference สำหรับแต่ละภาพ
        """
        if not images:
            return []
        
        results = []
        batch_size = min(self.batch_size, len(images))
        
        try:
            for i in range(0, len(images), batch_size):
                batch = images[i:i+batch_size]
                
                # Process batch
                batch_results = []
                for image in batch:
                    result = self.predict(image)
                    batch_results.append(result)
                
                results.extend(batch_results)
                
                # Yield control occasionally
                if i % (batch_size * 4) == 0:
                    time.sleep(0.001)  # Prevent CPU hogging
            
            return results
            
        except Exception as e:
            logger.error(f"Batch inference failed: {e}")
            raise InferenceError(f"Batch inference failed: {e}") from e
    
    def postprocess_output(self, output_data: Dict, original_shape: Tuple[int, int]) -> List[Dict[str, Any]]:
        """
        ประมวลผลข้อมูลที่ได้จาก inference
        
        Args:
            output_data: ข้อมูลจาก network output
            original_shape: ขนาดภาพต้นฉบับ (height, width)
            
        Returns:
            ผลการตรวจจับที่ประมวลผลแล้ว
        """
        try:
            # ใช้ postprocessor สำหรับการประมวลผล
            # TODO: ปรับแต่งตามประเภทโมเดล (YOLO, SSD, etc.)
            
            results = []
            
            for output_name, output_tensor in output_data.items():
                # ตัวอย่างการประมวลผลสำหรับ object detection
                if output_tensor.ndim >= 2:
                    # Process detections
                    detections = self.postprocessor.process_detections(
                        output_tensor, 
                        original_shape,
                        confidence_threshold=0.5,
                        nms_threshold=0.4
                    )
                    results.extend(detections)
            
            return results
            
        except Exception as e:
            logger.error(f"Post-processing failed: {e}")
            return []
    
    def get_performance_stats(self) -> Dict[str, float]:
        """
        ดึงสถิติประสิทธิภาพ
        
        Returns:
            สถิติการทำงาน
        """
        if self.inference_count == 0:
            return {
                "total_inferences": 0,
                "avg_inference_time": 0.0,
                "fps": 0.0,
                "error_rate": 0.0
            }
        
        avg_time = self.total_inference_time / self.inference_count
        fps = 1.0 / avg_time if avg_time > 0 else 0.0
        error_rate = self.error_count / self.inference_count
        
        return {
            "total_inferences": self.inference_count,
            "avg_inference_time": avg_time,
            "fps": fps,
            "error_rate": error_rate,
            "total_errors": self.error_count
        }
    
    def reset_stats(self) -> None:
        """รีเซ็ตสถิติประสิทธิภาพ"""
        self.inference_count = 0
        self.total_inference_time = 0.0
        self.error_count = 0
        logger.info("Performance stats reset")
    
    def cleanup(self) -> None:
        """
        ทำความสะอาดทรัพยากร
        """
        try:
            if self.input_vstreams:
                self.input_vstreams = None
            if self.output_vstreams:
                self.output_vstreams = None
            if self.network_group:
                self.network_group = None
            
            # Force garbage collection
            gc.collect()
            
            logger.info("Hailo8Processor cleaned up")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        self.load_model()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()


class HailoHealthMonitor:
    """
    ติดตามสุขภาพของ Hailo processor
    """
    
    def __init__(self):
        self.inference_count = 0
        self.error_count = 0
        self.start_time = time.time()
        self.last_check_time = time.time()
        
        # Temperature และ performance tracking
        self.temperature_readings = []
        self.memory_usage_readings = []
    
    def log_inference(self, success: bool = True, inference_time: float = 0.0) -> None:
        """
        บันทึกการ inference
        
        Args:
            success: True หากสำเร็จ
            inference_time: เวลาที่ใช้ในการ inference
        """
        self.inference_count += 1
        if not success:
            self.error_count += 1
            
        # Log performance metrics
        if inference_time > 0:
            # สามารถเพิ่มการติดตาม latency distribution
            pass
    
    def get_stats(self) -> Dict[str, Any]:
        """
        ดึงสถิติสุขภาพระบบ
        
        Returns:
            Dictionary ของสถิติ
        """
        runtime = time.time() - self.start_time
        success_rate = 0.0
        
        if self.inference_count > 0:
            success_rate = (self.inference_count - self.error_count) / self.inference_count
        
        fps = self.inference_count / runtime if runtime > 0 else 0.0
        
        return {
            "total_inferences": self.inference_count,
            "errors": self.error_count,
            "success_rate": success_rate,
            "avg_fps": fps,
            "runtime_seconds": runtime,
            "last_check": self.last_check_time
        }
    
    def check_system_health(self) -> Dict[str, Any]:
        """
        ตรวจสอบสุขภาพระบบ Hailo
        
        Returns:
            ข้อมูลสุขภาพระบบ
        """
        try:
            # TODO: เพิ่มการตรวจสอบ temperature, memory usage, etc.
            health_info = {
                "timestamp": time.time(),
                "status": "healthy",
                "temperature": None,  # จะได้จาก Hailo API
                "memory_usage": None,
                "device_available": HAILO_AVAILABLE
            }
            
            self.last_check_time = time.time()
            return health_info
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "timestamp": time.time(),
                "status": "error",
                "error": str(e)
            }


# Utility functions
def benchmark_inference(processor: Hailo8Processor, 
                       test_images: List[np.ndarray],
                       iterations: int = 100) -> Dict[str, float]:
    """
    วัดประสิทธิภาพการ inference
    
    Args:
        processor: Hailo8Processor instance
        test_images: ภาพทดสอบ
        iterations: จำนวนครั้งในการทดสอบ
        
    Returns:
        ผลการทดสอบประสิทธิภาพ
    """
    if not test_images:
        raise ValueError("No test images provided")
    
    logger.info(f"Starting benchmark with {iterations} iterations")
    
    times = []
    errors = 0
    
    for i in range(iterations):
        image = test_images[i % len(test_images)]
        
        try:
            start_time = time.perf_counter()
            result = processor.predict(image)
            end_time = time.perf_counter()
            
            times.append(end_time - start_time)
            
        except Exception as e:
            errors += 1
            logger.error(f"Benchmark iteration {i} failed: {e}")
    
    if not times:
        return {"error": "All iterations failed"}
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    results = {
        "iterations": iterations,
        "successful": len(times),
        "failed": errors,
        "avg_time_ms": avg_time * 1000,
        "min_time_ms": min_time * 1000,
        "max_time_ms": max_time * 1000,
        "fps": 1.0 / avg_time if avg_time > 0 else 0.0,
        "error_rate": errors / iterations
    }
    
    logger.info(f"Benchmark completed: {results}")
    return results


def detect_hailo_devices() -> List[Dict[str, Any]]:
    """
    ตรวจจับอุปกรณ์ Hailo ที่มีอยู่
    
    Returns:
        รายการอุปกรณ์ Hailo
    """
    devices = []
    
    if not HAILO_AVAILABLE:
        logger.warning("Hailo platform not available")
        return devices
    
    try:
        # ตรวจสอบอุปกรณ์ Hailo ที่เชื่อมต่อ
        device_infos = hailo.Device.scan()
        
        for i, device_info in enumerate(device_infos):
            device_data = {
                "index": i,
                "device_id": device_info.device_id if hasattr(device_info, 'device_id') else f"device_{i}",
                "status": "available"
            }
            devices.append(device_data)
        
        logger.info(f"Found {len(devices)} Hailo device(s)")
        
    except Exception as e:
        logger.error(f"Error detecting Hailo devices: {e}")
    
    return devices