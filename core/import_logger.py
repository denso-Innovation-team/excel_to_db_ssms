"""
core/import_logger.py
Import Operation Logging System
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class ImportLogger:
    """Logger for import operations"""

    def __init__(self, log_file: str = "logs/import_history.json"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(exist_ok=True)

    def log_import(
        self,
        excel_file: str,
        database: str,
        table: str,
        records_count: int,
        field_mappings: Dict[str, Any],
        status: str,
        error_message: str = None,
    ):
        """Log import operation"""

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "excel_file": excel_file,
            "database": database,
            "table": table,
            "records_count": records_count,
            "field_mappings": field_mappings,
            "status": status,
            "error_message": error_message,
            "duration": None,  # Could be calculated
        }

        # Read existing logs
        logs = self._read_logs()
        logs.append(log_entry)

        # Keep only last 1000 entries
        logs = logs[-1000:]

        # Save logs
        self._write_logs(logs)

    def get_import_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get import history"""
        logs = self._read_logs()
        return logs[-limit:]

    def get_statistics(self) -> Dict[str, Any]:
        """Get import statistics"""
        logs = self._read_logs()

        if not logs:
            return {"total_imports": 0, "successful_imports": 0, "failed_imports": 0}

        successful = len([log for log in logs if log.get("status") == "success"])
        failed = len([log for log in logs if log.get("status") == "failed"])

        return {
            "total_imports": len(logs),
            "successful_imports": successful,
            "failed_imports": failed,
            "success_rate": (successful / len(logs)) * 100 if logs else 0,
            "total_records": sum(log.get("records_count", 0) for log in logs),
        }

    def _read_logs(self) -> List[Dict[str, Any]]:
        """Read logs from file"""
        if not self.log_file.exists():
            return []

        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to read import logs: {e}")
            return []

    def _write_logs(self, logs: List[Dict[str, Any]]):
        """Write logs to file"""
        try:
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to write import logs: {e}")
