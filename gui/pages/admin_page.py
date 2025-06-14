""" "
Admin Dashboard สำหรับตรวจสอบการใช้งาน
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta


class AdminPage:
    def __init__(self, parent: tk.Widget, controller, theme):
        self.parent = parent
        self.controller = controller
        self.theme = theme

        # Import tracker
        from admin.user_tracker import UserActivityTracker

        self.tracker = UserActivityTracker()

        self.main_frame = None
        self._create_admin_page()

    def _create_admin_page(self):
        """สร้าง Admin Dashboard"""
        self.main_frame = tk.Frame(self.parent, bg=self.theme.colors.background)

        # Admin Header
        header_frame = tk.Frame(
            self.main_frame, bg=self.theme.colors.primary, height=80
        )
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="🛡️ Admin Dashboard - User Activity Monitor",
            font=self.theme.fonts["heading_lg"],
            bg=self.theme.colors.primary,
            fg="white",
        )
        title_label.pack(expand=True)

        # Create sections
        self._create_stats_section()
        self._create_ip_monitor_section()
        self._create_activity_log_section()
        self._create_actions_section()

        # Auto refresh
        self._schedule_refresh()

    def _create_stats_section(self):
        """สถิติการใช้งาน"""
        stats_frame = self._create_section("📊 Usage Statistics")

        # Stats cards
        cards_frame = tk.Frame(stats_frame, bg=self.theme.colors.surface)
        cards_frame.pack(fill="x", pady=(0, 20))

        # Get stats
        activities = self.tracker.get_activities(1000)
        ip_summary = self.tracker.get_ip_summary()

        # Today's activities
        today = datetime.now().date()
        today_activities = [
            a
            for a in activities
            if datetime.fromisoformat(a["timestamp"]).date() == today
        ]

        stats = [
            ("Total Sessions", len(activities), "🔢"),
            ("Today's Activity", len(today_activities), "📅"),
            ("Unique IPs", len(ip_summary), "🌐"),
            (
                "Most Active IP",
                (
                    max(ip_summary.keys(), key=lambda k: ip_summary[k])
                    if ip_summary
                    else "N/A"
                ),
                "🎯",
            ),
        ]

        for i, (label, value, icon) in enumerate(stats):
            self._create_stat_card(cards_frame, icon, label, str(value), i)

    def _create_stat_card(self, parent, icon, label, value, index):
        """สร้าง Card สถิติ"""
        card = tk.Frame(parent, bg=self.theme.colors.surface_dark, padx=20, pady=15)
        card.grid(row=0, column=index, padx=10, pady=5, sticky="ew")

        # Icon
        icon_label = tk.Label(
            card,
            text=icon,
            font=("Segoe UI", 24),
            bg=self.theme.colors.surface_dark,
            fg=self.theme.colors.primary,
        )
        icon_label.pack()

        # Value
        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 18, "bold"),
            bg=self.theme.colors.surface_dark,
            fg=self.theme.colors.text_primary,
        )
        value_label.pack()

        # Label
        label_label = tk.Label(
            card,
            text=label,
            font=self.theme.fonts["body_sm"],
            bg=self.theme.colors.surface_dark,
            fg=self.theme.colors.text_secondary,
        )
        label_label.pack()

        # Configure grid
        parent.grid_columnconfigure(index, weight=1)

    def _create_ip_monitor_section(self):
        """ตรวจสอบ IP Address"""
        ip_frame = self._create_section("🌐 IP Address Monitor")

        # IP summary table
        ip_tree = ttk.Treeview(
            ip_frame, columns=("ip", "count", "last_seen"), show="headings", height=6
        )

        # Configure columns
        ip_tree.heading("ip", text="IP Address")
        ip_tree.heading("count", text="Sessions")
        ip_tree.heading("last_seen", text="Last Seen")

        ip_tree.column("ip", width=200)
        ip_tree.column("count", width=100, anchor="center")
        ip_tree.column("last_seen", width=200)

        # Populate IP data
        ip_summary = self.tracker.get_ip_summary()
        activities = self.tracker.get_activities(1000)

        for ip, count in ip_summary.items():
            # Find last activity for this IP
            ip_activities = [a for a in activities if a.get("ip_address") == ip]
            if ip_activities:
                last_seen = datetime.fromisoformat(
                    ip_activities[-1]["timestamp"]
                ).strftime("%Y-%m-%d %H:%M")
            else:
                last_seen = "Unknown"

            ip_tree.insert("", "end", values=(ip, count, last_seen))

        ip_tree.pack(fill="both", expand=True, pady=(0, 10))

        # Add scrollbar
        scrollbar = ttk.Scrollbar(ip_frame, orient="vertical", command=ip_tree.yview)
        ip_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def _create_activity_log_section(self):
        """รายการ Activity Log"""
        log_frame = self._create_section("📝 Recent Activities")

        # Activity tree
        self.activity_tree = ttk.Treeview(
            log_frame,
            columns=("time", "ip", "action", "details"),
            show="headings",
            height=8,
        )

        # Configure columns
        self.activity_tree.heading("time", text="Time")
        self.activity_tree.heading("ip", text="IP Address")
        self.activity_tree.heading("action", text="Action")
        self.activity_tree.heading("details", text="Details")

        self.activity_tree.column("time", width=150)
        self.activity_tree.column("ip", width=120)
        self.activity_tree.column("action", width=150)
        self.activity_tree.column("details", width=300)

        self._refresh_activity_log()

        self.activity_tree.pack(fill="both", expand=True, pady=(0, 10))

        # Scrollbar for activities
        activity_scroll = ttk.Scrollbar(
            log_frame, orient="vertical", command=self.activity_tree.yview
        )
        self.activity_tree.configure(yscrollcommand=activity_scroll.set)
        activity_scroll.pack(side="right", fill="y")

    def _create_actions_section(self):
        """Actions สำหรับ Admin"""
        actions_frame = self._create_section("⚡ Admin Actions")

        buttons_frame = tk.Frame(actions_frame, bg=self.theme.colors.surface)
        buttons_frame.pack(fill="x")

        # Refresh button
        refresh_btn = tk.Button(
            buttons_frame,
            text="🔄 Refresh Data",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.info,
            fg="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self._manual_refresh,
        )
        refresh_btn.pack(side="left", padx=(0, 10))

        # Export logs button
        export_btn = tk.Button(
            buttons_frame,
            text="📊 Export Logs",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.success,
            fg="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self._export_logs,
        )
        export_btn.pack(side="left", padx=(0, 10))

        # Clear old logs button
        clear_btn = tk.Button(
            buttons_frame,
            text="🗑️ Clear Old Logs",
            font=self.theme.fonts["body_md"],
            bg=self.theme.colors.warning,
            fg="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self._clear_old_logs,
        )
        clear_btn.pack(side="left")

    def _create_section(self, title: str) -> tk.Widget:
        """สร้าง Section"""
        container = tk.Frame(self.main_frame, bg=self.theme.colors.background)
        container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Title
        title_label = tk.Label(
            container,
            text=title,
            font=self.theme.fonts["heading_md"],
            bg=self.theme.colors.background,
            fg=self.theme.colors.text_primary,
        )
        title_label.pack(anchor="w", pady=(0, 15))

        # Content frame
        content_frame = tk.Frame(
            container,
            bg=self.theme.colors.surface,
            relief="flat",
            bd=1,
            padx=25,
            pady=25,
        )
        content_frame.pack(fill="both", expand=True)

        return content_frame

    def _refresh_activity_log(self):
        """รีเฟรช Activity Log"""
        # Clear existing items
        for item in self.activity_tree.get_children():
            self.activity_tree.delete(item)

        # Load recent activities
        activities = self.tracker.get_activities(50)

        for activity in reversed(activities):  # Show newest first
            time_str = datetime.fromisoformat(activity["timestamp"]).strftime(
                "%H:%M:%S"
            )
            ip = activity.get("ip_address", "unknown")
            action = activity.get("action", "unknown")
            details = str(activity.get("details", ""))[:100]  # Limit length

            self.activity_tree.insert("", "end", values=(time_str, ip, action, details))

    def _manual_refresh(self):
        """Manual refresh"""
        self._refresh_activity_log()
        # Recreate stats section
        for widget in self.main_frame.winfo_children():
            if hasattr(widget, "destroy"):
                widget.destroy()
        self._create_admin_page()

    def _export_logs(self):
        """Export logs to file"""
        from tkinter import filedialog, messagebox

        filename = filedialog.asksaveasfilename(
            title="Export Activity Logs",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )

        if filename:
            try:
                activities = self.tracker.get_activities(1000)
                import json

                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(activities, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Export Success", f"Logs exported to {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export: {e}")

    def _clear_old_logs(self):
        """Clear logs older than 30 days"""
        from tkinter import messagebox

        if messagebox.askyesno("Clear Old Logs", "Clear logs older than 30 days?"):
            try:
                cutoff_date = datetime.now() - timedelta(days=30)
                activities = self.tracker.get_activities(1000)

                filtered_activities = [
                    a
                    for a in activities
                    if datetime.fromisoformat(a["timestamp"]) > cutoff_date
                ]

                # Save filtered logs
                import json

                with open(self.tracker.log_file, "w", encoding="utf-8") as f:
                    json.dump(filtered_activities, f, indent=2, ensure_ascii=False)

                removed_count = len(activities) - len(filtered_activities)
                messagebox.showinfo(
                    "Clear Complete", f"Removed {removed_count} old log entries"
                )

                self._manual_refresh()

            except Exception as e:
                messagebox.showerror("Clear Error", f"Failed to clear logs: {e}")

    def _schedule_refresh(self):
        """Auto refresh every 30 seconds"""
        self._refresh_activity_log()
        self.main_frame.after(30000, self._schedule_refresh)

    def show(self):
        """Show admin page"""
        self.main_frame.pack(fill="both", expand=True)

    def hide(self):
        """Hide admin page"""
        self.main_frame.pack_forget()

    def get_widget(self) -> tk.Widget:
        """Get main widget"""
        return self.main_frame
