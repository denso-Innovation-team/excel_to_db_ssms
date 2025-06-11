import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class Settings:
    """Clean SQL Server Configuration - No Port Issues"""
    
    def __init__(self):
        # Clean host - NO PORT
        self.DB_HOST = os.getenv("DB_HOST", "10.73.148.27")
        self.DB_NAME = os.getenv("DB_NAME", "excel_to_db")
        self.DB_USER = os.getenv("DB_USER", "TS00029")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", "Thammaphon@TS00029")
        self.DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
        
        # Pool settings
        self.POOL_SIZE = int(os.getenv("POOL_SIZE", "10"))
        self.MAX_OVERFLOW = int(os.getenv("MAX_OVERFLOW", "20"))
        self.POOL_TIMEOUT = int(os.getenv("POOL_TIMEOUT", "30"))
        self.POOL_RECYCLE = int(os.getenv("POOL_RECYCLE", "3600"))
        
        # Processing
        self.BATCH_SIZE = int(os.getenv("BATCH_SIZE", "2000"))
        self.MAX_WORKERS = int(os.getenv("MAX_WORKERS", "6"))
        self.CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "10000"))
    
    def get_database_url(self) -> str:
        """SQLAlchemy URL - HOST ONLY, no port"""
        password_encoded = quote_plus(self.DB_PASSWORD)
        
        # IMPORTANT: NO PORT in SQLAlchemy URL
        return (
            f"mssql+pyodbc://{self.DB_USER}:{password_encoded}@"
            f"{self.DB_HOST}/{self.DB_NAME}?"
            f"driver={self.DB_DRIVER.replace(' ', '+')}&"
            f"Encrypt=no&"
            f"TrustServerCertificate=yes"
        )
    
    def get_master_database_url(self) -> str:
        """Master database URL - HOST ONLY"""
        password_encoded = quote_plus(self.DB_PASSWORD)
        
        return (
            f"mssql+pyodbc://{self.DB_USER}:{password_encoded}@"
            f"{self.DB_HOST}/master?"
            f"driver={self.DB_DRIVER.replace(' ', '+')}&"
            f"Encrypt=no&"
            f"TrustServerCertificate=yes"
        )
    
    def get_direct_connection_string(self) -> str:
        """Direct pyodbc - CAN use port here"""
        return (
            f"DRIVER={{{self.DB_DRIVER}}};"
            f"SERVER={self.DB_HOST};"
            f"DATABASE={self.DB_NAME};"
            f"UID={self.DB_USER};"
            f"PWD={self.DB_PASSWORD};"
            f"Encrypt=no;"
            f"TrustServerCertificate=yes;"
        )

settings = Settings()
