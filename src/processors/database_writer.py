import pandas as pd
from sqlalchemy import (
    text, MetaData, Table, Column, Integer, String, 
    DateTime, Float, Boolean, NVARCHAR
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
        self.engine = db_manager.engine
        self.metadata = MetaData()
        self.table = None

    def create_table_from_dataframe(
        self,
        df_sample: pd.DataFrame,
        primary_key: str = "id",
        type_mapping: Optional[Dict[str, str]] = None,
    ) -> None:
        """สร้างตารางใน SQL Server ตาม DataFrame structure"""
        columns = [Column(primary_key, Integer, primary_key=True, autoincrement=True)]

        for col_name, dtype in df_sample.dtypes.items():
            if col_name == primary_key:
                continue

            if type_mapping and col_name in type_mapping:
                sql_type = self._get_sqlserver_type(type_mapping[col_name])
            else:
                sql_type = self._infer_sqlserver_type(dtype)

            columns.append(Column(col_name, sql_type))

        # Drop table if exists (SQL Server specific)
        try:
            with self.engine.connect() as conn:
                conn.execute(text(f"DROP TABLE IF EXISTS [{self.table_name}]"))
                conn.commit()
        except:
            pass

        self.table = Table(self.table_name, self.metadata, *columns)

        try:
            self.metadata.create_all(self.engine)
            logger.info(f"[SUCCESS] SQL Server table '{self.table_name}' created")
        except SQLAlchemyError as e:
            logger.error(f"[ERROR] Error creating SQL Server table: {e}")
            raise

    def _get_sqlserver_type(self, type_name: str):
        """แปลง type เป็น SQL Server types"""
        type_mapping = {
            "string": NVARCHAR(255),  # Unicode support
            "text": NVARCHAR(1000),
            "integer": Integer,
            "float": Float,
            "boolean": Boolean,
            "datetime": DateTime,
        }
        return type_mapping.get(type_name, NVARCHAR(255))

    def _infer_sqlserver_type(self, pandas_dtype):
        """อนุมาน SQL Server type จาก pandas dtype"""
        if pd.api.types.is_integer_dtype(pandas_dtype):
            return Integer
        elif pd.api.types.is_float_dtype(pandas_dtype):
            return Float
        elif pd.api.types.is_bool_dtype(pandas_dtype):
            return Boolean
        elif pd.api.types.is_datetime64_any_dtype(pandas_dtype):
            return DateTime
        else:
            return NVARCHAR(255)  # Unicode support for Thai text

    def bulk_insert_sqlserver(self, df: pd.DataFrame) -> int:
        """Optimized bulk insert สำหรับ SQL Server"""
        try:
            # Clean DataFrame for SQL Server
            df_clean = df.copy()
            
            # Convert datetime columns
            for col in df_clean.columns:
                if df_clean[col].dtype == 'datetime64[ns]':
                    df_clean[col] = df_clean[col].dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # Replace NaN with None for SQL Server
            df_clean = df_clean.where(pd.notnull(df_clean), None)
            
            with self.engine.begin() as conn:
                df_clean.to_sql(
                    name=self.table_name,
                    con=conn,
                    if_exists="append",
                    index=False,
                    method="multi",
                    chunksize=settings.BATCH_SIZE,
                )
                logger.info(f"[SUCCESS] Inserted {len(df)} rows to SQL Server")
                return len(df)
                
        except SQLAlchemyError as e:
            logger.error(f"[ERROR] SQL Server bulk insert error: {e}")
            raise

    def bulk_insert_batch(self, df: pd.DataFrame) -> int:
        """Main bulk insert method สำหรับ SQL Server"""
        return self.bulk_insert_sqlserver(df)

    def parallel_insert(self, dataframes: List[pd.DataFrame]) -> int:
        """Insert multiple dataframes แบบ parallel"""
        total_inserted = 0

        with ThreadPoolExecutor(max_workers=settings.MAX_WORKERS) as executor:
            futures = {
                executor.submit(self.bulk_insert_batch, df): df for df in dataframes
            }

            for future in as_completed(futures):
                try:
                    rows_inserted = future.result()
                    total_inserted += rows_inserted
                    logger.info(f"[SUCCESS] Batch inserted {rows_inserted} rows")
                except Exception as e:
                    logger.error(f"[ERROR] Parallel insert error: {e}")

        logger.info(f"[COMPLETE] Total inserted: {total_inserted} rows")
        return total_inserted

    def get_table_info(self) -> Dict[str, Any]:
        """ดึงข้อมูลตารางจาก SQL Server"""
        try:
            with self.engine.connect() as conn:
                # Count rows
                result = conn.execute(text(f"SELECT COUNT(*) FROM [{self.table_name}]"))
                row_count = result.fetchone()[0]

                # Get column info
                result = conn.execute(text(f"""
                    SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = '{self.table_name}'
                    ORDER BY ORDINAL_POSITION
                """))
                columns = result.fetchall()

                return {
                    "table_name": self.table_name,
                    "row_count": row_count,
                    "columns": [(col[0], col[1], col[2]) for col in columns],
                }
        except Exception as e:
            logger.error(f"[ERROR] Error getting SQL Server table info: {e}")
            return {"error": str(e)}
