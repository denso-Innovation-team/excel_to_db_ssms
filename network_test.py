#!/usr/bin/env python3
"""
Network Connectivity Test
ทดสอบการเชื่อมต่อ network ก่อน SQL Server
"""

import socket
import subprocess
import sys


def test_ping(host):
    """ทดสอบ ping"""
    try:
        result = subprocess.run(
            ["ping", "-n", "4", host], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            print(f"✅ Ping {host}: OK")
            return True
        else:
            print(f"❌ Ping {host}: Failed")
            return False
    except:
        print(f"❌ Ping {host}: Error")
        return False


def test_port(host, port, timeout=5):
    """ทดสอบ port connectivity"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()

        if result == 0:
            print(f"✅ Port {host}:{port}: Open")
            return True
        else:
            print(f"❌ Port {host}:{port}: Closed")
            return False
    except Exception as e:
        print(f"❌ Port {host}:{port}: Error - {e}")
        return False


def test_sql_server_alternatives():
    """ทดสอบ SQL Server alternatives"""

    # Common SQL Server ports
    servers_to_test = [
        ("10.73.148.27", 1433),  # Default
        ("10.73.148.27", 1434),  # Browser service
        ("localhost", 1433),  # Local instance
        ("127.0.0.1", 1433),  # Local IP
    ]

    print("\n🔍 ทดสอบ SQL Server instances...")

    working_servers = []
    for host, port in servers_to_test:
        if test_port(host, port, timeout=3):
            working_servers.append((host, port))

    return working_servers


def try_alternative_drivers():
    """ลองใช้ drivers อื่น"""
    print("\n🔧 ทดสอบ ODBC Drivers...")

    try:
        import pyodbc

        drivers = pyodbc.drivers()
        print("📋 Available drivers:")
        for driver in drivers:
            if "SQL Server" in driver:
                print(f"  ✅ {driver}")

        return drivers
    except Exception as e:
        print(f"❌ pyodbc error: {e}")
        return []


def create_offline_mode():
    """สร้างโหมดออฟไลน์สำหรับทดสอบ"""
    print("\n💾 สร้างโหมดออฟไลน์...")

    offline_test = '''#!/usr/bin/env python3
"""
Offline Excel Processing Test
ทดสอบการประมวลผล Excel โดยไม่ต้องใช้ database
"""

import pandas as pd
from pathlib import Path

def test_excel_only():
    """ทดสอบ Excel processing อย่างเดียว"""
    print("📊 ทดสอบ Excel processing...")
    
    # สร้างข้อมูลทดสอบ
    data = {
        "EmployeeID": ["EMP001", "EMP002", "EMP003"],
        "Name": ["สมชาย ใจดี", "สมหญิง รักดี", "วิชัย เจริญ"],
        "Department": ["IT", "การตลาด", "บัญชี"],
        "Salary": [50000, 75000, 85000]
    }
    
    df = pd.DataFrame(data)
    
    # เขียนไฟล์
    test_file = "offline_test.xlsx"
    df.to_excel(test_file, index=False)
    print(f"✅ สร้างไฟล์: {test_file}")
    
    # อ่านไฟล์
    df_read = pd.read_excel(test_file)
    print(f"✅ อ่านไฟล์: {len(df_read)} แถว")
    
    # แสดงข้อมูล
    print("\\n📋 ข้อมูลตัวอย่าง:")
    print(df_read.to_string(index=False))
    
    # ลบไฟล์
    Path(test_file).unlink()
    print(f"✅ ลบไฟล์ทดสอบ")
    
    return True

if __name__ == "__main__":
    test_excel_only()
'''

    with open("offline_test.py", "w", encoding="utf-8") as f:
        f.write(offline_test)

    print("✅ สร้าง offline_test.py")


def main():
    """Main network test"""

    print("🌐 Network Connectivity Test")
    print("=" * 40)

    host = "10.73.148.27"
    port = 1433

    # 1. Basic ping test
    ping_ok = test_ping(host)

    # 2. Port connectivity test
    port_ok = test_port(host, port)

    # 3. Test alternatives
    working_servers = test_sql_server_alternatives()

    # 4. Check drivers
    drivers = try_alternative_drivers()

    # 5. Create offline mode
    create_offline_mode()

    # Results
    print("\n" + "=" * 40)
    print("📊 Network Test Results")
    print("=" * 40)

    if ping_ok and port_ok:
        print("✅ Network connectivity: OK")
        print("💡 SQL Server configuration issue")
        print("🔧 Check SQL Server:")
        print("  1. Enable TCP/IP protocol")
        print("  2. Enable remote connections")
        print("  3. Check firewall rules")
        print("  4. Restart SQL Server service")

    elif ping_ok and not port_ok:
        print("⚠️ Host reachable, port blocked")
        print("🔧 Solutions:")
        print("  1. Check firewall (port 1433)")
        print("  2. Check SQL Server configuration")
        print("  3. Try different port")

    elif not ping_ok:
        print("❌ Host unreachable")
        print("🔧 Solutions:")
        print("  1. Check network connection")
        print("  2. Check VPN/proxy settings")
        print("  3. Contact network admin")
        print("  4. Use offline mode")

    if working_servers:
        print(f"\n✅ Working servers found: {working_servers}")
    else:
        print("\n⚠️ No SQL Server instances accessible")
        print("🚀 Try offline mode: python offline_test.py")


if __name__ == "__main__":
    main()
