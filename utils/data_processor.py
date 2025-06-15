"""
utils/data_processor.py
Data Processing Utilities
"""

import pandas as pd
from typing import Dict
import re

class DataProcessor:
    """Data processing and cleaning utilities"""
    
    @staticmethod
    def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
        """Clean column names for database compatibility"""
        cleaned_columns = []
        for col in df.columns:
            # Convert to string and clean
            clean_col = str(col).strip()
            # Replace special characters
            clean_col = re.sub(r'[^\w\s]', '_', clean_col)
            # Replace spaces with underscores
            clean_col = re.sub(r'\s+', '_', clean_col)
            # Remove multiple underscores
            clean_col = re.sub(r'_+', '_', clean_col)
            # Remove leading/trailing underscores
            clean_col = clean_col.strip('_').lower()
            
            # Ensure not empty
            if not clean_col:
                clean_col = f"column_{len(cleaned_columns)}"
            
            # Handle duplicates
            original_col = clean_col
            counter = 1
            while clean_col in cleaned_columns:
                clean_col = f"{original_col}_{counter}"
                counter += 1
            
            cleaned_columns.append(clean_col)
        
        df.columns = cleaned_columns
        return df
    
    @staticmethod
    def detect_data_types(df: pd.DataFrame) -> Dict[str, str]:
        """Detect optimal data types for database"""
        type_mapping = {}
        
        for column in df.columns:
            sample_data = df[column].dropna().head(100)
            
            if len(sample_data) == 0:
                type_mapping[column] = "TEXT"
                continue
            
            # Check for numeric data
            try:
                pd.to_numeric(sample_data)
                # Check if integers
                if sample_data.astype(str).str.match(r'^\d+).all():
                    type_mapping[column] = "INTEGER"
                else:
                    type_mapping[column] = "REAL"
                continue
            except (ValueError, TypeError):
                pass
            
            # Check for dates
            try:
                pd.to_datetime(sample_data)
                type_mapping[column] = "DATETIME"
                continue
            except (ValueError, TypeError):
                pass
            
            # Check for boolean
            unique_values = set(str(v).lower() for v in sample_data.unique())
            bool_values = {'true', 'false', 'yes', 'no', '1', '0', 'y', 'n'}
            if unique_values.issubset(bool_values):
                type_mapping[column] = "BOOLEAN"
                continue
            
            # Default to text
            type_mapping[column] = "TEXT"
        
        return type_mapping
    
    @staticmethod
    def clean_data_for_import(df: pd.DataFrame) -> pd.DataFrame:
        """Clean data for database import"""
        # Remove completely empty rows
        df = df.dropna(how='all')
        
        # Handle mixed data types
        for column in df.columns:
            if df[column].dtype == 'object':
                # Convert to string and strip whitespace
                df[column] = df[column].astype(str).str.strip()
                # Replace 'nan' strings with None
                df[column] = df[column].replace('nan', None)
        
        return df
    
    @staticmethod
    def chunk_dataframe(df: pd.DataFrame, chunk_size: int = 1000):
        """Split dataframe into chunks for processing"""
        for i in range(0, len(df), chunk_size):
            yield df[i:i + chunk_size]
    
    @staticmethod
    def validate_data_quality(df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze data quality"""
        total_cells = len(df) * len(df.columns)
        
        return {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "total_cells": total_cells,
            "null_cells": df.isnull().sum().sum(),
            "null_percentage": (df.isnull().sum().sum() / total_cells * 100) if total_cells > 0 else 0,
            "duplicate_rows": df.duplicated().sum(),
            "empty_columns": df.isnull().all().sum(),
            "numeric_columns": len(df.select_dtypes(include=[np.number]).columns),
            "text_columns": len(df.select_dtypes(include=['object']).columns),
            "datetime_columns": len(df.select_dtypes(include=['datetime']).columns)
        }

def clean_dataframe(df: pd.DataFrame, options: Dict[str, bool] = None) -> pd.DataFrame:
    """Clean dataframe with specified options"""
    if options is None:
        options = {
            "clean_columns": True,
            "remove_empty_rows": True,
            "clean_data": True
        }
    
    if options.get("clean_columns", True):
        df = DataProcessor.clean_column_names(df)
    
    if options.get("remove_empty_rows", True):
        df = df.dropna(how='all')
    
    if options.get("clean_data", True):
        df = DataProcessor.clean_data_for_import(df)
    
    return df