"""
config/settings.py
Application settings management
"""

import json
from pathlib import Path
from dataclasses import dataclass, asdict

@dataclass
class AppSettings:
    app_name: str = "DENSO888"
    version: str = "2.0.0"
    theme: str = "denso"
    language: str = "th"
    window_width: int = 1200
    window_height: int = 800
    batch_size: int = 1000
    max_workers: int = 4

    @classmethod
    def load(cls, config_path: str = "config/settings.json"):
        """Load settings from file"""
        path = Path(config_path)
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return cls(**data)
        return cls()
    
    def save(self, config_path: str = "config/settings.json"):
        """Save settings to file"""
        path = Path(config_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(asdict(self), f, indent=2, ensure_ascii=False)
