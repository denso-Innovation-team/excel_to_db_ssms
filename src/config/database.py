from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from .settings import settings
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.Base = declarative_base()
        self._setup_engine()

    def _setup_engine(self):
        url = settings.get_database_url()
        
        self.engine = create_engine(
            url,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False,
            connect_args={
                "sslmode": "require",
                "connect_timeout": 30,
                "application_name": "excel_to_db_processor"
            }
        )
        
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        logger.info("✅ Supabase PostgreSQL engine configured")

    def get_session(self):
        return self.SessionLocal()

    def test_connection(self):
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1 as test"))
                return True
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False

db_manager = DatabaseManager()
