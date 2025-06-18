"""
services/connection_pool_service.py
Enhanced Connection Pool Service - PRODUCTION READY
Fixed: Error handling, null checks, และ threading safety
"""

import sqlite3
import threading
from typing import Dict, List, Any, Optional, Tuple
from contextlib import contextmanager
import time
import logging
from datetime import datetime
from pathlib import Path
import queue

logger = logging.getLogger(__name__)


class ConnectionPool:
    """Production-ready connection pool with comprehensive error handling"""

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
        self.connections = queue.Queue(maxsize=pool_size)
        self.checked_out = set()
        self.overflow_connections = set()
        self.lock = threading.RLock()  # Re-entrant lock for nested calls
        self.created_at = datetime.now()
        self.total_connections_created = 0
        self.connection_errors = 0
        self._shutdown = False

        # Pre-populate pool
        self._initialize_pool()

    def _initialize_pool(self):
        """Initialize pool with minimum connections"""
        for _ in range(min(self.pool_size, 2)):  # Start with 2 connections
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
                    logger.debug(
                        f"Retrieved connection from pool. Queue size: {self.connections.qsize()}"
                    )
                    return conn
                else:
                    # Connection is invalid, discard it
                    logger.warning("Retrieved invalid connection, discarding")
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
                        logger.debug(
                            f"Created new connection. Total active: {total_active + 1}"
                        )
                        return conn
                    except Exception as e:
                        self.connection_errors += 1
                        logger.error(f"Failed to create connection: {e}")
                        # Continue to retry

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
                # Connection not tracked, just close it
                try:
                    conn.close()
                except:
                    pass
                return

            self.checked_out.remove(conn)

            # Test connection before returning to pool
            if self._is_connection_valid(conn):
                if conn in self.overflow_connections:
                    self.overflow_connections.remove(conn)
                    try:
                        conn.close()
                    except:
                        pass
                    logger.debug("Closed overflow connection")
                else:
                    try:
                        self.connections.put_nowait(conn)
                        logger.debug(
                            f"Returned connection to pool. Queue size: {self.connections.qsize()}"
                        )
                    except queue.Full:
                        # Pool is full, close connection
                        try:
                            conn.close()
                        except:
                            pass
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
        """Create new database connection with proper error handling"""
        if "sqlite" in self.connection_string.lower():
            return self._create_sqlite_connection()
        else:
            return self._create_sqlserver_connection()

    def _create_sqlite_connection(self):
        """Create SQLite connection with optimizations"""
        try:
            # Extract file path from connection string
            if self.connection_string.startswith("sqlite:///"):
                db_path = self.connection_string[10:]  # Remove sqlite:///
            else:
                db_path = self.connection_string

            # Ensure directory exists
            db_dir = Path(db_path).parent
            if db_dir != Path("."):  # Only create if not current directory
                db_dir.mkdir(parents=True, exist_ok=True)

            # Create connection with optimizations
            conn = sqlite3.connect(
                db_path,
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
        """Create SQL Server connection"""
        try:
            import pyodbc

            # Connection string should already be formatted
            conn = pyodbc.connect(self.connection_string, timeout=30)
            conn.autocommit = False
            return conn

        except ImportError:
            raise Exception(
                "pyodbc module required for SQL Server connections. Install with: pip install pyodbc"
            )
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
            result = cursor.fetchone()
            cursor.close()
            return result is not None
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
            # Rollback on error
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
        """Close all connections in pool safely"""
        logger.info("Closing all connections in pool...")
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

        logger.info("All connections closed")

    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive pool statistics"""
        with self.lock:
            return {
                "pool_size": self.pool_size,
                "max_overflow": self.max_overflow,
                "connections_in_pool": self.connections.qsize(),
                "checked_out_connections": len(self.checked_out),
                "overflow_connections": len(self.overflow_connections),
                "total_connections_created": self.total_connections_created,
                "connection_errors": self.connection_errors,
                "uptime_seconds": (datetime.now() - self.created_at).total_seconds(),
                "is_shutdown": self._shutdown,
            }

    def __del__(self):
        """Cleanup on destruction"""
        try:
            self.close_all()
        except:
            pass


class ConnectionPoolService:
    """Enhanced connection pool service with robust error handling"""

    def __init__(self):
        self.pools: Dict[str, ConnectionPool] = {}
        self.current_pool: Optional[ConnectionPool] = None
        self.current_config: Optional[Dict[str, Any]] = None
        self.service_stats = {
            "total_queries": 0,
            "failed_queries": 0,
            "start_time": datetime.now(),
        }
        self._lock = threading.RLock()

    def connect_database(self, config: Dict[str, Any]) -> bool:
        """Connect to database with comprehensive validation"""
        try:
            # Validate config
            if not self._validate_config(config):
                logger.error("Invalid database configuration")
                return False

            db_type = config.get("type", "sqlite")
            logger.info(f"Connecting to {db_type} database...")

            connection_string = self._build_connection_string(config)
            pool_key = self._get_pool_key(config)

            with self._lock:
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
                self.current_config = config.copy()

            # Test connection
            with self.current_pool.get_managed_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                cursor.close()

                if not result:
                    raise Exception("Connection test failed")

            logger.info(f"Successfully connected to database: {pool_key}")
            return True

        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            self.current_pool = None
            self.current_config = None
            return False

    def _validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate database configuration"""
        if not isinstance(config, dict):
            return False

        db_type = config.get("type")
        if not db_type:
            return False

        if db_type == "sqlite":
            # SQLite just needs a file path
            return True
        elif db_type == "sqlserver":
            required_fields = ["server", "database"]
            return all(config.get(field) for field in required_fields)
        else:
            return False

    def _build_connection_string(self, config: Dict[str, Any]) -> str:
        """Build connection string with proper validation"""
        db_type = config.get("type", "sqlite")

        if db_type == "sqlite":
            db_file = config.get("file", "denso888_data.db")
            return f"sqlite:///{db_file}"

        elif db_type == "sqlserver":
            server = config["server"]
            database = config["database"]

            base_conn = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
            )

            if config.get("use_windows_auth", True):
                return base_conn + "Trusted_Connection=yes;TrustServerCertificate=yes;"
            else:
                username = config.get("username", "")
                password = config.get("password", "")
                return (
                    base_conn
                    + f"UID={username};PWD={password};TrustServerCertificate=yes;"
                )

        raise ValueError(f"Unsupported database type: {db_type}")

    def _get_pool_key(self, config: Dict[str, Any]) -> str:
        """Generate unique key for connection pool"""
        db_type = config.get("type", "sqlite")

        if db_type == "sqlite":
            db_file = config.get("file", "database.db")
            return f"sqlite_{Path(db_file).absolute()}"
        elif db_type == "sqlserver":
            server = config.get("server", "")
            database = config.get("database", "")
            return f"sqlserver_{server}_{database}".replace("\\", "_")

        return f"{db_type}_default"

    def execute_query(self, query: str, params: Tuple = ()) -> Tuple[bool, Any]:
        """Execute query with comprehensive error handling"""
        if not self.current_pool:
            return False, "No database connection available"

        try:
            with self.current_pool.get_managed_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)

                if query.strip().upper().startswith("SELECT"):
                    # For SELECT queries, return data
                    columns = (
                        [desc[0] for desc in cursor.description]
                        if cursor.description
                        else []
                    )
                    rows = cursor.fetchall()
                    cursor.close()

                    # Convert to list of dictionaries
                    result = []
                    for row in rows:
                        row_dict = {}
                        for i, value in enumerate(row):
                            column_name = columns[i] if i < len(columns) else f"col_{i}"
                            row_dict[column_name] = value
                        result.append(row_dict)

                    self.service_stats["total_queries"] += 1
                    return True, result
                else:
                    # For non-SELECT queries, commit and return affected rows
                    conn.commit()
                    affected_rows = getattr(cursor, "rowcount", 0)
                    cursor.close()
                    self.service_stats["total_queries"] += 1
                    return (
                        True,
                        f"Query executed successfully. {affected_rows} rows affected.",
                    )

        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            self.service_stats["failed_queries"] += 1
            return False, str(e)

    def get_tables(self) -> List[str]:
        """Get list of tables with error handling"""
        if not self.current_pool or not self.current_config:
            return []

        try:
            if self.current_config.get("type") == "sqlite":
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
                return [row[list(row.keys())[0]] for row in result]
            else:
                logger.warning(f"Failed to get tables: {result}")
                return []

        except Exception as e:
            logger.error(f"Error getting tables: {e}")
            return []

    def bulk_insert(
        self, table_name: str, data: List[Dict], batch_size: int = 1000
    ) -> bool:
        """Enhanced bulk insert with comprehensive error handling"""
        if not self.current_pool or not data:
            logger.warning("No connection pool or data for bulk insert")
            return False

        if not table_name or not isinstance(table_name, str):
            logger.error("Invalid table name for bulk insert")
            return False

        try:
            logger.info(f"Starting bulk insert to {table_name}: {len(data)} records")

            # Validate data structure
            if not all(isinstance(row, dict) for row in data):
                logger.error("All data rows must be dictionaries")
                return False

            # Get columns from first record
            columns = list(data[0].keys())
            if not columns:
                logger.error("No columns found in data")
                return False

            # Prepare SQL
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
                    batch_num = i // batch_size + 1

                    try:
                        # Prepare batch data with validation
                        batch_values = []
                        for row_idx, row in enumerate(batch):
                            try:
                                values = []
                                for col in columns:
                                    value = row.get(col)
                                    # Handle None and convert types appropriately
                                    if value is None:
                                        values.append(None)
                                    elif isinstance(value, (str, int, float, bool)):
                                        values.append(value)
                                    else:
                                        values.append(str(value))
                                batch_values.append(values)
                            except Exception as e:
                                logger.warning(
                                    f"Skipping invalid row {row_idx} in batch {batch_num}: {e}"
                                )

                        if not batch_values:
                            logger.warning(f"No valid data in batch {batch_num}")
                            continue

                        # Execute batch insert
                        cursor.executemany(insert_sql, batch_values)
                        total_inserted += len(batch_values)

                        # Progress logging
                        progress = min(100, (total_inserted / len(data)) * 100)
                        logger.debug(
                            f"Bulk insert progress: {progress:.1f}% ({total_inserted}/{len(data)})"
                        )

                    except Exception as batch_error:
                        logger.warning(
                            f"Batch {batch_num} insert failed: {batch_error}"
                        )
                        failed_batches += 1

                        # Try inserting records one by one in failed batch
                        for record in batch:
                            try:
                                values = [record.get(col) for col in columns]
                                cursor.execute(insert_sql, values)
                                total_inserted += 1
                            except Exception as record_error:
                                logger.debug(
                                    f"Failed to insert individual record: {record_error}"
                                )

                # Commit transaction
                conn.commit()
                cursor.close()

            success_rate = (total_inserted / len(data)) * 100 if data else 0
            logger.info(
                f"Bulk insert completed: {total_inserted}/{len(data)} records ({success_rate:.1f}% success)"
            )

            if failed_batches > 0:
                logger.warning(
                    f"Had {failed_batches} failed batches, recovered with individual inserts"
                )

            self.service_stats["total_queries"] += 1
            return total_inserted > 0

        except Exception as e:
            logger.error(f"Bulk insert failed completely: {e}")
            self.service_stats["failed_queries"] += 1
            return False

    def get_service_stats(self) -> Dict[str, Any]:
        """Get comprehensive service statistics"""
        uptime = datetime.now() - self.service_stats["start_time"]

        stats = {
            **self.service_stats,
            "uptime_seconds": uptime.total_seconds(),
            "active_pools": len(self.pools),
            "success_rate": 0,
            "current_pool_key": None,
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
            if self.current_config:
                stats["current_pool_key"] = self._get_pool_key(self.current_config)

        return stats

    def close_all_pools(self):
        """Close all connection pools safely"""
        logger.info("Closing all connection pools")

        with self._lock:
            for pool_name, pool in list(self.pools.items()):
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
        try:
            self.close_all_pools()
        except:
            pass
