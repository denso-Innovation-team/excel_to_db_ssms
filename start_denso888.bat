@echo off
title DENSO888 Modern Edition
echo 🏭 Starting DENSO888...
echo Created by Thammaphon Chittasuwanna (SDM)
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install dependencies if needed
if not exist venv (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Start application
echo 🚀 Starting DENSO888...
python main_modern.py

pause
