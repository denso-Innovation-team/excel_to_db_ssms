"""Settings Manager for DENSO888"""
import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SettingsManager:
    """Manage application settings with persistence"""
    
    def __init__(self, settings_file: str = "denso888_settings.json"):
        self.settings_file = Path(settings_file)
        self._defaults = {
            "window": {"geometry": "1400x900", "maximized": False},
            "data_source": {
                "default_type": "mock",
                "default_template": "employees", 
                "default_rows": 1000,
                "recent_files": []
            },
            "database": {
                "default_type": "sqlite",
                "sqlite_file": "denso888_data.db",
                "sql_server": {
                    "host": "localhost",
                    "database": "excel_to_db",
                    "username": "sa",
                    "use_windows_auth": True
                }
            },
            "processing": {"chunk_size": 5000, "batch_size": 1000}
        }
    
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file or return defaults"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return self._defaults.copy()
        except Exception as e:
            logger.warning(f"Failed to load settings: {e}")
            return self._defaults.copy()
    
    def save_settings(self, settings: Dict[str, Any]) -> bool:
        """Save settings to file"""
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
            return False
