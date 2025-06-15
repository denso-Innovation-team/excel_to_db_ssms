"""
utils/database_utils.py
Database Utility Functions
"""

import sqlite3
import logging
from typing import Dict, Any, List, Tuple, Optional
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)


class DatabaseHelper:
    """Database utility functions"""

    @staticmethod
    def test_sqlite_connection(db_path: str) -> Tuple[bool, str]:
        """Test SQLite database connection"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            conn.close()
            return True, f"SQLite connection successful: {db_path}"
        except Exception as e:
            return False, f"SQLite connection failed: {str(e)}"

    @staticmethod
    def get_sqlite_tables(db_path: str) -> List[str]:
        """Get list of tables in SQLite database"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
            """
            )
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()
            return tables
        except Exception as e:
            logger.error(f"Error getting SQLite tables: {e}")
            return []

    @staticmethod
    def get_table_schema(db_path: str, table_name: str) -> List[Dict[str, Any]]:
        """Get table schema information"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
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
            conn.close()
            return columns
        except Exception as e:
            logger.error(f"Error getting table schema: {e}")
            return []

    @staticmethod
    def execute_safe_query(
        db_path: str, query: str, params: tuple = ()
    ) -> Tuple[bool, Any]:
        """Execute query safely"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(query, params)

            if query.strip().upper().startswith("SELECT"):
                result = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                conn.close()
                return True, {"columns": columns, "rows": result}
            else:
                conn.commit()
                affected = cursor.rowcount
                conn.close()
                return True, f"Query executed successfully. {affected} rows affected."
        except Exception as e:
            return False, str(e)


def connection_string_builder(config: Dict[str, Any]) -> Optional[str]:
    """Build database connection string"""
    db_type = config.get("db_type", "sqlite")

    if db_type == "sqlite":
        return f"sqlite:///{config.get('sqlite_file', 'denso888.db')}"

    elif db_type == "sqlserver":
        server = config.get("server", "")
        database = config.get("database", "")

        if config.get("use_windows_auth", True):
            return (
                f"mssql+pyodbc://@{server}/{database}"
                f"?driver=ODBC+Driver+17+for+SQL+Server"
                f"&trusted_connection=yes"
            )
        else:
            username = quote_plus(config.get("username", ""))
            password = quote_plus(config.get("password", ""))
            return (
                f"mssql+pyodbc://{username}:{password}@{server}/{database}"
                f"?driver=ODBC+Driver+17+for+SQL+Server"
            )

    return None
