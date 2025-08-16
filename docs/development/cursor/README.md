# Cursor AI Development Documentation

**คู่มือการใช้งาน Cursor AI สำหรับการพัฒนาโปรเจกต์ IoT แบบ Multi-Machine**

## 📚 **Documentation Index**

### 🎯 **Core Guides**
- **[01_cursor_basics.md](./01_cursor_basics.md)** - พื้นฐานการใช้งาน Cursor AI
- **[02_best_practices.md](./02_best_practices.md)** - แนวปฏิบัติที่ดีในการพัฒนา
- **[03_multi_instance_setup.md](./03_multi_instance_setup.md)** - การตั้งค่า Multi-Instance
- **[04_troubleshooting.md](./04_troubleshooting.md)** - การแก้ไขปัญหา

### 🛠️ **Configuration Files**
- **[settings.json](./config/settings.json)** - ไฟล์ตั้งค่า Cursor AI
- **[.cursorrules](./config/.cursorrules)** - กฎสำหรับโปรเจกต์ต่างๆ
- **[workspace_config.md](./config/workspace_config.md)** - การตั้งค่า Workspace

### 📖 **Templates & Examples**
- **[prompt_templates.md](./templates/prompt_templates.md)** - เทมเพลตคำสั่ง AI
- **[code_templates.md](./templates/code_templates.md)** - เทมเพลตโค้ด
- **[project_templates.md](./templates/project_templates.md)** - เทมเพลตโปรเจกต์

---

## 🚀 **Quick Start**

### 1. การติดตั้งและตั้งค่าพื้นฐาน
```bash
# ติดตั้ง Cursor AI
# ดาวน์โหลดจาก https://cursor.sh

# สร้างไฟล์ตั้งค่า
mkdir -p ~/.config/Cursor/User/
cp config/settings.json ~/.config/Cursor/User/
```

### 2. การตั้งค่าโปรเจกต์
```bash
# สร้าง .cursorrules สำหรับแต่ละโปรเจกต์
cp config/.cursorrules aicamera/
cp config/.cursorrules lprserver_v3/
```

### 3. การใช้งาน Multi-Instance
```bash
# เปิด Cursor AI หลายหน้าต่าง
cursor ~/iot-projects/aicamera/
cursor ~/iot-projects/lprserver_v3/
```

---

## 🎯 **Use Cases**

### Edge Development (Raspberry Pi)
- การพัฒนาโค้ดสำหรับ Raspberry Pi
- การจัดการเซ็นเซอร์และฮาร์ดแวร์
- การ optimize performance
- การจัดการ memory และ CPU

### Server Development (Ubuntu)
- การพัฒนา API และ backend
- การจัดการ database
- การ deploy และ monitoring
- การจัดการ security

### Multi-Machine Development
- การ sync โค้ดระหว่างเครื่อง
- การใช้ Tailscale VPN
- การ deploy แบบ automated
- การ monitor ระบบ

---

## 📋 **Best Practices Summary**

### 1. Project Organization
- แยก Edge และ Server development ให้ชัดเจน
- ใช้ .cursorrules ที่เหมาะสมสำหรับแต่ละโปรเจกต์
- จัดการ dependencies แยกกัน

### 2. Network Resilience
- ออกแบบระบบให้ทำงานได้แม้ network มีปัญหา
- ใช้ local caching และ buffering
- Implement retry logic และ circuit breakers

### 3. Development Efficiency
- ใช้ templates และ snippets
- Automate deployment และ testing
- Maintain consistent code style

---

## 🔧 **Troubleshooting**

### Common Issues
- **NGHTTP2_INTERNAL_ERROR**: ดู [Troubleshooting Guide](./04_troubleshooting.md)
- **Connection Issues**: ตรวจสอบ Tailscale และ network settings
- **Performance Issues**: ดู [Best Practices](./02_best_practices.md)

### Getting Help
- อ่าน [Troubleshooting Guide](./04_troubleshooting.md)
- ตรวจสอบ [Common Issues](./reference/common_issues.md)
- สอบถามใน [Community Forum](../community/forum.md)

---

## 📚 **Additional Resources**

- [Cursor AI Official Documentation](https://cursor.sh/docs)
- [Tailscale Documentation](https://tailscale.com/kb/)
- [Raspberry Pi Development](https://www.raspberrypi.org/documentation/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**Last Updated**: December 2024  
**Version**: 2.0.0
