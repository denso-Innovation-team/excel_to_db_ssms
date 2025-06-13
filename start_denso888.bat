@echo off
title DENSO888 - Quick Start
echo.
echo 🏭 DENSO888 - Excel to SQL Management System
echo    by เฮียตอมจัดหั้ย!!!
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Install Python 3.8+ from python.org
    pause
    exit /b 1
)

:: Install dependencies if needed
echo 📦 Checking dependencies...
python -c "import pandas, sqlalchemy, openpyxl" 2>nul
if errorlevel 1 (
    echo 📥 Installing dependencies...
    pip install pandas sqlalchemy pyodbc openpyxl python-dotenv tqdm
)

:: Create logs directory
if not exist logs mkdir logs

:: Run application
echo 🚀 Starting DENSO888...
echo.
python main.py

if errorlevel 1 (
    echo.
    echo ❌ Error occurred. Check logs/denso888.log
    pause
)
