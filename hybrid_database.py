"""Hybrid Database Manager - SQL Server with SQLite Fallback"""

import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
from typing import Optional, Any, Protocol
from config import DatabaseConfig


class DatabaseInterface(Protocol):
    """Interface สำหรับ database operations"""

    def connect(self) -> bool: ...
    def test(self) -> bool: ...
    def create_table_from_dataframe(
        self, table_name: str, df: pd.DataFrame, type_mapping: Optional[dict] = None
    ) -> None: ...
    def bulk_insert(self, table_name: str, df: pd.DataFrame) -> int: ...


class SQLServerManager:
    """SQL Server Manager หลัก"""

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.engine: Optional[Any] = None

    def connect(self) -> bool:
        try:
            self.engine = create_engine(
                self.config.get_url(), pool_size=3, max_overflow=5, pool_timeout=30
            )

            if self.engine:
                with self.engine.connect() as conn:
                    result = conn.execute(text("SELECT @@SERVERNAME, DB_NAME()"))
                    row = result.fetchone()
                    if row:
                        print(f"✅ SQL Server: {row[0]}/{row[1]}")
            return True

        except Exception as e:
            print(f"❌ SQL Server failed: {e}")
            return False

    def test(self) -> bool:
        if not self.engine and not self.connect():
            return False

        try:
            if self.engine:
                with self.engine.connect() as conn:
                    result = conn.execute(text("SELECT 1"))
                    return result.fetchone()[0] == 1
            return False
        except:
            return False

    def create_table_from_dataframe(
        self, table_name: str, df: pd.DataFrame, type_mapping: Optional[dict] = None
    ) -> None:
        if not self.engine:
            raise RuntimeError("SQL Server not connected")

        # Build SQL Server DDL
        columns_sql = ["id INT IDENTITY(1,1) PRIMARY KEY"]

        for col_name in df.columns:
            dtype = df[col_name].dtype
            sql_type = self._infer_sql_type(dtype)
            columns_sql.append(f"[{col_name}] {sql_type}")

        drop_sql = (
            f"IF OBJECT_ID('{table_name}', 'U') IS NOT NULL DROP TABLE [{table_name}]"
        )
        create_sql = f"CREATE TABLE [{table_name}] ({', '.join(columns_sql)})"

        with self.engine.connect() as conn:
            with conn.begin():
                conn.execute(text(drop_sql))
                conn.execute(text(create_sql))

        print(f"✅ SQL Server table '{table_name}' created")

    def bulk_insert(self, table_name: str, df: pd.DataFrame) -> int:
        if not self.engine:
            raise RuntimeError("SQL Server not connected")

        df_clean = self._clean_for_sqlserver(df)

        with self.engine.begin() as conn:
            df_clean.to_sql(
                name=table_name,
                con=conn,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=1000,
            )

        return len(df_clean)

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

    def _clean_for_sqlserver(self, df: pd.DataFrame) -> pd.DataFrame:
        df_clean = df.copy()

        # Handle datetime columns
        for col in df_clean.columns:
            if pd.api.types.is_datetime64_any_dtype(df_clean[col]):
                df_clean[col] = (
                    df_clean[col].dt.strftime("%Y-%m-%d %H:%M:%S").replace("NaT", None)
                )

        # Replace NaN with None
        df_clean = df_clean.where(pd.notnull(df_clean), None)
        return df_clean


class SQLiteManager:
    """SQLite Fallback Manager"""

    def __init__(self, db_file: str = "excel_data_fallback.db"):
        self.db_file = Path(db_file)
        self.connection: Optional[sqlite3.Connection] = None

    def connect(self) -> bool:
        try:
            self.connection = sqlite3.connect(self.db_file)
            print(f"✅ SQLite fallback: {self.db_file}")
            return True
        except Exception as e:
            print(f"❌ SQLite failed: {e}")
            return False

    def test(self) -> bool:
        if not self.connection and not self.connect():
            return False

        try:
            if self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT 1")
                return cursor.fetchone()[0] == 1
            return False
        except:
            return False

    def create_table_from_dataframe(
        self, table_name: str, df: pd.DataFrame, type_mapping: Optional[dict] = None
    ) -> None:
        if not self.connection:
            raise RuntimeError("SQLite not connected")

        # Drop existing table
        self.connection.execute(f"DROP TABLE IF EXISTS {table_name}")

        # Create table with auto-increment ID
        df_with_id = df.copy()
        df_with_id.to_sql(table_name, self.connection, index=False, if_exists="replace")

        print(f"✅ SQLite table '{table_name}' created")

    def bulk_insert(self, table_name: str, df: pd.DataFrame) -> int:
        if not self.connection:
            raise RuntimeError("SQLite not connected")

        df.to_sql(table_name, self.connection, index=False, if_exists="append")
        return len(df)


class HybridDatabaseManager:
    """Hybrid Manager - SQL Server primary, SQLite fallback"""

    def __init__(
        self, config: DatabaseConfig, fallback_db: str = "excel_data_fallback.db"
    ):
        self.config = config
        self.sqlserver = SQLServerManager(config)
        self.sqlite = SQLiteManager(fallback_db)
        self.active_db: Optional[DatabaseInterface] = None
        self.db_type: str = "unknown"

    def connect(self) -> bool:
        """พยายาม SQL Server ก่อน ถ้าไม่ได้ใช้ SQLite"""
        print("🔍 Attempting SQL Server connection...")

        if self.sqlserver.connect():
            self.active_db = self.sqlserver
            self.db_type = "sqlserver"
            return True

        print("⚠️ SQL Server unavailable, falling back to SQLite...")

        if self.sqlite.connect():
            self.active_db = self.sqlite
            self.db_type = "sqlite"
            return True

        return False

    def test(self) -> bool:
        if not self.active_db:
            return self.connect()
        return self.active_db.test()

    def create_table_from_dataframe(
        self, table_name: str, df: pd.DataFrame, type_mapping: Optional[dict] = None
    ) -> None:
        if not self.active_db:
            raise RuntimeError("No database connected")

        self.active_db.create_table_from_dataframe(table_name, df, type_mapping)

        if self.db_type == "sqlite":
            print(f"💡 Data saved to SQLite. Migrate to SQL Server later with:")
            print(f'   sqlite3 {self.sqlite.db_file} ".dump" | sql-server-import-tool')

    def bulk_insert(self, table_name: str, df: pd.DataFrame) -> int:
        if not self.active_db:
            raise RuntimeError("No database connected")

        rows = self.active_db.bulk_insert(table_name, df)

        if self.db_type == "sqlite":
            print(f"📊 {rows:,} rows → SQLite (fallback)")
        else:
            print(f"📊 {rows:,} rows → SQL Server")

        return rows

    def get_status(self) -> dict:
        return {
            "active_database": self.db_type,
            "sql_server_available": self.sqlserver.test(),
            "sqlite_fallback": (
                self.sqlite.db_file if self.db_type == "sqlite" else None
            ),
        }


# แก้ไข database.py ให้ใช้ HybridDatabaseManager
def create_database_manager(config: DatabaseConfig) -> HybridDatabaseManager:
    """Factory function สำหรับสร้าง database manager"""
    return HybridDatabaseManager(config)
