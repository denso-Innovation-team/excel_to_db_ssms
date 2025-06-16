"""
services/database_service.py
Database Operations Service
"""

import sqlite3
import os
from typing import Dict, Any, List, Tuple
from datetime import datetime


class DatabaseService:
    """Database operations service - SQLite focus with SQL Server support"""

    def __init__(self):
        self.connection = None
        self.db_config = {}
        self.db_type = "sqlite"
        self.db_file_path = None

    def get_config(self) -> Dict[str, Any]:
        """Get current database configuration"""
        return self.db_config.copy()

    def test_connection(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Test database connection"""
        try:
            db_type = config.get("type", "sqlite")

            if db_type == "sqlite":
                return self._test_sqlite(config)
            elif db_type == "sqlserver":
                return self._test_sqlserver(config)
            else:
                return False, f"Unsupported database type: {db_type}"

        except Exception as e:
            return False, str(e)

    def _test_sqlite(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Test SQLite connection"""
        try:
            db_file = config.get("file", "denso888.db")

            # Ensure absolute path
            if not os.path.isabs(db_file):
                db_file = os.path.abspath(db_file)

            # Ensure directory exists
            db_dir = os.path.dirname(db_file)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)

            # Test connection
            test_conn = sqlite3.connect(db_file, timeout=10)
            cursor = test_conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            test_conn.close()

            file_size = os.path.getsize(db_file) if os.path.exists(db_file) else 0
            return True, f"SQLite connection successful: {db_file} ({file_size} bytes)"

        except Exception as e:
            return False, f"SQLite test failed: {str(e)}"

    def _test_sqlserver(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Test SQL Server connection"""
        try:
            import pyodbc

            server = config.get("server", "")
            database = config.get("database", "")

            if config.get("use_windows_auth", True):
                conn_str = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={server};"
                    f"DATABASE={database};"
                    f"Trusted_Connection=yes;"
                )
            else:
                username = config.get("username", "")
                password = config.get("password", "")
                conn_str = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={server};"
                    f"DATABASE={database};"
                    f"UID={username};"
                    f"PWD={password};"
                )

            test_conn = pyodbc.connect(conn_str, timeout=10)
            cursor = test_conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            test_conn.close()

            return True, f"SQL Server connection successful: {server}/{database}"

        except ImportError:
            return False, "pyodbc module not installed. Run: pip install pyodbc"
        except Exception as e:
            return False, f"SQL Server test failed: {str(e)}"

    def connect(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Connect to database"""
        try:
            # Store config
            self.db_config = config.copy()
            self.db_type = config.get("type", "sqlite")

            if self.db_type == "sqlite":
                return self._connect_sqlite(config)
            elif self.db_type == "sqlserver":
                return self._connect_sqlserver(config)
            else:
                return False, f"Unsupported database type: {self.db_type}"

        except Exception as e:
            return False, str(e)

    def _connect_sqlite(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Connect to SQLite database"""
        try:
            db_file = config.get("file", "denso888.db")

            # Ensure absolute path
            if not os.path.isabs(db_file):
                db_file = os.path.abspath(db_file)

            # Store file path
            self.db_file_path = db_file

            # Ensure directory exists
            db_dir = os.path.dirname(db_file)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)

            # Connect
            self.connection = sqlite3.connect(db_file, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row

            # Test connection
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()

            # Create metadata table
            self._create_metadata_table()

            file_size = os.path.getsize(db_file) if os.path.exists(db_file) else 0
            return True, f"Connected to SQLite: {db_file} ({file_size:,} bytes)"

        except Exception as e:
            return False, f"SQLite connection failed: {str(e)}"

    def _connect_sqlserver(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Connect to SQL Server"""
        try:
            import pyodbc

            server = config.get("server", "")
            database = config.get("database", "")

            if config.get("use_windows_auth", True):
                conn_str = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={server};"
                    f"DATABASE={database};"
                    f"Trusted_Connection=yes;"
                )
            else:
                username = config.get("username", "")
                password = config.get("password", "")
                conn_str = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={server};"
                    f"DATABASE={database};"
                    f"UID={username};"
                    f"PWD={password};"
                )

            self.connection = pyodbc.connect(conn_str)
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()

            return True, f"Connected to SQL Server: {server}/{database}"

        except ImportError:
            return False, "pyodbc module not installed. Run: pip install pyodbc"
        except Exception as e:
            return False, f"SQL Server connection failed: {str(e)}"

    def _create_metadata_table(self):
        """Create metadata table for operation tracking"""
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
            print(f"Warning: Could not create metadata table: {e}")

    def get_tables(self) -> List[str]:
        """Get list of database tables"""
        try:
            if not self.connection:
                return []

            cursor = self.connection.cursor()

            if self.db_type == "sqlite":
                cursor.execute(
                    """
                    SELECT name FROM sqlite_master 
                    WHERE type='table' 
                    AND name NOT LIKE 'sqlite_%' 
                    AND name != 'denso888_metadata'
                    ORDER BY name
                """
                )
            else:  # SQL Server
                cursor.execute(
                    """
                    SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_TYPE='BASE TABLE' 
                    AND TABLE_NAME != 'denso888_metadata'
                    ORDER BY TABLE_NAME
                """
                )

            tables = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return tables

        except Exception as e:
            print(f"Error getting tables: {e}")
            return []

    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get detailed table information"""
        try:
            if not self.connection:
                return {"error": "Not connected to database"}

            cursor = self.connection.cursor()

            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM [{table_name}]")
            row_count = cursor.fetchone()[0]

            # Get column info
            if self.db_type == "sqlite":
                cursor.execute(f"PRAGMA table_info([{table_name}])")
                columns = [
                    {"name": row[1], "type": row[2], "nullable": not row[3]}
                    for row in cursor.fetchall()
                ]
            else:  # SQL Server
                cursor.execute(
                    """
                    SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = ?
                    ORDER BY ORDINAL_POSITION
                """,
                    (table_name,),
                )
                columns = [
                    {"name": row[0], "type": row[1], "nullable": row[2] == "YES"}
                    for row in cursor.fetchall()
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
            return {"error": str(e)}

    def create_table_from_data(
        self, table_name: str, data: List[Dict]
    ) -> Tuple[bool, str]:
        """Create table from data structure"""
        try:
            if not data:
                return False, "No data provided"

            if not self.connection:
                return False, "Not connected to database"

            # Analyze data structure
            sample_row = data[0]
            columns = list(sample_row.keys())

            # Clean column names
            clean_columns = [self._clean_column_name(col) for col in columns]

            # Create table SQL
            if self.db_type == "sqlite":
                create_sql = self._create_sqlite_table_sql(
                    table_name, sample_row, clean_columns
                )
            else:
                create_sql = self._create_sqlserver_table_sql(
                    table_name, sample_row, clean_columns
                )

            cursor = self.connection.cursor()

            # Drop existing table
            if self.db_type == "sqlite":
                cursor.execute(f"DROP TABLE IF EXISTS [{table_name}]")
            else:
                cursor.execute(
                    f"IF OBJECT_ID('{table_name}', 'U') IS NOT NULL DROP TABLE [{table_name}]"
                )

            # Create table
            cursor.execute(create_sql)
            self.connection.commit()
            cursor.close()

            # Log operation
            self._log_operation(
                "table_create", table_name, len(data), f"Columns: {len(clean_columns)}"
            )

            return (
                True,
                f"Table '{table_name}' created with {len(clean_columns)} columns",
            )

        except Exception as e:
            return False, str(e)

    def _clean_column_name(self, name: str) -> str:
        """Clean column name for database compatibility"""
        import re

        # Convert to string and strip
        clean = str(name).strip()

        # Replace special characters with underscore
        clean = re.sub(r"[^\w\s]", "_", clean)
        clean = re.sub(r"\s+", "_", clean)
        clean = re.sub(r"_+", "_", clean)
        clean = clean.strip("_").lower()

        # Ensure not empty
        if not clean:
            clean = "column"

        # Handle reserved keywords
        reserved = {"index", "order", "group", "select", "from", "where", "table"}
        if clean in reserved:
            clean = f"{clean}_col"

        return clean

    def _create_sqlite_table_sql(
        self, table_name: str, sample_row: Dict, columns: List[str]
    ) -> str:
        """Generate SQLite CREATE TABLE SQL"""
        column_defs = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]

        for i, (orig_col, new_col) in enumerate(zip(sample_row.keys(), columns)):
            value = sample_row[orig_col]

            # Type detection
            if value is None:
                col_type = "TEXT"
            elif isinstance(value, bool):
                col_type = "BOOLEAN"
            elif isinstance(value, int):
                col_type = "INTEGER"
            elif isinstance(value, float):
                col_type = "REAL"
            elif isinstance(value, str):
                col_type = "TEXT"
            else:
                col_type = "TEXT"

            column_defs.append(f"[{new_col}] {col_type}")

        return f"CREATE TABLE [{table_name}] ({', '.join(column_defs)})"

    def _create_sqlserver_table_sql(
        self, table_name: str, sample_row: Dict, columns: List[str]
    ) -> str:
        """Generate SQL Server CREATE TABLE SQL"""
        column_defs = ["id INT IDENTITY(1,1) PRIMARY KEY"]

        for i, (orig_col, new_col) in enumerate(zip(sample_row.keys(), columns)):
            value = sample_row[orig_col]

            # Type detection for SQL Server
            if value is None:
                col_type = "NVARCHAR(255)"
            elif isinstance(value, bool):
                col_type = "BIT"
            elif isinstance(value, int):
                col_type = "INT"
            elif isinstance(value, float):
                col_type = "FLOAT"
            elif isinstance(value, str):
                col_type = "NVARCHAR(255)"
            else:
                col_type = "NVARCHAR(255)"

            column_defs.append(f"[{new_col}] {col_type}")

        return f"CREATE TABLE [{table_name}] ({', '.join(column_defs)})"

    def insert_data(self, table_name: str, data: List[Dict]) -> Tuple[bool, str]:
        """Insert data into table"""
        try:
            if not data:
                return False, "No data to insert"

            if not self.connection:
                return False, "Not connected to database"

            # Get columns from first row
            sample_row = data[0]
            orig_columns = list(sample_row.keys())
            clean_columns = [self._clean_column_name(col) for col in orig_columns]

            # Prepare insert SQL
            placeholders = ", ".join(["?" for _ in clean_columns])
            columns_str = ", ".join([f"[{col}]" for col in clean_columns])
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
                        # Handle None values and data type conversion
                        if value is None:
                            values.append(None)
                        elif isinstance(value, (int, float, str, bool)):
                            values.append(value)
                        else:
                            values.append(str(value))
                    batch_values.append(values)

                cursor.executemany(insert_sql, batch_values)
                total_inserted += len(batch)

            self.connection.commit()
            cursor.close()

            # Log operation
            self._log_operation("data_insert", table_name, total_inserted)

            return True, f"Inserted {total_inserted:,} rows into '{table_name}'"

        except Exception as e:
            return False, str(e)

    def get_table_data(self, table_name: str, limit: int = None) -> List[Dict]:
        """Get data from table"""
        try:
            if not self.connection:
                return []

            cursor = self.connection.cursor()

            if limit:
                if self.db_type == "sqlite":
                    sql = f"SELECT * FROM [{table_name}] LIMIT {limit}"
                else:
                    sql = f"SELECT TOP {limit} * FROM [{table_name}]"
            else:
                sql = f"SELECT * FROM [{table_name}]"

            cursor.execute(sql)

            # Get column names
            columns = [description[0] for description in cursor.description]

            # Fetch data
            rows = cursor.fetchall()
            cursor.close()

            # Convert to list of dictionaries
            data = []
            for row in rows:
                row_dict = {}
                for i, value in enumerate(row):
                    row_dict[columns[i]] = value
                data.append(row_dict)

            return data

        except Exception as e:
            print(f"Error getting table data: {e}")
            return []

    def execute_query(self, query: str) -> Tuple[bool, Any]:
        """Execute custom SQL query"""
        try:
            if not self.connection:
                return False, "Not connected to database"

            cursor = self.connection.cursor()
            cursor.execute(query)

            if query.strip().upper().startswith("SELECT"):
                columns = [description[0] for description in cursor.description]
                rows = cursor.fetchall()
                result = {"columns": columns, "rows": [list(row) for row in rows]}
                cursor.close()
                return True, result
            else:
                self.connection.commit()
                affected_rows = cursor.rowcount
                cursor.close()
                return True, f"Query executed, {affected_rows} rows affected"

        except Exception as e:
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
            print(f"Warning: Could not log operation: {e}")

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
            print(f"Error getting recent operations: {e}")
            return []

    def backup_database(self, backup_path: str) -> Tuple[bool, str]:
        """Create database backup (SQLite only)"""
        try:
            if self.db_type != "sqlite":
                return False, "Backup only supported for SQLite databases"

            if not self.db_file_path or not os.path.exists(self.db_file_path):
                return False, "Source database file not found"

            import shutil

            # Ensure backup directory exists
            backup_dir = os.path.dirname(backup_path)
            if backup_dir:
                os.makedirs(backup_dir, exist_ok=True)

            # Copy database file
            shutil.copy2(self.db_file_path, backup_path)

            backup_size = os.path.getsize(backup_path)
            return True, f"Database backed up to {backup_path} ({backup_size:,} bytes)"

        except Exception as e:
            return False, f"Backup failed: {str(e)}"

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
                "tables_info": [],
            }

            if not self.connection:
                return stats

            # Get tables
            tables = self.get_tables()
            stats["total_tables"] = len(tables)

            # Get table info and total records
            total_records = 0
            for table in tables:
                try:
                    info = self.get_table_info(table)
                    row_count = info.get("row_count", 0)
                    total_records += row_count

                    stats["tables_info"].append(
                        {
                            "name": table,
                            "rows": row_count,
                            "columns": info.get("column_count", 0),
                        }
                    )
                except:
                    pass

            stats["total_records"] = total_records

            # Get database size (SQLite only)
            if (
                self.db_type == "sqlite"
                and self.db_file_path
                and os.path.exists(self.db_file_path)
            ):
                stats["database_size"] = os.path.getsize(self.db_file_path)

            return stats

        except Exception as e:
            return {"error": str(e)}

    def close(self):
        """Close database connection"""
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
                self.db_file_path = None
                self.db_config = {}
            except Exception as e:
                print(f"Error closing connection: {e}")
