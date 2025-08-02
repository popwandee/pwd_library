Markdown ระบบฐานข้อมูล:  `postgres.md` ครอบคลุมการติดตั้ง, ตั้งค่า, การใช้งานคำสั่ง SQL (CRUD), และการแก้ไขปัญหาเบื้องต้น เหมาะสำหรับใช้เป็นคู่มือการพัฒนาระบบ 🧠💾


## 🐘 `postgres.md`

```markdown
# 🐘 PostgreSQL คำสั่งพื้นฐานในการพัฒนาระบบ

## 🛠️ การติดตั้ง

### Linux (Ubuntu)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### macOS
```bash
brew install postgresql
```

## 🚀 เริ่มต้นใช้งาน

```bash
sudo service postgresql start
sudo -u postgres psql
```

## 🔄 CRUD เบื้องต้น

```sql
-- สร้างฐานข้อมูล
CREATE DATABASE mydb;

-- สร้างตาราง
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name TEXT,
    position TEXT
);

-- เพิ่มข้อมูล
INSERT INTO employees (name, position) VALUES ('Bob', 'Manager');

-- อ่านข้อมูล
SELECT * FROM employees;

-- แก้ไขข้อมูล
UPDATE employees SET position='Director' WHERE name='Bob';

-- ลบข้อมูล
DELETE FROM employees WHERE name='Bob';
```

## 🔍 ตรวจสอบการทำงาน

```bash
psql -d mydb -c "SELECT * FROM employees"
```

## 🧯 แก้ปัญหาเบื้องต้น

- ตรวจสอบว่า PostgreSQL รันอยู่: `sudo service postgresql status`
- เช็ค port: ค่า default คือ 5432
- ใช้ `\l` เพื่อดูฐานข้อมูล, `\dt` เพื่อดูตาราง
```

