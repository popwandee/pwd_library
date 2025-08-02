Markdown ระบบฐานข้อมูล:  `mysql.md` ครอบคลุมการติดตั้ง, ตั้งค่า, การใช้งานคำสั่ง SQL (CRUD), และการแก้ไขปัญหาเบื้องต้น เหมาะสำหรับใช้เป็นคู่มือการพัฒนาระบบ 🧠💾


## 🐬 `mysql.md`

```markdown
# 🐬 MySQL คำสั่งพื้นฐานในการพัฒนาระบบ

## 🛠️ การติดตั้ง

### Linux (Ubuntu)
```bash
sudo apt update
sudo apt install mysql-server
```

### macOS
```bash
brew install mysql
```

## 🚀 เริ่มต้นใช้งาน

```bash
sudo service mysql start
mysql -u root -p
```

## 🔄 CRUD เบื้องต้น

```sql
-- สร้างฐานข้อมูล
CREATE DATABASE myapp;

-- สร้างตาราง
USE myapp;
CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

-- เพิ่มข้อมูล
INSERT INTO customers (name, email) VALUES ('Jane', 'jane@example.com');

-- อ่านข้อมูล
SELECT * FROM customers;

-- แก้ไขข้อมูล
UPDATE customers SET email='new@example.com' WHERE name='Jane';

-- ลบข้อมูล
DELETE FROM customers WHERE name='Jane';
```

## 🔍 ตรวจสอบการทำงาน

```bash
mysqladmin -u root -p ping
```

## 🧯 แก้ปัญหาเบื้องต้น

- ลืมรหัสผ่าน root: เริ่ม MySQL ด้วย `--skip-grant-tables`
- ตรวจสอบ service: `sudo service mysql status`
- ใช้ `SHOW DATABASES;` และ `SHOW TABLES;` ตรวจสอบโครงสร้าง
```

---