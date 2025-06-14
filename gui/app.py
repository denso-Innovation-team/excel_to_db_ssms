"""
Add Admin Page to Main App
"""

from gui.pages.admin_page import AdminPage


class DENSO888App:
    def __init__(self):
        # ... existing code ...

        # Add admin page
        self.pages["admin"] = AdminPage(self.content_area, self.controller, self.theme)

        # Add to sidebar menu
        self.menu_items.append(
            {
                "id": "admin",
                "title": "Admin Panel",
                "icon": "🛡️",
                "description": "User Activity Monitor",
                "badge": "admin",
                "category": "system",
            }
        )
