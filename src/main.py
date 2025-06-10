# src/main.py
import pandas as pd
from sqlalchemy import create_engine


class ExcelToDatabaseProcessor:
    def __init__(self, excel_file, table_name, **kwargs):
        self.excel_file = excel_file
        self.table_name = table_name

    def process(self, create_table=True):
        engine = create_engine("db.ydmmxivfmfgbbphmitgy.supabase.co")
        df = pd.read_excel(self.excel_file)
        df.to_sql(self.table_name, engine, if_exists="replace", index=False)
        return {"inserted_rows": len(df), "processing_time": 1.0}
