"""
utils/config_manager.py
Configuration Management
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """Manage application configuration"""

    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        self._cache = {}

    def load_json(self, filename: str) -> Dict[str, Any]:
        """Load JSON configuration"""
        config_path = self.config_dir / filename

        if filename in self._cache:
            return self._cache[filename]

        try:
            if config_path.exists():
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                self._cache[filename] = config
                return config
        except Exception as e:
            print(f"Error loading {filename}: {e}")

        return {}

    def save_json(self, filename: str, data: Dict[str, Any]) -> bool:
        """Save JSON configuration"""
        config_path = self.config_dir / filename

        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self._cache[filename] = data
            return True
        except Exception as e:
            print(f"Error saving {filename}: {e}")
            return False

    def load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load YAML configuration"""
        config_path = self.config_dir / filename

        try:
            if config_path.exists():
                with open(config_path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error loading {filename}: {e}")

        return {}

    def get(self, filename: str, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        config = self.load_json(filename)
        return config.get(key, default)

    def set(self, filename: str, key: str, value: Any) -> bool:
        """Set configuration value"""
        config = self.load_json(filename)
        config[key] = value
        return self.save_json(filename, config)

    def clear_cache(self):
        """Clear configuration cache"""
        self._cache.clear()


# Global config manager
config_manager = ConfigManager()
