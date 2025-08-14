import io
import time
import random
import socketio
from datetime import datetime
from PIL import Image
from picamera2 import Picamera2
import numpy as np
import cv2
import utils_variable
sio = socketio.Client()
import requests
import socket

# กำหนดค่าเริ่มต้น ########################################
# เซิร์ฟเวอร์ที่ใช้ทดสอบ
#SERVER_URL = "http://localhost:port/"
SERVER_URL = "http://lprserver.tail605477.ts.net:1337/"

# ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต และ IP Address
try:
    # ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("lprserver.tail605477.ts.net", 80))
    print("✅ เชื่อมต่ออินเทอร์เน็ตสำเร็จ")
except OSError  as e:
    print(f"❌ ไม่สามารถเชื่อมต่ออินเทอร์เน็ต: {e}")
    exit(1)
# ตรวจสอบ IP Address
try:
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f"🌐 IP Address: {ip_address}" )
except OSError as e:
    print(f"❌ ไม่สามารถตรวจสอบ IP Address: {e}")
    exit(1)
# ตรวจสอบตำแหน่งที่ตั้ง
# ใช้ API ip-api.com เพื่อดึงข้อมูลตำแหน่งที่ตั้ง
try:
    response = requests.get("http://ip-api.com/json/")
    location = response.json()
    print(f"🌍 ตำแหน่งที่ตั้ง: {location['lat']}, {location['lon']}"
          f" ({location['city']}, {location['regionName']}, {location['country']})")
    lte_location = utils_variable.get_lte_info()
    print(f"📡 LTE ตำแหน่งที่ตั้ง: {lte_location}")
except requests.RequestException as e:
    print(f"❌ ไม่สามารถดึงข้อมูลตำแหน่งที่ตั้ง: {e}")
    exit(1)
# ตรวจสอบการเชื่อมต่อกับเซิร์ฟเวอร์
try:
    response = requests.get(SERVER_URL)
    if response.status_code == 200:
        print("✅ เชื่อมต่อกับเซิร์ฟเวอร์สำเร็จ")
    else:
        print(f"❌ ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์: {response.status_code}")
        exit(1)
except requests.RequestException as e:
    print(f"❌ ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์: {e}")
    exit(1)

######################################################

response_received = False

def compress_image_bytes(image_array, max_size=(640, 480), quality=50):
    """
    รับ numpy image array แล้วบีบอัดและแปลงเป็น binary JPEG
    """
    img = Image.fromarray(image_array).convert('RGB')
    img.thumbnail(max_size)
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=quality)
    return buffer.getvalue()  # return as binary


def capture_image_binary():
    picam2 = Picamera2()
    picam2.configure(picam2.create_still_configuration())

    try:
        picam2.start()
        time.sleep(2)
        frame = picam2.capture_array()  # numpy array
    except Exception as e:
        print(f"❌ ไม่สามารถถ่ายภาพได้: {e}")
        return None, None
    finally:
        picam2.close()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"plate_{timestamp}.jpg"
    img_binary = compress_image_bytes(frame, max_size=(640, 480), quality=50)

    print(f"📏 ขนาดภาพ JPEG บีบอัด: {len(img_binary) / 1024:.2f} KB")
    return img_binary, filename
    

def generate_mock_data():
    # สุ่มค่าหมวดตัวอักษรและจังหวัด
    lpr_str = random.choice(utils_variable.lpr_categories)
    province = random.choice(utils_variable.provinces)
    mock_data ={
        "license_plate": f"{lpr_str} {random.randint(1000, 9999)} {province}",
        #"location_lat": round(random.uniform(18.7, 18.9), 6),
        "location_lat": location["lat"],
        #"location_lon": round(random.uniform(98.9, 99.1), 6),
        "location_lon": location["lon"],
        "info": f" Image from  Raspberry Pi at ({location['city']}, {location['country']})"
    }
    print(f"ข้อมูลที่จะเตรียมส่ง: {mock_data} ")
    return mock_data


@sio.on('lpr_response')
def on_response(data):
    global response_received
    print("🎯 ได้รับผลตอบกลับจาก server:")
    print(f"  status: {data['status']}")
    print(f"  message: {data['message']}")
    print(f"  saved_path: {data.get('saved_path')}")
    response_received = True
    sio.disconnect()


def main():
    global response_received
    try:
        sio.connect(SERVER_URL)
        if sio.get_sid() is None:
            print("⚠️ ไม่สามารถรับ session ID จากเซิร์ฟเวอร์ อาจมีปัญหาการเชื่อมต่อ")
            return
        else:
            print(f"✅ เชื่อมต่อกับเซิร์ฟเวอร์สำเร็จ SID: {sio.get_sid()}")
    except Exception as e:
        print(f"❌ ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์: {e}")
        return

    image_binary, filename = capture_image_binary()
    if not image_binary or not filename:
        print("⚠️ ไม่สามารถถ่ายภาพได้ หรือแปลงเป็น binary ไม่สำเร็จ")
        return

    mock_data = generate_mock_data()

    # ส่ง metadata
    sio.emit('lpr_detection', {
        "license_plate": mock_data["license_plate"],
        "image_name": filename,
        "image_binary": image_binary,
        "location_lat": mock_data["location_lat"],
        "location_lon": mock_data["location_lon"],
        "info": mock_data["info"]
    })

    # ส่ง binary data
    #sio.emit('lpr_image', image_binary)

    print("📤 ส่ง metadata และ binary image ไปยัง server แล้ว รอผลตอบกลับ...")
    sio.wait()

if __name__ == "__main__":
    main()
