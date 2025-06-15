"""
core/database_manager.py
Working Database Manager with Real Implementation - Fixed Version
"""

import sqlite3
import logging
import os
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Working Database Manager with real SQLite support"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.connection = None
        self.db_type = config.get("db_type", "sqlite")
        self.db_file_path = None

    def connect(self) -> Tuple[bool, str]:
        """Connect to database and return success status"""
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
            # Get database file path
            db_file = self.config.get("sqlite_file", "denso888_data.db")

            # Ensure absolute path
            if not os.path.isabs(db_file):
                db_file = os.path.abspath(db_file)

            # Ensure directory exists
            db_dir = os.path.dirname(db_file)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)

            # Store file path for reference
            self.db_file_path = db_file

            # Connect to database
            self.connection = sqlite3.connect(db_file, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row  # Enable column access by name

            # Test connection
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()

            # Create metadata table if not exists
            self._create_metadata_table()

            file_size = os.path.getsize(db_file) if os.path.exists(db_file) else 0
            return True, f"SQLite connected: {db_file} (Size: {file_size} bytes)"

        except Exception as e:
            return False, f"SQLite connection failed: {e}"

    def _connect_sqlserver(self) -> Tuple[bool, str]:
        """Connect to SQL Server database"""
        try:
            # Try to import pyodbc
            try:
                import pyodbc
            except ImportError:
                return (
                    False,
                    "pyodbc module not installed. Install with: pip install pyodbc",
                )

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

    def _create_metadata_table(self):
        """Create metadata table for tracking operations"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS denso888_metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_type TEXT NOT NULL,
                    table_name TEXT NOT NULL,
                    created_date TEXT NOT NULL,
                    record_count INTEGER DEFAULT 0,
                    source_info TEXT,
                    notes TEXT
                )
            """
            )
            self.connection.commit()
            cursor.close()
        except Exception as e:
            logger.error(f"Failed to create metadata table: {e}")

    def test_connection(self) -> Tuple[bool, str]:
        """Test database connection"""
        return self.connect()

    def create_table_from_data(
        self, table_name: str, data: List[Dict], column_mappings: Optional[Dict] = None
    ) -> Tuple[bool, str]:
        """Create table from data with enhanced error handling"""
        try:
            if not data:
                return False, "No data provided"

            if not self.connection:
                return False, "Database not connected"

            # Get columns from first row
            sample_row = data[0]
            original_columns = list(sample_row.keys())

            # Apply column mappings if provided
            if column_mappings:
                mapped_columns = [
                    column_mappings.get(col, col) for col in original_columns
                ]
            else:
                mapped_columns = [
                    self._clean_column_name(col) for col in original_columns
                ]

            # Create table SQL
            if self.db_type == "sqlite":
                create_sql = self._create_sqlite_table(
                    table_name, sample_row, mapped_columns
                )
            else:
                create_sql = self._create_sqlserver_table(
                    table_name, sample_row, mapped_columns
                )

            cursor = self.connection.cursor()

            # Drop existing table if exists
            if self.db_type == "sqlite":
                cursor.execute(f"DROP TABLE IF EXISTS [{table_name}]")
            else:
                cursor.execute(
                    f"IF OBJECT_ID('{table_name}', 'U') IS NOT NULL DROP TABLE [{table_name}]"
                )

            # Create new table
            cursor.execute(create_sql)
            self.connection.commit()
            cursor.close()

            # Log operation in metadata
            self._log_operation(
                "table_create", table_name, len(data), f"Columns: {len(mapped_columns)}"
            )

            return (
                True,
                f"Table '{table_name}' created successfully with {len(mapped_columns)} columns",
            )

        except Exception as e:
            logger.error(f"Failed to create table: {e}")
            return False, str(e)

    def _clean_column_name(self, name: str) -> str:
        """Clean column name for database use"""
        import re

        # Convert to string and strip
        clean_name = str(name).strip()

        # Replace special characters with underscore
        clean_name = re.sub(r"[^\w\s]", "_", clean_name)

        # Replace spaces with underscore
        clean_name = re.sub(r"\s+", "_", clean_name)

        # Remove multiple underscores
        clean_name = re.sub(r"_+", "_", clean_name)

        # Remove leading/trailing underscores
        clean_name = clean_name.strip("_").lower()

        # Ensure not empty
        if not clean_name:
            clean_name = "column"

        # Handle reserved keywords
        reserved_words = {"index", "order", "group", "select", "from", "where"}
        if clean_name in reserved_words:
            clean_name = f"{clean_name}_col"

        return clean_name

    def _create_sqlite_table(
        self, table_name: str, sample_row: Dict, columns: List[str]
    ) -> str:
        """Create SQLite table SQL with better type detection"""
        column_defs = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]

        for i, (orig_col, new_col) in enumerate(zip(sample_row.keys(), columns)):
            value = sample_row[orig_col]

            # Enhanced type detection
            if value is None:
                col_type = "TEXT"
            elif isinstance(value, bool):
                col_type = "BOOLEAN"
            elif isinstance(value, int):
                col_type = "INTEGER"
            elif isinstance(value, float):
                col_type = "REAL"
            elif isinstance(value, str):
                # Check if string looks like date
                if self._looks_like_date(value):
                    col_type = "TEXT"  # Store dates as text in SQLite
                else:
                    col_type = "TEXT"
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

            if value is None:
                col_type = "NVARCHAR(255)"
            elif isinstance(value, bool):
                col_type = "BIT"
            elif isinstance(value, int):
                col_type = "INT"
            elif isinstance(value, float):
                col_type = "FLOAT"
            elif isinstance(value, str):
                if self._looks_like_date(value):
                    col_type = "DATETIME2"
                else:
                    col_type = "NVARCHAR(255)"
            else:
                col_type = "NVARCHAR(255)"

            column_defs.append(f"[{new_col}] {col_type}")

        return f"CREATE TABLE [{table_name}] ({', '.join(column_defs)})"

    def _looks_like_date(self, value: str) -> bool:
        """Check if string value looks like a date"""
        if not isinstance(value, str):
            return False

        import re

        date_patterns = [
            r"\d{4}-\d{2}-\d{2}",  # YYYY-MM-DD
            r"\d{2}/\d{2}/\d{4}",  # MM/DD/YYYY
            r"\d{2}-\d{2}-\d{4}",  # MM-DD-YYYY
        ]

        for pattern in date_patterns:
            if re.match(pattern, value.strip()):
                return True
        return False

    def insert_data(
        self, table_name: str, data: List[Dict], column_mappings: Optional[Dict] = None
    ) -> Tuple[bool, str]:
        """Insert data into table with progress tracking"""
        try:
            if not data:
                return False, "No data to insert"

            if not self.connection:
                return False, "Database not connected"

            # Get columns
            sample_row = data[0]
            orig_columns = list(sample_row.keys())

            # Apply column mappings if provided
            if column_mappings:
                mapped_columns = [column_mappings.get(col, col) for col in orig_columns]
            else:
                mapped_columns = [self._clean_column_name(col) for col in orig_columns]

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
                    values = []
                    for col in orig_columns:
                        value = row.get(col)
                        # Handle None values
                        if value is None:
                            values.append(None)
                        else:
                            values.append(value)
                    batch_values.append(values)

                cursor.executemany(insert_sql, batch_values)
                total_inserted += len(batch)

            self.connection.commit()
            cursor.close()

            # Log operation in metadata
            self._log_operation("data_insert", table_name, total_inserted)

            return True, f"Inserted {total_inserted:,} rows into '{table_name}'"

        except Exception as e:
            logger.error(f"Failed to insert data: {e}")
            return False, str(e)

    def _log_operation(
        self,
        operation_type: str,
        table_name: str,
        record_count: int = 0,
        notes: str = "",
    ):
        """Log operation in metadata table"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                INSERT INTO denso888_metadata 
                (operation_type, table_name, created_date, record_count, notes)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    operation_type,
                    table_name,
                    datetime.now().isoformat(),
                    record_count,
                    notes,
                ),
            )
            self.connection.commit()
            cursor.close()
        except Exception as e:
            logger.error(f"Failed to log operation: {e}")

    def get_tables(self) -> List[str]:
        """Get list of tables"""
        try:
            if not self.connection:
                return []

            cursor = self.connection.cursor()

            if self.db_type == "sqlite":
                cursor.execute(
                    """
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name NOT LIKE 'sqlite_%' 
                    AND name != 'denso888_metadata'
                """
                )
            else:
                cursor.execute(
                    """
                    SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_TYPE='BASE TABLE' AND TABLE_NAME != 'denso888_metadata'
                """
                )

            tables = [row[0] for row in cursor.fetchall()]
            cursor.close()

            return tables

        except Exception as e:
            logger.error(f"Failed to get tables: {e}")
            return []

    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get detailed table information"""
        try:
            if not self.connection:
                return {"error": "Database not connected"}

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
                "database_file": (
                    self.db_file_path if self.db_type == "sqlite" else None
                ),
            }

        except Exception as e:
            logger.error(f"Failed to get table info: {e}")
            return {"error": str(e)}

    def get_recent_operations(self, limit: int = 10) -> List[Dict]:
        """Get recent database operations"""
        try:
            if not self.connection:
                return []

            cursor = self.connection.cursor()
            cursor.execute(
                """
                SELECT operation_type, table_name, created_date, record_count, notes
                FROM denso888_metadata 
                ORDER BY id DESC 
                LIMIT ?
            """,
                (limit,),
            )

            operations = []
            for row in cursor.fetchall():
                operations.append(
                    {
                        "operation_type": row[0],
                        "table_name": row[1],
                        "created_date": row[2],
                        "record_count": row[3],
                        "notes": row[4] or "",
                    }
                )

            cursor.close()
            return operations

        except Exception as e:
            logger.error(f"Failed to get recent operations: {e}")
            return []

    def execute_query(self, query: str) -> Tuple[bool, Any]:
        """Execute custom SQL query"""
        try:
            if not self.connection:
                return False, "Database not connected"

            cursor = self.connection.cursor()
            cursor.execute(query)

            if query.strip().upper().startswith("SELECT"):
                result = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                cursor.close()
                return True, {"columns": columns, "rows": result}
            else:
                self.connection.commit()
                affected_rows = cursor.rowcount
                cursor.close()
                return True, f"Query executed, {affected_rows} rows affected"

        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return False, str(e)

    def get_database_stats(self) -> Dict[str, Any]:
        """Get comprehensive database statistics"""
        try:
            stats = {
                "database_type": self.db_type,
                "connected": self.connection is not None,
                "file_path": self.db_file_path if self.db_type == "sqlite" else None,
                "total_tables": 0,
                "total_records": 0,
                "database_size": 0,
            }

            if not self.connection:
                return stats

            # Get table count and total records
            tables = self.get_tables()
            stats["total_tables"] = len(tables)

            total_records = 0
            for table in tables:
                try:
                    cursor = self.connection.cursor()
                    cursor.execute(f"SELECT COUNT(*) FROM [{table}]")
                    count = cursor.fetchone()[0]
                    total_records += count
                    cursor.close()
                except:
                    pass

            stats["total_records"] = total_records

            # Get database file size for SQLite
            if (
                self.db_type == "sqlite"
                and self.db_file_path
                and os.path.exists(self.db_file_path)
            ):
                stats["database_size"] = os.path.getsize(self.db_file_path)

            return stats

        except Exception as e:
            logger.error(f"Failed to get database stats: {e}")
            return {"error": str(e)}

    def close(self):
        """Close database connection"""
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
                self.db_file_path = None
            except Exception as e:
                logger.error(f"Error closing connection: {e}")

    def backup_database(self, backup_path: str) -> Tuple[bool, str]:
        """Create database backup"""
        try:
            if self.db_type != "sqlite":
                return False, "Backup only supported for SQLite databases"

            if not self.db_file_path or not os.path.exists(self.db_file_path):
                return False, "Source database file not found"

            import shutil

            shutil.copy2(self.db_file_path, backup_path)

            backup_size = os.path.getsize(backup_path)
            return (
                True,
                f"Database backed up to {backup_path} (Size: {backup_size} bytes)",
            )

        except Exception as e:
            return False, f"Backup failed: {str(e)}"
