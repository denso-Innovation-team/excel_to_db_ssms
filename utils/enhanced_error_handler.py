"""
utils/enhanced_error_handler.py
Professional-Grade Error Handling System
"""

import logging
import traceback
import tkinter.messagebox as msgbox
from typing import Optional, Dict, Any, Callable, List
from pathlib import Path
import json
from datetime import datetime
from enum import Enum
from dataclasses import dataclass
import functools


class ErrorSeverity(Enum):
    """Error severity levels"""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ErrorCategory(Enum):
    """Error categories for better handling"""

    DATABASE = "database"
    EXCEL = "excel"
    NETWORK = "network"
    VALIDATION = "validation"
    PERMISSION = "permission"
    MEMORY = "memory"
    UNKNOWN = "unknown"


@dataclass
class ErrorContext:
    """Enhanced error context information"""

    operation: str
    user_action: str
    system_state: Dict[str, Any]
    timestamp: datetime
    thread_id: str
    memory_usage: float
    active_connections: int


class ErrorRecoveryStrategy:
    """Base class for error recovery strategies"""

    def can_recover(self, error: Exception, context: ErrorContext) -> bool:
        """Check if this strategy can handle the error"""
        raise NotImplementedError

    def recover(self, error: Exception, context: ErrorContext) -> bool:
        """Attempt to recover from the error"""
        raise NotImplementedError


class DatabaseRecoveryStrategy(ErrorRecoveryStrategy):
    """Recovery strategy for database errors"""

    def __init__(self, connection_service):
        self.connection_service = connection_service
        self.retry_count = 0
        self.max_retries = 3

    def can_recover(self, error: Exception, context: ErrorContext) -> bool:
        db_errors = ["ConnectionError", "OperationalError", "TimeoutError"]
        return any(err in str(type(error)) for err in db_errors)

    def recover(self, error: Exception, context: ErrorContext) -> bool:
        if self.retry_count >= self.max_retries:
            return False

        try:
            # Attempt to reconnect
            if hasattr(self.connection_service, "reconnect"):
                self.connection_service.reconnect()
                self.retry_count += 1
                return True
        except Exception:
            pass

        return False


class ExcelRecoveryStrategy(ErrorRecoveryStrategy):
    """Recovery strategy for Excel processing errors"""

    def can_recover(self, error: Exception, context: ErrorContext) -> bool:
        excel_errors = ["XLRDError", "PermissionError", "FileNotFoundError"]
        return any(err in str(type(error)) for err in excel_errors)

    def recover(self, error: Exception, context: ErrorContext) -> bool:
        error_type = type(error).__name__

        if error_type == "PermissionError":
            # Suggest closing Excel application
            return msgbox.askyesno(
                "File Access Error",
                "File might be open in Excel. Close Excel and retry?",
            )
        elif error_type == "FileNotFoundError":
            # Offer file selection dialog
            return msgbox.askyesno(
                "File Not Found", "Would you like to select a different file?"
            )

        return False


class EnhancedErrorHandler:
    """Professional-grade error handling system"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._get_default_config()
        self.error_log = Path("logs/errors.json")
        self.error_stats = Path("logs/error_stats.json")
        self.recovery_strategies: List[ErrorRecoveryStrategy] = []
        self.error_listeners: List[Callable] = []
        self.error_history: List[Dict[str, Any]] = []
        self.session_stats = {
            "total_errors": 0,
            "recovered_errors": 0,
            "critical_errors": 0,
            "session_start": datetime.now(),
        }

        # Initialize directories
        self.error_log.parent.mkdir(exist_ok=True)

        # Load existing error history
        self._load_error_history()

    def _get_default_config(self) -> Dict[str, Any]:
        """Default configuration"""
        return {
            "max_history": 1000,
            "auto_recovery": True,
            "show_dialogs": True,
            "log_to_file": True,
            "log_to_console": True,
            "collect_system_info": True,
            "enable_crash_dumps": False,
        }

    def add_recovery_strategy(self, strategy: ErrorRecoveryStrategy):
        """Add error recovery strategy"""
        self.recovery_strategies.append(strategy)

    def add_error_listener(self, listener: Callable):
        """Add error event listener"""
        self.error_listeners.append(listener)

    def handle_error(
        self,
        error: Exception,
        context: str = "",
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        user_action: str = "",
        recoverable: bool = True,
    ) -> bool:
        """
        Handle error with comprehensive logging and recovery
        Returns True if error was recovered, False otherwise
        """

        # Create enhanced error context
        error_context = self._create_error_context(context, user_action)

        # Classify error automatically if not specified
        if category == ErrorCategory.UNKNOWN:
            category = self._classify_error(error)

        # Create error record
        error_record = self._create_error_record(
            error, error_context, severity, category
        )

        # Log error
        self._log_error(error_record)

        # Update statistics
        self._update_stats(severity, category)

        # Notify listeners
        self._notify_listeners(error_record)

        # Attempt recovery if enabled and appropriate
        recovered = False
        if recoverable and self.config["auto_recovery"]:
            recovered = self._attempt_recovery(error, error_context, category)

        # Show user dialog if not recovered
        if not recovered and self.config["show_dialogs"]:
            self._show_error_dialog(error_record, recovered)

        return recovered

    def _create_error_context(self, operation: str, user_action: str) -> ErrorContext:
        """Create detailed error context"""
        import psutil
        import threading

        try:
            memory_usage = psutil.virtual_memory().percent
        except:
            memory_usage = 0.0

        return ErrorContext(
            operation=operation,
            user_action=user_action,
            system_state=self._collect_system_state(),
            timestamp=datetime.now(),
            thread_id=str(threading.current_thread().ident),
            memory_usage=memory_usage,
            active_connections=self._get_active_connections(),
        )

    def _classify_error(self, error: Exception) -> ErrorCategory:
        """Automatically classify error by type and message"""
        error_type = type(error).__name__
        error_msg = str(error).lower()

        # Database errors
        if any(
            term in error_type.lower() for term in ["connection", "database", "sql"]
        ):
            return ErrorCategory.DATABASE

        # Excel errors
        if any(term in error_type.lower() for term in ["excel", "xlrd", "openpyxl"]):
            return ErrorCategory.EXCEL

        # Network errors
        if any(
            term in error_type.lower() for term in ["network", "timeout", "connection"]
        ):
            return ErrorCategory.NETWORK

        # Permission errors
        if "permission" in error_type.lower() or "access" in error_msg:
            return ErrorCategory.PERMISSION

        # Memory errors
        if "memory" in error_type.lower() or "memory" in error_msg:
            return ErrorCategory.MEMORY

        # Validation errors
        if any(
            term in error_type.lower() for term in ["value", "validation", "format"]
        ):
            return ErrorCategory.VALIDATION

        return ErrorCategory.UNKNOWN

    def _create_error_record(
        self,
        error: Exception,
        context: ErrorContext,
        severity: ErrorSeverity,
        category: ErrorCategory,
    ) -> Dict[str, Any]:
        """Create comprehensive error record"""
        return {
            "id": f"ERR_{int(context.timestamp.timestamp())}",
            "timestamp": context.timestamp.isoformat(),
            "type": type(error).__name__,
            "message": str(error),
            "severity": severity.value,
            "category": category.value,
            "operation": context.operation,
            "user_action": context.user_action,
            "thread_id": context.thread_id,
            "memory_usage": context.memory_usage,
            "active_connections": context.active_connections,
            "traceback": traceback.format_exc(),
            "system_state": context.system_state,
            "recovery_attempted": False,
            "recovery_successful": False,
        }

    def _collect_system_state(self) -> Dict[str, Any]:
        """Collect current system state information"""
        if not self.config["collect_system_info"]:
            return {}

        try:
            import psutil

            return {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage("/").percent,
                "python_version": f"{psutil.sys.version_info.major}.{psutil.sys.version_info.minor}",
                "process_count": len(psutil.pids()),
            }
        except Exception:
            return {"collection_failed": True}

    def _get_active_connections(self) -> int:
        """Get number of active database connections"""
        # This would be integrated with your connection pool service
        try:
            # Placeholder - integrate with actual connection service
            return 0
        except Exception:
            return -1

    def _log_error(self, error_record: Dict[str, Any]):
        """Log error to various outputs"""

        # Console logging
        if self.config["log_to_console"]:
            logging.error(
                f"[{error_record['severity'].upper()}] {error_record['category']} "
                f"in {error_record['operation']}: {error_record['message']}"
            )

        # File logging
        if self.config["log_to_file"]:
            self.error_history.append(error_record)
            self._save_error_history()

    def _update_stats(self, severity: ErrorSeverity, category: ErrorCategory):
        """Update error statistics"""
        self.session_stats["total_errors"] += 1

        if severity == ErrorSeverity.CRITICAL:
            self.session_stats["critical_errors"] += 1

        # Save stats to file
        try:
            with open(self.error_stats, "w", encoding="utf-8") as f:
                json.dump(self.session_stats, f, indent=2, default=str)
        except Exception:
            pass

    def _notify_listeners(self, error_record: Dict[str, Any]):
        """Notify all registered error listeners"""
        for listener in self.error_listeners:
            try:
                listener(error_record)
            except Exception as e:
                logging.error(f"Error listener failed: {e}")

    def _attempt_recovery(
        self, error: Exception, context: ErrorContext, category: ErrorCategory
    ) -> bool:
        """Attempt to recover from error using available strategies"""

        for strategy in self.recovery_strategies:
            try:
                if strategy.can_recover(error, context):
                    if strategy.recover(error, context):
                        self.session_stats["recovered_errors"] += 1
                        logging.info(
                            f"Successfully recovered from {type(error).__name__}"
                        )
                        return True
            except Exception as recovery_error:
                logging.error(f"Recovery strategy failed: {recovery_error}")

        return False

    def _show_error_dialog(self, error_record: Dict[str, Any], recovered: bool):
        """Show user-friendly error dialog"""
        severity = error_record["severity"]
        category = error_record["category"]
        message = error_record["message"]

        # Get user-friendly message
        friendly_msg = self._get_friendly_message(error_record)
        recovery_suggestion = self._get_recovery_suggestion(
            category, error_record["type"]
        )

        # Choose dialog type based on severity
        if severity == "critical":
            title = "🚨 Critical Error"
            icon = "error"
        elif severity == "high":
            title = "⚠️ Error"
            icon = "error"
        else:
            title = "ℹ️ Notice"
            icon = "warning"

        dialog_message = f"{friendly_msg}\n\n💡 {recovery_suggestion}"

        if recovered:
            dialog_message += "\n\n✅ System has automatically recovered."

        # Show appropriate dialog
        if icon == "error":
            msgbox.showerror(title, dialog_message)
        else:
            msgbox.showwarning(title, dialog_message)

    def _get_friendly_message(self, error_record: Dict[str, Any]) -> str:
        """Generate user-friendly error message"""
        category = error_record["category"]
        error_type = error_record["type"]

        messages = {
            "database": {
                "ConnectionError": "ไม่สามารถเชื่อมต่อฐานข้อมูลได้",
                "TimeoutError": "การเชื่อมต่อฐานข้อมูลหมดเวลา",
                "default": "เกิดปัญหาในการใช้งานฐานข้อมูล",
            },
            "excel": {
                "FileNotFoundError": "ไม่พบไฟล์ Excel ที่ระบุ",
                "PermissionError": "ไม่สามารถเข้าถึงไฟล์ Excel ได้ (อาจเปิดอยู่)",
                "default": "เกิดปัญหาในการประมวลผลไฟล์ Excel",
            },
            "permission": {
                "PermissionError": "ไม่มีสิทธิ์เข้าถึงไฟล์หรือโฟลเดอร์",
                "default": "ปัญหาเรื่องสิทธิ์การเข้าถึง",
            },
            "memory": {
                "MemoryError": "หน่วยความจำไม่เพียงพอ",
                "default": "ปัญหาเรื่องหน่วยความจำ",
            },
        }

        category_messages = messages.get(category, {"default": "เกิดข้อผิดพลาดในระบบ"})
        return category_messages.get(error_type, category_messages["default"])

    def _get_recovery_suggestion(self, category: str, error_type: str) -> str:
        """Get recovery suggestion based on error"""
        suggestions = {
            "database": "ตรวจสอบการเชื่อมต่อและลองใหม่อีกครั้ง",
            "excel": "ปิดไฟล์ Excel และตรวจสอบ path ที่ระบุ",
            "permission": "รันโปรแกรมในฐานะ Administrator",
            "memory": "ปิดโปรแกรมอื่นๆ และลองใหม่",
            "network": "ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต",
            "validation": "ตรวจสอบรูปแบบข้อมูลที่ใส่เข้ามา",
        }

        return suggestions.get(category, "ลองดำเนินการใหม่อีกครั้ง")

    def _load_error_history(self):
        """Load error history from file"""
        try:
            if self.error_log.exists():
                with open(self.error_log, "r", encoding="utf-8") as f:
                    self.error_history = json.load(f)
        except Exception:
            self.error_history = []

    def _save_error_history(self):
        """Save error history to file"""
        try:
            # Keep only recent errors
            max_history = self.config["max_history"]
            if len(self.error_history) > max_history:
                self.error_history = self.error_history[-max_history:]

            with open(self.error_log, "w", encoding="utf-8") as f:
                json.dump(self.error_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Failed to save error history: {e}")

    def get_error_stats(self) -> Dict[str, Any]:
        """Get comprehensive error statistics"""
        if not self.error_history:
            return self.session_stats

        # Analyze error patterns
        categories = {}
        severities = {}
        recent_errors = []

        for error in self.error_history[-100:]:  # Last 100 errors
            cat = error.get("category", "unknown")
            sev = error.get("severity", "unknown")

            categories[cat] = categories.get(cat, 0) + 1
            severities[sev] = severities.get(sev, 0) + 1

            # Recent errors (last 24 hours)
            error_time = datetime.fromisoformat(error["timestamp"])
            if (datetime.now() - error_time).total_seconds() < 86400:
                recent_errors.append(error)

        return {
            **self.session_stats,
            "error_by_category": categories,
            "error_by_severity": severities,
            "recent_errors_24h": len(recent_errors),
            "total_logged_errors": len(self.error_history),
            "recovery_rate": (
                self.session_stats["recovered_errors"]
                / max(self.session_stats["total_errors"], 1)
                * 100
            ),
        }

    def clear_error_history(self):
        """Clear error history"""
        self.error_history = []
        try:
            if self.error_log.exists():
                self.error_log.unlink()
        except Exception:
            pass


# Decorator for automatic error handling
def handle_errors(
    operation: str = "",
    severity: ErrorSeverity = ErrorSeverity.MEDIUM,
    category: ErrorCategory = ErrorCategory.UNKNOWN,
    recoverable: bool = True,
    error_handler: Optional[EnhancedErrorHandler] = None,
):
    """Decorator for automatic error handling"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                handler = error_handler or _get_global_error_handler()

                # Try to get operation name from function if not provided
                op_name = operation or f"{func.__module__}.{func.__name__}"

                recovered = handler.handle_error(
                    e, op_name, severity, category, recoverable=recoverable
                )

                # Re-raise if not recovered
                if not recovered:
                    raise

                return None  # Or appropriate default value

        return wrapper

    return decorator


# Global error handler instance
_global_error_handler: Optional[EnhancedErrorHandler] = None


def setup_enhanced_error_handling(
    config: Optional[Dict[str, Any]] = None, connection_service=None
) -> EnhancedErrorHandler:
    """Setup global enhanced error handler"""
    global _global_error_handler

    _global_error_handler = EnhancedErrorHandler(config)

    # Add recovery strategies
    if connection_service:
        _global_error_handler.add_recovery_strategy(
            DatabaseRecoveryStrategy(connection_service)
        )

    _global_error_handler.add_recovery_strategy(ExcelRecoveryStrategy())

    # Set as default exception handler
    import sys

    def global_exception_handler(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        _global_error_handler.handle_error(
            exc_value, "global_exception", ErrorSeverity.CRITICAL
        )

    sys.excepthook = global_exception_handler

    return _global_error_handler


def _get_global_error_handler() -> EnhancedErrorHandler:
    """Get global error handler instance"""
    global _global_error_handler
    if _global_error_handler is None:
        _global_error_handler = EnhancedErrorHandler()
    return _global_error_handler


# Convenience functions
def log_error(
    error: Exception, context: str = "", severity: ErrorSeverity = ErrorSeverity.MEDIUM
):
    """Quick error logging"""
    handler = _get_global_error_handler()
    handler.handle_error(error, context, severity, recoverable=False)


def try_recover(error: Exception, context: str = "") -> bool:
    """Attempt error recovery"""
    handler = _get_global_error_handler()
    return handler.handle_error(error, context, recoverable=True)
