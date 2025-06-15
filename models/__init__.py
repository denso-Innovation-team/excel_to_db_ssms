try:
    from .app_config import AppConfig
    from .database_config import DatabaseConfig
    from .user_preferences import UserPreferences

    __all__ = ["AppConfig", "DatabaseConfig", "UserPreferences"]
except ImportError as e:
    print(f"Warning: Could not import some models: {e}")
    __all__ = []
