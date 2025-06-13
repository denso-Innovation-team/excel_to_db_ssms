#!/usr/bin/env python3
"""
DENSO888 Quick Setup Script - Python 3.6+ Compatible
เสียงง่ายรวดเร็ว ไม่มี error!
"""

import shutil
import json
from pathlib import Path


def create_modern_structure():
    """สร้างโครงสร้าง modern อย่างง่าย"""
    print("🏭 DENSO888 Quick Setup")
    print("=" * 40)

    # โครงสร้างพื้นฐาน
    dirs = [
        "denso888-modern/config",
        "denso888-modern/core",
        "denso888-modern/core/analytics",
        "denso888-modern/gui",
        "denso888-modern/gui/components",
        "denso888-modern/gui/themes",
        "denso888-modern/gui/windows",
        "denso888-modern/security",
        "denso888-modern/utils",
        "denso888-modern/automation",
        "denso888-modern/plugins",
        "denso888-modern/tests",
        "denso888-modern/docs",
        "denso888-modern/assets/themes",
        "denso888-modern/assets/images",
        "denso888-modern/logs",
        "denso888-modern/data",
    ]

    # สร้าง directories
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

        # สร้าง __init__.py สำหรับ Python packages
        if any(
            x in dir_path
            for x in [
                "config",
                "core",
                "gui",
                "security",
                "utils",
                "automation",
                "plugins",
            ]
        ):
            init_file = Path(dir_path) / "__init__.py"
            if not init_file.exists():
                init_file.write_text('"""DENSO888 Package"""\n')

    print(f"✅ Created {len(dirs)} directories")

    # Copy existing files
    copy_files()

    # สร้างไฟล์ template
    create_essential_files()

    print("\n🎉 Setup Complete!")
    print(f"📁 Project: denso888-modern/")
    print("🚀 Run: cd denso888-modern && python main_modern.py")


def copy_files():
    """Copy existing files safely"""
    print("📋 Copying existing files...")

    files_to_copy = [
        ("requirements.txt", "denso888-modern/requirements.txt"),
        (".env.example", "denso888-modern/.env.example"),
        (".gitignore", "denso888-modern/.gitignore"),
        ("main.py", "denso888-modern/main_legacy.py"),  # Keep as legacy
    ]

    # Copy directories
    dirs_to_copy = [
        ("config", "denso888-modern/config"),
        ("core", "denso888-modern/core"),
        ("gui", "denso888-modern/gui/legacy"),  # Keep legacy GUI
        ("utils", "denso888-modern/utils"),
    ]

    # Copy files
    for src, dst in files_to_copy:
        if Path(src).exists():
            try:
                shutil.copy2(src, dst)
                print(f"   📄 {src} → {dst}")
            except Exception as e:
                print(f"   ⚠️ Skip {src}: {e}")

    # Copy directories
    for src, dst in dirs_to_copy:
        if Path(src).exists():
            try:
                if Path(dst).exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
                print(f"   📁 {src}/ → {dst}/")
            except Exception as e:
                print(f"   ⚠️ Skip {src}/: {e}")


def create_essential_files():
    """สร้างไฟล์สำคัญ"""
    print("📝 Creating essential files...")

    # Main modern entry point
    main_modern = '''#!/usr/bin/env python3
"""
DENSO888 Modern Edition
Created by Thammaphon Chittasuwanna (SDM) | Innovation
"""

import sys
import tkinter as tk
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Modern DENSO888 Application"""
    print("🏭 DENSO888 Modern Edition")
    print("   by Thammaphon Chittasuwanna (SDM) | Innovation")
    
    try:
        # Try to import modern components
        try:
            from gui.windows.main_window import ModernDENSO888MainWindow
            from gui.themes.theme_manager import ModernThemeManager
            
            # Create modern app
            theme_manager = ModernThemeManager()
            app = ModernDENSO888MainWindow(theme_manager=theme_manager)
            return app.run()
            
        except ImportError as e:
            print(f"⚠️ Modern components not ready: {e}")
            print("🔄 Falling back to legacy mode...")
            
            # Fallback to legacy
            try:
                from gui.legacy.main_window import DENSO888MainWindow
                app = DENSO888MainWindow()
                app.run()
                return 0
            except ImportError:
                print("❌ Legacy components also missing")
                return 1
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
'''

    # Theme manager
    theme_manager = '''"""
Modern Theme Manager for DENSO888
"""

import tkinter as tk
from tkinter import ttk

class ModernThemeManager:
    """Simple theme manager"""
    
    def __init__(self):
        self.current_theme = "denso_corporate"
        self.themes = {
            "denso_corporate": {
                "primary": "#DC0003",
                "secondary": "#2C3E50", 
                "background": "#FFFFFF",
                "surface": "#F8F9FA",
                "text_primary": "#2C3E50"
            }
        }
    
    def get_theme(self, name=None):
        """Get theme colors"""
        theme_name = name or self.current_theme
        return type('Theme', (), self.themes.get(theme_name, self.themes["denso_corporate"]))()
    
    def apply_theme(self, root, theme_name):
        """Apply theme to tkinter app"""
        theme = self.get_theme(theme_name)
        root.configure(bg=theme.background)
        return True
'''

    # Modern main window (placeholder)
    main_window = '''"""
Modern Main Window for DENSO888
"""

import tkinter as tk
from tkinter import ttk, messagebox

class ModernDENSO888MainWindow:
    """Modern main window with enhanced UI"""
    
    def __init__(self, theme_manager=None):
        self.theme_manager = theme_manager
        self.root = tk.Tk()
        self._setup_window()
        self._create_ui()
    
    def _setup_window(self):
        """Setup main window"""
        self.root.title("🏭 DENSO888 Modern Edition")
        self.root.geometry("1200x800")
        
        if self.theme_manager:
            self.theme_manager.apply_theme(self.root, "denso_corporate")
    
    def _create_ui(self):
        """Create modern UI"""
        # Header
        header = tk.Frame(self.root, bg="#DC0003", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        title_label = tk.Label(header, 
                              text="🏭 DENSO888 Modern Edition",
                              bg="#DC0003", fg="white",
                              font=("Segoe UI", 16, "bold"))
        title_label.pack(expand=True)
        
        # Content
        content = tk.Frame(self.root, bg="#F8F9FA")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Welcome message
        welcome = tk.Label(content,
                          text="Welcome to DENSO888 Modern Edition!\\n\\nThis is the new modern interface.\\nLegacy features are still available.",
                          bg="#F8F9FA", fg="#2C3E50",
                          font=("Segoe UI", 12),
                          justify="center")
        welcome.pack(expand=True)
        
        # Buttons
        btn_frame = tk.Frame(content, bg="#F8F9FA")
        btn_frame.pack(pady=20)
        
        modern_btn = tk.Button(btn_frame,
                              text="🚀 Modern Features",
                              bg="#DC0003", fg="white",
                              font=("Segoe UI", 10, "bold"),
                              padx=20, pady=10,
                              command=self._show_modern_features)
        modern_btn.pack(side="left", padx=10)
        
        legacy_btn = tk.Button(btn_frame,
                              text="🔄 Legacy Mode", 
                              bg="#2C3E50", fg="white",
                              font=("Segoe UI", 10),
                              padx=20, pady=10,
                              command=self._show_legacy_mode)
        legacy_btn.pack(side="left", padx=10)
        
        # Footer
        footer = tk.Label(self.root,
                         text="Created by Thammaphon Chittasuwanna (SDM) | Innovation",
                         bg="#F8F9FA", fg="#7F8C8D",
                         font=("Segoe UI", 9))
        footer.pack(side="bottom", pady=10)
    
    def _show_modern_features(self):
        """Show modern features info"""
        features = """🎨 Modern Features Available:
        
• Advanced Theme System
• Real-time Dashboard 
• AI-Powered Analytics
• Enhanced Security
• Automation Workflows
• Interactive Visualizations

🚧 Status: Under Development
Some features may not be fully implemented yet."""
        
        messagebox.showinfo("Modern Features", features)
    
    def _show_legacy_mode(self):
        """Switch to legacy mode"""
        result = messagebox.askyesno("Legacy Mode", 
                                   "Switch to legacy DENSO888 interface?\\n\\nThis will close the modern interface.")
        if result:
            self.root.destroy()
            # Here you could launch legacy app
            print("🔄 Switching to legacy mode...")
    
    def run(self):
        """Run the application"""
        print("🖥️ Starting Modern DENSO888...")
        self.root.mainloop()
        return 0
'''

    # README
    readme = """# 🏭 DENSO888 Modern Edition

**Excel to SQL Management System**

Created by **Thammaphon Chittasuwanna (SDM) | Innovation**

## 🚀 Quick Start

```bash
# Navigate to project
cd denso888-modern

# Install dependencies  
pip install -r requirements.txt

# Run modern application
python main_modern.py

# Or run legacy version
python main_legacy.py
```

## 📁 Project Structure

- `main_modern.py` - Modern application entry
- `main_legacy.py` - Legacy application (migrated)
- `gui/windows/` - Modern UI components
- `gui/legacy/` - Legacy UI components
- `core/` - Business logic
- `config/` - Configuration

## 🎯 Features

- ✨ Modern UI with themes
- 📊 Advanced analytics
- 🔐 Enhanced security  
- 🔄 Legacy compatibility

## 👨‍💻 Creator

**Thammaphon Chittasuwanna**  
SDM | Innovation | DENSO  
เฮียตอมจัดหั้ย!!! 🚀
"""

    # เขียนไฟล์
    files_to_create = {
        "denso888-modern/main_modern.py": main_modern,
        "denso888-modern/gui/themes/theme_manager.py": theme_manager,
        "denso888-modern/gui/windows/main_window.py": main_window,
        "denso888-modern/README.md": readme,
    }

    for file_path, content in files_to_create.items():
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        Path(file_path).write_text(content, encoding="utf-8")
        print(f"   📄 Created {file_path}")

    # สร้าง theme files
    theme_data = {
        "name": "DENSO Corporate",
        "primary": "#DC0003",
        "secondary": "#2C3E50",
        "background": "#FFFFFF",
        "surface": "#F8F9FA",
        "text_primary": "#2C3E50",
    }

    theme_file = Path("denso888-modern/assets/themes/denso_corporate.json")
    theme_file.write_text(json.dumps(theme_data, indent=2), encoding="utf-8")
    print(f"   🎨 Created theme file")


if __name__ == "__main__":
    create_modern_structure()
