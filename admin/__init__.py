try:
    from .user_tracker import UserActivityTracker

    __all__ = ["UserActivityTracker"]
except ImportError:
    __all__ = []
