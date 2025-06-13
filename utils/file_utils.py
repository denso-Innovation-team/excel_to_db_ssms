"""File utilities for DENSO888"""
from pathlib import Path
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class FileUtils:
    """File operation utilities"""
    
    @staticmethod
    def get_excel_files(directory: str) -> List[Path]:
        """Get Excel files in directory"""
        try:
            path = Path(directory)
            if not path.exists():
                return []
            
            excel_files = []
            for ext in [".xlsx", ".xls", ".xlsm"]:
                excel_files.extend(path.glob(f"*{ext}"))
            
            return sorted(excel_files, key=lambda x: x.stat().st_mtime, reverse=True)
        except Exception as e:
            logger.error(f"Error getting Excel files: {e}")
            return []
    
    @staticmethod
    def ensure_directory(directory: str) -> Path:
        """Ensure directory exists"""
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @staticmethod
    def get_file_info(file_path: Path) -> Dict[str, Any]:
        """Get file information"""
        try:
            if not file_path.exists():
                return {"error": "File not found"}
            
            stat = file_path.stat()
            return {
                "name": file_path.name,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "modified": stat.st_mtime,
                "exists": True
            }
        except Exception as e:
            return {"error": str(e)}
