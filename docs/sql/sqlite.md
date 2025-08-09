Markdown ระบบฐานข้อมูล: `sqlite.md` ครอบคลุมการติดตั้ง, ตั้งค่า, การใช้งานคำสั่ง SQL (CRUD), และการแก้ไขปัญหาเบื้องต้น เหมาะสำหรับใช้เป็นคู่มือการพัฒนาระบบ 🧠💾

---

## 📄 `sqlite.md`

```markdown
# 🗂️ SQLite คำสั่งพื้นฐานในการพัฒนาระบบ

## 🛠️ การติดตั้ง

```bash
pip install sqlite3   # สำหรับใช้งานผ่าน Python (มักมาพร้อมอยู่แล้ว)
```

## 🧭 สร้างฐานข้อมูล

```python
import sqlite3
conn = sqlite3.connect('database.db')
```

## 🔄 CRUD เบื้องต้น

```sql
-- สร้างตาราง
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER
);

-- เพิ่มข้อมูล
INSERT INTO users (name, age) VALUES ('Alice', 30);

-- อ่านข้อมูล
SELECT * FROM users;

-- แก้ไขข้อมูล
UPDATE users SET age = 31 WHERE name = 'Alice';

-- ลบข้อมูล
DELETE FROM users WHERE name = 'Alice';
```

## 🔍 ตรวจสอบการทำงาน

```python
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
```

## 🧯 แก้ปัญหาเบื้องต้น

- ตรวจสอบสิทธิ์ของไฟล์ `.db`
- ลบไฟล์ `.db` แล้วสร้างใหม่ (เฉพาะกรณีทดสอบ)
```