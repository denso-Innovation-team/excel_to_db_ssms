"""
utils/settings_manager.py
Settings persistence for DENSO888
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class SettingsManager:
    """Manage application settings persistence"""

    def __init__(self, settings_file: str = "denso888_settings.json"):
        self.settings_file = Path(settings_file)
        self._default_settings = self._get_default_settings()

    def _get_default_settings(self) -> Dict[str, Any]:
        """Get default application settings"""
        return {
            "window": {"geometry": "1200x800", "maximized": False},
            "data_source": {
                "default_type": "mock",
                "default_template": "employees",
                "default_rows": 1000,
                "last_excel_directory": "",
                "recent_files": [],
            },
            "database": {
                "default_type": "sqlite",
                "sqlite_file": "denso888_data.db",
                "sql_server": {
                    "host": "localhost",
                    "database": "excel_to_db",
                    "username": "sa",
                    "remember_connection": False,
                },
            },
            "processing": {"chunk_size": 5000, "batch_size": 1000, "max_workers": 4},
            "ui": {"theme": "default", "show_tooltips": True, "auto_refresh": True},
            "logging": {
                "level": "INFO",
                "max_log_size": 1000,
                "auto_clear_logs": False,
            },
        }

    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    settings = json.load(f)

                # Merge with defaults to ensure all keys exist
                merged_settings = self._merge_settings(self._default_settings, settings)

                logger.info(f"Settings loaded from {self.settings_file}")
                return merged_settings
            else:
                logger.info("Settings file not found, using defaults")
                return self._default_settings.copy()

        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
            return self._default_settings.copy()

    def save_settings(self, settings: Dict[str, Any]) -> bool:
        """Save settings to file"""
        try:
            # Ensure parent directory exists
            self.settings_file.parent.mkdir(parents=True, exist_ok=True)

            # Write settings
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)

            logger.info(f"Settings saved to {self.settings_file}")
            return True

        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
            return False

    def get_setting(self, key_path: str, default: Any = None) -> Any:
        """Get specific setting using dot notation (e.g., 'database.sql_server.host')"""
        try:
            settings = self.load_settings()
            keys = key_path.split(".")

            value = settings
            for key in keys:
                value = value[key]

            return value

        except (KeyError, TypeError):
            return default

    def set_setting(self, key_path: str, value: Any) -> bool:
        """Set specific setting using dot notation"""
        try:
            settings = self.load_settings()
            keys = key_path.split(".")

            # Navigate to parent dict
            current = settings
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]

            # Set the value
            current[keys[-1]] = value

            return self.save_settings(settings)

        except Exception as e:
            logger.error(f"Failed to set setting {key_path}: {e}")
            return False

    def _merge_settings(
        self, default: Dict[str, Any], user: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Recursively merge user settings with defaults"""
        result = default.copy()

        for key, value in user.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = self._merge_settings(result[key], value)
            else:
                result[key] = value

        return result

    def reset_settings(self) -> bool:
        """Reset settings to defaults"""
        try:
            return self.save_settings(self._default_settings.copy())
        except Exception as e:
            logger.error(f"Failed to reset settings: {e}")
            return False

    def backup_settings(self, backup_file: Optional[str] = None) -> bool:
        """Create backup of current settings"""
        try:
            if not backup_file:
                from datetime import datetime

                timestamp = Path(self.settings_file).stem
                backup_file = (
                    f"{timestamp}_backup_{int(datetime.now().timestamp())}.json"
                )

            backup_path = Path(backup_file)

            if self.settings_file.exists():
                import shutil

                shutil.copy2(self.settings_file, backup_path)
                logger.info(f"Settings backed up to {backup_path}")
                return True
            else:
                logger.warning("No settings file to backup")
                return False

        except Exception as e:
            logger.error(f"Failed to backup settings: {e}")
            return False

    def get_recent_files(self, max_files: int = 10) -> list:
        """Get list of recent Excel files"""
        recent = self.get_setting("data_source.recent_files", [])
        return recent[:max_files]

    def add_recent_file(self, file_path: str, max_files: int = 10) -> bool:
        """Add file to recent files list"""
        try:
            recent = self.get_recent_files(max_files)

            # Remove if already exists
            if file_path in recent:
                recent.remove(file_path)

            # Add to beginning
            recent.insert(0, file_path)

            # Limit list size
            recent = recent[:max_files]

            return self.set_setting("data_source.recent_files", recent)

        except Exception as e:
            logger.error(f"Failed to add recent file: {e}")
            return False

    def clear_recent_files(self) -> bool:
        """Clear recent files list"""
        return self.set_setting("data_source.recent_files", [])
