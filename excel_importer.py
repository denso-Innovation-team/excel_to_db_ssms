import pandas as pd
from sqlalchemy import create_engine
import os

# Direct Supabase connection
engine = create_engine(
    "postgres://postgres.ydmmxivfmfgbbphmitgy:jsCvOpw2RbFdpf5L@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres?sslmode=require"
)

# Read Excel & Import
df = pd.read_excel("employees_1000.xlsx")
df.to_sql("employees_test", engine, if_exists="replace", index=False)
print(f"✅ Import: {len(df)} rows")
