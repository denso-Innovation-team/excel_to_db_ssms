#!/bin/bash
echo "🎯 Excel to SSMS - First Time Setup"
echo "====================================="

echo "1. Installing Python packages..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo ""
echo "2. Testing installation..."
python3 -c "import pandas, sqlalchemy, openpyxl; print('✅ Core packages OK')"

echo ""
echo "3. Creating sample data..."
python3 sample_data_generator.py test

echo ""
echo "4. Testing SQL Server connection..."
python3 connection_tester.py

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Copy .env.template to .env and edit your database settings"
echo "  2. Run: python3 quick_test.py"
