"""Data cleaning and validation"""
import pandas as pd
import re
from typing import Dict

class DataCleaner:
    @staticmethod
    def clean_column_name(name: str) -> str:
        clean = re.sub(r"[^a-zA-Z0-9_]", "_", str(name))
        return re.sub(r"_+", "_", clean).strip("_").lower()
    
    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        df_clean = df.copy()
        
        # Fix column names
        df_clean.columns = [self.clean_column_name(col) for col in df_clean.columns]
        
        # Remove empty rows
        df_clean = df_clean.dropna(how="all")
        
        # Clean string columns
        for col in df_clean.select_dtypes(include=["object"]).columns:
            df_clean[col] = (
                df_clean[col].astype(str).str.strip()
                .replace(["nan", "None", ""], None)
            )
        
        return df_clean
    
    def convert_types(self, df: pd.DataFrame, type_mapping: Dict[str, str]) -> pd.DataFrame:
        df_typed = df.copy()
        
        for column, target_type in type_mapping.items():
            if column not in df_typed.columns:
                continue
                
            try:
                if target_type == "integer":
                    df_typed[column] = pd.to_numeric(df_typed[column], errors="coerce").fillna(0).astype("Int64")
                elif target_type == "float":
                    df_typed[column] = pd.to_numeric(df_typed[column], errors="coerce").fillna(0.0)
                elif target_type == "datetime":
                    df_typed[column] = pd.to_datetime(df_typed[column], errors="coerce")
                elif target_type == "boolean":
                    df_typed[column] = df_typed[column].astype(str).str.lower().isin(["true", "1", "yes", "y"])
            except Exception as e:
                print(f"Type conversion failed for {column}: {e}")
        
        return df_typed
