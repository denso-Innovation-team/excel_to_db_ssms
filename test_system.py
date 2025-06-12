#!/usr/bin/env python3
"""
System testing - แยก modules
"""

import pandas as pd
import random
from datetime import datetime, timedelta

from config import DatabaseConfig
from database import DatabaseManager

def test_connection():
    print("🔍 Testing SQL Server connection...")
    
    config = DatabaseConfig.from_env()
    db_manager = DatabaseManager(config)
    
    if db_manager.test():
        print("✅ Connection successful!")
        return True
    else:
        print("❌ Connection failed!")
        return False

def create_sample_data():
    print("📝 Creating sample data...")
    
    data = []
    for i in range(100):
        data.append({
            "ID": i + 1,
            "Name": f"User {i+1:03d}",
            "Email": f"user{i+1:03d}@test.com",
            "Age": random.randint(20, 60),
            "Salary": random.randint(30000, 100000),
            "Department": random.choice(["Sales", "Marketing", "IT", "HR"]),
            "JoinDate": datetime.now() - timedelta(days=random.randint(30, 1000)),
            "Active": random.choice([True, False])
        })
    
    df = pd.DataFrame(data)
    test_file = "sample_data_100.xlsx"
    df.to_excel(test_file, index=False)
    
    print(f"✅ Created: {test_file}")
    return test_file

def main():
    print("🎯 Excel to SSMS - System Test")
    print("=" * 50)
    
    # Test connection
    conn_ok = test_connection()
    
    # Create sample data
    sample_file = create_sample_data() if conn_ok else None
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"  Connection: {'✅' if conn_ok else '❌'}")
    print(f"  Sample Data: {'✅' if sample_file else '❌'}")
    
    if conn_ok and sample_file:
        print(f"\n🚀 Ready to test:")
        print(f"  python excel_to_ssms.py {sample_file} test_employees")

if __name__ == "__main__":
    main()
