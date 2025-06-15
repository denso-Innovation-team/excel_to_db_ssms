try:
    from .gaming_theme import gaming_theme, GamingTheme

    __all__ = ["gaming_theme", "GamingTheme"]
except ImportError as e:
    print(f"Warning: Could not import gaming theme: {e}")
    __all__ = []
