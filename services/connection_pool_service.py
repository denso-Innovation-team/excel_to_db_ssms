"""
services/connection_pool_service.py
FIXED: SQL Server + SQLite Connection Pool with Auto-Creation
"""

import sqlite3
import threading
from typing import Dict, Any, Optional, Tuple
import logging
from sqlalchemy import create_engine, exc, event
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
import os
import queue
import time
from datetime import datetime

logger = logging.getLogger(__name__)


class ConnectionPool:
    """Production-ready connection pool with auto-creation support"""

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
        self.connections = queue.Queue(maxsize=pool_size)
        self.checked_out = set()
        self.overflow_connections = set()
        self.lock = threading.RLock()
        self.created_at = datetime.now()
        self.total_connections_created = 0
        self.connection_errors = 0
        self._shutdown = False

        # Auto-create database if needed
        self._ensure_database_exists()

        # Pre-populate pool
        self._initialize_pool()

    def _ensure_database_exists(self):
        """Auto-create database if it doesn't exist"""
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
                    # Create a basic metadata table
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
                # Try to get from pool (non-blocking)
                conn = self.connections.get_nowait()
                if self._is_connection_valid(conn):
                    with self.lock:
                        self.checked_out.add(conn)
                    return conn
                else:
                    # Connection is invalid, discard it
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

            # Wait and retry
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
        """Create new database connection with proper error handling"""
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

            # Ensure absolute path
            if not os.path.isabs(db_file):
                db_file = os.path.abspath(db_file)

            # Create connection
            conn = sqlite3.connect(
                db_file,
                check_same_thread=False,
                timeout=30,
                isolation_level=None,  # Autocommit mode
            )

            # Enable row factory for dict-like access
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
        """Create SQL Server connection with proper driver handling"""
        try:
            import pyodbc
        except ImportError:
            raise Exception(
                "pyodbc module required for SQL Server. Install with: pip install pyodbc"
            )

        try:
            server = self.connection_config.get("server", "")
            database = self.connection_config.get("database", "")

            # Build connection string
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

            # Create connection with timeout
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
    """Database connection pool service with enhanced features"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.engine = None
        self.pool_size = config.get("pool_size", 5)
        self.timeout = config.get("timeout", 30)
        self._setup_engine()

    def _setup_engine(self):
        """Setup SQLAlchemy engine with connection pool"""
        try:
            conn_str = self._build_connection_string()

            self.engine = create_engine(
                conn_str,
                poolclass=QueuePool,
                pool_size=self.pool_size,
                max_overflow=2,
                pool_timeout=self.timeout,
                pool_pre_ping=True,
            )

            # Setup event listeners
            event.listen(self.engine, "checkout", self._on_checkout)
            event.listen(self.engine, "checkin", self._on_checkin)

            logger.info("Connection pool initialized")

        except Exception as e:
            logger.error(f"Failed to setup connection pool: {e}")
            raise

    def _build_connection_string(self) -> str:
        """Build connection string based on config"""
        if self.config["type"] == "sqlite":
            return f"sqlite:///{self.config['file']}"

        elif self.config["type"] == "sqlserver":
            params = []

            # Server
            server = self.config["server"]
            if "\\" in server:  # Named instance
                params.append(f"SERVER={server}")
            else:
                host, port = server.split(":") if ":" in server else (server, "1433")
                params.append(f"SERVER={host},{port}")

            # Database
            params.append(f"DATABASE={self.config['database']}")

            # Authentication
            if self.config.get("use_windows_auth", True):
                params.append("Trusted_Connection=yes")
            else:
                params.append(f"UID={self.config['username']}")
                params.append(f"PWD={self.config['password']}")

            # Additional params
            params.extend(
                [
                    "DRIVER={ODBC Driver 17 for SQL Server}",
                    "TrustServerCertificate=yes",
                    f"Connection Timeout={self.timeout}",
                ]
            )

            return "mssql+pyodbc:///?" + "&".join(params)

        raise ValueError(f"Unsupported database type: {self.config['type']}")

    @contextmanager
    def get_connection(self):
        """Get connection from pool with auto-release"""
        connection = None
        try:
            connection = self.engine.connect()
            yield connection
        finally:
            if connection:
                connection.close()

    def test_connection(self) -> Tuple[bool, str]:
        """Test database connection"""
        try:
            with self.get_connection() as conn:
                conn.execute("SELECT 1")
            return True, "Connection successful"
        except SQLAlchemyError as e:
            return False, str(e)

    def get_pool_stats(self) -> Dict[str, int]:
        """Get connection pool statistics"""
        if not self.engine:
            return {}

        return {
            "pool_size": self.pool_size,
            "current_connections": self.engine.pool.size(),
            "in_use_connections": self.engine.pool.checkedin(),
            "overflow_connections": self.engine.pool.overflow(),
        }

    def _on_checkout(self, dbapi_connection, connection_record, connection_proxy):
        """Connection checkout event handler"""
        logger.debug("Connection checked out from pool")

    def _on_checkin(self, dbapi_connection, connection_record):
        """Connection checkin event handler"""
        logger.debug("Connection returned to pool")

    def cleanup(self):
        """Cleanup connection pool"""
        if self.engine:
            self.engine.dispose()
            logger.info("Connection pool disposed")

    def connect_database(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Connect to database with enhanced error handling"""
        try:
            if config["type"] == "sqlite":
                conn_str = f"sqlite:///{config['file']}"
            else:
                conn_str = self._build_mssql_conn_str(config)

            # Test connection before creating pool
            test_engine = create_engine(conn_str)
            with test_engine.connect() as conn:
                conn.execute("SELECT 1")

            # Create connection pool
            self.engine = create_engine(
                conn_str,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30,
                pool_pre_ping=True,
            )

            return True, "Connected successfully"

        except exc.OperationalError as e:
            error = str(e)
            if "timeout" in error.lower():
                return False, "Connection timeout - check server availability"
            elif "login failed" in error.lower():
                return False, "Login failed - check credentials"
            else:
                return False, f"Connection failed: {error}"

        except exc.DBAPIError as e:
            return False, f"Database API error: {str(e)}"

        except Exception as e:
            return False, f"Unexpected error: {str(e)}"

    def _build_mssql_conn_str(self, config: Dict[str, Any]) -> str:
        """Build SQL Server connection string safely"""
        try:
            server = config["server"]
            database = config["database"]

            # Build connection string
            if config.get("use_windows_auth", True):
                conn_str = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={server};"
                    f"DATABASE={database};"
                    f"Trusted_Connection=yes;"
                    f"TrustServerCertificate=yes;"
                    f"Encrypt=no;"
                )
            else:
                username = config["username"]
                password = config["password"]
                conn_str = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={server};"
                    f"DATABASE={database};"
                    f"UID={username};"
                    f"PWD={password};"
                    f"TrustServerCertificate=yes;"
                    f"Encrypt=no;"
                )

            return conn_str

        except KeyError as e:
            raise ValueError(f"Missing required config: {str(e)}")
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
                check_query = """
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name = ?
                """
            else:
                check_query = """
                    SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_NAME = ?
                """

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
