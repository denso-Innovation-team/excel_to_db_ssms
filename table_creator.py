"""SQL Server table management"""
import pandas as pd
from sqlalchemy import text
from typing import Dict, Optional
from database import DatabaseManager

class TableCreator:
    def __init__(self, table_name: str, db_manager: DatabaseManager):
        self.table_name = table_name
        self.db_manager = db_manager
    
    def create_from_dataframe(self, df: pd.DataFrame, type_mapping: Optional[Dict[str, str]] = None):
        if not self.db_manager.engine:
            raise RuntimeError("Database not connected")
        
        # Build column definitions
        columns_sql = ["id INT IDENTITY(1,1) PRIMARY KEY"]
        
        for col_name in df.columns:
            dtype = df[col_name].dtype
            
            if type_mapping and col_name in type_mapping:
                sql_type = self._get_sql_type(type_mapping[col_name])
            else:
                sql_type = self._infer_sql_type(dtype)
            
            columns_sql.append(f"[{col_name}] {sql_type}")
        
        # Execute DDL
        drop_sql = f"IF OBJECT_ID('{self.table_name}', 'U') IS NOT NULL DROP TABLE [{self.table_name}]"
        create_sql = f"CREATE TABLE [{self.table_name}] ({', '.join(columns_sql)})"
        
        with self.db_manager.engine.connect() as conn:
            with conn.begin():
                conn.execute(text(drop_sql))
                conn.execute(text(create_sql))
        
        print(f"✅ Table '{self.table_name}' created")
    
    def _get_sql_type(self, type_name: str) -> str:
        mapping = {
            "string": "NVARCHAR(255)",
            "text": "NVARCHAR(MAX)", 
            "integer": "INT",
            "float": "FLOAT",
            "boolean": "BIT",
            "datetime": "DATETIME2"
        }
        return mapping.get(type_name, "NVARCHAR(255)")
    
    def _infer_sql_type(self, pandas_dtype) -> str:
        if pd.api.types.is_integer_dtype(pandas_dtype):
            return "INT"
        elif pd.api.types.is_float_dtype(pandas_dtype):
            return "FLOAT" 
        elif pd.api.types.is_bool_dtype(pandas_dtype):
            return "BIT"
        elif pd.api.types.is_datetime64_any_dtype(pandas_dtype):
            return "DATETIME2"
        else:
            return "NVARCHAR(255)"
    
    def bulk_insert(self, df: pd.DataFrame) -> int:
        if not self.db_manager.engine:
            raise RuntimeError("Database not connected")
        
        df_clean = df.copy()
        
        # Handle datetime columns
        for col in df_clean.columns:
            if pd.api.types.is_datetime64_any_dtype(df_clean[col]):
                df_clean[col] = df_clean[col].dt.strftime("%Y-%m-%d %H:%M:%S").replace("NaT", None)
        
        # Replace NaN with None
        df_clean = df_clean.where(pd.notnull(df_clean), None)
        
        # Bulk insert
        with self.db_manager.engine.begin() as conn:
            df_clean.to_sql(
                name=self.table_name,
                con=conn,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=1000
            )
        
        print(f"✅ Inserted {len(df_clean):,} rows")
        return len(df_clean)
