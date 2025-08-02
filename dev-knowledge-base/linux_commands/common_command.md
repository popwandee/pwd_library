แน่นอนครับ! ด้านล่างนี้คือตัวอย่างไฟล์ Markdown ที่รวมคำสั่ง Linux ที่นิยมใช้บ่อยในการพัฒนาระบบที่เกี่ยวข้องกับ **LPR (printing)**, **Python**, **อุปกรณ์ (devices)** และ **GPIO (สำหรับงาน embedded)** เหมาะสำหรับใช้เป็น Cheat Sheet หรือคู่มืออ้างอิงขณะทำงาน:

---

```markdown
# 🛠️ Linux Development Cheat Sheet for LPR, Python, Devices & GPIO

## 🖨️ LPR (Line Printer)

- `lpstat -p`  
  ตรวจสอบสถานะเครื่องพิมพ์ที่ติดตั้ง

- `lp -d <printer_name> <file>`  
  พิมพ์ไฟล์ไปยังเครื่องพิมพ์ที่เลือก

- `lpoptions -d <printer_name>`  
  ตั้งค่าเครื่องพิมพ์เริ่มต้น

- `cancel <job_id>`  
  ยกเลิกงานพิมพ์

## 🐍 Python Environment

- `python3 --version`  
  ตรวจสอบเวอร์ชันของ Python

- `pip3 install <package>`  
  ติดตั้ง Python package

- `python3 <script>.py`  
  รันสคริปต์ Python

- `virtualenv <env_name>`  
  สร้าง virtual environment (ต้องติดตั้ง `virtualenv` ก่อน)

- `source <env_name>/bin/activate`  
  เปิดใช้งาน virtual environment

## 🔧 Devices & Drivers

- `lsusb`  
  แสดงข้อมูลอุปกรณ์ USB ที่เชื่อมต่อ

- `lspci`  
  แสดงข้อมูลอุปกรณ์ PCI

- `dmesg | grep <device>`  
  ดู log kernel ของอุปกรณ์

- `lsmod`  
  แสดง module ที่โหลดในระบบ

- `modprobe <module>`  
  โหลด kernel module

- `udevadm info --query=all --name=/dev/<device>`  
  แสดงรายละเอียดอุปกรณ์

## 🧲 GPIO (ใช้กับ Raspberry Pi หรือ Embedded Linux)

- `gpio readall`  
  แสดงสถานะ GPIO ทั้งหมด (ใช้ได้ในบางระบบ เช่น WiringPi)

- `echo "out" > /sys/class/gpio/gpio<pin>/direction`  
  ตั้งค่า pin เป็น output

- `echo "1" > /sys/class/gpio/gpio<pin>/value`  
  ส่งค่า high (1) ไปยัง pin

- `echo "in" > /sys/class/gpio/gpio<pin>/direction`  
  ตั้งค่า pin เป็น input

- `cat /sys/class/gpio/gpio<pin>/value`  
  อ่านค่าจาก GPIO pin

> 📝 หมายเหตุ: คำสั่ง GPIO อาจต้องใช้สิทธิ์ `sudo` และต้อง `export` pin ก่อนใช้ เช่น  
> `echo <pin> > /sys/class/gpio/export`

---

## ✅ คำแนะนำเพิ่มเติม

- ใช้ `sudo` สำหรับคำสั่งที่เข้าถึงระดับ system
- ตรวจสอบ permissions ด้วย `ls -l /dev/<device>`
- ใช้ `crontab -e` เพื่อตั้ง schedule งานอัตโนมัติ (เช่น รีเซ็ต GPIO หรือสั่งพิมพ์รายงาน)

```

---

อยากให้ผมช่วยเพิ่มหัวข้ออื่น เช่น network tools, log monitoring หรือ shell scripting ไหมครับ? หรือจะให้แปลงเป็นรูปแบบไฟล์อื่นก็ยินดีช่วยได้เสมอ 🤝📂