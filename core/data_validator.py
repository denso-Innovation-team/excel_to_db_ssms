"""
Data Validator - Excel Data Validation and Cleaning
Validates and cleans Excel data before database import
"""

import pandas as pd
import re
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class DataValidator:
    """Data validation and cleaning for Excel imports"""

    def __init__(self):
        self.validation_rules = {}
        self.errors = []
        self.warnings = []

    def validate_dataframe(
        self, df: pd.DataFrame, rules: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Validate entire dataframe"""
        self.errors = []
        self.warnings = []

        if rules:
            self.validation_rules = rules

        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "stats": self._get_data_stats(df),
            "cleaned_data": df.copy(),
        }

        # Basic validation
        result["cleaned_data"] = self._clean_dataframe(df)

        # Apply custom rules
        if self.validation_rules:
            self._apply_validation_rules(result["cleaned_data"])

        result["errors"] = self.errors
        result["warnings"] = self.warnings
        result["valid"] = len(self.errors) == 0

        return result

    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean dataframe for database import"""
        cleaned = df.copy()

        # Remove completely empty rows
        cleaned = cleaned.dropna(how="all")

        # Clean column names
        cleaned.columns = [self._clean_column_name(col) for col in cleaned.columns]

        # Handle data types and null values
        for col in cleaned.columns:
            cleaned[col] = self._clean_column_data(cleaned[col])

        return cleaned

    def _clean_column_name(self, name: str) -> str:
        """Clean column name for database compatibility"""
        # Convert to string and strip
        clean = str(name).strip()

        # Replace special characters
        clean = re.sub(r"[^\w\s]", "_", clean)
        clean = re.sub(r"\s+", "_", clean)
        clean = re.sub(r"_+", "_", clean)
        clean = clean.strip("_").lower()

        # Ensure not empty
        if not clean:
            clean = "column"

        return clean

    def _clean_column_data(self, series: pd.Series) -> pd.Series:
        """Clean data in a column"""
        if series.dtype == "object":
            # String cleaning
            series = series.astype(str)
            series = series.str.strip()
            series = series.replace(["nan", "NaN", "NULL", ""], None)

        return series

    def _apply_validation_rules(self, df: pd.DataFrame):
        """Apply custom validation rules"""
        for column, rules in self.validation_rules.items():
            if column not in df.columns:
                self.warnings.append(f"Column '{column}' not found in data")
                continue

            self._validate_column(df[column], column, rules)

    def _validate_column(
        self, series: pd.Series, column_name: str, rules: Dict[str, Any]
    ):
        """Validate individual column"""
        # Required field validation
        if rules.get("required", False):
            null_count = series.isnull().sum()
            if null_count > 0:
                self.errors.append(
                    f"Column '{column_name}' has {null_count} null values but is required"
                )

        # Data type validation
        expected_type = rules.get("type")
        if expected_type:
            self._validate_data_type(series, column_name, expected_type)

        # Range validation for numeric columns
        if "min_value" in rules or "max_value" in rules:
            self._validate_numeric_range(series, column_name, rules)

        # String length validation
        if "max_length" in rules:
            self._validate_string_length(series, column_name, rules["max_length"])

        # Pattern validation
        if "pattern" in rules:
            self._validate_pattern(series, column_name, rules["pattern"])

        # Custom validation function
        if "custom_validator" in rules:
            self._apply_custom_validator(series, column_name, rules["custom_validator"])

    def _validate_data_type(
        self, series: pd.Series, column_name: str, expected_type: str
    ):
        """Validate data type"""
        if expected_type == "integer":
            try:
                pd.to_numeric(series.dropna(), errors="raise")
            except (ValueError, TypeError):
                self.errors.append(
                    f"Column '{column_name}' contains non-numeric values"
                )

        elif expected_type == "float":
            try:
                pd.to_numeric(series.dropna(), errors="raise")
            except (ValueError, TypeError):
                self.errors.append(
                    f"Column '{column_name}' contains non-numeric values"
                )

        elif expected_type == "date":
            try:
                pd.to_datetime(series.dropna(), errors="raise")
            except (ValueError, TypeError):
                self.errors.append(
                    f"Column '{column_name}' contains invalid date values"
                )

        elif expected_type == "email":
            self._validate_email_column(series, column_name)

    def _validate_numeric_range(
        self, series: pd.Series, column_name: str, rules: Dict[str, Any]
    ):
        """Validate numeric range"""
        try:
            numeric_series = pd.to_numeric(series.dropna(), errors="coerce")

            if "min_value" in rules:
                min_violations = (numeric_series < rules["min_value"]).sum()
                if min_violations > 0:
                    self.errors.append(
                        f"Column '{column_name}' has {min_violations} values below minimum {rules['min_value']}"
                    )

            if "max_value" in rules:
                max_violations = (numeric_series > rules["max_value"]).sum()
                if max_violations > 0:
                    self.errors.append(
                        f"Column '{column_name}' has {max_violations} values above maximum {rules['max_value']}"
                    )

        except Exception as e:
            self.errors.append(
                f"Could not validate numeric range for '{column_name}': {str(e)}"
            )

    def _validate_string_length(
        self, series: pd.Series, column_name: str, max_length: int
    ):
        """Validate string length"""
        try:
            string_series = series.astype(str).dropna()
            long_values = (string_series.str.len() > max_length).sum()

            if long_values > 0:
                self.warnings.append(
                    f"Column '{column_name}' has {long_values} values exceeding {max_length} characters"
                )

        except Exception as e:
            self.warnings.append(
                f"Could not validate string length for '{column_name}': {str(e)}"
            )

    def _validate_pattern(self, series: pd.Series, column_name: str, pattern: str):
        """Validate regex pattern"""
        try:
            string_series = series.astype(str).dropna()
            pattern_violations = (~string_series.str.match(pattern, na=False)).sum()

            if pattern_violations > 0:
                self.errors.append(
                    f"Column '{column_name}' has {pattern_violations} values not matching pattern"
                )

        except Exception as e:
            self.errors.append(
                f"Pattern validation failed for '{column_name}': {str(e)}"
            )

    def _validate_email_column(self, series: pd.Series, column_name: str):
        """Validate email addresses"""
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        try:
            string_series = series.astype(str).dropna()
            invalid_emails = (~string_series.str.match(email_pattern, na=False)).sum()

            if invalid_emails > 0:
                self.errors.append(
                    f"Column '{column_name}' has {invalid_emails} invalid email addresses"
                )

        except Exception as e:
            self.errors.append(f"Email validation failed for '{column_name}': {str(e)}")

    def _apply_custom_validator(
        self, series: pd.Series, column_name: str, validator_func
    ):
        """Apply custom validation function"""
        try:
            result = validator_func(series)
            if not result.get("valid", True):
                self.errors.extend(result.get("errors", []))
                self.warnings.extend(result.get("warnings", []))
        except Exception as e:
            self.errors.append(
                f"Custom validation failed for '{column_name}': {str(e)}"
            )

    def _get_data_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get data quality statistics"""
        total_cells = len(df) * len(df.columns)
        null_cells = df.isnull().sum().sum()

        return {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "total_cells": total_cells,
            "null_cells": null_cells,
            "null_percentage": (
                (null_cells / total_cells * 100) if total_cells > 0 else 0
            ),
            "duplicate_rows": df.duplicated().sum(),
            "empty_columns": df.isnull().all().sum(),
            "data_types": {col: str(dtype) for col, dtype in df.dtypes.items()},
        }

    def detect_data_types(self, df: pd.DataFrame) -> Dict[str, str]:
        """Auto-detect optimal data types"""
        type_suggestions = {}

        for column in df.columns:
            sample_data = df[column].dropna().head(100)

            if len(sample_data) == 0:
                type_suggestions[column] = "TEXT"
                continue

            # Try numeric
            try:
                numeric_data = pd.to_numeric(sample_data)
                if (numeric_data % 1 == 0).all():
                    type_suggestions[column] = "INTEGER"
                else:
                    type_suggestions[column] = "FLOAT"
                continue
            except (ValueError, TypeError):
                pass

            # Try date
            try:
                pd.to_datetime(sample_data)
                type_suggestions[column] = "DATETIME"
                continue
            except (ValueError, TypeError):
                pass

            # Check for boolean
            unique_values = set(str(v).lower() for v in sample_data.unique())
            bool_values = {"true", "false", "yes", "no", "1", "0", "y", "n"}
            if unique_values.issubset(bool_values):
                type_suggestions[column] = "BOOLEAN"
                continue

            # Default to text
            type_suggestions[column] = "TEXT"

        return type_suggestions

    def suggest_validation_rules(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """Suggest validation rules based on data analysis"""
        suggestions = {}

        for column in df.columns:
            rules = {}
            series = df[column].dropna()

            if len(series) == 0:
                continue

            # Suggest required if low null percentage
            null_percentage = (df[column].isnull().sum() / len(df)) * 100
            if null_percentage < 5:
                rules["required"] = True

            # Suggest data type
            suggested_type = self.detect_data_types(df)[column]
            rules["type"] = suggested_type.lower()

            # Suggest string length limits
            if suggested_type == "TEXT":
                max_length = series.astype(str).str.len().max()
                if max_length > 0:
                    rules["max_length"] = min(max_length * 2, 255)  # Add some buffer

            # Suggest numeric ranges
            if suggested_type in ["INTEGER", "FLOAT"]:
                try:
                    numeric_series = pd.to_numeric(series)
                    rules["min_value"] = numeric_series.min()
                    rules["max_value"] = numeric_series.max()
                except:
                    pass

            suggestions[column] = rules

        return suggestions
