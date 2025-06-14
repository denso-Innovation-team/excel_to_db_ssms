#!/usr/bin/env python3
"""
main_modern.py
DENSO888 Modern Edition - Main Entry Point
Created by: Thammaphon Chittasuwanna (SDM) | Innovation
"""

import sys
import os
from pathlib import Path
import argparse

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Core imports
from config.settings import get_config
from utils.logger import setup_logger
from gui.windows.modern_main_window import ModernDENSO888MainWindow

# Setup logging
logger = setup_logger("denso888")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="DENSO888 Modern Edition")
    parser.add_argument("--theme", default="denso_corporate", 
                       help="UI theme (denso_corporate, dark_premium, ocean_blue)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        config = get_config()
        
        # Apply debug settings
        if args.debug:
            logger.setLevel("DEBUG")
            logger.debug("Debug mode enabled")
        
        # Log startup
        logger.info(f"🏭 Starting DENSO888 {config.version}")
        logger.info(f"Created by: {config.author}")
        
        # Create and run application
        app = ModernDENSO888MainWindow(config)
        app.theme_manager.apply_theme(args.theme, app.root)
        
        logger.info("Application started successfully")
        app.run()
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application startup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
