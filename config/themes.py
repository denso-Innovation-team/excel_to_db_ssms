"""Theme management"""

THEMES = {
    "denso_corporate": {
        "primary": "#DC0003",
        "secondary": "#2C3E50",
        "background": "#FFFFFF",
        "surface": "#F8F9FA"
    },
    "dark_mode": {
        "primary": "#6366F1", 
        "secondary": "#1F2937",
        "background": "#111827",
        "surface": "#1F2937"
    }
}

def get_theme(name: str = "denso_corporate") -> dict:
    """Get theme colors"""
    return THEMES.get(name, THEMES["denso_corporate"])
