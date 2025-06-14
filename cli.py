#!/usr/bin/env python3
"""
cli.py
DENSO888 Command Line Interface
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.data_processor import process_excel_simple
from core.mock_generator import MockDataTemplates
from config.settings import get_config
from utils.logger import setup_logger

logger = setup_logger("denso888_cli")


def cmd_process_excel(args):
    """Process Excel file command"""
    config = get_config()
    db_config = config.database
    
    print(f"📊 Processing Excel file: {args.file}")
    
    result = process_excel_simple(
        file_path=args.file,
        db_config=db_config,
        table_name=args.table
    )
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return 1
    
    print(f"✅ Success: {result['rows_processed']} rows processed")
    print(f"📋 Table: {result['table_name']}")
    return 0


def cmd_generate_mock(args):
    """Generate mock data command"""
    print(f"🎲 Generating {args.template} data: {args.rows} rows")
    
    try:
        df = MockDataTemplates.generate_by_template(
            args.template, 
            args.rows
        )
        
        output_file = args.output or f"mock_{args.template}_{args.rows}.xlsx"
        df.to_excel(output_file, index=False)
        
        print(f"✅ Generated: {output_file}")
        print(f"📊 {len(df)} rows, {len(df.columns)} columns")
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def cmd_list_templates(args):
    """List available templates"""
    templates = MockDataTemplates.get_template_list()
    
    print("🎲 Available Mock Data Templates:")
    print("-" * 50)
    
    for template in templates:
        print(f"📋 {template['name']}")
        print(f"   Description: {template['description']}")
        print(f"   Default rows: {template['default_rows']:,}")
        print(f"   Columns: ~{template['estimated_columns']}")
        print()


def main():
    """CLI main function"""
    parser = argparse.ArgumentParser(description="DENSO888 CLI Tools")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Excel processing command
    excel_parser = subparsers.add_parser("process", help="Process Excel file")
    excel_parser.add_argument("file", help="Excel file path")
    excel_parser.add_argument("--table", help="Target table name")
    excel_parser.set_defaults(func=cmd_process_excel)
    
    # Mock data generation
    mock_parser = subparsers.add_parser("mock", help="Generate mock data")
    mock_parser.add_argument("template", choices=["employees", "sales", "inventory", "financial"])
    mock_parser.add_argument("rows", type=int, help="Number of rows")
    mock_parser.add_argument("--output", help="Output file name")
    mock_parser.set_defaults(func=cmd_generate_mock)
    
    # List templates
    list_parser = subparsers.add_parser("templates", help="List mock data templates")
    list_parser.set_defaults(func=cmd_list_templates)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
