# Excel to SQL Server Setup Guide

## 🎯 Overview
ระบบ import ข้อมูลจาก Excel เข้า SQL Server ด้วย Python

## 📋 Prerequisites

### 1. SQL Server
- SQL Server 2019+ หรือ SQL Server Express
- SQL Server Management Studio (SSMS)
- SQL Server Authentication เปิดใช้งาน

### 2. Python Requirements
```bash
pip install -r requirements.txt
```

### 3. ODBC Driver
- Windows: ติดตั้ง "ODBC Driver 17 for SQL Server" จาก Microsoft
- Linux/Mac: ดูคู่มือติดตั้งจาก Microsoft

## ⚙️ Configuration

### 1. แก้ไข .env file
```env
DB_HOST=localhost
DB_PORT=1433
DB_NAME=ExcelImportDB
DB_USER=sa
DB_PASSWORD=YourStrongPassword123
DB_TYPE=mssql
DB_DRIVER=ODBC Driver 17 for SQL Server
```

### 2. สร้าง Database ใน SQL Server
```sql
CREATE DATABASE ExcelImportDB;
```

## 🚀 Usage

### Quick Test
```bash
python test_sqlserver.py
```

### Import Excel File
```bash
python test_sqlserver.py data.xlsx table_name
```

### Advanced Processing
```bash
python src/main.py data.xlsx employees
```

## 🔧 Troubleshooting

### Connection Issues
1. ตรวจสอบ SQL Server ทำงานหรือไม่
2. ตรวจสอบ SQL Server Authentication
3. ตรวจสอบ Windows Firewall
4. ลอง pymssql หาก ODBC ไม่ได้

### Performance Tips
- ลด BATCH_SIZE หาก memory ไม่พอ
- เพิ่ม CHUNK_SIZE สำหรับไฟล์ใหญ่
- ปรับ MAX_WORKERS ตาม CPU cores

## 📊 Features
- Auto-detect data types
- Parallel processing
- Progress tracking
- Error handling
- Unicode support (Thai text)
- Chunked processing for large files

## 🎉 Success!
หากทุกอย่างทำงานได้ คุณจะเห็นข้อมูลใน SSMS → ExcelImportDB → Tables
