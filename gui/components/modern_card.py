"""
gui/components/modern_card.py
Modern Card Component - สำหรับแสดงข้อมูลแบบ Card Layout
"""

import tkinter as tk
from typing import Optional, Dict


class ModernCard:
    """Card component สำหรับแสดงข้อมูล"""

    def __init__(
        self,
        parent: tk.Widget,
        title: str = "",
        content: str = "",
        icon: Optional[str] = None,
        color: str = "default",
        width: int = 300,
        height: int = 150,
    ):
        self.parent = parent
        self.title = title
        self.content = content
        self.icon = icon
        self.width = width
        self.height = height

        self.colors = self._get_colors(color)
        self.card_frame = self._create_card()

    def _get_colors(self, color: str) -> Dict[str, str]:
        """สีสำหรับ card แต่ละประเภท"""
        color_schemes = {
            "default": {
                "bg": "#FFFFFF",
                "border": "#E2E8F0",
                "title": "#1E293B",
                "content": "#64748B",
                "accent": "#3B82F6",
            },
            "primary": {
                "bg": "#DBEAFE",
                "border": "#3B82F6",
                "title": "#1E40AF",
                "content": "#1E40AF",
                "accent": "#3B82F6",
            },
            "success": {
                "bg": "#D1FAE5",
                "border": "#059669",
                "title": "#065F46",
                "content": "#065F46",
                "accent": "#059669",
            },
            "warning": {
                "bg": "#FEF3C7",
                "border": "#D97706",
                "title": "#92400E",
                "content": "#92400E",
                "accent": "#D97706",
            },
            "danger": {
                "bg": "#FEE2E2",
                "border": "#DC2626",
                "title": "#991B1B",
                "content": "#991B1B",
                "accent": "#DC2626",
            },
        }
        return color_schemes.get(color, color_schemes["default"])

    def _create_card(self) -> tk.Frame:
        """สร้าง card frame"""
        # Main card frame
        card = tk.Frame(
            self.parent,
            bg=self.colors["bg"],
            relief="solid",
            bd=1,
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            width=self.width,
            height=self.height,
        )
        card.pack_propagate(False)

        # Content container
        content_frame = tk.Frame(card, bg=self.colors["bg"])
        content_frame.pack(fill="both", expand=True, padx=20, pady=15)

        # Header section
        if self.icon or self.title:
            header_frame = tk.Frame(content_frame, bg=self.colors["bg"])
            header_frame.pack(fill="x", pady=(0, 10))

            # Icon
            if self.icon:
                icon_label = tk.Label(
                    header_frame,
                    text=self.icon,
                    font=("Segoe UI", 20),
                    bg=self.colors["bg"],
                    fg=self.colors["accent"],
                )
                icon_label.pack(side="left", padx=(0, 10))

            # Title
            if self.title:
                title_label = tk.Label(
                    header_frame,
                    text=self.title,
                    font=("Segoe UI", 14, "bold"),
                    bg=self.colors["bg"],
                    fg=self.colors["title"],
                    anchor="w",
                )
                title_label.pack(side="left", fill="x", expand=True)

        # Content section
        if self.content:
            content_label = tk.Label(
                content_frame,
                text=self.content,
                font=("Segoe UI", 11),
                bg=self.colors["bg"],
                fg=self.colors["content"],
                justify="left",
                anchor="nw",
                wraplength=self.width - 50,
            )
            content_label.pack(fill="both", expand=True)

        return card

    def update_content(self, title: str = None, content: str = None, icon: str = None):
        """อัพเดทเนื้อหา card"""
        if title is not None:
            self.title = title
        if content is not None:
            self.content = content
        if icon is not None:
            self.icon = icon

        # ลบ content เก่าและสร้างใหม่
        for widget in self.card_frame.winfo_children():
            widget.destroy()

        content_frame = tk.Frame(self.card_frame, bg=self.colors["bg"])
        content_frame.pack(fill="both", expand=True, padx=20, pady=15)

        # สร้าง header และ content ใหม่
        if self.icon or self.title:
            header_frame = tk.Frame(content_frame, bg=self.colors["bg"])
            header_frame.pack(fill="x", pady=(0, 10))

            if self.icon:
                icon_label = tk.Label(
                    header_frame,
                    text=self.icon,
                    font=("Segoe UI", 20),
                    bg=self.colors["bg"],
                    fg=self.colors["accent"],
                )
                icon_label.pack(side="left", padx=(0, 10))

            if self.title:
                title_label = tk.Label(
                    header_frame,
                    text=self.title,
                    font=("Segoe UI", 14, "bold"),
                    bg=self.colors["bg"],
                    fg=self.colors["title"],
                    anchor="w",
                )
                title_label.pack(side="left", fill="x", expand=True)

        if self.content:
            content_label = tk.Label(
                content_frame,
                text=self.content,
                font=("Segoe UI", 11),
                bg=self.colors["bg"],
                fg=self.colors["content"],
                justify="left",
                anchor="nw",
                wraplength=self.width - 50,
            )
            content_label.pack(fill="both", expand=True)

    def pack(self, **kwargs):
        """Pack card"""
        self.card_frame.pack(**kwargs)

    def grid(self, **kwargs):
        """Grid card"""
        self.card_frame.grid(**kwargs)

    def get_widget(self) -> tk.Frame:
        """ได้ widget หลัก"""
        return self.card_frame


class StatCard(ModernCard):
    """Card สำหรับแสดงสถิติ"""

    def __init__(
        self,
        parent: tk.Widget,
        title: str,
        value: str,
        icon: str,
        color: str = "default",
    ):
        self.value = value
        content = f"Value: {value}"
        super().__init__(parent, title, content, icon, color, 250, 120)
        self._create_stat_layout()

    def _create_stat_layout(self):
        """Layout พิเศษสำหรับ stat card"""
        # ลบ content เก่า
        for widget in self.card_frame.winfo_children():
            widget.destroy()

        content_frame = tk.Frame(self.card_frame, bg=self.colors["bg"])
        content_frame.pack(fill="both", expand=True, padx=20, pady=15)

        # Icon และ Title
        header_frame = tk.Frame(content_frame, bg=self.colors["bg"])
        header_frame.pack(fill="x")

        icon_label = tk.Label(
            header_frame,
            text=self.icon,
            font=("Segoe UI", 16),
            bg=self.colors["bg"],
            fg=self.colors["accent"],
        )
        icon_label.pack(side="left")

        title_label = tk.Label(
            header_frame,
            text=self.title,
            font=("Segoe UI", 10),
            bg=self.colors["bg"],
            fg=self.colors["content"],
        )
        title_label.pack(side="left", padx=(8, 0))

        # Value แสดงใหญ่
        value_label = tk.Label(
            content_frame,
            text=self.value,
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["title"],
        )
        value_label.pack(pady=(10, 0))

    def update_value(self, new_value: str):
        """อัพเดทค่าสถิติ"""
        self.value = new_value
        self._create_stat_layout()


class ClickableCard(ModernCard):
    """Card ที่คลิกได้"""

    def __init__(
        self,
        parent: tk.Widget,
        title: str,
        content: str,
        icon: str = None,
        command=None,
        **kwargs,
    ):
        self.command = command
        super().__init__(parent, title, content, icon, **kwargs)
        self._setup_click_events()

    def _setup_click_events(self):
        """ตั้งค่าการคลิก"""
        if not self.command:
            return

        def on_click(event):
            if self.command:
                self.command()

        def on_enter(event):
            self.card_frame.configure(highlightbackground="#3B82F6")

        def on_leave(event):
            self.card_frame.configure(highlightbackground=self.colors["border"])

        # Bind click events
        self.card_frame.bind("<Button-1>", on_click)
        self.card_frame.bind("<Enter>", on_enter)
        self.card_frame.bind("<Leave>", on_leave)

        # Bind to all child widgets
        def bind_recursive(widget):
            widget.bind("<Button-1>", on_click)
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            for child in widget.winfo_children():
                bind_recursive(child)

        bind_recursive(self.card_frame)
