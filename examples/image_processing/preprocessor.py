"""
PWD Vision Works - Image Preprocessor
สำหรับเตรียมภาพสำหรับ AI model inference

Author: PWD Vision Works
Version: 1.0.0
"""

import cv2
import numpy as np
import logging
from typing import Tuple, Optional, Union, List
from pathlib import Path

from ..utils.exceptions import PreprocessingError, InvalidImageFormatError, ImageResizeError

logger = logging.getLogger(__name__)


class ImagePreprocessor:
    """
    Class สำหรับการ preprocess ภาพก่อนส่งเข้า AI model
    """
    
    def __init__(self, target_size: Tuple[int, int] = (640, 640)):
        """
        เริ่มต้น ImagePreprocessor
        
        Args:
            target_size: ขนาดเป้าหมาย (width, height)
        """
        self.target_size = target_size
        self.mean = np.array([0.485, 0.456, 0.406])  # ImageNet mean
        self.std = np.array([0.229, 0.224, 0.225])   # ImageNet std
        
        logger.info(f"ImagePreprocessor initialized with target size: {target_size}")
    
    def validate_image(self, image: np.ndarray) -> bool:
        """
        ตรวจสอบความถูกต้องของภาพ
        
        Args:
            image: ภาพ input
            
        Returns:
            True หากภาพถูกต้อง
            
        Raises:
            InvalidImageFormatError: หากภาพไม่ถูกต้อง
        """
        try:
            if image is None:
                raise InvalidImageFormatError("Image is None")
            
            if not isinstance(image, np.ndarray):
                raise InvalidImageFormatError("Image must be numpy array")
            
            if image.size == 0:
                raise InvalidImageFormatError("Image is empty")
            
            if len(image.shape) < 2:
                raise InvalidImageFormatError("Image must have at least 2 dimensions")
            
            if len(image.shape) == 3 and image.shape[2] not in [1, 3, 4]:
                raise InvalidImageFormatError(f"Invalid number of channels: {image.shape[2]}")
            
            # ตรวจสอบขนาดภาพ
            if image.shape[0] < 10 or image.shape[1] < 10:
                raise InvalidImageFormatError("Image too small (minimum 10x10)")
            
            return True
            
        except Exception as e:
            logger.error(f"Image validation failed: {e}")
            raise
    
    def resize_with_padding(self, 
                           image: np.ndarray, 
                           target_size: Optional[Tuple[int, int]] = None,
                           maintain_aspect_ratio: bool = True,
                           padding_color: Tuple[int, int, int] = (114, 114, 114)) -> np.ndarray:
        """
        ปรับขนาดภาพพร้อม padding เพื่อรักษา aspect ratio
        
        Args:
            image: ภาพ input (BGR format)
            target_size: ขนาดเป้าหมาย (width, height)
            maintain_aspect_ratio: รักษา aspect ratio หรือไม่
            padding_color: สีสำหรับ padding (B, G, R)
            
        Returns:
            ภาพที่ปรับขนาดแล้ว
            
        Raises:
            ImageResizeError: หากไม่สามารถปรับขนาดได้
        """
        try:
            self.validate_image(image)
            
            target_size = target_size or self.target_size
            target_width, target_height = target_size
            
            if not maintain_aspect_ratio:
                # Resize โดยไม่รักษา aspect ratio
                resized = cv2.resize(image, (target_width, target_height))
                return resized
            
            # คำนวณ scale factor เพื่อรักษา aspect ratio
            h, w = image.shape[:2]
            scale = min(target_width / w, target_height / h)
            
            # ขนาดใหม่หลังจาก scale
            new_w = int(w * scale)
            new_h = int(h * scale)
            
            # Resize ภาพ
            resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
            
            # สร้างภาพใหม่ด้วยขนาดเป้าหมาย
            if len(image.shape) == 3:
                padded = np.full((target_height, target_width, image.shape[2]), 
                               padding_color[:image.shape[2]], dtype=image.dtype)
            else:
                padded = np.full((target_height, target_width), 
                               padding_color[0], dtype=image.dtype)
            
            # วาง resized image ตรงกลาง
            y_offset = (target_height - new_h) // 2
            x_offset = (target_width - new_w) // 2
            
            if len(image.shape) == 3:
                padded[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
            else:
                padded[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
            
            logger.debug(f"Image resized from {image.shape} to {padded.shape}")
            return padded
            
        except Exception as e:
            logger.error(f"Image resize failed: {e}")
            raise ImageResizeError(f"Failed to resize image: {e}") from e
    
    def normalize(self, 
                  image: np.ndarray, 
                  method: str = "imagenet",
                  custom_mean: Optional[np.ndarray] = None,
                  custom_std: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Normalize ภาพ
        
        Args:
            image: ภาพ input (BGR format)
            method: วิธี normalize ("imagenet", "zero_one", "neg_one_one", "custom")
            custom_mean: ค่า mean สำหรับ custom normalization
            custom_std: ค่า std สำหรับ custom normalization
            
        Returns:
            ภาพที่ normalize แล้ว
        """
        try:
            self.validate_image(image)
            
            # แปลงเป็น float32
            normalized = image.astype(np.float32)
            
            if method == "zero_one":
                # Normalize เป็น 0-1
                normalized = normalized / 255.0
                
            elif method == "neg_one_one":
                # Normalize เป็น -1 ถึง 1
                normalized = (normalized / 255.0 - 0.5) * 2.0
                
            elif method == "imagenet":
                # Normalize ด้วย ImageNet statistics
                normalized = normalized / 255.0
                
                # แปลงจาก BGR เป็น RGB สำหรับ ImageNet
                if len(normalized.shape) == 3 and normalized.shape[2] == 3:
                    normalized = cv2.cvtColor(normalized, cv2.COLOR_BGR2RGB)
                    
                    # Apply mean และ std
                    normalized = (normalized - self.mean) / self.std
                    
            elif method == "custom":
                if custom_mean is None or custom_std is None:
                    raise ValueError("custom_mean and custom_std must be provided for custom normalization")
                
                normalized = normalized / 255.0
                normalized = (normalized - custom_mean) / custom_std
                
            else:
                raise ValueError(f"Unknown normalization method: {method}")
            
            logger.debug(f"Image normalized using method: {method}")
            return normalized
            
        except Exception as e:
            logger.error(f"Normalization failed: {e}")
            raise PreprocessingError(f"Failed to normalize image: {e}") from e
    
    def convert_color_space(self, 
                           image: np.ndarray, 
                           source: str = "BGR",
                           target: str = "RGB") -> np.ndarray:
        """
        แปลง color space
        
        Args:
            image: ภาพ input
            source: color space ต้นทาง
            target: color space เป้าหมาย
            
        Returns:
            ภาพที่แปลง color space แล้ว
        """
        try:
            self.validate_image(image)
            
            if len(image.shape) != 3 or image.shape[2] != 3:
                logger.warning("Color conversion requires 3-channel image")
                return image
            
            conversion_map = {
                ("BGR", "RGB"): cv2.COLOR_BGR2RGB,
                ("RGB", "BGR"): cv2.COLOR_RGB2BGR,
                ("BGR", "GRAY"): cv2.COLOR_BGR2GRAY,
                ("RGB", "GRAY"): cv2.COLOR_RGB2GRAY,
                ("GRAY", "BGR"): cv2.COLOR_GRAY2BGR,
                ("GRAY", "RGB"): cv2.COLOR_GRAY2RGB,
                ("BGR", "HSV"): cv2.COLOR_BGR2HSV,
                ("RGB", "HSV"): cv2.COLOR_RGB2HSV,
                ("HSV", "BGR"): cv2.COLOR_HSV2BGR,
                ("HSV", "RGB"): cv2.COLOR_HSV2RGB
            }
            
            if (source, target) in conversion_map:
                converted = cv2.cvtColor(image, conversion_map[(source, target)])
                logger.debug(f"Color space converted from {source} to {target}")
                return converted
            elif source == target:
                return image.copy()
            else:
                raise ValueError(f"Unsupported color conversion: {source} to {target}")
                
        except Exception as e:
            logger.error(f"Color conversion failed: {e}")
            raise PreprocessingError(f"Failed to convert color space: {e}") from e
    
    def apply_gaussian_blur(self, 
                           image: np.ndarray, 
                           kernel_size: int = 5,
                           sigma: float = 1.0) -> np.ndarray:
        """
        ใช้ Gaussian blur
        
        Args:
            image: ภาพ input
            kernel_size: ขนาด kernel (ต้องเป็นเลขคี่)
            sigma: ค่า sigma สำหรับ Gaussian
            
        Returns:
            ภาพที่ blur แล้ว
        """
        try:
            self.validate_image(image)
            
            # ตรวจสอบ kernel size
            if kernel_size % 2 == 0:
                kernel_size += 1
                logger.warning(f"Kernel size adjusted to {kernel_size} (must be odd)")
            
            blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
            logger.debug(f"Gaussian blur applied: kernel={kernel_size}, sigma={sigma}")
            return blurred
            
        except Exception as e:
            logger.error(f"Gaussian blur failed: {e}")
            raise PreprocessingError(f"Failed to apply Gaussian blur: {e}") from e
    
    def enhance_contrast(self, 
                        image: np.ndarray, 
                        method: str = "clahe",
                        alpha: float = 1.5,
                        beta: int = 0) -> np.ndarray:
        """
        เพิ่ม contrast ของภาพ
        
        Args:
            image: ภาพ input
            method: วิธี enhance ("clahe", "linear")
            alpha: ค่า contrast สำหรับ linear method
            beta: ค่า brightness สำหรับ linear method
            
        Returns:
            ภาพที่ enhance contrast แล้ว
        """
        try:
            self.validate_image(image)
            
            if method == "clahe":
                # ใช้ CLAHE (Contrast Limited Adaptive Histogram Equalization)
                if len(image.shape) == 3:
                    # แปลงเป็น LAB color space
                    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
                    l_channel = lab[:, :, 0]
                    
                    # ใช้ CLAHE กับ L channel
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    enhanced_l = clahe.apply(l_channel)
                    
                    # รวม channels กลับ
                    lab[:, :, 0] = enhanced_l
                    enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
                else:
                    # Grayscale image
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    enhanced = clahe.apply(image)
                    
            elif method == "linear":
                # Linear contrast enhancement
                enhanced = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
                
            else:
                raise ValueError(f"Unknown contrast enhancement method: {method}")
            
            logger.debug(f"Contrast enhanced using method: {method}")
            return enhanced
            
        except Exception as e:
            logger.error(f"Contrast enhancement failed: {e}")
            raise PreprocessingError(f"Failed to enhance contrast: {e}") from e
    
    def apply_noise_reduction(self, 
                             image: np.ndarray, 
                             method: str = "bilateral") -> np.ndarray:
        """
        ลด noise ในภาพ
        
        Args:
            image: ภาพ input
            method: วิธี noise reduction ("bilateral", "gaussian", "median")
            
        Returns:
            ภาพที่ลด noise แล้ว
        """
        try:
            self.validate_image(image)
            
            if method == "bilateral":
                # Bilateral filter - ลด noise โดยรักษา edges
                filtered = cv2.bilateralFilter(image, 9, 75, 75)
                
            elif method == "gaussian":
                # Gaussian filter
                filtered = cv2.GaussianBlur(image, (5, 5), 1.0)
                
            elif method == "median":
                # Median filter
                filtered = cv2.medianBlur(image, 5)
                
            else:
                raise ValueError(f"Unknown noise reduction method: {method}")
            
            logger.debug(f"Noise reduction applied using method: {method}")
            return filtered
            
        except Exception as e:
            logger.error(f"Noise reduction failed: {e}")
            raise PreprocessingError(f"Failed to reduce noise: {e}") from e
    
    def preprocess_batch(self, 
                        images: List[np.ndarray],
                        target_size: Optional[Tuple[int, int]] = None,
                        normalize_method: str = "imagenet") -> np.ndarray:
        """
        ประมวลผล batch ของภาพ
        
        Args:
            images: รายการภาพ
            target_size: ขนาดเป้าหมาย
            normalize_method: วิธี normalize
            
        Returns:
            numpy array ของภาพที่ประมวลผลแล้ว
        """
        try:
            if not images:
                raise ValueError("No images provided")
            
            target_size = target_size or self.target_size
            processed_images = []
            
            for i, image in enumerate(images):
                try:
                    # Resize with padding
                    resized = self.resize_with_padding(image, target_size)
                    
                    # Normalize
                    normalized = self.normalize(resized, method=normalize_method)
                    
                    processed_images.append(normalized)
                    
                except Exception as e:
                    logger.warning(f"Failed to process image {i}: {e}")
                    continue
            
            if not processed_images:
                raise PreprocessingError("No images were successfully processed")
            
            # Stack เป็น batch
            batch = np.stack(processed_images, axis=0)
            logger.info(f"Processed batch of {len(processed_images)} images: {batch.shape}")
            
            return batch
            
        except Exception as e:
            logger.error(f"Batch preprocessing failed: {e}")
            raise PreprocessingError(f"Failed to preprocess batch: {e}") from e
    
    def preprocess_for_model(self, 
                            image: np.ndarray,
                            model_type: str = "yolo") -> np.ndarray:
        """
        เตรียมภาพสำหรับ model เฉพาะ
        
        Args:
            image: ภาพ input
            model_type: ประเภท model ("yolo", "ssd", "resnet", "efficientnet")
            
        Returns:
            ภาพที่เตรียมสำหรับ model
        """
        try:
            if model_type.lower() == "yolo":
                # YOLO preprocessing
                resized = self.resize_with_padding(image, self.target_size)
                normalized = self.normalize(resized, method="zero_one")
                
                # YOLO expects RGB format
                if len(normalized.shape) == 3 and normalized.shape[2] == 3:
                    normalized = cv2.cvtColor(normalized, cv2.COLOR_BGR2RGB)
                
                # Add batch dimension
                processed = np.expand_dims(normalized, axis=0)
                
            elif model_type.lower() == "ssd":
                # SSD preprocessing
                resized = self.resize_with_padding(image, self.target_size, maintain_aspect_ratio=False)
                normalized = self.normalize(resized, method="zero_one")
                processed = np.expand_dims(normalized, axis=0)
                
            elif model_type.lower() in ["resnet", "efficientnet"]:
                # ImageNet-based models
                resized = self.resize_with_padding(image, self.target_size, maintain_aspect_ratio=False)
                normalized = self.normalize(resized, method="imagenet")
                processed = np.expand_dims(normalized, axis=0)
                
            else:
                # Default preprocessing
                resized = self.resize_with_padding(image, self.target_size)
                normalized = self.normalize(resized, method="zero_one")
                processed = np.expand_dims(normalized, axis=0)
            
            logger.debug(f"Image preprocessed for {model_type} model: {processed.shape}")
            return processed
            
        except Exception as e:
            logger.error(f"Model-specific preprocessing failed: {e}")
            raise PreprocessingError(f"Failed to preprocess for {model_type}: {e}") from e
    
    def get_preprocessing_info(self) -> dict:
        """
        ดึงข้อมูลการตั้งค่าปัจจุบัน
        
        Returns:
            Dictionary ของการตั้งค่า
        """
        return {
            "target_size": self.target_size,
            "imagenet_mean": self.mean.tolist(),
            "imagenet_std": self.std.tolist(),
            "version": "1.0.0"
        }
