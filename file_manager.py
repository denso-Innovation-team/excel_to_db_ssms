import pandas as pd
import sys
import time
from pathlib import Path
import logging
from datetime import datetime


def setup_logging():
    """Setup Windows-compatible logging configuration"""
    import logging
    import sys

    # Configure logger to handle Unicode properly on Windows
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            # Console handler with UTF-8 encoding
            logging.StreamHandler(sys.stdout),
            # File handler with UTF-8 encoding
            logging.FileHandler("logs/file_manager.log", encoding="utf-8"),
        ],
    )

    # Get logger
    logger = logging.getLogger(__name__)

    # Override logging methods to remove Unicode emojis on Windows
    if sys.platform == "win32":
        original_info = logger.info
        original_error = logger.error
        original_warning = logger.warning

        def safe_info(msg, *args, **kwargs):
            clean_msg = str(msg).encode("ascii", errors="ignore").decode("ascii")
            return original_info(clean_msg, *args, **kwargs)

        def safe_error(msg, *args, **kwargs):
            clean_msg = str(msg).encode("ascii", errors="ignore").decode("ascii")
            return original_error(clean_msg, *args, **kwargs)

        def safe_warning(msg, *args, **kwargs):
            clean_msg = str(msg).encode("ascii", errors="ignore").decode("ascii")
            return original_warning(clean_msg, *args, **kwargs)

        logger.info = safe_info
        logger.error = safe_error
        logger.warning = safe_warning

    return logger


def create_test_file(size="small"):
    """สร้างไฟล์ Excel สำหรับทดสอบ"""

    size_config = {
        "small": (100, "employees_100.xlsx"),
        "medium": (5000, "employees_5000.xlsx"),
        "large": (10000, "employees_10000.xlsx"),
        "xlarge": (50000, "employees_50000.xlsx"),
    }

    rows, filename = size_config.get(size, (1000, "employees_test.xlsx"))

    print(f"📊 สร้างข้อมูลทดสอบ: {rows:,} rows")
    start_time = time.time()

    # สร้างข้อมูลตัวอย่าง
    import random
    from datetime import datetime, timedelta

    data = []
    departments = [
        "Engineering",
        "Sales",
        "Marketing",
        "HR",
        "Finance",
        "Operations",
        "Support",
    ]
    positions = ["Junior", "Senior", "Lead", "Manager", "Director", "VP", "SVP"]
    locations = [
        "Bangkok",
        "Phuket",
        "Chiang Mai",
        "Pattaya",
        "Khon Kaen",
        "Nakhon Ratchasima",
    ]
    skills = [
        "Python",
        "JavaScript",
        "SQL",
        "Excel",
        "PowerBI",
        "Tableau",
        "AWS",
        "Azure",
    ]

    for i in range(rows):
        data.append(
            {
                "employee_id": f"EMP{i+1:06d}",
                "first_name": f"Name{i+1}",
                "last_name": f"Surname{i+1}",
                "email": f"employee{i+1}@company.com",
                "department": random.choice(departments),
                "position": random.choice(positions),
                "salary": random.randint(30000, 200000),
                "hire_date": datetime.now() - timedelta(days=random.randint(0, 3650)),
                "is_active": random.choice([True, False]),
                "age": random.randint(22, 65),
                "location": random.choice(locations),
                "bonus": random.randint(0, 100000),
                "skills": ",".join(random.sample(skills, random.randint(1, 3))),
                "performance_score": round(random.uniform(1.0, 5.0), 2),
            }
        )

    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

    creation_time = time.time() - start_time
    print(f"✅ สร้างไฟล์: {filename} ({creation_time:.2f}s)")

    return filename


def ensure_directories():
    """สร้าง directories ที่จำเป็น"""
    dirs = ["logs", "data", "tests", "src/config", "src/processors", "src/utils"]
    for dir_name in dirs:
        Path(dir_name).mkdir(parents=True, exist_ok=True)


def setup_supabase_config():
    """Setup Supabase configuration files"""

    # Create settings.py
    settings_code = '''import os

class Settings:
    """Supabase PostgreSQL Configuration"""
    
    def __init__(self):
        # Supabase PostgreSQL
        self.DB_HOST = "aws-0-ap-southeast-1.pooler.supabase.com"
        self.DB_PORT = 6543
        self.DB_NAME = "postgres"
        self.DB_USER = "postgres.ydmmxivfmfgbbphmitgy"
        self.DB_PASSWORD = "jsCvOpw2RbFdpf5L"
        self.DB_TYPE = "postgresql"
        
        # Processing Configuration
        self.BATCH_SIZE = 2000
        self.MAX_WORKERS = 6
        self.CHUNK_SIZE = 10000
        
        # Logging
        self.LOG_LEVEL = "INFO"
        self.LOG_FILE = "logs/excel_to_db.log"
        
    def get_database_url(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?sslmode=require"

settings = Settings()
'''

    # Create database.py
    database_code = """from sqlalchemy import create_engine, text
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
"""

    # Write files
    with open("src/config/settings.py", "w", encoding="utf-8") as f:
        f.write(settings_code)

    with open("src/config/database.py", "w", encoding="utf-8") as f:
        f.write(database_code)

    # Create __init__.py files
    for path in [
        "src/__init__.py",
        "src/config/__init__.py",
        "src/processors/__init__.py",
        "src/utils/__init__.py",
    ]:
        Path(path).touch()

    print("✅ Supabase configuration files created")


def test_system_components():
    """ทดสอบส่วนประกอบของระบบ"""

    print("\n🧪 ทดสอบระบบ...")
    test_results = {
        "imports": False,
        "database": False,
        "excel_processing": False,
        "data_validation": False,
        "database_operations": False,
    }

    try:
        # Test imports
        print("  📦 Testing imports...")
        from src.config.settings import settings
        from src.config.database import db_manager
        from src.processors.excel_reader import ExcelReader
        from src.processors.data_validator import DataValidator
        from src.processors.database_writer import DatabaseWriter

        test_results["imports"] = True
        print("    ✅ All imports successful")

        # Test database connection
        print("  🔗 Testing Supabase connection...")
        if db_manager.test_connection():
            test_results["database"] = True
            print("    ✅ Supabase connection successful")
        else:
            print("    ❌ Supabase connection failed")
            return test_results

        return test_results

    except Exception as e:
        print(f"    ❌ System test failed: {e}")
        return test_results


def run_complete_pipeline(filename, table_name="test_employees"):
    """รันกระบวนการสมบูรณ์พร้อมการจับเวลา"""

    logger = setup_logging()

    # Performance metrics
    metrics = {
        "start_time": time.time(),
        "file_size_mb": Path(filename).stat().st_size / (1024 * 1024),
        "total_rows": 0,
        "processed_rows": 0,
        "inserted_rows": 0,
        "errors": 0,
        "stages": {},
    }

    try:
        print(f"\n🚀 เริ่มกระบวนการ: {filename} → {table_name}")
        print("=" * 60)

        # Stage 1: Excel Reading
        stage_start = time.time()
        print("📖 Stage 1: Reading Excel file...")

        from src.processors.excel_reader import ExcelReader

        reader = ExcelReader(filename)
        info = reader.get_sheet_info()
        metrics["total_rows"] = info["total_rows"]

        metrics["stages"]["excel_reading"] = time.time() - stage_start
        print(
            f"    ✅ Read: {info['total_rows']:,} rows, {len(info['columns'])} columns ({metrics['stages']['excel_reading']:.2f}s)"
        )

        # Stage 2: Data Validation Setup
        stage_start = time.time()
        print("🧹 Stage 2: Setting up data validation...")

        from src.processors.data_validator import DataValidator

        validator = DataValidator()

        # Type mapping for employee data
        type_mapping = {
            "employee_id": "string",
            "first_name": "string",
            "last_name": "string",
            "email": "string",
            "department": "string",
            "position": "string",
            "salary": "integer",
            "hire_date": "datetime",
            "is_active": "boolean",
            "age": "integer",
            "location": "string",
            "bonus": "integer",
            "skills": "string",
            "performance_score": "float",
        }

        metrics["stages"]["validation_setup"] = time.time() - stage_start
        print(
            f"    ✅ Validation setup complete ({metrics['stages']['validation_setup']:.2f}s)"
        )

        # Stage 3: Database Setup
        stage_start = time.time()
        print("🏗️ Stage 3: Setting up database table...")

        from src.processors.database_writer import DatabaseWriter

        db_writer = DatabaseWriter(table_name)

        # Create table from first chunk
        first_chunk = next(reader.read_chunks(chunk_size=100))
        clean_sample = validator.clean_dataframe(first_chunk)
        typed_sample = validator.validate_data_types(clean_sample, type_mapping)

        db_writer.create_table_from_dataframe(typed_sample, type_mapping=type_mapping)

        metrics["stages"]["database_setup"] = time.time() - stage_start
        print(
            f"    ✅ Table '{table_name}' created ({metrics['stages']['database_setup']:.2f}s)"
        )

        # Import settings for chunk processing
        from src.config.settings import settings

        # Stage 4: Data Processing
        stage_start = time.time()
        print("⚡ Stage 4: Processing and inserting data...")

        # Process in chunks
        chunk_count = 0
        batch_chunks = []

        for chunk in reader.read_chunks(chunk_size=settings.CHUNK_SIZE):
            chunk_count += 1

            # Clean and validate
            clean_chunk = validator.clean_dataframe(chunk)
            typed_chunk = validator.validate_data_types(clean_chunk, type_mapping)

            batch_chunks.append(typed_chunk)
            metrics["processed_rows"] += len(typed_chunk)

            # Process in batches
            if len(batch_chunks) >= settings.MAX_WORKERS:
                inserted = db_writer.parallel_insert(batch_chunks)
                metrics["inserted_rows"] += inserted
                batch_chunks = []

                print(
                    f"    📊 Processed chunk {chunk_count}: {metrics['processed_rows']:,}/{metrics['total_rows']:,} rows"
                )

        # Process remaining chunks
        if batch_chunks:
            inserted = db_writer.parallel_insert(batch_chunks)
            metrics["inserted_rows"] += inserted

        metrics["stages"]["data_processing"] = time.time() - stage_start
        print(
            f"    ✅ Data processing complete ({metrics['stages']['data_processing']:.2f}s)"
        )

        # Final metrics calculation
        metrics["end_time"] = time.time()
        metrics["total_time"] = metrics["end_time"] - metrics["start_time"]
        metrics["rows_per_second"] = (
            metrics["inserted_rows"] / metrics["total_time"]
            if metrics["total_time"] > 0
            else 0
        )
        metrics["mb_per_second"] = (
            metrics["file_size_mb"] / metrics["total_time"]
            if metrics["total_time"] > 0
            else 0
        )

        # Verification
        print("✅ Stage 5: Verification...")
        table_info = db_writer.get_table_info()

        print("\n🎉 กระบวนการเสร็จสิ้น!")
        print("=" * 60)
        print(f"📊 Performance Summary:")
        print(f"    File: {filename} ({metrics['file_size_mb']:.1f} MB)")
        print(f"    Total rows: {metrics['total_rows']:,}")
        print(f"    Processed: {metrics['processed_rows']:,}")
        print(f"    Inserted: {metrics['inserted_rows']:,}")
        print(
            f"    Success rate: {(metrics['inserted_rows']/metrics['total_rows']*100):.1f}%"
        )
        print(f"    Total time: {metrics['total_time']:.2f} seconds")
        print(f"    Speed: {metrics['rows_per_second']:.1f} rows/sec")
        print(f"    Throughput: {metrics['mb_per_second']:.1f} MB/sec")

        print(f"\n⏱️ Stage Breakdown:")
        for stage, duration in metrics["stages"].items():
            percentage = (duration / metrics["total_time"]) * 100
            print(f"    {stage}: {duration:.2f}s ({percentage:.1f}%)")

        print(
            f"\n🗄️ Database: Table '{table_name}' contains {table_info.get('row_count', 0):,} rows"
        )

        return True, metrics

    except Exception as e:
        metrics["end_time"] = time.time()
        metrics["total_time"] = metrics["end_time"] - metrics["start_time"]

        print(f"\n❌ กระบวนการล้มเหลว: {e}")
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        return False, metrics


def benchmark_performance():
    """ทดสอบ performance หลายขนาด"""

    print("\n⚡ Performance Benchmark")
    print("=" * 50)

    sizes = ["small", "medium", "large"]
    results = []

    for size in sizes:
        print(f"\n📊 Benchmarking {size}...")

        # Create test file
        filename = create_test_file(size)
        table_name = f"benchmark_{size}_{int(time.time())}"

        # Run pipeline
        success, metrics = run_complete_pipeline(filename, table_name)

        if success:
            results.append(
                {
                    "size": size,
                    "rows": metrics["total_rows"],
                    "time": metrics["total_time"],
                    "speed": metrics["rows_per_second"],
                    "file_size": metrics["file_size_mb"],
                }
            )

        # Cleanup
        Path(filename).unlink(missing_ok=True)

    # Summary
    print("\n📈 Benchmark Results:")
    print("-" * 70)
    print(
        f"{'Size':<10} {'Rows':<10} {'Time (s)':<10} {'Speed (r/s)':<12} {'File (MB)':<10}"
    )
    print("-" * 70)

    for result in results:
        print(
            f"{result['size']:<10} {result['rows']:<10,} {result['time']:<10.2f} {result['speed']:<12.1f} {result['file_size']:<10.1f}"
        )

    return results


def main():
    """Main function with enhanced options"""

    if len(sys.argv) < 2:
        print("🔧 Excel to Supabase - Advanced File Manager")
        print("=" * 50)
        print("Usage:")
        print("  python file_manager.py small      # 100 rows")
        print("  python file_manager.py medium     # 5,000 rows")
        print("  python file_manager.py large      # 10,000 rows")
        print("  python file_manager.py xlarge     # 50,000 rows")
        print("  python file_manager.py benchmark  # Performance test")
        print("  python file_manager.py custom <rows> <table_name>")
        return

    mode = sys.argv[1]

    # Setup
    print("🔧 Excel to Supabase - Advanced Processing")
    print("=" * 50)

    ensure_directories()
    setup_supabase_config()

    # Test system
    test_results = test_system_components()
    if not test_results["database"]:
        print("\n❌ System not ready. Please check configuration.")
        return

    if mode == "benchmark":
        benchmark_performance()

    elif mode == "custom" and len(sys.argv) >= 3:
        rows = int(sys.argv[2])
        table_name = (
            sys.argv[3] if len(sys.argv) > 3 else f"custom_test_{int(time.time())}"
        )

        print(f"🎯 Custom processing: {rows:,} rows → {table_name}")

        # Create custom file
        import random
        from datetime import datetime, timedelta

        data = []
        for i in range(rows):
            data.append(
                {
                    "id": i + 1,
                    "name": f"Item_{i+1}",
                    "value": random.randint(1, 1000),
                    "created_at": datetime.now()
                    - timedelta(days=random.randint(0, 365)),
                }
            )

        df = pd.DataFrame(data)
        filename = f"custom_{rows}.xlsx"
        df.to_excel(filename, index=False)

        success, metrics = run_complete_pipeline(filename, table_name)
        Path(filename).unlink(missing_ok=True)

    elif mode in ["small", "medium", "large", "xlarge"]:
        filename = create_test_file(mode)
        table_name = f"employees_{mode}_{int(time.time())}"

        success, metrics = run_complete_pipeline(filename, table_name)
        Path(filename).unlink(missing_ok=True)

        if success:
            print(f"\n🎯 ระบบพร้อมใช้งาน! Next: python file_manager.py benchmark")

    else:
        print(
            "❌ Invalid option. Use: small, medium, large, xlarge, benchmark, or custom"
        )


if __name__ == "__main__":
    main()
