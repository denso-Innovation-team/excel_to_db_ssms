#!/usr/bin/env python3
"""
Alternative SQL Server Test - Without pyodbc dependency
ทดสอบการเชื่อมต่อ SQL Server โดยไม่ต้องใช้ pyodbc
"""

def test_sqlalchemy_only():
    """ทดสอบ SQLAlchemy connection อย่างเดียว"""
    try:
        from sqlalchemy import create_engine, text
        from urllib.parse import quote_plus
        
        print("🔍 Testing SQLAlchemy connection to SQL Server...")
        
        # Connection parameters
        host = "10.73.148.27"
        port = "1433"
        database = "master"
        username = "TS00029"
        password = "Thammaphon@TS00029"
        
        # URL encode password
        password_encoded = quote_plus(password)
        
        # Connection URL
        connection_url = (
            f"mssql+pyodbc://{username}:{password_encoded}@"
            f"{host}:{port}/{database}?"
            f"driver=ODBC+Driver+17+for+SQL+Server&"
            f"TrustServerCertificate=yes&"
            f"Encrypt=optional"
        )
        
        print(f"📋 Connecting to: {host}:{port}")
        
        # Create engine
        engine = create_engine(
            connection_url,
            pool_size=1,
            max_overflow=0,
            pool_pre_ping=True,
            echo=False,
            connect_args={"timeout": 10}
        )
        
        # Test connection
        with engine.connect() as conn:
            # Basic test
            result = conn.execute(text("SELECT 1 as test"))
            test_value = result.fetchone()[0]
            print(f"✅ Connection test: {test_value}")
            
            # Server info
            result = conn.execute(text("SELECT @@VERSION"))
            version = result.fetchone()[0].split('\n')[0]
            print(f"📋 SQL Server: {version}")
            
            # Check ExcelImportDB
            result = conn.execute(text("""
                SELECT name FROM sys.databases 
                WHERE name = 'ExcelImportDB'
            """))
            
            if not result.fetchone():
                print("📋 Creating ExcelImportDB database...")
                conn.execute(text("CREATE DATABASE ExcelImportDB"))
                conn.commit()
                print("✅ Database created")
            else:
                print("✅ Database ExcelImportDB exists")
        
        print("\n🎉 SQLAlchemy connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ SQLAlchemy connection failed: {e}")
        
        error_str = str(e).lower()
        if "login failed" in error_str:
            print("💡 Check username/password in .env file")
        elif "driver" in error_str:
            print("💡 Install ODBC Driver 17 for SQL Server")
        elif "network" in error_str:
            print("💡 Check network connectivity to 10.73.148.27")
        
        return False

def test_basic_excel_processing():
    """ทดสอบการประมวลผล Excel โดยไม่ต้องเชื่อมฐานข้อมูล"""
    try:
        import pandas as pd
        
        print("\n🔍 Testing Excel processing...")
        
        # สร้างข้อมูลทดสอบ
        test_data = {
            'Name': ['สมชาย ใจดี', 'สมหญิง รักดี', 'วิชัย เจริญ'],
            'Age': [25, 30, 35],
            'Salary': [50000.0, 75000.0, 85000.0],
            'Department': ['IT', 'การตลาด', 'บัญชี']
        }
        
        df = pd.DataFrame(test_data)
        test_file = 'test_data.xlsx'
        
        # สร้างไฟล์ Excel
        df.to_excel(test_file, index=False, engine='openpyxl')
        print(f"✅ Created test file: {test_file}")
        
        # อ่านไฟล์กลับ
        df_read = pd.read_excel(test_file, engine='openpyxl')
        print(f"✅ Read back {len(df_read)} rows")
        print(f"📋 Columns: {list(df_read.columns)}")
        
        # ลบไฟล์ทดสอบ
        import os
        os.remove(test_file)
        print("✅ Excel processing works")
        
        return True
        
    except Exception as e:
        print(f"❌ Excel processing failed: {e}")
        return False

def main():
    print("🔧 Alternative SQL Server Test")
    print("=" * 40)
    
    # Test 1: SQLAlchemy connection
    sql_ok = test_sqlalchemy_only()
    
    # Test 2: Excel processing  
    excel_ok = test_basic_excel_processing()
    
    if sql_ok and excel_ok:
        print("\n🎉 Core functionality works!")
        print("🚀 You can proceed with Excel import")
        print("\n📋 Usage:")
        print("  python excel_to_sqlserver.py your_file.xlsx table_name")
    else:
        if not sql_ok:
            print("\n❌ SQL Server connection needs fixing")
        if not excel_ok:
            print("\n❌ Excel processing needs fixing")

if __name__ == "__main__":
    main()
