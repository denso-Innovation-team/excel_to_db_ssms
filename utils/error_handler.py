"""Error handling for DENSO888"""

def get_user_friendly_error(exception):
    error_map = {
        "ConnectionError": "ไม่สามารถเชื่อมต่อฐานข้อมูล",
        "FileNotFoundError": "ไม่พบไฟล์ที่ระบุ",
        "ValueError": "ข้อมูลไม่ถูกต้อง",
        "ImportError": "ไม่พบโมดูลที่ต้องการ"
    }
    return error_map.get(type(exception).__name__, str(exception))

def setup_error_handling():
    import sys, logging
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    sys.excepthook = handle_exception
