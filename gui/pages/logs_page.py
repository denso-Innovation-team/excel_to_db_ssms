"""
gui/pages/logs_page.py
Logs and Status Page
"""

import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
from gui.components.modern_components import ModernButton


class LogsPage:
    """Logs and status monitoring page"""

    def __init__(self, parent: tk.Widget, controller, theme):
        self.parent = parent
        self.controller = controller
        self.theme = theme
        self.logs_text: scrolledtext.ScrolledText = None

        self._create_ui()

    def _create_ui(self):
        """Create logs page UI"""
        main_frame = tk.Frame(self.parent, bg=self.theme.colors.background)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Logs section
        section_frame = tk.Frame(main_frame, bg=self.theme.colors.background)
        section_frame.pack(fill="both", expand=True, pady=(0, 20))

        title_label = tk.Label(
            section_frame,
            text="📝 Operation Logs",
            font=("Segoe UI", 14, "bold"),
            fg=self.theme.colors.text_primary,
            bg=self.theme.colors.background,
        )
        title_label.pack(anchor="w", pady=(0, 15))

        # Logs container
        logs_container = tk.Frame(section_frame, bg=self.theme.colors.background)
        logs_container.pack(fill="both", expand=True, pady=10)

        self.logs_text = scrolledtext.ScrolledText(
            logs_container,
            font=("Consolas", 9),
            relief="solid",
            borderwidth=1,
            state="disabled",
            bg="white",
            fg=self.theme.colors.text_primary,
            wrap=tk.WORD,
        )
        self.logs_text.pack(fill="both", expand=True)

        # Action buttons
        actions_frame = tk.Frame(main_frame, bg=self.theme.colors.background)
        actions_frame.pack(fill="x", pady=20)

        clear_btn = ModernButton(
            actions_frame,
            text="🗑️ Clear Logs",
            style="danger",
            size="medium",
            command=self._clear_logs,
        )
        clear_btn.get_widget().pack(side="left", padx=(0, 10))

    def add_log_message(self, message: str, level: str = "INFO"):
        """Add message to logs"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {level}: {message}\n"

        self.logs_text.configure(state="normal")
        self.logs_text.insert(tk.END, formatted_message)
        self.logs_text.configure(state="disabled")
        self.logs_text.see(tk.END)

    def _clear_logs(self):
        """Clear all logs"""
        self.logs_text.configure(state="normal")
        self.logs_text.delete(1.0, tk.END)
        self.logs_text.configure(state="disabled")
