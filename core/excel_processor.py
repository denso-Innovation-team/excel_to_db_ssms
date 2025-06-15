"""
core/excel_processor.py
Enhanced Excel Processor with Column Mapping Support
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ExcelProcessor:
    """Enhanced Excel Processor"""

    def __init__(self):
        self.supported_extensions = [".xlsx", ".xls", ".xlsm"]

    def validate_file(self, file_path: str) -> Tuple[bool, str]:
        """Validate Excel file"""
        try:
            path = Path(file_path)

            if not path.exists():
                return False, "File does not exist"

            if path.suffix.lower() not in self.supported_extensions:
                return (
                    False,
                    f"Unsupported file type. Supported: {', '.join(self.supported_extensions)}",
                )

            # Try to read file
            df = pd.read_excel(file_path, nrows=1)
            if df.empty:
                return False, "File appears to be empty"

            return True, "File is valid"

        except Exception as e:
            return False, f"File validation failed: {str(e)}"

    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get Excel file information"""
        try:
            # Get basic file info
            path = Path(file_path)
            file_size = path.stat().st_size / (1024 * 1024)  # MB

            # Read Excel file
            df = pd.read_excel(file_path)

            # Get data quality metrics
            data_quality = self._analyze_data_quality(df)

            return {
                "file_name": path.name,
                "file_size_mb": round(file_size, 2),
                "total_rows": len(df),
                "total_columns": len(df.columns),
                "columns": list(df.columns),
                "data_types": {col: str(dtype) for col, dtype in df.dtypes.items()},
                "sample_data": df.head(5).to_dict("records"),
                "data_quality": data_quality,
                "modified_date": datetime.fromtimestamp(path.stat().st_mtime).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            }

        except Exception as e:
            logger.error(f"Failed to get file info: {e}")
            return {"error": str(e)}

    def _analyze_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze data quality"""
        total_cells = len(df) * len(df.columns)
        null_cells = df.isnull().sum().sum()

        return {
            "null_percentage": (
                round((null_cells / total_cells) * 100, 2) if total_cells > 0 else 0
            ),
            "duplicate_rows": df.duplicated().sum(),
            "empty_columns": df.isnull().all().sum(),
            "columns_with_nulls": df.isnull().any().sum(),
        }

    def process_file(
        self,
        file_path: str,
        column_mappings: Optional[Dict[str, str]] = None,
        selected_columns: Optional[List[str]] = None,
    ) -> Tuple[bool, Any]:
        """Process Excel file with optional column mappings and selection"""
        try:
            # Read Excel file
            df = pd.read_excel(file_path)

            # Select specific columns if specified
            if selected_columns:
                missing_cols = [
                    col for col in selected_columns if col not in df.columns
                ]
                if missing_cols:
                    return False, f"Columns not found: {', '.join(missing_cols)}"
                df = df[selected_columns]

            # Apply column mappings if provided
            if column_mappings:
                df = df.rename(columns=column_mappings)

            # Clean data
            df = self._clean_data(df)

            # Convert to list of dictionaries
            data = df.to_dict("records")

            return True, data

        except Exception as e:
            logger.error(f"Failed to process file: {e}")
            return False, str(e)

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean data"""
        # Remove completely empty rows
        df = df.dropna(how="all")

        # Clean column names
        df.columns = [self._clean_column_name(col) for col in df.columns]

        # Fill NaN values
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].fillna("")
            else:
                df[col] = df[col].fillna(0)

        return df

    def _clean_column_name(self, name: str) -> str:
        """Clean column name"""
        import re

        # Convert to string and strip
        clean_name = str(name).strip()

        # Replace special characters with underscore
        clean_name = re.sub(r"[^\w\s]", "_", clean_name)

        # Replace spaces with underscore
        clean_name = re.sub(r"\s+", "_", clean_name)

        # Remove multiple underscores
        clean_name = re.sub(r"_+", "_", clean_name)

        # Remove leading/trailing underscores
        clean_name = clean_name.strip("_")

        # Ensure not empty
        if not clean_name:
            clean_name = "column"

        return clean_name

    def get_sheet_names(self, file_path: str) -> List[str]:
        """Get Excel sheet names"""
        try:
            excel_file = pd.ExcelFile(file_path)
            return excel_file.sheet_names
        except Exception as e:
            logger.error(f"Failed to get sheet names: {e}")
            return []

    def preview_data(self, file_path: str, rows: int = 10) -> Tuple[bool, Any]:
        """Preview Excel data"""
        try:
            df = pd.read_excel(file_path, nrows=rows)
            return True, df.to_dict("records")
        except Exception as e:
            logger.error(f"Failed to preview data: {e}")
            return False, str(e)
