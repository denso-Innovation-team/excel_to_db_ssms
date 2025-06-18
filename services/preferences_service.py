import json
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class PreferencesService:
    """User preferences management"""

    def __init__(self):
        self.prefs_file = Path("config/user_preferences.json")
        self.prefs_file.parent.mkdir(exist_ok=True)
        self.defaults = {
            "theme": "light",
            "language": "en",
            "batch_size": 1000,
            "auto_backup": True,
            "backup_interval": 60,
            "recent_files": [],
            "default_import_mode": "append",
            "window_size": (1400, 900),
            "show_preview": True,
            "max_recent_files": 10,
        }
        self._preferences = self.load_preferences()

    def load_preferences(self) -> Dict[str, Any]:
        """Load preferences from file"""
        try:
            if self.prefs_file.exists():
                with open(self.prefs_file, "r", encoding="utf-8") as f:
                    return {**self.defaults, **json.load(f)}
        except Exception as e:
            logger.error(f"Error loading preferences: {e}")
        return self.defaults.copy()

    def save_preferences(self) -> bool:
        """Save current preferences to file"""
        try:
            with open(self.prefs_file, "w", encoding="utf-8") as f:
                json.dump(self._preferences, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving preferences: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """Get preference value"""
        return self._preferences.get(key, default)

    def set(self, key: str, value: Any) -> bool:
        """Set preference value"""
        try:
            self._preferences[key] = value
            return self.save_preferences()
        except Exception as e:
            logger.error(f"Error setting preference: {e}")
            return False

    def add_recent_file(self, file_path: str):
        """Add file to recent files list"""
        recent = self._preferences.get("recent_files", [])
        if file_path in recent:
            recent.remove(file_path)
        recent.insert(0, file_path)
        self._preferences["recent_files"] = recent[: self.get("max_recent_files", 10)]
        self.save_preferences()
