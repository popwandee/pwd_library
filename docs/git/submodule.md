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
นี่คือหนึ่งในคุณสมบัติหลักที่ทำให้ Submodule มีประโยชน์มาก เพราะมันยังคงสถานะเป็น Git Repository ที่สมบูรณ์อยู่ภายในโปรเจกต์หลักของเรา

เมื่อคุณ cd เข้าไปในโฟลเดอร์ของ Submodule โฟลเดอร์นั้นจะทำงานเหมือน Git Repository ทั่วไปเลยครับ คุณสามารถแก้ไขโค้ด, สร้าง commit, และ push การเปลี่ยนแปลงไปยัง Remote Repository ของ Submodule ได้โดยตรง

ผมจะอธิบายขั้นตอนการทำงานให้ละเอียดขึ้นดังนี้ครับ

ขั้นตอนการแก้ไขและ Push โค้ดใน Submodule
เข้าสู่โฟลเดอร์ Submodule:
ใช้คำสั่ง cd เพื่อเข้าไปในโฟลเดอร์ของ Submodule ที่คุณต้องการแก้ไขโค้ด

```bash
cd <ชื่อโฟลเดอร์ submodule>
```
เช่น cd vendor/my-utility

แก้ไขและ Commit โค้ด:
ทำการแก้ไขไฟล์ใน Submodule ตามปกติ จากนั้นใช้คำสั่ง git add และ git commit ภายในโฟลเดอร์ของ Submodule นั้น

```bash
# (หลังจากแก้ไขไฟล์แล้ว)
git add .
git commit -m "Fix: แก้ไข bug ใน my-utility library"
```
Push การเปลี่ยนแปลงไปยัง Remote Repository ของ Submodule:
ใช้คำสั่ง git push เพื่อส่ง commit ใหม่นี้ไปยัง Remote Repository ของ Submodule

```bash
git push origin main
```
ตอนนี้ Remote Repository ของ Submodule ก็จะมีการเปลี่ยนแปลงล่าสุดแล้วครับ

อัปเดตโปรเจกต์หลักให้ชี้ไปที่ Commit ใหม่ของ Submodule:
นี่คือขั้นตอนที่สำคัญที่สุดครับ! เมื่อคุณ cd กลับมาที่ root directory ของโปรเจกต์หลัก Git จะตรวจพบว่า Submodule ได้เปลี่ยนไปชี้ยัง Commit ใหม่
คุณจะต้อง add และ commit การเปลี่ยนแปลงนี้ในโปรเจกต์หลักของคุณ เพื่อบันทึกว่า Submodule ตอนนี้อ้างอิงถึง Commit ที่คุณเพิ่ง push ไป

```bash

# กลับมาที่โปรเจกต์หลัก
cd ..

# ตรวจสอบสถานะ จะเห็นว่า submodule มีการเปลี่ยนแปลง
git status

# เพิ่มการเปลี่ยนแปลงและ commit
git add <ชื่อโฟลเดอร์ submodule>
git commit -m "Update: อัปเดต my-utility submodule ให้เป็นเวอร์ชันล่าสุด"

# Push โปรเจกต์หลักขึ้น remote
git push origin main
```
สรุป:

คุณสามารถแก้ไขและ Push โค้ดได้โดยตรงจากภายในโฟลเดอร์ Submodule

หลังจาก Push ใน Submodule เสร็จแล้ว คุณต้องกลับมา commit และ push ในโปรเจกต์หลักอีกครั้ง เพื่ออัปเดต reference (ตัวอ้างอิง) ที่ชี้ไปยัง Commit ล่าสุดของ Submodule
นี่คือวิธีการทำงานที่ถูกต้องเพื่อให้โปรเจกต์หลักของคุณทราบว่า Submodule มีการเปลี่ยนแปลงครับ