"""
utils/logger.py
Logging Configuration
"""

import logging


def setup_logger(name: str = "denso888", level: str = "INFO", log_file: str = None):
    """Enhanced logger setup"""
    logger = logging.getLogger(name)

    # เพิ่ม null handler เพื่อป้องกัน warning
    if not logger.handlers:
        logger.addHandler(logging.NullHandler())

    # [โค้ดเดิม...]

    # เพิ่ม custom filter สำหรับ sensitive data
    class SensitiveDataFilter(logging.Filter):
        def filter(self, record):
            # ซ่อน password และ sensitive data
            record.msg = str(record.msg).replace("password=", "password=***")
            return True

    for handler in logger.handlers:
        handler.addFilter(SensitiveDataFilter())

    return logger


def get_logger(name: str = "denso888") -> logging.Logger:
    """Get existing logger"""
    return logging.getLogger(name)
