#!/usr/bin/env python3
"""
DENSO888 Authentication System Upgrade
ปรับปรุงระบบ Auth ให้ยืดหยุ่นและสวยงาม + ปรับปรุง UX
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any


class AuthConfigManager:
    """จัดการการตั้งค่า Authentication"""

    def __init__(self):
        self.config_file = Path("auth_config.json")
        self.default_config = {
            "authentication": {
                "enabled": True,
                "guest_mode": True,
                "auto_login": False,
                "remember_user": True,
                "session_timeout": 3600,
            },
            "database_access": {
                "guest_restrictions": {
                    "sqlite_only": True,
                    "max_rows": 10000,
                    "no_delete": True,
                    "read_only_mode": False,
                },
                "authenticated_access": {
                    "all_databases": True,
                    "unlimited_rows": True,
                    "full_permissions": True,
                },
            },
            "ui_settings": {
                "show_advanced_options": False,
                "default_database": "sqlite",
                "startup_mode": "guided",
            },
        }

    def load_config(self) -> Dict[str, Any]:
        """โหลดการตั้งค่า auth"""
        try:
            if self.config_file.exists():
                with open(self.config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return self.default_config.copy()
        except Exception:
            return self.default_config.copy()

    def save_config(self, config: Dict[str, Any]) -> bool:
        """บันทึกการตั้งค่า"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False


class ModernLoginDialog:
    """หน้าต่าง Login ที่สวยงามและ Modern"""

    def __init__(self, parent, auth_manager, config_manager):
        self.auth_manager = auth_manager
        self.config_manager = config_manager
        self.config = config_manager.load_config()
        self.success = False
        self.selected_mode = "authenticated"  # authenticated, guest, skip

        # สร้างหน้าต่างหลัก
        self.dialog = tk.Toplevel(parent)
        self._setup_window()
        self._create_modern_ui()

    def _setup_window(self):
        """ตั้งค่าหน้าต่าง"""
        self.dialog.title("DENSO888 - Choose Your Experience")
        self.dialog.geometry("600x500")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()

        # ตั้งค่าให้อยู่กลางจอ
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"600x500+{x}+{y}")

        # Modern styling
        self.dialog.configure(bg="#f8f9fa")

        # Gradient effect simulation
        style = ttk.Style()
        style.theme_use("clam")

        # Custom styles
        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 24, "bold"),
            foreground="#2c3e50",
            background="#f8f9fa",
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 11),
            foreground="#7f8c8d",
            background="#f8f9fa",
        )

        style.configure("Card.TFrame", relief="flat", borderwidth=1, background="white")

        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"))

    def _create_modern_ui(self):
        """สร้าง UI แบบ Modern"""
        # Header Section
        self._create_header()

        # Mode Selection Cards
        self._create_mode_cards()

        # Login Form (initially hidden)
        self._create_login_form()

        # Footer with actions
        self._create_footer()

    def _create_header(self):
        """สร้าง Header"""
        header_frame = tk.Frame(self.dialog, bg="#f8f9fa", height=120)
        header_frame.pack(fill="x", pady=(30, 20))
        header_frame.pack_propagate(False)

        # App Icon/Logo area
        icon_frame = tk.Frame(header_frame, bg="#f8f9fa")
        icon_frame.pack(pady=10)

        # สร้าง Icon แบบ ASCII Art
        icon_label = tk.Label(
            icon_frame, text="🏭", font=("Segoe UI", 48), bg="#f8f9fa"
        )
        icon_label.pack()

        # Title
        title_label = ttk.Label(header_frame, text="DENSO888", style="Title.TLabel")
        title_label.pack()

        subtitle_label = ttk.Label(
            header_frame, text="Excel to SQL Management System", style="Subtitle.TLabel"
        )
        subtitle_label.pack(pady=(0, 10))

    def _create_mode_cards(self):
        """สร้างการ์ดเลือกโหมด"""
        cards_frame = tk.Frame(self.dialog, bg="#f8f9fa")
        cards_frame.pack(fill="both", expand=True, padx=40, pady=20)

        # Guest Mode Card
        self._create_mode_card(
            cards_frame,
            mode="guest",
            title="🎯 Quick Start (Guest)",
            description="Start immediately with SQLite\n• No login required\n• Local database only\n• Limited to 10,000 rows",
            color="#2ecc71",
            row=0,
        )

        # Authenticated Mode Card
        self._create_mode_card(
            cards_frame,
            mode="authenticated",
            title="🔐 Full Access (Login)",
            description="Complete features with authentication\n• SQL Server + SQLite support\n• Unlimited data processing\n• Full admin capabilities",
            color="#3498db",
            row=1,
        )

        # Skip Mode Card (if enabled)
        if self.config.get("authentication", {}).get("guest_mode", True):
            self._create_mode_card(
                cards_frame,
                mode="skip",
                title="⚡ Developer Mode",
                description="Skip authentication for testing\n• Full access without login\n• Development purposes only\n• All features enabled",
                color="#e67e22",
                row=2,
            )

    def _create_mode_card(self, parent, mode, title, description, color, row):
        """สร้างการ์ดแต่ละโหมด"""
        # Card Frame
        card_frame = tk.Frame(parent, bg="white", relief="flat", bd=1)
        card_frame.pack(fill="x", pady=8)

        # เพิ่ม shadow effect
        shadow_frame = tk.Frame(parent, bg="#e0e0e0", height=2)
        shadow_frame.pack(fill="x")

        # Card Content
        content_frame = tk.Frame(card_frame, bg="white")
        content_frame.pack(fill="both", expand=True, padx=20, pady=15)

        # Radio button + Title
        header_frame = tk.Frame(content_frame, bg="white")
        header_frame.pack(fill="x")

        self.mode_var = getattr(self, "mode_var", tk.StringVar(value="guest"))

        radio = tk.Radiobutton(
            header_frame,
            text=title,
            variable=self.mode_var,
            value=mode,
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg=color,
            selectcolor="white",
            activebackground="white",
            command=lambda: self._on_mode_change(mode),
        )
        radio.pack(side="left")

        # Description
        desc_label = tk.Label(
            content_frame,
            text=description,
            font=("Segoe UI", 10),
            bg="white",
            fg="#5d6d7e",
            justify="left",
        )
        desc_label.pack(fill="x", pady=(5, 0))

        # Hover effects
        def on_enter(e):
            card_frame.configure(bg="#f1f2f6")
            content_frame.configure(bg="#f1f2f6")
            header_frame.configure(bg="#f1f2f6")
            desc_label.configure(bg="#f1f2f6")

        def on_leave(e):
            card_frame.configure(bg="white")
            content_frame.configure(bg="white")
            header_frame.configure(bg="white")
            desc_label.configure(bg="white")

        for widget in [card_frame, content_frame, header_frame, desc_label]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", lambda e, m=mode: self._select_mode(m))

    def _create_login_form(self):
        """สร้างฟอร์ม Login (ซ่อนไว้ตอนแรก)"""
        self.login_frame = tk.Frame(self.dialog, bg="#f8f9fa")

        # Login Card
        login_card = tk.Frame(self.login_frame, bg="white", relief="flat", bd=1)
        login_card.pack(padx=40, pady=20, fill="x")

        # Card content
        card_content = tk.Frame(login_card, bg="white")
        card_content.pack(fill="both", expand=True, padx=30, pady=20)

        # Form title
        form_title = tk.Label(
            card_content,
            text="🔑 Authentication Required",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#2c3e50",
        )
        form_title.pack(pady=(0, 15))

        # Username field
        tk.Label(
            card_content,
            text="Username:",
            font=("Segoe UI", 10),
            bg="white",
            fg="#5d6d7e",
        ).pack(anchor="w")

        self.username_entry = tk.Entry(
            card_content, font=("Segoe UI", 11), relief="flat", bd=5, bg="#f8f9fa"
        )
        self.username_entry.pack(fill="x", pady=(5, 10), ipady=8)
        self.username_entry.insert(0, "admin")  # Default value

        # Password field
        tk.Label(
            card_content,
            text="Password:",
            font=("Segoe UI", 10),
            bg="white",
            fg="#5d6d7e",
        ).pack(anchor="w")

        self.password_entry = tk.Entry(
            card_content,
            font=("Segoe UI", 11),
            relief="flat",
            bd=5,
            bg="#f8f9fa",
            show="*",
        )
        self.password_entry.pack(fill="x", pady=(5, 10), ipady=8)

        # Remember me checkbox
        self.remember_var = tk.BooleanVar(value=True)
        remember_check = tk.Checkbutton(
            card_content,
            text="Remember my login",
            variable=self.remember_var,
            font=("Segoe UI", 9),
            bg="white",
            fg="#7f8c8d",
        )
        remember_check.pack(anchor="w", pady=(0, 10))

        # Default credentials hint
        hint_label = tk.Label(
            card_content,
            text="💡 Default: admin / admin123",
            font=("Segoe UI", 9),
            bg="white",
            fg="#95a5a6",
        )
        hint_label.pack(pady=(0, 10))

        # Bind Enter key
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self._authenticate())

    def _create_footer(self):
        """สร้าง Footer พร้อมปุ่ม Action"""
        footer_frame = tk.Frame(self.dialog, bg="#f8f9fa")
        footer_frame.pack(fill="x", side="bottom", padx=40, pady=30)

        # Back button (if in login mode)
        self.back_btn = tk.Button(
            footer_frame,
            text="← Back to Mode Selection",
            font=("Segoe UI", 10),
            bg="#ecf0f1",
            fg="#5d6d7e",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            command=self._show_mode_selection,
        )

        # Main action button
        self.action_btn = tk.Button(
            footer_frame,
            text="🚀 Start Application",
            font=("Segoe UI", 11, "bold"),
            bg="#2ecc71",
            fg="white",
            relief="flat",
            bd=0,
            padx=30,
            pady=12,
            command=self._handle_action,
        )
        self.action_btn.pack(side="right")

        # Cancel button
        cancel_btn = tk.Button(
            footer_frame,
            text="Cancel",
            font=("Segoe UI", 10),
            bg="#e74c3c",
            fg="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            command=self.dialog.destroy,
        )
        cancel_btn.pack(side="right", padx=(0, 10))

        # Hover effects for buttons
        self._add_button_hover_effects()

    def _add_button_hover_effects(self):
        """เพิ่ม Hover Effects ให้ปุ่ม"""

        def create_hover_effect(button, normal_color, hover_color):
            def on_enter(e):
                button.configure(bg=hover_color)

            def on_leave(e):
                button.configure(bg=normal_color)

            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)

        create_hover_effect(self.action_btn, "#2ecc71", "#27ae60")

    def _on_mode_change(self, mode):
        """เมื่อเปลี่ยนโหมด"""
        self.selected_mode = mode

        if mode == "authenticated":
            self.action_btn.configure(text="🔑 Login to Continue", bg="#3498db")
        elif mode == "guest":
            self.action_btn.configure(text="🎯 Start as Guest", bg="#2ecc71")
        elif mode == "skip":
            self.action_btn.configure(text="⚡ Skip & Start", bg="#e67e22")

    def _select_mode(self, mode):
        """เลือกโหมด"""
        self.mode_var.set(mode)
        self._on_mode_change(mode)

    def _handle_action(self):
        """จัดการ Action หลัก"""
        if self.selected_mode == "authenticated":
            self._show_login_form()
        elif self.selected_mode == "guest":
            self._start_guest_mode()
        elif self.selected_mode == "skip":
            self._start_skip_mode()

    def _show_login_form(self):
        """แสดงฟอร์ม Login"""
        # ซ่อน mode selection
        for widget in self.dialog.winfo_children():
            if widget != self.login_frame:
                widget.pack_forget()

        # แสดง login form
        self.login_frame.pack(fill="both", expand=True)
        self.back_btn.pack(side="left")
        self.action_btn.configure(text="🔑 Login", command=self._authenticate)

        # Focus ที่ password field
        self.password_entry.focus()

    def _show_mode_selection(self):
        """กลับไปหน้าเลือกโหมด"""
        self.login_frame.pack_forget()
        self.back_btn.pack_forget()

        # สร้าง UI ใหม่
        for widget in self.dialog.winfo_children():
            widget.destroy()

        self._create_modern_ui()

    def _authenticate(self):
        """ดำเนินการ Login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning(
                "Input Required", "Please enter both username and password"
            )
            return

        # Loading effect
        original_text = self.action_btn.cget("text")
        self.action_btn.configure(text="🔄 Authenticating...", state="disabled")
        self.dialog.update()

        def auth_thread():
            success, message = self.auth_manager.authenticate(username, password)

            def finish_auth():
                if success:
                    self.success = True
                    self.selected_mode = "authenticated"
                    self.dialog.destroy()
                else:
                    self.action_btn.configure(text=original_text, state="normal")
                    messagebox.showerror("Login Failed", message)
                    self.password_entry.delete(0, tk.END)
                    self.password_entry.focus()

            self.dialog.after(0, finish_auth)

        threading.Thread(target=auth_thread, daemon=True).start()

    def _start_guest_mode(self):
        """เริ่มโหมด Guest"""
        self.success = True
        self.selected_mode = "guest"

        # สร้าง guest user
        self.auth_manager.current_user = {"username": "guest", "role": "guest"}

        messagebox.showinfo(
            "Guest Mode",
            "Starting in Guest Mode\n\n"
            + "• SQLite database only\n"
            + "• Limited to 10,000 rows\n"
            + "• No administrative features",
        )

        self.dialog.destroy()

    def _start_skip_mode(self):
        """เริ่มโหมด Skip (Developer)"""
        result = messagebox.askyesno(
            "Developer Mode",
            "Enable Developer Mode?\n\n"
            + "This will skip authentication and grant full access.\n"
            + "Recommended for development only.\n\n"
            + "Continue?",
        )

        if result:
            self.success = True
            self.selected_mode = "skip"

            # สร้าง developer user
            self.auth_manager.current_user = {"username": "developer", "role": "admin"}

            self.dialog.destroy()


class FlexibleAuthManager:
    """ระบบ Auth ที่ยืดหยุ่น รองรับหลายโหมด"""

    def __init__(self):
        self.config_manager = AuthConfigManager()
        self.current_user = None
        self.current_mode = None

    def show_auth_dialog(self, parent) -> tuple[bool, str]:
        """แสดง Dialog เลือกโหมด"""
        dialog = ModernLoginDialog(parent, self, self.config_manager)
        parent.wait_window(dialog.dialog)

        if dialog.success:
            self.current_mode = dialog.selected_mode
            return True, dialog.selected_mode
        else:
            return False, "cancelled"

    def authenticate(self, username: str, password: str) -> tuple[bool, str]:
        """Authentication logic (simplified for demo)"""
        # Default admin credentials
        if username == "admin" and password == "admin123":
            self.current_user = {"username": username, "role": "admin"}
            return True, "Login successful"
        else:
            return False, "Invalid credentials"

    def check_permission(self, db_type: str, action: str) -> bool:
        """ตรวจสอบสิทธิ์ตามโหมด"""
        if not self.current_user:
            return False

        if self.current_mode == "skip" or self.current_user["role"] == "admin":
            return True

        if self.current_mode == "guest":
            # Guest restrictions
            if db_type == "sqlserver":
                return False  # SQLite only
            if action in ["delete", "admin"]:
                return False  # Limited permissions
            return True

        return True

    def get_database_restrictions(self) -> Dict[str, Any]:
        """ส่งข้อจำกัดของฐานข้อมูลตามโหมด"""
        if self.current_mode == "guest":
            return {
                "max_rows": 10000,
                "allowed_databases": ["sqlite"],
                "readonly_tables": [],
                "restricted_operations": ["delete", "drop"],
            }

        return {
            "max_rows": None,  # Unlimited
            "allowed_databases": ["sqlite", "sqlserver"],
            "readonly_tables": [],
            "restricted_operations": [],
        }


def demo_auth_system():
    """ทดสอบระบบ Auth ใหม่"""
    root = tk.Tk()
    root.withdraw()  # ซ่อนหน้าต่างหลัก

    auth_manager = FlexibleAuthManager()
    success, mode = auth_manager.show_auth_dialog(root)

    if success:
        print(f"✅ Authentication successful!")
        print(f"Mode: {mode}")
        print(f"User: {auth_manager.current_user}")
        print(f"Database restrictions: {auth_manager.get_database_restrictions()}")

        # แสดงหน้าต่างหลัก (demo)
        root.deiconify()
        root.title(f"DENSO888 - {mode.title()} Mode")
        root.geometry("800x600")

        info_label = tk.Label(
            root,
            text=f"🎉 Welcome to DENSO888!\n\n"
            + f"Mode: {mode}\n"
            + f"User: {auth_manager.current_user['username']}\n"
            + f"Role: {auth_manager.current_user['role']}",
            font=("Segoe UI", 14),
            justify="center",
        )
        info_label.pack(expand=True)

        root.mainloop()
    else:
        print("❌ Authentication cancelled")


if __name__ == "__main__":
    demo_auth_system()
