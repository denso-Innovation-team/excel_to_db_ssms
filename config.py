"""Configuration management"""
import os
from dataclasses import dataclass
from urllib.parse import quote_plus

@dataclass
class DatabaseConfig:
    host: str = "localhost"
    database: str = "excel_to_db"
    username: str = "sa"
    password: str = "your_password"
    
    @classmethod
    def from_env(cls):
        return cls(
            host=os.getenv("DB_HOST", cls.host),
            database=os.getenv("DB_NAME", cls.database),
            username=os.getenv("DB_USER", cls.username),
            password=os.getenv("DB_PASSWORD", cls.password)
        )
    
    def get_url(self) -> str:
        password_encoded = quote_plus(self.password)
        return (
            f"mssql+pyodbc://{self.username}:{password_encoded}@"
            f"{self.host}/{self.database}?"
            f"driver=ODBC+Driver+17+for+SQL+Server&"
            f"TrustServerCertificate=yes&Encrypt=no"
        )

@dataclass  
class ProcessingConfig:
    batch_size: int = 1000
    chunk_size: int = 5000
    
    @classmethod
    def from_env(cls):
        return cls(
            batch_size=int(os.getenv("BATCH_SIZE", str(cls.batch_size))),
            chunk_size=int(os.getenv("CHUNK_SIZE", str(cls.chunk_size)))
        )
