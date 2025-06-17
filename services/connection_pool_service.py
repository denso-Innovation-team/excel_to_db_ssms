"""
services/connection_pool_service.py
Enhanced Connection Pool Service for Multiple Database Types
Production Ready with Full Error Handling
"""

import sqlite3
import threading
from typing import Dict, List, Any
from contextlib import contextmanager
import time
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class ConnectionPool:
    """Enhanced connection pool with automatic cleanup and monitoring"""

    def __init__(
        self,
        connection_string: str,
        pool_size: int = 5,
        max_overflow: int = 10,
        timeout: int = 30,
    ):
        self.connection_string = connection_string
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.timeout = timeout
        self.connections = []
        self.checked_out = set()
        self.overflow_connections = set()
        self.lock = threading.Lock()
        self.created_at = datetime.now()
        self.total_connections_created = 0
        self.connection_errors = 0

    def get_connection(self):
        """Get connection from pool with timeout handling"""
        start_time = time.time()

        while time.time() - start_time < self.timeout:
            with self.lock:
                # Try to get from pool
                if self.connections:
                    conn = self.connections.pop()
                    self.checked_out.add(conn)
                    logger.debug(
                        f"Retrieved connection from pool. Pool size: {len(self.connections)}"
                    )
                    return conn

                # Create overflow connection if allowed
                total_active = len(self.checked_out) + len(self.overflow_connections)
                if total_active < self.pool_size + self.max_overflow:
                    try:
                        conn = self._create_connection()
                        if total_active >= self.pool_size:
                            self.overflow_connections.add(conn)
                        self.checked_out.add(conn)
                        self.total_connections_created += 1
                        logger.debug(
                            f"Created new connection. Total active: {total_active + 1}"
                        )
                        return conn
                    except Exception as e:
                        self.connection_errors += 1
                        logger.error(f"Failed to create connection: {e}")
                        raise

            # Wait and retry
            time.sleep(0.1)

        raise Exception(f"Connection timeout after {self.timeout} seconds")

    def return_connection(self, conn):
        """Return connection to pool with validation"""
        with self.lock:
            if conn in self.checked_out:
                self.checked_out.remove(conn)

                # Test connection before returning to pool
                if self._is_connection_valid(conn):
                    if conn in self.overflow_connections:
                        self.overflow_connections.remove(conn)
                        conn.close()
                        logger.debug("Closed overflow connection")
                    else:
                        if len(self.connections) < self.pool_size:
                            self.connections.append(conn)
                            logger.debug(
                                f"Returned connection to pool. Pool size: {len(self.connections)}"
                            )
                        else:
                            conn.close()
                            logger.debug("Pool full, closed connection")
                else:
                    # Connection is invalid, close it
                    logger.warning("Invalid connection detected, closing")
                    try:
                        conn.close()
                    except:
                        pass
                    if conn in self.overflow_connections:
                        self.overflow_connections.remove(conn)

    def _create_connection(self):
        """Create new database connection"""
        if "sqlite" in self.connection_string.lower():
            # Handle SQLite connections
            db_path = self.connection_string.replace("sqlite:///", "")

            # Ensure directory exists
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)

            conn = sqlite3.connect(db_path, check_same_thread=False, timeout=30)
            conn.row_factory = sqlite3.Row  # Enable column access by name

            # Enable foreign keys and other optimizations
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("PRAGMA synchronous = NORMAL")
            conn.execute("PRAGMA cache_size = 10000")

            return conn
        else:
            # Handle SQL Server connections
            try:
                import pyodbc

                conn = pyodbc.connect(self.connection_string, timeout=30)
                conn.autocommit = False
                return conn
            except ImportError:
                raise Exception(
                    "pyodbc module required for SQL Server connections. Install with: pip install pyodbc"
                )

    def _is_connection_valid(self, conn) -> bool:
        """Check if connection is still valid"""
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return True
        except Exception:
            return False

    @contextmanager
    def get_managed_connection(self):
        """Context manager for automatic connection management"""
        conn = self.get_connection()
        try:
            yield conn
        except Exception:
            # Rollback on error
            try:
                conn.rollback()
            except:
                pass
            raise
        finally:
            self.return_connection(conn)

    def close_all(self):
        """Close all connections in pool"""
        with self.lock:
            # Close pool connections
            for conn in self.connections:
                try:
                    conn.close()
                except:
                    pass
            self.connections.clear()

            # Close checked out connections
            for conn in list(self.checked_out):
                try:
                    conn.close()
                except:
                    pass
            self.checked_out.clear()

            # Close overflow connections
            for conn in list(self.overflow_connections):
                try:
                    conn.close()
                except:
                    pass
            self.overflow_connections.clear()

        logger.info(f"Closed all connections in pool")

    def get_stats(self) -> Dict[str, Any]:
        """Get pool statistics"""
        with self.lock:
            return {
                "pool_size": self.pool_size,
                "max_overflow": self.max_overflow,
                "connections_in_pool": len(self.connections),
                "checked_out_connections": len(self.checked_out),
                "overflow_connections": len(self.overflow_connections),
                "total_connections_created": self.total_connections_created,
                "connection_errors": self.connection_errors,
                "uptime_seconds": (datetime.now() - self.created_at).total_seconds(),
            }


class ConnectionPoolService:
    """Enhanced connection pool service with monitoring and management"""

    def __init__(self):
        self.pools: Dict[str, ConnectionPool] = {}
        self.current_pool = None
        self.current_config = None
        self.service_stats = {
            "total_queries": 0,
            "failed_queries": 0,
            "start_time": datetime.now(),
        }

    def connect_database(self, config: Dict[str, Any]) -> bool:
        """Connect to database and create connection pool"""
        try:
            logger.info(f"Connecting to database: {config.get('type', 'unknown')}")

            connection_string = self._build_connection_string(config)
            pool_key = self._get_pool_key(config)

            # Create or get existing pool
            if pool_key not in self.pools:
                self.pools[pool_key] = ConnectionPool(
                    connection_string,
                    pool_size=config.get("pool_size", 5),
                    max_overflow=config.get("max_overflow", 10),
                    timeout=config.get("timeout", 30),
                )
                logger.info(f"Created new connection pool: {pool_key}")

            self.current_pool = self.pools[pool_key]
            self.current_config = config

            # Test connection
            with self.current_pool.get_managed_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                cursor.close()

            logger.info(f"Successfully connected to database: {pool_key}")
            return True

        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False

    def _build_connection_string(self, config: Dict[str, Any]) -> str:
        """Build connection string based on database type"""
        db_type = config.get("type", "sqlite")

        if db_type == "sqlite":
            db_file = config.get("file", "database.db")
            return f"sqlite:///{db_file}"

        elif db_type == "sqlserver":
            server = config["server"]
            database = config["database"]

            if config.get("use_windows_auth", True):
                return (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={server};"
                    f"DATABASE={database};"
                    f"Trusted_Connection=yes;"
                    f"TrustServerCertificate=yes;"
                )
            else:
                username = config["username"]
                password = config["password"]
                return (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={server};"
                    f"DATABASE={database};"
                    f"UID={username};"
                    f"PWD={password};"
                    f"TrustServerCertificate=yes;"
                )

        raise ValueError(f"Unsupported database type: {db_type}")

    def _get_pool_key(self, config: Dict[str, Any]) -> str:
        """Generate unique key for connection pool"""
        db_type = config.get("type", "sqlite")

        if db_type == "sqlite":
            return f"sqlite_{config.get('file', 'database.db')}"
        elif db_type == "sqlserver":
            return f"sqlserver_{config['server']}_{config['database']}"

        return f"{db_type}_default"

    def get_tables(self) -> List[str]:
        """Get list of tables in current database"""
        if not self.current_pool:
            return []

        try:
            with self.current_pool.get_managed_connection() as conn:
                cursor = conn.cursor()

                if self.current_config.get("type") == "sqlite":
                    cursor.execute(
                        """
                        SELECT name FROM sqlite_master 
                        WHERE type='table' AND name NOT LIKE 'sqlite_%'
                        ORDER BY name
                        """
                    )
                else:  # SQL Server
                    cursor.execute(
                        """
                        SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES 
                        WHERE TABLE_TYPE='BASE TABLE'
                        ORDER BY TABLE_NAME
                        """
                    )

                tables = [row[0] for row in cursor.fetchall()]
                cursor.close()

                self.service_stats["total_queries"] += 1
                logger.debug(f"Retrieved {len(tables)} tables")
                return tables

        except Exception as e:
            logger.error(f"Error getting tables: {e}")
            self.service_stats["failed_queries"] += 1
            return []

    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """Get detailed table schema information"""
        if not self.current_pool:
            return []

        try:
            with self.current_pool.get_managed_connection() as conn:
                cursor = conn.cursor()

                if self.current_config.get("type") == "sqlite":
                    cursor.execute(f"PRAGMA table_info([{table_name}])")
                    columns = []
                    for row in cursor.fetchall():
                        columns.append(
                            {
                                "name": row[1],
                                "type": row[2],
                                "nullable": not row[3],
                                "default": row[4],
                                "primary_key": bool(row[5]),
                            }
                        )
                else:  # SQL Server
                    cursor.execute(
                        """
                        SELECT 
                            COLUMN_NAME, 
                            DATA_TYPE, 
                            IS_NULLABLE, 
                            COLUMN_DEFAULT,
                            CASE WHEN COLUMNPROPERTY(OBJECT_ID(TABLE_SCHEMA+'.'+TABLE_NAME), COLUMN_NAME, 'IsIdentity') = 1 
                                 THEN 1 ELSE 0 END as IS_IDENTITY
                        FROM INFORMATION_SCHEMA.COLUMNS 
                        WHERE TABLE_NAME = ?
                        ORDER BY ORDINAL_POSITION
                        """,
                        (table_name,),
                    )

                    columns = []
                    for row in cursor.fetchall():
                        columns.append(
                            {
                                "name": row[0],
                                "type": row[1],
                                "nullable": row[2] == "YES",
                                "default": row[3],
                                "primary_key": bool(row[4]),
                            }
                        )

                cursor.close()
                self.service_stats["total_queries"] += 1
                logger.debug(
                    f"Retrieved schema for table {table_name}: {len(columns)} columns"
                )
                return columns

        except Exception as e:
            logger.error(f"Error getting table schema for {table_name}: {e}")
            self.service_stats["failed_queries"] += 1
            return []

    def bulk_insert(
        self, table_name: str, data: List[Dict], batch_size: int = 1000
    ) -> bool:
        """Enhanced bulk insert with progress tracking and error recovery"""
        if not self.current_pool or not data:
            return False

        try:
            logger.info(f"Starting bulk insert to {table_name}: {len(data)} records")

            # Get columns from first record
            columns = list(data[0].keys())
            placeholders = ", ".join(["?" for _ in columns])
            column_names = ", ".join([f"[{col}]" for col in columns])

            insert_sql = (
                f"INSERT INTO [{table_name}] ({column_names}) VALUES ({placeholders})"
            )

            total_inserted = 0
            failed_batches = 0

            with self.current_pool.get_managed_connection() as conn:
                cursor = conn.cursor()

                # Process in batches
                for i in range(0, len(data), batch_size):
                    batch = data[i : i + batch_size]

                    try:
                        # Prepare batch data
                        batch_values = []
                        for row in batch:
                            values = [row.get(col) for col in columns]
                            batch_values.append(values)

                        # Execute batch insert
                        cursor.executemany(insert_sql, batch_values)
                        total_inserted += len(batch)

                        # Progress logging
                        progress = (i + len(batch)) / len(data) * 100
                        logger.debug(
                            f"Bulk insert progress: {progress:.1f}% ({total_inserted}/{len(data)})"
                        )

                    except Exception as batch_error:
                        logger.warning(
                            f"Batch insert failed at batch {i//batch_size + 1}: {batch_error}"
                        )
                        failed_batches += 1

                        # Try inserting records one by one in failed batch
                        for record in batch:
                            try:
                                values = [record.get(col) for col in columns]
                                cursor.execute(insert_sql, values)
                                total_inserted += 1
                            except Exception as record_error:
                                logger.error(f"Failed to insert record: {record_error}")

                # Commit transaction
                conn.commit()
                cursor.close()

            success_rate = (total_inserted / len(data)) * 100
            logger.info(
                f"Bulk insert completed: {total_inserted}/{len(data)} records ({success_rate:.1f}% success)"
            )

            if failed_batches > 0:
                logger.warning(
                    f"Had {failed_batches} failed batches, but recovered with individual inserts"
                )

            self.service_stats["total_queries"] += 1
            return total_inserted > 0

        except Exception as e:
            logger.error(f"Bulk insert failed completely: {e}")
            self.service_stats["failed_queries"] += 1
            return False

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute query and return results as list of dictionaries"""
        if not self.current_pool:
            return []

        try:
            with self.current_pool.get_managed_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)

                if query.strip().upper().startswith("SELECT"):
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()

                    result = []
                    for row in rows:
                        row_dict = {}
                        for i, value in enumerate(row):
                            row_dict[columns[i]] = value
                        result.append(row_dict)

                    cursor.close()
                    self.service_stats["total_queries"] += 1
                    return result
                else:
                    # For non-SELECT queries
                    conn.commit()
                    affected_rows = cursor.rowcount
                    cursor.close()
                    self.service_stats["total_queries"] += 1
                    return [{"affected_rows": affected_rows}]

        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            self.service_stats["failed_queries"] += 1
            return []

    def get_database_info(self) -> Dict[str, Any]:
        """Get comprehensive database information"""
        if not self.current_pool or not self.current_config:
            return {}

        try:
            info = {
                "type": self.current_config.get("type"),
                "connected": True,
                "tables": [],
                "total_tables": 0,
                "total_records": 0,
                "database_size": 0,
            }

            # Get tables and calculate total records
            tables = self.get_tables()
            info["tables"] = tables
            info["total_tables"] = len(tables)

            total_records = 0
            for table in tables:
                try:
                    with self.current_pool.get_managed_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute(f"SELECT COUNT(*) FROM [{table}]")
                        count = cursor.fetchone()[0]
                        total_records += count
                        cursor.close()
                except Exception as e:
                    logger.warning(f"Could not get record count for table {table}: {e}")

            info["total_records"] = total_records

            # Get database size for SQLite
            if self.current_config.get("type") == "sqlite":
                db_file = self.current_config.get("file")
                if db_file and Path(db_file).exists():
                    info["database_size"] = Path(db_file).stat().st_size

            return info

        except Exception as e:
            logger.error(f"Error getting database info: {e}")
            return {"error": str(e)}

    def get_service_stats(self) -> Dict[str, Any]:
        """Get service statistics"""
        uptime = datetime.now() - self.service_stats["start_time"]

        stats = {
            **self.service_stats,
            "uptime_seconds": uptime.total_seconds(),
            "active_pools": len(self.pools),
            "success_rate": 0,
        }

        # Calculate success rate
        total_queries = stats["total_queries"]
        if total_queries > 0:
            stats["success_rate"] = (
                (total_queries - stats["failed_queries"]) / total_queries
            ) * 100

        # Add current pool stats if available
        if self.current_pool:
            stats["current_pool"] = self.current_pool.get_stats()

        return stats

    def create_table_from_data(self, table_name: str, data: List[Dict]) -> bool:
        """Create table from data sample with enhanced type detection"""
        if not self.current_pool or not data:
            return False

        try:
            logger.info(f"Creating table {table_name} from data sample")

            # Analyze data types
            sample_row = data[0]
            columns = list(sample_row.keys())

            # Enhanced type detection
            column_types = {}
            for col in columns:
                # Analyze values in this column across multiple rows
                values = [
                    row.get(col)
                    for row in data[: min(100, len(data))]
                    if row.get(col) is not None
                ]

                if not values:
                    column_types[col] = "TEXT"
                    continue

                # Check for integers
                if all(
                    isinstance(v, int) or (isinstance(v, str) and v.isdigit())
                    for v in values
                ):
                    column_types[col] = "INTEGER"
                # Check for floats
                elif all(
                    isinstance(v, (int, float)) or self._is_numeric(str(v))
                    for v in values
                ):
                    column_types[col] = "REAL"
                # Check for dates
                elif all(self._looks_like_date(str(v)) for v in values):
                    column_types[col] = (
                        "DATETIME"
                        if self.current_config.get("type") == "sqlserver"
                        else "TEXT"
                    )
                # Check for booleans
                elif all(
                    str(v).lower() in ["true", "false", "1", "0", "yes", "no"]
                    for v in values
                ):
                    column_types[col] = (
                        "BIT"
                        if self.current_config.get("type") == "sqlserver"
                        else "BOOLEAN"
                    )
                else:
                    column_types[col] = "TEXT"

            # Generate CREATE TABLE SQL
            create_sql = self._generate_create_table_sql(
                table_name, columns, column_types
            )

            with self.current_pool.get_managed_connection() as conn:
                cursor = conn.cursor()

                # Drop table if exists
                if self.current_config.get("type") == "sqlite":
                    cursor.execute(f"DROP TABLE IF EXISTS [{table_name}]")
                else:
                    cursor.execute(
                        f"IF OBJECT_ID('{table_name}', 'U') IS NOT NULL DROP TABLE [{table_name}]"
                    )

                # Create table
                cursor.execute(create_sql)
                conn.commit()
                cursor.close()

            logger.info(
                f"Successfully created table {table_name} with {len(columns)} columns"
            )
            self.service_stats["total_queries"] += 1
            return True

        except Exception as e:
            logger.error(f"Failed to create table {table_name}: {e}")
            self.service_stats["failed_queries"] += 1
            return False

    def _generate_create_table_sql(
        self, table_name: str, columns: List[str], column_types: Dict[str, str]
    ) -> str:
        """Generate CREATE TABLE SQL based on database type"""
        if self.current_config.get("type") == "sqlite":
            column_defs = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]
        else:
            column_defs = ["id INT IDENTITY(1,1) PRIMARY KEY"]

        for col in columns:
            # Clean column name
            clean_col = self._clean_column_name(col)
            col_type = column_types.get(col, "TEXT")

            # Adjust types for SQL Server
            if self.current_config.get("type") == "sqlserver":
                if col_type == "TEXT":
                    col_type = "NVARCHAR(255)"
                elif col_type == "BOOLEAN":
                    col_type = "BIT"
                elif col_type == "REAL":
                    col_type = "FLOAT"

            column_defs.append(f"[{clean_col}] {col_type}")

        return f"CREATE TABLE [{table_name}] ({', '.join(column_defs)})"

    def _clean_column_name(self, name: str) -> str:
        """Clean column name for database compatibility"""
        import re

        # Convert to string and clean
        clean = str(name).strip()
        clean = re.sub(r"[^\w\s]", "_", clean)
        clean = re.sub(r"\s+", "_", clean)
        clean = re.sub(r"_+", "_", clean)
        clean = clean.strip("_").lower()

        if not clean:
            clean = "column"

        # Handle reserved keywords
        reserved = {
            "index",
            "order",
            "group",
            "select",
            "from",
            "where",
            "table",
            "user",
            "date",
            "time",
        }
        if clean in reserved:
            clean = f"{clean}_col"

        return clean

    def _is_numeric(self, value: str) -> bool:
        """Check if string represents a number"""
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    def _looks_like_date(self, value: str) -> bool:
        """Check if string looks like a date"""
        import re

        date_patterns = [
            r"\d{4}-\d{2}-\d{2}",  # YYYY-MM-DD
            r"\d{2}/\d{2}/\d{4}",  # MM/DD/YYYY
            r"\d{2}-\d{2}-\d{4}",  # MM-DD-YYYY
            r"\d{4}/\d{2}/\d{2}",  # YYYY/MM/DD
        ]

        for pattern in date_patterns:
            if re.match(pattern, value.strip()):
                return True
        return False

    def backup_database(self, backup_path: str) -> bool:
        """Backup database (SQLite only)"""
        if not self.current_pool or self.current_config.get("type") != "sqlite":
            logger.warning("Backup only supported for SQLite databases")
            return False

        try:
            import shutil

            source_file = self.current_config.get("file")
            if not source_file or not Path(source_file).exists():
                logger.error("Source database file not found")
                return False

            # Ensure backup directory exists
            backup_dir = Path(backup_path).parent
            backup_dir.mkdir(parents=True, exist_ok=True)

            # Create backup
            shutil.copy2(source_file, backup_path)

            backup_size = Path(backup_path).stat().st_size
            logger.info(f"Database backed up to {backup_path} ({backup_size:,} bytes)")
            return True

        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return False

    def close_all_pools(self):
        """Close all connection pools"""
        logger.info("Closing all connection pools")

        for pool_name, pool in self.pools.items():
            try:
                pool.close_all()
                logger.debug(f"Closed pool: {pool_name}")
            except Exception as e:
                logger.error(f"Error closing pool {pool_name}: {e}")

        self.pools.clear()
        self.current_pool = None
        self.current_config = None

        logger.info("All connection pools closed")

    def __del__(self):
        """Cleanup when service is destroyed"""
        self.close_all_pools()
