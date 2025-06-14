"""
config/database.py
Database Configuration Wrapper for DENSO888
"""

from dataclasses import dataclass
from typing import Optional
import os


@dataclass
class DatabaseConfig:
    """Database configuration with connection URL generation"""
    
    server: str = "localhost"
    database: str = "excel_to_db" 
    username: str = "sa"
    password: str = ""
    use_windows_auth: bool = True
    sqlite_file: str = "denso888_data.db"
    
    # Connection settings
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 30
    pool_recycle: int = 3600
    
    def get_connection_url(self) -> Optional[str]:
        """Generate SQLAlchemy connection URL"""
        if self.use_windows_auth:
            return f"mssql+pyodbc://{self.server}/{self.database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
        else:
            return f"mssql+pyodbc://{self.username}:{self.password}@{self.server}/{self.database}?driver=ODBC+Driver+17+for+SQL+Server"
    
    @classmethod
    def from_env(cls):
        """Create config from environment variables"""
        return cls(
            server=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "excel_to_db"),
            username=os.getenv("DB_USER", "sa"),
            password=os.getenv("DB_PASSWORD", ""),
            use_windows_auth=os.getenv("DB_USE_WINDOWS_AUTH", "true").lower() == "true",
            sqlite_file=os.getenv("SQLITE_FILE", "denso888_data.db")
        )


def get_database_config() -> DatabaseConfig:
    """Get database configuration"""
    return DatabaseConfig.from_env()
