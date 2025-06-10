import os

class Settings:
    """Supabase PostgreSQL Configuration"""
    
    def __init__(self):
        # Supabase PostgreSQL
        self.DB_HOST = "aws-0-ap-southeast-1.pooler.supabase.com"
        self.DB_PORT = 6543
        self.DB_NAME = "postgres"
        self.DB_USER = "postgres.ydmmxivfmfgbbphmitgy"
        self.DB_PASSWORD = "jsCvOpw2RbFdpf5L"
        self.DB_TYPE = "postgresql"
        
        # Processing Configuration
        self.BATCH_SIZE = 2000
        self.MAX_WORKERS = 6
        self.CHUNK_SIZE = 10000
        
        # Logging
        self.LOG_LEVEL = "INFO"
        self.LOG_FILE = "logs/excel_to_db.log"
        
    def get_database_url(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?sslmode=require"

settings = Settings()
