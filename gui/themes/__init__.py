import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from .modern_theme import modern_theme, ModernTheme

    __all__ = ["modern_theme", "ModernTheme"]
except ImportError as e:
    print(f"Warning: Could not import modern theme: {e}")
    __all__ = []
