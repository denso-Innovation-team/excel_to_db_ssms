@echo off
echo Setting up DENSO888 environment...

:: Check Python installation
python --version 2>NUL
if errorlevel 1 (
    echo Python not found! Please install Python 3.11
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Create virtual environment
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

:: Activate virtual environment
call .venv\Scripts\activate

:: Upgrade pip
python -m pip install --upgrade pip

:: Install requirements
pip install -r requirements.txt

echo Setup complete!
echo Run 'python main.py' to start the application
pause
