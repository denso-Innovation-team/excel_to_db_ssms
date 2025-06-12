from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from .settings import settings
import logging
import time

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Production SQL Server Database Manager"""

    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.Base = declarative_base()

    def _setup_engine(self):
        """Setup production SQL Server engine"""
        try:
            connection_url = settings.get_database_url()

            self.engine = create_engine(
                connection_url,
                pool_size=settings.POOL_SIZE,
                max_overflow=settings.MAX_OVERFLOW,
                pool_timeout=settings.POOL_TIMEOUT,
                pool_recycle=settings.POOL_RECYCLE,
                pool_pre_ping=True,
                echo=False,
                fast_executemany=True,
                connect_args={
                    "timeout": 30,
                    "autocommit": False,
                },
            )

            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT @@SERVERNAME, DB_NAME()"))
                server, database = result.fetchone()
                logger.info(f"✅ Connected to: {server}/{database}")

            self.SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine
            )
            return True

        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            return False

    def test_connection(self) -> bool:
        """Test production database connection"""
        if not self.engine:
            if not self._setup_engine():
                return False

        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                return result.fetchone()[0] == 1
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False

    def get_pool_status(self) -> dict:
        """Get connection pool status"""
        if not self.engine:
            return {"error": "No engine"}

        try:
            pool = self.engine.pool
            return {
                "pool_size": pool.size(),
                "checked_in": pool.checkedin(),
                "checked_out": pool.checkedout(),
                "overflow": pool.overflow(),
                "total_connections": pool.size() + pool.overflow(),
            }
        except Exception as e:
            return {"error": str(e)}

    def cleanup_connections(self):
        """Clean up database connections"""
        try:
            if self.engine:
                self.engine.dispose()
                logger.info("✅ Database connections cleaned up")
        except Exception as e:
            logger.error(f"Connection cleanup error: {e}")


# Global database manager instance
db_manager = DatabaseManager()
