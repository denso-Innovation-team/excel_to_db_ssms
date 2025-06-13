# 🏭 DENSO888 - Excel to SQL Management System

**Professional Desktop Application สำหรับนำเข้าข้อมูล Excel เข้าสู่ฐานข้อมูล SQL Server และ SQLite**

Created by **เฮียตอมจัดหั้ย!!!** 🚀

## ✨ Key Features

### 🔐 **Authentication & Security**
- User Login/Logout system with role-based permissions
- Admin and User roles with database access control
- Session management with auto-timeout

### 📊 **Data Sources**
- **Mock Data Generation:** สร้างข้อมูลทดสอบ 100-50,000 แถว
  - Employee, Sales, Inventory, Financial templates
- **Excel Import:** รองรับ .xlsx, .xls, .xlsm
  - Multi-sheet support และ auto-type detection

### 🗄️ **Database Support**
- **SQLite:** ใช้งานได้ทันที (Local database)
- **SQL Server:** Enterprise database support
  - Windows Authentication และ SQL Server Authentication
  - Auto-fallback to SQLite เมื่อ SQL Server ไม่พร้อม

### ⚙️ **Processing Features**
- Real-time progress tracking
- Chunked processing สำหรับไฟล์ขนาดใหญ่
- Background processing ไม่หยุดการทำงาน UI
- Comprehensive error handling

## 🚀 Quick Start

### ✅ **Easy Installation**
```bash
# 1. Clone or download project
# 2. Double-click start_denso888.bat (Windows)
# หรือ run manually:
pip install pandas sqlalchemy pyodbc openpyxl python-dotenv tqdm
python main.py
```

### 🔑 **Default Login**
```
Username: admin
Password: admin123
```

### 📋 **Basic Usage**
1. Login เข้าระบบ
2. เลือกแหล่งข้อมูล (Mock Data หรือ Excel File)
3. กำหนดค่าฐานข้อมูล (SQLite หรือ SQL Server)
4. กดปุ่ม "🚀 Start Processing"
5. ใช้ "🔐 DB Test" สำหรับทดสอบการเชื่อมต่อ

## 🛠️ Configuration

### **SQL Server Connection**
```
Server: localhost หรือ ชื่อ Server
Database: excel_to_db
Authentication: 
  ✅ Windows Authentication (แนะนำ)
  ✅ SQL Server Authentication (username/password)
```

### **SQLite (Default)**
```
File: denso888_data.db
✅ ไม่ต้องติดตั้งเพิ่มเติม
✅ ใช้งานได้ทันที
```

## 📁 Project Structure

```
denso888-excel-to-sql/
├── main.py                    # Entry point
├── config/                    # Configuration
│   └── settings.py           # App settings
├── core/                      # Business logic
│   ├── excel_handler.py      # Excel processing
│   ├── database_manager.py   # Database operations
│   ├── mock_generator.py     # Mock data generation
│   └── data_processor.py     # Main processing pipeline
├── gui/                       # User interface
│   └── main_window.py        # Main GUI application
├── utils/                     # Utilities
│   ├── logger.py            # Logging system
│   ├── settings_manager.py  # Settings persistence
│   └── file_utils.py        # File operations
└── requirements.txt           # Dependencies
```

## 🔧 System Requirements

- **Python 3.8+**
- **Windows 10/11** (สำหรับ .exe build)
- **ODBC Driver 17 for SQL Server** (สำหรับ SQL Server connections)
- **RAM:** 4GB minimum, 8GB recommended
- **Storage:** 100MB สำหรับแอปพลิเคชัน

## 🎯 Performance

| Dataset Size  | Processing Time | Memory Usage |
|---------------|-----------------|--------------|
| 1,000 rows    | < 5 seconds    | < 50 MB      |
| 10,000 rows   | < 30 seconds   | < 100 MB     |
| 50,000 rows   | < 2 minutes    | < 200 MB     |

## 🛡️ Security Features

- Password hashing (SHA-256)
- Session management with timeout
- Role-based database permissions
- SQL injection prevention
- File validation และ error sanitization

## 🔄 Build Executable

```bash
# สร้าง .exe file
python build.py

# ติดตั้งจาก dist/
INSTALL_DENSO888.bat
```

## 📞 Support & Troubleshooting

### **Common Issues:**

1. **"ไม่สามารถเชื่อมต่อ SQL Server ได้"**
   - ตรวจสอบชื่อ Server และ ODBC Driver
   - ใช้ SQLite แทนได้

2. **"Excel file ไม่สามารถอ่านได้"**
   - ปิดไฟล์ใน Excel ก่อนประมวลผล
   - ตรวจสอบสิทธิ์การเข้าถึงไฟล์

3. **"Authentication ล้มเหลว"**
   - ใช้ admin/admin123 สำหรับ default login

### **Logs Location:**
```
logs/denso888.log - Application logs
auth.db - Authentication database  
denso888_settings.json - User settings
```

---

🏭 **DENSO888** - _Making Excel to SQL migration simple and secure!_ 🚀
