#!/bin/bash
echo "========================================"
echo " 🏭 DENSO888 - Excel to SQL"
echo " by เฮียตอมจัดหั้ย!!!"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found! Please install Python 3.8+"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Run application
echo
echo "🚀 Starting DENSO888..."
echo
python main.py

if [ $? -ne 0 ]; then
    echo
    echo "❌ Application encountered an error"
    echo "Check logs/denso888.log for details"
fi
