"""
PWD Vision Works - Custom Exceptions
กำหนด exception classes สำหรับการจัดการ errors ในระบบ

Author: PWD Vision Works
Version: 1.0.0
"""


class PWDVisionError(Exception):
    """
    Base exception class สำหรับ PWD Vision Works
    Exception อื่น ๆ ทั้งหมดจะ inherit จาก class นี้
    """
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(message)


# Camera related exceptions
class CameraError(PWDVisionError):
    """Base exception สำหรับ camera operations"""
    pass


class CameraInitializationError(CameraError):
    """Exception สำหรับการเริ่มต้นกล้องผิดพลาด"""
    def __init__(self, message: str):
        super().__init__(f"Camera initialization failed: {message}", "CAM_INIT_001")


class FrameCaptureError(CameraError):
    """Exception สำหรับการจับภาพผิดพลาด"""
    def __init__(self, message: str):
        super().__init__(f"Frame capture failed: {message}", "CAM_CAPTURE_001")


class CameraConfigurationError(CameraError):
    """Exception สำหรับการตั้งค่ากล้องผิดพลาด"""
    def __init__(self, message: str):
        super().__init__(f"Camera configuration failed: {message}", "CAM_CONFIG_001")


# Hailo AI related exceptions  
class HailoError(PWDVisionError):
    """Base exception สำหรับ Hailo operations"""
    pass


class ModelLoadError(HailoError):
    """Exception สำหรับการโหลดโมเดลผิดพลาด"""
    def __init__(self, message: str):
        super().__init__(f"Model load failed: {message}", "HAILO_MODEL_001")


class InferenceError(HailoError):
    """Exception สำหรับการ inference ผิดพลาด"""
    def __init__(self, message: str):
        super().__init__(f"Inference failed: {message}", "HAILO_INFER_001")


class ModelValidationError(HailoError):
    """Exception สำหรับการ validate โมเดลผิดพลาด"""
    def __init__(self, message: str):
        super().__init__(f"Model validation failed: {message}", "HAILO_VALID_001")


# Image processing related exceptions
class ImageProcessingError(PWDVisionError):
    """Base exception สำหรับ image processing operations"""
    pass


class PreprocessingError(ImageProcessingError):
    """Exception สำหรับ preprocessing ผิดพลาด"""
    def __init__(self, message: str):
        super().__init__(f"Preprocessing failed: {message}", "IMG_PREPROC_001")


class PostprocessingError(ImageProcessingError):
    """Exception สำหรับ postprocessing ผิดพลาด"""
    def __init__(self, message: str):
        super().__init__(f"Postprocessing failed: {message}", "IMG_POSTPROC_001")


class InvalidImageFormatError(ImageProcessingError):
    """Exception สำหรับรูปแบบภาพไม่ถูกต้อง"""
    def __init__(self, message: str):
        super().__init__(f"Invalid image format: {message}", "IMG_FORMAT_001")


class ImageResizeError(ImageProcessingError):
    """Exception สำหรับการปรับขนาดภาพผิดพลาด"""
    def __init__(self, message: str):
        super().__init__(f"Image resize failed: {message}", "IMG_RESIZE_001")


# Network and API related exceptions
class NetworkError(PWDVisionError):
    """Base exception สำหรับ network operations"""
    pass


class APIConnectionError(NetworkError):
    """Exception สำหรับการเชื่อมต่อ API ผิดพลาด"""
    def __init__(self, message: str):
        super().__init__(f"API connection failed: {message}", "NET_API_001")


class DataTransmissionError(NetworkError):
    """Exception สำหรับการส่งข้อมูลผิดพลาด"""
    def __init__(self, message: str):
        super().__init__(f"Data transmission failed: {message}", "NET_TRANS_001")


# Configuration related exceptions
class ConfigurationError(PWDVisionError):
    """Base exception สำหรับ configuration operations"""
    pass


class InvalidConfigError(ConfigurationError):
    """Exception สำหรับการตั้งค่าไม่ถูกต้อง"""
    def __init__(self, message: str):
        super().__init__(f"Invalid configuration: {message}", "CONFIG_001")


class MissingConfigError(ConfigurationError):
    """Exception สำหรับการตั้งค่าที่ขาดหายไป"""
    def __init__(self, message: str):
        super().__init__(f"Missing configuration: {message}", "CONFIG_002")


# Storage related exceptions
class StorageError(PWDVisionError):
    """Base exception สำหรับ storage operations"""
    pass


class FileNotFoundError(StorageError):
    """Exception สำหรับไฟล์ไม่พบ"""
    def __init__(self, message: str):
        super().__init__(f"File not found: {message}", "STORAGE_001")


class DiskSpaceError(StorageError):
    """Exception สำหรับพื้นที่ดิสก์ไม่เพียงพอ"""
    def __init__(self, message: str):
        super().__init__(f"Insufficient disk space: {message}", "STORAGE_002")


class FilePermissionError(StorageError):
    """Exception สำหรับสิทธิ์การเข้าถึงไฟล์"""
    def __init__(self, message: str):
        super().__init__(f"File permission error: {message}", "STORAGE_003")


# System resource related exceptions
class ResourceError(PWDVisionError):
    """Base exception สำหรับ system resource operations"""
    pass


class MemoryError(ResourceError):
    """Exception สำหรับหน่วยความจำไม่เพียงพอ"""
    def __init__(self, message: str):
        super().__init__(f"Memory error: {message}", "RESOURCE_MEM_001")


class CPUOverloadError(ResourceError):
    """Exception สำหรับ CPU overload"""
    def __init__(self, message: str):
        super().__init__(f"CPU overload: {message}", "RESOURCE_CPU_001")


class GPUError(ResourceError):
    """Exception สำหรับ GPU operations"""
    def __init__(self, message: str):
        super().__init__(f"GPU error: {message}", "RESOURCE_GPU_001")


# Detection and analysis related exceptions
class DetectionError(PWDVisionError):
    """Base exception สำหรับ detection operations"""
    pass


class NoObjectDetectedError(DetectionError):
    """Exception สำหรับไม่พบ object ที่ต้องการ"""
    def __init__(self, message: str = "No objects detected"):
        super().__init__(message, "DETECT_NONE_001")


class InvalidDetectionError(DetectionError):
    """Exception สำหรับผลการ detection ไม่ถูกต้อง"""
    def __init__(self, message: str):
        super().__init__(f"Invalid detection result: {message}", "DETECT_INVALID_001")


class ConfidenceThresholdError(DetectionError):
    """Exception สำหรับ confidence threshold ไม่ผ่าน"""
    def __init__(self, message: str):
        super().__init__(f"Confidence threshold not met: {message}", "DETECT_CONF_001")


# Utility functions for exception handling
def log_exception(exception: Exception, logger=None, include_traceback: bool = True):
    """
    บันทึก exception ด้วย logger
    
    Args:
        exception: Exception ที่เกิดขึ้น
        logger: Logger instance (ถ้าไม่ระบุจะใช้ default)
        include_traceback: รวม traceback หรือไม่
    """
    import logging
    import traceback
    
    if logger is None:
        logger = logging.getLogger(__name__)
    
    error_msg = f"Exception occurred: {type(exception).__name__}: {str(exception)}"
    
    if isinstance(exception, PWDVisionError) and exception.error_code:
        error_msg += f" (Error Code: {exception.error_code})"
    
    if include_traceback:
        error_msg += f"\nTraceback:\n{traceback.format_exc()}"
    
    logger.error(error_msg)


def handle_exception(exception: Exception, 
                    default_return=None,
                    raise_on_critical: bool = True,
                    logger=None):
    """
    จัดการ exception ตามประเภท
    
    Args:
        exception: Exception ที่เกิดขึ้น
        default_return: ค่า default ที่จะ return
        raise_on_critical: raise exception อีกครั้งหากเป็น critical error
        logger: Logger instance
        
    Returns:
        default_return หรือ raise exception ใหม่
    """
    log_exception(exception, logger)
    
    # Critical errors ที่ต้อง raise ใหม่
    critical_errors = (
        CameraInitializationError,
        ModelLoadError,
        MemoryError,
        CPUOverloadError,
        DiskSpaceError
    )
    
    if raise_on_critical and isinstance(exception, critical_errors):
        raise exception
    
    return default_return


class ExceptionContext:
    """
    Context manager สำหรับจัดการ exception
    """
    
    def __init__(self, 
                 operation_name: str,
                 logger=None,
                 default_return=None,
                 raise_on_error: bool = True):
        self.operation_name = operation_name
        self.logger = logger or logging.getLogger(__name__)
        self.default_return = default_return
        self.raise_on_error = raise_on_error
    
    def __enter__(self):
        self.logger.debug(f"Starting operation: {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.logger.error(f"Operation '{self.operation_name}' failed: {exc_val}")
            
            if not self.raise_on_error:
                return True  # Suppress exception
        else:
            self.logger.debug(f"Operation completed successfully: {self.operation_name}")
        
        return False  # Don't suppress exception


# Error code mappings for easy lookup
ERROR_CODES = {
    "CAM_INIT_001": "Camera initialization failed",
    "CAM_CAPTURE_001": "Frame capture failed", 
    "CAM_CONFIG_001": "Camera configuration failed",
    "HAILO_MODEL_001": "Model load failed",
    "HAILO_INFER_001": "Inference failed",
    "HAILO_VALID_001": "Model validation failed",
    "IMG_PREPROC_001": "Preprocessing failed",
    "IMG_POSTPROC_001": "Postprocessing failed",
    "IMG_FORMAT_001": "Invalid image format",
    "IMG_RESIZE_001": "Image resize failed",
    "NET_API_001": "API connection failed",
    "NET_TRANS_001": "Data transmission failed",
    "CONFIG_001": "Invalid configuration",
    "CONFIG_002": "Missing configuration",
    "STORAGE_001": "File not found",
    "STORAGE_002": "Insufficient disk space",
    "STORAGE_003": "File permission error",
    "RESOURCE_MEM_001": "Memory error",
    "RESOURCE_CPU_001": "CPU overload",
    "RESOURCE_GPU_001": "GPU error",
    "DETECT_NONE_001": "No objects detected",
    "DETECT_INVALID_001": "Invalid detection result",
    "DETECT_CONF_001": "Confidence threshold not met"
}


def get_error_description(error_code: str) -> str:
    """
    ดึงคำอธิบาย error จาก error code
    
    Args:
        error_code: รหัส error
        
    Returns:
        คำอธิบาย error
    """
    return ERROR_CODES.get(error_code, "Unknown error")