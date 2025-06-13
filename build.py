#!/usr/bin/env python3
"""DENSO888 Build System - Clean Version"""
import os
import sys
import shutil
import subprocess
from pathlib import Path


def main():
    print("🏭 DENSO888 Build System")
    print("=" * 50)

    # Check dependencies
    required = ["pyinstaller", "pandas", "sqlalchemy", "pyodbc", "openpyxl"]
    missing = []

    for pkg in required:
        try:
            __import__(pkg.replace("-", "_"))
            print(f"  ✅ {pkg}")
        except ImportError:
            missing.append(pkg)
            print(f"  ❌ {pkg}")

    if missing:
        print(f"\n⚠️ ติดตั้งก่อน: pip install {' '.join(missing)}")
        input("กด Enter เพื่อออก...")
        return

    # Build config
    app_name = "DENSO888_ExcelToSQL"
    project_root = Path(__file__).parent

    # Create complete PyInstaller spec
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['{str(project_root)}'],
    binaries=[],
    datas=[
        ('.env.example', '.'),
        ('assets', 'assets'),
        ('config', 'config'),
        ('utils', 'utils')
    ],
    hiddenimports=[
        'pandas',
        'sqlalchemy',
        'sqlalchemy.dialects.mssql',  
        'sqlalchemy.dialects.sqlite',
        'pyodbc',
        'openpyxl',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'dotenv',
        'tqdm',
        'sqlite3',
        'threading',
        'logging',
        'pathlib',
        'typing'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=['matplotlib', 'test', 'tests', 'pytest'],
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
    name='{app_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None
)
"""

    # Write spec file
    spec_file = project_root / f"{app_name}.spec"
    with open(spec_file, "w", encoding="utf-8") as f:
        f.write(spec_content)

    print(f"\n📄 สร้าง spec: {spec_file}")

    # Build executable
    print("\n🔨 กำลัง build (อาจใช้เวลา 2-5 นาที)...")

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "PyInstaller",
                "--clean",
                "--noconfirm",
                str(spec_file),
            ],
            capture_output=True,
            text=True,
            timeout=600,
        )

        if result.returncode == 0:
            exe_path = project_root / "dist" / f"{app_name}.exe"
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"✅ สำเร็จ: {size_mb:.1f} MB")

                # Create enhanced installer
                installer_content = f"""@echo off
chcp 65001 >nul
echo.
echo ========================================
echo  DENSO888 - Excel to SQL Installer
echo  by เฮียตอมจัดหั้ย!!!
echo ========================================
echo.

set "INSTALL_DIR=%USERPROFILE%\\DENSO888"
echo 📁 ติดตั้งไปยัง: %INSTALL_DIR%

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo 📋 คัดลอกไฟล์โปรแกรม...
copy "{app_name}.exe" "%INSTALL_DIR%\\" >nul
if errorlevel 1 (
    echo ❌ ไม่สามารถคัดลอกไฟล์ได้
    pause
    exit /b 1
)

REM สร้างโฟลเดอร์ข้อมูล  
if not exist "%INSTALL_DIR%\\input_excels" mkdir "%INSTALL_DIR%\\input_excels"
if not exist "%INSTALL_DIR%\\logs" mkdir "%INSTALL_DIR%\\logs"
if not exist "%INSTALL_DIR%\\assets" mkdir "%INSTALL_DIR%\\assets"

REM คัดลอกไฟล์เพิ่มเติม
if exist "assets" xcopy "assets" "%INSTALL_DIR%\\assets\\" /E /I /Q >nul 2>&1
if exist ".env.example" copy ".env.example" "%INSTALL_DIR%\\.env" >nul 2>&1

echo 🖥️ สร้าง desktop shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\DENSO888.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\{app_name}.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'DENSO888 - Excel to SQL'; $Shortcut.Save()" >nul 2>&1

echo 📱 สร้าง Start Menu shortcut...
set "STARTMENU=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs"
if not exist "%STARTMENU%\\DENSO888" mkdir "%STARTMENU%\\DENSO888"
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTMENU%\\DENSO888\\DENSO888.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\{app_name}.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'DENSO888 - Excel to SQL'; $Shortcut.Save()" >nul 2>&1

echo.
echo ✅ ติดตั้งเสร็จสิ้น!
echo 📁 โฟลเดอร์โปรแกรม: %INSTALL_DIR%
echo 🖥️ Desktop shortcut: %USERPROFILE%\\Desktop\\DENSO888.lnk
echo 📱 Start Menu: Programs\\DENSO888
echo.
echo 💡 หมายเหตุ:
echo    • ต้องมี ODBC Driver 17 for SQL Server สำหรับ SQL Server
echo    • SQLite ใช้งานได้ทันที
echo    • สามารถแก้ไข .env ในโฟลเดอร์โปรแกรมได้
echo.
pause
"""

                installer_path = project_root / "dist" / "INSTALL_DENSO888.bat"
                with open(installer_path, "w", encoding="utf-8") as f:
                    f.write(installer_content)

                print(f"✅ สร้าง installer: {installer_path}")

                # Cleanup build files
                build_dir = project_root / "build"
                if build_dir.exists():
                    shutil.rmtree(build_dir)
                spec_file.unlink()

                print("\n🎉 Build เสร็จแล้ว!")
                print(f"📦 ไฟล์อยู่ที่: {project_root / 'dist'}")
                print("\n🚀 วิธีใช้:")
                print("1. คัดลอกโฟลเดอร์ dist/ ไปเครื่องเป้าหมาย")
                print("2. รัน INSTALL_DENSO888.bat เพื่อติดตั้ง")
                print("3. หรือรัน .exe โดยตรง")

            else:
                print("❌ ไม่พบไฟล์ .exe หลังจาก build")
        else:
            print("❌ Build ล้มเหลว:")
            print(result.stderr[-1000:] if result.stderr else "No error output")

    except subprocess.TimeoutExpired:
        print("❌ Build timeout (10 นาที)")
    except Exception as e:
        print(f"❌ Build error: {e}")

    input("\nกด Enter เพื่อออก...")


if __name__ == "__main__":
    main()
