# postprocessing.py

import cv2
import numpy as np
from PIL import Image

def threshold_image(image, threshold=127):
    """แปลงภาพเป็น binary ด้วย threshold"""
    _, binary = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    return binary

def draw_contours(image):
    """วาดเส้นขอบของวัตถุในภาพ"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 2)

def save_image(image, path):
    """บันทึกภาพเป็นไฟล์"""
    cv2.imwrite(path, image)

def convert_to_pil(image):
    """แปลงจาก OpenCV เป็น PIL"""
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

def overlay_text(image, text, position=(10,30)):
    """ใส่ข้อความลงบนภาพ"""
    return cv2.putText(image.copy(), text, position,
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

def morphological_ops(image, operation='dilate', kernel_size=3):
    """ประมวลผลภาพแบบ morph เช่น dilate, erode"""
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    if operation == 'dilate':
        return cv2.dilate(image, kernel, iterations=1)
    elif operation == 'erode':
        return cv2.erode(image, kernel, iterations=1)
    else:
        raise ValueError("operation must be 'dilate' or 'erode'")
