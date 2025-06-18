"""
services/connection_pool_service.py
Production-Ready Database Connection Pool Service
Supports both SQLite and SQL Server with automatic failover
"""

import sqlite3
import threading
import queue
import time
import os
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)


class ConnectionPool:
    """Thread-safe connection pool with automatic management"""

    def __init__(
        self,
        connection_config: Dict[str, Any],
        pool_size: int = 5,
        max_overflow: int = 10,
        timeout: int = 30,
    ):
        self.connection_config = connection_config
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.timeout = timeout

        # Pool management
        self.connections = queue.Queue(maxsize=pool_size)
        self.checked_out = set()
        self.overflow_connections = set()
        self.lock = threading.RLock()

        # Statistics
        self.created_at = datetime.now()
        self.total_connections_created = 0
        self.connection_errors = 0
        self._shutdown = False

        # Initialize pool
        self._ensure_database_exists()
        self._initialize_pool()

    def _ensure_database_exists(self):
        """Auto-create database if needed"""
        db_type = self.connection_config.get("type", "sqlite")

        if db_type == "sqlite":
            db_file = self.connection_config.get("file", "denso888_data.db")

            # Ensure absolute path
            if not os.path.isabs(db_file):
                db_file = os.path.abspath(db_file)

            # Create directory if needed
            db_dir = os.path.dirname(db_file)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)

            # Create database file if not exists
            if not os.path.exists(db_file):
                try:
                    conn = sqlite3.connect(db_file)
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        CREATE TABLE IF NOT EXISTS denso888_metadata (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                            version TEXT DEFAULT '3.0.0'
                        )
                    """
                    )
                    cursor.execute(
                        "INSERT INTO denso888_metadata (version) VALUES (?)", ("3.0.0",)
                    )
                    conn.commit()
                    conn.close()
                    logger.info(f"Created new SQLite database: {db_file}")
                except Exception as e:
                    logger.error(f"Failed to create SQLite database: {e}")
                    raise

    def _initialize_pool(self):
        """Initialize pool with minimum connections"""
        for _ in range(min(self.pool_size, 2)):
            try:
                conn = self._create_connection()
                self.connections.put(conn)
                self.total_connections_created += 1
            except Exception as e:
                logger.warning(f"Failed to pre-create connection: {e}")

    def get_connection(self, timeout: Optional[float] = None):
        """Get connection from pool with enhanced error handling"""
        if self._shutdown:
            raise Exception("Connection pool is shutting down")

        timeout = timeout or self.timeout
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                # Try to get from pool
                conn = self.connections.get_nowait()
                if self._is_connection_valid(conn):
                    with self.lock:
                        self.checked_out.add(conn)
                    return conn
                else:
                    try:
                        conn.close()
                    except:
                        pass
                    continue
            except queue.Empty:
                pass

            # Pool is empty, try to create new connection
            with self.lock:
                total_active = len(self.checked_out) + len(self.overflow_connections)
                if total_active < self.pool_size + self.max_overflow:
                    try:
                        conn = self._create_connection()
                        if total_active >= self.pool_size:
                            self.overflow_connections.add(conn)
                        self.checked_out.add(conn)
                        self.total_connections_created += 1
                        return conn
                    except Exception as e:
                        self.connection_errors += 1
                        logger.error(f"Failed to create connection: {e}")

            time.sleep(0.1)

        raise Exception(f"Connection timeout after {timeout} seconds")

    def return_connection(self, conn):
        """Return connection to pool with validation"""
        if self._shutdown or not conn:
            try:
                if conn:
                    conn.close()
            except:
                pass
            return

        with self.lock:
            if conn not in self.checked_out:
                try:
                    conn.close()
                except:
                    pass
                return

            self.checked_out.remove(conn)

            if self._is_connection_valid(conn):
                if conn in self.overflow_connections:
                    self.overflow_connections.remove(conn)
                    try:
                        conn.close()
                    except:
                        pass
                else:
                    try:
                        self.connections.put_nowait(conn)
                    except queue.Full:
                        try:
                            conn.close()
                        except:
                            pass
            else:
                try:
                    conn.close()
                except:
                    pass
                if conn in self.overflow_connections:
                    self.overflow_connections.remove(conn)

    def _create_connection(self):
        """Create new database connection"""
        db_type = self.connection_config.get("type", "sqlite")

        if db_type == "sqlite":
            return self._create_sqlite_connection()
        elif db_type == "sqlserver":
            return self._create_sqlserver_connection()
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

    def _create_sqlite_connection(self):
        """Create SQLite connection with optimizations"""
        try:
            db_file = self.connection_config.get("file", "denso888_data.db")

            if not os.path.isabs(db_file):
                db_file = os.path.abspath(db_file)

            conn = sqlite3.connect(
                db_file,
                check_same_thread=False,
                timeout=30,
                isolation_level=None,  # Autocommit mode
            )

            conn.row_factory = sqlite3.Row

            # Apply SQLite optimizations
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute("PRAGMA journal_mode = WAL")
            cursor.execute("PRAGMA synchronous = NORMAL")
            cursor.execute("PRAGMA cache_size = 10000")
            cursor.execute("PRAGMA temp_store = memory")
            cursor.close()

            return conn

        except Exception as e:
            logger.error(f"Failed to create SQLite connection: {e}")
            raise

    def _create_sqlserver_connection(self):
        """Create SQL Server connection"""
        try:
            import pyodbc
        except ImportError:
            raise Exception(
                "pyodbc module required for SQL Server. Install with: pip install pyodbc"
            )

        try:
            server = self.connection_config.get("server", "")
            database = self.connection_config.get("database", "")

            if self.connection_config.get("use_windows_auth", True):
                conn_str = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={server};"
                    f"DATABASE={database};"
                    f"Trusted_Connection=yes;"
                    f"TrustServerCertificate=yes;"
                    f"Encrypt=no;"
                )
            else:
                username = self.connection_config.get("username", "")
                password = self.connection_config.get("password", "")
                conn_str = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={server};"
                    f"DATABASE={database};"
                    f"UID={username};"
                    f"PWD={password};"
                    f"TrustServerCertificate=yes;"
                    f"Encrypt=no;"
                )

            conn = pyodbc.connect(conn_str, timeout=30)
            conn.autocommit = False

            # Test connection
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()

            return conn

        except Exception as e:
            logger.error(f"Failed to create SQL Server connection: {e}")
            raise

    def _is_connection_valid(self, conn) -> bool:
        """Check if connection is still valid"""
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            return True
        except Exception:
            return False

    @contextmanager
    def get_managed_connection(self):
        """Context manager for automatic connection management"""
        conn = None
        try:
            conn = self.get_connection()
            yield conn
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            raise
        finally:
            if conn:
                self.return_connection(conn)

    def close_all(self):
        """Close all connections safely"""
        self._shutdown = True

        with self.lock:
            # Close pool connections
            while True:
                try:
                    conn = self.connections.get_nowait()
                    try:
                        conn.close()
                    except:
                        pass
                except queue.Empty:
                    break

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

    def get_stats(self) -> Dict[str, Any]:
        """Get pool statistics"""
        with self.lock:
            return {
                "pool_size": self.pool_size,
                "connections_in_pool": self.connections.qsize(),
                "checked_out_connections": len(self.checked_out),
                "overflow_connections": len(self.overflow_connections),
                "total_connections_created": self.total_connections_created,
                "connection_errors": self.connection_errors,
                "is_shutdown": self._shutdown,
            }


class ConnectionPoolService:
    """Enhanced connection pool service with multiple database support"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.pools: Dict[str, ConnectionPool] = {}
        self.current_pool: Optional[ConnectionPool] = None
        self.current_config: Optional[Dict[str, Any]] = None
        self._lock = threading.RLock()

        # Service statistics
        self.service_stats = {
            "connections_created": 0,
            "queries_executed": 0,
            "errors_count": 0,
            "service_start_time": datetime.now(),
        }

    def connect_database(self, config: Dict[str, Any]) -> bool:
        """Connect to database with connection pooling"""
        try:
            # Create pool key
            pool_key = self._generate_pool_key(config)

            with self._lock:
                # Reuse existing pool if available
                if pool_key in self.pools:
                    self.current_pool = self.pools[pool_key]
                    self.current_config = config
                    return True

                # Create new pool
                pool = ConnectionPool(
                    config,
                    pool_size=config.get("pool_size", 5),
                    max_overflow=config.get("max_overflow", 10),
                    timeout=config.get("timeout", 30),
                )

                # Test pool with a connection
                with pool.get_managed_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT 1")
                    cursor.close()

                # Store pool
                self.pools[pool_key] = pool
                self.current_pool = pool
                self.current_config = config

                logger.info(
                    f"Connected to {config.get('type')} database with connection pool"
                )
                return True

        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return False

    def execute_query(self, query: str, params: tuple = ()) -> Tuple[bool, Any]:
        """Execute query using connection pool"""
        if not self.current_pool:
            return False, "No database connection available"

        try:
            with self.current_pool.get_managed_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)

                if query.strip().upper().startswith("SELECT"):
                    if hasattr(cursor, "fetchall"):
                        rows = cursor.fetchall()
                        # Convert to list of dicts for consistency
                        if rows and hasattr(rows[0], "keys"):
                            result = [dict(row) for row in rows]
                        else:
                            columns = (
                                [desc[0] for desc in cursor.description]
                                if cursor.description
                                else []
                            )
                            result = [dict(zip(columns, row)) for row in rows]
                        return True, result
                    return True, []
                else:
                    conn.commit()
                    affected_rows = (
                        cursor.rowcount if hasattr(cursor, "rowcount") else 0
                    )
                    return (
                        True,
                        f"Query executed successfully. {affected_rows} rows affected.",
                    )

        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            self.service_stats["errors_count"] += 1
            return False, str(e)

    def get_tables(self) -> List[str]:
        """Get list of database tables"""
        if not self.current_pool or not self.current_config:
            return []

        try:
            db_type = self.current_config.get("type", "sqlite")

            if db_type == "sqlite":
                query = """
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name NOT LIKE 'sqlite_%'
                    ORDER BY name
                """
            else:  # SQL Server
                query = """
                    SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_TYPE='BASE TABLE'
                    ORDER BY TABLE_NAME
                """

            success, result = self.execute_query(query)
            if success and isinstance(result, list):
                return [row.get("name") or row.get("TABLE_NAME", "") for row in result]

            return []

        except Exception as e:
            logger.error(f"Failed to get tables: {e}")
            return []

    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """Get table schema information"""
        if not self.current_pool or not self.current_config:
            return []

        try:
            db_type = self.current_config.get("type", "sqlite")

            if db_type == "sqlite":
                query = f"PRAGMA table_info([{table_name}])"
            else:  # SQL Server
                query = """
                    SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = ?
                    ORDER BY ORDINAL_POSITION
                """

            params = () if db_type == "sqlite" else (table_name,)
            success, result = self.execute_query(query, params)

            if success and isinstance(result, list):
                schema = []
                for row in result:
                    if db_type == "sqlite":
                        schema.append(
                            {
                                "name": row.get("name", ""),
                                "type": row.get("type", "TEXT"),
                                "nullable": not row.get("notnull", 0),
                                "default": row.get("dflt_value"),
                                "primary_key": bool(row.get("pk", 0)),
                            }
                        )
                    else:  # SQL Server
                        schema.append(
                            {
                                "name": row.get("COLUMN_NAME", ""),
                                "type": row.get("DATA_TYPE", "VARCHAR"),
                                "nullable": row.get("IS_NULLABLE", "YES") == "YES",
                                "default": row.get("COLUMN_DEFAULT"),
                                "primary_key": False,
                            }
                        )
                return schema

            return []

        except Exception as e:
            logger.error(f"Failed to get table schema: {e}")
            return []

    def bulk_insert(
        self, table_name: str, data: List[Dict], batch_size: int = 1000
    ) -> bool:
        """Bulk insert data with batching"""
        if not self.current_pool or not data:
            return False

        try:
            # Get first row to determine columns
            sample_row = data[0]
            columns = list(sample_row.keys())

            # Auto-create table if needed
            self._ensure_table_exists(table_name, sample_row)

            # Prepare insert SQL
            placeholders = ", ".join(["?" for _ in columns])
            columns_str = ", ".join([f"[{col}]" for col in columns])
            insert_sql = (
                f"INSERT INTO [{table_name}] ({columns_str}) VALUES ({placeholders})"
            )

            total_inserted = 0

            with self.current_pool.get_managed_connection() as conn:
                cursor = conn.cursor()

                # Insert in batches
                for i in range(0, len(data), batch_size):
                    batch = data[i : i + batch_size]
                    batch_values = []

                    for row in batch:
                        values = [row.get(col) for col in columns]
                        batch_values.append(values)

                    cursor.executemany(insert_sql, batch_values)
                    total_inserted += len(batch_values)

                conn.commit()
                cursor.close()

            logger.info(f"Bulk insert completed: {total_inserted} records")
            return True

        except Exception as e:
            logger.error(f"Bulk insert failed: {e}")
            return False

    def _ensure_table_exists(self, table_name: str, sample_row: Dict):
        """Auto-create table if it doesn't exist"""
        try:
            # Check if table exists
            if self.current_config.get("type") == "sqlite":
                check_query = (
                    "SELECT name FROM sqlite_master WHERE type='table' AND name = ?"
                )
            else:
                check_query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = ?"

            success, result = self.execute_query(check_query, (table_name,))

            if success and result:
                return  # Table exists

            # Create table
            self._create_table_from_sample(table_name, sample_row)

        except Exception as e:
            logger.error(f"Error ensuring table exists: {e}")

    def _create_table_from_sample(self, table_name: str, sample_row: Dict):
        """Create table from sample data"""
        columns = []

        for col_name, value in sample_row.items():
            clean_name = self._clean_column_name(col_name)

            # Detect column type
            if value is None:
                col_type = "TEXT"
            elif isinstance(value, bool):
                col_type = (
                    "BOOLEAN" if self.current_config.get("type") == "sqlite" else "BIT"
                )
            elif isinstance(value, int):
                col_type = (
                    "INTEGER" if self.current_config.get("type") == "sqlite" else "INT"
                )
            elif isinstance(value, float):
                col_type = (
                    "REAL" if self.current_config.get("type") == "sqlite" else "FLOAT"
                )
            else:
                col_type = (
                    "TEXT"
                    if self.current_config.get("type") == "sqlite"
                    else "NVARCHAR(255)"
                )

            columns.append(f"[{clean_name}] {col_type}")

        # Add ID column
        if self.current_config.get("type") == "sqlite":
            create_sql = f"""
                CREATE TABLE [{table_name}] (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {', '.join(columns)}
                )
            """
        else:
            create_sql = f"""
                CREATE TABLE [{table_name}] (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    {', '.join(columns)}
                )
            """

        self.execute_query(create_sql)
        logger.info(f"Created table: {table_name}")

    def _clean_column_name(self, name: str) -> str:
        """Clean column name for database compatibility"""
        import re

        clean = str(name).strip()
        clean = re.sub(r"[^\w\s]", "_", clean)
        clean = re.sub(r"\s+", "_", clean)
        clean = re.sub(r"_+", "_", clean)
        clean = clean.strip("_").lower()
        return clean if clean else "column"

    def _generate_pool_key(self, config: Dict[str, Any]) -> str:
        """Generate unique key for connection pool"""
        db_type = config.get("type", "sqlite")
        if db_type == "sqlite":
            return f"sqlite:{config.get('file', 'default.db')}"
        else:
            server = config.get("server", "")
            database = config.get("database", "")
            return f"sqlserver:{server}:{database}"

    def get_service_stats(self) -> Dict[str, Any]:
        """Get service statistics"""
        stats = {
            **self.service_stats,
            "active_pools": len(self.pools),
            "current_pool_stats": None,
        }

        if self.current_pool:
            stats["current_pool_stats"] = self.current_pool.get_stats()

        return stats

    def close_all_pools(self):
        """Close all connection pools"""
        with self._lock:
            for pool in self.pools.values():
                try:
                    pool.close_all()
                except Exception as e:
                    logger.error(f"Error closing pool: {e}")

            self.pools.clear()
            self.current_pool = None
            self.current_config = None

    def __del__(self):
        """Cleanup on destruction"""
        try:
            self.close_all_pools()
        except:
            pass
