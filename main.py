"""
main.py
Enhanced Excel to Database Pool System Entry Point
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from gui.enhanced_main_window import EnhancedMainWindow
from controllers.pool_controller import PoolController
from services.connection_pool_service import ConnectionPoolService
from utils.logger import setup_logger


def main():
    """เริ่มต้นระบบ Excel to Database Pool"""
    try:
        # Setup logging
        logger = setup_logger("excel_db_pool", "INFO")
        logger.info("🚀 Starting Excel to Database Pool System...")

        # Initialize services
        pool_service = ConnectionPoolService()
        controller = PoolController(pool_service)

        # Create and run main window
        app = EnhancedMainWindow(controller)
        app.run()

    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
