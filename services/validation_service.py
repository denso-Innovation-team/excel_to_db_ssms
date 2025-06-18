from typing import Dict, Any, List, Optional
import logging
import pandas as pd

logger = logging.getLogger(__name__)


class ValidationService:
    """Enhanced data validation service"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.validation_rules = {
            "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "phone": r"^\+?[\d\-\(\)\s]+$",
            "date": [r"^\d{4}-\d{2}-\d{2}$", r"^\d{2}/\d{2}/\d{4}$"],
        }

    def validate_dataframe(
        self, df: pd.DataFrame, rules: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Validate DataFrame against rules"""
        results = {"valid": True, "errors": [], "warnings": [], "column_stats": {}}

        try:
            for column, rule in rules.items():
                if column not in df.columns:
                    results["errors"].append(f"Column {column} not found")
                    continue

                # Get column stats
                stats = self._analyze_column(df[column])
                results["column_stats"][column] = stats

                # Check required
                if rule.get("required", False):
                    null_count = df[column].isnull().sum()
                    if null_count > 0:
                        results["errors"].append(
                            f"Column {column} has {null_count} null values"
                        )

                # Validate format
                if rule.get("format"):
                    invalid_format = self._validate_format(
                        df[column], rule["format"], rule.get("format_params", {})
                    )
                    if invalid_format:
                        results["errors"].extend(invalid_format)

                # Check unique
                if rule.get("unique", False):
                    duplicates = df[column].duplicated().sum()
                    if duplicates > 0:
                        results["errors"].append(
                            f"Column {column} has {duplicates} duplicate values"
                        )

                # Value range check
                if "min_value" in rule or "max_value" in rule:
                    range_errors = self._check_value_range(
                        df[column], rule.get("min_value"), rule.get("max_value")
                    )
                    if range_errors:
                        results["errors"].extend(range_errors)

            results["valid"] = len(results["errors"]) == 0
            return results

        except Exception as e:
            logger.error(f"Validation error: {e}")
            results["valid"] = False
            results["errors"].append(f"Validation failed: {str(e)}")
            return results

    def _analyze_column(self, series: pd.Series) -> Dict[str, Any]:
        """Analyze column statistics"""
        stats = {
            "total_rows": len(series),
            "null_count": series.isnull().sum(),
            "unique_count": series.nunique(),
            "data_type": str(series.dtype),
        }

        if pd.api.types.is_numeric_dtype(series):
            stats.update(
                {
                    "min": series.min(),
                    "max": series.max(),
                    "mean": series.mean(),
                    "median": series.median(),
                }
            )

        return stats

    def _validate_format(
        self, series: pd.Series, format_type: str, params: Dict[str, Any]
    ) -> List[str]:
        """Validate column format"""
        errors = []

        if format_type in self.validation_rules:
            pattern = self.validation_rules[format_type]
            invalid_mask = ~series.fillna("").str.match(pattern)
            invalid_count = invalid_mask.sum()

            if invalid_count > 0:
                errors.append(
                    f"Found {invalid_count} invalid {format_type} format values"
                )

        return errors

    def _check_value_range(
        self,
        series: pd.Series,
        min_value: Optional[Any] = None,
        max_value: Optional[Any] = None,
    ) -> List[str]:
        """Check value range"""
        errors = []

        if min_value is not None:
            below_min = (series < min_value).sum()
            if below_min > 0:
                errors.append(f"Found {below_min} values below minimum {min_value}")

        if max_value is not None:
            above_max = (series > max_value).sum()
            if above_max > 0:
                errors.append(f"Found {above_max} values above maximum {max_value}")

        return errors
