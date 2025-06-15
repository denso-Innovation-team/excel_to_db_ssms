"""
models/database_config.py
Fixed Database Configuration Model
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class DatabaseConfig:
    """Database configuration model"""

    # Connection Type
    db_type: str = "sqlite"  # sqlite, sqlserver

    # SQLite Settings
    sqlite_file: str = "denso888_data.db"

    # SQL Server Settings
    server: str = ""
    database: str = ""
    username: str = ""
    password: str = ""
    port: int = 1433
    driver: str = "ODBC Driver 17 for SQL Server"
    use_windows_auth: bool = True
    trust_certificate: bool = True
    encrypt: bool = True

    # Connection Pool Settings
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 30
    pool_recycle: int = 3600

    def get_connection_params(self) -> Dict[str, Any]:
        """Get connection parameters for database manager"""
        if self.db_type == "sqlite":
            return {"db_type": "sqlite", "sqlite_file": self.sqlite_file}
        elif self.db_type == "sqlserver":
            return {
                "db_type": "sqlserver",
                "server": self.server,
                "database": self.database,
                "username": self.username,
                "password": self.password,
                "port": self.port,
                "driver": self.driver,
                "use_windows_auth": self.use_windows_auth,
                "trust_certificate": self.trust_certificate,
                "encrypt": self.encrypt,
            }
        else:
            return {"db_type": "sqlite", "sqlite_file": self.sqlite_file}

    def update_from_dict(self, data: Dict[str, Any]):
        """Update configuration from dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def validate(self) -> tuple[bool, str]:
        """Validate configuration"""
        if self.db_type == "sqlite":
            if not self.sqlite_file:
                return False, "SQLite file path is required"
            return True, "Valid SQLite configuration"

        elif self.db_type == "sqlserver":
            if not self.server:
                return False, "Server name is required"
            if not self.database:
                return False, "Database name is required"
            if not self.use_windows_auth and (not self.username or not self.password):
                return False, "Username and password required for SQL authentication"
            return True, "Valid SQL Server configuration"

        else:
            return False, f"Unknown database type: {self.db_type}"
