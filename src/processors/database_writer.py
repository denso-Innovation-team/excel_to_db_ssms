import pandas as pd
from sqlalchemy import (
    text,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Boolean,
    NVARCHAR,
)
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, Any, List, Optional
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..config.database import db_manager
from ..config.settings import settings

logger = logging.getLogger(__name__)


class DatabaseWriter:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.engine = None
        self.metadata = MetaData()
        self.table = None

    def _get_engine(self):
        """Get working engine instance"""
        if not self.engine:
            if not db_manager.engine:
                db_manager._setup_engine()
            self.engine = db_manager.engine
        return self.engine

    def create_table_from_dataframe(
        self,
        df_sample: pd.DataFrame,
        primary_key: str = "id",
        type_mapping: Optional[Dict[str, str]] = None,
    ) -> None:
        """Create table using direct SQL - Fix DDL issue"""

        try:
            engine = self._get_engine()

            # Build CREATE TABLE statement
            columns_sql = [f"[{primary_key}] INT IDENTITY(1,1) PRIMARY KEY"]

            for col_name, dtype in df_sample.dtypes.items():
                if col_name == primary_key:
                    continue

                if type_mapping and col_name in type_mapping:
                    sql_type = self._get_sqlserver_type(type_mapping[col_name])
                else:
                    sql_type = self._infer_sqlserver_type(dtype)

                columns_sql.append(f"[{col_name}] {sql_type}")

            # Drop and create table
            drop_sql = f"IF OBJECT_ID('{self.table_name}', 'U') IS NOT NULL DROP TABLE [{self.table_name}]"
            create_sql = f"CREATE TABLE [{self.table_name}] ({', '.join(columns_sql)})"

            with engine.connect() as conn:
                conn.execute(text(drop_sql))
                conn.execute(text(create_sql))
                conn.commit()

            logger.info(f"✅ Table '{self.table_name}' created")

        except Exception as e:
            logger.error(f"❌ Table creation failed: {e}")
            raise

    def _get_sqlserver_type(self, type_name: str) -> str:
        """Convert type name to SQL Server type"""
        type_mapping = {
            "string": "NVARCHAR(255)",
            "text": "NVARCHAR(1000)",
            "integer": "INT",
            "float": "FLOAT",
            "boolean": "BIT",
            "datetime": "DATETIME",
        }
        return type_mapping.get(type_name, "NVARCHAR(255)")

    def _infer_sqlserver_type(self, pandas_dtype) -> str:
        """Infer SQL Server type from pandas dtype"""
        if pd.api.types.is_integer_dtype(pandas_dtype):
            return "INT"
        elif pd.api.types.is_float_dtype(pandas_dtype):
            return "FLOAT"
        elif pd.api.types.is_bool_dtype(pandas_dtype):
            return "BIT"
        elif pd.api.types.is_datetime64_any_dtype(pandas_dtype):
            return "DATETIME"
        else:
            return "NVARCHAR(255)"

    def bulk_insert_batch(self, df: pd.DataFrame) -> int:
        """Optimized bulk insert for SQL Server"""
        try:
            engine = self._get_engine()

            # Clean DataFrame
            df_clean = df.copy()

            # Handle datetime columns
            for col in df_clean.columns:
                if df_clean[col].dtype == "datetime64[ns]":
                    df_clean[col] = df_clean[col].dt.strftime("%Y-%m-%d %H:%M:%S")

            # Replace NaN with None
            df_clean = df_clean.where(pd.notnull(df_clean), None)

            with engine.begin() as conn:
                df_clean.to_sql(
                    name=self.table_name,
                    con=conn,
                    if_exists="append",
                    index=False,
                    method="multi",
                    chunksize=settings.BATCH_SIZE,
                )

            logger.info(f"✅ Inserted {len(df)} rows")
            return len(df)

        except Exception as e:
            logger.error(f"❌ Bulk insert failed: {e}")
            raise

    def parallel_insert(self, dataframes: List[pd.DataFrame]) -> int:
        """Insert multiple dataframes in parallel"""
        total_inserted = 0

        with ThreadPoolExecutor(max_workers=settings.MAX_WORKERS) as executor:
            futures = {
                executor.submit(self.bulk_insert_batch, df): df for df in dataframes
            }

            for future in as_completed(futures):
                try:
                    rows_inserted = future.result()
                    total_inserted += rows_inserted
                except Exception as e:
                    logger.error(f"❌ Parallel insert error: {e}")

        return total_inserted

    def get_table_info(self) -> Dict[str, Any]:
        """Get table information"""
        try:
            engine = self._get_engine()

            with engine.connect() as conn:
                # Count rows
                count_result = conn.execute(
                    text(f"SELECT COUNT(*) FROM [{self.table_name}]")
                )
                row_count = count_result.fetchone()[0]

                # Get columns
                columns_result = conn.execute(
                    text(
                        f"""
                    SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = '{self.table_name}'
                    ORDER BY ORDINAL_POSITION
                """
                    )
                )
                columns = [
                    (row[0], row[1], row[2]) for row in columns_result.fetchall()
                ]

                return {
                    "table_name": self.table_name,
                    "row_count": row_count,
                    "columns": columns,
                }
        except Exception as e:
            logger.error(f"❌ Get table info failed: {e}")
            return {"error": str(e)}
