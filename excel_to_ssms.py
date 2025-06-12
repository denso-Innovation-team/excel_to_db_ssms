#!/usr/bin/env python3
"""
Excel to SSMS - Fixed Complete System
ระบบ import Excel เข้า SQL Server ที่แก้ไขแล้ว
"""

import pandas as pd
import sqlalchemy as sa
from sqlalchemy import (
    create_engine,
    text,
)
import os
import sys
import time
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Iterator
from urllib.parse import quote_plus
from tqdm import tqdm
from datetime import datetime


# =================== CONFIGURATION ===================
class Config:
    """การตั้งค่าระบบ"""

    def __init__(self):
        self.DB_HOST = os.getenv("DB_HOST", "10.73.148.27")
        self.DB_PORT = os.getenv("DB_PORT", "1433")
        self.DB_NAME = os.getenv("DB_NAME", "excel_to_db")
        self.DB_USER = os.getenv("DB_USER", "TS00029")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", "Thammaphon@TS00029")
        self.POOL_SIZE = int(os.getenv("POOL_SIZE", "5"))
        self.MAX_OVERFLOW = int(os.getenv("MAX_OVERFLOW", "10"))
        self.BATCH_SIZE = int(os.getenv("BATCH_SIZE", "2000"))
        self.MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))
        self.CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "5000"))
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    def get_connection_url(self) -> str:
        """สร้าง SQLAlchemy connection URL"""
        password_encoded = quote_plus(self.DB_PASSWORD)
        return (
            f"mssql+pyodbc://{self.DB_USER}:{password_encoded}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?"
            f"driver=ODBC+Driver+17+for+SQL+Server&"
            f"TrustServerCertificate=yes&Encrypt=no&timeout=30"
        )

    def get_direct_connection_string(self) -> str:
        """สร้าง pyodbc connection string"""
        return (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={self.DB_HOST},{self.DB_PORT};"
            f"DATABASE={self.DB_NAME};"
            f"UID={self.DB_USER};"
            f"PWD={self.DB_PASSWORD};"
            f"TrustServerCertificate=yes;Encrypt=no;Timeout=30;"
        )


# =================== LOGGER SETUP ===================
def setup_logger() -> logging.Logger:
    """ตั้งค่า logging"""
    logger = logging.getLogger("excel_to_ssms")
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter("%(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    try:
        Path("logs").mkdir(exist_ok=True)
        file_handler = logging.FileHandler("logs/excel_to_ssms.log", encoding="utf-8")
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except Exception:
        pass

    return logger


# =================== DATABASE MANAGER ===================
class DatabaseManager:
    """จัดการการเชื่อมต่อฐานข้อมูล"""

    def __init__(self, config: Config):
        self.config = config
        self.engine = None
        self.logger = setup_logger()

    def create_engine(self) -> bool:
        """สร้าง SQLAlchemy engine"""
        try:
            connection_url = self.config.get_connection_url()
            self.engine = create_engine(
                connection_url,
                pool_size=self.config.POOL_SIZE,
                max_overflow=self.config.MAX_OVERFLOW,
                pool_timeout=30,
                pool_recycle=3600,
                pool_pre_ping=True,
                echo=False,
            )

            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT @@SERVERNAME, DB_NAME()"))
                server, database = result.fetchone()
                self.logger.info(f"✅ Connected to: {server}/{database}")

            return True

        except Exception as e:
            self.logger.error(f"❌ Database connection failed: {e}")
            return False

    def test_connection(self) -> bool:
        """ทดสอบการเชื่อมต่อ"""
        if not self.engine and not self.create_engine():
            return False

        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                return result.fetchone()[0] == 1
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False

    def execute_sql(self, sql: str, params: dict = None) -> Any:
        """Execute SQL command"""
        try:
            with self.engine.connect() as conn:
                result = (
                    conn.execute(text(sql), params)
                    if params
                    else conn.execute(text(sql))
                )
                conn.commit()
                return result
        except Exception as e:
            self.logger.error(f"SQL execution failed: {e}")
            raise


# =================== EXCEL READER ===================
class ExcelReader:
    """อ่านและประมวลผลไฟล์ Excel"""

    def __init__(self, file_path: str, sheet_name: Optional[str] = None):
        self.file_path = Path(file_path)
        self.sheet_name = sheet_name
        self.logger = setup_logger()

    def validate_file(self) -> bool:
        """ตรวจสอบไฟล์ Excel"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

        if self.file_path.suffix.lower() not in [".xlsx", ".xls"]:
            raise ValueError("File must be Excel format (.xlsx or .xls)")

        return True

    def get_file_info(self) -> Dict[str, Any]:
        """ดึงข้อมูลไฟล์ Excel"""
        self.validate_file()

        try:
            with pd.ExcelFile(self.file_path) as excel_file:
                sheets = excel_file.sheet_names
                target_sheet = self.sheet_name or sheets[0]
                df_sample = pd.read_excel(excel_file, sheet_name=target_sheet, nrows=5)
                df_count = pd.read_excel(
                    excel_file, sheet_name=target_sheet, usecols=[0]
                )
                total_rows = len(df_count)

                return {
                    "sheets": sheets,
                    "target_sheet": target_sheet,
                    "total_rows": total_rows,
                    "columns": df_sample.columns.tolist(),
                    "file_size_mb": self.file_path.stat().st_size / 1024 / 1024,
                }

        except Exception as e:
            self.logger.error(f"Error reading Excel file: {e}")
            raise

    def read_chunks(self, chunk_size: int = 5000) -> Iterator[pd.DataFrame]:
        """อ่านไฟล์เป็น chunks"""
        self.validate_file()

        try:
            target_sheet = self.sheet_name or 0
            df_full = pd.read_excel(self.file_path, sheet_name=target_sheet)
            total_rows = len(df_full)
            for start_idx in range(0, total_rows, chunk_size):
                end_idx = min(start_idx + chunk_size, total_rows)
                chunk = df_full.iloc[start_idx:end_idx].copy()

                if not chunk.empty:
                    yield chunk

        except Exception as e:
            self.logger.error(f"Error reading Excel chunks: {e}")
            raise


# =================== DATA VALIDATOR ===================
class DataValidator:
    """ตรวจสอบและทำความสะอาดข้อมูล"""

    def __init__(self):
        self.logger = setup_logger()

    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """ทำความสะอาด DataFrame"""
        df_clean = df.copy()
        df_clean.columns = [self._clean_column_name(col) for col in df_clean.columns]
        df_clean = df_clean.dropna(how="all")

        for col in df_clean.select_dtypes(include=["object"]).columns:
            df_clean[col] = (
                df_clean[col].astype(str).str.strip().replace(["nan", "None", ""], None)
            )

        return df_clean

    def _clean_column_name(self, col_name: str) -> str:
        """ทำความสะอาดชื่อ column"""
        import re

        clean_name = re.sub(r"[^a-zA-Z0-9_]", "_", str(col_name))
        clean_name = re.sub(r"_+", "_", clean_name).strip("_")
        return clean_name.lower()

    def validate_data_types(
        self, df: pd.DataFrame, type_mapping: Dict[str, str]
    ) -> pd.DataFrame:
        """แปลงประเภทข้อมูล"""
        df_typed = df.copy()

        for column, target_type in type_mapping.items():
            if column not in df_typed.columns:
                continue

            try:
                if target_type == "integer":
                    df_typed[column] = (
                        pd.to_numeric(df_typed[column], errors="coerce")
                        .fillna(0)
                        .astype("Int64")
                    )
                elif target_type == "float":
                    df_typed[column] = pd.to_numeric(
                        df_typed[column], errors="coerce"
                    ).fillna(0.0)
                elif target_type == "datetime":
                    df_typed[column] = pd.to_datetime(df_typed[column], errors="coerce")
                elif target_type == "boolean":
                    df_typed[column] = (
                        df_typed[column]
                        .astype(str)
                        .str.lower()
                        .isin(["true", "1", "yes", "y"])
                    )
            except Exception as e:
                self.logger.warning(f"Type conversion failed for {column}: {e}")

        return df_typed


# =================== DATABASE WRITER ===================
class DatabaseWriter:
    """เขียนข้อมูลลงฐานข้อมูล"""

    def __init__(self, table_name: str, db_manager: DatabaseManager):
        self.table_name = table_name
        self.db_manager = db_manager
        self.logger = setup_logger()

    def create_table_from_dataframe(
        self, df_sample: pd.DataFrame, type_mapping: Dict[str, str] = None
    ):
        """สร้างตารางจาก DataFrame"""
        try:
            columns_sql = ["id INT IDENTITY(1,1) PRIMARY KEY"]

            for col_name, dtype in df_sample.dtypes.items():
                if type_mapping and col_name in type_mapping:
                    sql_type = self._get_sql_type(type_mapping[col_name])
                else:
                    sql_type = self._infer_sql_type(dtype)

                columns_sql.append(f"[{col_name}] {sql_type}")

            drop_sql = f"IF OBJECT_ID('{self.table_name}', 'U') IS NOT NULL DROP TABLE [{self.table_name}]"
            create_sql = f"CREATE TABLE [{self.table_name}] ({', '.join(columns_sql)})"

            self.db_manager.execute_sql(drop_sql)
            self.db_manager.execute_sql(create_sql)

            self.logger.info(f"✅ Table '{self.table_name}' created successfully")

        except Exception as e:
            self.logger.error(f"❌ Table creation failed: {e}")
            raise

    def _get_sql_type(self, type_name: str) -> str:
        """แปลง type เป็น SQL Server type"""
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
        """อนุมาน SQL type จาก pandas dtype"""
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
        """แทรกข้อมูลแบบ bulk"""
        try:
            df_clean = df.copy()

            for col in df_clean.columns:
                if pd.api.types.is_datetime64_any_dtype(df_clean[col]):
                    df_clean[col] = (
                        df_clean[col]
                        .dt.strftime("%Y-%m-%d %H:%M:%S")
                        .replace("NaT", None)
                    )

            df_clean = df_clean.where(pd.notnull(df_clean), None)

            with self.db_manager.engine.begin() as conn:
                df_clean.to_sql(
                    name=self.table_name,
                    con=conn,
                    if_exists="append",
                    index=False,
                    method="multi",
                    chunksize=1000,
                )

            rows_inserted = len(df_clean)
            self.logger.info(f"✅ Inserted {rows_inserted:,} rows")
            return rows_inserted

        except Exception as e:
            self.logger.error(f"❌ Bulk insert failed: {e}")
            raise

    def get_table_info(self) -> Dict[str, Any]:
        """ดึงข้อมูลตาราง"""
        try:
            result = self.db_manager.execute_sql(
                f"SELECT COUNT(*) FROM [{self.table_name}]"
            )
            row_count = result.fetchone()[0]

            columns_sql = f"""
                SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = '{self.table_name}'
                ORDER BY ORDINAL_POSITION
            """
            result = self.db_manager.execute_sql(columns_sql)
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
    """ตัวประมวลผลหลัก"""

    def __init__(self, excel_file: str, table_name: str, sheet_name: str = None):
        self.excel_file = excel_file
        self.table_name = table_name
        self.sheet_name = sheet_name
        self.logger = setup_logger()

        self.config = Config()
        self.db_manager = DatabaseManager(self.config)
        self.reader = ExcelReader(excel_file, sheet_name)
        self.validator = DataValidator()
        self.writer = DatabaseWriter(table_name, self.db_manager)

    def auto_detect_types(self, columns: list) -> Dict[str, str]:
        """ตรวจจับประเภทข้อมูลอัตโนมัติ"""
        type_mapping = {}

        patterns = {
            "datetime": ["date", "time", "วันที่", "เวลา", "created", "updated"],
            "integer": ["id", "age", "count", "number", "จำนวน", "อายุ"],
            "float": ["price", "salary", "amount", "total", "value", "ราคา", "เงินเดือน"],
            "boolean": ["active", "enabled", "is_", "has_", "flag"],
        }

        for column in columns:
            col_lower = column.lower()
            column_type = "string"  # default

            for data_type, pattern_list in patterns.items():
                if any(pattern in col_lower for pattern in pattern_list):
                    column_type = data_type
                    break

            type_mapping[column] = column_type

        return type_mapping

    def process(self, create_table: bool = True) -> Dict[str, Any]:
        """ประมวลผลไฟล์ Excel"""
        start_time = time.time()

        try:
            self.logger.info("🔍 Testing database connection...")
            if not self.db_manager.test_connection():
                raise Exception("Cannot connect to SQL Server")

            self.logger.info("📊 Analyzing Excel file...")
            file_info = self.reader.get_file_info()
            self.logger.info(
                f"File: {file_info['total_rows']:,} rows, {file_info['file_size_mb']:.1f} MB"
            )

            type_mapping = self.auto_detect_types(file_info["columns"])

            total_inserted = 0
            table_created = False

            with tqdm(
                total=file_info["total_rows"], desc="Processing", unit="rows"
            ) as pbar:
                for chunk in self.reader.read_chunks(self.config.CHUNK_SIZE):
                    df_clean = self.validator.clean_dataframe(chunk)
                    df_typed = self.validator.validate_data_types(
                        df_clean, type_mapping
                    )

                    if create_table and not table_created:
                        self.writer.create_table_from_dataframe(df_typed, type_mapping)
                        table_created = True

                    rows_inserted = self.writer.bulk_insert(df_typed)
                    total_inserted += rows_inserted

                    pbar.update(len(chunk))
                    pbar.set_postfix({"Inserted": f"{total_inserted:,}"})

            processing_time = time.time() - start_time
            table_info = self.writer.get_table_info()

            results = {
                "success": True,
                "total_rows": file_info["total_rows"],
                "inserted_rows": total_inserted,
                "processing_time": processing_time,
                "table_info": table_info,
            }

            self.logger.info(
                f"🎉 SUCCESS: {total_inserted:,} rows in {processing_time:.2f}s"
            )
            return results

        except Exception as e:
            self.logger.error(f"❌ Processing failed: {e}")
            return {"success": False, "error": str(e)}


# =================== CLI INTERFACE ===================
def main():
    """Command Line Interface"""

    if len(sys.argv) < 3:
        print(
            """
🎯 Excel to SSMS - Fixed Version

Usage:
  python excel_to_ssms.py <excel_file> <table_name> [sheet_name]

Examples:
  python excel_to_ssms.py data.xlsx employees
  python excel_to_ssms.py sales.xlsx sales_data Sheet1
        """
        )
        sys.exit(1)

    excel_file = sys.argv[1]
    table_name = sys.argv[2]
    sheet_name = sys.argv[3] if len(sys.argv) > 3 else None

    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        pass

    if not Path(excel_file).exists():
        print(f"❌ File not found: {excel_file}")
        sys.exit(1)

    print(f"🚀 Excel to SSMS: {Path(excel_file).name} → {table_name}")
    print("=" * 60)

    processor = ExcelToSSMSProcessor(excel_file, table_name, sheet_name)
    results = processor.process(create_table=True)

    if results["success"]:
        print("\n🎉 Processing Complete!")
        print(f"📋 Total rows: {results['total_rows']:,}")
        print(f"✅ Inserted: {results['inserted_rows']:,}")
        print(f"⏱️ Time: {results['processing_time']:.2f} seconds")
    else:
        print(f"\n❌ Processing failed: {results['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
