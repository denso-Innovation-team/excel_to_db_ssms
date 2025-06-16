import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

"""
gui/pages/logs_page.py
Real-time Application Logs Viewer
Created by: Thammaphon Chittasuwanna (SDM) | Innovation Department
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import threading
import time


class LogsPage:
    """Real-time logs viewer with filtering and export"""

    def __init__(self, parent: tk.Widget, controller, theme):
        self.parent = parent
        self.controller = controller
        self.theme = theme

        # Log data
        self.log_entries: List[Dict[str, Any]] = []
        self.filtered_entries: List[Dict[str, Any]] = []
        self.auto_scroll = tk.BooleanVar(value=True)
        self.filter_level = tk.StringVar(value="ALL")

        # UI components
        self.main_frame = None
        self.log_text: Optional[scrolledtext.ScrolledText] = None

        self._create_logs_page()
        self._setup_auto_refresh()

    def _create_logs_page(self):
        """Create logs viewer interface"""
        self.main_frame = tk.Frame(self.parent, bg=self.theme.colors.background)

        # Header section
        self._create_header_section()

        # Controls section
        self._create_controls_section()

        # Logs display section
        self._create_logs_display_section()

        # Load initial logs
        self._refresh_logs()

    def _create_header_section(self):
        """Create header with title and stats"""
        header_frame = tk.Frame(
            self.main_frame, bg=self.theme.colors.primary, height=80
        )
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        header_content = tk.Frame(header_frame, bg=self.theme.colors.primary)
        header_content.pack(expand=True)

        # Title
        title_label = tk.Label(
            header_content,
            text="📝 Application Logs",
            font=self.theme.fonts.heading_lg,
            bg=self.theme.colors.primary,
            fg="white",
        )
        title_label.pack(pady=20)

        # Stats
        self.stats_label = tk.Label(
            header_content,
            text="Total entries: 0 | Filtered: 0",
            font=self.theme.fonts.body_md,
            bg=self.theme.colors.primary,
            fg="rgba(255,255,255,0.8)",
        )
        self.stats_label.pack()

    def _create_controls_section(self):
        """Create log controls and filters"""
        controls_frame = tk.Frame(
            self.main_frame, bg=self.theme.colors.surface, height=60
        )
        controls_frame.pack(fill="x")
        controls_frame.pack_propagate(False)

        content_frame = tk.Frame(controls_frame, bg=self.theme.colors.surface)
        content_frame.pack(expand=True, fill="x", padx=20)

        # Left controls
        left_frame = tk.Frame(content_frame, bg=self.theme.colors.surface)
        left_frame.pack(side="left", fill="y")

        # Filter by level
        tk.Label(
            left_frame,
            text="Level:",
            font=self.theme.fonts.body_md,
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
        ).pack(side="left", padx=(0, 10))

        level_combo = ttk.Combobox(
            left_frame,
            textvariable=self.filter_level,
            values=["ALL", "DEBUG", "INFO", "WARNING", "ERROR"],
            state="readonly",
            width=10,
        )
        level_combo.pack(side="left", padx=(0, 20))
        level_combo.bind("<<ComboboxSelected>>", lambda e: self._apply_filters())

        # Auto-scroll checkbox
        auto_scroll_check = tk.Checkbutton(
            left_frame,
            text="Auto-scroll",
            variable=self.auto_scroll,
            font=self.theme.fonts.body_md,
            bg=self.theme.colors.surface,
            activebackground=self.theme.colors.surface,
        )
        auto_scroll_check.pack(side="left", padx=(0, 20))

        # Right controls
        right_frame = tk.Frame(content_frame, bg=self.theme.colors.surface)
        right_frame.pack(side="right", fill="y")

        # Clear button
        clear_btn = tk.Button(
            right_frame,
            text="🗑️ Clear",
            font=self.theme.fonts.body_md,
            bg=self.theme.colors.danger,
            fg="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self._clear_logs,
        )
        clear_btn.pack(side="right", padx=(10, 0))

        # Export button
        export_btn = tk.Button(
            right_frame,
            text="📊 Export",
            font=self.theme.fonts.body_md,
            bg=self.theme.colors.info,
            fg="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self._export_logs,
        )
        export_btn.pack(side="right", padx=(10, 0))

        # Refresh button
        refresh_btn = tk.Button(
            right_frame,
            text="🔄 Refresh",
            font=self.theme.fonts.body_md,
            bg=self.theme.colors.success,
            fg="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self._refresh_logs,
        )
        refresh_btn.pack(side="right")

    def _create_logs_display_section(self):
        """Create logs display area"""
        display_frame = tk.Frame(self.main_frame, bg=self.theme.colors.background)
        display_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Log text area with scrolling
        self.log_text = scrolledtext.ScrolledText(
            display_frame,
            font=("Consolas", 10),
            bg=self.theme.colors.surface_dark,
            fg=self.theme.colors.text_primary,
            relief="flat",
            bd=1,
            wrap=tk.WORD,
            state="disabled",
        )
        self.log_text.pack(fill="both", expand=True)

        # Configure text tags for different log levels
        self.log_text.tag_configure("DEBUG", foreground="#64748B")
        self.log_text.tag_configure("INFO", foreground="#3B82F6")
        self.log_text.tag_configure("WARNING", foreground="#F59E0B")
        self.log_text.tag_configure("ERROR", foreground="#EF4444")
        self.log_text.tag_configure("timestamp", foreground="#94A3B8")

    def _setup_auto_refresh(self):
        """Setup automatic log refresh"""

        def refresh_loop():
            while True:
                try:
                    self._refresh_logs()
                    time.sleep(2)  # Refresh every 2 seconds
                except Exception as e:
                    print(f"Log refresh error: {e}")
                    time.sleep(5)

        # Start refresh thread
        refresh_thread = threading.Thread(target=refresh_loop, daemon=True)
        refresh_thread.start()

    def _refresh_logs(self):
        """Refresh log entries"""
        try:
            # Get logs from controller
            if hasattr(self.controller, "get_recent_logs"):
                new_logs = self.controller.get_recent_logs(100)
            else:
                # Mock logs for demonstration
                new_logs = self._generate_mock_logs()

            # Update log entries
            self.log_entries = new_logs

            # Apply filters
            self._apply_filters()

            # Update display
            self._update_log_display()

            # Update stats
            self._update_stats()

        except Exception as e:
            print(f"Error refreshing logs: {e}")

    def _generate_mock_logs(self) -> List[Dict[str, Any]]:
        """Generate mock log entries for demonstration"""
        import random

        levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
        messages = [
            "Database connection established",
            "Excel file processed successfully",
            "Mock data generation started",
            "User authentication completed",
            "Configuration loaded",
            "Connection pool initialized",
            "Data validation completed",
            "File import operation started",
            "System backup completed",
            "Cache refresh operation",
            "Network timeout detected",
            "Invalid data format detected",
            "Memory usage threshold exceeded",
            "Database query failed",
        ]

        logs = []
        base_time = datetime.now()

        for i in range(50):
            log_entry = {
                "timestamp": (base_time - timedelta(minutes=i)).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "level": random.choice(levels),
                "message": random.choice(messages),
                "module": random.choice(
                    ["Database", "Excel", "UI", "Controller", "Core"]
                ),
            }
            logs.append(log_entry)

        return list(reversed(logs))  # Newest first

    def _apply_filters(self):
        """Apply log filters"""
        level_filter = self.filter_level.get()

        if level_filter == "ALL":
            self.filtered_entries = self.log_entries.copy()
        else:
            self.filtered_entries = [
                entry
                for entry in self.log_entries
                if entry.get("level") == level_filter
            ]

    def _update_log_display(self):
        """Update log display with filtered entries"""
        try:
            # Clear current display
            self.log_text.configure(state="normal")
            self.log_text.delete(1.0, tk.END)

            # Add filtered entries
            for entry in self.filtered_entries[-100:]:  # Show last 100 entries
                timestamp = entry.get("timestamp", "")
                level = entry.get("level", "INFO")
                module = entry.get("module", "System")
                message = entry.get("message", "")

                # Format log line
                log_line = f"[{timestamp}] [{level:8}] [{module:10}] {message}\n"

                # Insert with appropriate tag
                self.log_text.insert(tk.END, log_line, level)

            # Auto-scroll to bottom if enabled
            if self.auto_scroll.get():
                self.log_text.see(tk.END)

            self.log_text.configure(state="disabled")

        except Exception as e:
            print(f"Error updating log display: {e}")

    def _update_stats(self):
        """Update statistics display"""
        total_entries = len(self.log_entries)
        filtered_entries = len(self.filtered_entries)

        stats_text = f"Total entries: {total_entries} | Filtered: {filtered_entries}"
        self.stats_label.configure(text=stats_text)

    def _clear_logs(self):
        """Clear all log entries"""
        from tkinter import messagebox

        if messagebox.askyesno("Clear Logs", "Clear all log entries?"):
            self.log_entries.clear()
            self.filtered_entries.clear()
            self._update_log_display()
            self._update_stats()

    def _export_logs(self):
        """Export logs to file"""
        from tkinter import filedialog

        filename = filedialog.asksaveasfilename(
            title="Export Logs",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("CSV files", "*.csv"),
                ("All files", "*.*"),
            ],
        )

        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("DENSO888 Application Logs\n")
                    f.write("=" * 50 + "\n\n")

                    for entry in self.filtered_entries:
                        timestamp = entry.get("timestamp", "")
                        level = entry.get("level", "INFO")
                        module = entry.get("module", "System")
                        message = entry.get("message", "")

                        f.write(f"[{timestamp}] [{level:8}] [{module:10}] {message}\n")

                from tkinter import messagebox

                messagebox.showinfo("Export Complete", f"Logs exported to {filename}")

            except Exception as e:
                from tkinter import messagebox

                messagebox.showerror("Export Error", f"Failed to export logs: {str(e)}")

    def show(self):
        """Show logs page"""
        self.main_frame.pack(fill="both", expand=True)

    def hide(self):
        """Hide logs page"""
        self.main_frame.pack_forget()

    def refresh(self):
        """Refresh page data"""
        self._refresh_logs()

    def get_widget(self) -> tk.Widget:
        """Get main widget"""
        return self.main_frame


# Fix import in __init__.py
from datetime import timedelta
