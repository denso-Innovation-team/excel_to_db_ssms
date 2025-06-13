# 🏭 DENSO888 - Excel to SQL Management System

## Professional Desktop Application สำหรับนำเข้าข้อมูล Excel เข้าสู่ฐานข้อมูล SQL Server และ SQLite

Created by **เฮียตอมจัดหั้ย!!!** 🚀

## ✨ Key Features

### 🔐 **Authentication & Security**

- ✅ **User Authentication System** - ระบบ Login/Logout
- ✅ **Role-based Permissions** - Admin, User roles
- ✅ **Database Privileges Management** - CRUD permissions control
- ✅ **Session Management** - Auto-logout, session timeout

### 📊 **Data Sources**

- ✅ **Mock Data Generation** - สร้างข้อมูลทดสอบ (100 - 50,000 rows)
  - 👥 Employee data (บุคลากร)
  - 💰 Sales transactions (ยอดขาย)
  - 📦 Inventory management (คลังสินค้า)
  - 💳 Financial records (บัญชี)
- ✅ **Excel File Import** - รองรับ .xlsx, .xls, .xlsm
  - 📋 Multi-sheet support
  - 🔍 Auto-type detection
  - 🧹 Data cleaning & validation

### 🗄️ **Database Support**

- ✅ **SQLite** (Local database) - ใช้งานได้ทันที
- ✅ **SQL Server** - Enterprise database
  - 🔑 Windows Authentication
  - 👤 SQL Server Authentication
  - 🔍 Server discovery
  - 📊 Database listing
- ✅ **Auto-fallback** - SQLite เมื่อ SQL Server ไม่พร้อม

### ⚙️ **Processing Features**

- ✅ **Real-time Progress** tracking
- ✅ **Chunked Processing** - จัดการไฟล์ใหญ่
- ✅ **Batch Operations** - ประสิทธิภาพสูง
- ✅ **Background Processing** - ไม่หยุดการทำงาน UI
- ✅ **Error Handling** - จัดการข้อผิดพลาด

### 🛠️ **Admin Tools**

- ✅ **Database Connection Testing** - ทดสอบการเชื่อมต่อ
- ✅ **CRUD Testing** - ทดสอบการ Create, Read, Update, Delete
- ✅ **Permission Verification** - ตรวจสอบสิทธิ์
- ✅ **Server Discovery** - ค้นหา SQL Server อัตโนมัติ

### 💻 **User Interface**

- ✅ **Modern GUI** - Tkinter with custom styling
- ✅ **Tabbed Interface** - Results, Logs, Settings
- ✅ **Real-time Logs** - แสดงสถานะการทำงาน
- ✅ **Progress Visualization** - Progress bar และ status
- ✅ **Error Dialogs** - ข้อความแสดงข้อผิดพลาดภาษาไทย

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **ODBC Driver 17 for SQL Server** (สำหรับ SQL Server)
- **Windows 10/11** (สำหรับ .exe build)

### Development Setup

```bash
# 1. Clone repository
git clone https://github.com/your-repo/denso888-excel-to-sql.git
cd denso888-excel-to-sql

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run application
python main.py
```

### Production Build

```bash
# Build executable
python build.py

# Install from dist/
INSTALL_DENSO888.bat
```

## 📋 Default Login

```
Username: admin
Password: admin123
```

## 🔧 Configuration

### Environment Variables (.env)

```bash
# SQL Server Configuration
DB_HOST=localhost
DB_NAME=excel_to_db
DB_USER=sa
DB_PASSWORD=your_password

# Processing Settings
BATCH_SIZE=1000
CHUNK_SIZE=5000
MAX_WORKERS=4

# Authentication
AUTH_ENABLE=true
SESSION_TIMEOUT=3600
```

### Database Permissions

| Role      | SQLite        | SQL Server | CRUD Test  | Admin  |
| --------- | ------------- | ---------- | ---------- | ------ |
| **Admin** | ✅ All        | ✅ All     | ✅ Yes     | ✅ Yes |
| **User**  | ✅ Read/Write | ❌ Limited | ✅ Limited | ❌ No  |

## 📁 Project Structure

```
denso888-excel-to-sql/
├── 📄 main.py                    # Entry point
├── 📁 config/                    # Configuration
│   ├── settings.py              # App configuration
│   └── environment.py           # Environment setup
├── 📁 core/                      # Business logic
│   ├── excel_handler.py         # Excel processing
│   ├── database_manager.py      # Database operations
│   ├── mock_generator.py        # Mock data creation
│   └── data_processor.py        # Main processing pipeline
├── 📁 gui/                       # User interface
│   └── main_window.py           # Main GUI application
├── 📁 utils/                     # Utilities
│   ├── logger.py                # Logging system
│   ├── error_handler.py         # Error handling
│   ├── settings_manager.py      # Settings persistence
│   └── file_utils.py            # File operations
├── 📁 assets/                    # Static files
├── 📁 tests/                     # Test suite
└── 📁 dist/                      # Build output
```

## 🎯 Usage Guide

### 1. **Authentication**

- Launch application
- Login with credentials
- System checks user permissions

### 2. **Data Source Selection**

```
📊 Mock Data:
- Template: employees/sales/inventory/financial
- Rows: 100 - 50,000

📁 Excel Import:
- Browse file (.xlsx/.xls)
- Select sheet
- Auto-validation
```

### 3. **Database Configuration**

```
📁 SQLite:
- Local file database
- No server required
- Immediate usage

🏢 SQL Server:
- Server name/IP
- Database selection
- Authentication method
- Permission testing
```

### 4. **Processing**

- Configure table name
- Start processing
- Monitor real-time progress
- View results and logs

### 5. **Database Testing**

- Use "🔐 DB Test" button
- Test connections
- Verify CRUD permissions
- List available databases

## 📊 Performance

| Dataset Size  | Processing Time    | Memory Usage |
| ------------- | ------------------ | ------------ |
| 1,000 rows    | < 5 seconds        | < 50 MB      |
| 10,000 rows   | < 30 seconds       | < 100 MB     |
| 50,000 rows   | < 2 minutes        | < 200 MB     |
| 100,000+ rows | Chunked processing | Optimized    |

## 🛡️ Security Features

- ✅ **Password Hashing** - SHA-256
- ✅ **Session Management** - Timeout protection
- ✅ **Permission Control** - Role-based access
- ✅ **SQL Injection Prevention** - Parameterized queries
- ✅ **File Validation** - Excel file verification
- ✅ **Error Sanitization** - No sensitive data in errors

## 🔧 Troubleshooting

### Common Issues

### 1. "ไม่สามารถเชื่อมต่อ SQL Server ได้"

- ตรวจสอบชื่อ Server
- เปิด SQL Server Browser service
- ตรวจสอบ Firewall settings
- ลองใช้ SQLite แทน

### 2. "Excel file ไม่สามารถอ่านได้"

- ตรวจสอบไฟล์ไม่เสียหาย
- ปิดไฟล์ใน Excel ก่อนประมวลผล
- ตรวจสอบสิทธิ์การเข้าถึงไฟล์

### 3. "Authentication ล้มเหลว"

- ตรวจสอบ username/password
- ตรวจสอบ User permissions
- ลองใช้ Windows Authentication

### 4. "หน่วยความจำไม่เพียงพอ"

- ลดจำนวน rows ในการประมวลผล
- ใช้ chunked processing
- ปิดโปรแกรมอื่นที่ไม่จำเป็น

## 📝 Logs Location

```
logs/
├── denso888.log          # Application logs
├── auth.db              # Authentication database
└── denso888_settings.json # User settings
```

## 🔄 Updates & Maintenance

### Version History

- **v2.0.0** - Complete rewrite with authentication
- **v1.5.0** - Added SQL Server support
- **v1.0.0** - Initial SQLite version

### Regular Maintenance

- Clean temporary files automatically
- Backup authentication database
- Monitor log file sizes
- Update dependencies regularly

## 🤝 Support

### Getting Help

1. **Check logs** in `logs/denso888.log`
2. **Use DB Test** feature to diagnose connection issues
3. **Enable detailed logging** for troubleshooting
4. **Create issue** with error details

### System Requirements

- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.8+ (for development)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 100MB for application + data storage
- **Network**: Required for SQL Server connections

## 📞 Contact

**Developer**: เฮียตอมจัดหั้ย!!!  
**Version**: 2.0.0  
**License**: MIT License  
**Built with**: Python, Tkinter, SQLAlchemy, Pandas

---

🏭 **DENSO888** - _Making Excel to SQL migration simple and secure!_ 🚀
