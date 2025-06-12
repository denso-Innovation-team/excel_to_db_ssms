#!/usr/bin/env python3
"""Offline Excel Processor - No Database Required"""
import pandas as pd
import json
from datetime import datetime
from pathlib import Path

class OfflineExcelProcessor:
    def __init__(self):
        self.output_dir = Path("offline_output")
        self.output_dir.mkdir(exist_ok=True)
    
    def process_excel(self, excel_file, table_name="data"):
        """Process Excel without database"""
        try:
            # Read Excel
            df = pd.read_excel(excel_file)
            print(f"📊 Read {len(df)} rows from {excel_file}")
            
            # Clean data
            df.columns = [col.replace(" ", "_").lower() for col in df.columns]
            
            # Export formats
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 1. CSV
            csv_file = self.output_dir / f"{table_name}_{timestamp}.csv"
            df.to_csv(csv_file, index=False, encoding='utf-8-sig')
            print(f"✅ CSV: {csv_file}")
            
            # 2. JSON
            json_file = self.output_dir / f"{table_name}_{timestamp}.json"
            df.to_json(json_file, orient='records', ensure_ascii=False, indent=2)
            print(f"✅ JSON: {json_file}")
            
            # 3. Summary
            summary = {
                "file": str(excel_file),
                "table_name": table_name,
                "rows": len(df),
                "columns": list(df.columns),
                "timestamp": timestamp,
                "data_types": df.dtypes.astype(str).to_dict()
            }
            
            summary_file = self.output_dir / f"{table_name}_{timestamp}_summary.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
            print(f"✅ Summary: {summary_file}")
            
            return True
            
        except Exception as e:
            print(f"❌ Processing failed: {e}")
            return False

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python offline_excel_processor.py <excel_file> [table_name]")
        return
    
    excel_file = sys.argv[1]
    table_name = sys.argv[2] if len(sys.argv) > 2 else "data"
    
    processor = OfflineExcelProcessor()
    success = processor.process_excel(excel_file, table_name)
    
    if success:
        print("\n🎉 Offline processing complete!")
        print("📁 Check offline_output/ folder for results")
    else:
        print("\n❌ Processing failed")

if __name__ == "__main__":
    main()
