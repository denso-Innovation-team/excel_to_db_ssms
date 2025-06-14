"""
Unified Configuration for DENSO888
"""

import os
from dataclasses import dataclass
from typing import Dict, Any
from .database import DatabaseConfig

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
    database: DatabaseConfig = None
    ui: UIConfig = None
    
    def __post_init__(self):
        if self.database is None:
            self.database = DatabaseConfig.from_env()
        if self.ui is None:
            self.ui = UIConfig()

def get_config() -> AppConfig:
    """Get application configuration"""
    return AppConfig()
