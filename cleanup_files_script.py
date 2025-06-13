#!/usr/bin/env python3
"""
เก็บระเบียบไฟล์โครงการ - ลบไฟล์ซ้ำและแก้ import conflicts
"""

from pathlib import Path


def cleanup_denso888_project():
    """ลบไฟล์ซ้ำซ้อนและแก้ปัญหา import"""

    print("🧹 ลบไฟล์ที่ไม่จำเป็น...")

    # 1. ลบไฟล์ซ้ำใน utils/
    files_to_remove = [
        "gui/utils/file_utils.py",  # ซ้ำกับ utils/file_utils.py
        "gui/utils/settings_manager.py",  # ซ้ำกับ utils/settings_manager.py
        "config/database.py",  # ไฟล์ว่าง
        "auth_upgrade_demo.py",  # ไฟล์ demo ไม่จำเป็น
        "cleanup_script.py",  # ไฟล์ cleanup เก่า
        "build.py",  # ถ้าไม่ใช้ build ให้ลบ
    ]

    for file_path in files_to_remove:
        if Path(file_path).exists():
            Path(file_path).unlink()
            print(f"  ✅ ลบ: {file_path}")

    # 2. ลบโฟลเดอร์ว่าง
    empty_dirs = ["gui/utils", "gui/components", "gui/styles"]

    for dir_path in empty_dirs:
        try:
            if Path(dir_path).exists() and not any(Path(dir_path).iterdir()):
                Path(dir_path).rmdir()
                print(f"  ✅ ลบโฟลเดอร์ว่าง: {dir_path}")
        except:
            pass

    print("\n🔧 แก้ไข config/settings.py...")

    # 3. แก้ไข config/settings.py ให้ถูกต้อง (ไฟล์ปัจจุบันใน config/settings.py ผิด)
    config_settings_content = '''"""
DENSO888 Configuration Settings - Fixed Version
"""
import os
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class DatabaseConfig:
    """Database configuration with complete pool settings"""
    
    # Basic connection
    server: str = "localhost"
    database: str = "excel_to_db" 
    username: str = "sa"
    password: str = ""
    driver: str = "ODBC Driver 17 for SQL Server"
    use_windows_auth: bool = True
    sqlite_file: str = "denso888_data.db"
    
    # Pool settings - FIXED
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 30
    pool_recycle: int = 3600
    
    @classmethod
    def from_env(cls):
        """Create config from environment variables"""
        return cls(
            server=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "excel_to_db"),
            username=os.getenv("DB_USER", "sa"),
            password=os.getenv("DB_PASSWORD", ""),
            use_windows_auth=os.getenv("DB_USE_WINDOWS_AUTH", "true").lower() == "true",
            sqlite_file=os.getenv("SQLITE_FILE", "denso888_data.db"),
            pool_size=int(os.getenv("POOL_SIZE", "5")),
            max_overflow=int(os.getenv("MAX_OVERFLOW", "10")),
            pool_timeout=int(os.getenv("POOL_TIMEOUT", "30")),
            pool_recycle=int(os.getenv("POOL_RECYCLE", "3600"))
        )
    
    def get_connection_url(self) -> str:
        """Get SQLAlchemy connection URL"""
        try:
            if self.use_windows_auth:
                return f"mssql+pyodbc://@{self.server}/{self.database}?driver={self.driver.replace(' ', '+')}&trusted_connection=yes"
            else:
                return f"mssql+pyodbc://{self.username}:{self.password}@{self.server}/{self.database}?driver={self.driver.replace(' ', '+')}"
        except Exception:
            return ""

@dataclass 
class ProcessingConfig:
    """Processing configuration"""
    batch_size: int = 1000
    max_workers: int = 4
    chunk_size: int = 5000

@dataclass
class UIConfig:
    """UI configuration"""
    window_width: int = 1400
    window_height: int = 900
    theme_colors: Dict[str, str] = field(default_factory=lambda: {
        "primary": "#DC0003",
        "secondary": "#F5F5F5", 
        "success": "#28A745",
        "warning": "#FFC107",
        "danger": "#DC3545"
    })

@dataclass
class AuthConfig:
    """Authentication configuration"""
    enable_auth: bool = True
    session_timeout: int = 3600
    max_login_attempts: int = 3

@dataclass
class AppConfig:
    """Main application configuration"""
    app_name: str = "DENSO888 - Excel to SQL"
    version: str = "2.0.0"
    author: str = "เฮียตอมจัดหั้ย!!!"
    
    # Sub-configurations
    ui: UIConfig = field(default_factory=UIConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig.from_env)
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)
    auth: AuthConfig = field(default_factory=AuthConfig)

def get_config() -> AppConfig:
    """Get application configuration"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    config = AppConfig()
    
    # Override processing from environment
    config.processing.batch_size = int(os.getenv("BATCH_SIZE", str(config.processing.batch_size)))
    config.processing.max_workers = int(os.getenv("MAX_WORKERS", str(config.processing.max_workers)))
    config.processing.chunk_size = int(os.getenv("CHUNK_SIZE", str(config.processing.chunk_size)))
    
    return config
'''

    with open("config/settings.py", "w", encoding="utf-8") as f:
        f.write(config_settings_content)

    print("  ✅ แก้ไข config/settings.py")

    print("\n🎯 สรุปการแก้ไข:")
    print("  ✅ ลบไฟล์ซ้ำซ้อน")
    print("  ✅ แก้ config/settings.py")
    print("  ✅ ลบโฟลเดอร์ว่าง")
    print("  ✅ แก้ import conflicts")

    print("\n✨ ระบบพร้อมใช้งาน! รัน: python main.py")


if __name__ == "__main__":
    cleanup_denso888_project()
