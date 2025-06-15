try:
    from .app_controller import AppController

    __all__ = ["AppController"]
except ImportError as e:
    print(f"Warning: Could not import app controller: {e}")
    __all__ = []
