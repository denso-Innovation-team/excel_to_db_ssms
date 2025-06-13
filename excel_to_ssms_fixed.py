#!/usr/bin/env python3

import pandas as pd
import sqlalchemy as sa
from sqlalchemy import (
    create_engine,
    text,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
)
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError
import os
import sys
import time
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Iterator, List
from urllib.parse import quote_plus
from tqdm import tqdm
from datetime import datetime
import pyodbc
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from contextlib import contextmanager


# =================== CONFIGURATION ===================
class DatabaseConfig:
    """Database configuration with connection testing"""

    def __init__(self):
        # Load from environment
        self.DB_HOST = os.getenv("DB_HOST", "10.73.148.27")
        self.DB_NAME = os.getenv("DB_NAME", "excel_to_db")
        self.DB_USER = os.getenv("DB_USER", "TS00029")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", "Thammaphon@TS00029")

        # Pool settings - Conservative for stability
        self.POOL_SIZE = int(os.getenv("POOL_SIZE", "3"))
        self.MAX_OVERFLOW = int(os.getenv("MAX_OVERFLOW", "5"))
        self.POOL_TIMEOUT = 30
        self.POOL_RECYCLE = 3600

        # Processing settings
        self.BATCH_SIZE = int(os.getenv("BATCH_SIZE", "500"))
        self.MAX_WORKERS = int(os.getenv("MAX_WORKERS", "2"))
        self.CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "2000"))

        # Logging
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    def get_connection_variations(self) -> List[Dict[str, str]]:
        """Get multiple connection string variations to try"""
        password_encoded = quote_plus(self.DB_PASSWORD)

        return [
            {
                "name": "Default Instance",
                "url": f"mssql+pyodbc://{self.DB_USER}:{password_encoded}@{self.DB_HOST}/{self.DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes&Encrypt=no",
                "direct": f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.DB_HOST};DATABASE={self.DB_NAME};UID={self.DB_USER};PWD={self.DB_PASSWORD};TrustServerCertificate=yes;Encrypt=no;",
            },
            {
                "name": "Port 1433",
                "url": f"mssql+pyodbc://{self.DB_USER}:{password_encoded}@{self.DB_HOST}:1433/{self.DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes&Encrypt=no",
                "direct": f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.DB_HOST},1433;DATABASE={self.DB_NAME};UID={self.DB_USER};PWD={self.DB_PASSWORD};TrustServerCertificate=yes;Encrypt=no;",
            },
            {
                "name": "Named Instance MSSQL2S",
                "url": f"mssql+pyodbc://{self.DB_USER}:{password_encoded}@{self.DB_HOST}\\MSSQL2S/{self.DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes&Encrypt=no",
                "direct": f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.DB_HOST}\\MSSQL2S;DATABASE={self.DB_NAME};UID={self.DB_USER};PWD={self.DB_PASSWORD};TrustServerCertificate=yes;Encrypt=no;",
            },
        ]


# =================== ENHANCED DATABASE MANAGER ===================
class DatabaseManager:
    """Enhanced database manager with automatic connection testing"""

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.engine = None
        self.working_connection = None
        self._lock = threading.Lock()
        self.setup_logging()

    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=getattr(logging, self.config.LOG_LEVEL),
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler("logs/excel_to_ssms.log", encoding="utf-8"),
            ],
        )
        self.logger = logging.getLogger(__name__)

        # Create logs directory
        Path("logs").mkdir(exist_ok=True)

    def find_working_connection(self) -> bool:
        """Find a working connection from multiple variations"""
        variations = self.config.get_connection_variations()

        self.logger.info("🔍 Testing SQL Server connections...")

        for variation in variations:
            self.logger.info(f"  Testing: {variation['name']}")

            try:
                # Test direct pyodbc connection first
                conn = pyodbc.connect(variation["direct"], timeout=10)
                cursor = conn.cursor()
                cursor.execute("SELECT @@SERVERNAME, DB_NAME()")
                server, database = cursor.fetchone()
                conn.close()

                self.logger.info(f"    ✅ Direct connection OK: {server}/{database}")

                # Now test SQLAlchemy
                test_engine = create_engine(
                    variation["url"],
                    pool_size=1,
                    max_overflow=1,
                    pool_timeout=10,
                    echo=False,
                )

                with test_engine.connect() as test_conn:
                    result = test_conn.execute(text("SELECT 1"))
                    if result.fetchone()[0] == 1:
                        self.working_connection = variation
                        self.logger.info(f"    ✅ SQLAlchemy connection OK")
                        test_engine.dispose()
                        return True

                test_engine.dispose()

            except Exception as e:
                self.logger.info(f"    ❌ Failed: {str(e)[:100]}...")
                continue

        return False

    def create_engine(self) -> bool:
        """Create SQLAlchemy engine with working connection"""
        with self._lock:
            if self.engine:
                return True

            if not self.working_connection:
                if not self.find_working_connection():
                    self.logger.error("❌ No working connection found")
                    return False

            try:
                self.engine = create_engine(
                    self.working_connection["url"],
                    poolclass=QueuePool,
                    pool_size=self.config.POOL_SIZE,
                    max_overflow=self.config.MAX_OVERFLOW,
                    pool_timeout=self.config.POOL_TIMEOUT,
                    pool_recycle=self.config.POOL_RECYCLE,
                    pool_pre_ping=True,
                    echo=False,
                    connect_args={"timeout": 30, "autocommit": False},
                )

                # Verify engine works
                with self.engine.connect() as conn:
                    result = conn.execute(text("SELECT @@SERVERNAME, DB_NAME()"))
                    server, database = result.fetchone()
                    self.logger.info(f"✅ Engine created: {server}/{database}")

                return True

            except Exception as e:
                self.logger.error(f"❌ Engine creation failed: {e}")
                return False

    def test_connection(self) -> bool:
        """Test database connection"""
        if not self.engine and not self.create_engine():
            return False

        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                return result.fetchone()[0] == 1
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False

    @contextmanager
    def get_connection(self):
        """Get database connection with proper cleanup"""
        if not self.engine and not self.create_engine():
            raise ConnectionError("Cannot establish database connection")

        conn = self.engine.connect()
        try:
            yield conn
        finally:
            conn.close()

    def get_pool_status(self) -> Dict[str, Any]:
        """Get connection pool status"""
        if not self.engine:
            return {"status": "No engine"}

        try:
            pool = self.engine.pool
            return {
                "pool_size": pool.size(),
                "checked_in": pool.checkedin(),
                "checked_out": pool.checkedout(),
                "overflow": pool.overflow(),
                "total": pool.size() + pool.overflow(),
            }
        except Exception as e:
            return {"error": str(e)}


# =================== ENHANCED EXCEL READER ===================
class ExcelReader:
    """Enhanced Excel reader with better error handling"""

    def __init__(self, file_path: str, sheet_name: Optional[str] = None):
        self.file_path = Path(file_path)
        self.sheet_name = sheet_name
        self.total_rows = 0

    def validate_file(self) -> bool:
        """Validate Excel file"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        if self.file_path.suffix.lower() not in [".xlsx", ".xls"]:
            raise ValueError("File must be Excel format (.xlsx or .xls)")
        return True

    def get_file_info(self) -> Dict[str, Any]:
        """Get comprehensive file information"""
        self.validate_file()

        try:
            with pd.ExcelFile(self.file_path) as excel_file:
                sheets = excel_file.sheet_names
                target_sheet = self.sheet_name or sheets[0]

                # Get sample for columns
                df_sample = pd.read_excel(excel_file, sheet_name=target_sheet, nrows=5)

                # Count total rows efficiently
                df_count = pd.read_excel(
                    excel_file, sheet_name=target_sheet, usecols=[0]
                )
                self.total_rows = len(df_count)

                return {
                    "sheets": sheets,
                    "target_sheet": target_sheet,
                    "total_rows": self.total_rows,
                    "columns": df_sample.columns.tolist(),
                    "sample_data": df_sample.head(3).to_dict("records"),
                    "file_size_mb": self.file_path.stat().st_size / 1024 / 1024,
                }

        except Exception as e:
            raise Exception(f"Error reading Excel file: {e}")

    def read_chunks(self, chunk_size: int = 2000) -> Iterator[pd.DataFrame]:
        """Read Excel file in chunks with better memory management"""
        self.validate_file()

        try:
            # Read entire file first (for smaller files, this is more efficient)
            df_full = pd.read_excel(self.file_path, sheet_name=self.sheet_name or 0)

            # Process in chunks
            for start in range(0, len(df_full), chunk_size):
                end = min(start + chunk_size, len(df_full))
                chunk = df_full.iloc[start:end].copy()

                if not chunk.empty:
                    yield chunk

        except Exception as e:
            raise Exception(f"Error reading Excel chunks: {e}")


# =================== DATA VALIDATOR ===================
class DataValidator:
    """Enhanced data validator with type inference"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize DataFrame"""
        df_clean = df.copy()

        # Clean column names
        df_clean.columns = [self._clean_column_name(col) for col in df_clean.columns]

        # Remove completely empty rows
        df_clean = df_clean.dropna(how="all")

        # Clean string columns
        for col in df_clean.select_dtypes(include=["object"]).columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()
            df_clean[col] = df_clean[col].replace(["nan", "None", "null", ""], None)

        return df_clean

    def _clean_column_name(self, col_name: str) -> str:
        """Clean column name for database compatibility"""
        import re

        clean_name = re.sub(r"[^a-zA-Z0-9_\u0E00-\u0E7F]", "_", str(col_name))
        clean_name = re.sub(r"_+", "_", clean_name).strip("_")
        return clean_name

    def infer_data_types(self, df: pd.DataFrame) -> Dict[str, str]:
        """Infer data types from DataFrame"""
        type_mapping = {}

        for col in df.columns:
            col_lower = col.lower()

            # Check actual data
            sample_data = df[col].dropna().head(100)

            if len(sample_data) == 0:
                type_mapping[col] = "string"
                continue

            # Try to infer from column name patterns
            if any(
                pattern in col_lower for pattern in ["id", "number", "count", "จำนวน"]
            ):
                if pd.api.types.is_integer_dtype(sample_data):
                    type_mapping[col] = "integer"
                else:
                    type_mapping[col] = "string"
            elif any(
                pattern in col_lower
                for pattern in ["price", "amount", "salary", "ราคา", "เงิน"]
            ):
                try:
                    pd.to_numeric(sample_data)
                    type_mapping[col] = "float"
                except:
                    type_mapping[col] = "string"
            elif any(pattern in col_lower for pattern in ["date", "time", "วันที่"]):
                try:
                    pd.to_datetime(sample_data)
                    type_mapping[col] = "datetime"
                except:
                    type_mapping[col] = "string"
            else:
                type_mapping[col] = "string"

        return type_mapping

    def apply_data_types(
        self, df: pd.DataFrame, type_mapping: Dict[str, str]
    ) -> pd.DataFrame:
        """Apply data type conversions"""
        df_typed = df.copy()

        for col, target_type in type_mapping.items():
            if col not in df_typed.columns:
                continue

            try:
                if target_type == "integer":
                    df_typed[col] = (
                        pd.to_numeric(df_typed[col], errors="coerce")
                        .fillna(0)
                        .astype("Int64")
                    )
                elif target_type == "float":
                    df_typed[col] = pd.to_numeric(
                        df_typed[col], errors="coerce"
                    ).fillna(0.0)
                elif target_type == "datetime":
                    df_typed[col] = pd.to_datetime(df_typed[col], errors="coerce")
                elif target_type == "boolean":
                    df_typed[col] = (
                        df_typed[col]
                        .astype(str)
                        .str.lower()
                        .isin(["true", "1", "yes", "y"])
                    )
                # string is default, no conversion needed

            except Exception as e:
                self.logger.warning(f"Type conversion failed for {col}: {e}")

        return df_typed


# =================== DATABASE WRITER ===================
class DatabaseWriter:
    """Enhanced database writer with better error handling"""

    def __init__(self, table_name: str, db_manager: DatabaseManager):
        self.table_name = table_name
        self.db_manager = db_manager
        self.logger = logging.getLogger(__name__)

    def create_table_from_dataframe(
        self, df_sample: pd.DataFrame, type_mapping: Dict[str, str] = None
    ):
        """Create table with proper SQL Server syntax"""
        try:
            # Build column definitions
            columns_sql = ["id INT IDENTITY(1,1) PRIMARY KEY"]

            for col_name, dtype in df_sample.dtypes.items():
                if type_mapping and col_name in type_mapping:
                    sql_type = self._get_sql_type(type_mapping[col_name])
                else:
                    sql_type = self._infer_sql_type(dtype)

                # Escape column names properly
                columns_sql.append(f"[{col_name}] {sql_type}")

            # SQL statements
            drop_sql = f"IF OBJECT_ID('{self.table_name}', 'U') IS NOT NULL DROP TABLE [{self.table_name}]"
            create_sql = f"CREATE TABLE [{self.table_name}] ({', '.join(columns_sql)})"

            # Execute with transaction
            with self.db_manager.get_connection() as conn:
                with conn.begin():
                    conn.execute(text(drop_sql))
                    conn.execute(text(create_sql))

            self.logger.info(f"✅ Table '{self.table_name}' created successfully")

        except Exception as e:
            self.logger.error(f"❌ Table creation failed: {e}")
            raise

    def _get_sql_type(self, type_name: str) -> str:
        """Convert type name to SQL Server type"""
        type_map = {
            "string": "NVARCHAR(255)",
            "text": "NVARCHAR(MAX)",
            "integer": "INT",
            "float": "FLOAT",
            "boolean": "BIT",
            "datetime": "DATETIME2",
        }
        return type_map.get(type_name, "NVARCHAR(255)")

    def _infer_sql_type(self, pandas_dtype) -> str:
        """Infer SQL type from pandas dtype"""
        if pd.api.types.is_integer_dtype(pandas_dtype):
            return "INT"
        elif pd.api.types.is_float_dtype(pandas_dtype):
            return "FLOAT"
        elif pd.api.types.is_bool_dtype(pandas_dtype):
            return "BIT"
        elif pd.api.types.is_datetime64_any_dtype(pandas_dtype):
            return "DATETIME2"
        else:
            return "NVARCHAR(255)"

    def bulk_insert(self, df: pd.DataFrame) -> int:
        """Optimized bulk insert with proper error handling"""
        try:
            df_clean = df.copy()

            # Handle datetime columns
            for col in df_clean.columns:
                if pd.api.types.is_datetime64_any_dtype(df_clean[col]):
                    df_clean[col] = df_clean[col].dt.strftime("%Y-%m-%d %H:%M:%S")
                    df_clean[col] = df_clean[col].replace("NaT", None)

            # Replace NaN with None
            df_clean = df_clean.where(pd.notnull(df_clean), None)

            # Use to_sql with transaction
            with self.db_manager.get_connection() as conn:
                with conn.begin():
                    df_clean.to_sql(
                        name=self.table_name,
                        con=conn,
                        if_exists="append",
                        index=False,
                        method="multi",
                        chunksize=self.db_manager.config.BATCH_SIZE,
                    )

            rows_inserted = len(df_clean)
            self.logger.info(f"✅ Inserted {rows_inserted:,} rows")
            return rows_inserted

        except Exception as e:
            self.logger.error(f"❌ Bulk insert failed: {e}")
            raise

    def get_table_info(self) -> Dict[str, Any]:
        """Get table information"""
        try:
            with self.db_manager.get_connection() as conn:
                # Get row count
                result = conn.execute(text(f"SELECT COUNT(*) FROM [{self.table_name}]"))
                row_count = result.fetchone()[0]

                # Get column info
                columns_sql = f"""
                    SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = '{self.table_name}'
                    ORDER BY ORDINAL_POSITION
                """
                result = conn.execute(text(columns_sql))
                columns = [(row[0], row[1], row[2]) for row in result.fetchall()]

                return {
                    "table_name": self.table_name,
                    "row_count": row_count,
                    "columns": columns,
                }

        except Exception as e:
            self.logger.error(f"❌ Get table info failed: {e}")
            return {"error": str(e)}


# =================== MAIN PROCESSOR ===================
class ExcelToSSMSProcessor:
    """Main processor with enhanced error handling and monitoring"""

    def __init__(self, excel_file: str, table_name: str, sheet_name: str = None):
        self.excel_file = excel_file
        self.table_name = table_name
        self.sheet_name = sheet_name

        # Initialize components
        self.config = DatabaseConfig()
        self.db_manager = DatabaseManager(self.config)
        self.reader = ExcelReader(excel_file, sheet_name)
        self.validator = DataValidator()
        self.writer = DatabaseWriter(table_name, self.db_manager)

        self.logger = logging.getLogger(__name__)

    def process(self, create_table: bool = True) -> Dict[str, Any]:
        """Main processing method with comprehensive error handling"""
        start_time = time.time()

        try:
            # 1. Test database connection
            self.logger.info("🔍 Testing database connection...")
            if not self.db_manager.test_connection():
                raise Exception("Cannot connect to SQL Server")

            # 2. Analyze Excel file
            self.logger.info("📊 Analyzing Excel file...")
            file_info = self.reader.get_file_info()
            self.logger.info(
                f"File: {file_info['total_rows']:,} rows, {file_info['file_size_mb']:.1f} MB"
            )

            # 3. Process data
            total_inserted = 0
            table_created = False

            with tqdm(
                total=file_info["total_rows"], desc="Processing", unit="rows"
            ) as pbar:
                for chunk_num, chunk in enumerate(
                    self.reader.read_chunks(self.config.CHUNK_SIZE)
                ):
                    # Clean and validate
                    df_clean = self.validator.clean_dataframe(chunk)

                    # Auto-detect types on first chunk
                    if chunk_num == 0:
                        type_mapping = self.validator.infer_data_types(df_clean)
                        self.logger.info(f"Detected types: {type_mapping}")

                    df_typed = self.validator.apply_data_types(df_clean, type_mapping)

                    # Create table on first chunk
                    if create_table and not table_created:
                        self.writer.create_table_from_dataframe(df_typed, type_mapping)
                        table_created = True

                    # Insert data
                    rows_inserted = self.writer.bulk_insert(df_typed)
                    total_inserted += rows_inserted

                    # Update progress
                    pbar.update(len(chunk))
                    pbar.set_postfix(
                        {
                            "Inserted": f"{total_inserted:,}",
                            "Pool": str(
                                self.db_manager.get_pool_status().get("checked_out", 0)
                            ),
                        }
                    )

            # 4. Final results
            processing_time = time.time() - start_time
            table_info = self.writer.get_table_info()

            results = {
                "success": True,
                "total_rows": file_info["total_rows"],
                "inserted_rows": total_inserted,
                "processing_time": processing_time,
                "speed_rows_per_sec": (
                    total_inserted / processing_time if processing_time > 0 else 0
                ),
                "table_info": table_info,
                "pool_status": self.db_manager.get_pool_status(),
            }

            self.logger.info(
                f"🎉 SUCCESS: {total_inserted:,} rows in {processing_time:.2f}s"
            )
            return results

        except Exception as e:
            self.logger.error(f"❌ Processing failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "processing_time": time.time() - start_time,
            }


# =================== CLI INTERFACE ===================
def main():
    """Enhanced CLI with better error messages"""

    if len(sys.argv) < 3:
        print(
            """
🎯 Excel to SSMS - Fixed Complete System

Usage:
  python excel_to_ssms_fixed.py <excel_file> <table_name> [sheet_name]

Examples:
  python excel_to_ssms_fixed.py data.xlsx employees
  python excel_to_ssms_fixed.py sales.xlsx sales_data "Sheet1"
  python excel_to_ssms_fixed.py "C:/path/data.xlsx" customer_data

Features:
  ✅ Auto-detect SQL Server connection
  ✅ Connection pooling with monitoring
  ✅ Type inference and validation
  ✅ Progress tracking with pool status
  ✅ Comprehensive error handling
        """
        )
        sys.exit(1)

    excel_file = sys.argv[1]
    table_name = sys.argv[2]
    sheet_name = sys.argv[3] if len(sys.argv) > 3 else None

    # Load environment variables
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        pass

    # Validate file
    if not Path(excel_file).exists():
        print(f"❌ File not found: {excel_file}")
        sys.exit(1)

    print(f"🚀 Excel to SSMS Fixed: {Path(excel_file).name} → {table_name}")
    print("=" * 60)

    # Process
    processor = ExcelToSSMSProcessor(excel_file, table_name, sheet_name)
    results = processor.process(create_table=True)

    if results["success"]:
        print("\n🎉 Processing Complete!")
        print("=" * 60)
        print(f"📋 Total rows: {results['total_rows']:,}")
        print(f"✅ Inserted: {results['inserted_rows']:,}")
        print(f"⏱️  Time: {results['processing_time']:.2f} seconds")
        print(f"🚀 Speed: {results['speed_rows_per_sec']:.0f} rows/second")

        if "table_info" in results and "row_count" in results["table_info"]:
            print(f"🗄️  Table rows: {results['table_info']['row_count']:,}")

        if "pool_status" in results:
            pool = results["pool_status"]
            print(f"🔗 Pool status: {pool}")

        print(f"\n📊 Check results in SQL Server Management Studio:")
        print(f"   Server: {os.getenv('DB_HOST', '10.73.148.27')}")
        print(f"   Database: {os.getenv('DB_NAME', 'excel_to_db')}")
        print(f"   Table: {table_name}")
    else:
        print(f"\n❌ Processing failed: {results['error']}")
        print("\n💡 Troubleshooting:")
        print("  1. Check .env file configuration")
        print("  2. Verify SQL Server is running")
        print("  3. Check network connectivity")
        print("  4. Verify user permissions")
        sys.exit(1)


if __name__ == "__main__":
    main()  #!/usr/bin/env python3
"""
Excel to SSMS - Complete Fixed System
ระบบ import Excel เข้า SQL Server ที่แก้ไขปัญหาแล้ว
"""

import pandas as pd
import sqlalchemy as sa
from sqlalchemy import (
    create_engine,
    text,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
)
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError
import os
import sys
import time
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Iterator, List
from urllib.parse import quote_plus
from tqdm import tqdm
from datetime import datetime
import pyodbc
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from contextlib import contextmanager


# =================== CONFIGURATION ===================
class DatabaseConfig:
    """Database configuration with connection testing"""

    def __init__(self):
        # Load from environment
        self.DB_HOST = os.getenv("DB_HOST", "10.73.148.27")
        self.DB_NAME = os.getenv("DB_NAME", "excel_to_db")
        self.DB_USER = os.getenv("DB_USER", "TS00029")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", "Thammaphon@TS00029")

        # Pool settings - Conservative for stability
        self.POOL_SIZE = int(os.getenv("POOL_SIZE", "3"))
        self.MAX_OVERFLOW = int(os.getenv("MAX_OVERFLOW", "5"))
        self.POOL_TIMEOUT = 30
        self.POOL_RECYCLE = 3600

        # Processing settings
        self.BATCH_SIZE = int(os.getenv("BATCH_SIZE", "500"))
        self.MAX_WORKERS = int(os.getenv("MAX_WORKERS", "2"))
        self.CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "2000"))

        # Logging
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    def get_connection_variations(self) -> List[Dict[str, str]]:
        """Get multiple connection string variations to try"""
        password_encoded = quote_plus(self.DB_PASSWORD)

        return [
            {
                "name": "Default Instance",
                "url": f"mssql+pyodbc://{self.DB_USER}:{password_encoded}@{self.DB_HOST}/{self.DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes&Encrypt=no",
                "direct": f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.DB_HOST};DATABASE={self.DB_NAME};UID={self.DB_USER};PWD={self.DB_PASSWORD};TrustServerCertificate=yes;Encrypt=no;",
            },
            {
                "name": "Port 1433",
                "url": f"mssql+pyodbc://{self.DB_USER}:{password_encoded}@{self.DB_HOST}:1433/{self.DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes&Encrypt=no",
                "direct": f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.DB_HOST},1433;DATABASE={self.DB_NAME};UID={self.DB_USER};PWD={self.DB_PASSWORD};TrustServerCertificate=yes;Encrypt=no;",
            },
            {
                "name": "Named Instance MSSQL2S",
                "url": f"mssql+pyodbc://{self.DB_USER}:{password_encoded}@{self.DB_HOST}\\MSSQL2S/{self.DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes&Encrypt=no",
                "direct": f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.DB_HOST}\\MSSQL2S;DATABASE={self.DB_NAME};UID={self.DB_USER};PWD={self.DB_PASSWORD};TrustServerCertificate=yes;Encrypt=no;",
            },
        ]


# =================== ENHANCED DATABASE MANAGER ===================
class DatabaseManager:
    """Enhanced database manager with automatic connection testing"""

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.engine = None
        self.working_connection = None
        self._lock = threading.Lock()
        self.setup_logging()

    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=getattr(logging, self.config.LOG_LEVEL),
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler("logs/excel_to_ssms.log", encoding="utf-8"),
            ],
        )
        self.logger = logging.getLogger(__name__)

        # Create logs directory
        Path("logs").mkdir(exist_ok=True)

    def find_working_connection(self) -> bool:
        """Find a working connection from multiple variations"""
        variations = self.config.get_connection_variations()

        self.logger.info("🔍 Testing SQL Server connections...")

        for variation in variations:
            self.logger.info(f"  Testing: {variation['name']}")

            try:
                # Test direct pyodbc connection first
                conn = pyodbc.connect(variation["direct"], timeout=10)
                cursor = conn.cursor()
                cursor.execute("SELECT @@SERVERNAME, DB_NAME()")
                server, database = cursor.fetchone()
                conn.close()

                self.logger.info(f"    ✅ Direct connection OK: {server}/{database}")

                # Now test SQLAlchemy
                test_engine = create_engine(
                    variation["url"],
                    pool_size=1,
                    max_overflow=1,
                    pool_timeout=10,
                    echo=False,
                )

                with test_engine.connect() as test_conn:
                    result = test_conn.execute(text("SELECT 1"))
                    if result.fetchone()[0] == 1:
                        self.working_connection = variation
                        self.logger.info(f"    ✅ SQLAlchemy connection OK")
                        test_engine.dispose()
                        return True

                test_engine.dispose()

            except Exception as e:
                self.logger.info(f"    ❌ Failed: {str(e)[:100]}...")
                continue

        return False

    def create_engine(self) -> bool:
        """Create SQLAlchemy engine with working connection"""
        with self._lock:
            if self.engine:
                return True

            if not self.working_connection:
                if not self.find_working_connection():
                    self.logger.error("❌ No working connection found")
                    return False

            try:
                self.engine = create_engine(
                    self.working_connection["url"],
                    poolclass=QueuePool,
                    pool_size=self.config.POOL_SIZE,
                    max_overflow=self.config.MAX_OVERFLOW,
                    pool_timeout=self.config.POOL_TIMEOUT,
                    pool_recycle=self.config.POOL_RECYCLE,
                    pool_pre_ping=True,
                    echo=False,
                    connect_args={"timeout": 30, "autocommit": False},
                )

                # Verify engine works
                with self.engine.connect() as conn:
                    result = conn.execute(text("SELECT @@SERVERNAME, DB_NAME()"))
                    server, database = result.fetchone()
                    self.logger.info(f"✅ Engine created: {server}/{database}")

                return True

            except Exception as e:
                self.logger.error(f"❌ Engine creation failed: {e}")
                return False

    def test_connection(self) -> bool:
        """Test database connection"""
        if not self.engine and not self.create_engine():
            return False

        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                return result.fetchone()[0] == 1
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False

    @contextmanager
    def get_connection(self):
        """Get database connection with proper cleanup"""
        if not self.engine and not self.create_engine():
            raise ConnectionError("Cannot establish database connection")

        conn = self.engine.connect()
        try:
            yield conn
        finally:
            conn.close()

    def get_pool_status(self) -> Dict[str, Any]:
        """Get connection pool status"""
        if not self.engine:
            return {"status": "No engine"}

        try:
            pool = self.engine.pool
            return {
                "pool_size": pool.size(),
                "checked_in": pool.checkedin(),
                "checked_out": pool.checkedout(),
                "overflow": pool.overflow(),
                "total": pool.size() + pool.overflow(),
            }
        except Exception as e:
            return {"error": str(e)}


# =================== ENHANCED EXCEL READER ===================
class ExcelReader:
    """Enhanced Excel reader with better error handling"""

    def __init__(self, file_path: str, sheet_name: Optional[str] = None):
        self.file_path = Path(file_path)
        self.sheet_name = sheet_name
        self.total_rows = 0

    def validate_file(self) -> bool:
        """Validate Excel file"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        if self.file_path.suffix.lower() not in [".xlsx", ".xls"]:
            raise ValueError("File must be Excel format (.xlsx or .xls)")
        return True

    def get_file_info(self) -> Dict[str, Any]:
        """Get comprehensive file information"""
        self.validate_file()

        try:
            with pd.ExcelFile(self.file_path) as excel_file:
                sheets = excel_file.sheet_names
                target_sheet = self.sheet_name or sheets[0]

                # Get sample for columns
                df_sample = pd.read_excel(excel_file, sheet_name=target_sheet, nrows=5)

                # Count total rows efficiently
                df_count = pd.read_excel(
                    excel_file, sheet_name=target_sheet, usecols=[0]
                )
                self.total_rows = len(df_count)

                return {
                    "sheets": sheets,
                    "target_sheet": target_sheet,
                    "total_rows": self.total_rows,
                    "columns": df_sample.columns.tolist(),
                    "sample_data": df_sample.head(3).to_dict("records"),
                    "file_size_mb": self.file_path.stat().st_size / 1024 / 1024,
                }

        except Exception as e:
            raise Exception(f"Error reading Excel file: {e}")

    def read_chunks(self, chunk_size: int = 2000) -> Iterator[pd.DataFrame]:
        """Read Excel file in chunks with better memory management"""
        self.validate_file()

        try:
            # Read entire file first (for smaller files, this is more efficient)
            df_full = pd.read_excel(self.file_path, sheet_name=self.sheet_name or 0)

            # Process in chunks
            for start in range(0, len(df_full), chunk_size):
                end = min(start + chunk_size, len(df_full))
                chunk = df_full.iloc[start:end].copy()

                if not chunk.empty:
                    yield chunk

        except Exception as e:
            raise Exception(f"Error reading Excel chunks: {e}")


# =================== DATA VALIDATOR ===================
class DataValidator:
    """Enhanced data validator with type inference"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize DataFrame"""
        df_clean = df.copy()

        # Clean column names
        df_clean.columns = [self._clean_column_name(col) for col in df_clean.columns]

        # Remove completely empty rows
        df_clean = df_clean.dropna(how="all")

        # Clean string columns
        for col in df_clean.select_dtypes(include=["object"]).columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()
            df_clean[col] = df_clean[col].replace(["nan", "None", "null", ""], None)

        return df_clean

    def _clean_column_name(self, col_name: str) -> str:
        """Clean column name for database compatibility"""
        import re

        clean_name = re.sub(r"[^a-zA-Z0-9_\u0E00-\u0E7F]", "_", str(col_name))
        clean_name = re.sub(r"_+", "_", clean_name).strip("_")
        return clean_name

    def infer_data_types(self, df: pd.DataFrame) -> Dict[str, str]:
        """Infer data types from DataFrame"""
        type_mapping = {}

        for col in df.columns:
            col_lower = col.lower()

            # Check actual data
            sample_data = df[col].dropna().head(100)

            if len(sample_data) == 0:
                type_mapping[col] = "string"
                continue

            # Try to infer from column name patterns
            if any(
                pattern in col_lower for pattern in ["id", "number", "count", "จำนวน"]
            ):
                if pd.api.types.is_integer_dtype(sample_data):
                    type_mapping[col] = "integer"
                else:
                    type_mapping[col] = "string"
            elif any(
                pattern in col_lower
                for pattern in ["price", "amount", "salary", "ราคา", "เงิน"]
            ):
                try:
                    pd.to_numeric(sample_data)
                    type_mapping[col] = "float"
                except:
                    type_mapping[col] = "string"
            elif any(pattern in col_lower for pattern in ["date", "time", "วันที่"]):
                try:
                    pd.to_datetime(sample_data)
                    type_mapping[col] = "datetime"
                except:
                    type_mapping[col] = "string"
            else:
                type_mapping[col] = "string"

        return type_mapping

    def apply_data_types(
        self, df: pd.DataFrame, type_mapping: Dict[str, str]
    ) -> pd.DataFrame:
        """Apply data type conversions"""
        df_typed = df.copy()

        for col, target_type in type_mapping.items():
            if col not in df_typed.columns:
                continue

            try:
                if target_type == "integer":
                    df_typed[col] = (
                        pd.to_numeric(df_typed[col], errors="coerce")
                        .fillna(0)
                        .astype("Int64")
                    )
                elif target_type == "float":
                    df_typed[col] = pd.to_numeric(
                        df_typed[col], errors="coerce"
                    ).fillna(0.0)
                elif target_type == "datetime":
                    df_typed[col] = pd.to_datetime(df_typed[col], errors="coerce")
                elif target_type == "boolean":
                    df_typed[col] = (
                        df_typed[col]
                        .astype(str)
                        .str.lower()
                        .isin(["true", "1", "yes", "y"])
                    )
                # string is default, no conversion needed

            except Exception as e:
                self.logger.warning(f"Type conversion failed for {col}: {e}")

        return df_typed


# =================== DATABASE WRITER ===================
class DatabaseWriter:
    """Enhanced database writer with better error handling"""

    def __init__(self, table_name: str, db_manager: DatabaseManager):
        self.table_name = table_name
        self.db_manager = db_manager
        self.logger = logging.getLogger(__name__)

    def create_table_from_dataframe(
        self, df_sample: pd.DataFrame, type_mapping: Dict[str, str] = None
    ):
        """Create table with proper SQL Server syntax"""
        try:
            # Build column definitions
            columns_sql = ["id INT IDENTITY(1,1) PRIMARY KEY"]

            for col_name, dtype in df_sample.dtypes.items():
                if type_mapping and col_name in type_mapping:
                    sql_type = self._get_sql_type(type_mapping[col_name])
                else:
                    sql_type = self._infer_sql_type(dtype)

                # Escape column names properly
                columns_sql.append(f"[{col_name}] {sql_type}")

            # SQL statements
            drop_sql = f"IF OBJECT_ID('{self.table_name}', 'U') IS NOT NULL DROP TABLE [{self.table_name}]"
            create_sql = f"CREATE TABLE [{self.table_name}] ({', '.join(columns_sql)})"

            # Execute with transaction
            with self.db_manager.get_connection() as conn:
                with conn.begin():
                    conn.execute(text(drop_sql))
                    conn.execute(text(create_sql))

            self.logger.info(f"✅ Table '{self.table_name}' created successfully")

        except Exception as e:
            self.logger.error(f"❌ Table creation failed: {e}")
            raise

    def _get_sql_type(self, type_name: str) -> str:
        """Convert type name to SQL Server type"""
        type_map = {
            "string": "NVARCHAR(255)",
            "text": "NVARCHAR(MAX)",
            "integer": "INT",
            "float": "FLOAT",
            "boolean": "BIT",
            "datetime": "DATETIME2",
        }
        return type_map.get(type_name, "NVARCHAR(255)")

    def _infer_sql_type(self, pandas_dtype) -> str:
        """Infer SQL type from pandas dtype"""
        if pd.api.types.is_integer_dtype(pandas_dtype):
            return "INT"
        elif pd.api.types.is_float_dtype(pandas_dtype):
            return "FLOAT"
        elif pd.api.types.is_bool_dtype(pandas_dtype):
            return "BIT"
        elif pd.api.types.is_datetime64_any_dtype(pandas_dtype):
            return "DATETIME2"
        else:
            return "NVARCHAR(255)"

    def bulk_insert(self, df: pd.DataFrame) -> int:
        """Optimized bulk insert with proper error handling"""
        try:
            df_clean = df.copy()

            # Handle datetime columns
            for col in df_clean.columns:
                if pd.api.types.is_datetime64_any_dtype(df_clean[col]):
                    df_clean[col] = df_clean[col].dt.strftime("%Y-%m-%d %H:%M:%S")
                    df_clean[col] = df_clean[col].replace("NaT", None)

            # Replace NaN with None
            df_clean = df_clean.where(pd.notnull(df_clean), None)

            # Use to_sql with transaction
            with self.db_manager.get_connection() as conn:
                with conn.begin():
                    df_clean.to_sql(
                        name=self.table_name,
                        con=conn,
                        if_exists="append",
                        index=False,
                        method="multi",
                        chunksize=self.db_manager.config.BATCH_SIZE,
                    )

            rows_inserted = len(df_clean)
            self.logger.info(f"✅ Inserted {rows_inserted:,} rows")
            return rows_inserted

        except Exception as e:
            self.logger.error(f"❌ Bulk insert failed: {e}")
            raise

    def get_table_info(self) -> Dict[str, Any]:
        """Get table information"""
        try:
            with self.db_manager.get_connection() as conn:
                # Get row count
                result = conn.execute(text(f"SELECT COUNT(*) FROM [{self.table_name}]"))
                row_count = result.fetchone()[0]

                # Get column info
                columns_sql = f"""
                    SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = '{self.table_name}'
                    ORDER BY ORDINAL_POSITION
                """
                result = conn.execute(text(columns_sql))
                columns = [(row[0], row[1], row[2]) for row in result.fetchall()]

                return {
                    "table_name": self.table_name,
                    "row_count": row_count,
                    "columns": columns,
                }

        except Exception as e:
            self.logger.error(f"❌ Get table info failed: {e}")
            return {"error": str(e)}


# =================== MAIN PROCESSOR ===================
class ExcelToSSMSProcessor:
    """Main processor with enhanced error handling and monitoring"""

    def __init__(self, excel_file: str, table_name: str, sheet_name: str = None):
        self.excel_file = excel_file
        self.table_name = table_name
        self.sheet_name = sheet_name

        # Initialize components
        self.config = DatabaseConfig()
        self.db_manager = DatabaseManager(self.config)
        self.reader = ExcelReader(excel_file, sheet_name)
        self.validator = DataValidator()
        self.writer = DatabaseWriter(table_name, self.db_manager)

        self.logger = logging.getLogger(__name__)

    def process(self, create_table: bool = True) -> Dict[str, Any]:
        """Main processing method with comprehensive error handling"""
        start_time = time.time()

        try:
            # 1. Test database connection
            self.logger.info("🔍 Testing database connection...")
            if not self.db_manager.test_connection():
                raise Exception("Cannot connect to SQL Server")

            # 2. Analyze Excel file
            self.logger.info("📊 Analyzing Excel file...")
            file_info = self.reader.get_file_info()
            self.logger.info(
                f"File: {file_info['total_rows']:,} rows, {file_info['file_size_mb']:.1f} MB"
            )

            # 3. Process data
            total_inserted = 0
            table_created = False

            with tqdm(
                total=file_info["total_rows"], desc="Processing", unit="rows"
            ) as pbar:
                for chunk_num, chunk in enumerate(
                    self.reader.read_chunks(self.config.CHUNK_SIZE)
                ):
                    # Clean and validate
                    df_clean = self.validator.clean_dataframe(chunk)

                    # Auto-detect types on first chunk
                    if chunk_num == 0:
                        type_mapping = self.validator.infer_data_types(df_clean)
                        self.logger.info(f"Detected types: {type_mapping}")

                    df_typed = self.validator.apply_data_types(df_clean, type_mapping)

                    # Create table on first chunk
                    if create_table and not table_created:
                        self.writer.create_table_from_dataframe(df_typed, type_mapping)
                        table_created = True

                    # Insert data
                    rows_inserted = self.writer.bulk_insert(df_typed)
                    total_inserted += rows_inserted

                    # Update progress
                    pbar.update(len(chunk))
                    pbar.set_postfix(
                        {
                            "Inserted": f"{total_inserted:,}",
                            "Pool": str(
                                self.db_manager.get_pool_status().get("checked_out", 0)
                            ),
                        }
                    )

            # 4. Final results
            processing_time = time.time() - start_time
            table_info = self.writer.get_table_info()

            results = {
                "success": True,
                "total_rows": file_info["total_rows"],
                "inserted_rows": total_inserted,
                "processing_time": processing_time,
                "speed_rows_per_sec": (
                    total_inserted / processing_time if processing_time > 0 else 0
                ),
                "table_info": table_info,
                "pool_status": self.db_manager.get_pool_status(),
            }

            self.logger.info(
                f"🎉 SUCCESS: {total_inserted:,} rows in {processing_time:.2f}s"
            )
            return results

        except Exception as e:
            self.logger.error(f"❌ Processing failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "processing_time": time.time() - start_time,
            }


# =================== CLI INTERFACE ===================
def main():
    """Enhanced CLI with better error messages"""

    if len(sys.argv) < 3:
        print(
            """
🎯 Excel to SSMS - Fixed Complete System

Usage:
  python excel_to_ssms_fixed.py <excel_file> <table_name> [sheet_name]

Examples:
  python excel_to_ssms_fixed.py data.xlsx employees
  python excel_to_ssms_fixed.py sales.xlsx sales_data "Sheet1"
  python excel_to_ssms_fixed.py "C:/path/data.xlsx" customer_data

Features:
  ✅ Auto-detect SQL Server connection
  ✅ Connection pooling with monitoring
  ✅ Type inference and validation
  ✅ Progress tracking with pool status
  ✅ Comprehensive error handling
        """
        )
        sys.exit(1)

    excel_file = sys.argv[1]
    table_name = sys.argv[2]
    sheet_name = sys.argv[3] if len(sys.argv) > 3 else None

    # Load environment variables
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        pass

    # Validate file
    if not Path(excel_file).exists():
        print(f"❌ File not found: {excel_file}")
        sys.exit(1)

    print(f"🚀 Excel to SSMS Fixed: {Path(excel_file).name} → {table_name}")
    print("=" * 60)

    # Process
    processor = ExcelToSSMSProcessor(excel_file, table_name, sheet_name)
    results = processor.process(create_table=True)

    if results["success"]:
        print("\n🎉 Processing Complete!")
        print("=" * 60)
        print(f"📋 Total rows: {results['total_rows']:,}")
        print(f"✅ Inserted: {results['inserted_rows']:,}")
        print(f"⏱️  Time: {results['processing_time']:.2f} seconds")
        print(f"🚀 Speed: {results['speed_rows_per_sec']:.0f} rows/second")

        if "table_info" in results and "row_count" in results["table_info"]:
            print(f"🗄️  Table rows: {results['table_info']['row_count']:,}")

        if "pool_status" in results:
            pool = results["pool_status"]
            print(f"🔗 Pool status: {pool}")

        print(f"\n📊 Check results in SQL Server Management Studio:")
        print(f"   Server: {os.getenv('DB_HOST', '10.73.148.27')}")
        print(f"   Database: {os.getenv('DB_NAME', 'excel_to_db')}")
        print(f"   Table: {table_name}")
    else:
        print(f"\n❌ Processing failed: {results['error']}")
        print("\n💡 Troubleshooting:")
        print("  1. Check .env file configuration")
        print("  2. Verify SQL Server is running")
        print("  3. Check network connectivity")
        print("  4. Verify user permissions")
        sys.exit(1)


if __name__ == "__main__":
    main()
