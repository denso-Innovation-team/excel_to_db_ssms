"""
Unified Configuration for DENSO888
"""

import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class DatabaseConfig:
    """Database configuration"""
    server: str = "localhost"
    database: str = "excel_to_db"
    username: str = "sa"
    password: str = ""
    use_windows_auth: bool = True
    sqlite_file: str = "denso888_data.db"
    
@dataclass
class UIConfig:
    """UI configuration"""
    theme: str = "denso_corporate"
    window_width: int = 1200
    window_height: int = 800
    
@dataclass
class AppConfig:
    """Main application configuration"""
    app_name: str = "DENSO888"
    version: str = "2.0.0"
    author: str = "Thammaphon Chittasuwanna (SDM)"
    
    # Sub-configs
    database: DatabaseConfig = DatabaseConfig()
    ui: UIConfig = UIConfig()

def get_config() -> AppConfig:
    """Get application configuration"""
    config = AppConfig()
    
    # Override from environment
    if os.getenv("DB_HOST"):
        config.database.server = os.getenv("DB_HOST")
    if os.getenv("DB_NAME"):
        config.database.database = os.getenv("DB_NAME")
        
    return config
