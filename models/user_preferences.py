"""
models/user_preferences.py
Fixed User Preferences Model
"""

from dataclasses import dataclass, field
from typing import List, Optional
import json
from pathlib import Path


@dataclass
class UserPreferences:
    """User preferences and settings"""

    # UI Preferences
    theme: str = "gaming"
    language: str = "th"

    # Recent Files
    recent_files: List[str] = field(default_factory=list)
    max_recent_files: int = 10

    # Gaming preferences
    achievements_unlocked: List[str] = field(default_factory=list)
    show_animations: bool = True
    sound_effects: bool = True

    # Window preferences
    last_window_state: Optional[str] = None
    last_page: str = "dashboard"

    def add_recent_file(self, file_path: str):
        """Add file to recent files list"""
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)

        self.recent_files.insert(0, file_path)

        # Keep only max_recent_files
        if len(self.recent_files) > self.max_recent_files:
            self.recent_files = self.recent_files[: self.max_recent_files]

    def unlock_achievement(self, achievement_id: str):
        """Unlock an achievement"""
        if achievement_id not in self.achievements_unlocked:
            self.achievements_unlocked.append(achievement_id)

    def is_achievement_unlocked(self, achievement_id: str) -> bool:
        """Check if achievement is unlocked"""
        return achievement_id in self.achievements_unlocked

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

                # Filter only known fields
                known_fields = {
                    field.name for field in cls.__dataclass_fields__.values()
                }
                filtered_data = {k: v for k, v in data.items() if k in known_fields}

                return cls(**filtered_data)
            except Exception as e:
                print(f"Warning: Could not load preferences from {prefs_path}: {e}")

        return cls()

    def save_to_file(self, prefs_path: str = "config/preferences.json"):
        """Save preferences to file"""
        prefs_file = Path(prefs_path)
        try:
            # Ensure config directory exists
            prefs_file.parent.mkdir(parents=True, exist_ok=True)

            # Convert to dictionary and save
            data = {
                "theme": self.theme,
                "language": self.language,
                "recent_files": self.recent_files,
                "max_recent_files": self.max_recent_files,
                "achievements_unlocked": self.achievements_unlocked,
                "show_animations": self.show_animations,
                "sound_effects": self.sound_effects,
                "last_window_state": self.last_window_state,
                "last_page": self.last_page,
            }

            with open(prefs_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            print(f"Warning: Could not save preferences to {prefs_path}: {e}")

    def clear_recent_files(self):
        """Clear recent files list"""
        self.recent_files.clear()

    def reset_to_defaults(self):
        """Reset preferences to default values"""
        self.theme = "gaming"
        self.language = "th"
        self.recent_files.clear()
        self.max_recent_files = 10
        self.achievements_unlocked.clear()
        self.show_animations = True
        self.sound_effects = True
        self.last_window_state = None
        self.last_page = "dashboard"
