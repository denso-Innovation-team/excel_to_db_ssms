"""Simple error handling for DENSO888"""


def get_user_friendly_error(exception):
    """Convert errors to Thai messages"""
    error_map = {
        "ConnectionError": "ไม่สามารถเชื่อมต่อฐานข้อมูล",
        "FileNotFoundError": "ไม่พบไฟล์ที่ระบุ",
        "PermissionError": "ไม่มีสิทธิ์เข้าถึงไฟล์",
        "ValueError": "ข้อมูลไม่ถูกต้อง",
        "ImportError": "ไม่พบโมดูลที่ต้องการ",
        "AttributeError": "ฟังก์ชันไม่พร้อมใช้งาน",
    }
    error_type = type(exception).__name__
    return error_map.get(error_type, f"ข้อผิดพลาด: {str(exception)}")


def setup_error_handling():
    """Basic error setup - placeholder for compatibility"""
    pass
