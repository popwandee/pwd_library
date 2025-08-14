### 🚀 **Docker Workflow: คำสั่งพื้นฐานและแนวทางการใช้งานอย่างเป็นระบบ**

การใช้งาน **Docker Image** มีหลายขั้นตอน ตั้งแต่การ **สร้างไฟล์ที่จำเป็น**, **Build Image**, **Manage Containers**, ไปจนถึง **การส่งออกและนำเข้า Image ไปยังเครื่องอื่น**  

---

## 🔹 **1. การเตรียมไฟล์ที่จำเป็น**
สร้างไฟล์ **Dockerfile** เพื่อกำหนด **Image Build Process**  
ตัวอย่าง **Dockerfile** สำหรับ **Python App**
```dockerfile
# ใช้ Base Image Python
FROM python:3.11

# ตั้งค่า Working Directory
WORKDIR /app

# คัดลอกไฟล์จาก Local เข้า Container
COPY requirements.txt .

# ติดตั้ง Dependencies
RUN pip install -r requirements.txt

# คัดลอก Source Code ทั้งหมดไปยัง Container
COPY . .

# ตั้งค่า Default Command
CMD ["python", "app.py"]
```

---

## 🔹 **2. สร้าง Docker Image**
หลังจากเตรียม **Dockerfile**, ใช้คำสั่ง **Build Image**  
```bash
docker build -t my_python_app .
```
🔹 `-t my_python_app` 👉 กำหนดชื่อ Image  
🔹 `.` 👉 จุดหมายถึง **Build จาก Dockerfile ใน Directory ปัจจุบัน**  

📌 **ตรวจสอบ Images ที่มีอยู่**  
```bash
docker images
```

---

## 🔹 **3. รัน Container จาก Image**
เมื่อสร้าง Image เสร็จแล้ว ให้รัน Container
```bash
docker run -d --name my_container -p 5000:5000 my_python_app
```
🔹 `-d` 👉 Run แบบ **Background (Detached Mode)**  
🔹 `--name my_container` 👉 ตั้งชื่อ Container  
🔹 `-p 5000:5000` 👉 Map Port จาก Container ไปยัง Host  

📌 **ดู Container ที่กำลังทำงาน**
```bash
docker ps
```
📌 **ดู Container ทั้งหมด (รวมที่หยุดทำงานแล้ว)**
```bash
docker ps -a
```

📌 **เชื่อมเข้า Container ด้วย Bash**
```bash
docker exec -it my_container bash
```

---

## 🔹 **4. จัดการ Containers**
📌 **หยุด Container**
```bash
docker stop my_container
```

📌 **ลบ Container**
```bash
docker rm my_container
```

📌 **ลบ Image**
```bash
docker rmi my_python_app
```

---

## 🔹 **5. ส่งออก (Save) และนำเข้า (Load) Docker Image**
📌 **ส่งออก Image ไปเก็บไฟล์ `.tar`**
```bash
docker save -o my_python_app.tar my_python_app
```

📌 **นำเข้า Image บนเครื่องอื่น**
```bash
docker load -i my_python_app.tar
```

📌 **Push Image ไปที่ Docker Hub**
```bash
docker tag my_python_app mydockerhubuser/my_python_app:latest
docker push mydockerhubuser/my_python_app:latest
```

📌 **Pull Image จาก Docker Hub**
```bash
docker pull mydockerhubuser/my_python_app:latest
```

---

### 🚀 **สรุป Workflow อย่างเป็นระบบ**
✅ **เตรียมไฟล์** (`Dockerfile`, `requirements.txt`, Source Code)  
✅ **Build Image** (`docker build`)  
✅ **Run Container** (`docker run`)  
✅ **Manage Containers** (`docker ps`, `docker stop`, `docker rm`)  
✅ **ส่งออกและนำเข้า Image** (`docker save`, `docker load`)  
✅ **Push และ Pull จาก Docker Hub** (`docker push`, `docker pull`)  

คุณต้องการให้เพิ่ม **การใช้ Docker Compose สำหรับจัดการหลาย Container พร้อมกัน** ไหม? 🎯  
ฉันสามารถช่วยตั้งค่า **ระบบ CI/CD** ให้ Build Image อัตโนมัติได้! 🚀
