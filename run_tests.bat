@echo off
title DENSO888 Tests
echo 🧪 Running DENSO888 Tests...

call venv\Scripts\activate.bat
python -m pytest tests/ -v

pause
