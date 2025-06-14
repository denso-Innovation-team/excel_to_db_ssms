# core/services/__init__.py
"""
Service Layer - Business Logic Separation
แยก business logic ออกจาก UI layer
"""

from abc import ABC, abstractmethod
from typing import Protocol, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


# ===== SERVICE PROTOCOLS =====
class DatabaseService(Protocol):
    """Database operations interface"""

    def connect(self) -> bool: ...
    def execute_query(self, query: str) -> Any: ...
    def bulk_insert(self, table: str, data: Any) -> int: ...


class ExcelService(Protocol):
    """Excel processing interface"""

    def validate_file(self, path: str) -> Dict[str, Any]: ...
    def process_file(self, path: str) -> Any: ...


class AuthService(Protocol):
    """Authentication interface"""

    def authenticate(self, username: str, password: str) -> bool: ...
    def get_current_user(self) -> Optional[Dict[str, Any]]: ...


# ===== BASE SERVICE =====
class BaseService(ABC):
    """Base service with common functionality"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize service"""
        pass

    def get_status(self) -> Dict[str, Any]:
        """Get service status"""
        return {
            "name": self.__class__.__name__,
            "status": "active",
            "config": self.config,
        }


# ===== CONCRETE SERVICES =====
class ExcelProcessingService(BaseService):
    """เฉพาะการประมวลผล Excel"""

    def __init__(self, config=None):
        super().__init__(config)
        self.supported_formats = [".xlsx", ".xls", ".xlsm"]

    def initialize(self) -> bool:
        self.logger.info("Excel service initialized")
        return True

    def validate_file(self, file_path: str) -> Dict[str, Any]:
        """Validate Excel file"""
        from pathlib import Path

        path = Path(file_path)

        result = {"valid": True, "errors": [], "warnings": [], "info": {}}

        # Basic validation
        if not path.exists():
            result["valid"] = False
            result["errors"].append("File not found")
            return result

        if path.suffix not in self.supported_formats:
            result["valid"] = False
            result["errors"].append(f"Unsupported format: {path.suffix}")
            return result

        # Size check
        size_mb = path.stat().st_size / (1024 * 1024)
        if size_mb > 100:
            result["warnings"].append(f"Large file: {size_mb:.1f}MB")

        result["info"] = {
            "file_name": path.name,
            "size_mb": round(size_mb, 2),
            "format": path.suffix,
        }

        return result

    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get detailed file information"""
        validation = self.validate_file(file_path)
        if not validation["valid"]:
            return {"error": validation["errors"][0]}

        try:
            import pandas as pd

            # Quick info extraction
            df_sample = pd.read_excel(file_path, nrows=5)

            return {
                "file_path": file_path,
                "sample_rows": len(df_sample),
                "columns": df_sample.columns.tolist(),
                "column_count": len(df_sample.columns),
                "validation": validation,
            }
        except Exception as e:
            return {"error": f"Failed to read file: {e}"}


class MockDataService(BaseService):
    """เฉพาะการสร้าง Mock Data"""

    def initialize(self) -> bool:
        self.logger.info("Mock data service initialized")
        return True

    def get_available_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get available data templates"""
        return {
            "employees": {
                "name": "Employee Records",
                "description": "HR data with departments and salaries",
                "default_rows": 1000,
                "columns": ["id", "name", "email", "department", "salary"],
            },
            "sales": {
                "name": "Sales Transactions",
                "description": "Transaction data with customers",
                "default_rows": 5000,
                "columns": ["id", "customer", "product", "amount", "date"],
            },
            "inventory": {
                "name": "Product Inventory",
                "description": "Stock levels and locations",
                "default_rows": 2000,
                "columns": ["sku", "product", "stock", "location", "price"],
            },
        }

    def generate_data(self, template: str, rows: int = 1000) -> Dict[str, Any]:
        """Generate mock data by template"""
        templates = self.get_available_templates()

        if template not in templates:
            return {"error": f"Unknown template: {template}"}

        try:
            # Import only when needed
            from core.mock_generator import MockDataTemplates

            df = MockDataTemplates.generate_by_template(template, rows)

            return {
                "success": True,
                "template": template,
                "rows_generated": len(df),
                "columns": df.columns.tolist(),
                "data": df,  # Real DataFrame
            }
        except Exception as e:
            return {"error": f"Generation failed: {e}"}


class DatabaseConnectionService(BaseService):
    """เฉพาะการจัดการ Database Connection"""

    def __init__(self, config=None):
        super().__init__(config)
        self.connection = None
        self.db_type = "none"

    def initialize(self) -> bool:
        """Initialize database connection"""
        return self.connect()

    def connect(self, db_type: str = "auto") -> bool:
        """Connect to database with fallback"""
        if db_type == "auto":
            # Try SQL Server first, fallback to SQLite
            if self._try_sqlserver():
                self.db_type = "sqlserver"
                return True
            elif self._try_sqlite():
                self.db_type = "sqlite"
                return True
            return False

        elif db_type == "sqlite":
            return self._try_sqlite()
        elif db_type == "sqlserver":
            return self._try_sqlserver()

        return False

    def _try_sqlserver(self) -> bool:
        """Try SQL Server connection"""
        try:
            from core.database_manager import SQLServerManager
            from config.database import DatabaseConfig

            config = DatabaseConfig.from_env()
            manager = SQLServerManager(config)

            if manager.connect():
                self.connection = manager
                self.logger.info("Connected to SQL Server")
                return True
        except Exception as e:
            self.logger.warning(f"SQL Server connection failed: {e}")

        return False

    def _try_sqlite(self) -> bool:
        """Try SQLite connection"""
        try:
            from core.database_manager import SQLiteManager

            manager = SQLiteManager("denso888_data.db")
            if manager.connect():
                self.connection = manager
                self.logger.info("Connected to SQLite")
                return True
        except Exception as e:
            self.logger.error(f"SQLite connection failed: {e}")

        return False

    def get_connection_info(self) -> Dict[str, Any]:
        """Get current connection information"""
        if not self.connection:
            return {"status": "disconnected"}

        return {
            "status": "connected",
            "type": self.db_type,
            "connection": self.connection,
        }


# ===== SERVICE MANAGER =====
class ServiceManager:
    """Central service management"""

    def __init__(self):
        self.services: Dict[str, BaseService] = {}
        self.logger = logging.getLogger("ServiceManager")

    def register_service(self, name: str, service: BaseService):
        """Register a service"""
        self.services[name] = service
        self.logger.info(f"Registered service: {name}")

    def initialize_all(self) -> Dict[str, bool]:
        """Initialize all services"""
        results = {}
        for name, service in self.services.items():
            try:
                results[name] = service.initialize()
                self.logger.info(f"Service {name}: {'✅' if results[name] else '❌'}")
            except Exception as e:
                results[name] = False
                self.logger.error(f"Service {name} failed: {e}")

        return results

    def get_service(self, name: str) -> Optional[BaseService]:
        """Get service by name"""
        return self.services.get(name)

    def get_status_all(self) -> Dict[str, Any]:
        """Get status of all services"""
        return {name: service.get_status() for name, service in self.services.items()}


# ===== GLOBAL SERVICE REGISTRY =====
# Singleton pattern for global access
_service_manager = None


def get_service_manager() -> ServiceManager:
    """Get global service manager"""
    global _service_manager
    if _service_manager is None:
        _service_manager = ServiceManager()

        # Register default services
        _service_manager.register_service("excel", ExcelProcessingService())
        _service_manager.register_service("mock", MockDataService())
        _service_manager.register_service("database", DatabaseConnectionService())

    return _service_manager


def get_service(name: str) -> Optional[BaseService]:
    """Quick access to services"""
    return get_service_manager().get_service(name)


# ===== CONVENIENCE FUNCTIONS =====
def init_services(config: Dict[str, Any] = None) -> Dict[str, bool]:
    """Initialize all services with config"""
    manager = get_service_manager()
    return manager.initialize_all()


def get_excel_service() -> ExcelProcessingService:
    """Get Excel service"""
    return get_service("excel")


def get_mock_service() -> MockDataService:
    """Get Mock data service"""
    return get_service("mock")


def get_database_service() -> DatabaseConnectionService:
    """Get Database service"""
    return get_service("database")
