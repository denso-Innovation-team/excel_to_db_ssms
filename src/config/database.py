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
        """Setup SQL Server engine with fallback options"""
        
        # Try ODBC first (recommended)
        try:
            url = settings.get_database_url()
            self.engine = create_engine(
                url,
                pool_size=5,
                max_overflow=10,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False,
                connect_args={
                    "timeout": 30,
                    "autocommit": False
                }
            )
            
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            logger.info("✅ SQL Server connected via ODBC Driver")
            
        except Exception as e:
            logger.warning(f"ODBC connection failed: {e}")
            
            # Fallback to pymssql
            try:
                url = settings.get_pymssql_url()
                self.engine = create_engine(
                    url,
                    pool_size=5,
                    max_overflow=10,
                    pool_pre_ping=True,
                    echo=False
                )
                
                # Test connection
                with self.engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                
                logger.info("✅ SQL Server connected via pymssql")
                
            except Exception as e2:
                logger.error(f"Both connection methods failed: ODBC({e}), pymssql({e2})")
                raise
        
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        return self.SessionLocal()

    def test_connection(self):
        """ทดสอบการเชื่อมต่อ SQL Server"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT @@VERSION as version"))
                version = result.fetchone()[0]
                logger.info(f"SQL Server version: {version[:50]}...")
                return True
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def create_database_if_not_exists(self):
        """สร้าง database หากยังไม่มี (เฉพาะ SQL Server)"""
        try:
            # Connect to master database first
            master_url = settings.get_database_url().replace(f"/{settings.DB_NAME}", "/master")
            master_engine = create_engine(master_url)
            
            with master_engine.connect() as conn:
                # Check if database exists
                result = conn.execute(text(f"""
                    SELECT database_id FROM sys.databases 
                    WHERE name = '{settings.DB_NAME}'
                """))
                
                if not result.fetchone():
                    # Create database
                    conn.execute(text(f"CREATE DATABASE [{settings.DB_NAME}]"))
                    conn.commit()
                    logger.info(f"✅ Created database: {settings.DB_NAME}")
                else:
                    logger.info(f"✅ Database exists: {settings.DB_NAME}")
                    
        except Exception as e:
            logger.warning(f"Could not create database: {e}")

db_manager = DatabaseManager()
