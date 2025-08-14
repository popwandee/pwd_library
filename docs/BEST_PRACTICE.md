จากเอกสารที่แนบมาและข้อมูลเพิ่มเติมที่ค้นหามา ผมได้รวบรวมคำสั่งและแนวทางปฏิบัติที่จำเป็นในการพัฒนาโปรแกรม โดยจัดทำในรูปแบบไฟล์ `.md` เพื่อให้ง่ายต่อการใช้งาน ดังนี้ครับ

# คู่มือการพัฒนาและจัดการระบบ

## 1\. คำสั่ง Git ที่จำเป็น

คู่มือนี้รวบรวมคำสั่ง Git ขั้นพื้นฐานสำหรับการจัดการ Repository ของคุณ

### การตั้งค่า Git Repository

  * **ตั้งค่าโปรเจกต์ใหม่:** ใช้คำสั่งนี้ในโฟลเดอร์โปรเจกต์ของคุณเพื่อสร้าง Git Repository ใหม่
    ```bash
    git init
    ```
  * **เพิ่มไฟล์เข้าสู่ Staging Area:** เตรียมไฟล์ที่แก้ไขเพื่อทำการ commit
    ```bash
    git add .
    ```
  * **บันทึกการเปลี่ยนแปลง:** สร้าง commit เพื่อบันทึกการเปลี่ยนแปลงใน History
    ```bash
    git commit -m "ข้อความอธิบายการเปลี่ยนแปลง"
    ```
  * **เชื่อมต่อกับ Remote Repository:** ตั้งค่า Remote Repository (เช่น GitHub)
    ```bash
    git remote add origin <URL ของ Remote Repository>
    ```
  * **Push โค้ดขึ้น Remote:** ส่งโค้ดที่ commit แล้วขึ้นไปยัง Remote Repository
    ```bash
    git push -u origin main
    ```

### การจัดการ Branch

  * **สร้างและสลับไป Branch ใหม่:** สร้าง Branch ใหม่และสลับไปใช้งานทันที
    ```bash
    git switch -c <ชื่อ branch>
    ```
    หรือ
    ```bash
    git checkout -b <ชื่อ branch>
    ```
  * **สลับไป Branch ที่มีอยู่แล้ว:**
    ```bash
    git checkout <ชื่อ branch>
    ```
  * **ดู Branch ทั้งหมด:**
    ```bash
    git branch
    ```
  * **รวมโค้ดจากอีก Branch หนึ่ง:** รวมโค้ดจาก Branch ปัจจุบันเข้ากับ Branch อื่น
    ```bash
    git merge <ชื่อ branch ที่จะนำมารวม>
    ```

### การแก้ไขปัญหา Conflict

เมื่อเกิด `Merge Conflict` Git จะหยุดการ Merge และแจ้งว่ามีไฟล์ที่เกิดความขัดแย้ง

  * **ตรวจสอบสถานะ:** ใช้คำสั่งนี้เพื่อดูว่ามีไฟล์ใดที่เกิด Conflict
    ```bash
    git status
    ```
  * **การแก้ไข Conflict:** เมื่อเปิดไฟล์ที่มีปัญหา จะเห็นโค้ดที่มีเครื่องหมาย `<<<<<<<`, `=======`, และ `>>>>>>>` คุณต้องเลือกว่าจะใช้โค้ดส่วนไหนหรือแก้ไขใหม่ทั้งหมด
  * **ยกเลิกการ Merge:** หากไม่ต้องการแก้ไข Conflict สามารถยกเลิกการ Merge ได้ด้วยคำสั่ง
    ```bash
    git merge --abort
    ```
  * **ยืนยันการแก้ไข:** หลังจากแก้ไขไฟล์ที่มี Conflict แล้ว ให้ `add` และ `commit` เพื่อยืนยันว่าแก้ไขเสร็จสิ้น
    ```bash
    git add .
    git commit -m "Resolve merge conflict"
    ```

## 2\. คำสั่งสำหรับ Systemd

### `systemctl`

`systemctl` เป็นคำสั่งหลักสำหรับจัดการบริการ (services) และหน่วย (units) ต่างๆ ในระบบ Linux ที่ใช้ `systemd`

| คำสั่ง | คำอธิบาย |
| :--- | :--- |
| `systemctl start <ชื่อ service>` | เริ่มการทำงานของ Service นั้น |
| `systemctl stop <ชื่อ service>` | หยุดการทำงานของ Service นั้น |
| `systemctl restart <ชื่อ service>` | Restart Service |
| `systemctl reload <ชื่อ service>` | Reload Service โดยไม่ต้องหยุดการทำงาน (ถ้า Service รองรับ) |
| `systemctl status <ชื่อ service>` | แสดงสถานะปัจจุบันของ Service นั้นอย่างละเอียด |
| `systemctl enable <ชื่อ service>` | กำหนดให้ Service เริ่มทำงานอัตโนมัติเมื่อ Boot เครื่อง |
| `systemctl disable <ชื่อ service>` | ยกเลิกการเริ่มทำงานอัตโนมัติของ Service นั้น |
| `systemctl is-active <ชื่อ service>` | ตรวจสอบว่า Service กำลังทำงานหรือไม่ |
| `systemctl is-enabled <ชื่อ service>` | ตรวจสอบว่า Service ถูกตั้งค่าให้เริ่มอัตโนมัติหรือไม่ |

### `journalctl`

`journalctl` ใช้สำหรับดู Log ของระบบที่จัดการโดย `systemd`

* **ดู Log ทั้งหมด:** แสดง Log ทั้งหมดในระบบ
```bash
journalctl
```
* **ดู Log ของ Service เฉพาะ:** ดู Log ของ Service ที่ต้องการ
```bash
journalctl -u <ชื่อ service>
```
* **ดู Log แบบ Real-time:** แสดง Log ที่เข้ามาใหม่แบบต่อเนื่องเหมือนคำสั่ง `tail -f`
```bash
journalctl -f
```
* **ดู Log ตั้งแต่เวลาที่กำหนด:**
```bash
journalctl --since "YYYY-MM-DD HH:MM:SS"
```
* **จัดการ Log:** ตรวจสอบขนาดของ Log และลบ Log เก่าเพื่อประหยัดพื้นที่
```bash
journalctl --disk-usage
sudo journalctl --vacuum-size=1G
```

## 3\. แนวทางปฏิบัติที่ดีในการ Config Nginx, Gunicorn และ Systemd

### Nginx (Reverse Proxy)

Nginx ทำหน้าที่เป็น Reverse Proxy เพื่อรับ Request จากผู้ใช้และส่งต่อไปยัง Gunicorn ช่วยเพิ่มประสิทธิภาพและความปลอดภัย

* **ตัวอย่างไฟล์ `server block` ของ Nginx**
```nginx
server {
    listen 80;
    server_name your_domain.com www.your_domain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock; # ส่ง Request ไปยัง Gunicorn ผ่าน Unix socket
    }
}
```
* **แนวทางปฏิบัติ:**
    * ใช้ Nginx ในการจัดการ Request ที่เข้ามาทั้งหมด
    * ใช้ Nginx ในการ Serve ไฟล์ Static เพื่อลดภาระของ Gunicorn
    * ตั้งค่า `proxy_set_header` เพื่อให้ Gunicorn ทราบข้อมูล Request ที่ถูกต้อง เช่น `X-Forwarded-Proto` สำหรับ HTTPS
    * ตรวจสอบความถูกต้องของ Configuration ด้วย `sudo nginx -t` และ `sudo systemctl restart nginx` หลังจากการแก้ไข

### Gunicorn (Application Server)

Gunicorn ทำหน้าที่รันโปรแกรม Python ของคุณใน Production Environment

  * **แนวทางปฏิบัติ:**
      * ใช้ Gunicorn ร่วมกับ Nginx
      * ตั้งค่า Gunicorn ให้ทำงานใน Background โดยใช้ `systemd`
      * ใช้ Unix Socket (`/run/gunicorn.sock`) เพื่อให้ Nginx และ Gunicorn สื่อสารกันอย่างรวดเร็วและปลอดภัย

### Systemd (Configuration)

การใช้ `systemd` ในการจัดการ Gunicorn เป็นวิธีที่แนะนำเพื่อให้แอปพลิเคชันทำงานได้อย่างเสถียร

  * **ตัวอย่างไฟล์ `gunicorn.socket`:**
    ```ini
    [Unit]
    Description=gunicorn socket for my app

    [Socket]
    ListenStream=/run/gunicorn.sock

    [Install]
    WantedBy=sockets.target
    ```
  * **ตัวอย่างไฟล์ `gunicorn.service`:**
    ```ini
    [Unit]
    Description=Gunicorn service for my app
    After=network.target

    [Service]
    User=your_username
    Group=www-data
    WorkingDirectory=/path/to/your/app
    ExecStart=/path/to/your/venv/bin/gunicorn --workers 3 --bind unix:/run/gunicorn.sock wsgi:app
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```
  * **แนวทางปฏิบัติ:**
      * ใช้ `systemctl daemon-reload` เพื่อโหลดไฟล์ Configuration ใหม่หลังจากแก้ไข
      * ใช้ `systemctl enable --now gunicorn.socket gunicorn.service` เพื่อเริ่มและเปิดใช้งานบริการทันที
      * ตรวจสอบสถานะด้วย `systemctl status gunicorn.service`
      * ตั้งค่า `User` และ `Group` ให้เหมาะสมเพื่อความปลอดภัย
      * กำหนด `WorkingDirectory` ให้ถูกต้องเพื่อให้ Gunicorn หาไฟล์โปรเจกต์เจอ


การเขียนโค้ดตามแนวทางปฏิบัติที่ดีเป็นสิ่งสำคัญที่จะช่วยให้โค้ดอ่านง่าย บำรุงรักษาง่าย และทำงานร่วมกับผู้อื่นได้อย่างมีประสิทธิภาพ 

-----

### 1\. แนวทางปฏิบัติที่ดีสำหรับการเขียนโค้ด Python ตามมาตรฐาน PEP 8

**PEP 8 (Python Enhancement Proposal 8)** คือแนวทางในการเขียนโค้ด Python ที่ทุกคนในชุมชน Python ยอมรับและใช้เป็นมาตรฐาน เพื่อให้โค้ดมีความสอดคล้องกันและอ่านง่ายขึ้นมากครับ

**หลักการสำคัญของ PEP 8:**

  * **การเว้นวรรค (Indentation):** ใช้ 4 Space ในการเว้นวรรคแต่ละระดับ **ไม่ใช้ Tab**

    ```python
    # ถูกต้อง
    def my_function():
        x = 1
        if x == 1:
            print("Hello")

    # ผิด (ใช้ 2 space)
    def my_function():
      x = 1
    ```

  * **ความยาวบรรทัด:** จำกัดความยาวบรรทัดไม่เกิน 79 ตัวอักษร เพื่อให้โค้ดดูง่ายบนหน้าจอขนาดเล็ก

    ```python
    # ถูกต้อง (ตัดบรรทัดโดยใช้ \ หรือในวงเล็บ)
    long_variable_name = "This is a very long string that needs " \
                         "to be broken into multiple lines."

    def long_function(param_1, param_2,
                      param_3, param_4):
        pass
    ```

  * **การเว้นบรรทัดเปล่า:**

      * เว้น 2 บรรทัดเปล่าระหว่าง Class และ Function ระดับบนสุด (Top-level)
      * เว้น 1 บรรทัดเปล่าระหว่าง method ภายใน Class

    <!-- end list -->

    ```python
    # เว้น 2 บรรทัดระหว่าง class และ function
    class MyClass:
        pass


    def my_function():
        pass
    ```

  * **การตั้งชื่อ (Naming Conventions):**

      * **ตัวแปรและฟังก์ชัน:** ใช้ `snake_case` (ตัวพิมพ์เล็กคั่นด้วยขีดล่าง) เช่น `my_variable`, `calculate_total()`
      * **คลาส (Class):** ใช้ `PascalCase` หรือ `CamelCase` (ตัวอักษรตัวแรกของแต่ละคำเป็นตัวใหญ่) เช่น `MyClass`
      * **ค่าคงที่ (Constants):** ใช้ `ALL_CAPS` (ตัวพิมพ์ใหญ่ทั้งหมดคั่นด้วยขีดล่าง) เช่น `MAX_SIZE`

  * **การใช้เว้นวรรครอบตัวดำเนินการ (Operators):**

      * เว้น 1 ช่องว่างรอบๆ ตัวดำเนินการ เช่น `=`, `+`, `-`, `*`

    <!-- end list -->

    ```python
    # ถูกต้อง
    x = 1 + 2

    # ผิด
    x=1+2
    ```

**เครื่องมือช่วยตรวจสอบ:**

  * **`flake8`:** เป็นเครื่องมือที่ใช้ตรวจสอบโค้ดตามมาตรฐาน PEP 8 และอื่นๆ
  * **`autopep8`:** เป็นเครื่องมือที่แก้ไขโค้ดของคุณให้เป็นไปตาม PEP 8 โดยอัตโนมัติ

-----

### 2\. การ Import แบบ Absolute Imports

**Absolute Imports** คือการอ้างอิงโมดูลหรือแพ็กเกจจาก root directory ของโปรเจกต์ของคุณ ซึ่งเป็นวิธีที่แนะนำเพราะทำให้โค้ดมีความชัดเจนและไม่สับสนเมื่อต้องจัดการกับโครงสร้างไฟล์ที่ซับซ้อน

**ตัวอย่างโครงสร้างโปรเจกต์:**

```
my_project/
├── main.py
├── package_a/
│   ├── __init__.py
│   ├── module_1.py
│   └── sub_package_a/
│       ├── __init__.py
│       └── module_2.py
└── package_b/
    ├── __init__.py
    └── module_3.py
```

**ตัวอย่างการ Import แบบ Absolute:**
ถ้าคุณต้องการ import `do_something()` จาก `module_2.py` ไปใช้ใน `main.py`

```python
# ในไฟล์ my_project/main.py
from package_a.sub_package_a.module_2 import do_something

def main():
    do_something()

if __name__ == "__main__":
    main()
```

การ Import แบบนี้จะเริ่มจากชื่อแพ็กเกจหลัก `package_a` เสมอ ทำให้คุณทราบทันทีว่าโค้ดที่เรียกใช้มาจากที่ใด

-----