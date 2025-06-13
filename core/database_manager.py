import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
from typing import Optional, Any, Dict, Union
import logging

logger = logging.getLogger(__name__)


class SQLServerManager:
    """SQL Server database manager"""

    def __init__(self, config):
        self.config = config
        self.engine: Optional[Any] = None
        self._connection_info: Dict[str, str] = {}

    def connect(self) -> bool:
        """Establish SQL Server connection"""
        try:
            self.engine = create_engine(
                self.config.get_connection_url(),
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
                pool_timeout=self.config.pool_timeout,
                pool_recycle=self.config.pool_recycle,
                echo=False,
            )

            # Test connection
            if not self.engine:
                return False
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("SELECT @@SERVERNAME as server, DB_NAME() as database")
                )
                row = result.fetchone()
                if row:
                    self._connection_info = {
                        "server": str(row.server),
                        "database": str(row.database),
                        "type": "SQL Server",
                    }
                    logger.info(f"Connected to SQL Server: {row.server}/{row.database}")
                    return True

            return False

        except Exception as e:
            logger.error(f"SQL Server connection failed: {e}")
            self.engine = None
            return False

    def test_connection(self) -> bool:
        """Test existing connection"""
        if not self.engine:
            if not self.connect():
                return False
            if not self.engine:  # Double check after connect attempt
                return False

        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                return result.fetchone()[0] == 1
        except Exception as e:
            logger.error(f"SQL Server connection test failed: {e}")
            return False

    def create_table_from_dataframe(
        self,
        table_name: str,
        df: pd.DataFrame,
        type_mapping: Optional[Dict[str, str]] = None,
    ) -> None:
        """Create table from DataFrame structure"""
        if not self.engine:
            raise RuntimeError("SQL Server not connected")

        # Build column definitions
        columns_sql = ["id INT IDENTITY(1,1) PRIMARY KEY"]

        for col_name in df.columns:
            dtype = df[col_name].dtype
            sql_type = self._map_pandas_to_sql_type(
                dtype, type_mapping.get(col_name) if type_mapping else None
            )
            columns_sql.append(f"[{col_name}] {sql_type}")

        # Execute DDL
        drop_sql = (
            f"IF OBJECT_ID('{table_name}', 'U') IS NOT NULL DROP TABLE [{table_name}]"
        )
        create_sql = f"CREATE TABLE [{table_name}] ({', '.join(columns_sql)})"

        try:
            with self.engine.connect() as conn:
                with conn.begin():
                    conn.execute(text(drop_sql))
                    conn.execute(text(create_sql))

            logger.info(f"SQL Server table '{table_name}' created successfully")

        except Exception as e:
            logger.error(f"Failed to create SQL Server table '{table_name}': {e}")
            raise

    def bulk_insert(self, table_name: str, df: pd.DataFrame) -> int:
        """Bulk insert DataFrame to table"""
        if not self.engine:
            raise RuntimeError("SQL Server not connected")

        df_clean = self._prepare_dataframe_for_sql_server(df)

        try:
            with self.engine.begin() as conn:
                df_clean.to_sql(
                    name=table_name,
                    con=conn,
                    if_exists="append",
                    index=False,
                    method="multi",
                    chunksize=1000,
                )

            row_count = len(df_clean)
            logger.debug(
                f"Inserted {row_count:,} rows to SQL Server table '{table_name}'"
            )
            return row_count

        except Exception as e:
            logger.error(
                f"Failed to insert data to SQL Server table '{table_name}': {e}"
            )
            raise

    def execute_query(self, query: str) -> Any:
        """Execute custom SQL query"""
        if not self.engine:
            raise RuntimeError("SQL Server not connected")

        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                return result.fetchall()
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise

    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get table information"""
        if not self.engine:
            raise RuntimeError("SQL Server not connected")

        try:
            query = f"""
            SELECT 
                COUNT(*) as row_count,
                (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}') as column_count
            FROM [{table_name}]
            """

            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                row = result.fetchone()

                return {
                    "table_name": table_name,
                    "row_count": row.row_count if row else 0,
                    "column_count": row.column_count if row else 0,
                    "database_type": "SQL Server",
                    "server_info": self._connection_info,
                }
        except Exception as e:
            logger.error(f"Failed to get table info for '{table_name}': {e}")
            return {"error": str(e)}

    def _map_pandas_to_sql_type(
        self, pandas_dtype, explicit_type: Optional[str] = None
    ) -> str:
        """Map pandas dtype to SQL Server type"""
        if explicit_type:
            type_mapping = {
                "string": "NVARCHAR(255)",
                "text": "NVARCHAR(MAX)",
                "integer": "INT",
                "float": "FLOAT",
                "boolean": "BIT",
                "datetime": "DATETIME2",
            }
            return type_mapping.get(explicit_type, "NVARCHAR(255)")

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

    def _prepare_dataframe_for_sql_server(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare DataFrame for SQL Server insertion"""
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
    """SQLite fallback database manager"""

    def __init__(self, db_file: Union[str, Path] = "denso888_data.db"):
        self.db_file = Path(db_file)
        self.connection: Optional[sqlite3.Connection] = None
        self._connection_info: Dict[str, Union[str, float]] = {}

    def connect(self) -> bool:
        """Establish SQLite connection"""
        try:
            self.connection = sqlite3.connect(str(self.db_file))
            self._connection_info = {
                "file_path": str(self.db_file),
                "file_size_mb": (
                    self.db_file.stat().st_size / 1024 / 1024
                    if self.db_file.exists()
                    else 0
                ),
                "type": "SQLite",
            }
            logger.info(f"Connected to SQLite database: {self.db_file}")
            return True
        except Exception as e:
            logger.error(f"SQLite connection failed: {e}")
            return False

    def test_connection(self) -> bool:
        """Test existing connection"""
        if not self.connection:
            return self.connect()

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            return cursor.fetchone()[0] == 1
        except Exception as e:
            logger.error(f"SQLite connection test failed: {e}")
            return False

    def create_table_from_dataframe(
        self,
        table_name: str,
        df: pd.DataFrame,
        type_mapping: Optional[Dict[str, str]] = None,
    ) -> None:
        """Create table from DataFrame structure"""
        if not self.connection:
            raise RuntimeError("SQLite not connected")

        try:
            # Drop existing table
            self.connection.execute(f"DROP TABLE IF EXISTS {table_name}")

            # Create table using pandas to_sql
            df_sample = df.head(0)  # Empty DataFrame with structure
            df_sample.to_sql(
                table_name, self.connection, index=False, if_exists="replace"
            )

            logger.info(f"SQLite table '{table_name}' created successfully")

        except Exception as e:
            logger.error(f"Failed to create SQLite table '{table_name}': {e}")
            raise

    def bulk_insert(self, table_name: str, df: pd.DataFrame) -> int:
        """Bulk insert DataFrame to table"""
        if not self.connection:
            raise RuntimeError("SQLite not connected")

        try:
            df.to_sql(table_name, self.connection, index=False, if_exists="append")
            row_count = len(df)
            logger.debug(f"Inserted {row_count:,} rows to SQLite table '{table_name}'")
            return row_count

        except Exception as e:
            logger.error(f"Failed to insert data to SQLite table '{table_name}': {e}")
            raise

    def execute_query(self, query: str) -> Any:
        """Execute custom SQL query"""
        if not self.connection:
            raise RuntimeError("SQLite not connected")

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise

    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get table information"""
        if not self.connection:
            raise RuntimeError("SQLite not connected")

        try:
            cursor = self.connection.cursor()

            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cursor.fetchone()[0]

            # Get column info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            return {
                "table_name": table_name,
                "row_count": row_count,
                "column_count": len(columns),
                "database_type": "SQLite",
                "file_info": self._connection_info,
            }
        except Exception as e:
            logger.error(f"Failed to get table info for '{table_name}': {e}")
            return {"error": str(e)}


class DatabaseManager:
    """Hybrid database manager with SQL Server primary and SQLite fallback"""

    def __init__(self, config, sqlite_file: Optional[Union[str, Path]] = None):
        self.config = config
        self.sqlserver = SQLServerManager(config)
        self.sqlite = SQLiteManager(sqlite_file or "denso888_data.db")

        self.active_db: Optional[Union[SQLServerManager, SQLiteManager]] = None
        self.db_type: str = "none"
        self._forced_mode: Optional[str] = None

    def connect(self, force_mode: Optional[str] = None) -> bool:
        """Connect with fallback logic"""
        self._forced_mode = force_mode

        if force_mode == "sqlite":
            return self._connect_sqlite_only()
        elif force_mode == "sqlserver":
            return self._connect_sqlserver_only()
        else:
            return self._connect_with_fallback()

    def _connect_with_fallback(self) -> bool:
        """Try SQL Server first, fallback to SQLite"""
        logger.info("Attempting SQL Server connection...")

        if self.sqlserver.connect():
            self.active_db = self.sqlserver
            self.db_type = "sqlserver"
            logger.info("Connected to SQL Server")
            return True

        logger.warning("SQL Server unavailable, falling back to SQLite...")

        if self.sqlite.connect():
            self.active_db = self.sqlite
            self.db_type = "sqlite"
            logger.info("Connected to SQLite fallback")
            return True

        logger.error("No database connection available")
        return False

    def _connect_sqlite_only(self) -> bool:
        """Connect to SQLite only"""
        if self.sqlite.connect():
            self.active_db = self.sqlite
            self.db_type = "sqlite"
            return True
        return False

    def _connect_sqlserver_only(self) -> bool:
        """Connect to SQL Server only"""
        if self.sqlserver.connect():
            self.active_db = self.sqlserver
            self.db_type = "sqlserver"
            return True
        return False

    def test_connection(self) -> bool:
        """Test current connection"""
        if not self.active_db:
            return self.connect()
        return self.active_db.test_connection()

    def create_table_from_dataframe(
        self,
        table_name: str,
        df: pd.DataFrame,
        type_mapping: Optional[Dict[str, str]] = None,
    ) -> None:
        """Create table from DataFrame"""
        if not self.active_db:
            raise RuntimeError("No database connected")

        self.active_db.create_table_from_dataframe(table_name, df, type_mapping)

        if self.db_type == "sqlite":
            logger.info("💡 Data saved to SQLite. Can migrate to SQL Server later.")

    def bulk_insert(self, table_name: str, df: pd.DataFrame) -> int:
        """Bulk insert data"""
        if not self.active_db:
            raise RuntimeError("No database connected")

        return self.active_db.bulk_insert(table_name, df)

    def execute_query(self, query: str) -> Any:
        """Execute custom query"""
        if not self.active_db:
            raise RuntimeError("No database connected")

        return self.active_db.execute_query(query)

    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get table information"""
        if not self.active_db:
            raise RuntimeError("No database connected")

        return self.active_db.get_table_info(table_name)

    def get_status(self) -> Dict[str, Any]:
        """Get database manager status"""
        status = {
            "active_database": self.db_type,
            "forced_mode": self._forced_mode,
            "connections": {
                "sqlserver_available": self.sqlserver.test_connection(),
                "sqlite_available": self.sqlite.test_connection(),
            },
        }

        if self.db_type == "sqlserver":
            status["sqlserver_info"] = self.sqlserver._connection_info
        elif self.db_type == "sqlite":
            status["sqlite_info"] = self.sqlite._connection_info

        return status

    def switch_database(self, target: str) -> bool:
        """Switch between database types"""
        if target not in ["sqlserver", "sqlite"]:
            raise ValueError("Target must be 'sqlserver' or 'sqlite'")

        logger.info(f"Switching to {target} database...")
        return self.connect(force_mode=target)

    def close(self):
        """Close all connections"""
        if self.sqlserver.engine:
            self.sqlserver.engine.dispose()
        if self.sqlite.connection:
            self.sqlite.connection.close()

        self.active_db = None
        self.db_type = "none"
        logger.info("Database connections closed")
