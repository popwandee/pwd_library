# pwd_library
Utilities library for python project
# วิธีนำไปใช้ในโปรเจกต์อื่น
วิธีที่ 1 เป็น Submodule ของ Git
- เพิ่มไลบรารีเป็น Submodule
<code>
git submodule add https://github.com/popwandee/pwd_library.git
</code>
- จากนั้นคุณสามารถ import ฟังก์ชั่นได้โดยตรงจากโฟลเดอร์ pwd_library/ ได้เลย

วิธิที่ 2 (ไม่แนะนำ) Copy - Paste ใช้ได้สำหรับโปรเจกต์เล็กๆ
- คัดลอกไฟล์และโฟลเดอร์ของไลบรารีไปวางในโปรเจกต์ใหม่
- จากนั้น import ฟังก์ชั่นที่ต้องการใช้

## ตัวอย่าง การนำไปใช้
 from pwd_library.data_processing
 import cleaning_functions

 text = "   Hello, World! "
 cleaned = cleaning_functions.clean_text(text)
 print(cleaned)