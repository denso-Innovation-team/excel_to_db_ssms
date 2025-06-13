@echo off
echo Starting DENSO888 application...

:: Activate virtual environment if exists
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

:: Run setup
python setup.py

:: Run application if setup successful
if %ERRORLEVEL% EQU 0 (
    python main.py
) else (
    echo Failed to start application
    pause
)
