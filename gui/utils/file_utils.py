"""
utils/file_utils.py - Complete File Operation Utilities
"""

import os
import shutil
import json
from pathlib import Path
from typing import List, Optional, Dict, Any, Union
import logging
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)


class FileUtils:
    """Comprehensive file operation utilities for DENSO888"""

    @staticmethod
    def get_excel_files(directory: Union[str, Path]) -> List[Path]:
        """Get all Excel files in directory with detailed info"""
        try:
            path = Path(directory)
            if not path.exists():
                logger.warning(f"Directory does not exist: {directory}")
                return []

            excel_extensions = [".xlsx", ".xls", ".xlsm", ".xlsb"]
            excel_files = []

            for ext in excel_extensions:
                excel_files.extend(path.glob(f"*{ext}"))
                excel_files.extend(path.glob(f"*{ext.upper()}"))

            # Sort by modification time (newest first)
            excel_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

            logger.info(f"Found {len(excel_files)} Excel files in {directory}")
            return excel_files

        except Exception as e:
            logger.error(f"Error getting Excel files from {directory}: {e}")
            return []

    @staticmethod
    def get_file_info(file_path: Union[str, Path]) -> Dict[str, Any]:
        """Get detailed file information"""
        try:
            path = Path(file_path)
            if not path.exists():
                return {"error": "File does not exist"}

            stat = path.stat()

            return {
                "name": path.name,
                "stem": path.stem,
                "suffix": path.suffix,
                "size_bytes": stat.st_size,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "created": datetime.fromtimestamp(stat.st_ctime),
                "modified": datetime.fromtimestamp(stat.st_mtime),
                "accessed": datetime.fromtimestamp(stat.st_atime),
                "is_readonly": not os.access(path, os.W_OK),
                "absolute_path": str(path.absolute()),
                "parent_dir": str(path.parent),
                "exists": True,
            }

        except Exception as e:
            logger.error(f"Error getting file info for {file_path}: {e}")
            return {"error": str(e)}

    @staticmethod
    def ensure_directory(
        directory: Union[str, Path], create_parents: bool = True
    ) -> Path:
        """Ensure directory exists, create if necessary"""
        try:
            path = Path(directory)

            if create_parents:
                path.mkdir(parents=True, exist_ok=True)
            else:
                path.mkdir(exist_ok=True)

            logger.debug(f"Directory ensured: {path}")
            return path

        except Exception as e:
            logger.error(f"Error ensuring directory {directory}: {e}")
            raise

    @staticmethod
    def safe_filename(filename: str, replacement: str = "_") -> str:
        """Create safe filename by replacing invalid characters"""
        # Characters that are not allowed in filenames
        invalid_chars = '<>:"/\\|?*'

        safe_name = filename
        for char in invalid_chars:
            safe_name = safe_name.replace(char, replacement)

        # Remove leading/trailing spaces and dots
        safe_name = safe_name.strip(" .")

        # Ensure filename is not empty
        if not safe_name:
            safe_name = f"file_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Limit length
        if len(safe_name) > 200:
            name_part = safe_name[:180]
            ext_part = safe_name[-20:] if "." in safe_name[-20:] else ""
            safe_name = name_part + ext_part

        return safe_name

    @staticmethod
    def backup_file(
        file_path: Union[str, Path], backup_dir: Optional[Union[str, Path]] = None
    ) -> Optional[Path]:
        """Create backup of a file"""
        try:
            source_path = Path(file_path)
            if not source_path.exists():
                logger.warning(f"Source file does not exist: {file_path}")
                return None

            # Determine backup directory
            if backup_dir:
                backup_path = Path(backup_dir)
            else:
                backup_path = source_path.parent / "backups"

            FileUtils.ensure_directory(backup_path)

            # Create backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = (
                f"{source_path.stem}_backup_{timestamp}{source_path.suffix}"
            )
            backup_file_path = backup_path / backup_filename

            # Copy file
            shutil.copy2(source_path, backup_file_path)

            logger.info(f"File backed up: {file_path} -> {backup_file_path}")
            return backup_file_path

        except Exception as e:
            logger.error(f"Error backing up file {file_path}: {e}")
            return None

    @staticmethod
    def calculate_file_hash(
        file_path: Union[str, Path], algorithm: str = "md5"
    ) -> Optional[str]:
        """Calculate hash of a file"""
        try:
            path = Path(file_path)
            if not path.exists():
                return None

            hash_algo = hashlib.new(algorithm)

            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_algo.update(chunk)

            return hash_algo.hexdigest()

        except Exception as e:
            logger.error(f"Error calculating hash for {file_path}: {e}")
            return None

    @staticmethod
    def find_duplicate_files(directory: Union[str, Path]) -> Dict[str, List[Path]]:
        """Find duplicate files in directory based on content hash"""
        try:
            path = Path(directory)
            if not path.exists():
                return {}

            file_hashes = {}

            for file_path in path.rglob("*"):
                if file_path.is_file():
                    file_hash = FileUtils.calculate_file_hash(file_path)
                    if file_hash:
                        if file_hash not in file_hashes:
                            file_hashes[file_hash] = []
                        file_hashes[file_hash].append(file_path)

            # Return only duplicates (hash with more than one file)
            duplicates = {
                h: files for h, files in file_hashes.items() if len(files) > 1
            }

            logger.info(
                f"Found {len(duplicates)} sets of duplicate files in {directory}"
            )
            return duplicates

        except Exception as e:
            logger.error(f"Error finding duplicates in {directory}: {e}")
            return {}

    @staticmethod
    def clean_temp_files(temp_dir: Union[str, Path], max_age_hours: int = 24) -> int:
        """Clean temporary files older than specified hours"""
        try:
            path = Path(temp_dir)
            if not path.exists():
                return 0

            cutoff_time = datetime.now().timestamp() - (max_age_hours * 3600)
            cleaned_count = 0

            for file_path in path.rglob("*"):
                if file_path.is_file():
                    try:
                        if file_path.stat().st_mtime < cutoff_time:
                            file_path.unlink()
                            cleaned_count += 1
                            logger.debug(f"Cleaned temp file: {file_path}")
                    except Exception as file_error:
                        logger.warning(f"Could not clean {file_path}: {file_error}")

            logger.info(f"Cleaned {cleaned_count} temporary files from {temp_dir}")
            return cleaned_count

        except Exception as e:
            logger.error(f"Error cleaning temp files in {temp_dir}: {e}")
            return 0

    @staticmethod
    def get_directory_size(directory: Union[str, Path]) -> Dict[str, Any]:
        """Get directory size information"""
        try:
            path = Path(directory)
            if not path.exists():
                return {"error": "Directory does not exist"}

            total_size = 0
            file_count = 0
            dir_count = 0

            for item in path.rglob("*"):
                if item.is_file():
                    total_size += item.stat().st_size
                    file_count += 1
                elif item.is_dir():
                    dir_count += 1

            return {
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "total_size_gb": round(total_size / (1024 * 1024 * 1024), 3),
                "file_count": file_count,
                "directory_count": dir_count,
                "path": str(path.absolute()),
            }

        except Exception as e:
            logger.error(f"Error getting directory size for {directory}: {e}")
            return {"error": str(e)}

    @staticmethod
    def validate_excel_file(file_path: Union[str, Path]) -> Dict[str, Any]:
        """Validate Excel file and get basic info"""
        try:
            path = Path(file_path)

            validation_result = {
                "valid": True,
                "errors": [],
                "warnings": [],
                "info": {},
            }

            # Check if file exists
            if not path.exists():
                validation_result["valid"] = False
                validation_result["errors"].append("ไฟล์ไม่มีอยู่")
                return validation_result

            # Check file extension
            valid_extensions = [".xlsx", ".xls", ".xlsm", ".xlsb"]
            if path.suffix.lower() not in valid_extensions:
                validation_result["valid"] = False
                validation_result["errors"].append(
                    f"นามสกุลไฟล์ไม่ถูกต้อง (ต้องเป็น {', '.join(valid_extensions)})"
                )
                return validation_result

            # Get file info
            file_info = FileUtils.get_file_info(path)
            validation_result["info"] = file_info

            # Check file size
            max_size_mb = 100  # 100 MB limit
            if file_info.get("size_mb", 0) > max_size_mb:
                validation_result["warnings"].append(
                    f"ไฟล์ใหญ่ ({file_info['size_mb']:.1f} MB) อาจใช้เวลาประมวลผลนาน"
                )

            # Check if file is locked
            if file_info.get("is_readonly", False):
                validation_result["warnings"].append("ไฟล์เป็น read-only")

            # Try to open with pandas to check if it's a valid Excel file
            try:
                import pandas as pd

                with pd.ExcelFile(path) as excel_file:
                    validation_result["info"]["sheet_names"] = excel_file.sheet_names
                    validation_result["info"]["sheet_count"] = len(
                        excel_file.sheet_names
                    )

                    # Quick sample to check if data exists
                    first_sheet = excel_file.sheet_names[0]
                    sample_df = pd.read_excel(
                        excel_file, sheet_name=first_sheet, nrows=5
                    )
                    validation_result["info"]["sample_columns"] = list(
                        sample_df.columns
                    )
                    validation_result["info"]["sample_rows"] = len(sample_df)

            except Exception as excel_error:
                validation_result["valid"] = False
                validation_result["errors"].append(
                    f"ไม่สามารถอ่านไฟล์ Excel ได้: {str(excel_error)}"
                )

            return validation_result

        except Exception as e:
            logger.error(f"Error validating Excel file {file_path}: {e}")
            return {
                "valid": False,
                "errors": [f"เกิดข้อผิดพลาดในการตรวจสอบไฟล์: {str(e)}"],
                "warnings": [],
                "info": {},
            }

    @staticmethod
    def create_sample_excel(
        output_path: Union[str, Path], template: str = "employees", rows: int = 100
    ) -> bool:
        """Create sample Excel file for testing"""
        try:
            import pandas as pd
            from datetime import datetime, timedelta
            import random

            path = Path(output_path)
            FileUtils.ensure_directory(path.parent)

            if template == "employees":
                # Employee data template
                data = {
                    "employee_id": [f"EMP{i+1:05d}" for i in range(rows)],
                    "first_name": [
                        random.choice(["สมชาย", "สิริพร", "นิรันดร์", "วิภาดา", "อาทิตย์"])
                        for _ in range(rows)
                    ],
                    "last_name": [
                        random.choice(["ใจดี", "ศิริโชติ", "วรรณกุล", "ธนกิจ"])
                        for _ in range(rows)
                    ],
                    "department": [
                        random.choice(["Sales", "IT", "HR", "Finance", "Operations"])
                        for _ in range(rows)
                    ],
                    "salary": [random.randint(25000, 80000) for _ in range(rows)],
                    "hire_date": [
                        (
                            datetime.now() - timedelta(days=random.randint(30, 1825))
                        ).strftime("%Y-%m-%d")
                        for _ in range(rows)
                    ],
                    "active": [random.choice([True, False]) for _ in range(rows)],
                }

            elif template == "sales":
                # Sales data template
                data = {
                    "transaction_id": [f"TXN{i+1:08d}" for i in range(rows)],
                    "customer_name": [f"Customer {i+1}" for i in range(rows)],
                    "product": [
                        random.choice(["Widget A", "Widget B", "Gadget X", "Tool Y"])
                        for _ in range(rows)
                    ],
                    "quantity": [random.randint(1, 100) for _ in range(rows)],
                    "unit_price": [
                        round(random.uniform(10.0, 500.0), 2) for _ in range(rows)
                    ],
                    "total_amount": [0] * rows,  # Will calculate below
                    "sale_date": [
                        (
                            datetime.now() - timedelta(days=random.randint(0, 365))
                        ).strftime("%Y-%m-%d")
                        for _ in range(rows)
                    ],
                    "sales_rep": [
                        f"REP{random.randint(1, 20):03d}" for _ in range(rows)
                    ],
                }

                # Calculate total amount
                for i in range(rows):
                    data["total_amount"][i] = (
                        data["quantity"][i] * data["unit_price"][i]
                    )

            else:  # default/simple template
                data = {
                    "id": list(range(1, rows + 1)),
                    "name": [f"Item {i+1}" for i in range(rows)],
                    "value": [random.randint(1, 1000) for _ in range(rows)],
                    "category": [
                        random.choice(["A", "B", "C", "D"]) for _ in range(rows)
                    ],
                    "date": [
                        (
                            datetime.now() - timedelta(days=random.randint(0, 365))
                        ).strftime("%Y-%m-%d")
                        for _ in range(rows)
                    ],
                }

            # Create DataFrame and save
            df = pd.DataFrame(data)
            df.to_excel(path, index=False, engine="openpyxl")

            logger.info(
                f"Sample Excel file created: {path} ({template} template, {rows} rows)"
            )
            return True

        except Exception as e:
            logger.error(f"Error creating sample Excel file: {e}")
            return False

    @staticmethod
    def monitor_file_changes(
        file_path: Union[str, Path], callback: callable = None
    ) -> Dict[str, Any]:
        """Monitor file for changes (basic implementation)"""
        try:
            path = Path(file_path)
            if not path.exists():
                return {"error": "File does not exist"}

            initial_stat = path.stat()
            initial_info = {
                "size": initial_stat.st_size,
                "modified": initial_stat.st_mtime,
                "hash": FileUtils.calculate_file_hash(path),
            }

            return {"path": str(path), "initial_info": initial_info, "monitoring": True}

        except Exception as e:
            logger.error(f"Error setting up file monitoring for {file_path}: {e}")
            return {"error": str(e)}

    @staticmethod
    def compress_directory(
        source_dir: Union[str, Path], output_file: Union[str, Path]
    ) -> bool:
        """Compress directory to zip file"""
        try:
            import zipfile

            source_path = Path(source_dir)
            output_path = Path(output_file)

            if not source_path.exists():
                logger.error(f"Source directory does not exist: {source_dir}")
                return False

            FileUtils.ensure_directory(output_path.parent)

            with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for file_path in source_path.rglob("*"):
                    if file_path.is_file():
                        # Calculate relative path for archive
                        arcname = file_path.relative_to(source_path)
                        zipf.write(file_path, arcname)

            logger.info(f"Directory compressed: {source_dir} -> {output_file}")
            return True

        except Exception as e:
            logger.error(f"Error compressing directory {source_dir}: {e}")
            return False

    @staticmethod
    def extract_archive(
        archive_file: Union[str, Path], extract_to: Union[str, Path]
    ) -> bool:
        """Extract zip archive"""
        try:
            import zipfile

            archive_path = Path(archive_file)
            extract_path = Path(extract_to)

            if not archive_path.exists():
                logger.error(f"Archive file does not exist: {archive_file}")
                return False

            FileUtils.ensure_directory(extract_path)

            with zipfile.ZipFile(archive_path, "r") as zipf:
                zipf.extractall(extract_path)

            logger.info(f"Archive extracted: {archive_file} -> {extract_to}")
            return True

        except Exception as e:
            logger.error(f"Error extracting archive {archive_file}: {e}")
            return False


class RecentFilesManager:
    """Manage recent files list with persistence"""

    def __init__(self, config_file: str = "recent_files.json", max_files: int = 10):
        self.config_file = Path(config_file)
        self.max_files = max_files
        self.recent_files = self._load_recent_files()

    def _load_recent_files(self) -> List[Dict[str, Any]]:
        """Load recent files from config"""
        try:
            if self.config_file.exists():
                with open(self.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("recent_files", [])
            return []
        except Exception as e:
            logger.error(f"Error loading recent files: {e}")
            return []

    def _save_recent_files(self) -> bool:
        """Save recent files to config"""
        try:
            FileUtils.ensure_directory(self.config_file.parent)

            data = {
                "recent_files": self.recent_files,
                "last_updated": datetime.now().isoformat(),
            }

            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            logger.error(f"Error saving recent files: {e}")
            return False

    def add_file(self, file_path: Union[str, Path], file_type: str = "excel") -> bool:
        """Add file to recent files list"""
        try:
            path = Path(file_path)
            if not path.exists():
                return False

            file_info = FileUtils.get_file_info(path)

            recent_item = {
                "path": str(path.absolute()),
                "name": path.name,
                "type": file_type,
                "size_mb": file_info.get("size_mb", 0),
                "modified": file_info.get("modified", datetime.now()).isoformat(),
                "added_at": datetime.now().isoformat(),
            }

            # Remove if already exists
            self.recent_files = [
                item
                for item in self.recent_files
                if item["path"] != recent_item["path"]
            ]

            # Add to beginning
            self.recent_files.insert(0, recent_item)

            # Trim to max size
            self.recent_files = self.recent_files[: self.max_files]

            # Save
            self._save_recent_files()

            logger.info(f"Added to recent files: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Error adding recent file {file_path}: {e}")
            return False

    def get_recent_files(self, file_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get recent files list, optionally filtered by type"""
        try:
            # Filter out non-existent files
            existing_files = []
            for item in self.recent_files:
                if Path(item["path"]).exists():
                    existing_files.append(item)

            # Update list if any files were removed
            if len(existing_files) != len(self.recent_files):
                self.recent_files = existing_files
                self._save_recent_files()

            # Filter by type if specified
            if file_type:
                return [
                    item for item in self.recent_files if item.get("type") == file_type
                ]

            return self.recent_files

        except Exception as e:
            logger.error(f"Error getting recent files: {e}")
            return []

    def clear_recent_files(self) -> bool:
        """Clear all recent files"""
        try:
            self.recent_files = []
            self._save_recent_files()
            logger.info("Recent files cleared")
            return True
        except Exception as e:
            logger.error(f"Error clearing recent files: {e}")
            return False

    def remove_file(self, file_path: Union[str, Path]) -> bool:
        """Remove specific file from recent files"""
        try:
            path_str = str(Path(file_path).absolute())
            original_count = len(self.recent_files)

            self.recent_files = [
                item for item in self.recent_files if item["path"] != path_str
            ]

            if len(self.recent_files) < original_count:
                self._save_recent_files()
                logger.info(f"Removed from recent files: {file_path}")
                return True

            return False

        except Exception as e:
            logger.error(f"Error removing recent file {file_path}: {e}")
            return False
