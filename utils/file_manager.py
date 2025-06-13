"""File management utilities"""

from pathlib import Path
from typing import List

class FileManager:
    """Simple file management"""
    
    @staticmethod
    def get_excel_files(directory: str) -> List[Path]:
        """Get Excel files from directory"""
        path = Path(directory)
        if not path.exists():
            return []
            
        excel_files = []
        for ext in [".xlsx", ".xls", ".xlsm"]:
            excel_files.extend(path.glob(f"*{ext}"))
            
        return sorted(excel_files)
    
    @staticmethod
    def ensure_directory(directory: str) -> Path:
        """Ensure directory exists"""
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        return path
