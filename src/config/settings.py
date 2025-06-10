import os
from typing import Optional

class Settings:
    """SQL Server Configuration"""
    
    def __init__(self):
        # SQL Server Configuration
        self.DB_HOST = os.getenv("DB_HOST", "localhost")
        self.DB_PORT = int(os.getenv("DB_PORT", "1433"))
        self.DB_NAME = os.getenv("DB_NAME", "ExcelImportDB")
        self.DB_USER = os.getenv("DB_USER", "sa")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", "YourStrongPassword123")
        self.DB_TYPE = os.getenv("DB_TYPE", "mssql")
        self.DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
        
        # Processing Configuration
        self.BATCH_SIZE = int(os.getenv("BATCH_SIZE", "1000"))
        self.MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))
        self.CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "5000"))
        
        # Logging
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FILE = os.getenv("LOG_FILE", "logs/excel_to_sqlserver.log")
        
    def get_database_url(self) -> str:
        """สร้าง connection string สำหรับ SQL Server"""
        return (
            f"mssql+pyodbc://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?"
            f"driver={self.DB_DRIVER.replace(' ', '+')}&TrustServerCertificate=yes"
        )
    
    def get_pymssql_url(self) -> str:
        """Alternative connection string using pymssql"""
        return (
            f"mssql+pymssql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

settings = Settings()
