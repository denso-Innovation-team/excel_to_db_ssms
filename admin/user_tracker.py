"""
User Activity & IP Tracking System
สำหรับแอดมินตรวจสอบการใช้งาน
"""

import json
import socket
from datetime import datetime
from typing import Dict, List
from pathlib import Path


class UserActivityTracker:
    def __init__(self):
        self.log_file = Path("logs/user_activity.json")
        self.log_file.parent.mkdir(exist_ok=True)

    def get_client_ip(self) -> str:
        """ดึง IP address ของ client"""
        try:
            # Get local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "localhost"

    def log_activity(self, action: str, details: Dict = None):
        """บันทึกการใช้งาน"""
        activity = {
            "timestamp": datetime.now().isoformat(),
            "ip_address": self.get_client_ip(),
            "action": action,
            "details": details or {},
            "user_agent": "DENSO888_Desktop",
        }

        # Read existing logs
        logs = []
        if self.log_file.exists():
            try:
                with open(self.log_file, "r", encoding="utf-8") as f:
                    logs = json.load(f)
            except:
                logs = []

        # Add new activity
        logs.append(activity)

        # Keep only last 1000 activities
        logs = logs[-1000:]

        # Save logs
        with open(self.log_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)

    def get_activities(self, limit: int = 100) -> List[Dict]:
        """ดึงรายการการใช้งาน"""
        if not self.log_file.exists():
            return []

        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                logs = json.load(f)
            return logs[-limit:]
        except:
            return []

    def get_ip_summary(self) -> Dict[str, int]:
        """สรุปการใช้งานแยกตาม IP"""
        activities = self.get_activities(1000)
        ip_count = {}

        for activity in activities:
            ip = activity.get("ip_address", "unknown")
            ip_count[ip] = ip_count.get(ip, 0) + 1

        return dict(sorted(ip_count.items(), key=lambda x: x[1], reverse=True))
