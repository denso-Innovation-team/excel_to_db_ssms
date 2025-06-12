import pandas as pd
import re
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Iterator
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)


class TypeDetector:
    """Auto-detect column data types"""

    TYPE_PATTERNS = {
        "datetime": ["date", "time", "วันที่", "เวลา", "created", "updated", "timestamp"],
        "integer": ["id", "age", "count", "number", "จำนวน", "อายุ", "qty", "quantity"],
        "float": [
            "price",
            "salary",
            "amount",
            "total",
            "value",
            "ราคา",
            "เงินเดือน",
            "rate",
            "percent",
        ],
        "boolean": ["active", "enabled", "is_", "has_", "flag", "status"],
    }

    @classmethod
    def detect_types(cls, columns: List[str]) -> Dict[str, str]:
        """Detect data types based on column names"""
        type_mapping = {}

        for column in columns:
            col_lower = column.lower()
            column_type = "string"  # default

            for data_type, pattern_list in cls.TYPE_PATTERNS.items():
                if any(pattern in col_lower for pattern in pattern_list):
                    column_type = data_type
                    break

            type_mapping[column] = column_type

        return type_mapping


class DataCleaner:
    """Data cleaning and validation utilities"""

    @staticmethod
    def clean_column_name(name: str) -> str:
        """Clean column names for database compatibility"""
        clean = re.sub(r"[^a-zA-Z0-9_]", "_", str(name))
        return re.sub(r"_+", "_", clean).strip("_").lower()

    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize DataFrame"""
        df_clean = df.copy()

        # Fix column names
        df_clean.columns = [self.clean_column_name(col) for col in df_clean.columns]

        # Remove completely empty rows
        df_clean = df_clean.dropna(how="all")

        # Clean string columns
        for col in df_clean.select_dtypes(include=["object"]).columns:
            df_clean[col] = (
                df_clean[col].astype(str).str.strip().replace(["nan", "None", ""], None)
            )

        return df_clean

    def convert_types(
        self, df: pd.DataFrame, type_mapping: Dict[str, str]
    ) -> pd.DataFrame:
        """Convert DataFrame columns to specified types"""
        df_typed = df.copy()

        for column, target_type in type_mapping.items():
            if column not in df_typed.columns:
                continue

            try:
                if target_type == "integer":
                    # Handle possible NaN values before conversion
                    df_typed[column] = pd.to_numeric(df_typed[column], errors="coerce")
                    df_typed[column] = df_typed[column].fillna(0).astype("Int64")
                elif target_type == "float":
                    # Better float handling with NaN values
                    df_typed[column] = pd.to_numeric(df_typed[column], errors="coerce")
                    df_typed[column] = df_typed[column].fillna(0.0).astype("float64")
                elif target_type == "datetime":
                    # More robust datetime parsing
                    df_typed[column] = pd.to_datetime(
                        df_typed[column],
                        errors="coerce",
                        format=None,  # Attempt to infer format
                        exact=False,  # Allow partial matches
                    )
                elif target_type == "boolean":
                    # Enhanced boolean conversion
                    df_typed[column] = df_typed[column].astype(str).str.lower()
                    df_typed[column] = (
                        df_typed[column]
                        .map(
                            {
                                "true": True,
                                "1": True,
                                "yes": True,
                                "y": True,
                                "false": False,
                                "0": False,
                                "no": False,
                                "n": False,
                            }
                        )
                        .fillna(False)
                    )
            except Exception as e:
                logger.error(f"Type conversion failed for column {column}: {str(e)}")
                # Keep original column data if conversion fails
                continue

        return df_typed


class ExcelReader:
    """Excel file reader with chunking support"""

    def __init__(self, file_path: str, sheet_name: Optional[str] = None):
        self.file_path = Path(file_path)
        self.sheet_name = sheet_name
        self.cleaner = DataCleaner()
        self.type_detector = TypeDetector()

    def validate(self) -> bool:
        """Validate Excel file"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        if self.file_path.suffix.lower() not in [".xlsx", ".xls"]:
            raise ValueError("Must be Excel format (.xlsx or .xls)")
        return True

    def get_file_info(self) -> Dict[str, Any]:
        """Get Excel file information"""
        self.validate()

        with pd.ExcelFile(self.file_path) as excel_file:
            sheets = excel_file.sheet_names
            target_sheet = self.sheet_name or sheets[0]

            # Quick sample for columns and preview
            df_sample = pd.read_excel(excel_file, sheet_name=target_sheet, nrows=10)

            # Count total rows efficiently
            df_count = pd.read_excel(excel_file, sheet_name=target_sheet, usecols=[0])

            return {
                "file_path": str(self.file_path),
                "file_size_mb": self.file_path.stat().st_size / 1024 / 1024,
                "available_sheets": sheets,
                "target_sheet": target_sheet,
                "total_rows": len(df_count),
                "total_columns": len(df_sample.columns),
                "columns": df_sample.columns.tolist(),
                "sample_data": df_sample.head(5),
                "modified_date": datetime.fromtimestamp(self.file_path.stat().st_mtime),
            }

    def get_sheet_names(self) -> List[str]:
        """Get available sheet names"""
        self.validate()
        with pd.ExcelFile(self.file_path) as excel_file:
            return [str(name) for name in excel_file.sheet_names]

    def read_chunks(self, chunk_size: int = 5000) -> Iterator[pd.DataFrame]:
        """Read Excel file in chunks"""
        self.validate()

        target_sheet = self.sheet_name or 0
        df_full = pd.read_excel(self.file_path, sheet_name=target_sheet)

        for start in range(0, len(df_full), chunk_size):
            end = min(start + chunk_size, len(df_full))
            chunk = df_full.iloc[start:end].copy()
            if not chunk.empty:
                yield chunk.to_frame() if isinstance(chunk, pd.Series) else chunk

    def read_with_processing(self, chunk_size: int = 5000) -> Iterator[Dict[str, Any]]:
        """Read Excel with automatic cleaning and type detection"""
        file_info = self.get_file_info()
        type_mapping = self.type_detector.detect_types(file_info["columns"])

        for i, chunk in enumerate(self.read_chunks(chunk_size)):
            # Clean and type convert
            df_clean = self.cleaner.clean_dataframe(chunk)
            df_typed = self.cleaner.convert_types(df_clean, type_mapping)

            yield {
                "chunk_number": i + 1,
                "dataframe": df_typed,
                "rows_count": len(df_typed),
                "type_mapping": type_mapping if i == 0 else None,
                "file_info": file_info if i == 0 else None,
            }


class ExcelHandler:
    """Main Excel handling facade"""

    def __init__(self):
        self.reader: Optional[ExcelReader] = None
        self.current_file_info: Optional[Dict[str, Any]] = None

    def load_file(
        self, file_path: str, sheet_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Load Excel file and return basic info"""
        self.reader = ExcelReader(file_path, sheet_name)
        self.current_file_info = self.reader.get_file_info()
        return self.current_file_info

    def get_sheets(self, file_path: str) -> List[str]:
        """Get available sheet names"""
        reader = ExcelReader(file_path)
        return reader.get_sheet_names()

    def preview_data(self, rows: int = 10) -> Optional[pd.DataFrame]:
        """Get preview of loaded data"""
        if not self.current_file_info:
            return None
        return self.current_file_info["sample_data"].head(rows)

    def process_file(self, chunk_size: int = 5000) -> Iterator[Dict[str, Any]]:
        """Process loaded file in chunks"""
        if not self.reader:
            raise ValueError("No file loaded. Call load_file() first.")

        return self.reader.read_with_processing(chunk_size)

    def validate_file(self, file_path: str, max_size_mb: int = 100) -> Dict[str, Any]:
        """Validate Excel file for processing"""
        try:
            reader = ExcelReader(file_path)
            info = reader.get_file_info()

            validation_result = {
                "valid": True,
                "errors": [],
                "warnings": [],
                "info": info,
            }

            # Size check
            if info["file_size_mb"] > max_size_mb:
                validation_result["warnings"].append(
                    f"File size ({info['file_size_mb']:.1f}MB) exceeds recommended limit ({max_size_mb}MB)"
                )

            # Row count check
            if info["total_rows"] > 100000:
                validation_result["warnings"].append(
                    f"Large file ({info['total_rows']:,} rows) may take longer to process"
                )

            # Column check
            if info["total_columns"] > 50:
                validation_result["warnings"].append(
                    f"Many columns ({info['total_columns']}) detected"
                )

            return validation_result

        except Exception as e:
            return {"valid": False, "errors": [str(e)], "warnings": [], "info": None}
