"""
services/connection_pool_service.py
Enhanced Connection Pool Service for Multiple Database Types
"""

import pyodbc
import sqlite3
import threading
from typing import Dict, List, Any
from contextlib import contextmanager
import time


class ConnectionPool:
    """Connection pool สำหรับจัดการการเชื่อมต่อฐานข้อมูล"""

    def __init__(
        self, connection_string: str, pool_size: int = 5, max_overflow: int = 10
    ):
        self.connection_string = connection_string
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.connections = []
        self.checked_out = set()
        self.overflow_connections = set()
        self.lock = threading.Lock()

    def get_connection(self):
        """ดึง connection จาก pool"""
        with self.lock:
            # Try to get from pool
            if self.connections:
                conn = self.connections.pop()
                self.checked_out.add(conn)
                return conn

            # Create overflow connection if allowed
            if len(self.overflow_connections) < self.max_overflow:
                conn = self._create_connection()
                self.overflow_connections.add(conn)
                self.checked_out.add(conn)
                return conn

            # Wait for available connection
            time.sleep(0.1)
            return self.get_connection()

    def return_connection(self, conn):
        """คืน connection กลับไป pool"""
        with self.lock:
            if conn in self.checked_out:
                self.checked_out.remove(conn)

                if conn in self.overflow_connections:
                    self.overflow_connections.remove(conn)
                    conn.close()
                else:
                    if len(self.connections) < self.pool_size:
                        self.connections.append(conn)
                    else:
                        conn.close()

    def _create_connection(self):
        """สร้าง connection ใหม่"""
        if "sqlite" in self.connection_string.lower():
            return sqlite3.connect(self.connection_string.replace("sqlite:///", ""))
        else:
            return pyodbc.connect(self.connection_string)

    @contextmanager
    def get_managed_connection(self):
        """Context manager สำหรับจัดการ connection อัตโนมัติ"""
        conn = self.get_connection()
        try:
            yield conn
        finally:
            self.return_connection(conn)


class ConnectionPoolService:
    """บริการจัดการ Connection Pool สำหรับหลายฐานข้อมูล"""

    def __init__(self):
        self.pools: Dict[str, ConnectionPool] = {}
        self.current_pool = None
        self.current_config = None

    def connect_database(self, config: Dict[str, Any]) -> bool:
        """เชื่อมต่อกับฐานข้อมูลและสร้าง connection pool"""
        try:
            connection_string = self._build_connection_string(config)
            pool_key = self._get_pool_key(config)

            # Create or get existing pool
            if pool_key not in self.pools:
                self.pools[pool_key] = ConnectionPool(
                    connection_string,
                    pool_size=config.get("pool_size", 5),
                    max_overflow=config.get("max_overflow", 10),
                )

            self.current_pool = self.pools[pool_key]
            self.current_config = config

            # Test connection
            with self.current_pool.get_managed_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.close()

            return True

        except Exception as e:
            print(f"Database connection failed: {e}")
            return False

    def _build_connection_string(self, config: Dict[str, Any]) -> str:
        """สร้าง connection string ตาม database type"""
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
                )

        raise ValueError(f"Unsupported database type: {db_type}")

    def _get_pool_key(self, config: Dict[str, Any]) -> str:
        """สร้าง unique key สำหรับ connection pool"""
        db_type = config.get("type", "sqlite")

        if db_type == "sqlite":
            return f"sqlite_{config.get('file', 'database.db')}"
        elif db_type == "sqlserver":
            return f"sqlserver_{config['server']}_{config['database']}"

        return f"{db_type}_default"

    def get_sqlserver_databases(self) -> List[str]:
        """ดึงรายการฐานข้อมูล SQL Server"""
        try:
            if not self.current_pool or self.current_config.get("type") != "sqlserver":
                return []

            with self.current_pool.get_managed_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sys.databases WHERE database_id > 4")
                databases = [row[0] for row in cursor.fetchall()]
                cursor.close()
                return databases

        except Exception as e:
            print(f"Error getting SQL Server databases: {e}")
            return []

    def get_sqlite_databases(self) -> List[str]:
        """ดึงรายการฐานข้อมูล SQLite ในโฟลเดอร์ปัจจุบัน"""
        try:
            from pathlib import Path

            db_files = list(Path(".").glob("*.db"))
            return [str(db_file) for db_file in db_files]
        except Exception as e:
            print(f"Error getting SQLite databases: {e}")
            return []

    def get_tables(self) -> List[str]:
        """ดึงรายการตารางในฐานข้อมูลปัจจุบัน"""
        try:
            if not self.current_pool:
                return []

            with self.current_pool.get_managed_connection() as conn:
                cursor = conn.cursor()

                if self.current_config.get("type") == "sqlite":
                    cursor.execute(
                        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
                    )
                else:  # SQL Server
                    cursor.execute(
                        "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"
                    )

                tables = [row[0] for row in cursor.fetchall()]
                cursor.close()
                return tables

        except Exception as e:
            print(f"Error getting tables: {e}")
            return []

    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """ดึงโครงสร้างตาราง"""
        try:
            if not self.current_pool:
                return []

            with self.current_pool.get_managed_connection() as conn:
                cursor = conn.cursor()

                if self.current_config.get("type") == "sqlite":
                    cursor.execute(f"PRAGMA table_info({table_name})")
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
                        SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
                        FROM INFORMATION_SCHEMA.COLUMNS 
                        WHERE TABLE_NAME = ?
                        ORDER BY ORDINAL_POSITION
                    """,
                        table_name,
                    )

                    columns = []
                    for row in cursor.fetchall():
                        columns.append(
                            {
                                "name": row[0],
                                "type": row[1],
                                "nullable": row[2] == "YES",
                                "default": row[3],
                                "primary_key": False,  # Would need additional query
                            }
                        )

                cursor.close()
                return columns

        except Exception as e:
            print(f"Error getting table schema: {e}")
            return []

    def bulk_insert(
        self, table_name: str, data: List[Dict], batch_size: int = 1000
    ) -> bool:
        """นำเข้าข้อมูลจำนวนมากด้วย batch processing"""
        try:
            if not self.current_pool or not data:
                return False

            # Get columns from first record
            columns = list(data[0].keys())
            placeholders = ", ".join(["?" for _ in columns])
            column_names = ", ".join([f"[{col}]" for col in columns])

            insert_sql = (
                f"INSERT INTO [{table_name}] ({column_names}) VALUES ({placeholders})"
            )

            with self.current_pool.get_managed_connection() as conn:
                cursor = conn.cursor()

                # Process in batches
                for i in range(0, len(data), batch_size):
                    batch = data[i : i + batch_size]

                    # Prepare batch data
                    batch_values = []
                    for row in batch:
                        values = [row.get(col) for col in columns]
                        batch_values.append(values)

                    # Execute batch insert
                    cursor.executemany(insert_sql, batch_values)

                conn.commit()
                cursor.close()

            return True

        except Exception as e:
            print(f"Bulk insert failed: {e}")
            return False

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """ดำเนินการ query และคืนผลลัพธ์"""
        try:
            if not self.current_pool:
                return []

            with self.current_pool.get_managed_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)

                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()

                result = []
                for row in rows:
                    result.append(dict(zip(columns, row)))

                cursor.close()
                return result

        except Exception as e:
            print(f"Query execution failed: {e}")
            return []

    def close_all_pools(self):
        """ปิด connection pools ทั้งหมด"""
        for pool in self.pools.values():
            # Close all connections in pools
            for conn in pool.connections:
                try:
                    conn.close()
                except:
                    pass

            for conn in pool.overflow_connections:
                try:
                    conn.close()
                except:
                    pass

        self.pools.clear()
        self.current_pool = None
        self.current_config = None
