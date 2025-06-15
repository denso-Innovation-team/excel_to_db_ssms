"""
utils/file_utils.py
File Management Utilities
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import shutil


class FileManager:
    """Enhanced file management utilities"""

    @staticmethod
    def ensure_directory(path: str) -> bool:
        """Create directory if not exists"""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False

    @staticmethod
    def get_safe_filename(filename: str) -> str:
        """Convert filename to safe format"""
        import re

        # Remove unsafe characters
        safe_name = re.sub(r'[<>:"/\\|?*]', "_", filename)
        # Limit length
        return safe_name[:200]

    @staticmethod
    def backup_file(file_path: str, backup_dir: str = "backups") -> Optional[str]:
        """Create backup of file"""
        try:
            FileManager.ensure_directory(backup_dir)

            file_path = Path(file_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
            backup_path = Path(backup_dir) / backup_name

            shutil.copy2(file_path, backup_path)
            return str(backup_path)
        except Exception:
            return None

    @staticmethod
    def clean_old_files(directory: str, days: int = 30) -> int:
        """Clean files older than specified days"""
        try:
            directory = Path(directory)
            if not directory.exists():
                return 0

            cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
            cleaned = 0

            for file_path in directory.glob("*"):
                if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
                    cleaned += 1

            return cleaned
        except Exception:
            return 0


def validate_file_path(file_path: str, extensions: List[str] = None) -> bool:
    """Validate file path and extension"""
    try:
        path = Path(file_path)
        if not path.exists():
            return False

        if extensions:
            return path.suffix.lower() in [ext.lower() for ext in extensions]

        return True
    except Exception:
        return False


def get_file_info(file_path: str) -> Dict[str, Any]:
    """Get comprehensive file information"""
    try:
        path = Path(file_path)
        if not path.exists():
            return {"error": "File not found"}

        stat = path.stat()
        return {
            "name": path.name,
            "size": stat.st_size,
            "size_mb": round(stat.st_size / (1024 * 1024), 2),
            "modified": datetime.fromtimestamp(stat.st_mtime),
            "extension": path.suffix,
            "is_file": path.is_file(),
            "absolute_path": str(path.absolute()),
        }
    except Exception as e:
        return {"error": str(e)}
