import os
import sys
import subprocess
from pathlib import Path


def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]
        )
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        return False


def check_tcl_tk():
    """Verify Tcl/Tk installation"""
    try:
        import tkinter

        root = tkinter.Tk()
        root.destroy()
        return True
    except Exception:
        return False


def main():
    print("Setting up DENSO888 environment...")

    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements")
        sys.exit(1)

    # Check Tcl/Tk
    if not check_tcl_tk():
        print("❌ Tcl/Tk not properly installed")
        print("Please install Python with Tcl/Tk support")
        sys.exit(1)

    print("✅ Setup completed successfully!")


if __name__ == "__main__":
    main()
