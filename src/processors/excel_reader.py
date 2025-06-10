# src/processors/excel_reader.py - Fixed version
import pandas as pd
from typing import Iterator, Dict, Any, Optional
from pathlib import Path
import logging
import math

logger = logging.getLogger(__name__)


class ExcelReader:
    def __init__(self, file_path: str, sheet_name: Optional[str] = None):
        self.file_path = Path(file_path)
        self.sheet_name = sheet_name
        self.total_rows = 0

    def validate_file(self) -> bool:
        """Validate Excel file"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        if self.file_path.suffix.lower() not in [".xlsx", ".xls"]:
            raise ValueError("File must be Excel format (.xlsx or .xls)")
        return True

    def get_sheet_info(self) -> Dict[str, Any]:
        """Get Excel file information"""
        self.validate_file()

        with pd.ExcelFile(self.file_path) as excel_file:
            sheets = excel_file.sheet_names
            target_sheet = self.sheet_name or sheets[0]

            # Get columns
            df_sample = pd.read_excel(excel_file, sheet_name=target_sheet, nrows=0)

            # Count total rows
            df_count = pd.read_excel(excel_file, sheet_name=target_sheet, usecols=[0])
            self.total_rows = len(df_count)

            return {
                "sheets": sheets,
                "target_sheet": target_sheet,
                "total_rows": self.total_rows,
                "columns": df_sample.columns.tolist(),
            }

    def read_chunks(self, chunk_size: int = 1000) -> Iterator[pd.DataFrame]:
        """Read Excel file in chunks (manual implementation)"""
        self.validate_file()

        try:
            target_sheet = self.sheet_name or 0

            # Get total rows first
            if self.total_rows == 0:
                self.get_sheet_info()

            # Manual chunking - read skiprows/nrows
            for start_row in range(0, self.total_rows, chunk_size):
                if start_row == 0:
                    # First chunk - include headers
                    chunk = pd.read_excel(
                        self.file_path,
                        sheet_name=target_sheet,
                        skiprows=0,
                        nrows=chunk_size,
                        dtype=str,
                        na_filter=False,
                    )
                else:
                    # Skip headers for subsequent chunks
                    chunk = pd.read_excel(
                        self.file_path,
                        sheet_name=target_sheet,
                        skiprows=start_row + 1,  # +1 to skip header
                        nrows=chunk_size,
                        header=None,  # No header in subsequent chunks
                        dtype=str,
                        na_filter=False,
                    )

                    # Get column names from first chunk
                    first_chunk = pd.read_excel(
                        self.file_path, sheet_name=target_sheet, nrows=0
                    )
                    chunk.columns = first_chunk.columns

                if not chunk.empty:
                    yield chunk

        except Exception as e:
            logger.error(f"Error reading Excel file {self.file_path}: {e}")
            raise
