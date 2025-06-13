"""
Tkinter wrapper with environment fix
"""
import os
import sys
from pathlib import Path

def setup_tkinter_environment():
    """Setup Tcl/Tk environment before importing tkinter"""
    
    # Python installation path  
    python_path = Path(sys.executable).parent.parent
    
    # Set TCL/TK paths
    tcl_paths = [
        python_path / "tcl" / "tcl8.6",
        python_path / "lib" / "tcl8.6",
        Path("C:/Python313/tcl/tcl8.6")
    ]
    
    tk_paths = [
        python_path / "tcl" / "tk8.6", 
        python_path / "lib" / "tk8.6",
        Path("C:/Python313/tcl/tk8.6")
    ]
    
    for path in tcl_paths:
        if path.exists():
            os.environ["TCL_LIBRARY"] = str(path)
            break
    
    for path in tk_paths:
        if path.exists():
            os.environ["TK_LIBRARY"] = str(path)
            break

# Setup environment before importing
setup_tkinter_environment()

# Now import tkinter
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
    
    # Test basic functionality
    def test_tkinter():
        root = tk.Tk()
        root.withdraw()
        root.destroy()
        return True
    
    TKINTER_AVAILABLE = True
    
except Exception as e:
    print(f"Tkinter still not available: {e}")
    TKINTER_AVAILABLE = False
    
    # Create dummy classes
    class DummyTk:
        def __init__(self): pass
        def withdraw(self): pass
        def destroy(self): pass
        def quit(self): pass
        def mainloop(self): pass
    
    tk = type('module', (), {'Tk': DummyTk})
    ttk = type('module', (), {})
    messagebox = type('module', (), {})
    filedialog = type('module', (), {})
