#!/usr/bin/env python3
"""
SQLAlchemy Connection Test - Generated
"""

from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

def test_sqlalchemy():
    password_encoded = quote_plus("Thammaphon@TS00029")
    url = f"mssql+pyodbc://TS00029:{password_encoded}@10.73.148.27:1433/excel_to_db?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes&Encrypt=no"
    
    try:
        engine = create_engine(url, pool_size=3, max_overflow=5)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT @@SERVERNAME, DB_NAME()"))
            server, db = result.fetchone()
            print(f"✅ SQLAlchemy OK: {server}/{db}")
        engine.dispose()
        return True
    except Exception as e:
        print(f"❌ SQLAlchemy failed: {e}")
        return False

if __name__ == "__main__":
    test_sqlalchemy()
