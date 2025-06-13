# วางโค้ดนี้ลงในไฟล์ utils/settings_manager.py
import json
from pathlib import Path
from typing import Dict, Any


class SettingsManager:
    """Settings persistence for DENSO888"""

    def __init__(self, settings_file: str = "denso888_settings.json"):
        self.settings_file = Path(settings_file)
        self._default_settings = {
            "window": {"geometry": "1200x800"},
            "database": {"default_type": "sqlite"},
            "data_source": {"default_type": "mock"},
        }

    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return self._default_settings.copy()
        except Exception:
            return self._default_settings.copy()

    def save_settings(self, settings: Dict[str, Any]) -> bool:
        """Save settings to file"""
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
