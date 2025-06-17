"""
core/field_mapper.py
Field Mapping System for Excel to Database
"""

import re
from typing import Dict, List, Any
from difflib import SequenceMatcher


class FieldMapper:
    """Field mapping between Excel columns and database columns"""

    def __init__(self):
        self.mappings = {}
        self.similarity_threshold = 0.6

    def auto_map(
        self, excel_columns: List[str], db_columns: List[str]
    ) -> Dict[str, str]:
        """Auto-map Excel columns to database columns"""
        mappings = {}

        for excel_col in excel_columns:
            best_match = self._find_best_match(excel_col, db_columns)
            if best_match:
                mappings[excel_col] = best_match

        return mappings

    def _find_best_match(self, excel_col: str, db_columns: List[str]) -> str:
        """Find best matching database column"""
        excel_clean = self._normalize_name(excel_col)
        best_score = 0
        best_match = ""

        for db_col in db_columns:
            db_clean = self._normalize_name(db_col)

            # Exact match
            if excel_clean == db_clean:
                return db_col

            # Similarity match
            score = SequenceMatcher(None, excel_clean, db_clean).ratio()
            if score > best_score and score >= self.similarity_threshold:
                best_score = score
                best_match = db_col

        return best_match

    def _normalize_name(self, name: str) -> str:
        """Normalize column name for comparison"""
        normalized = str(name).lower().strip()
        normalized = re.sub(r"[^\w]", "_", normalized)
        normalized = re.sub(r"_+", "_", normalized)
        return normalized.strip("_")

    def create_mapping(self, excel_col: str, db_col: str, transformation: str = None):
        """Create manual field mapping"""
        self.mappings[excel_col] = {
            "db_column": db_col,
            "transformation": transformation,
        }

    def get_mappings(self) -> Dict[str, Dict[str, Any]]:
        """Get all current mappings"""
        return self.mappings.copy()

    def clear_mappings(self):
        """Clear all mappings"""
        self.mappings.clear()
