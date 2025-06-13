"""Environment setup utilities"""

import os
from pathlib import Path


def ensure_environment():
    """Ensure application environment is ready"""
    # Create required directories
    required_dirs = ["logs", "assets/icons", "assets/samples"]

    for dir_name in required_dirs:
        Path(dir_name).mkdir(parents=True, exist_ok=True)

    print("✅ Environment ready")
