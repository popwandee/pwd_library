เนื่องจาก feature/detection branch เก่าเกินไปแล้ว และต้องการ sync กับ main branch ล่าสุด ให้ทำตามขั้นตอนนี้:

## 🔄 **วิธี Sync Feature Branch กับ Main**

### **Option 1: Rebase (แนะนำ) - เพื่อ Clean History**

```bash
# 1. Switch ไป main branch และ pull ล่าสุด
git checkout main
git pull origin main

# 2. Switch กลับไป feature/detection
git checkout feature/detection

# 3. Rebase feature branch บน main ล่าสุด
git rebase main

# หากมี conflicts:
# - แก้ไข conflicts ในไฟล์ที่ขัดแย้ง
# - git add <resolved-files>
# - git rebase --continue

# 4. Force push (ระวัง: ใช้เฉพาะ feature branch)
git push --force-with-lease origin feature/detection
```

### **Option 2: Merge (ง่ายกว่า) - รักษา History**

```bash
# 1. อยู่ใน feature/detection branch
git checkout feature/detection

# 2. Pull main branch เข้ามา
git pull origin main

# หรือ
git merge origin/main

# 3. แก้ไข conflicts (หากมี)
# 4. Push
git push origin feature/detection
```

### **Option 3: สร้าง Branch ใหม่ (ปลอดภัยที่สุด)**

```bash
# 1. สร้าง branch ใหม่จาก main ล่าสุด
git checkout main
git pull origin main
git checkout -b feature/detection-v2

# 2. Cherry-pick commits ที่ต้องการจาก feature/detection เก่า
git log feature/detection --oneline  # ดู commit history
git cherry-pick <commit-hash>  # เลือก commits ที่ต้องการ

# 3. Push branch ใหม่
git push origin feature/detection-v2
```

## ⚠️ **สิ่งที่ต้องระวัง**

### **ก่อน Sync:**
```bash
# สำรองงานปัจจุบัน
git stash push -m "WIP: detection system before sync"

# หรือสร้าง backup branch
git branch feature/detection-backup
```

### **หลัง Sync:**
```bash
# ตรวจสอบว่าไฟล์ที่พัฒนาไว้ยังคงอยู่
ls -la v1_3/src/components/detection_processor.py
ls -la v1_3/src/services/detection_manager.py
ls -la v1_3/src/web/blueprints/detection.py

# ตรวจสอบ git status
git status
```

## 🛠️ **แก้ไข Conflicts ที่อาจเกิดขึ้น**

เนื่องจากคุณได้พัฒนา Detection system ไว้แล้ว อาจมี conflicts ในไฟล์:

1. **`v1_3/src/core/dependency_container.py`** - การ register detection services
2. **`v1_3/src/web/blueprints/__init__.py`** - การ register detection blueprint  
3. **`v1_3/src/core/config.py`** - detection configuration parameters

### **วิธีแก้ Conflicts:**
```bash
# เมื่อเกิด conflict
git status  # ดูไฟล์ที่ขัดแย้ง

# แก้ไขไฟล์ที่ขัดแย้ง โดยรักษาการพัฒนา Detection system ไว้
# ลบ conflict markers: <<<<<<< ======= >>>>>>>

# เพิ่มไฟล์ที่แก้แล้ว
git add <resolved-files>

# Continue rebase หรือ complete merge
git rebase --continue  # สำหรับ rebase
# หรือ
git commit  # สำหรับ merge
```

## 📋 **แนะนำ: ใช้ Option 1 (Rebase)**

เนื่องจากเป็น feature branch และต้องการ clean history:

```bash
git checkout main
git pull origin main
git checkout feature/detection
git rebase main
# แก้ conflicts (หากมี)
git push --force-with-lease origin feature/detection
```

หลังจาก sync เสร็จแล้ว ระบบ Detection ที่พัฒนาไว้จะยังคงอยู่ และสามารถทำงานร่วมกับ main branch ล่าสุดได้ครับ 🚀