@echo off
title DENSO888 - Excel to SQL Management System
echo.
echo ========================================
echo  🏭 DENSO888 - Excel to SQL
echo  by เฮียตอมจัดหั้ย!!!
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist .venv (
    echo 📦 Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo 📥 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

REM Run application
echo.
echo 🚀 Starting DENSO888...
echo.
python main.py

if errorlevel 1 (
    echo.
    echo ❌ Application encountered an error
    echo Check logs/denso888.log for details
    pause
)
