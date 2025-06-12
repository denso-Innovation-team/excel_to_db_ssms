"""Auto-detect column data types"""
from typing import Dict, List

class TypeDetector:
    @staticmethod
    def detect_types(columns: List[str]) -> Dict[str, str]:
        type_mapping = {}
        
        patterns = {
            "datetime": ["date", "time", "วันที่", "เวลา", "created", "updated"],
            "integer": ["id", "age", "count", "number", "จำนวน", "อายุ"],
            "float": ["price", "salary", "amount", "total", "value", "ราคา", "เงินเดือน"],
            "boolean": ["active", "enabled", "is_", "has_", "flag"]
        }
        
        for column in columns:
            col_lower = column.lower()
            column_type = "string"  # default
            
            for data_type, pattern_list in patterns.items():
                if any(pattern in col_lower for pattern in pattern_list):
                    column_type = data_type
                    break
            
            type_mapping[column] = column_type
        
        return type_mapping
