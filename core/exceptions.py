# สร้างไฟล์ใหม่: core/exceptions.py
class DENSO888Exception(Exception):
    """Base exception for DENSO888 application"""

    pass


class DatabaseConnectionError(DENSO888Exception):
    """Database connection related errors"""

    pass


class FileProcessingError(DENSO888Exception):
    """File processing related errors"""

    pass


class ConfigurationError(DENSO888Exception):
    """Configuration related errors"""

    pass
