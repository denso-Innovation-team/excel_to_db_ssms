#!/usr/bin/env python3
"""Quick install script for DENSO888"""

import subprocess
import sys
import os

def main():
    print("🏭 Installing DENSO888 Dependencies...")
    
    try:
        # Upgrade pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("✅ Installation completed successfully!")
        print("\nRun: python main.py")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
