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
        """Create table based on DataFrame structure"""
        columns = [Column(primary_key, Integer, primary_key=True, autoincrement=True)]

        for col_name, dtype in df_sample.dtypes.items():
            if col_name == primary_key:
                continue

            if type_mapping and col_name in type_mapping:
                sql_type = self._get_sqlalchemy_type(type_mapping[col_name])
            else:
                sql_type = self._infer_sql_type(dtype)

            columns.append(Column(col_name, sql_type))

        self.table = Table(self.table_name, self.metadata, *columns)

        try:
            self.metadata.create_all(self.engine)
            logger.info(f"[SUCCESS] Table '{self.table_name}' created successfully")
        except SQLAlchemyError as e:
            logger.error(f"[ERROR] Error creating table: {e}")
            raise

    def _get_sqlalchemy_type(self, type_name: str):
        type_mapping = {
            "string": String(255),
            "text": String(1000),
            "integer": Integer,
            "float": Float,
            "boolean": Boolean,
            "datetime": DateTime,
        }
        return type_mapping.get(type_name, String(255))

    def _infer_sql_type(self, pandas_dtype):
        if pd.api.types.is_integer_dtype(pandas_dtype):
            return Integer
        elif pd.api.types.is_float_dtype(pandas_dtype):
            return Float
        elif pd.api.types.is_bool_dtype(pandas_dtype):
            return Boolean
        elif pd.api.types.is_datetime64_any_dtype(pandas_dtype):
            return DateTime
        else:
            return String(255)

    def bulk_insert_postgresql(self, df: pd.DataFrame) -> int:
        """Optimized bulk insert for PostgreSQL/Supabase"""
        try:
            with self.engine.begin() as conn:
                df.to_sql(
                    name=self.table_name,
                    con=conn,
                    if_exists="append",
                    index=False,
                    method="multi",
                    chunksize=settings.BATCH_SIZE,
                )
                logger.info(f"[SUCCESS] Inserted {len(df)} rows to PostgreSQL")
                return len(df)
        except SQLAlchemyError as e:
            logger.error(f"[ERROR] PostgreSQL bulk insert error: {e}")
            raise

    def bulk_insert_mysql(self, df: pd.DataFrame) -> int:
        try:
            with self.engine.begin() as conn:
                df.to_sql(
                    name=self.table_name,
                    con=conn,
                    if_exists="append",
                    index=False,
                    method="multi",
                    chunksize=settings.BATCH_SIZE,
                )
                logger.info(f"[SUCCESS] Inserted {len(df)} rows to MySQL")
                return len(df)
        except SQLAlchemyError as e:
            logger.error(f"[ERROR] MySQL bulk insert error: {e}")
            raise

    def bulk_insert_generic(self, df: pd.DataFrame) -> int:
        try:
            with self.engine.begin() as conn:
                df.to_sql(
                    name=self.table_name,
                    con=conn,
                    if_exists="append",
                    index=False,
                    chunksize=settings.BATCH_SIZE,
                )
                logger.info(f"[SUCCESS] Inserted {len(df)} rows using generic method")
                return len(df)
        except SQLAlchemyError as e:
            logger.error(f"[ERROR] Generic bulk insert error: {e}")
            raise

    def bulk_insert_batch(self, df: pd.DataFrame) -> int:
        """Main bulk insert method with auto-detection"""
        if settings.DB_TYPE == "postgresql":
            return self.bulk_insert_postgresql(df)
        elif settings.DB_TYPE == "mysql":
            return self.bulk_insert_mysql(df)
        else:
            return self.bulk_insert_generic(df)

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
                    logger.info(f"[SUCCESS] Batch inserted {rows_inserted} rows")
                except Exception as e:
                    logger.error(f"[ERROR] Parallel insert error: {e}")

        logger.info(f"[COMPLETE] Total inserted: {total_inserted} rows")
        return total_inserted

    def get_table_info(self) -> Dict[str, Any]:
        """Get table information"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {self.table_name}"))
                row_count = result.fetchone()[0]

                if settings.DB_TYPE == "postgresql":
                    result = conn.execute(
                        text(
                            f"""
                        SELECT column_name, data_type 
                        FROM information_schema.columns 
                        WHERE table_name = '{self.table_name}'
                    """
                        )
                    )
                    columns = result.fetchall()
                else:
                    columns = []

                return {
                    "table_name": self.table_name,
                    "row_count": row_count,
                    "columns": columns,
                }
        except Exception as e:
            logger.error(f"[ERROR] Error getting table info: {e}")
            return {"error": str(e)}
