# preprocessing.py
import cv2
import numpy as np
from PIL import Image

def resize_image(image:np.ndarray, size: tuple) ->np.ndarray:
    """
    
    """
    return cv2.resize(image, size,interpolation=cv2.INTER_AREA)

def read_image(path):
    """อ่านภาพจาก path ที่กำหนด"""
    return cv2.imread(path)

def resize_image(image, width, height):
    """ปรับขนาดภาพ"""
    return cv2.resize(image, (width, height))

def convert_to_gray(image):
    """แปลงภาพเป็นขาวดำ"""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def blur_image(image, kernel_size=5):
    """เบลอภาพด้วย Gaussian Blur"""
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def normalize_image(image):
    """ทำ normalization ให้ภาพในช่วง 0-1"""
    return image / 255.0

def sharpen_image(image):
    """เพิ่มความคมชัดให้ภาพ"""
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    return cv2.filter2D(src=image, ddepth=-1, kernel=kernel)

def remove_noise(image):
    """ลบ noise ด้วย median filter"""
    return cv2.medianBlur(image, 3)
