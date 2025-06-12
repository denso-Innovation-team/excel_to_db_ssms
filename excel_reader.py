"""Excel file processing"""
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional, Iterator

class ExcelReader:
    def __init__(self, file_path: str, sheet_name: Optional[str] = None):
        self.file_path = Path(file_path)
        self.sheet_name = sheet_name
    
    def validate(self) -> bool:
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        if self.file_path.suffix.lower() not in [".xlsx", ".xls"]:
            raise ValueError("Must be Excel format")
        return True
    
    def get_info(self) -> Dict[str, Any]:
        self.validate()
        
        with pd.ExcelFile(self.file_path) as excel_file:
            sheets = excel_file.sheet_names
            target_sheet = self.sheet_name or sheets[0]
            
            # Quick sample for columns
            df_sample = pd.read_excel(excel_file, sheet_name=target_sheet, nrows=5)
            
            # Count rows efficiently
            df_count = pd.read_excel(excel_file, sheet_name=target_sheet, usecols=[0])
            
            return {
                "target_sheet": target_sheet,
                "total_rows": len(df_count),
                "columns": df_sample.columns.tolist(),
                "file_size_mb": self.file_path.stat().st_size / 1024 / 1024
            }
    
    def read_chunks(self, chunk_size: int = 5000) -> Iterator[pd.DataFrame]:
        self.validate()
        
        target_sheet = self.sheet_name or 0
        df_full = pd.read_excel(self.file_path, sheet_name=target_sheet)
        
        for start in range(0, len(df_full), chunk_size):
            end = min(start + chunk_size, len(df_full))
            chunk = df_full.iloc[start:end].copy()
            if not chunk.empty:
                yield chunk
