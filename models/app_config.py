"""
models/app_config.py
Application Configuration Model
"""

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AppConfig:
    """Main application configuration"""

    # Application Info
    app_name: str = "DENSO888"
    version: str = "2.0.0"
    author: str = "Thammaphon Chittasuwanna (SDM)"
    department: str = "Innovation Department"

    # Window Settings
    window_width: int = 1200
    window_height: int = 800
    window_resizable: bool = True

    # Processing Settings
    batch_size: int = 1000
    max_workers: int = 4
    chunk_size: int = 5000

    # UI Settings
    theme: str = "denso"
    language: str = "th"

    # Paths
    data_dir: str = "data"
    imports_dir: str = "data/imports"
    exports_dir: str = "data/exports"
    assets_dir: str = "assets"

    def __post_init__(self):
        """Validate and setup configuration"""
        self._ensure_directories()

    def _ensure_directories(self):
        """Create required directories"""
        dirs = [self.data_dir, self.imports_dir, self.exports_dir]
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)

    @classmethod
    def load_from_file(cls, config_path: str = "config/settings.json") -> "AppConfig":
        """Load configuration from file"""
        config_file = Path(config_path)
        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return cls(**data)
            except Exception:
                pass
        return cls()
