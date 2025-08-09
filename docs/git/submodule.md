การนำโค้ดจาก Git Repository อื่นเข้ามาเป็นส่วนหนึ่งของโปรเจกต์เรา มักทำได้ด้วยวิธี **Git Submodule** ซึ่งเป็นการผูก Repository ภายนอกเข้ากับโปรเจกต์หลักของเรา โดยจะยังคงสถานะเป็น Repository แยกต่างหาก

#### แนวทางการใช้ Git Submodule

**ขั้นตอนที่ 1: การเพิ่ม Submodule**
ใช้คำสั่ง `git submodule add` เพื่อเพิ่ม Repository ที่ต้องการเข้ามาในโปรเจกต์ของคุณ
สมมติว่าคุณต้องการเพิ่มไลบรารีชื่อ `my-utility` เข้ามาในโฟลเดอร์ `vendor/`

```bash
git submodule add https://github.com/user/my-utility.git vendor/my-utility
```

คำสั่งนี้จะ:

1.  Clone `my-utility` Repository เข้ามาในโฟลเดอร์ `vendor/my-utility`
2.  เพิ่มไฟล์ `.gitmodules` ที่จะเก็บข้อมูลของ Submodule
3.  เพิ่มโฟลเดอร์ `vendor/my-utility` เข้ามาใน Git Index ของโปรเจกต์หลัก

**ขั้นตอนที่ 2: Clone Repository ที่มี Submodule**
หากมีผู้อื่น `git clone` โปรเจกต์หลักของคุณไป พวกเขาจะต้องใช้คำสั่งเพิ่มเติมเพื่อดึงโค้ดของ Submodule เข้ามาด้วย

```bash
# Clone โปรเจกต์หลัก
git clone https://github.com/popwandee/your-project.git

# Initialise และ Update submodule
cd your-project
git submodule update --init --recursive
```

  * `--init` ใช้สำหรับ Initialise Submodule ที่ยังไม่ถูกโหลดเข้ามา
  * `--recursive` ใช้สำหรับกรณีที่ Submodule นั้นมี Submodule ซ้อนอยู่ข้างในอีกที

**ข้อดีของ Git Submodule:**

  * สามารถรันและแก้ไขโค้ดใน Submodule ได้เหมือนกับเป็น Git Repository ปกติ
  * โค้ดของ Submodule จะแยกจากโค้ดของโปรเจกต์หลัก ทำให้จัดการการเปลี่ยนแปลงได้ง่าย

**ข้อควรระวัง:**

  * เมื่อทำการ Commit ใน Submodule และต้องการให้โปรเจกต์หลักอ้างอิงถึง Commit ล่าสุดนั้น ต้อง `git add` และ `git commit` ในโปรเจกต์หลักอีกครั้ง เพื่อบันทึกการเปลี่ยนแปลงของ Submodule

# อัปเดต submodules
```bash
git submodule update --init --recursive
```
