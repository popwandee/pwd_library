เอกสาร Markdown สำหรับใช้เป็นแหล่งอ้างอิงคำสั่ง Git ที่พบบ่อย พร้อมการแก้ปัญหาเบื้องต้น สำหรับนักพัฒนาในระบบที่ต้องการความเร็วและความชัดเจนในการใช้งาน:

---

```markdown
# 📚 Git Cheat Sheet & Troubleshooting Guide

## 🚀 Common Git Commands

### 📂 Repository Setup
- `git init`  
  สร้าง Git repository ใหม่ใน directory ปัจจุบัน  
- `git clone <url>`  
  คัดลอก repository จาก remote ไปยังเครื่อง local

### 🔍 Status & Logs
- `git status`  
  ตรวจสอบสถานะไฟล์ที่มีการเปลี่ยนแปลง  
- `git log`  
  ดูประวัติ commit ย้อนหลัง

### 💾 Staging & Commit
- `git add <file>`  
  เพิ่มไฟล์เข้าสู่ staging area  
- `git commit -m "Message"`  
  บันทึกการเปลี่ยนแปลงพร้อมข้อความ

### 🔁 Branch & Merge
- `git branch`  
  แสดงรายการ branch ที่มีอยู่  
- `git checkout -b <branch-name>`  
  สร้างและสลับไปยัง branch ใหม่  
- `git merge <branch>`  
  รวม branch เข้ากับ branch ปัจจุบัน

### 🔄 Remote & Push/Pull
- `git remote add origin <url>`  
  เพิ่ม remote repository  
- `git push -u origin <branch>`  
  ส่ง commit ไปยัง remote branch  
- `git pull`  
  ดึงข้อมูลล่าสุดจาก remote repository

---

## 🧯 Troubleshooting

### ❌ Merge Conflicts
- 🔍 ปัญหา: มีไฟล์ที่แก้ไขทั้งสอง branch  
- 🛠 วิธีแก้:
  1. เปิดไฟล์ที่มี conflict และแก้ไขตามต้องการ
  2. ใช้ `git add <file>` เพื่อ mark ว่าแก้ไขแล้ว
  3. แล้วทำ `git commit` เพื่อบันทึกการรวม

### ❌ Detached HEAD
- 🔍 ปัญหา: อยู่ใน commit ที่ไม่ได้ผูกกับ branch  
- 🛠 วิธีแก้:
  ```bash
  git checkout <branch-name>
  ```

### ❌ Forgot to Add Remote
- 🔍 ปัญหา: Push ไม่ได้เพราะไม่มี remote  
- 🛠 วิธีแก้:
  ```bash
  git remote add origin <url>
  git push -u origin main
  ```

### ❌ Untracked Files Not Removed
- 🔍 ปัญหา: มีไฟล์ที่ไม่อยู่ใน Git และไม่ต้องการใช้  
- 🛠 วิธีแก้:
  ```bash
  git clean -f     # ลบไฟล์ไม่ถูก track
  git clean -fd    # ลบทั้งไฟล์และ directory
  ```

---

## 📌 Tips
- ใช้ `git stash` เพื่อเก็บงานชั่วคราวก่อนเปลี่ยน branch
- ใช้ `.gitignore` เพื่อระบุไฟล์ที่ไม่ต้องการให้ Git track
- ตรวจสอบ config ด้วย `git config --list`

```

---

