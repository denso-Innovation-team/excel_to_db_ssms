#!/usr/bin/env python3
"""
Generated Test Script - Working Configuration
"""

import pyodbc

def test_working_connection():
    """ทดสอบ connection ที่ทำงานได้"""
    
    conn_str = """DRIVER={ODBC Driver 17 for SQL Server};SERVER=10.73.148.27;DATABASE=master;UID=TS00029;PWD=Thammaphon@TS00029;TrustServerCertificate=yes;Encrypt=no;ConnectRetryCount=1;ConnectRetryInterval=1;LoginTimeout=10;"""
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT @@SERVERNAME, DB_NAME()")
        server, db = cursor.fetchone()
        
        print(f"✅ Connection successful: {server} / {db}")
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_working_connection()
