import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class Settings:
    """LocalDB Configuration"""
    
    def __init__(self):
        self.DB_HOST = os.getenv("DB_HOST", "(LocalDB)\MSSQLLocalDB")
        self.DB_NAME = os.getenv("DB_NAME", "excel_to_db")
        self.DB_TRUSTED_CONNECTION = os.getenv("DB_TRUSTED_CONNECTION", "yes")
        self.DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
        
        # Processing settings
        self.BATCH_SIZE = int(os.getenv("BATCH_SIZE", "2000"))
        self.MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))
        self.CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "10000"))
        
    def get_database_url(self) -> str:
        """LocalDB connection string"""
        if self.DB_TRUSTED_CONNECTION.lower() == "yes":
            return (
                f"mssql+pyodbc://@{self.DB_HOST}/{self.DB_NAME}?"
                f"driver={self.DB_DRIVER.replace(' ', '+')}&"
                f"TrustServerCertificate=yes&"
                f"Trusted_Connection=yes"
            )
        else:
            # Fallback to username/password
            user = os.getenv("DB_USER", "")
            password = quote_plus(os.getenv("DB_PASSWORD", ""))
            return (
                f"mssql+pyodbc://{user}:{password}@{self.DB_HOST}/{self.DB_NAME}?"
                f"driver={self.DB_DRIVER.replace(' ', '+')}&"
                f"TrustServerCertificate=yes"
            )
    
    def get_direct_connection_string(self) -> str:
        """Direct pyodbc connection string"""
        return (
            f"DRIVER={{{self.DB_DRIVER}}};"
            f"SERVER={self.DB_HOST};"
            f"DATABASE={self.DB_NAME};"
            f"Trusted_Connection=yes;"
        )

settings = Settings()
