"""Enhanced Excel handler with robust error handling and performance optimization"""

import pandas as pd
import re
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Iterator, Union
from datetime import datetime
import warnings

# Suppress pandas warnings for cleaner output
warnings.filterwarnings("ignore", category=UserWarning)

logger = logging.getLogger(__name__)


class TypeDetector:
    """Enhanced auto-detection of column data types"""

    TYPE_PATTERNS = {
        "datetime": {
            "keywords": [
                "date",
                "time",
                "วันที่",
                "เวลา",
                "created",
                "updated",
                "timestamp",
                "born",
                "expire",
            ],
            "patterns": [
                r"\d{4}-\d{2}-\d{2}",
                r"\d{2}/\d{2}/\d{4}",
                r"\d{2}-\d{2}-\d{4}",
            ],
        },
        "integer": {
            "keywords": [
                "id",
                "age",
                "count",
                "number",
                "จำนวน",
                "อายุ",
                "qty",
                "quantity",
                "year",
                "rank",
            ],
            "patterns": [r"^\d+$"],
        },
        "float": {
            "keywords": [
                "price",
                "salary",
                "amount",
                "total",
                "value",
                "ราคา",
                "เงินเดือน",
                "rate",
                "percent",
                "score",
            ],
            "patterns": [r"^\d+\.\d+$", r"^\d+,\d+\.\d+$"],
        },
        "boolean": {
            "keywords": [
                "active",
                "enabled",
                "is_",
                "has_",
                "flag",
                "status",
                "valid",
                "confirmed",
            ],
            "patterns": [r"^(true|false|yes|no|y|n|1|0)$"],
        },
        "email": {
            "keywords": ["email", "mail", "อีเมล"],
            "patterns": [r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"],
        },
        "phone": {
            "keywords": ["phone", "tel", "mobile", "โทร", "มือถือ"],
            "patterns": [r"^\+?[\d\-\(\)\s]+$"],
        },
    }

    @classmethod
    def detect_types(
        cls, columns: List[str], sample_data: Optional[pd.DataFrame] = None
    ) -> Dict[str, str]:
        """Enhanced type detection with sample data analysis"""
        type_mapping = {}

        for column in columns:
            col_lower = column.lower().strip()
            detected_type = "string"  # default

            # Pattern-based detection
            for data_type, type_info in cls.TYPE_PATTERNS.items():
                # Check keywords
                if any(keyword in col_lower for keyword in type_info["keywords"]):
                    detected_type = data_type
                    break

            # Sample data analysis if provided
            if sample_data is not None and column in sample_data.columns:
                sample_type = cls._analyze_sample_data(sample_data[column])
                if sample_type != "string":
                    detected_type = sample_type

            type_mapping[column] = detected_type

        return type_mapping

    @classmethod
    def _analyze_sample_data(cls, series: pd.Series) -> str:
        """Analyze sample data to determine type"""
        # Remove null values for analysis
        clean_series = series.dropna().astype(str)

        if len(clean_series) == 0:
            return "string"

        # Check for numeric patterns
        try:
            pd.to_numeric(clean_series)
            # Check if all values are integers
            if clean_series.str.match(r"^\d+$").all():
                return "integer"
            else:
                return "float"
        except (ValueError, TypeError):
            pass

        # Check for date patterns
        try:
            pd.to_datetime(clean_series.head(10))
            return "datetime"
        except (ValueError, TypeError):
            pass

        # Check for boolean patterns
        bool_values = {"true", "false", "yes", "no", "y", "n", "1", "0"}
        if clean_series.str.lower().isin(bool_values).all():
            return "boolean"

        # Check for email pattern
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if clean_series.str.match(email_pattern).any():
            return "email"

        return "string"


class DataCleaner:
    """Enhanced data cleaning with configurable options"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Default cleaning configuration"""
        return {
            "clean_column_names": True,
            "remove_empty_rows": True,
            "trim_strings": True,
            "standardize_nulls": True,
            "remove_duplicates": False,
            "max_string_length": 1000,
            "date_formats": ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y"],
            "decimal_separator": ".",
            "thousand_separator": ",",
        }

    def clean_column_name(self, name: str) -> str:
        """Enhanced column name cleaning"""
        if not self.config["clean_column_names"]:
            return name

        # Convert to string and handle None
        clean_name = str(name).strip()

        # Remove special characters and replace with underscore
        clean_name = re.sub(r"[^\w\s]", "_", clean_name)

        # Replace spaces and multiple underscores
        clean_name = re.sub(r"\s+", "_", clean_name)
        clean_name = re.sub(r"_+", "_", clean_name)

        # Remove leading/trailing underscores
        clean_name = clean_name.strip("_")

        # Convert to lowercase
        clean_name = clean_name.lower()

        # Ensure not empty
        if not clean_name:
            clean_name = "column"

        # Handle reserved keywords
        reserved_words = {"index", "level", "values", "items"}
        if clean_name in reserved_words:
            clean_name = f"{clean_name}_col"

        return clean_name

    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Enhanced DataFrame cleaning"""
        df_clean = df.copy()

        # Clean column names
        if self.config["clean_column_names"]:
            df_clean.columns = [self.clean_column_name(col) for col in df_clean.columns]

        # Remove completely empty rows
        if self.config["remove_empty_rows"]:
            df_clean = df_clean.dropna(how="all")

        # Clean string columns
        if self.config["trim_strings"]:
            string_columns = df_clean.select_dtypes(include=["object"]).columns
            for col in string_columns:
                df_clean[col] = df_clean[col].astype(str).str.strip()

                # Limit string length
                max_length = self.config["max_string_length"]
                df_clean[col] = df_clean[col].str[:max_length]

        # Standardize null values
        if self.config["standardize_nulls"]:
            null_values = [
                "",
                "NULL",
                "null",
                "None",
                "none",
                "N/A",
                "n/a",
                "#N/A",
                "nan",
                "NaN",
            ]
            df_clean = df_clean.replace(null_values, None)

        # Remove duplicates
        if self.config["remove_duplicates"]:
            df_clean = df_clean.drop_duplicates()

        return df_clean

    def convert_types(
        self, df: pd.DataFrame, type_mapping: Dict[str, str]
    ) -> pd.DataFrame:
        """Enhanced type conversion with error handling"""
        df_typed = df.copy()

        for column, target_type in type_mapping.items():
            if column not in df_typed.columns:
                logger.warning(f"Column '{column}' not found in DataFrame")
                continue

            try:
                if target_type == "integer":
                    df_typed[column] = self._convert_to_integer(df_typed[column])
                elif target_type == "float":
                    df_typed[column] = self._convert_to_float(df_typed[column])
                elif target_type == "datetime":
                    df_typed[column] = self._convert_to_datetime(df_typed[column])
                elif target_type == "boolean":
                    df_typed[column] = self._convert_to_boolean(df_typed[column])
                elif target_type == "email":
                    df_typed[column] = self._clean_email(df_typed[column])
                elif target_type == "phone":
                    df_typed[column] = self._clean_phone(df_typed[column])

            except Exception as e:
                logger.error(
                    f"Type conversion failed for column '{column}' to {target_type}: {e}"
                )
                continue

        return df_typed

    def _convert_to_integer(self, series: pd.Series) -> pd.Series:
        """Convert to integer with enhanced handling"""
        # Clean numeric strings
        clean_series = series.astype(str).str.replace(
            self.config["thousand_separator"], ""
        )
        clean_series = clean_series.str.replace(r"[^\d.-]", "", regex=True)

        # Convert to numeric first, then to Int64 (nullable integer)
        numeric_series = pd.to_numeric(clean_series, errors="coerce")
        return numeric_series.fillna(0).astype("Int64")

    def _convert_to_float(self, series: pd.Series) -> pd.Series:
        """Convert to float with enhanced handling"""
        # Handle different decimal separators
        clean_series = series.astype(str)

        # Replace decimal separator if needed
        if self.config["decimal_separator"] != ".":
            clean_series = clean_series.str.replace(
                self.config["decimal_separator"], "."
            )

        # Remove thousand separators
        clean_series = clean_series.str.replace(self.config["thousand_separator"], "")

        # Remove non-numeric characters except decimal point and minus
        clean_series = clean_series.str.replace(r"[^\d.-]", "", regex=True)

        return pd.to_numeric(clean_series, errors="coerce").fillna(0.0)

    def _convert_to_datetime(self, series: pd.Series) -> pd.Series:
        """Convert to datetime with multiple format support"""
        # Try multiple datetime formats
        for date_format in self.config["date_formats"]:
            try:
                return pd.to_datetime(series, format=date_format, errors="coerce")
            except (ValueError, TypeError):
                continue

        # Fallback to pandas auto-detection
        return pd.to_datetime(series, errors="coerce", dayfirst=True)

    def _convert_to_boolean(self, series: pd.Series) -> pd.Series:
        """Convert to boolean with enhanced mapping"""
        bool_mapping = {
            "true": True,
            "1": True,
            "yes": True,
            "y": True,
            "on": True,
            "active": True,
            "false": False,
            "0": False,
            "no": False,
            "n": False,
            "off": False,
            "inactive": False,
        }

        clean_series = series.astype(str).str.lower().str.strip()
        return clean_series.map(bool_mapping).fillna(False)

    def _clean_email(self, series: pd.Series) -> pd.Series:
        """Clean and validate email addresses"""
        clean_series = series.astype(str).str.lower().str.strip()

        # Basic email validation pattern
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        def validate_email(email):
            if pd.isna(email) or email == "nan":
                return None
            return email if re.match(email_pattern, email) else None

        return clean_series.apply(validate_email)

    def _clean_phone(self, series: pd.Series) -> pd.Series:
        """Clean phone numbers"""

        def clean_phone_number(phone):
            if pd.isna(phone) or phone == "nan":
                return None

            # Remove all non-digit characters except + at the beginning
            clean_phone = re.sub(r"[^\d+]", "", str(phone))

            # Ensure + is only at the beginning
            if clean_phone.startswith("+"):
                clean_phone = "+" + re.sub(r"[^\d]", "", clean_phone[1:])
            else:
                clean_phone = re.sub(r"[^\d]", "", clean_phone)

            return clean_phone if len(clean_phone) >= 7 else None

        return series.apply(clean_phone_number)


class ExcelReader:
    """Enhanced Excel reader with chunking and error recovery"""

    def __init__(
        self,
        file_path: Union[str, Path],
        sheet_name: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        self.file_path = Path(file_path)
        self.sheet_name = sheet_name
        self.config = config or self._get_default_config()
        self.cleaner = DataCleaner(self.config.get("cleaning", {}))
        self.type_detector = TypeDetector()

    def _get_default_config(self) -> Dict[str, Any]:
        """Default reader configuration"""
        return {
            "max_file_size_mb": 100,
            "sample_rows": 1000,
            "skip_rows": 0,
            "use_header": True,
            "engine": "openpyxl",
            "cleaning": {},
            "type_detection": True,
        }

    def validate(self) -> Dict[str, Any]:
        """Enhanced file validation"""
        validation_result = {"valid": True, "errors": [], "warnings": []}

        # Check file existence
        if not self.file_path.exists():
            validation_result["valid"] = False
            validation_result["errors"].append(f"File not found: {self.file_path}")
            return validation_result

        # Check file extension
        valid_extensions = [".xlsx", ".xls", ".xlsm", ".xlsb"]
        if self.file_path.suffix.lower() not in valid_extensions:
            validation_result["valid"] = False
            validation_result["errors"].append(
                f"Invalid file type. Must be: {', '.join(valid_extensions)}"
            )
            return validation_result

        # Check file size
        file_size_mb = self.file_path.stat().st_size / (1024 * 1024)
        max_size = self.config["max_file_size_mb"]

        if file_size_mb > max_size:
            validation_result["warnings"].append(
                f"Large file ({file_size_mb:.1f}MB > {max_size}MB)"
            )

        # Check file accessibility
        try:
            with pd.ExcelFile(
                self.file_path, engine=self.config["engine"]
            ) as excel_file:
                if not excel_file.sheet_names:
                    validation_result["valid"] = False
                    validation_result["errors"].append("No sheets found in Excel file")
        except Exception as e:
            validation_result["valid"] = False
            validation_result["errors"].append(f"Cannot read Excel file: {str(e)}")

        return validation_result

    def get_file_info(self) -> Dict[str, Any]:
        """Enhanced file information"""
        validation = self.validate()
        if not validation["valid"]:
            return {"error": validation["errors"][0]}

        try:
            with pd.ExcelFile(
                self.file_path, engine=self.config["engine"]
            ) as excel_file:
                sheets = excel_file.sheet_names
                target_sheet = self.sheet_name or sheets[0]

                # Sample data for analysis
                sample_df = pd.read_excel(
                    excel_file,
                    sheet_name=target_sheet,
                    nrows=self.config["sample_rows"],
                    skiprows=self.config["skip_rows"],
                    header=0 if self.config["use_header"] else None,
                )

                # Full row count (efficient method)
                full_df = pd.read_excel(
                    excel_file, sheet_name=target_sheet, usecols=[0]
                )
                total_rows = len(full_df)

                # Type detection
                type_mapping = {}
                if self.config["type_detection"]:
                    type_mapping = self.type_detector.detect_types(
                        sample_df.columns.tolist(), sample_df
                    )

                return {
                    "file_path": str(self.file_path),
                    "file_size_mb": self.file_path.stat().st_size / (1024 * 1024),
                    "available_sheets": sheets,
                    "target_sheet": target_sheet,
                    "total_rows": total_rows,
                    "total_columns": len(sample_df.columns),
                    "columns": sample_df.columns.tolist(),
                    "sample_data": sample_df.head(5),
                    "type_mapping": type_mapping,
                    "data_quality": self._analyze_data_quality(sample_df),
                    "modified_date": datetime.fromtimestamp(
                        self.file_path.stat().st_mtime
                    ),
                    "validation": validation,
                }

        except Exception as e:
            logger.error(f"Error getting file info: {e}")
            return {"error": str(e)}

    def _analyze_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze data quality metrics"""
        return {
            "null_percentage": (
                df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100
            ),
            "duplicate_rows": df.duplicated().sum(),
            "empty_columns": df.isnull().all().sum(),
            "mixed_types": self._detect_mixed_types(df),
            "outliers": self._detect_outliers(df),
        }

    def _detect_mixed_types(self, df: pd.DataFrame) -> List[str]:
        """Detect columns with mixed data types"""
        mixed_type_columns = []

        for col in df.columns:
            if df[col].dtype == "object":
                # Check if column has mixed numeric and string data
                non_null_data = df[col].dropna()
                if len(non_null_data) > 0:
                    try:
                        pd.to_numeric(non_null_data)
                    except (ValueError, TypeError):
                        # Check if partially numeric
                        numeric_count = 0
                        for value in non_null_data:
                            try:
                                float(str(value))
                                numeric_count += 1
                            except (ValueError, TypeError):
                                pass

                        if 0 < numeric_count < len(non_null_data):
                            mixed_type_columns.append(col)

        return mixed_type_columns

    def _detect_outliers(self, df: pd.DataFrame) -> Dict[str, int]:
        """Detect potential outliers in numeric columns"""
        outliers = {}

        numeric_columns = df.select_dtypes(include=["number"]).columns
        for col in numeric_columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1

            outlier_count = (
                (df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))
            ).sum()
            if outlier_count > 0:
                outliers[col] = outlier_count

        return outliers

    def get_sheet_names(self) -> List[str]:
        """Get available sheet names"""
        try:
            with pd.ExcelFile(
                self.file_path, engine=self.config["engine"]
            ) as excel_file:
                return excel_file.sheet_names
        except Exception as e:
            logger.error(f"Error getting sheet names: {e}")
            return []

    def read_chunks(self, chunk_size: int = 5000) -> Iterator[pd.DataFrame]:
        """Read Excel file in chunks with error recovery"""
        try:
            target_sheet = self.sheet_name or 0

            # Read full file first (for Excel, chunking requires full read)
            df_full = pd.read_excel(
                self.file_path,
                sheet_name=target_sheet,
                skiprows=self.config["skip_rows"],
                header=0 if self.config["use_header"] else None,
                engine=self.config["engine"],
            )

            # Yield chunks
            for start in range(0, len(df_full), chunk_size):
                end = min(start + chunk_size, len(df_full))
                chunk = df_full.iloc[start:end].copy()

                if not chunk.empty:
                    yield chunk

        except Exception as e:
            logger.error(f"Error reading Excel chunks: {e}")
            raise

    def read_with_processing(self, chunk_size: int = 5000) -> Iterator[Dict[str, Any]]:
        """Read Excel with automatic cleaning and type detection"""
        file_info = self.get_file_info()

        if "error" in file_info:
            raise ValueError(f"Cannot read file: {file_info['error']}")

        type_mapping = file_info.get("type_mapping", {})

        for i, chunk in enumerate(self.read_chunks(chunk_size)):
            try:
                # Clean data
                df_clean = self.cleaner.clean_dataframe(chunk)

                # Convert types
                df_typed = self.cleaner.convert_types(df_clean, type_mapping)

                yield {
                    "chunk_number": i + 1,
                    "dataframe": df_typed,
                    "rows_count": len(df_typed),
                    "type_mapping": type_mapping if i == 0 else None,
                    "file_info": file_info if i == 0 else None,
                    "data_quality": (
                        self._analyze_data_quality(df_typed) if i == 0 else None
                    ),
                }

            except Exception as e:
                logger.error(f"Error processing chunk {i + 1}: {e}")
                # Skip problematic chunk and continue
                continue


class ExcelHandler:
    """Main Excel handling facade with enhanced features"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._get_default_config()
        self.reader: Optional[ExcelReader] = None
        self.current_file_info: Optional[Dict[str, Any]] = None

    def _get_default_config(self) -> Dict[str, Any]:
        """Default handler configuration"""
        return {
            "reader": {
                "max_file_size_mb": 100,
                "sample_rows": 1000,
                "engine": "openpyxl",
            },
            "cleaning": {
                "clean_column_names": True,
                "remove_empty_rows": True,
                "trim_strings": True,
            },
            "validation": {
                "max_file_size_mb": 100,
                "allowed_extensions": [".xlsx", ".xls", ".xlsm"],
            },
        }

    def load_file(
        self, file_path: Union[str, Path], sheet_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Load Excel file and return comprehensive info"""
        try:
            self.reader = ExcelReader(file_path, sheet_name, self.config["reader"])
            self.current_file_info = self.reader.get_file_info()

            if "error" in self.current_file_info:
                logger.error(f"Failed to load file: {self.current_file_info['error']}")
            else:
                logger.info(f"Successfully loaded Excel file: {file_path}")

            return self.current_file_info

        except Exception as e:
            error_msg = f"Error loading Excel file: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}

    def get_sheets(self, file_path: Union[str, Path]) -> List[str]:
        """Get available sheet names"""
        try:
            reader = ExcelReader(file_path, config=self.config["reader"])
            return reader.get_sheet_names()
        except Exception as e:
            logger.error(f"Error getting sheets: {e}")
            return []

    def preview_data(self, rows: int = 10) -> Optional[pd.DataFrame]:
        """Get preview of loaded data"""
        if not self.current_file_info or "error" in self.current_file_info:
            return None

        sample_data = self.current_file_info.get("sample_data")
        if sample_data is not None:
            return sample_data.head(rows)

        return None

    def get_data_quality_report(self) -> Dict[str, Any]:
        """Get comprehensive data quality report"""
        if not self.current_file_info or "error" in self.current_file_info:
            return {"error": "No file loaded"}

        return self.current_file_info.get("data_quality", {})

    def process_file(self, chunk_size: int = 5000) -> Iterator[Dict[str, Any]]:
        """Process loaded file in chunks"""
        if not self.reader:
            raise ValueError("No file loaded. Call load_file() first.")

        return self.reader.read_with_processing(chunk_size)

    def validate_file(
        self, file_path: Union[str, Path], max_size_mb: Optional[int] = None
    ) -> Dict[str, Any]:
        """Comprehensive file validation"""
        max_size = max_size_mb or self.config["validation"]["max_file_size_mb"]

        try:
            reader = ExcelReader(file_path, config=self.config["reader"])
            validation_result = reader.validate()

            # Additional custom validations
            if validation_result["valid"]:
                file_info = reader.get_file_info()

                # Size validation
                file_size_mb = file_info.get("file_size_mb", 0)
                if file_size_mb > max_size:
                    validation_result["warnings"].append(
                        f"Large file ({file_size_mb:.1f}MB) may impact performance"
                    )

                # Data quality warnings
                data_quality = file_info.get("data_quality", {})

                null_percentage = data_quality.get("null_percentage", 0)
                if null_percentage > 50:
                    validation_result["warnings"].append(
                        f"High percentage of missing data ({null_percentage:.1f}%)"
                    )

                mixed_types = data_quality.get("mixed_types", [])
                if mixed_types:
                    validation_result["warnings"].append(
                        f"Columns with mixed data types: {', '.join(mixed_types)}"
                    )

                # Add file info to result
                validation_result["file_info"] = file_info

            return validation_result

        except Exception as e:
            return {
                "valid": False,
                "errors": [f"Validation error: {str(e)}"],
                "warnings": [],
                "file_info": None,
            }

    def repair_file(
        self,
        file_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
    ) -> Dict[str, Any]:
        """Attempt to repair corrupted Excel file"""
        try:
            # Try different engines
            engines = ["openpyxl", "xlrd"]

            for engine in engines:
                try:
                    df = pd.read_excel(file_path, engine=engine)

                    # If successful, save repaired version
                    repair_path = output_path or str(file_path).replace(
                        ".xlsx", "_repaired.xlsx"
                    )
                    df.to_excel(repair_path, index=False, engine="openpyxl")

                    return {
                        "success": True,
                        "message": f"File repaired using {engine} engine",
                        "repaired_file": repair_path,
                        "rows_recovered": len(df),
                        "columns_recovered": len(df.columns),
                    }

                except Exception:
                    continue

            return {
                "success": False,
                "message": "Could not repair file with any available engine",
            }

        except Exception as e:
            return {"success": False, "message": f"Repair failed: {str(e)}"}

    def convert_file_format(
        self, file_path: Union[str, Path], output_format: str = "xlsx"
    ) -> Dict[str, Any]:
        """Convert Excel file to different format"""
        try:
            supported_formats = {
                "xlsx": {"engine": "openpyxl", "extension": ".xlsx"},
                "csv": {"engine": None, "extension": ".csv"},
                "parquet": {"engine": None, "extension": ".parquet"},
                "json": {"engine": None, "extension": ".json"},
            }

            if output_format not in supported_formats:
                return {
                    "success": False,
                    "message": f"Unsupported format. Available: {list(supported_formats.keys())}",
                }

            # Read source file
            df = pd.read_excel(file_path)

            # Generate output path
            input_path = Path(file_path)
            output_path = input_path.with_suffix(
                supported_formats[output_format]["extension"]
            )

            # Convert to target format
            if output_format == "xlsx":
                df.to_excel(output_path, index=False, engine="openpyxl")
            elif output_format == "csv":
                df.to_csv(output_path, index=False, encoding="utf-8")
            elif output_format == "parquet":
                df.to_parquet(output_path, index=False)
            elif output_format == "json":
                df.to_json(output_path, orient="records", indent=2)

            return {
                "success": True,
                "message": f"File converted to {output_format}",
                "output_file": str(output_path),
                "file_size_mb": output_path.stat().st_size / (1024 * 1024),
            }

        except Exception as e:
            return {"success": False, "message": f"Conversion failed: {str(e)}"}

    def create_template(
        self, template_type: str, output_path: Union[str, Path], rows: int = 10
    ) -> Dict[str, Any]:
        """Create Excel template files"""
        templates = {
            "employees": {
                "columns": [
                    "employee_id",
                    "first_name",
                    "last_name",
                    "email",
                    "department",
                    "position",
                    "salary",
                    "hire_date",
                    "active",
                ],
                "sample_data": {
                    "employee_id": ["EMP001", "EMP002", "EMP003"],
                    "first_name": ["John", "Jane", "Mike"],
                    "last_name": ["Doe", "Smith", "Johnson"],
                    "email": [
                        "john.doe@company.com",
                        "jane.smith@company.com",
                        "mike.johnson@company.com",
                    ],
                    "department": ["IT", "HR", "Sales"],
                    "position": ["Developer", "Manager", "Representative"],
                    "salary": [50000, 75000, 45000],
                    "hire_date": ["2023-01-15", "2022-03-10", "2023-05-20"],
                    "active": [True, True, False],
                },
            },
            "sales": {
                "columns": [
                    "transaction_id",
                    "customer_name",
                    "product",
                    "quantity",
                    "unit_price",
                    "total_amount",
                    "sale_date",
                ],
                "sample_data": {
                    "transaction_id": ["TXN001", "TXN002", "TXN003"],
                    "customer_name": ["ABC Corp", "XYZ Ltd", "DEF Inc"],
                    "product": ["Widget A", "Gadget B", "Tool C"],
                    "quantity": [10, 5, 15],
                    "unit_price": [25.50, 100.00, 15.75],
                    "total_amount": [255.00, 500.00, 236.25],
                    "sale_date": ["2024-01-01", "2024-01-02", "2024-01-03"],
                },
            },
        }

        try:
            if template_type not in templates:
                return {
                    "success": False,
                    "message": f"Template type not found. Available: {list(templates.keys())}",
                }

            template_data = templates[template_type]

            # Create DataFrame
            df_data = {}
            for col in template_data["columns"]:
                if col in template_data["sample_data"]:
                    # Repeat sample data to reach desired rows
                    sample_values = template_data["sample_data"][col]
                    df_data[col] = (sample_values * ((rows // len(sample_values)) + 1))[
                        :rows
                    ]
                else:
                    df_data[col] = [f"Sample {col} {i+1}" for i in range(rows)]

            df = pd.DataFrame(df_data)

            # Save to Excel
            with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="Data", index=False)

                # Add instructions sheet
                instructions_df = pd.DataFrame(
                    {
                        "Instructions": [
                            f"This is a {template_type} template",
                            "Replace sample data with your actual data",
                            "Maintain column structure for best results",
                            "Date format: YYYY-MM-DD",
                            "Boolean values: TRUE/FALSE or 1/0",
                            "Save file before importing to DENSO888",
                        ]
                    }
                )
                instructions_df.to_excel(writer, sheet_name="Instructions", index=False)

            return {
                "success": True,
                "message": f"Template created: {template_type}",
                "output_file": str(output_path),
                "rows": rows,
                "columns": len(template_data["columns"]),
            }

        except Exception as e:
            return {"success": False, "message": f"Template creation failed: {str(e)}"}


# Utility functions
def create_sample_excel(
    file_path: Union[str, Path], template: str = "employees", rows: int = 100
) -> bool:
    """Create sample Excel file - wrapper function"""
    try:
        handler = ExcelHandler()
        result = handler.create_template(template, file_path, rows)
        return result["success"]
    except Exception as e:
        logger.error(f"Error creating sample Excel: {e}")
        return False


def validate_excel_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Validate Excel file - wrapper function"""
    try:
        handler = ExcelHandler()
        return handler.validate_file(file_path)
    except Exception as e:
        logger.error(f"Error validating Excel file: {e}")
        return {"valid": False, "errors": [str(e)], "warnings": []}
        print(f"❌ Error: {e}")
        return {"valid": False, "errors": [str(e)], "warnings": []}
        print(f"❌ Error: {e}")
