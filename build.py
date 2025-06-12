import os
import sys
import shutil
import subprocess
from pathlib import Path
import json
from typing import List, Dict, Any


class DENSO888Builder:
    """Build automation for DENSO888 application"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"
        self.assets_dir = self.project_root / "assets"

        # Build configuration
        self.build_config = {
            "app_name": "DENSO888_ExcelToSQL",
            "main_script": "main.py",
            "icon_file": "assets/icons/denso_icon.ico",
            "hidden_imports": [
                "pandas",
                "sqlalchemy",
                "pyodbc",
                "openpyxl",
                "tqdm",
                "PIL",
                "tkinter",
                "tkinter.ttk",
                "tkinter.filedialog",
                "tkinter.messagebox",
                "tkinter.scrolledtext",
                "sqlite3",
                "dotenv",
            ],
            "data_files": [
                ("assets", "assets"),
                ("config", "config"),
                (".env.example", "."),
            ],
            "exclude_modules": ["matplotlib", "numpy.random._examples", "tcl", "tk"],
        }

    def check_requirements(self) -> bool:
        """Check build requirements"""
        print("🔍 Checking build requirements...")

        required_packages = [
            "pyinstaller",
            "pandas",
            "sqlalchemy",
            "pyodbc",
            "openpyxl",
            "pillow",
            "python-dotenv",
            "tqdm",
        ]

        missing = []
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
                print(f"  ✅ {package}")
            except ImportError:
                missing.append(package)
                print(f"  ❌ {package} - ไม่พบ")

        if missing:
            print(f"\n⚠️ ต้องติดตั้ง packages ที่ขาดหายไป:")
            print(f"pip install {' '.join(missing)}")
            return False

        print("✅ Dependencies ครบถ้วน!\n")
        return True

    def prepare_build_environment(self) -> bool:
        """Prepare build environment"""
        print("📁 เตรียมสภาพแวดล้อมการ build...")

        try:
            # Create build directories
            self.dist_dir.mkdir(exist_ok=True)
            self.build_dir.mkdir(exist_ok=True)

            # Ensure assets exist
            self.assets_dir.mkdir(exist_ok=True)
            (self.assets_dir / "icons").mkdir(exist_ok=True)
            (self.assets_dir / "samples").mkdir(exist_ok=True)

            # Create icon if not exists
            self._create_default_icon()

            # Validate main script
            main_script = self.project_root / self.build_config["main_script"]
            if not main_script.exists():
                print(f"❌ ไม่พบไฟล์หลัก: {main_script}")
                return False

            print("✅ สภาพแวดล้อมพร้อม!\n")
            return True

        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการเตรียมสภาพแวดล้อม: {e}")
            return False

    def _create_default_icon(self):
        """Create default icon if not exists"""
        icon_path = self.assets_dir / "icons" / "denso_icon.ico"

        if icon_path.exists():
            return

        try:
            from PIL import Image, ImageDraw, ImageFont

            # Create 256x256 icon
            img = Image.new("RGB", (256, 256), "#DC0003")  # #DC0003 in RGB values
            draw = ImageDraw.Draw(img)

            # Draw text
            try:
                font = ImageFont.truetype("arial.ttf", 60)
            except:
                font = ImageFont.load_default()

            text = "D888"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            x = (256 - text_width) // 2
            y = (256 - text_height) // 2

            draw.text((x, y), text, fill="white", font=font)

            # Save as ICO with multiple sizes
            img.save(
                icon_path,
                format="ICO",
                sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)],
            )

            print(f"  📝 สร้าง icon: {icon_path}")

        except Exception as e:
            print(f"  ⚠️ ไม่สามารถสร้าง icon: {e}")

    def create_spec_file(self) -> Path:
        """Create PyInstaller spec file"""
        print("📄 สร้างไฟล์ .spec...")

        spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

block_cipher = None

# Project paths
project_root = Path(__file__).parent

a = Analysis(
    ['{self.build_config["main_script"]}'],
    pathex=[str(project_root)],
    binaries=[],
    datas={self.build_config["data_files"]},
    hiddenimports={self.build_config["hidden_imports"]},
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes={self.build_config["exclude_modules"]},
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{self.build_config["app_name"]}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI Application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='{self.build_config["icon_file"]}' if Path('{self.build_config["icon_file"]}').exists() else None
)
"""

        spec_file = self.project_root / f"{self.build_config['app_name']}.spec"

        with open(spec_file, "w", encoding="utf-8") as f:
            f.write(spec_content)

        print(f"  ✅ {spec_file.name}")
        return spec_file

    def build_executable(self, spec_file: Path) -> bool:
        """Build executable using PyInstaller"""
        print("🚀 เริ่มสร้าง .exe...")
        print("   (อาจใช้เวลาหลายนาที กรุณารอสักครู่...)\n")

        try:
            cmd = [
                sys.executable,
                "-m",
                "PyInstaller",
                "--clean",
                "--noconfirm",
                str(spec_file),
            ]

            print(f"🔧 รันคำสั่ง: {' '.join(cmd)}")

            # Run PyInstaller
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            if result.returncode == 0:
                print("✅ สร้าง .exe สำเร็จ!")

                # Check output file
                exe_path = self.dist_dir / f"{self.build_config['app_name']}.exe"
                if exe_path.exists():
                    size_mb = exe_path.stat().st_size / (1024 * 1024)
                    print(f"📦 ไฟล์: {exe_path}")
                    print(f"📊 ขนาด: {size_mb:.1f} MB")
                    return True
                else:
                    print("❌ ไม่พบไฟล์ .exe ที่สร้าง")
                    return False
            else:
                print("❌ การสร้าง .exe ล้มเหลว:")
                print(result.stderr)
                return False

        except Exception as e:
            print(f"❌ ข้อผิดพลาดในการสร้าง: {e}")
            return False

    def create_installer_package(self) -> bool:
        """Create installation package"""
        print("📦 สร้างแพ็คเกจติดตั้ง...")

        try:
            # Create installer batch script
            installer_content = f"""@echo off
chcp 65001 >nul
echo.
echo ==============================================
echo  DENSO888 - Excel to SQL Installation
echo  by เฮียตอมจัดหั้ย!!!
echo ==============================================
echo.

REM ตรวจสอบสิทธิ์ Administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ รันด้วยสิทธิ์ Administrator
) else (
    echo ⚠️ แนะนำให้รันด้วยสิทธิ์ Administrator
)

REM สร้างโฟลเดอร์โปรแกรม
set "INSTALL_DIR=%USERPROFILE%\\DENSO888"
echo 📁 ติดตั้งไปยัง: %INSTALL_DIR%

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM คัดลอกไฟล์
echo 📋 คัดลอกไฟล์โปรแกรม...
copy "{self.build_config['app_name']}.exe" "%INSTALL_DIR%\\" >nul

REM สร้างโฟลเดอร์ข้อมูล
if not exist "%INSTALL_DIR%\\input_excels" mkdir "%INSTALL_DIR%\\input_excels"
if not exist "%INSTALL_DIR%\\logs" mkdir "%INSTALL_DIR%\\logs"
if not exist "%INSTALL_DIR%\\assets" mkdir "%INSTALL_DIR%\\assets"

REM คัดลอกไฟล์เพิ่มเติม
if exist "assets" xcopy "assets" "%INSTALL_DIR%\\assets\\" /E /I /Q >nul
if exist ".env.example" copy ".env.example" "%INSTALL_DIR%\\.env" >nul

REM สร้าง shortcut บน Desktop
echo 🖥️ สร้าง shortcut บน Desktop...
set "SHORTCUT=%USERPROFILE%\\Desktop\\DENSO888.lnk"
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); $Shortcut.TargetPath = '%INSTALL_DIR%\\{self.build_config['app_name']}.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'DENSO888 - Excel to SQL'; $Shortcut.Save()" >nul 2>&1

REM สร้าง Start Menu shortcut
echo 📱 สร้าง shortcut ใน Start Menu...
set "STARTMENU=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs"
if not exist "%STARTMENU%\\DENSO888" mkdir "%STARTMENU%\\DENSO888"
set "STARTSHORTCUT=%STARTMENU%\\DENSO888\\DENSO888.lnk"
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTSHORTCUT%'); $Shortcut.TargetPath = '%INSTALL_DIR%\\{self.build_config['app_name']}.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'DENSO888 - Excel to SQL'; $Shortcut.Save()" >nul 2>&1

echo.
echo ✅ ติดตั้งเรียบร้อย!
echo 📁 โฟลเดอร์โปรแกรม: %INSTALL_DIR%
echo 🖥️ Desktop Shortcut: %USERPROFILE%\\Desktop\\DENSO888.lnk
echo 📱 Start Menu: Programs\\DENSO888
echo.
echo 💡 หมายเหตุ:
echo    • ต้องมี ODBC Driver 17 for SQL Server สำหรับเชื่อมต่อ SQL Server
echo    • สามารถแก้ไข .env ในโฟลเดอร์โปรแกรมได้
echo    • SQLite ทำงานได้ทันทีโดยไม่ต้องติดตั้งเพิ่ม
echo.
echo กดปุ่มใดก็ได้เพื่อปิด...
pause > nul
"""

            installer_path = self.dist_dir / "INSTALL_DENSO888.bat"
            with open(installer_path, "w", encoding="utf-8") as f:
                f.write(installer_content)

            # Create uninstaller
            uninstaller_content = f"""@echo off
chcp 65001 >nul
echo.
echo ==============================================
echo  DENSO888 - Uninstaller
echo ==============================================
echo.

set "INSTALL_DIR=%USERPROFILE%\\DENSO888"
set "DESKTOP_SHORTCUT=%USERPROFILE%\\Desktop\\DENSO888.lnk"
set "STARTMENU_DIR=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\DENSO888"

echo กำลังถอนการติดตั้ง DENSO888...
echo.

REM ลบ shortcuts
if exist "%DESKTOP_SHORTCUT%" (
    del "%DESKTOP_SHORTCUT%" >nul 2>&1
    echo ✅ ลบ Desktop shortcut
)

if exist "%STARTMENU_DIR%" (
    rmdir /s /q "%STARTMENU_DIR%" >nul 2>&1
    echo ✅ ลบ Start Menu shortcuts
)

REM ถามเกี่ยวกับข้อมูล
echo.
choice /c YN /m "ต้องการลบข้อมูลและ logs ทั้งหมดหรือไม่ (Y/N)"
if errorlevel 2 goto keep_data

REM ลบทั้งหมด
if exist "%INSTALL_DIR%" (
    rmdir /s /q "%INSTALL_DIR%" >nul 2>&1
    echo ✅ ลบโฟลเดอร์โปรแกรมและข้อมูลทั้งหมด
)
goto done

:keep_data
REM ลบเฉพาะไฟล์โปรแกรม
if exist "%INSTALL_DIR%\\{self.build_config['app_name']}.exe" (
    del "%INSTALL_DIR%\\{self.build_config['app_name']}.exe" >nul 2>&1
    echo ✅ ลบไฟล์โปรแกรม (เก็บข้อมูลไว้)
)

:done
echo.
echo ✅ ถอนการติดตั้งเรียบร้อย!
echo.
echo กดปุ่มใดก็ได้เพื่อปิด...
pause > nul
"""

            uninstaller_path = self.dist_dir / "UNINSTALL_DENSO888.bat"
            with open(uninstaller_path, "w", encoding="utf-8") as f:
                f.write(uninstaller_content)

            # Create README for distribution
            readme_content = f"""# DENSO888 - Excel to SQL
**Created by เฮียตอมจัดหั้ย!!!**

## 📦 Package Contents
- `{self.build_config['app_name']}.exe` - Main application
- `INSTALL_DENSO888.bat` - Installation script
- `UNINSTALL_DENSO888.bat` - Uninstaller script
- `assets/` - Application assets
- `.env.example` - Configuration template

## 🚀 Installation
1. Right-click `INSTALL_DENSO888.bat`
2. Select "Run as administrator" (recommended)
3. Follow installation prompts

## ✨ Features
- ✅ Mock data generation (100 - 50,000 rows)
- ✅ Excel file import (.xlsx, .xls)
- ✅ SQL Server + SQLite support
- ✅ Real-time progress tracking
- ✅ Modern GUI interface

## 🔧 Requirements
- Windows 10/11
- ODBC Driver 17 for SQL Server (for SQL Server connections)
- No additional software required for SQLite

## 📞 Support
For issues or questions, check the logs in:
`%USERPROFILE%\\DENSO888\\logs\\denso888.log`
"""

            readme_path = self.dist_dir / "README.txt"
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(readme_content)

            print("  ✅ INSTALL_DENSO888.bat")
            print("  ✅ UNINSTALL_DENSO888.bat")
            print("  ✅ README.txt")
            print("✅ แพ็คเกจติดตั้งเรียบร้อย!\n")
            return True

        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการสร้างแพ็คเกจ: {e}")
            return False

    def cleanup_build(self):
        """Clean up build artifacts"""
        print("🧹 ทำความสะอาด...")

        cleanup_items = [
            self.build_dir,
            self.project_root / f"{self.build_config['app_name']}.spec",
            self.project_root / "__pycache__",
        ]

        for item in cleanup_items:
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                    print(f"  🗑️ ลบ {item.name}/")
                elif item.is_file():
                    item.unlink()
                    print(f"  🗑️ ลบ {item.name}")
            except Exception as e:
                print(f"  ⚠️ ไม่สามารถลบ {item}: {e}")

        print("✅ ทำความสะอาดเรียบร้อย!\n")

    def create_build_info(self) -> Dict[str, Any]:
        """Create build information"""
        import datetime

        exe_path = self.dist_dir / f"{self.build_config['app_name']}.exe"

        build_info = {
            "app_name": self.build_config["app_name"],
            "build_date": datetime.datetime.now().isoformat(),
            "python_version": sys.version,
            "platform": sys.platform,
            "exe_size_mb": (
                round(exe_path.stat().st_size / (1024 * 1024), 2)
                if exe_path.exists()
                else 0
            ),
            "build_config": self.build_config,
        }

        info_path = self.dist_dir / "build_info.json"
        with open(info_path, "w", encoding="utf-8") as f:
            json.dump(build_info, f, indent=2, ensure_ascii=False)

        return build_info

    def build(self) -> bool:
        """Main build process"""
        print("=" * 60)
        print("🏭 DENSO888 - Excel to SQL Build System")
        print("   by เฮียตอมจัดหั้ย!!!")
        print("=" * 60)
        print()

        steps = [
            ("ตรวจสอบ Requirements", self.check_requirements),
            ("เตรียมสภาพแวดล้อม", self.prepare_build_environment),
            ("สร้างไฟล์ .spec", lambda: self.create_spec_file()),
        ]

        spec_file = None

        # Execute preparation steps
        for step_name, step_func in steps[:2]:
            print(f"🔄 {step_name}...")
            if not step_func():
                print(f"❌ ล้มเหลวในขั้นตอน: {step_name}")
                return False

        # Create spec file
        print(f"🔄 สร้างไฟล์ .spec...")
        spec_file = self.create_spec_file()

        # Build executable
        print(f"🔄 สร้างไฟล์ .exe...")
        if not self.build_executable(spec_file):
            print("❌ ล้มเหลวในการสร้าง executable")
            return False

        # Create installer package
        print(f"🔄 สร้างแพ็คเกจติดตั้ง...")
        if not self.create_installer_package():
            print("❌ ล้มเหลวในการสร้างแพ็คเกจติดตั้ง")
            return False

        # Create build info
        build_info = self.create_build_info()

        # Cleanup
        self.cleanup_build()

        # Success summary
        print("=" * 60)
        print("🎉 Build สำเร็จ!")
        print("=" * 60)
        print("📦 ไฟล์ที่ได้:")
        print(f"   • {self.build_config['app_name']}.exe - แอปพลิเคชันหลัก")
        print("   • INSTALL_DENSO888.bat - ไฟล์ติดตั้ง")
        print("   • UNINSTALL_DENSO888.bat - ไฟล์ถอนการติดตั้ง")
        print("   • README.txt - คำแนะนำการใช้งาน")
        print("   • build_info.json - ข้อมูล build")
        print()
        print("🚀 วิธีใช้:")
        print("   1. คัดลอกโฟลเดอร์ dist/ ไปยังเครื่องเป้าหมาย")
        print("   2. รัน INSTALL_DENSO888.bat เพื่อติดตั้ง")
        print("   3. หรือรัน .exe โดยตรง")
        print()
        print(f"📊 ข้อมูล Build:")
        print(f"   • ขนาดไฟล์: {build_info['exe_size_mb']} MB")
        print(f"   • Python: {build_info['python_version'].split()[0]}")
        print(f"   • Platform: {build_info['platform']}")

        return True


def main():
    """Main build script"""
    builder = DENSO888Builder()

    try:
        success = builder.build()

        if not success:
            print("\n❌ Build ล้มเหลว!")
            input("กดปุ่ม Enter เพื่อปิด...")
            sys.exit(1)
        else:
            print("\n✅ Build เสร็จสิ้น!")
            input("กดปุ่ม Enter เพื่อปิด...")

    except KeyboardInterrupt:
        print("\n⚠️ Build ถูกยกเลิกโดยผู้ใช้")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาดร้ายแรง: {e}")
        input("กดปุ่ม Enter เพื่อปิด...")
        sys.exit(1)


if __name__ == "__main__":
    main()
