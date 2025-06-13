@echo off
echo Installing DENSO888 dependencies...

:: Create and activate venv if it doesn't exist
if not exist .venv (
    python -m venv .venv
)
call .venv\Scripts\activate.bat

:: Run installation script
python install_deps.py

if %ERRORLEVEL% EQU 0 (
    echo Installation successful!
) else (
    echo Installation failed!
    pause
    exit /b 1
)

pause
