"""Database connection management - Updated with Hybrid Support"""

from hybrid_database import HybridDatabaseManager
from config import DatabaseConfig


def create_database_manager() -> HybridDatabaseManager:
    """สร้าง database manager ที่รองรับ SQL Server + SQLite fallback"""
    config = DatabaseConfig.from_env()
    return HybridDatabaseManager(config)


# Backward compatibility
class DatabaseManager:
    """Wrapper class สำหรับ backward compatibility"""

    def __init__(self, config: DatabaseConfig):
        self.hybrid_manager = HybridDatabaseManager(config)
        self.engine = None  # For compatibility

    def connect(self) -> bool:
        return self.hybrid_manager.connect()

    def test(self) -> bool:
        return self.hybrid_manager.test()

    @property
    def active_db(self):
        """ให้ access ถึง active database"""
        return self.hybrid_manager.active_db

    def get_status(self) -> dict:
        """ดูสถานะ database ปัจจุบัน"""
        return self.hybrid_manager.get_status()
