import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class Settings:
    def __init__(self):
        self.DB_HOST = os.getenv("DB_HOST", "10.73.148.27")
        self.DB_PORT = os.getenv("DB_PORT", "1433") 
        self.DB_NAME = os.getenv("DB_NAME", "excel_to_db")
        self.DB_USER = os.getenv("DB_USER", "TS00029")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", "Thammaphon@TS00029")
        self.DB_DRIVER = "ODBC Driver 17 for SQL Server"
        
        self.POOL_SIZE = int(os.getenv("POOL_SIZE", "5"))
        self.MAX_OVERFLOW = int(os.getenv("MAX_OVERFLOW", "10"))
        self.POOL_TIMEOUT = 30
        self.POOL_RECYCLE = 3600
        
        self.BATCH_SIZE = int(os.getenv("BATCH_SIZE", "2000"))
        self.MAX_WORKERS = int(os.getenv("MAX_WORKERS", "6"))
        self.CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "10000"))
        
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FILE = os.getenv("LOG_FILE", "logs/excel_to_ssms.log")
    
    def get_database_url(self):
        password_encoded = quote_plus(self.DB_PASSWORD)
        return (
            f"mssql+pyodbc://{self.DB_USER}:{password_encoded}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?"
            f"driver=ODBC+Driver+17+for+SQL+Server&"
            f"TrustServerCertificate=yes&Encrypt=no"
        )
    
    def get_direct_connection_string(self):
        return (
            f"DRIVER={{{self.DB_DRIVER}}};"
            f"SERVER={self.DB_HOST},{self.DB_PORT};"
            f"DATABASE={self.DB_NAME};"
            f"UID={self.DB_USER};"
            f"PWD={self.DB_PASSWORD};"
            f"TrustServerCertificate=yes;Encrypt=no;"
        )

settings = Settings()