import os
import sys
import subprocess
from pathlib import Path

WHEELS = {
    "numpy": "numpy-1.24.3-cp311-cp311-win_amd64.whl",
    "pandas": "pandas-1.5.3-cp311-cp311-win_amd64.whl",
}


def install_wheel(wheel_name, wheel_file):
    """Install a specific wheel file"""
    wheel_url = f"https://download.lfd.uci.edu/pythonlibs/archived/{wheel_file}"
    try:
        # Download wheel
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "download",
                "--no-deps",
                "--dest",
                "wheels",
                wheel_url,
            ]
        )

        # Install wheel
        wheel_path = Path("wheels") / wheel_file
        if wheel_path.exists():
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", str(wheel_path)]
            )
            return True
    except Exception as e:
        print(f"Failed to install {wheel_name}: {e}")
        return False


def main():
    """Main installation function"""
    print("Installing dependencies...")

    # Create wheels directory
    Path("wheels").mkdir(exist_ok=True)

    # Upgrade pip
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

    # Install wheels first
    for wheel_name, wheel_file in WHEELS.items():
        if not install_wheel(wheel_name, wheel_file):
            print(f"❌ Failed to install {wheel_name}")
            sys.exit(1)

    # Install remaining requirements
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("✅ Dependencies installed successfully!")
    except Exception as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
