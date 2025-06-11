#!/usr/bin/env python3
"""
Fix Unicode Logging + ProgressTracker Context Manager
แก้ไข 2 ปัญหาหลัก: Unicode encoding + ProgressTracker
"""


def fix_logger():
    """แก้ไข logger.py สำหรับ Unicode"""

    logger_content = '''import logging
import logging.handlers
from pathlib import Path
import sys

def setup_logger(name: str = "excel_to_db") -> logging.Logger:
    """Setup logger with UTF-8 encoding for Windows"""

    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "excel_to_ssms.log"

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Create formatter (NO EMOJIS for file logging)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    console_formatter = logging.Formatter(
        "%(levelname)s - %(message)s"
    )

    # File handler with UTF-8 encoding
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, 
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'  # Force UTF-8
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not setup file logging: {e}")

    # Console handler with UTF-8 for Windows
    try:
        console_handler = logging.StreamHandler(sys.stdout)
        
        # Force UTF-8 encoding for Windows console
        if sys.platform == "win32":
            try:
                # Try to set console to UTF-8
                import locale
                console_handler.stream.reconfigure(encoding='utf-8')
            except:
                # Fallback: use basic formatter without emojis
                pass
        
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    except Exception as e:
        print(f"Warning: Console logging issue: {e}")

    return logger
'''

    with open("src/utils/logger.py", "w", encoding="utf-8") as f:
        f.write(logger_content)

    print("✅ Fixed logger.py (UTF-8 encoding)")


def fix_progress_tracker():
    """แก้ไข ProgressTracker ให้รองรับ context manager"""

    progress_content = '''from tqdm import tqdm
from typing import Optional, Iterator, Any
import time

class ProgressTracker:
    """Progress tracker with context manager support"""
    
    def __init__(self, total: int, description: str = "Processing"):
        self.total = total
        self.description = description
        self.progress_bar = None
        self.start_time = None

    def __enter__(self):
        """Enter context manager"""
        self.start_time = time.time()
        self.progress_bar = tqdm(
            total=self.total, 
            desc=self.description, 
            unit="rows", 
            unit_scale=True,
            ncols=100
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager"""
        if self.progress_bar:
            self.progress_bar.close()
        
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            print(f"\\nProcessing completed in {elapsed_time:.2f} seconds")
            if self.total > 0:
                print(f"Average speed: {self.total/elapsed_time:.0f} rows/second")

    def update(self, n: int = 1):
        """Update progress bar"""
        if self.progress_bar:
            self.progress_bar.update(n)

    def set_postfix(self, **kwargs):
        """Set progress bar postfix"""
        if self.progress_bar:
            self.progress_bar.set_postfix(**kwargs)

    def close(self):
        """Manual close (for backward compatibility)"""
        if self.progress_bar:
            self.progress_bar.close()

def track_progress(iterator: Iterator[Any], total: int, description: str = "Processing"):
    """Context manager for progress tracking"""
    with ProgressTracker(total, description) as tracker:
        for item in iterator:
            yield item
            tracker.update(len(item) if hasattr(item, "__len__") else 1)
'''

    with open("src/utils/progress.py", "w", encoding="utf-8") as f:
        f.write(progress_content)

    print("✅ Fixed progress.py (context manager)")


def fix_main_script():
    """แก้ไข excel_to_ssms.py ลบ emojis ออกจาก logging"""

    try:
        with open("excel_to_ssms.py", "r", encoding="utf-8") as f:
            content = f.read()

        # แทนที่ emoji logging ด้วย text only
        emoji_replacements = [
            (
                'self.logger.info(f"🚀 เริ่มประมวลผล:',
                'self.logger.info(f"Starting process:',
            ),
            ('self.logger.info(f"📊 ไฟล์:', 'self.logger.info(f"File info:'),
            (
                'self.logger.info(f"🔍 ตรวจจับประเภทข้อมูล:',
                'self.logger.info(f"Type detection:',
            ),
            ('self.logger.info(f"✅ สร้างตาราง', 'self.logger.info(f"Created table'),
            (
                'self.logger.error(f"❌ การประมวลผลล้มเหลว:',
                'self.logger.error(f"Processing failed:',
            ),
        ]

        for old, new in emoji_replacements:
            content = content.replace(old, new)

        with open("excel_to_ssms.py", "w", encoding="utf-8") as f:
            f.write(content)

        print("✅ Fixed excel_to_ssms.py (removed emoji logging)")

    except Exception as e:
        print(f"⚠️ Could not fix main script: {e}")


def test_fixes():
    """ทดสอบการแก้ไข"""

    print("\\n🧪 Testing fixes...")

    try:
        # Test logger
        from src.utils.logger import setup_logger

        logger = setup_logger()
        logger.info("Test logging without emojis")
        print("✅ Logger working")

        # Test progress tracker
        from src.utils.progress import ProgressTracker

        with ProgressTracker(10, "Test") as progress:
            import time

            for i in range(10):
                time.sleep(0.01)
                progress.update(1)

        print("✅ ProgressTracker working")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def main():
    """Fix Unicode and ProgressTracker issues"""

    print("🔧 Fix Unicode + ProgressTracker Issues")
    print("=" * 40)

    # Fix components
    fix_logger()
    fix_progress_tracker()
    fix_main_script()

    # Test fixes
    if test_fixes():
        print("\\n✅ All fixes applied!")
        print(
            "🚀 Try again: python excel_to_ssms.py data/samples/sales_50000.xlsx sales_50k"
        )
    else:
        print("\\n❌ Some issues remain")


if __name__ == "__main__":
    main()
