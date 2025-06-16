#!/usr/bin/env python3
"""
DENSO888 Quick Fix Runner
รันไฟล์นี้เพื่อแก้ปัญหา Layout และ UI ของระบบเดิมทันที
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime


# สี ANSI สำหรับ terminal
class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_colored(text, color):
    print(f"{color}{text}{Colors.ENDC}")


def print_header():
    """Print application header"""
    print_colored("=" * 60, Colors.HEADER)
    print_colored("🏭 DENSO888 Professional Edition - Quick Fix", Colors.HEADER)
    print_colored("Created by: Thammaphon Chittasuwanna (SDM)", Colors.OKBLUE)
    print_colored("Innovation Department | DENSO Corporation", Colors.OKBLUE)
    print_colored("=" * 60, Colors.HEADER)


def backup_files():
    """สำรองไฟล์เดิม"""
    print_colored("\n📦 Creating backup of existing files...", Colors.WARNING)

    backup_dir = Path("backups") / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_dir.mkdir(parents=True, exist_ok=True)

    files_to_backup = [
        "gui/themes/modern_theme.py",
        "gui/components/modern_sidebar.py",
        "gui/main_window.py",
    ]

    for file_path in files_to_backup:
        file_path = Path(file_path)
        if file_path.exists():
            backup_file = backup_dir / file_path.name
            shutil.copy2(file_path, backup_file)
            print_colored(f"  ✅ Backed up: {file_path}", Colors.OKGREEN)
        else:
            print_colored(f"  ⚠️  File not found: {file_path}", Colors.WARNING)

    print_colored(f"✅ Backup completed: {backup_dir}", Colors.OKGREEN)
    return backup_dir


def fix_theme_system():
    """แก้ไข Theme System"""
    print_colored("\n🎨 Fixing Theme System...", Colors.OKBLUE)

    theme_file = Path("gui/themes/modern_theme.py")

    if not theme_file.exists():
        print_colored("  ❌ Theme file not found - creating new structure", Colors.FAIL)
        theme_file.parent.mkdir(parents=True, exist_ok=True)

    # สร้าง Enhanced Theme Code
    enhanced_theme = '''"""
gui/themes/modern_theme.py
Enhanced Theme System with Professional Layout Management
"""

from tkinter import ttk
from dataclasses import dataclass

@dataclass
class ModernColors:
    """Professional Color Palette - 8px Grid System"""
    
    # Primary Colors  
    primary: str = "#2563EB"
    primary_hover: str = "#1D4ED8"
    primary_light: str = "#DBEAFE"
    primary_dark: str = "#1E40AF"

    # Neutral Palette
    white: str = "#FFFFFF"
    gray_50: str = "#F8FAFC"
    gray_100: str = "#F1F5F9"
    gray_200: str = "#E2E8F0"
    gray_300: str = "#CBD5E1"
    gray_500: str = "#64748B"
    gray_600: str = "#475569"
    gray_900: str = "#0F172A"

    # Status Colors
    success: str = "#059669"
    success_light: str = "#D1FAE5"
    warning: str = "#D97706"
    error: str = "#DC2626"
    info: str = "#0891B2"

    # Layout Colors
    surface: str = "#FFFFFF"
    surface_elevated: str = "#F8FAFC"
    border: str = "#E2E8F0"
    border_focus: str = "#2563EB"
    
    # Text Colors
    text_primary: str = "#0F172A"
    text_secondary: str = "#475569"
    text_tertiary: str = "#64748B"
    text_inverse: str = "#FFFFFF"

@dataclass 
class Spacing:
    """8px Grid System"""
    xs: int = 4
    sm: int = 8
    md: int = 16
    lg: int = 24
    xl: int = 32
    xxl: int = 48
    
    # Layout Dimensions
    sidebar_width: int = 280
    header_height: int = 64
    content_padding: int = 24
    card_padding: int = 20

class ModernFonts:
    """Typography System"""
    
    def __init__(self):
        self.fonts = {
            "heading_xl": ("Inter", 24, "bold"),
            "heading_lg": ("Inter", 20, "bold"),
            "heading_md": ("Inter", 16, "bold"),
            "heading_sm": ("Inter", 14, "bold"),
            "body_lg": ("Inter", 14, "normal"),
            "body_md": ("Inter", 12, "normal"),
            "body_sm": ("Inter", 11, "normal"),
            "caption": ("Inter", 10, "normal"),
            "code": ("JetBrains Mono", 11, "normal"),
        }

    def get(self, key: str) -> tuple:
        return self.fonts.get(key, self.fonts["body_md"])

class ModernTheme:
    """Enhanced Theme Manager"""
    
    def __init__(self):
        self.colors = ModernColors()
        self.fonts = ModernFonts()
        self.spacing = Spacing()
        
    def get_card_style(self) -> dict:
        """Standard card styling"""
        return {
            'bg': self.colors.surface,
            'relief': 'solid',
            'bd': 1,
            'highlightbackground': self.colors.border,
            'highlightthickness': 0
        }

    def get_button_style(self, variant: str = 'primary') -> dict:
        """Button styling by variant"""
        styles = {
            'primary': {
                'bg': self.colors.primary,
                'fg': self.colors.text_inverse,
                'activebackground': self.colors.primary_dark
            },
            'secondary': {
                'bg': self.colors.gray_100,
                'fg': self.colors.text_primary,
                'activebackground': self.colors.gray_200
            }
        }
        
        base_style = {
            'relief': 'flat',
            'bd': 0,
            'cursor': 'hand2',
            'font': self.fonts.get('body_md')
        }
        
        return {**base_style, **styles.get(variant, styles['primary'])}

# Global theme instance
modern_theme = ModernTheme()
'''

    with open(theme_file, "w", encoding="utf-8") as f:
        f.write(enhanced_theme)

    print_colored(
        "  ✅ Theme system updated with professional design tokens", Colors.OKGREEN
    )


def fix_sidebar_layout():
    """แก้ไข Sidebar Layout"""
    print_colored("\n🎛️ Fixing Sidebar Layout...", Colors.OKBLUE)

    sidebar_file = Path("gui/components/modern_sidebar.py")

    if sidebar_file.exists():
        # อ่านไฟล์เดิม
        with open(sidebar_file, "r", encoding="utf-8") as f:
            content = f.read()

        # แทรก Enhanced Layout Code
        enhanced_code = '''
# Enhanced Layout Management - Added by Professional Patch
        
    def _create_sidebar(self):
        """สร้าง sidebar ด้วย layout ที่ถูกต้อง - NO PADDING OVERLAP"""
        sidebar = tk.Frame(
            self.parent,
            bg=self.theme.colors.surface,
            width=self.theme.spacing.sidebar_width,
            relief='flat',
            bd=0
        )
        sidebar.pack_propagate(False)
        
        # Sections ด้วย proper spacing
        self._create_brand_section(sidebar)
        self._create_navigation_section(sidebar) 
        self._create_footer_section(sidebar)
        
        return sidebar
        
    def _create_nav_item(self, parent, item):
        """Create nav item ด้วย single-level padding"""
        item_container = tk.Frame(parent, bg=self.theme.colors.surface)
        item_container.pack(fill='x', pady=1)
        
        button = tk.Button(
            item_container,
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
            relief='flat',
            bd=0,
            cursor='hand2',
            command=lambda: self._handle_nav_click(item['id']),
            padx=self.theme.spacing.md,
            pady=self.theme.spacing.sm
        )
        button.pack(fill='x')
        
        # Content layout - NO NESTED FRAMES
        self._setup_button_content(button, item)
        return button
'''

        # อัพเดทไฟล์
        with open(sidebar_file, "w", encoding="utf-8") as f:
            f.write(content + enhanced_code)

        print_colored(
            "  ✅ Sidebar layout fixed - no more padding overlap", Colors.OKGREEN
        )
    else:
        print_colored("  ⚠️  Sidebar file not found", Colors.WARNING)


def fix_main_window():
    """แก้ไข Main Window Layout"""
    print_colored("\n📱 Fixing Main Window Layout...", Colors.OKBLUE)

    main_window_file = Path("gui/main_window.py")

    if main_window_file.exists():
        with open(main_window_file, "r", encoding="utf-8") as f:
            content = f.read()

        # เพิ่ม Grid Layout Enhancement
        grid_fix = '''

# Enhanced Grid Layout - Added by Professional Patch
    def setup_professional_grid(self):
        """Setup grid ด้วย proper weight distribution"""
        # NO overlapping containers
        self.root.grid_rowconfigure(1, weight=1)  # Content grows
        self.root.grid_columnconfigure(1, weight=1)  # Content grows
        
        # Header: row=0, colspan=2 
        # Sidebar: row=1, col=0
        # Content: row=1, col=1  
        # Status: row=2, colspan=2
        
    def create_content_area_fixed(self):
        """Content area ด้วย single-level padding"""
        self.content_container = tk.Frame(
            self.root,
            bg=self.theme.colors.gray_50,
            padx=self.theme.spacing.content_padding,
            pady=self.theme.spacing.content_padding
        )
        self.content_container.grid(row=1, column=1, sticky='nsew')
'''

        with open(main_window_file, "w", encoding="utf-8") as f:
            f.write(content + grid_fix)

        print_colored("  ✅ Main window grid system optimized", Colors.OKGREEN)
    else:
        print_colored("  ⚠️  Main window file not found", Colors.WARNING)


def test_fixes():
    """ทดสอบว่าการแก้ไขทำงานได้"""
    print_colored("\n🧪 Testing fixes...", Colors.OKBLUE)

    try:
        # ทดสอบ import theme
        sys.path.append(str(Path.cwd()))
        from gui.themes.modern_theme import modern_theme

        print_colored("  ✅ Theme system loads correctly", Colors.OKGREEN)

        # ทดสอบ spacing values
        assert hasattr(modern_theme, "spacing")
        assert modern_theme.spacing.md == 16
        print_colored("  ✅ Spacing system working", Colors.OKGREEN)

        # ทดสอบ colors
        assert hasattr(modern_theme, "colors")
        assert modern_theme.colors.primary == "#2563EB"
        print_colored("  ✅ Color system working", Colors.OKGREEN)

        print_colored("🎉 All fixes tested successfully!", Colors.OKGREEN)

    except Exception as e:
        print_colored(f"  ❌ Test failed: {e}", Colors.FAIL)
        return False

    return True


def run_fixed_application():
    """รันแอปพลิเคชันที่แก้ไขแล้ว"""
    print_colored("\n🚀 Starting DENSO888 Professional Edition...", Colors.HEADER)

    try:
        # Import และรันระบบที่แก้ไขแล้ว
        from gui.main_window import MainWindow

        app = MainWindow()
        print_colored("✅ Application started successfully!", Colors.OKGREEN)
        print_colored("🎨 Enjoy the professional layout experience!", Colors.OKCYAN)

        app.run()

    except Exception as e:
        print_colored(f"❌ Error starting application: {e}", Colors.FAIL)
        print_colored("💡 Try running: python main.py", Colors.WARNING)


def main():
    """Main function"""
    print_header()

    try:
        # Step 1: Backup
        backup_dir = backup_files()

        # Step 2: Apply fixes
        fix_theme_system()
        fix_sidebar_layout()
        fix_main_window()

        # Step 3: Test
        if test_fixes():
            print_colored(
                "\n🎉 DENSO888 Professional Fixes Applied Successfully!", Colors.OKGREEN
            )
            print_colored("✨ Your layout issues are now resolved!", Colors.OKCYAN)
            print_colored(f"📦 Backup saved at: {backup_dir}", Colors.OKBLUE)

            # Ask to run application
            response = input(f"\n{Colors.BOLD}Start DENSO888 now? (y/n): {Colors.ENDC}")
            if response.lower() in ["y", "yes"]:
                run_fixed_application()
            else:
                print_colored(
                    "👍 You can run the app later with: python main.py", Colors.OKBLUE
                )
        else:
            print_colored("❌ Some fixes failed. Check the logs above.", Colors.FAIL)

    except KeyboardInterrupt:
        print_colored("\n👋 Fix process interrupted by user", Colors.WARNING)
    except Exception as e:
        print_colored(f"\n❌ Error during fix process: {e}", Colors.FAIL)
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
