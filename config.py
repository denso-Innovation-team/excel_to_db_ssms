"""
config.py - DENSO888 Configuration
"""

import os
from dataclasses import dataclass

@dataclass
class Config:
    APP_NAME: str = "DENSO888"
    VERSION: str = "2.0.0"
    AUTHOR: str = "Thammaphon Chittasuwanna (SDM)"
    
    # Database
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_NAME: str = os.getenv("DB_NAME", "denso888") 
    DB_USER: str = os.getenv("DB_USER", "sa")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    SQLITE_FILE: str = "denso888_data.db"
    
    # UI
    WINDOW_WIDTH: int = 1200
    WINDOW_HEIGHT: int = 800
    
    # Processing
    BATCH_SIZE: int = 1000
    MAX_WORKERS: int = 4
    
    def get_sqlite_url(self) -> str:
        return f"sqlite:///{self.SQLITE_FILE}"

# Global config
config = Config()
