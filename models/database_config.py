"""
models/database_config.py
Database Configuration Model
Created by: Thammaphon Chittasuwanna (SDM) | Innovation Department
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from urllib.parse import quote_plus


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

    def get_connection_url(self) -> Optional[str]:
        """Get SQLAlchemy connection URL"""
        if self.db_type == "sqlite":
            return f"sqlite:///{self.sqlite_file}"

        elif self.db_type == "sqlserver":
            if self.use_windows_auth:
                server_part = f"{self.server}"
                if self.port != 1433:
                    server_part += f",{self.port}"

                params = []
                if self.trust_certificate:
                    params.append("TrustServerCertificate=yes")
                if self.encrypt:
                    params.append("Encrypt=yes")

                param_string = "&".join(params)
                if param_string:
                    param_string = "&" + param_string

                return (
                    f"mssql+pyodbc://@{server_part}/{self.database}"
                    f"?driver={quote_plus(self.driver)}"
                    f"&trusted_connection=yes{param_string}"
                )
            else:
                server_part = f"{self.server}"
                if self.port != 1433:
                    server_part += f",{self.port}"

                params = []
                if self.trust_certificate:
                    params.append("TrustServerCertificate=yes")
                if self.encrypt:
                    params.append("Encrypt=yes")

                param_string = "&".join(params)
                if param_string:
                    param_string = "&" + param_string

                return (
                    f"mssql+pyodbc://{quote_plus(self.username)}:"
                    f"{quote_plus(self.password)}@{server_part}/"
                    f"{self.database}?driver={quote_plus(self.driver)}{param_string}"
                )

        return None

    def update_from_dict(self, data: Dict[str, Any]):
        """Update configuration from dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
