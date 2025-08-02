เอกสารในรูปแบบ **Markdown** ที่รวบรวมคำสั่งที่จำเป็นสำหรับการพัฒนาระบบด้วย **Python** และ **pip** ซึ่งครอบคลุมตั้งแต่การติดตั้ง ตั้งค่า ตรวจสอบ ไปจนถึงการแก้ปัญหาเบื้องต้น เหมาะมากสำหรับใช้เป็นคู่มือพัฒนา ⚙️🐍

---

```markdown
# 🛠️ คู่มือคำสั่ง Python และ pip สำหรับการพัฒนาระบบ

## 📦 ติดตั้งและตั้งค่าพื้นฐาน

### ติดตั้ง Python
- Windows: ดาวน์โหลดจาก [python.org](https://www.python.org/) และเลือก "Add Python to PATH" ขณะติดตั้ง
- macOS: ใช้ Homebrew
  ```bash
  brew install python
  ```
- Linux (Debian/Ubuntu):
  ```bash
  sudo apt update
  sudo apt install python3 python3-pip
  ```

### ตรวจสอบเวอร์ชัน
```bash
python --version
python3 --version
pip --version
```

### เปลี่ยนเวอร์ชัน Python (Linux/macOS)
```bash
update-alternatives --config python
```

---

## 🐍 จัดการแพ็กเกจด้วย pip

### ติดตั้งแพ็กเกจ
```bash
pip install <ชื่อแพ็กเกจ>
```

### ติดตั้งหลายแพ็กเกจจากไฟล์ requirements.txt
```bash
pip install -r requirements.txt
```

### สร้าง requirements.txt อัตโนมัติ
```bash
pip freeze > requirements.txt
```

### อัปเดตแพ็กเกจ
```bash
pip install --upgrade <ชื่อแพ็กเกจ>
```

### ถอนการติดตั้งแพ็กเกจ
```bash
pip uninstall <ชื่อแพ็กเกจ>
```

---

## 🧪 ตรวจสอบการทำงานของระบบ

### ทดสอบโค้ด Python
```bash
python <ชื่อไฟล์>.py
```

### ใช้งาน virtual environment (แนะนำให้ใช้เพื่อแยก dependencies)
```bash
python -m venv venv
source venv/bin/activate         # macOS/Linux
venv\Scripts\activate            # Windows
deactivate                       # ออกจาก venv
```

---

## 🩺 แก้ไขปัญหาเบื้องต้น

### pip ใช้งานไม่ได้
```bash
python -m ensurepip
```

### ล้าง cache ของ pip
```bash
pip cache purge
```

### ติดตั้ง pip ใหม่
```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

### ตรวจสอบ path ของ Python/Pip
```bash
which python
which pip
```

---

## 📚 ทรัพยากรเพิ่มเติม
- [เอกสาร Python](https://docs.python.org/3/)
- [pip Documentation](https://pip.pypa.io/en/stable/)

```

---
