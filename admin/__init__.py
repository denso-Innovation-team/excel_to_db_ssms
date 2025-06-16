import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from .user_tracker import UserActivityTracker

    __all__ = ["UserActivityTracker"]
except ImportError:
    __all__ = []
