import threading
from pathlib import Path
import shutil
from datetime import datetime
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class BackupService:
    """Automatic backup service"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
        self._stop_event = threading.Event()
        self._backup_thread: Optional[threading.Thread] = None

    def start(self):
        """Start backup service"""
        if not self._backup_thread or not self._backup_thread.is_alive():
            self._stop_event.clear()
            self._backup_thread = threading.Thread(
                target=self._backup_loop, daemon=True
            )
            self._backup_thread.start()
            logger.info("Backup service started")

    def stop(self):
        """Stop backup service"""
        if self._backup_thread and self._backup_thread.is_alive():
            self._stop_event.set()
            self._backup_thread.join(timeout=5)
            logger.info("Backup service stopped")

    def _backup_loop(self):
        """Main backup loop"""
        interval = self.config.get("backup_interval", 60)  # minutes

        while not self._stop_event.is_set():
            try:
                self._perform_backup()
            except Exception as e:
                logger.error(f"Backup error: {e}")

            # Wait for next backup or stop
            self._stop_event.wait(timeout=interval * 60)

    def _perform_backup(self):
        """Perform backup operation"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Backup database
        db_file = Path("data/denso888.db")
        if db_file.exists():
            backup_path = self.backup_dir / f"denso888_{timestamp}.db"
            shutil.copy2(db_file, backup_path)
            logger.info(f"Database backed up to {backup_path}")

        # Backup config
        config_dir = Path("config")
        if config_dir.exists():
            backup_config = self.backup_dir / f"config_{timestamp}"
            shutil.copytree(config_dir, backup_config, dirs_exist_ok=True)
            logger.info(f"Config backed up to {backup_config}")

        # Cleanup old backups
        self._cleanup_old_backups()

    def _cleanup_old_backups(self):
        """Clean up old backup files"""
        keep_days = self.config.get("keep_backups_days", 7)
        cutoff = datetime.now().timestamp() - (keep_days * 24 * 60 * 60)

        for file in self.backup_dir.glob("*"):
            if file.stat().st_mtime < cutoff:
                try:
                    if file.is_file():
                        file.unlink()
                    elif file.is_dir():
                        shutil.rmtree(file)
                except Exception as e:
                    logger.error(f"Cleanup error for {file}: {e}")
