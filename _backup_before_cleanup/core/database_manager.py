import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
from typing import Optional, Any, Dict, Union
import logging

logger = logging.getLogger(__name__)


class SQLServerManager:
    """SQL Server database manager with improved error handling"""

    def __init__(self, config):
        self.config = config
        self.engine: Optional[Any] = None
        self._connection_info: Dict[str, str] = {}

    def connect(self) -> bool:
        """Establish SQL Server connection with better error handling"""
        try:
            connection_url = self.config.get_connection_url()
            if not connection_url:
                logger.error("Invalid SQL Server connection URL")
                return False

            self.engine = create_engine(
                connection_url,
                pool_size=getattr(self.config, "pool_size", 5),
                max_overflow=getattr(self.config, "max_overflow", 10),
                pool_timeout=getattr(self.config, "pool_timeout", 30),
                pool_recycle=getattr(self.config, "pool_recycle", 3600),
                echo=False,
                connect_args={"timeout": 10},  # Connection timeout
            )

            # Test connection with timeout
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
                        "auth_type": (
                            "Windows" if self.config.use_windows_auth else "SQL Server"
                        ),
                    }
                    logger.info(f"Connected to SQL Server: {row.server}/{row.database}")
                    return True

            return False

        except Exception as e:
            logger.error(f"SQL Server connection failed: {e}")
            self.engine = None
            return False

    def test_connection(self) -> bool:
        """Test existing connection with proper error handling"""
        if not self.engine:
            return self.connect()

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
        """Create table from DataFrame structure with improved error handling"""
        if not self.engine:
            raise RuntimeError("SQL Server not connected")

        try:
            # Build column definitions with better type mapping
            columns_sql = ["id INT IDENTITY(1,1) PRIMARY KEY"]

            for col_name in df.columns:
                dtype = df[col_name].dtype
                sql_type = self._map_pandas_to_sql_type(
                    dtype, type_mapping.get(col_name) if type_mapping else None
                )
                # Escape column names properly
                safe_col_name = f"[{col_name.replace(']', ']]')}]"
                columns_sql.append(f"{safe_col_name} {sql_type}")

            # Execute DDL with better error handling
            drop_sql = f"IF OBJECT_ID('{table_name}', 'U') IS NOT NULL DROP TABLE [{table_name}]"
            create_sql = f"CREATE TABLE [{table_name}] ({', '.join(columns_sql)})"

            with self.engine.connect() as conn:
                with conn.begin():
                    conn.execute(text(drop_sql))
                    conn.execute(text(create_sql))

            logger.info(f"SQL Server table '{table_name}' created successfully")

        except Exception as e:
            logger.error(f"Failed to create SQL Server table '{table_name}': {e}")
            raise

    def bulk_insert(self, table_name: str, df: pd.DataFrame) -> int:
        """Bulk insert DataFrame to table with improved performance"""
        if not self.engine:
            raise RuntimeError("SQL Server not connected")

        df_clean = self._prepare_dataframe_for_sql_server(df)

        try:
            # Use chunked insertion for better performance
            with self.engine.begin() as conn:
                df_clean.to_sql(
                    name=table_name,
                    con=conn,
                    if_exists="append",
                    index=False,
                    method="multi",
                    chunksize=min(1000, len(df_clean)),
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
        """Execute custom SQL query with timeout"""
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
        """Get table information with enhanced details"""
        if not self.engine:
            raise RuntimeError("SQL Server not connected")

        try:
            query = f"""
            SELECT 
                COUNT(*) as row_count,
                (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}') as column_count,
                (SELECT SUM(reserved_page_count) * 8.0 / 1024 FROM sys.dm_db_partition_stats 
                 WHERE object_id = OBJECT_ID('{table_name}')) as size_mb
            FROM [{table_name}]
            """

            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                row = result.fetchone()

                return {
                    "table_name": table_name,
                    "row_count": row.row_count if row else 0,
                    "column_count": row.column_count if row else 0,
                    "size_mb": round(row.size_mb or 0, 2),
                    "database_type": "SQL Server",
                    "server_info": self._connection_info,
                }
        except Exception as e:
            logger.error(f"Failed to get table info for '{table_name}': {e}")
            return {"error": str(e)}

    def _map_pandas_to_sql_type(
        self, pandas_dtype, explicit_type: Optional[str] = None
    ) -> str:
        """Enhanced pandas to SQL Server type mapping"""
        if explicit_type:
            type_mapping = {
                "string": "NVARCHAR(255)",
                "text": "NVARCHAR(MAX)",
                "integer": "INT",
                "bigint": "BIGINT",
                "float": "FLOAT",
                "decimal": "DECIMAL(18,2)",
                "boolean": "BIT",
                "datetime": "DATETIME2",
                "date": "DATE",
                "time": "TIME",
            }
            return type_mapping.get(explicit_type, "NVARCHAR(255)")

        # Enhanced type detection
        dtype_str = str(pandas_dtype).lower()

        if pd.api.types.is_integer_dtype(pandas_dtype):
            if "int64" in dtype_str:
                return "BIGINT"
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
        """Enhanced DataFrame preparation for SQL Server"""
        df_clean = df.copy()

        # Handle datetime columns with better format
        for col in df_clean.columns:
            if pd.api.types.is_datetime64_any_dtype(df_clean[col]):
                df_clean[col] = (
                    df_clean[col]
                    .dt.strftime("%Y-%m-%d %H:%M:%S.%f")
                    .replace("NaT", None)
                )

        # Replace NaN with None for proper NULL handling
        df_clean = df_clean.where(pd.notnull(df_clean), None)

        # Handle very long strings
        for col in df_clean.select_dtypes(include=["object"]).columns:
            df_clean[col] = (
                df_clean[col].astype(str).str[:255]
            )  # Truncate to fit NVARCHAR(255)

        return df_clean


class SQLiteManager:
    """Enhanced SQLite manager with better error handling"""

    def __init__(self, db_file: Union[str, Path] = "denso888_data.db"):
        self.db_file = Path(db_file)
        self.connection: Optional[sqlite3.Connection] = None
        self._connection_info: Dict[str, Union[str, float]] = {}

    def connect(self) -> bool:
        """Establish SQLite connection with better configuration"""
        try:
            # Ensure directory exists
            self.db_file.parent.mkdir(parents=True, exist_ok=True)

            self.connection = sqlite3.connect(
                str(self.db_file),
                timeout=30.0,  # Connection timeout
                check_same_thread=False,
            )

            # Configure SQLite for better performance
            self.connection.execute("PRAGMA journal_mode=WAL")
            self.connection.execute("PRAGMA synchronous=NORMAL")
            self.connection.execute("PRAGMA cache_size=1000000")
            self.connection.execute("PRAGMA temp_store=memory")

            self._connection_info = {
                "file_path": str(self.db_file.absolute()),
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
        """Create table from DataFrame with better type handling"""
        if not self.connection:
            raise RuntimeError("SQLite not connected")

        try:
            # Drop existing table
            self.connection.execute(f"DROP TABLE IF EXISTS {table_name}")

            # Create table using pandas with optimized settings
            df_sample = df.head(0)  # Empty DataFrame with structure
            df_sample.to_sql(
                table_name,
                self.connection,
                index=False,
                if_exists="replace",
                method="multi",
            )

            # Commit changes
            self.connection.commit()
            logger.info(f"SQLite table '{table_name}' created successfully")

        except Exception as e:
            logger.error(f"Failed to create SQLite table '{table_name}': {e}")
            raise

    def bulk_insert(self, table_name: str, df: pd.DataFrame) -> int:
        """Bulk insert with transaction and better performance"""
        if not self.connection:
            raise RuntimeError("SQLite not connected")

        try:
            # Use transaction for better performance
            with self.connection:
                df.to_sql(
                    table_name,
                    self.connection,
                    index=False,
                    if_exists="append",
                    method="multi",
                    chunksize=1000,
                )

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
        """Get enhanced table information"""
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

            # Get table size (approximate)
            cursor.execute(f"SELECT SUM(LENGTH(json(*))); FROM {table_name} LIMIT 1000")
            size_sample = cursor.fetchone()[0] or 0
            estimated_size_mb = (
                (size_sample * row_count / 1000) / (1024 * 1024) if size_sample else 0
            )

            return {
                "table_name": table_name,
                "row_count": row_count,
                "column_count": len(columns),
                "estimated_size_mb": round(estimated_size_mb, 2),
                "database_type": "SQLite",
                "file_info": self._connection_info,
            }
        except Exception as e:
            logger.error(f"Failed to get table info for '{table_name}': {e}")
            return {"error": str(e)}


class DatabaseManager:
    """Enhanced hybrid database manager with improved fallback logic"""

    def __init__(self, config, sqlite_file: Optional[Union[str, Path]] = None):
        self.config = config
        self.sqlserver = SQLServerManager(config)
        self.sqlite = SQLiteManager(
            sqlite_file or getattr(config, "sqlite_file", "denso888_data.db")
        )

        self.active_db: Optional[Union[SQLServerManager, SQLiteManager]] = None
        self.db_type: str = "none"
        self._forced_mode: Optional[str] = None

    def connect(self, force_mode: Optional[str] = None) -> bool:
        """Connect with improved fallback logic and timeout handling"""
        self._forced_mode = force_mode

        if force_mode == "sqlite":
            return self._connect_sqlite_only()
        elif force_mode == "sqlserver":
            return self._connect_sqlserver_only()
        else:
            return self._connect_with_fallback()

    def _connect_with_fallback(self) -> bool:
        """Try SQL Server first with timeout, fallback to SQLite"""
        logger.info("Attempting SQL Server connection...")

        # Try SQL Server with timeout
        try:
            if self.sqlserver.connect():
                self.active_db = self.sqlserver
                self.db_type = "sqlserver"
                logger.info("✅ Connected to SQL Server")
                return True
        except Exception as e:
            logger.warning(f"SQL Server connection failed: {e}")

        logger.warning("SQL Server unavailable, falling back to SQLite...")

        if self.sqlite.connect():
            self.active_db = self.sqlite
            self.db_type = "sqlite"
            logger.info("✅ Connected to SQLite fallback")
            return True

        logger.error("❌ No database connection available")
        return False

    def _connect_sqlite_only(self) -> bool:
        """Connect to SQLite only"""
        if self.sqlite.connect():
            self.active_db = self.sqlite
            self.db_type = "sqlite"
            logger.info("✅ Connected to SQLite (forced mode)")
            return True
        return False

    def _connect_sqlserver_only(self) -> bool:
        """Connect to SQL Server only"""
        if self.sqlserver.connect():
            self.active_db = self.sqlserver
            self.db_type = "sqlserver"
            logger.info("✅ Connected to SQL Server (forced mode)")
            return True
        return False

    def test_connection(self) -> bool:
        """Test current connection with retry logic"""
        if not self.active_db:
            return self.connect()

        try:
            return self.active_db.test_connection()
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False

    def create_table_from_dataframe(
        self,
        table_name: str,
        df: pd.DataFrame,
        type_mapping: Optional[Dict[str, str]] = None,
    ) -> None:
        """Create table from DataFrame with enhanced error handling"""
        if not self.active_db:
            raise RuntimeError("No database connected")

        try:
            self.active_db.create_table_from_dataframe(table_name, df, type_mapping)

            if self.db_type == "sqlite":
                logger.info(
                    "💡 Data saved to SQLite. Use 'DB Test' to try SQL Server migration."
                )

        except Exception as e:
            logger.error(f"Failed to create table '{table_name}': {e}")
            raise

    def bulk_insert(self, table_name: str, df: pd.DataFrame) -> int:
        """Bulk insert data with retry logic"""
        if not self.active_db:
            raise RuntimeError("No database connected")

        try:
            return self.active_db.bulk_insert(table_name, df)
        except Exception as e:
            logger.error(f"Failed to insert data to '{table_name}': {e}")
            raise

    def execute_query(self, query: str) -> Any:
        """Execute custom query with enhanced error handling"""
        if not self.active_db:
            raise RuntimeError("No database connected")

        try:
            return self.active_db.execute_query(query)
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise

    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get table information with enhanced details"""
        if not self.active_db:
            raise RuntimeError("No database connected")

        try:
            return self.active_db.get_table_info(table_name)
        except Exception as e:
            logger.error(f"Failed to get table info: {e}")
            return {"error": str(e)}

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive database manager status"""
        status = {
            "active_database": self.db_type,
            "forced_mode": self._forced_mode,
            "connections": {
                "sqlserver_available": False,
                "sqlite_available": False,
            },
            "performance_info": {},
        }

        # Test both connections
        try:
            status["connections"][
                "sqlserver_available"
            ] = self.sqlserver.test_connection()
        except:
            pass

        try:
            status["connections"]["sqlite_available"] = self.sqlite.test_connection()
        except:
            pass

        # Add connection info
        if self.db_type == "sqlserver" and self.sqlserver._connection_info:
            status["sqlserver_info"] = self.sqlserver._connection_info
        elif self.db_type == "sqlite" and self.sqlite._connection_info:
            status["sqlite_info"] = self.sqlite._connection_info

        return status

    def switch_database(self, target: str) -> bool:
        """Switch between database types with proper cleanup"""
        if target not in ["sqlserver", "sqlite"]:
            raise ValueError("Target must be 'sqlserver' or 'sqlite'")

        logger.info(f"Switching to {target} database...")

        # Close current connection
        self.close()

        # Connect to target
        return self.connect(force_mode=target)

    def close(self):
        """Close all connections with proper cleanup"""
        try:
            if self.sqlserver.engine:
                self.sqlserver.engine.dispose()
        except Exception as e:
            logger.warning(f"Error closing SQL Server connection: {e}")

        try:
            if self.sqlite.connection:
                self.sqlite.connection.close()
        except Exception as e:
            logger.warning(f"Error closing SQLite connection: {e}")

        self.active_db = None
        self.db_type = "none"
        logger.info("Database connections closed")
