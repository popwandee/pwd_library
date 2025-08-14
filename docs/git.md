การแยก **Git Branch** สำหรับ **Development (`dev`)**, **Version 1 (`v1`)**, และ **Version 2 (`v2`)** ทำได้ง่ายและช่วยให้คุณจัดการโค้ดอย่างเป็นระบบ เพื่อให้ทำงานร่วมกันได้โดยไม่กระทบกัน  

---

### **🔷 ขั้นตอนการสร้างและจัดการ Git Branch**
#### **1️⃣ ตรวจสอบ Branch ปัจจุบัน**
ก่อนสร้าง Branch ใหม่ ให้ตรวจสอบ Branch ปัจจุบันว่าอยู่ที่ไหน
```bash
git branch
```
ถ้าคุณต้องการดู **Branch ที่อยู่บน Remote Repository ด้วย**
```bash
git branch -r
```

#### **2️⃣ สร้าง Branch สำหรับแต่ละเวอร์ชัน**
สร้าง Branch ใหม่สำหรับ **Development (dev)**
```bash
git branch dev
```
สร้าง Branch ใหม่สำหรับ **Version 1 (v1)**
```bash
git branch v1
```
สร้าง Branch ใหม่สำหรับ **Version 2 (v2)**
```bash
git branch v2
```

#### **3️⃣ สลับไปยัง Branch ที่ต้องการ**
สลับไปยัง `dev`
```bash
git checkout dev
```
หรือใช้คำสั่งย่อ:
```bash
git switch dev
```

#### **4️⃣ Push Branch ไปยัง Remote Repository**
หากคุณต้องการให้ Branch ใหม่ถูกส่งไปยัง **GitHub หรือ GitLab**, ใช้คำสั่ง:
```bash
git push -u origin dev
git push -u origin v1
git push -u origin v2
```

---

### **🔷 วิธีจัดการ Git Branch สำหรับแต่ละเวอร์ชัน**
#### **กรณี 1: พัฒนา `dev` และ Merge เข้า `v1`**
ถ้าคุณพัฒนาโค้ดใน `dev` และต้องการให้มันไปอยู่ใน `v1`
```bash
git checkout v1
git merge dev
```
จากนั้น **Push ไป Remote Repository**
```bash
git push origin v1
```

#### **กรณี 2: อัปเดต `v2` จาก `v1`**
ถ้าคุณต้องการให้ `v2` อัปเดตจาก `v1`
```bash
git checkout v2
git merge v1
git push origin v2
```

---

### **🔷 วิธีลบ Branch ที่ไม่ต้องการ**
หากต้องการลบ **Local Branch**
```bash
git branch -d dev
```
ถ้าต้องการลบ **Remote Branch**
```bash
git push origin --delete dev
```

---

### **🚀 สรุป**
✅ **สร้าง Branch แยกสำหรับ dev, v1, v2**  
✅ **ใช้ `git switch` หรือ `git checkout` เพื่อเปลี่ยน Branch**  
✅ **ใช้ `git merge` เพื่อรวมการเปลี่ยนแปลงระหว่าง Branch**  
✅ **Push Branch ไปยัง Remote Repository (`git push -u origin branch_name`)**  

ต้องการ **ปรับระบบ CI/CD ให้ทำงานร่วมกับ Branch แยก** ไหม? 🎯  
ฉันสามารถช่วยตั้งค่า **GitHub Actions หรือ GitLab CI/CD** เพื่อให้โค้ด Deploy อัตโนมัติ! 🚀
