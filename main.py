#!/usr/bin/env python3
"""
DENSO888 - Unified Entry Point
Created by Thammaphon Chittasuwanna (SDM) | Innovation

Single entry point with multiple UI modes
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="DENSO888 Excel to SQL System")
    parser.add_argument("--ui", choices=["modern", "classic", "auto"], 
                       default="auto", help="UI mode")
    parser.add_argument("--version", action="version", version="DENSO888 2.0.0")
    
    args = parser.parse_args()
    
    print("🏭 DENSO888 - Excel to SQL Management System")
    print("   by Thammaphon Chittasuwanna (SDM) | Innovation")
    print(f"   UI Mode: {args.ui}")
    print("=" * 50)
    
    try:
        # Setup logging
        from utils.logger import setup_logger
        logger = setup_logger()
        logger.info(f"Starting DENSO888 in {args.ui} mode")
        
        # Load configuration
        from config.settings import get_config
        config = get_config()
        
        # Create and run GUI
        from gui.app_factory import AppFactory
        app = AppFactory.create_app(mode=args.ui, config=config)
        
        return app.run()
        
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
