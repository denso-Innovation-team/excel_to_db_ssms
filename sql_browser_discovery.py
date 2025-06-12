#!/usr/bin/env python3
"""
SQL Server Browser Discovery
ค้นหา SQL Server instances และ dynamic ports
"""

import socket
import struct
import time


def discover_sql_instances(server_ip="10.73.148.27", timeout=5):
    """ใช้ SQL Browser Service ค้นหา instances"""

    print(f"🔍 Discovering SQL Server instances on {server_ip}")
    print("-" * 50)

    try:
        # SQL Browser listens on UDP port 1434
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)

        # SQL Server Browser query packet
        query = b"\x02"  # CLNT_BCAST_EX

        sock.sendto(query, (server_ip, 1434))
        response, addr = sock.recvfrom(4096)
        sock.close()

        # Parse response
        if len(response) > 3:
            # Skip first 3 bytes, then parse server list
            data = response[3:].decode("utf-8", errors="ignore")

            print("📋 SQL Server Browser Response:")
            print(f"  Raw data length: {len(data)} bytes")

            # Parse instances (format: ServerName;InstanceName;IsClustered;Version;tcp;port;;)
            instances = []
            entries = data.split(";;")

            for entry in entries:
                if entry.strip():
                    parts = entry.split(";")
                    if len(parts) >= 6:
                        instance_info = {
                            "server_name": parts[0] if len(parts) > 0 else "",
                            "instance_name": parts[1] if len(parts) > 1 else "DEFAULT",
                            "is_clustered": parts[2] if len(parts) > 2 else "",
                            "version": parts[3] if len(parts) > 3 else "",
                            "protocol": parts[4] if len(parts) > 4 else "",
                            "port": parts[5] if len(parts) > 5 else "1433",
                        }
                        instances.append(instance_info)

            print(f"\n✅ Found {len(instances)} SQL Server instance(s):")
            for i, inst in enumerate(instances, 1):
                print(f"\n📋 Instance {i}:")
                print(f"  Server: {inst['server_name']}")
                print(f"  Instance: {inst['instance_name']}")
                print(f"  Port: {inst['port']}")
                print(f"  Version: {inst['version']}")
                print(f"  Protocol: {inst['protocol']}")

            return instances

    except socket.timeout:
        print("❌ SQL Browser timeout - service may be disabled")
    except Exception as e:
        print(f"❌ Browser discovery failed: {e}")

    return []


def test_direct_ports(server_ip="10.73.148.27"):
    """ทดสอบ common SQL Server ports โดยตรง"""

    print(f"\n🔍 Testing common SQL Server ports on {server_ip}")
    print("-" * 50)

    # Common SQL Server ports
    test_ports = [1433, 1434, 2433, 14333, 1435, 1436]

    open_ports = []

    for port in test_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((server_ip, port))
            sock.close()

            if result == 0:
                print(f"  ✅ Port {port}: OPEN")
                open_ports.append(port)
            else:
                print(f"  ❌ Port {port}: CLOSED")

        except Exception as e:
            print(f"  ❌ Port {port}: ERROR - {e}")

    return open_ports


def test_connection_alternatives(server_ip="10.73.148.27", open_ports=[]):
    """ทดสอบ connection ด้วย ports ที่เปิดอยู่"""

    print(f"\n🔍 Testing connections with discovered ports")
    print("-" * 50)

    import pyodbc

    working_connections = []

    # Test discovered ports
    for port in open_ports:
        if port == 1434:  # Skip SQL Browser port
            continue

        connection_formats = [
            # Direct port connection
            f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_ip},{port};DATABASE=master;UID=TS00029;PWD=Thammaphon@TS00029;TrustServerCertificate=yes;Encrypt=no;",
            # Alternative format
            f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_ip}:{port};DATABASE=master;UID=TS00029;PWD=Thammaphon@TS00029;TrustServerCertificate=yes;Encrypt=no;",
        ]

        for conn_str in connection_formats:
            try:
                print(f"  🔄 Testing port {port}...")
                conn = pyodbc.connect(conn_str, timeout=10)
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT @@SERVERNAME, @@VERSION, SERVERPROPERTY('InstanceName')"
                )
                server_name, version, instance = cursor.fetchone()

                print(f"    ✅ SUCCESS on port {port}")
                print(f"    📋 Server: {server_name}")
                print(f"    📋 Instance: {instance or 'DEFAULT'}")
                print(
                    f"    📋 Version: {version.split()[3] if len(version.split()) > 3 else 'Unknown'}"
                )

                conn.close()
                working_connections.append((port, conn_str))
                break

            except Exception as e:
                print(f"    ❌ Failed on port {port}: {str(e)[:100]}...")

    return working_connections


def ping_test(server_ip="10.73.148.27"):
    """ทดสอบ basic network connectivity"""

    print(f"🔍 Testing basic network connectivity to {server_ip}")
    print("-" * 50)

    import subprocess
    import platform

    try:
        # Choose ping command based on OS
        ping_cmd = (
            ["ping", "-n", "4"]
            if platform.system().lower() == "windows"
            else ["ping", "-c", "4"]
        )
        ping_cmd.append(server_ip)

        result = subprocess.run(ping_cmd, capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            print("✅ Network connectivity: OK")
            print("  Host is reachable")
            return True
        else:
            print("❌ Network connectivity: FAILED")
            print("  Host unreachable or ping blocked")
            return False

    except Exception as e:
        print(f"❌ Ping test error: {e}")
        return False


def main():
    """Main discovery process"""

    print("🎯 SQL Server Instance Discovery Tool")
    print("=" * 60)

    server_ip = "10.73.148.27"

    # 1. Basic network test
    network_ok = ping_test(server_ip)

    if not network_ok:
        print("\n💡 Network connectivity issue - check:")
        print("  1. VPN connection")
        print("  2. Network routes")
        print("  3. Firewall rules")
        return

    # 2. SQL Browser discovery
    instances = discover_sql_instances(server_ip)

    # 3. Port scanning
    open_ports = test_direct_ports(server_ip)

    # 4. Connection testing
    working_connections = []
    if open_ports:
        working_connections = test_connection_alternatives(server_ip, open_ports)

    # 5. Generate working configuration
    print("\n" + "=" * 60)
    print("📊 Discovery Summary")
    print("=" * 60)

    if instances:
        print(f"✅ SQL Browser found {len(instances)} instance(s)")
        for inst in instances:
            if inst["instance_name"] and inst["instance_name"] != "DEFAULT":
                print(
                    f"  Named Instance: {inst['instance_name']} on port {inst['port']}"
                )

    if open_ports:
        print(f"✅ Open ports: {', '.join(map(str, open_ports))}")

    if working_connections:
        print(f"✅ Working connections: {len(working_connections)}")

        port, conn_str = working_connections[0]
        print(f"\n🎯 **USE THIS CONNECTION:**")
        print(f"Connection String: {conn_str}")

        # Generate .env configuration
        print(f"\n📝 .env Configuration:")
        print(f"DB_HOST={server_ip}")
        print(f"DB_PORT={port}")
        print(f"DB_NAME=excel_to_db")
        print(f"# Remove DB_INSTANCE (use direct port instead)")

        # Generate Python code
        print(f"\n💻 Python Connection Code:")
        print(
            f"""
connection_url = (
    f"mssql+pyodbc://TS00029:{{quote_plus('Thammaphon@TS00029')}}@"
    f"{server_ip}:{port}/excel_to_db?"
    f"driver=ODBC+Driver+17+for+SQL+Server&"
    f"TrustServerCertificate=yes&Encrypt=no"
)
"""
        )
    else:
        print("❌ No working connections found")
        print("\n💡 Next steps:")
        print("  1. Check SQL Server service status")
        print("  2. Enable SQL Browser service")
        print("  3. Configure SQL Server for remote connections")
        print("  4. Check Windows Firewall")


if __name__ == "__main__":
    main()
