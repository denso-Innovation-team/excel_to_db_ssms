"""
models/user_preferences.py
User Preferences Model
"""

from dataclasses import dataclass
from typing import List
import json
from pathlib import Path


@dataclass
class UserPreferences:
    """User preferences and settings"""

    # UI Preferences
    theme: str = "denso"
    language: str = "th"

    # Recent Files
    recent_files: List[str] = None
    max_recent_files: int = 10

    def __post_init__(self):
        """Initialize default values"""
        if self.recent_files is None:
            self.recent_files = []

    @classmethod
    def load_from_file(
        cls, prefs_path: str = "config/preferences.json"
    ) -> "UserPreferences":
        """Load preferences from file"""
        prefs_file = Path(prefs_path)
        if prefs_file.exists():
            try:
                with open(prefs_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return cls(**data)
            except Exception:
                pass
        return cls()
