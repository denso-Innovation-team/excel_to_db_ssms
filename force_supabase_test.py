import sqlalchemy
import os
from pathlib import Path


def force_supabase_connection():
    """บังคับเชื่อมต่อ Supabase โดยตรง"""

    # ข้อมูล Supabase แบบ hardcode (ห้ามใช้ fallback)
    SUPABASE_CONFIG = {
        "host": "aws-0-ap-southeast-1.pooler.supabase.com",
        "port": 6543,
        "user": "postgres.ydmmxivfmfgbbphmitgy",
        "password": "jsCvOpw2RbFdpf5L",
        "database": "postgres",
    }

    print("🎯 Force Supabase Connection Test")
    print("=" * 40)
    print(f"Host: {SUPABASE_CONFIG['host']}")
    print(f"Port: {SUPABASE_CONFIG['port']}")
    print(f"User: {SUPABASE_CONFIG['user']}")
    print()

    # สร้าง URL แบบ hardcode
    url = f"postgresql://{SUPABASE_CONFIG['user']}:{SUPABASE_CONFIG['password']}@{SUPABASE_CONFIG['host']}:{SUPABASE_CONFIG['port']}/{SUPABASE_CONFIG['database']}?sslmode=require"

    try:
        print("🚀 กำลังเชื่อมต่อ Supabase...")

        engine = sqlalchemy.create_engine(
            url, connect_args={"connect_timeout": 30, "sslmode": "require"}, echo=False
        )

        with engine.connect() as conn:
            # Test basic connection
            result = conn.execute(sqlalchemy.text("SELECT 1 as test"))
            print(f"✅ เชื่อมต่อสำเร็จ: {result.fetchone()[0]}")

            # Test server info
            result = conn.execute(
                sqlalchemy.text("SELECT current_database(), current_user")
            )
            db_info = result.fetchone()
            print(f"📋 Database: {db_info[0]}, User: {db_info[1]}")

            # Test create table
            print("\n🏗️ ทดสอบสร้าง table...")
            conn.execute(
                sqlalchemy.text(
                    """
                DROP TABLE IF EXISTS test_connection;
                CREATE TABLE test_connection (
                    id SERIAL PRIMARY KEY,
                    message TEXT,
                    created_at TIMESTAMP DEFAULT NOW()
                );
            """
                )
            )

            # Insert test data
            conn.execute(
                sqlalchemy.text(
                    """
                INSERT INTO test_connection (message) 
                VALUES ('Supabase connection working!');
            """
                )
            )

            # Read test data
            result = conn.execute(
                sqlalchemy.text(
                    """
                SELECT id, message, created_at 
                FROM test_connection 
                ORDER BY id DESC LIMIT 1;
            """
                )
            )
            test_data = result.fetchone()
            print(f"✅ Test table: ID={test_data[0]}, Message='{test_data[1]}'")

            conn.commit()

        print("\n🎉 Supabase connection ใช้งานได้เต็มที่!")
        return True

    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")

        # Detailed error analysis
        error_str = str(e).lower()
        if "connection refused" in error_str:
            print("\n🔍 ปัญหา: Network connection")
            print("💡 ลองตรวจสอบ:")
            print("  - Internet connection")
            print("  - Firewall settings")
            print("  - VPN (หากใช้)")

        elif "authentication failed" in error_str:
            print("\n🔍 ปัญหา: Username/Password")
            print("💡 ตรวจสอบ Supabase dashboard:")
            print("  - Project settings → Database → Connection parameters")

        elif "timeout" in error_str:
            print("\n🔍 ปัญหา: Connection timeout")
            print("💡 ลองเพิ่ม timeout หรือใช้ direct connection")

        return False


def fix_project_settings():
    """แก้ไข project settings ให้ใช้ Supabase"""

    print("\n🔧 แก้ไข Project Settings")
    print("=" * 30)

    # สร้าง .env file
    env_content = """DB_HOST=aws-0-ap-southeast-1.pooler.supabase.com
DB_PORT=6543
DB_NAME=postgres
DB_USER=postgres.ydmmxivfmfgbbphmitgy
DB_PASSWORD=jsCvOpw2RbFdpf5L
DB_TYPE=postgresql
BATCH_SIZE=2000
MAX_WORKERS=6
CHUNK_SIZE=10000
LOG_LEVEL=INFO
LOG_FILE=logs/excel_to_db.log"""

    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        print("✅ สร้าง .env file")

        # แก้ไข settings.py
        settings_code = """from pydantic import BaseModel

class Settings(BaseModel):
    # Supabase Configuration - Hardcoded
    DB_HOST: str = "aws-0-ap-southeast-1.pooler.supabase.com"
    DB_PORT: int = 6543
    DB_NAME: str = "postgres"
    DB_USER: str = "postgres.ydmmxivfmfgbbphmitgy"
    DB_PASSWORD: str = "jsCvOpw2RbFdpf5L"
    DB_TYPE: str = "postgresql"
    
    BATCH_SIZE: int = 2000
    MAX_WORKERS: int = 6
    CHUNK_SIZE: int = 10000
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/excel_to_db.log"

settings = Settings()
"""

        # สร้าง directory หากไม่มี
        Path("src/config").mkdir(parents=True, exist_ok=True)

        with open("src/config/settings.py", "w", encoding="utf-8") as f:
            f.write(settings_code)
        print("✅ แก้ไข src/config/settings.py")

        # แก้ไข database.py
        database_code = """from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from .settings import settings

class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.Base = declarative_base()
        self._setup_engine()

    def _setup_engine(self):
        url = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}?sslmode=require"
        
        self.engine = create_engine(
            url,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            connect_args={"sslmode": "require", "connect_timeout": 30}
        )
        
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        return self.SessionLocal()

    def test_connection(self):
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                return True
        except:
            return False

db_manager = DatabaseManager()
"""

        with open("src/config/database.py", "w", encoding="utf-8") as f:
            f.write(database_code)
        print("✅ แก้ไข src/config/database.py")

        return True

    except Exception as e:
        print(f"❌ แก้ไขล้มเหลว: {e}")
        return False


def test_project_integration():
    """ทดสอบ project หลังแก้ไข"""

    print("\n🧪 ทดสอบ Project Integration")
    print("=" * 30)

    try:
        # Clear Python cache
        import sys

        modules_to_clear = [k for k in sys.modules.keys() if k.startswith("src.config")]
        for module in modules_to_clear:
            del sys.modules[module]

        # Test imports
        from src.config.settings import settings

        print(f"✅ Settings: {settings.DB_HOST}:{settings.DB_PORT}")

        from src.config.database import db_manager

        if db_manager.test_connection():
            print("✅ Database connection successful")
            return True
        else:
            print("❌ Database connection failed")
            return False

    except Exception as e:
        print(f"❌ Project test failed: {e}")
        return False


def main():
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "fix":
        # แก้ไข settings และทดสอบ
        if fix_project_settings():
            print("\n⏳ รอสักครู่...")
            import time

            time.sleep(1)  # รอให้ไฟล์เขียนเสร็จ

            if test_project_integration():
                print("\n🎉 แก้ไขสำเร็จ! ระบบพร้อมใช้งาน")
            else:
                print("\n⚠️ แก้ไขแล้วแต่ยังมีปัญหา")
        return

    # ทดสอบ Supabase connection โดยตรง
    if force_supabase_connection():
        print("\n💡 Supabase ใช้งานได้ ปัญหาอยู่ที่ project settings")
        print("รัน: python force_supabase_test.py fix")
    else:
        print("\n💡 ปัญหาอยู่ที่ Supabase connection")
        print("ตรวจสอบ network/credentials")


if __name__ == "__main__":
    main()
