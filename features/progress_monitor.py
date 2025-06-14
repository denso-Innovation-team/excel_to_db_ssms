"""
Progress Monitor Widget
แสดง progress bar และสถานะการทำงาน
"""

import tkinter as tk
from tkinter import ttk


class ProgressMonitor:
    """Modern Progress Monitor Component"""

    def __init__(self, parent: tk.Widget, title: str = "Processing..."):
        self.parent = parent
        self.title = title
        self.cancelled = False

        self.create_window()

    def create_window(self):
        """Create progress monitor window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title(self.title)
        self.window.geometry("500x250")
        self.window.configure(bg="#FFFFFF")
        self.window.resizable(False, False)
        self.window.grab_set()
        self.window.transient(self.parent)

        # Center window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - 250
        y = (self.window.winfo_screenheight() // 2) - 125
        self.window.geometry(f"500x250+{x}+{y}")

        self.create_widgets()

    def create_widgets(self):
        """Create progress widgets"""
        main_frame = tk.Frame(self.window, bg="#FFFFFF")
        main_frame.pack(fill="both", expand=True, padx=40, pady=30)

        # Header
        header_frame = tk.Frame(main_frame, bg="#FFFFFF")
        header_frame.pack(fill="x", pady=(0, 20))

        # Icon and title
        icon_label = tk.Label(
            header_frame, text="🏭", font=("Segoe UI", 24), fg="#DC0003", bg="#FFFFFF"
        )
        icon_label.pack(side="left")

        title_label = tk.Label(
            header_frame,
            text="DENSO888 Processing",
            font=("Segoe UI", 16, "bold"),
            fg="#2C3E50",
            bg="#FFFFFF",
        )
        title_label.pack(side="left", padx=(15, 0))

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            length=400,
            mode="determinate",
            style="DENSO.Horizontal.TProgressbar",
        )
        self.progress_bar.pack(pady=(0, 15))

        # Status labels
        self.status_var = tk.StringVar(value="Initializing...")
        self.status_label = tk.Label(
            main_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 12, "bold"),
            fg="#2C3E50",
            bg="#FFFFFF",
        )
        self.status_label.pack(pady=(0, 5))

        self.details_var = tk.StringVar(value="")
        self.details_label = tk.Label(
            main_frame,
            textvariable=self.details_var,
            font=("Segoe UI", 10),
            fg="#7F8C8D",
            bg="#FFFFFF",
        )
        self.details_label.pack(pady=(0, 20))

        # Cancel button
        self.cancel_btn = tk.Button(
            main_frame,
            text="Cancel",
            command=self.cancel,
            font=("Segoe UI", 11),
            bg="#DC3545",
            fg="#FFFFFF",
            relief="flat",
            padx=25,
            pady=8,
            cursor="hand2",
        )
        self.cancel_btn.pack()

        # Configure progress bar style
        style = ttk.Style()
        style.configure(
            "DENSO.Horizontal.TProgressbar",
            background="#DC0003",
            troughcolor="#E9ECEF",
            borderwidth=0,
            lightcolor="#DC0003",
            darkcolor="#DC0003",
        )

    def update(self, progress: float, status: str, details: str = ""):
        """Update progress"""
        if not self.window.winfo_exists():
            return

        self.progress_var.set(progress)
        self.status_var.set(status)
        self.details_var.set(details)

        self.window.update()

    def cancel(self):
        """Cancel operation"""
        self.cancelled = True
        self.close()

    def is_cancelled(self) -> bool:
        """Check if cancelled"""
        return self.cancelled

    def close(self):
        """Close progress window"""
        if self.window.winfo_exists():
            self.window.grab_release()
            self.window.destroy()
