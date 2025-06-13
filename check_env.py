import os
import sys
import subprocess
from pathlib import Path


def check_tcl():
    """Check Tcl/Tk installation"""
    try:
        import tkinter

        root = tkinter.Tk()
        root.destroy()
        return True
    except Exception as e:
        print(f"❌ Tkinter error: {e}")
        return False


def setup_tcl():
    """Setup Tcl environment"""
    python_dir = Path(sys.executable).parent
    tcl_paths = [
        python_dir / "tcl" / "tcl8.6",
        python_dir / "Lib" / "tcl8.6",
        Path("C:/") / "Program Files" / "Python311" / "tcl" / "tcl8.6",
    ]

    for tcl_path in tcl_paths:
        if tcl_path.exists():
            os.environ["TCL_LIBRARY"] = str(tcl_path)
            tk_path = tcl_path.parent / "tk8.6"
            if tk_path.exists():
                os.environ["TK_LIBRARY"] = str(tk_path)
                return True

    return False


def main():
    """Main environment check"""
    if not check_tcl():
        if not setup_tcl():
            print("❌ Tcl/Tk not properly installed")
            print("Please reinstall Python with Tcl/Tk support")
            sys.exit(1)

    print("✅ Environment check passed")


if __name__ == "__main__":
    main()
