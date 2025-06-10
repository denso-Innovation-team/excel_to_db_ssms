import os
from dotenv import load_dotenv
import sqlalchemy
from pathlib import Path


def test_env_loading():
    """ทดสอบการโหลด .env"""
    print("🔍 ทดสอบการโหลด .env file...")

    # หา .env file
    env_path = Path(".env")
    if not env_path.exists():
        print(f"❌ ไม่พบไฟล์ .env ที่ {env_path.absolute()}")
        return False

    print(f"✅ พบไฟล์ .env ที่ {env_path.absolute()}")

    # โหลด .env
    load_dotenv()

    # ตรวจสอบค่าที่โหลดมา
    db_config = {
        "DB_HOST": os.getenv("DB_HOST"),
        "DB_PORT": os.getenv("DB_PORT"),
        "DB_USER": os.getenv("DB_USER"),
        "DB_NAME": os.getenv("DB_NAME"),
        "DB_TYPE": os.getenv("DB_TYPE"),
    }

    print("📋 ค่าที่โหลดจาก .env:")
    for key, value in db_config.items():
        print(f"   {key}: {value}")

    # ตรวจสอบว่าโหลดค่ามาครบไหม
    missing = [k for k, v in db_config.items() if not v]
    if missing:
        print(f"❌ ขาดค่า: {missing}")
        return False

    print("✅ โหลด .env สำเร็จ")
    return True


def test_direct_connection():
    """ทดสอบเชื่อมต่อ Supabase โดยตรง"""
    print("\n🚀 ทดสอบเชื่อมต่อ Supabase โดยตรง...")

    # ค่าจาก .env
    load_dotenv()
    host = os.getenv("DB_HOST", "aws-0-ap-southeast-1.pooler.supabase.com")
    port = os.getenv("DB_PORT", "6543")
    user = os.getenv("DB_USER", "postgres.ydmmxivfmfgbbphmitgy")
    password = os.getenv("DB_PASSWORD", "jsCvOpw2RbFdpf5L")
    database = os.getenv("DB_NAME", "postgres")

    # สร้าง connection URL
    url = f"postgresql://{user}:{password}@{host}:{port}/{database}?sslmode=require"
    print(f"🔗 Connection URL: postgresql://{user}:***@{host}:{port}/{database}")

    try:
        # ทดสอบ connection
        engine = sqlalchemy.create_engine(url, connect_args={"connect_timeout": 10})

        with engine.connect() as conn:
            result = conn.execute(sqlalchemy.text("SELECT 1 as test"))
            test_result = result.fetchone()[0]
            print(f"✅ การเชื่อมต่อ Supabase สำเร็จ: {test_result}")

            # ทดสอบ version
            result = conn.execute(sqlalchemy.text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"📋 PostgreSQL version: {version[:50]}...")

        return True

    except Exception as e:
        print(f"❌ การเชื่อมต่อ Supabase ล้มเหลว: {e}")
        return False


def test_project_settings():
    """ทดสอบ project settings"""
    print("\n⚙️ ทดสอบ project settings...")

    try:
        # ทดสอบ import settings
        from src.config.settings import settings

        print("✅ Import settings สำเร็จ")

        # แสดงค่า settings
        print("📋 Settings ที่โหลดมา:")
        print(f"   DB_HOST: {settings.DB_HOST}")
        print(f"   DB_PORT: {settings.DB_PORT}")
        print(f"   DB_USER: {settings.DB_USER}")
        print(f"   DB_NAME: {settings.DB_NAME}")
        print(f"   DB_TYPE: {settings.DB_TYPE}")

        # ตรวจสอบว่าเป็น Supabase values
        if settings.DB_HOST == "localhost":
            print("❌ ยังเป็น localhost - settings ไม่ได้โหลด .env")
            return False

        if "supabase.com" in settings.DB_HOST:
            print("✅ Settings ตรงกับ Supabase")
            return True
        else:
            print("⚠️ Settings ไม่ตรงกับ Supabase")
            return False

    except Exception as e:
        print(f"❌ Import settings ล้มเหลว: {e}")
        return False


def main():
    print("🔧 Debug Supabase Connection")
    print("=" * 40)

    # Step 1: ทดสอบ .env
    if not test_env_loading():
        print("\n💡 แนวทางแก้ไข:")
        print("1. ตรวจสอบว่าไฟล์ .env อยู่ใน root directory")
        print("2. ตรวจสอบว่าค่าใน .env ครบถ้วน")
        return

    # Step 2: ทดสอบ direct connection
    if not test_direct_connection():
        print("\n💡 แนวทางแก้ไข:")
        print("1. ตรวจสอบ network connection")
        print("2. ตรวจสอบ Supabase credentials")
        print("3. pip install psycopg2-binary")
        return

    # Step 3: ทดสอบ project settings
    if not test_project_settings():
        print("\n💡 แนวทางแก้ไข:")
        print("1. แทนที่ src/config/settings.py ด้วยโค้ดใหม่")
        print("2. แทนที่ src/config/database.py ด้วยโค้ดใหม่")
        return

    print("\n🎉 ทุกการทดสอบผ่าน!")
    print("🚀 ระบบพร้อมใช้งาน")


if __name__ == "__main__":
    main()
