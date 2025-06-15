"""
models/app_config.py
Fixed Application Configuration Model
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
    theme: str = "gaming"
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
            try:
                Path(dir_path).mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"Warning: Could not create directory {dir_path}: {e}")

    @classmethod
    def load_from_file(cls, config_path: str = "config/settings.json") -> "AppConfig":
        """Load configuration from file"""
        config_file = Path(config_path)
        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Filter only known fields
                known_fields = {
                    field.name for field in cls.__dataclass_fields__.values()
                }
                filtered_data = {k: v for k, v in data.items() if k in known_fields}

                return cls(**filtered_data)
            except Exception as e:
                print(f"Warning: Could not load config from {config_path}: {e}")

        return cls()

    def save_to_file(self, config_path: str = "config/settings.json"):
        """Save configuration to file"""
        config_file = Path(config_path)
        try:
            # Ensure config directory exists
            config_file.parent.mkdir(parents=True, exist_ok=True)

            # Convert to dictionary and save
            data = {
                "app_name": self.app_name,
                "version": self.version,
                "author": self.author,
                "department": self.department,
                "window_width": self.window_width,
                "window_height": self.window_height,
                "window_resizable": self.window_resizable,
                "batch_size": self.batch_size,
                "max_workers": self.max_workers,
                "chunk_size": self.chunk_size,
                "theme": self.theme,
                "language": self.language,
                "data_dir": self.data_dir,
                "imports_dir": self.imports_dir,
                "exports_dir": self.exports_dir,
                "assets_dir": self.assets_dir,
            }

            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            print(f"Warning: Could not save config to {config_path}: {e}")

    def validate(self) -> tuple[bool, list]:
        """Validate configuration"""
        errors = []

        # Validate window dimensions
        if self.window_width < 800:
            errors.append("Window width must be at least 800 pixels")
        if self.window_height < 600:
            errors.append("Window height must be at least 600 pixels")

        # Validate processing settings
        if self.batch_size < 100:
            errors.append("Batch size must be at least 100")
        if self.max_workers < 1:
            errors.append("Max workers must be at least 1")
        if self.chunk_size < 1000:
            errors.append("Chunk size must be at least 1000")

        # Validate paths
        if not self.data_dir:
            errors.append("Data directory cannot be empty")

        return len(errors) == 0, errors
