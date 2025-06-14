"""
core/database_manager.py
Enhanced Database Manager with Full SQL Server & SQLite Support
"""

import sqlite3
import logging
from typing import Optional, Dict, Any, List, Tuple

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Enhanced Database Manager"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.connection = None
        self.db_type = config.get("db_type", "sqlite")

    def connect(self) -> Tuple[bool, str]:
        """Connect to database"""
        try:
            if self.db_type == "sqlite":
                return self._connect_sqlite()
            elif self.db_type == "sqlserver":
                return self._connect_sqlserver()
            else:
                return False, f"Unsupported database type: {self.db_type}"
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False, str(e)

    def _connect_sqlite(self) -> Tuple[bool, str]:
        """Connect to SQLite database"""
        try:
            db_file = self.config.get("sqlite_file", "denso888_data.db")
            self.connection = sqlite3.connect(db_file, check_same_thread=False)
            self.connection.execute("SELECT 1")
            return True, f"SQLite connected: {db_file}"
        except Exception as e:
            return False, f"SQLite connection failed: {e}"

    def _connect_sqlserver(self) -> Tuple[bool, str]:
        """Connect to SQL Server database"""
        try:
            import pyodbc

            server = self.config.get("server", "")
            database = self.config.get("database", "")

            if self.config.get("use_windows_auth", True):
                conn_str = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={server};"
                    f"DATABASE={database};"
                    f"Trusted_Connection=yes;"
                )
            else:
                username = self.config.get("username", "")
                password = self.config.get("password", "")
                conn_str = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={server};"
                    f"DATABASE={database};"
                    f"UID={username};"
                    f"PWD={password};"
                )

            self.connection = pyodbc.connect(conn_str, timeout=10)
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()

            return True, f"SQL Server connected: {server}/{database}"

        except ImportError:
            return (
                False,
                "pyodbc module not installed. Install with: pip install pyodbc",
            )
        except Exception as e:
            return False, f"SQL Server connection failed: {e}"

    def test_connection(self) -> Tuple[bool, str]:
        """Test database connection"""
        return self.connect()

    def create_table_from_data(
        self, table_name: str, data: List[Dict], column_mappings: Optional[Dict] = None
    ) -> Tuple[bool, str]:
        """Create table from data with optional column mappings"""
        try:
            if not data:
                return False, "No data provided"

            # Get columns from first row
            sample_row = data[0]
            columns = list(sample_row.keys())

            # Apply column mappings if provided
            if column_mappings:
                columns = [column_mappings.get(col, col) for col in columns]

            # Create table SQL
            if self.db_type == "sqlite":
                create_sql = self._create_sqlite_table(table_name, sample_row, columns)
            else:
                create_sql = self._create_sqlserver_table(
                    table_name, sample_row, columns
                )

            cursor = self.connection.cursor()

            # Drop existing table
            if self.db_type == "sqlite":
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            else:
                cursor.execute(
                    f"IF OBJECT_ID('{table_name}', 'U') IS NOT NULL DROP TABLE {table_name}"
                )

            # Create new table
            cursor.execute(create_sql)
            self.connection.commit()
            cursor.close()

            return True, f"Table '{table_name}' created successfully"

        except Exception as e:
            logger.error(f"Failed to create table: {e}")
            return False, str(e)

    def _create_sqlite_table(
        self, table_name: str, sample_row: Dict, columns: List[str]
    ) -> str:
        """Create SQLite table SQL"""
        column_defs = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]

        for i, (orig_col, new_col) in enumerate(zip(sample_row.keys(), columns)):
            value = sample_row[orig_col]

            if isinstance(value, int):
                col_type = "INTEGER"
            elif isinstance(value, float):
                col_type = "REAL"
            elif isinstance(value, bool):
                col_type = "BOOLEAN"
            else:
                col_type = "TEXT"

            column_defs.append(f"[{new_col}] {col_type}")

        return f"CREATE TABLE [{table_name}] ({', '.join(column_defs)})"

    def _create_sqlserver_table(
        self, table_name: str, sample_row: Dict, columns: List[str]
    ) -> str:
        """Create SQL Server table SQL"""
        column_defs = ["id INT IDENTITY(1,1) PRIMARY KEY"]

        for i, (orig_col, new_col) in enumerate(zip(sample_row.keys(), columns)):
            value = sample_row[orig_col]

            if isinstance(value, int):
                col_type = "INT"
            elif isinstance(value, float):
                col_type = "FLOAT"
            elif isinstance(value, bool):
                col_type = "BIT"
            else:
                col_type = "NVARCHAR(255)"

            column_defs.append(f"[{new_col}] {col_type}")

        return f"CREATE TABLE [{table_name}] ({', '.join(column_defs)})"

    def insert_data(
        self, table_name: str, data: List[Dict], column_mappings: Optional[Dict] = None
    ) -> Tuple[bool, str]:
        """Insert data into table"""
        try:
            if not data:
                return False, "No data to insert"

            # Get columns
            sample_row = data[0]
            orig_columns = list(sample_row.keys())

            # Apply column mappings if provided
            if column_mappings:
                mapped_columns = [column_mappings.get(col, col) for col in orig_columns]
            else:
                mapped_columns = orig_columns

            # Prepare insert SQL
            placeholders = ", ".join(["?" for _ in mapped_columns])
            columns_str = ", ".join([f"[{col}]" for col in mapped_columns])
            insert_sql = (
                f"INSERT INTO [{table_name}] ({columns_str}) VALUES ({placeholders})"
            )

            cursor = self.connection.cursor()

            # Insert data in batches
            batch_size = 1000
            total_inserted = 0

            for i in range(0, len(data), batch_size):
                batch = data[i : i + batch_size]
                batch_values = []

                for row in batch:
                    values = [row.get(col) for col in orig_columns]
                    batch_values.append(values)

                cursor.executemany(insert_sql, batch_values)
                total_inserted += len(batch)

            self.connection.commit()
            cursor.close()

            return True, f"Inserted {total_inserted:,} rows into '{table_name}'"

        except Exception as e:
            logger.error(f"Failed to insert data: {e}")
            return False, str(e)

    def get_tables(self) -> List[str]:
        """Get list of tables"""
        try:
            cursor = self.connection.cursor()

            if self.db_type == "sqlite":
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
                )
            else:
                cursor.execute(
                    "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"
                )

            tables = [row[0] for row in cursor.fetchall()]
            cursor.close()

            return tables

        except Exception as e:
            logger.error(f"Failed to get tables: {e}")
            return []

    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get table information"""
        try:
            cursor = self.connection.cursor()

            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM [{table_name}]")
            row_count = cursor.fetchone()[0]

            # Get column info
            if self.db_type == "sqlite":
                cursor.execute(f"PRAGMA table_info([{table_name}])")
                columns = [
                    {"name": row[1], "type": row[2]} for row in cursor.fetchall()
                ]
            else:
                cursor.execute(
                    """
                    SELECT COLUMN_NAME, DATA_TYPE 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = ?
                """,
                    (table_name,),
                )
                columns = [
                    {"name": row[0], "type": row[1]} for row in cursor.fetchall()
                ]

            cursor.close()

            return {
                "table_name": table_name,
                "row_count": row_count,
                "column_count": len(columns),
                "columns": columns,
                "database_type": self.db_type,
            }

        except Exception as e:
            logger.error(f"Failed to get table info: {e}")
            return {"error": str(e)}

    def close(self):
        """Close database connection"""
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
            except Exception as e:
                logger.error(f"Error closing connection: {e}")
