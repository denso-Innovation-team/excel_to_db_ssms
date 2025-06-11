from sqlalchemy import create_engine, text, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import DisconnectionError
from .settings import settings
import logging
import time

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Enhanced SQL Server Connection Manager with Pooling"""

    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.Base = declarative_base()
        self._setup_engine()

    def _setup_engine(self):
        """Setup SQL Server engine with optimized connection pooling"""

        try:
            connection_url = settings.get_database_url()

            # Optimized connection parameters
            self.engine = create_engine(
                connection_url,
                # Connection Pool Settings
                poolclass=QueuePool,
                pool_size=settings.POOL_SIZE,
                max_overflow=settings.MAX_OVERFLOW,
                pool_timeout=settings.POOL_TIMEOUT,
                pool_recycle=settings.POOL_RECYCLE,
                pool_pre_ping=True,
                # SQL Server Optimizations
                echo=False,
                fast_executemany=True,
                # ODBC Driver 17 Compatible Parameters
                connect_args={
                    "Encrypt": "no",
                    "timeout": 30,
                    "autocommit": False,
                    "TrustServerCertificate": "yes",
                },
            )

            # Setup event listeners for monitoring
            self._setup_engine_events()

            # Test connection
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT @@VERSION, @@SERVERNAME"))
                version, server = result.fetchone()
                logger.info(f"✅ Connected to SQL Server: {server}")
                logger.info(
                    f"📋 Pool configured: {settings.POOL_SIZE}+{settings.MAX_OVERFLOW} connections"
                )

            self.SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine
            )

        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            raise

    def _setup_engine_events(self):
        """Setup SQLAlchemy events for monitoring"""

        @event.listens_for(self.engine, "connect")
        def on_connect(dbapi_connection, connection_record):
            logger.debug("🔗 New database connection established")

        @event.listens_for(self.engine, "checkout")
        def on_checkout(dbapi_connection, connection_record, connection_proxy):
            logger.debug("📤 Connection checked out from pool")

        @event.listens_for(self.engine, "checkin")
        def on_checkin(dbapi_connection, connection_record):
            logger.debug("📥 Connection returned to pool")

    def get_session(self):
        """Get database session with error handling"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Session error: {e}")
            raise
        finally:
            session.close()

    def test_connection(self) -> bool:
        """Test database connection and pool health"""
        try:
            start_time = time.time()

            with self.engine.connect() as conn:
                # Basic connectivity test
                result = conn.execute(text("SELECT 1 as test_value"))
                test_value = result.fetchone()[0]

                # Performance test
                conn.execute(text("SELECT COUNT(*) FROM sys.databases"))

                connection_time = time.time() - start_time

                # Pool status
                pool_status = self.get_pool_status()

                logger.info(f"✅ Connection test successful ({connection_time:.3f}s)")
                logger.info(f"📊 Pool status: {pool_status}")

                return True

        except Exception as e:
            logger.error(f"❌ Connection test failed: {e}")
            return False

    def get_pool_status(self) -> dict:
        """Get connection pool status"""
        pool = self.engine.pool
        return {
            "pool_size": pool.size(),
            "checked_in": pool.checkedin(),
            "checked_out": pool.checkedout(),
            "overflow": pool.overflow(),
            "total_connections": pool.size() + pool.overflow(),
        }

    def create_database_if_not_exists(self):
        """Create database if it doesn't exist"""
        try:
            # Connect to master database
            master_url = settings.get_master_database_url()
            master_engine = create_engine(master_url)

            with master_engine.connect() as conn:
                # Check if database exists
                result = conn.execute(
                    text(
                        f"""
                    SELECT database_id FROM sys.databases 
                    WHERE name = '{settings.DB_NAME}'
                """
                    )
                )

                if not result.fetchone():
                    # Create database with optimized settings
                    conn.execute(
                        text(
                            f"""
                        CREATE DATABASE [{settings.DB_NAME}]
                        COLLATE SQL_Latin1_General_CP1_CI_AS
                    """
                        )
                    )
                    conn.commit()
                    logger.info(f"✅ Created database: {settings.DB_NAME}")
                else:
                    logger.info(f"✅ Database exists: {settings.DB_NAME}")

            master_engine.dispose()

        except Exception as e:
            logger.warning(f"Database creation failed: {e}")

    def execute_bulk_insert(self, table_name: str, data: list) -> int:
        """Optimized bulk insert for SQL Server"""
        try:
            with self.engine.begin() as conn:
                if data:
                    # Use SQL Server bulk insert capabilities
                    placeholders = ", ".join(
                        [
                            f"({', '.join(['?' for _ in data[0]])})"
                            for _ in range(len(data))
                        ]
                    )

                    columns = (
                        ", ".join(data[0].keys()) if isinstance(data[0], dict) else ""
                    )

                    if isinstance(data[0], dict):
                        query = f"""
                            INSERT INTO [{table_name}] ({columns})
                            VALUES {placeholders}
                        """
                        flat_data = [list(row.values()) for row in data]
                    else:
                        query = f"INSERT INTO [{table_name}] VALUES {placeholders}"
                        flat_data = data

                    conn.execute(
                        text(query), [item for sublist in flat_data for item in sublist]
                    )

                logger.info(f"✅ Bulk insert: {len(data)} rows to {table_name}")
                return len(data)

        except Exception as e:
            logger.error(f"❌ Bulk insert failed: {e}")
            raise

    def cleanup_connections(self):
        """Clean up database connections"""
        try:
            if self.engine:
                self.engine.dispose()
                logger.info("✅ Database connections cleaned up")
        except Exception as e:
            logger.error(f"Connection cleanup error: {e}")

    def __del__(self):
        """Cleanup on object destruction"""
        self.cleanup_connections()


# Global database manager instance
db_manager = DatabaseManager()
