#!/usr/bin/env python3
"""
DENSO888 - Enhanced Professional Desktop App
Modern UI/UX with comprehensive functionality
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import tkinter.font as tkFont
import pandas as pd
from pathlib import Path
import threading
import sys
import os
import queue
import time
import json
from datetime import datetime
import subprocess
import webbrowser

# Add existing modules
sys.path.insert(0, str(Path(__file__).parent))

# Try importing required modules with fallback
try:
    from src.config.database import db_manager
    from src.config.settings import settings
    from src.processors.excel_reader import ExcelReader
    from src.processors.data_validator import DataValidator
    from src.processors.database_writer import DatabaseWriter

    MODULES_AVAILABLE = True
except ImportError:
    MODULES_AVAILABLE = False


class ModernTheme:
    """Modern Design System"""

    # Primary Brand Colors (DENSO inspired)
    PRIMARY = "#DC143C"  # Crimson Red
    PRIMARY_DARK = "#B91C3C"  # Dark Red
    PRIMARY_LIGHT = "#FCA5A5"  # Light Red

    # Neutral Colors
    WHITE = "#FFFFFF"
    SURFACE = "#FEFEFE"
    BACKGROUND = "#F8FAFC"
    CARD = "#FFFFFF"

    # Text Colors
    TEXT_PRIMARY = "#1F2937"  # Gray 800
    TEXT_SECONDARY = "#6B7280"  # Gray 500
    TEXT_DISABLED = "#9CA3AF"  # Gray 400

    # Status Colors
    SUCCESS = "#10B981"  # Emerald 500
    WARNING = "#F59E0B"  # Amber 500
    ERROR = "#EF4444"  # Red 500
    INFO = "#3B82F6"  # Blue 500

    # Borders & Shadows
    BORDER = "#E5E7EB"  # Gray 200
    SHADOW = "#0000001A"  # Black 10%


class ModernButton(tk.Button):
    """Enhanced Modern Button with animations"""

    def __init__(self, parent, text="", command=None, style="primary", **kwargs):

        styles = {
            "primary": {
                "bg": ModernTheme.PRIMARY,
                "fg": ModernTheme.WHITE,
                "active_bg": ModernTheme.PRIMARY_DARK,
                "hover_bg": ModernTheme.PRIMARY_DARK,
            },
            "secondary": {
                "bg": ModernTheme.SURFACE,
                "fg": ModernTheme.TEXT_PRIMARY,
                "active_bg": ModernTheme.BACKGROUND,
                "hover_bg": ModernTheme.BACKGROUND,
                "relief": "solid",
                "bd": 1,
            },
            "success": {
                "bg": ModernTheme.SUCCESS,
                "fg": ModernTheme.WHITE,
                "active_bg": "#059669",
                "hover_bg": "#059669",
            },
            "warning": {
                "bg": ModernTheme.WARNING,
                "fg": ModernTheme.WHITE,
                "active_bg": "#D97706",
                "hover_bg": "#D97706",
            },
        }

        button_style = styles.get(style, styles["primary"])

        super().__init__(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            bg=button_style["bg"],
            fg=button_style["fg"],
            activebackground=button_style["active_bg"],
            **kwargs,
        )

        self.default_bg = button_style["bg"]
        self.hover_bg = button_style["hover_bg"]

        # Hover effects
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, event):
        self.configure(bg=self.hover_bg)

    def _on_leave(self, event):
        self.configure(bg=self.default_bg)


class ModernCard(tk.Frame):
    """Material Design Card Component"""

    def __init__(self, parent, title="", icon="", **kwargs):
        super().__init__(
            parent,
            bg=ModernTheme.CARD,
            relief="flat",
            bd=1,
            highlightbackground=ModernTheme.BORDER,
            highlightthickness=1,
            **kwargs,
        )

        if title:
            header_frame = tk.Frame(self, bg=ModernTheme.CARD)
            header_frame.pack(fill="x", padx=20, pady=(20, 10))

            title_frame = tk.Frame(header_frame, bg=ModernTheme.CARD)
            title_frame.pack(fill="x")

            if icon:
                icon_label = tk.Label(
                    title_frame,
                    text=icon,
                    font=("Segoe UI", 16),
                    bg=ModernTheme.CARD,
                    fg=ModernTheme.PRIMARY,
                )
                icon_label.pack(side="left", padx=(0, 10))

            title_label = tk.Label(
                title_frame,
                text=title,
                font=("Segoe UI", 14, "bold"),
                bg=ModernTheme.CARD,
                fg=ModernTheme.TEXT_PRIMARY,
            )
            title_label.pack(side="left")


class StatusIndicator(tk.Frame):
    """Animated Status Indicator"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=ModernTheme.CARD, **kwargs)

        self.canvas = tk.Canvas(
            self, width=12, height=12, bg=ModernTheme.CARD, highlightthickness=0
        )
        self.canvas.pack(side="left", padx=(0, 8))

        self.label = tk.Label(
            self,
            text="Ready",
            font=("Segoe UI", 9),
            bg=ModernTheme.CARD,
            fg=ModernTheme.TEXT_SECONDARY,
        )
        self.label.pack(side="left")

        self.set_status("idle", "Ready")

    def set_status(self, status, text):
        """Update status with animation"""
        colors = {
            "idle": ModernTheme.TEXT_DISABLED,
            "working": ModernTheme.WARNING,
            "success": ModernTheme.SUCCESS,
            "error": ModernTheme.ERROR,
            "info": ModernTheme.INFO,
        }

        color = colors.get(status, ModernTheme.TEXT_DISABLED)

        self.canvas.delete("all")
        self.canvas.create_oval(2, 2, 10, 10, fill=color, outline=color)
        self.label.configure(text=text)


class ProgressCard(ModernCard):
    """Enhanced Progress Display"""

    def __init__(self, parent):
        super().__init__(parent, title="Processing Status", icon="⚡")

        content_frame = tk.Frame(self, bg=ModernTheme.CARD)
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Status indicator
        self.status_indicator = StatusIndicator(content_frame)
        self.status_indicator.pack(anchor="w", pady=(0, 15))

        # Progress bar with percentage
        progress_frame = tk.Frame(content_frame, bg=ModernTheme.CARD)
        progress_frame.pack(fill="x", pady=(0, 10))

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode="determinate",
            style="Modern.Horizontal.TProgressbar",
        )
        self.progress_bar.pack(fill="x", side="left", expand=True)

        self.progress_label = tk.Label(
            progress_frame,
            text="0%",
            font=("Segoe UI", 9, "bold"),
            bg=ModernTheme.CARD,
            fg=ModernTheme.TEXT_PRIMARY,
            width=5,
        )
        self.progress_label.pack(side="right", padx=(10, 0))

        # Statistics grid
        stats_frame = tk.Frame(content_frame, bg=ModernTheme.CARD)
        stats_frame.pack(fill="x", pady=(10, 0))
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.stats = {}
        self.create_stat("Rows", "0", 0, 0)
        self.create_stat("Speed", "0/s", 0, 1)
        self.create_stat("Time", "0s", 0, 2)

    def create_stat(self, label, value, row, col):
        """Create a statistic display"""
        stat_frame = tk.Frame(self, bg=ModernTheme.BACKGROUND, relief="solid", bd=1)
        stat_frame.grid(
            row=row,
            column=col,
            padx=2,
            pady=2,
            sticky="ew",
            in_=self.children[list(self.children.keys())[-1]],
        )

        value_label = tk.Label(
            stat_frame,
            text=value,
            font=("Segoe UI", 12, "bold"),
            bg=ModernTheme.BACKGROUND,
            fg=ModernTheme.PRIMARY,
        )
        value_label.pack(pady=(8, 2))

        label_label = tk.Label(
            stat_frame,
            text=label,
            font=("Segoe UI", 8),
            bg=ModernTheme.BACKGROUND,
            fg=ModernTheme.TEXT_SECONDARY,
        )
        label_label.pack(pady=(0, 8))

        self.stats[label.lower()] = value_label

    def update_progress(self, value, status_text="Processing...", stats=None):
        """Update progress with statistics"""
        self.progress_var.set(value)
        self.progress_label.configure(text=f"{int(value)}%")
        self.status_indicator.set_status(
            "working" if value < 100 else "success", status_text
        )

        if stats:
            for key, value in stats.items():
                if key in self.stats:
                    self.stats[key].configure(text=str(value))


class DENSO888App:
    """Enhanced DENSO888 Desktop Application"""

    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_variables()
        self.setup_styles()
        self.check_dependencies()
        self.setup_ui()

        # Message queue for thread communication
        self.message_queue = queue.Queue()
        self.processing = False

        # Start message handler
        self.handle_messages()

    def setup_window(self):
        """Configure main window"""
        self.root.title("DENSO888 - Professional Excel to Database Import")
        self.root.geometry("1200x800")
        self.root.configure(bg=ModernTheme.BACKGROUND)
        self.root.minsize(1000, 600)

        # Center window
        self.center_window()

        # Configure grid weights
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"+{x}+{y}")

    def setup_variables(self):
        """Initialize tkinter variables"""
        self.selected_file = tk.StringVar()
        self.table_name = tk.StringVar()
        self.selected_sheet = tk.StringVar()
        self.duplicate_action = tk.StringVar(value="replace")
        self.create_table = tk.BooleanVar(value=True)

        # File info
        self.file_info = None

    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()

        # Configure progress bar style
        style.theme_use("clam")
        style.configure(
            "Modern.Horizontal.TProgressbar",
            background=ModernTheme.PRIMARY,
            troughcolor=ModernTheme.BACKGROUND,
            borderwidth=0,
            lightcolor=ModernTheme.PRIMARY,
            darkcolor=ModernTheme.PRIMARY,
        )

    def check_dependencies(self):
        """Check if required modules are available"""
        if not MODULES_AVAILABLE:
            self.show_dependency_dialog()

    def setup_ui(self):
        """Setup main user interface"""
        # Header
        self.create_header()

        # Main content
        main_frame = tk.Frame(self.root, bg=ModernTheme.BACKGROUND)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        # Left panel
        self.create_left_panel(main_frame)

        # Right panel
        self.create_right_panel(main_frame)

    def create_header(self):
        """Create modern header"""
        header_frame = tk.Frame(self.root, bg=ModernTheme.PRIMARY, height=80)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)

        # Logo section
        logo_frame = tk.Frame(header_frame, bg=ModernTheme.PRIMARY)
        logo_frame.grid(row=0, column=0, sticky="w", padx=30)

        # Title
        title_label = tk.Label(
            logo_frame,
            text="DENSO888",
            font=("Segoe UI", 24, "bold"),
            bg=ModernTheme.PRIMARY,
            fg=ModernTheme.WHITE,
        )
        title_label.pack(anchor="w", pady=(15, 0))

        subtitle_label = tk.Label(
            logo_frame,
            text="Professional Data Import Suite",
            font=("Segoe UI", 11),
            bg=ModernTheme.PRIMARY,
            fg=ModernTheme.PRIMARY_LIGHT,
        )
        subtitle_label.pack(anchor="w")

        # Status section
        status_frame = tk.Frame(header_frame, bg=ModernTheme.PRIMARY)
        status_frame.grid(row=0, column=2, sticky="e", padx=30)

        self.header_status = StatusIndicator(status_frame)
        self.header_status.pack(pady=25)

    def create_left_panel(self, parent):
        """Create left configuration panel"""
        left_frame = tk.Frame(parent, bg=ModernTheme.BACKGROUND, width=400)
        left_frame.grid(row=0, column=0, sticky="ns", padx=(0, 15))
        left_frame.grid_propagate(False)

        # File selection card
        self.create_file_card(left_frame)

        # Configuration card
        self.create_config_card(left_frame)

        # Control buttons
        self.create_control_card(left_frame)

    def create_file_card(self, parent):
        """File selection card with preview"""
        file_card = ModernCard(parent, title="Excel File Selection", icon="📁")
        file_card.pack(fill="x", pady=(0, 20))

        content_frame = tk.Frame(file_card, bg=ModernTheme.CARD)
        content_frame.pack(fill="x", padx=20, pady=(0, 20))

        # File display
        self.file_display = tk.Frame(
            content_frame, bg=ModernTheme.BACKGROUND, relief="solid", bd=1, height=60
        )
        self.file_display.pack(fill="x", pady=(0, 15))
        self.file_display.pack_propagate(False)

        self.file_label = tk.Label(
            self.file_display,
            text="No file selected - Click browse to select Excel file",
            font=("Segoe UI", 10),
            bg=ModernTheme.BACKGROUND,
            fg=ModernTheme.TEXT_SECONDARY,
            wraplength=350,
        )
        self.file_label.pack(expand=True)

        # Browse button
        ModernButton(
            content_frame,
            text="📎 Browse Excel Files",
            command=self.select_file,
            style="primary",
        ).pack(anchor="w")

        # File info section (hidden initially)
        self.file_info_frame = tk.Frame(content_frame, bg=ModernTheme.CARD)

    def create_config_card(self, parent):
        """Configuration options card"""
        config_card = ModernCard(parent, title="Import Configuration", icon="⚙️")
        config_card.pack(fill="x", pady=(0, 20))

        content_frame = tk.Frame(config_card, bg=ModernTheme.CARD)
        content_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Table name
        tk.Label(
            content_frame,
            text="Target Table Name:",
            font=("Segoe UI", 10, "bold"),
            bg=ModernTheme.CARD,
            fg=ModernTheme.TEXT_PRIMARY,
        ).pack(anchor="w", pady=(0, 5))

        table_entry = tk.Entry(
            content_frame,
            textvariable=self.table_name,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
            bg=ModernTheme.WHITE,
        )
        table_entry.pack(fill="x", pady=(0, 15))

        # Sheet selection (hidden initially)
        self.sheet_frame = tk.Frame(content_frame, bg=ModernTheme.CARD)

        # Import options
        options_frame = tk.LabelFrame(
            content_frame,
            text="Import Options",
            font=("Segoe UI", 10, "bold"),
            bg=ModernTheme.CARD,
            fg=ModernTheme.TEXT_PRIMARY,
            relief="flat",
            bd=1,
        )
        options_frame.pack(fill="x", pady=(10, 0))

        # Create table option
        tk.Checkbutton(
            options_frame,
            text="Create new table (drop if exists)",
            variable=self.create_table,
            font=("Segoe UI", 10),
            bg=ModernTheme.CARD,
            fg=ModernTheme.TEXT_PRIMARY,
            activebackground=ModernTheme.CARD,
            selectcolor=ModernTheme.WHITE,
        ).pack(anchor="w", padx=10, pady=5)

        # Duplicate handling
        duplicate_frame = tk.Frame(options_frame, bg=ModernTheme.CARD)
        duplicate_frame.pack(fill="x", padx=10, pady=(0, 10))

        tk.Label(
            duplicate_frame,
            text="If table exists:",
            font=("Segoe UI", 9, "bold"),
            bg=ModernTheme.CARD,
            fg=ModernTheme.TEXT_SECONDARY,
        ).pack(anchor="w")

        options = [
            ("Replace data", "replace"),
            ("Append data", "append"),
            ("Skip if exists", "skip"),
        ]

        for text, value in options:
            tk.Radiobutton(
                duplicate_frame,
                text=text,
                variable=self.duplicate_action,
                value=value,
                font=("Segoe UI", 9),
                bg=ModernTheme.CARD,
                fg=ModernTheme.TEXT_PRIMARY,
                activebackground=ModernTheme.CARD,
                selectcolor=ModernTheme.WHITE,
            ).pack(anchor="w", padx=20)

    def create_control_card(self, parent):
        """Control buttons card"""
        control_card = ModernCard(parent, title="Import Control", icon="🚀")
        control_card.pack(fill="x")

        content_frame = tk.Frame(control_card, bg=ModernTheme.CARD)
        content_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Buttons frame
        btn_frame = tk.Frame(content_frame, bg=ModernTheme.CARD)
        btn_frame.pack(fill="x")

        self.start_btn = ModernButton(
            btn_frame,
            text="🚀 Start Import",
            command=self.start_processing,
            style="primary",
        )
        self.start_btn.pack(side="left", padx=(0, 10))

        self.test_btn = ModernButton(
            btn_frame,
            text="🔍 Test Connection",
            command=self.test_connection,
            style="secondary",
        )
        self.test_btn.pack(side="left", padx=(0, 10))

        # Sample data button
        sample_btn = ModernButton(
            btn_frame,
            text="📊 Generate Sample",
            command=self.generate_sample,
            style="secondary",
        )
        sample_btn.pack(side="right")

    def create_right_panel(self, parent):
        """Create right panel with progress and logs"""
        right_frame = tk.Frame(parent, bg=ModernTheme.BACKGROUND)
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.grid_rowconfigure(1, weight=1)

        # Progress card
        self.progress_card = ProgressCard(right_frame)
        self.progress_card.pack(fill="x", pady=(0, 20))

        # Logs card
        logs_card = ModernCard(right_frame, title="Activity Logs", icon="📝")
        logs_card.pack(fill="both", expand=True)

        logs_content = tk.Frame(logs_card, bg=ModernTheme.CARD)
        logs_content.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Logs text area
        text_frame = tk.Frame(logs_content, bg=ModernTheme.CARD)
        text_frame.pack(fill="both", expand=True)

        self.logs_text = tk.Text(
            text_frame,
            font=("Consolas", 9),
            bg=ModernTheme.BACKGROUND,
            fg=ModernTheme.TEXT_PRIMARY,
            relief="flat",
            bd=0,
            wrap="word",
            state="disabled",
        )

        scrollbar = tk.Scrollbar(text_frame, command=self.logs_text.yview)
        self.logs_text.configure(yscrollcommand=scrollbar.set)

        self.logs_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Clear logs button
        clear_btn = ModernButton(
            logs_content,
            text="🗑️ Clear Logs",
            command=self.clear_logs,
            style="secondary",
        )
        clear_btn.pack(anchor="e", pady=(10, 0))

        # Initial log messages
        self.log_message("🎯 DENSO888 Professional Import Tool Ready")
        self.log_message("💡 Select Excel file and configure import settings to begin")
        self.log_message("=" * 60)

    def select_file(self):
        """Enhanced file selection with analysis"""
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")],
        )

        if file_path:
            self.selected_file.set(file_path)
            filename = Path(file_path).name

            # Update display
            self.file_label.configure(text=f"📁 {filename}", fg=ModernTheme.SUCCESS)

            # Auto-generate table name
            table_name = (
                Path(file_path).stem.replace(" ", "_").replace("-", "_").lower()
            )
            self.table_name.set(table_name)

            self.log_message(f"✅ Selected: {filename}")

            # Analyze file in background
            self.analyze_file_async(file_path)

    def analyze_file_async(self, file_path):
        """Analyze Excel file in background thread"""

        def analyze():
            try:
                self.log_message("🔍 Analyzing Excel file structure...")

                # Basic file info
                file_size = Path(file_path).stat().st_size / 1024 / 1024

                # Read Excel info
                with pd.ExcelFile(file_path) as excel_file:
                    sheets = excel_file.sheet_names

                    # Sample first sheet
                    df_sample = pd.read_excel(excel_file, sheet_name=sheets[0], nrows=5)

                    # Count total rows
                    df_full = pd.read_excel(excel_file, sheet_name=sheets[0])
                    total_rows = len(df_full)

                    file_info = {
                        "sheets": sheets,
                        "total_rows": total_rows,
                        "columns": df_sample.columns.tolist(),
                        "file_size_mb": file_size,
                        "sample_data": df_sample.head(3).to_dict("records"),
                    }

                    # Update UI on main thread
                    self.root.after(0, lambda: self.display_file_info(file_info))

            except Exception as e:
                self.root.after(
                    0, lambda: self.log_message(f"❌ File analysis error: {e}")
                )

        threading.Thread(target=analyze, daemon=True).start()

    def display_file_info(self, info):
        """Display file analysis results"""
        self.file_info = info

        # Update file display with details
        details = f"📊 {info['total_rows']:,} rows • {len(info['columns'])} columns • {info['file_size_mb']:.1f} MB"
        self.file_label.configure(text=details)

        # Show sheet selection if multiple sheets
        if len(info["sheets"]) > 1:
            self.show_sheet_selection(info["sheets"])

        self.log_message(
            f"📊 Analysis complete: {info['total_rows']:,} rows, {len(info['columns'])} columns"
        )
        self.log_message(f"📁 File size: {info['file_size_mb']:.1f} MB")

        if len(info["sheets"]) > 1:
            self.log_message(f"📋 Multiple sheets found: {', '.join(info['sheets'])}")

    def show_sheet_selection(self, sheets):
        """Show sheet selection dropdown"""
        self.sheet_frame.pack(fill="x", pady=(0, 15))

        # Clear existing widgets
        for widget in self.sheet_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.sheet_frame,
            text="Select Sheet:",
            font=("Segoe UI", 10, "bold"),
            bg=ModernTheme.CARD,
            fg=ModernTheme.TEXT_PRIMARY,
        ).pack(anchor="w", pady=(0, 5))

        sheet_combo = ttk.Combobox(
            self.sheet_frame,
            textvariable=self.selected_sheet,
            values=sheets,
            state="readonly",
            font=("Segoe UI", 10),
        )
        sheet_combo.pack(fill="x")
        sheet_combo.set(sheets[0])  # Default to first sheet

    def test_connection(self):
        """Test database connection"""
        if not MODULES_AVAILABLE:
            messagebox.showerror(
                "Error", "Required modules not available. Please install dependencies."
            )
            return

        self.test_btn.configure(state="disabled", text="Testing...")
        self.header_status.set_status("working", "Testing connection...")

        def test():
            try:
                success = db_manager.test_connection()

                if success:
                    self.root.after(0, lambda: self.connection_success())
                else:
                    self.root.after(
                        0, lambda: self.connection_failed("Connection test failed")
                    )

            except Exception as e:
                self.root.after(0, lambda: self.connection_failed(str(e)))

        threading.Thread(target=test, daemon=True).start()

    def connection_success(self):
        """Handle successful connection"""
        self.test_btn.configure(state="normal", text="🔍 Test Connection")
        self.header_status.set_status("success", "Database connected")
        self.log_message("✅ Database connection successful")
        messagebox.showinfo("Connection Test", "✅ Database connection successful!")

    def connection_failed(self, error):
        """Handle failed connection"""
        self.test_btn.configure(state="normal", text="🔍 Test Connection")
        self.header_status.set_status("error", "Connection failed")
        self.log_message(f"❌ Connection failed: {error}")
        messagebox.showerror(
            "Connection Failed", f"❌ Database connection failed:\n\n{error}"
        )

    def start_processing(self):
        """Start the import process"""
        # Validation
        if not self.selected_file.get():
            messagebox.showwarning(
                "Validation Error", "Please select an Excel file first"
            )
            return

        if not self.table_name.get().strip():
            messagebox.showwarning("Validation Error", "Please enter a table name")
            return

        if not MODULES_AVAILABLE:
            messagebox.showerror("Error", "Required modules not available")
            return

        # Test connection first
        try:
            if not db_manager.test_connection():
                messagebox.showerror(
                    "Database Error",
                    "Cannot connect to database. Please check connection.",
                )
                return
        except Exception as e:
            messagebox.showerror("Database Error", f"Database connection error: {e}")
            return

        # Confirm import
        confirmation = messagebox.askyesno(
            "Confirm Import",
            (
                f"Start importing data to table '{self.table_name.get()}'?\n\n"
                f"File: {Path(self.selected_file.get()).name}\n"
                f"Rows: {self.file_info['total_rows']:,} (estimated)"
                if self.file_info
                else "Start import process?"
            ),
        )

        if not confirmation:
            return

        # Start processing
        self.processing = True
        self.start_btn.configure(state="disabled", text="🔄 Processing...")
        self.header_status.set_status("working", "Import in progress")

        self.log_message("🚀 Starting Excel import process...")

        # Start worker thread
        threading.Thread(target=self.import_worker, daemon=True).start()

    def import_worker(self):
        """Background worker for import process"""
        try:
            start_time = time.time()
            file_path = self.selected_file.get()
            table_name = self.table_name.get().strip()
            sheet_name = (
                self.selected_sheet.get() if self.selected_sheet.get() else None
            )

            self.send_message(
                "progress", {"value": 5, "text": "Initializing import..."}
            )

            # Initialize processors
            reader = ExcelReader(file_path, sheet_name)
            validator = DataValidator()
            writer = DatabaseWriter(table_name)

            self.send_message(
                "progress", {"value": 10, "text": "Reading Excel file..."}
            )

            # Get file info
            info = reader.get_sheet_info()
            total_rows = info["total_rows"]

            self.send_message(
                "progress", {"value": 20, "text": f"Analyzing {total_rows:,} rows..."}
            )

            # Auto-detect column types
            type_mapping = self.detect_column_types(info["columns"])

            self.send_message(
                "progress", {"value": 30, "text": "Creating database table..."}
            )

            # Create table if needed
            if self.create_table.get():
                # Get sample data for table creation
                first_chunk = next(reader.read_chunks(chunk_size=100))
                clean_chunk = validator.clean_dataframe(first_chunk)
                typed_chunk = validator.validate_data_types(clean_chunk, type_mapping)

                writer.create_table_from_dataframe(
                    typed_chunk, type_mapping=type_mapping
                )
                self.send_message("log", f"✅ Created table: {table_name}")

            self.send_message(
                "progress", {"value": 40, "text": "Starting data import..."}
            )

            # Process data in chunks
            reader = ExcelReader(file_path, sheet_name)  # Reset reader
            total_inserted = 0
            chunk_count = 0

            for chunk in reader.read_chunks(chunk_size=5000):
                chunk_count += 1

                # Clean and validate
                clean_chunk = validator.clean_dataframe(chunk)
                typed_chunk = validator.validate_data_types(clean_chunk, type_mapping)

                # Insert data
                inserted = writer.bulk_insert_batch(typed_chunk)
                total_inserted += inserted

                # Calculate progress
                progress = 40 + (total_inserted / total_rows) * 50
                elapsed = time.time() - start_time
                speed = total_inserted / elapsed if elapsed > 0 else 0

                self.send_message(
                    "progress",
                    {
                        "value": min(progress, 90),
                        "text": f"Imported {total_inserted:,}/{total_rows:,} rows",
                        "stats": {
                            "rows": f"{total_inserted:,}",
                            "speed": f"{speed:.0f}/s",
                            "time": f"{elapsed:.1f}s",
                        },
                    },
                )

            # Verify results
            self.send_message("progress", {"value": 95, "text": "Verifying import..."})

            table_info = writer.get_table_info()
            final_count = table_info.get("row_count", total_inserted)
            total_time = time.time() - start_time

            # Success
            self.send_message(
                "complete",
                {
                    "total_rows": total_rows,
                    "inserted_rows": final_count,
                    "table_name": table_name,
                    "time": total_time,
                },
            )

        except Exception as e:
            self.send_message("error", str(e))

    def send_message(self, msg_type, data):
        """Send message to main thread"""
        self.message_queue.put((msg_type, data))

    def handle_messages(self):
        """Handle messages from worker thread"""
        try:
            while True:
                try:
                    msg_type, data = self.message_queue.get_nowait()

                    if msg_type == "progress":
                        self.progress_card.update_progress(
                            data["value"], data["text"], data.get("stats")
                        )

                    elif msg_type == "log":
                        self.log_message(data)

                    elif msg_type == "complete":
                        self.import_complete(data)

                    elif msg_type == "error":
                        self.import_error(data)

                except queue.Empty:
                    break

        except Exception:
            pass

        # Schedule next check
        self.root.after(100, self.handle_messages)

    def import_complete(self, results):
        """Handle successful import completion"""
        self.processing = False
        self.start_btn.configure(state="normal", text="🚀 Start Import")
        self.header_status.set_status("success", "Import completed")

        # Final progress update
        self.progress_card.update_progress(
            100,
            "Import completed successfully!",
            {
                "rows": f"{results['inserted_rows']:,}",
                "speed": f"{results['inserted_rows']/results['time']:.0f}/s",
                "time": f"{results['time']:.1f}s",
            },
        )

        success_message = f"""
✅ Import Completed Successfully!

📊 Results:
• Total rows processed: {results['total_rows']:,}
• Rows inserted: {results['inserted_rows']:,}
• Processing time: {results['time']:.2f} seconds
• Average speed: {results['inserted_rows']/results['time']:.0f} rows/second

🗄️ Table: {results['table_name']}
🔗 Database: {settings.DB_NAME if MODULES_AVAILABLE else 'excel_to_db'}
        """.strip()

        self.log_message("🎉 Import completed successfully!")
        self.log_message(f"📊 Processed: {results['total_rows']:,} rows")
        self.log_message(f"✅ Inserted: {results['inserted_rows']:,} rows")
        self.log_message(f"⏱️ Time: {results['time']:.2f} seconds")
        self.log_message("=" * 60)

        messagebox.showinfo("Import Successful", success_message)

    def import_error(self, error_message):
        """Handle import error"""
        self.processing = False
        self.start_btn.configure(state="normal", text="🚀 Start Import")
        self.header_status.set_status("error", "Import failed")

        self.log_message(f"❌ Import failed: {error_message}")
        messagebox.showerror(
            "Import Failed", f"Import process failed:\n\n{error_message}"
        )

    def generate_sample(self):
        """Generate sample Excel file with enhanced data"""
        try:
            # Create sample data directory
            Path("data/samples").mkdir(parents=True, exist_ok=True)

            # Enhanced sample data
            import random
            from datetime import datetime, timedelta

            # Generate realistic business data
            companies = [
                "บริษัท เทค จำกัด",
                "ห้างหุ้นส่วน ดิจิทัล",
                "บจก. อินโนเวชั่น",
                "สมาคม เทคโนโลยี",
            ]
            products = [
                "โน้ตบุ๊ค",
                "คอมพิวเตอร์",
                "โทรศัพท์",
                "แท็บเล็ต",
                "เครื่องพิมพ์",
                "จอมอนิเตอร์",
            ]
            names = ["สมชาย ใจดี", "สมหญิง รักดี", "วิชัย เจริญ", "นารี สุขใส", "ประเสริฐ มั่นคง"]

            # Create comprehensive dataset
            data = {
                "OrderID": [f"ORD{i+1:06d}" for i in range(2000)],
                "OrderDate": [
                    (datetime.now() - timedelta(days=random.randint(0, 365))).strftime(
                        "%Y-%m-%d"
                    )
                    for _ in range(2000)
                ],
                "CustomerName": [random.choice(names) for _ in range(2000)],
                "Company": [random.choice(companies) for _ in range(2000)],
                "ProductName": [random.choice(products) for _ in range(2000)],
                "Quantity": [random.randint(1, 50) for _ in range(2000)],
                "UnitPrice": [random.uniform(1000, 50000) for _ in range(2000)],
                "Discount": [random.choice([0, 5, 10, 15, 20]) for _ in range(2000)],
                "TotalAmount": [0] * 2000,
                "Status": [
                    random.choice(["Pending", "Completed", "Cancelled", "Shipped"])
                    for _ in range(2000)
                ],
                "SalesRep": [random.choice(names) for _ in range(2000)],
                "Notes": [
                    random.choice(["", "ลูกค้า VIP", "จัดส่งด่วน", "ชำระเงินแล้ว", ""])
                    for _ in range(2000)
                ],
            }

            # Calculate total amount
            for i in range(2000):
                subtotal = data["Quantity"][i] * data["UnitPrice"][i]
                discount_amount = subtotal * (data["Discount"][i] / 100)
                data["TotalAmount"][i] = round(subtotal - discount_amount, 2)

            df = pd.DataFrame(data)
            sample_file = "data/samples/enhanced_business_data.xlsx"
            df.to_excel(sample_file, index=False)

            # Auto-select the generated file
            self.selected_file.set(str(Path(sample_file).absolute()))
            self.file_label.configure(
                text=f"📁 {Path(sample_file).name} (Generated)", fg=ModernTheme.SUCCESS
            )

            # Auto-generate table name
            self.table_name.set("sample_business_data")

            self.log_message(f"✅ Generated sample data: {sample_file}")
            self.log_message(
                f"📊 Sample contains: {len(df):,} rows, {len(df.columns)} columns"
            )

            # Analyze the generated file
            self.analyze_file_async(str(Path(sample_file).absolute()))

            messagebox.showinfo(
                "Sample Generated",
                f"✅ Sample data generated successfully!\n\n"
                f"📁 File: {sample_file}\n"
                f"📊 Data: {len(df):,} rows, {len(df.columns)} columns\n\n"
                f"The file has been automatically selected for import.",
            )

        except Exception as e:
            self.log_message(f"❌ Sample generation error: {e}")
            messagebox.showerror("Error", f"Failed to generate sample data:\n\n{e}")

    def detect_column_types(self, columns):
        """Enhanced column type detection"""
        type_mapping = {}
        patterns = {
            "datetime": [
                "date",
                "time",
                "วันที่",
                "เวลา",
                "created",
                "updated",
                "timestamp",
            ],
            "integer": [
                "id",
                "age",
                "count",
                "number",
                "จำนวน",
                "อายุ",
                "quantity",
                "qty",
            ],
            "float": [
                "price",
                "salary",
                "amount",
                "total",
                "value",
                "ราคา",
                "เงินเดือน",
                "discount",
                "percent",
            ],
            "boolean": ["active", "enabled", "is_", "has_", "flag", "status_flag"],
        }

        for column in columns:
            col_lower = column.lower()
            column_type = "string"  # default

            for data_type, pattern_list in patterns.items():
                if any(pattern in col_lower for pattern in pattern_list):
                    column_type = data_type
                    break

            type_mapping[column] = column_type

        return type_mapping

    def log_message(self, message):
        """Add timestamped message to logs"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"

        self.logs_text.configure(state="normal")
        self.logs_text.insert("end", formatted_message)
        self.logs_text.see("end")
        self.logs_text.configure(state="disabled")

    def clear_logs(self):
        """Clear all log messages"""
        self.logs_text.configure(state="normal")
        self.logs_text.delete("1.0", "end")
        self.logs_text.configure(state="disabled")
        self.log_message("🗑️ Logs cleared")

    def show_dependency_dialog(self):
        """Show dependency installation dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Missing Dependencies")
        dialog.geometry("600x500")
        dialog.configure(bg=ModernTheme.SURFACE)
        dialog.grab_set()
        dialog.resizable(False, False)

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"+{x}+{y}")

        # Header
        header_frame = tk.Frame(dialog, bg=ModernTheme.ERROR, height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="⚠️ Missing Dependencies",
            font=("Segoe UI", 16, "bold"),
            bg=ModernTheme.ERROR,
            fg=ModernTheme.WHITE,
        ).pack(pady=25)

        # Content
        content_frame = tk.Frame(dialog, bg=ModernTheme.SURFACE)
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Message
        message_label = tk.Label(
            content_frame,
            text="Required Python packages are missing for database functionality:",
            font=("Segoe UI", 11),
            bg=ModernTheme.SURFACE,
            fg=ModernTheme.TEXT_PRIMARY,
            wraplength=540,
        )
        message_label.pack(anchor="w", pady=(0, 20))

        # Requirements list
        req_frame = tk.Frame(
            content_frame, bg=ModernTheme.BACKGROUND, relief="solid", bd=1
        )
        req_frame.pack(fill="x", pady=(0, 20))

        requirements = [
            "pandas>=2.0.0",
            "sqlalchemy>=2.0.0",
            "pyodbc>=4.0.39",
            "openpyxl>=3.1.0",
            "python-dotenv>=1.0.0",
        ]

        for req in requirements:
            tk.Label(
                req_frame,
                text=f"• {req}",
                font=("Consolas", 10),
                bg=ModernTheme.BACKGROUND,
                fg=ModernTheme.TEXT_PRIMARY,
                anchor="w",
            ).pack(fill="x", padx=15, pady=2)

        # Installation command
        tk.Label(
            content_frame,
            text="Installation command:",
            font=("Segoe UI", 11, "bold"),
            bg=ModernTheme.SURFACE,
            fg=ModernTheme.TEXT_PRIMARY,
        ).pack(anchor="w", pady=(10, 5))

        cmd_frame = tk.Frame(
            content_frame, bg=ModernTheme.BACKGROUND, relief="solid", bd=1
        )
        cmd_frame.pack(fill="x", pady=(0, 20))

        cmd_text = "pip install pandas sqlalchemy pyodbc openpyxl python-dotenv"
        tk.Label(
            cmd_frame,
            text=cmd_text,
            font=("Consolas", 10),
            bg=ModernTheme.BACKGROUND,
            fg=ModernTheme.TEXT_PRIMARY,
            wraplength=540,
        ).pack(padx=15, pady=10)

        # Buttons
        btn_frame = tk.Frame(content_frame, bg=ModernTheme.SURFACE)
        btn_frame.pack(fill="x")

        def auto_install():
            try:
                self.log_message("🔄 Installing dependencies...")
                result = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        "pandas",
                        "sqlalchemy",
                        "pyodbc",
                        "openpyxl",
                        "python-dotenv",
                    ],
                    capture_output=True,
                    text=True,
                )

                if result.returncode == 0:
                    messagebox.showinfo(
                        "Installation Complete",
                        "✅ Dependencies installed successfully!\n\nPlease restart the application.",
                    )
                    dialog.destroy()
                    self.root.quit()
                else:
                    messagebox.showerror(
                        "Installation Failed",
                        f"❌ Installation failed:\n\n{result.stderr}",
                    )
            except Exception as e:
                messagebox.showerror("Error", f"Installation error:\n\n{e}")

        def open_help():
            webbrowser.open("https://pip.pypa.io/en/stable/installation/")

        ModernButton(
            btn_frame, "🔄 Auto Install", command=auto_install, style="primary"
        ).pack(side="left")
        ModernButton(btn_frame, "❓ Help", command=open_help, style="secondary").pack(
            side="left", padx=(10, 0)
        )
        ModernButton(
            btn_frame, "❌ Close", command=dialog.destroy, style="secondary"
        ).pack(side="right")

    def run(self):
        """Run the application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    try:
        # Try to load environment variables
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        pass

    # Create and run application
    app = DENSO888App()
    app.run()


if __name__ == "__main__":
    main()
