import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from .app_controller import AppController

    __all__ = ["AppController"]
except ImportError as e:
    print(f"Warning: Could not import app controller: {e}")
    __all__ = []
