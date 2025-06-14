"""
Mock Data Selector Widget
ฟีเจอร์เลือก mock data 100, 500, 1000, 5000, 10000, 50000 rows
"""

import tkinter as tk
from typing import Callable, Optional


class MockDataSelector:
    """Modern Mock Data Selection Component"""

    def __init__(self, parent: tk.Widget, callback: Optional[Callable] = None):
        self.parent = parent
        self.callback = callback
        self.selected_count = tk.IntVar(value=1000)
        self.template_type = tk.StringVar(value="employees")

        self.frame = tk.Frame(parent, bg="#FFFFFF")
        self.create_widgets()

    def create_widgets(self):
        """Create mock data selection widgets"""
        # Title
        title = tk.Label(
            self.frame,
            text="🎲 Generate Mock Data",
            font=("Segoe UI", 16, "bold"),
            fg="#DC0003",
            bg="#FFFFFF",
        )
        title.pack(pady=(0, 20))

        # Template selection
        template_frame = tk.LabelFrame(
            self.frame,
            text="Data Template",
            font=("Segoe UI", 12, "bold"),
            fg="#2C3E50",
            bg="#FFFFFF",
            padx=20,
            pady=15,
        )
        template_frame.pack(fill="x", pady=(0, 15))

        templates = [
            (
                "employees",
                "👥 Employee Records",
                "Personnel data with departments & salaries",
            ),
            ("sales", "💰 Sales Transactions", "Sales data with products & customers"),
            ("inventory", "📦 Inventory Items", "Stock management with suppliers"),
        ]

        for value, title, desc in templates:
            radio_frame = tk.Frame(template_frame, bg="#FFFFFF")
            radio_frame.pack(fill="x", pady=3)

            radio = tk.Radiobutton(
                radio_frame,
                text=title,
                variable=self.template_type,
                value=value,
                font=("Segoe UI", 11, "bold"),
                fg="#2C3E50",
                bg="#FFFFFF",
                activebackground="#FFFFFF",
            )
            radio.pack(anchor="w")

            desc_label = tk.Label(
                radio_frame,
                text=f"   {desc}",
                font=("Segoe UI", 9),
                fg="#7F8C8D",
                bg="#FFFFFF",
            )
            desc_label.pack(anchor="w")

        # Row count selection
        count_frame = tk.LabelFrame(
            self.frame,
            text="Number of Records",
            font=("Segoe UI", 12, "bold"),
            fg="#2C3E50",
            bg="#FFFFFF",
            padx=20,
            pady=15,
        )
        count_frame.pack(fill="x", pady=(0, 20))

        # Preset buttons
        preset_frame = tk.Frame(count_frame, bg="#FFFFFF")
        preset_frame.pack(fill="x", pady=(0, 15))

        presets = [100, 500, 1000, 5000, 10000, 50000]

        for i, count in enumerate(presets):
            row = i // 3
            col = i % 3

            if i % 3 == 0:
                button_row = tk.Frame(preset_frame, bg="#FFFFFF")
                button_row.pack(fill="x", pady=2)

            btn = tk.Radiobutton(
                button_row,
                text=f"{count:,}",
                variable=self.selected_count,
                value=count,
                font=("Segoe UI", 11, "bold"),
                fg="#FFFFFF",
                bg="#28A745",
                selectcolor="#34CE57",
                activebackground="#218838",
                activeforeground="#FFFFFF",
                relief="flat",
                borderwidth=0,
                padx=15,
                pady=8,
                width=8,
            )
            btn.pack(side="left", padx=5, fill="x", expand=True)

        # Custom input
        custom_frame = tk.Frame(count_frame, bg="#FFFFFF")
        custom_frame.pack(fill="x", pady=(10, 0))

        tk.Label(
            custom_frame,
            text="Custom Count:",
            font=("Segoe UI", 11, "bold"),
            fg="#2C3E50",
            bg="#FFFFFF",
        ).pack(side="left")

        self.custom_entry = tk.Entry(
            custom_frame, font=("Segoe UI", 11), width=15, relief="solid", borderwidth=1
        )
        self.custom_entry.pack(side="left", padx=(10, 0))
        self.custom_entry.bind("<Return>", self._on_custom_enter)

        # Generate button
        generate_btn = tk.Button(
            self.frame,
            text="🚀 Generate Data",
            command=self._generate_data,
            font=("Segoe UI", 14, "bold"),
            bg="#DC0003",
            fg="#FFFFFF",
            relief="flat",
            borderwidth=0,
            padx=40,
            pady=15,
            cursor="hand2",
        )
        generate_btn.pack(pady=20)

    def _on_custom_enter(self, event):
        """Handle custom count entry"""
        try:
            custom_count = int(self.custom_entry.get())
            if 1 <= custom_count <= 1000000:
                self.selected_count.set(custom_count)
        except ValueError:
            pass

    def _generate_data(self):
        """Generate mock data"""
        # Get custom count if entered
        if self.custom_entry.get():
            try:
                custom_count = int(self.custom_entry.get())
                if 1 <= custom_count <= 1000000:
                    count = custom_count
                else:
                    count = self.selected_count.get()
            except ValueError:
                count = self.selected_count.get()
        else:
            count = self.selected_count.get()

        template = self.template_type.get()

        if self.callback:
            self.callback(template, count)

    def get_widget(self):
        """Get the main widget"""
        return self.frame
