import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

"""
gui/pages/settings_page.py
Application Settings & Configuration Page - FIXED
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from pathlib import Path
from datetime import datetime

from gui.components.modern_button import ModernButton
from gui.components.modern_card import ModernCard
from gui.components.modern_input import LabeledInput


class SettingsPage:
    """Application settings and configuration page"""

    def __init__(self, parent: tk.Widget, controller):
        self.parent = parent
        self.controller = controller
        self.main_frame = None
        self.settings = {}
        self.settings_widgets = {}

        # Initialize ALL variables first
        self._init_variables()

        self._load_settings()
        self._create_settings_page()

    def _init_variables(self):
        """Initialize all tkinter variables"""
        # General tab variables
        self.auto_save_var = tk.BooleanVar(value=True)
        self.remember_window_var = tk.BooleanVar(value=True)
        self.auto_connect_var = tk.BooleanVar(value=False)

        # Appearance tab variables
        self.animations_var = tk.BooleanVar(value=True)
        self.notifications_var = tk.BooleanVar(value=True)
        self.compact_mode_var = tk.BooleanVar(value=False)

        # Data tab variables
        self.include_headers_var = tk.BooleanVar(value=True)
        self.compress_exports_var = tk.BooleanVar(value=False)

        # Advanced tab variables
        self.enable_cache_var = tk.BooleanVar(value=True)
        self.log_to_file_var = tk.BooleanVar(value=True)
        self.debug_mode_var = tk.BooleanVar(value=False)

    def _create_settings_page(self):
        """สร้างหน้า settings"""
        self.main_frame = tk.Frame(self.parent, bg="#FFFFFF")

        # Header
        self._create_header()

        # Settings notebook
        self._create_settings_notebook()

        # Action buttons
        self._create_action_buttons()

    def _create_header(self):
        """สร้าง header section"""
        header_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        header_frame.pack(fill="x", padx=20, pady=(20, 0))

        # Title
        title_label = tk.Label(
            header_frame,
            text="⚙️ Application Settings",
            font=("Segoe UI", 18, "bold"),
            bg="#FFFFFF",
            fg="#1F2937",
        )
        title_label.pack(anchor="w")

        # Description
        desc_label = tk.Label(
            header_frame,
            text="Configure application preferences and behavior",
            font=("Segoe UI", 12),
            bg="#FFFFFF",
            fg="#6B7280",
        )
        desc_label.pack(anchor="w", pady=(5, 0))

    def _create_settings_notebook(self):
        """สร้าง settings notebook"""
        notebook_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        notebook_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.pack(fill="both", expand=True)

        # Create tabs
        self._create_general_tab()
        self._create_appearance_tab()
        self._create_data_tab()
        self._create_advanced_tab()

    def _create_general_tab(self):
        """สร้าง general settings tab"""
        general_frame = tk.Frame(self.notebook, bg="#FFFFFF")
        self.notebook.add(general_frame, text="🏠 General")

        # Application settings card
        app_card = ModernCard(
            general_frame,
            title="🎯 Application Settings",
            width=700,
            height=250,
        )
        app_card.pack(fill="x", padx=20, pady=20)

        app_form = tk.Frame(app_card.get_widget(), bg="#FFFFFF")
        app_form.pack(fill="both", expand=True, padx=20, pady=10)

        # Language selection
        self.settings_widgets["language"] = LabeledInput(
            app_form,
            "Language:",
            "combobox",
            values=["English", "ไทย (Thai)"],
            width=20,
        )
        self.settings_widgets["language"].pack(fill="x", pady=(0, 15))

        # Auto-save settings
        auto_save_frame = tk.Frame(app_form, bg="#FFFFFF")
        auto_save_frame.pack(fill="x", pady=(0, 15))

        tk.Label(
            auto_save_frame,
            text="Auto-save settings:",
            font=("Segoe UI", 11, "bold"),
            bg="#FFFFFF",
            fg="#374151",
        ).pack(anchor="w")

        auto_save_cb = tk.Checkbutton(
            auto_save_frame,
            text="Automatically save configuration changes",
            variable=self.auto_save_var,
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            activebackground="#FFFFFF",
        )
        auto_save_cb.pack(anchor="w", pady=(5, 0))

        # Startup settings
        startup_frame = tk.Frame(app_form, bg="#FFFFFF")
        startup_frame.pack(fill="x")

        tk.Label(
            startup_frame,
            text="Startup options:",
            font=("Segoe UI", 11, "bold"),
            bg="#FFFFFF",
            fg="#374151",
        ).pack(anchor="w")

        remember_cb = tk.Checkbutton(
            startup_frame,
            text="Remember window size and position",
            variable=self.remember_window_var,
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            activebackground="#FFFFFF",
        )
        remember_cb.pack(anchor="w", pady=(5, 0))

        connect_cb = tk.Checkbutton(
            startup_frame,
            text="Auto-connect to last database on startup",
            variable=self.auto_connect_var,
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            activebackground="#FFFFFF",
        )
        connect_cb.pack(anchor="w", pady=(2, 0))

    def _create_appearance_tab(self):
        """สร้าง appearance settings tab"""
        appearance_frame = tk.Frame(self.notebook, bg="#FFFFFF")
        self.notebook.add(appearance_frame, text="🎨 Appearance")

        # Theme settings card
        theme_card = ModernCard(
            appearance_frame,
            title="🎭 Theme & Visual Settings",
            width=700,
            height=300,
        )
        theme_card.pack(fill="x", padx=20, pady=20)

        theme_form = tk.Frame(theme_card.get_widget(), bg="#FFFFFF")
        theme_form.pack(fill="both", expand=True, padx=20, pady=10)

        # Theme selection
        self.settings_widgets["theme"] = LabeledInput(
            theme_form,
            "Application Theme:",
            "combobox",
            values=["Modern Light", "Modern Dark", "Gaming", "Classic"],
            width=25,
        )
        self.settings_widgets["theme"].pack(fill="x", pady=(0, 15))

        # Font size
        self.settings_widgets["font_size"] = LabeledInput(
            theme_form,
            "Font Size:",
            "combobox",
            values=["Small", "Medium", "Large", "Extra Large"],
            width=20,
        )
        self.settings_widgets["font_size"].pack(fill="x", pady=(0, 15))

        # UI options
        ui_options_frame = tk.Frame(theme_form, bg="#FFFFFF")
        ui_options_frame.pack(fill="x")

        tk.Label(
            ui_options_frame,
            text="Interface options:",
            font=("Segoe UI", 11, "bold"),
            bg="#FFFFFF",
            fg="#374151",
        ).pack(anchor="w")

        animations_cb = tk.Checkbutton(
            ui_options_frame,
            text="Enable animations and transitions",
            variable=self.animations_var,
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            activebackground="#FFFFFF",
        )
        animations_cb.pack(anchor="w", pady=(5, 0))

        notifications_cb = tk.Checkbutton(
            ui_options_frame,
            text="Show desktop notifications",
            variable=self.notifications_var,
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            activebackground="#FFFFFF",
        )
        notifications_cb.pack(anchor="w", pady=(2, 0))

        compact_cb = tk.Checkbutton(
            ui_options_frame,
            text="Compact interface mode",
            variable=self.compact_mode_var,
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            activebackground="#FFFFFF",
        )
        compact_cb.pack(anchor="w", pady=(2, 0))

    def _create_data_tab(self):
        """สร้าง data settings tab"""
        data_frame = tk.Frame(self.notebook, bg="#FFFFFF")
        self.notebook.add(data_frame, text="📊 Data")

        # Import settings card
        import_card = ModernCard(
            data_frame,
            title="📁 Import Settings",
            width=700,
            height=200,
        )
        import_card.pack(fill="x", padx=20, pady=20)

        import_form = tk.Frame(import_card.get_widget(), bg="#FFFFFF")
        import_form.pack(fill="both", expand=True, padx=20, pady=10)

        # Batch size
        self.settings_widgets["batch_size"] = LabeledInput(
            import_form,
            "Import Batch Size:",
            "entry",
            placeholder="1000",
            width=15,
        )
        self.settings_widgets["batch_size"].pack(fill="x", pady=(0, 15))

        # Max workers
        self.settings_widgets["max_workers"] = LabeledInput(
            import_form,
            "Maximum Workers:",
            "entry",
            placeholder="4",
            width=15,
        )
        self.settings_widgets["max_workers"].pack(fill="x", pady=(0, 15))

        # Export settings card
        export_card = ModernCard(
            data_frame,
            title="📤 Export Settings",
            width=700,
            height=180,
        )
        export_card.pack(fill="x", padx=20, pady=(0, 20))

        export_form = tk.Frame(export_card.get_widget(), bg="#FFFFFF")
        export_form.pack(fill="both", expand=True, padx=20, pady=10)

        # Default export format
        self.settings_widgets["export_format"] = LabeledInput(
            export_form,
            "Default Export Format:",
            "combobox",
            values=["Excel (.xlsx)", "CSV (.csv)", "JSON (.json)"],
            width=25,
        )
        self.settings_widgets["export_format"].pack(fill="x", pady=(0, 15))

        # Export options
        export_options_frame = tk.Frame(export_form, bg="#FFFFFF")
        export_options_frame.pack(fill="x")

        tk.Label(
            export_options_frame,
            text="Export options:",
            font=("Segoe UI", 11, "bold"),
            bg="#FFFFFF",
            fg="#374151",
        ).pack(anchor="w")

        headers_cb = tk.Checkbutton(
            export_options_frame,
            text="Include column headers",
            variable=self.include_headers_var,
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            activebackground="#FFFFFF",
        )
        headers_cb.pack(anchor="w", pady=(5, 0))

        compress_cb = tk.Checkbutton(
            export_options_frame,
            text="Compress large exports",
            variable=self.compress_exports_var,
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            activebackground="#FFFFFF",
        )
        compress_cb.pack(anchor="w", pady=(2, 0))

    def _create_advanced_tab(self):
        """สร้าง advanced settings tab"""
        advanced_frame = tk.Frame(self.notebook, bg="#FFFFFF")
        self.notebook.add(advanced_frame, text="🔧 Advanced")

        # Performance settings card
        perf_card = ModernCard(
            advanced_frame,
            title="⚡ Performance Settings",
            width=700,
            height=200,
        )
        perf_card.pack(fill="x", padx=20, pady=20)

        perf_form = tk.Frame(perf_card.get_widget(), bg="#FFFFFF")
        perf_form.pack(fill="both", expand=True, padx=20, pady=10)

        # Memory settings
        self.settings_widgets["memory_limit"] = LabeledInput(
            perf_form,
            "Memory Limit (MB):",
            "entry",
            placeholder="1024",
            width=15,
        )
        self.settings_widgets["memory_limit"].pack(fill="x", pady=(0, 15))

        # Cache settings
        cache_frame = tk.Frame(perf_form, bg="#FFFFFF")
        cache_frame.pack(fill="x")

        tk.Label(
            cache_frame,
            text="Cache settings:",
            font=("Segoe UI", 11, "bold"),
            bg="#FFFFFF",
            fg="#374151",
        ).pack(anchor="w")

        cache_cb = tk.Checkbutton(
            cache_frame,
            text="Enable data caching",
            variable=self.enable_cache_var,
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            activebackground="#FFFFFF",
        )
        cache_cb.pack(anchor="w", pady=(5, 0))

        # Logging settings card
        log_card = ModernCard(
            advanced_frame,
            title="📝 Logging Settings",
            width=700,
            height=220,
        )
        log_card.pack(fill="x", padx=20, pady=(0, 20))

        log_form = tk.Frame(log_card.get_widget(), bg="#FFFFFF")
        log_form.pack(fill="both", expand=True, padx=20, pady=10)

        # Log level
        self.settings_widgets["log_level"] = LabeledInput(
            log_form,
            "Log Level:",
            "combobox",
            values=["DEBUG", "INFO", "WARNING", "ERROR"],
            width=20,
        )
        self.settings_widgets["log_level"].pack(fill="x", pady=(0, 15))

        # Log options
        log_options_frame = tk.Frame(log_form, bg="#FFFFFF")
        log_options_frame.pack(fill="x")

        tk.Label(
            log_options_frame,
            text="Logging options:",
            font=("Segoe UI", 11, "bold"),
            bg="#FFFFFF",
            fg="#374151",
        ).pack(anchor="w")

        log_file_cb = tk.Checkbutton(
            log_options_frame,
            text="Log to file",
            variable=self.log_to_file_var,
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            activebackground="#FFFFFF",
        )
        log_file_cb.pack(anchor="w", pady=(5, 0))

        debug_cb = tk.Checkbutton(
            log_options_frame,
            text="Enable debug mode",
            variable=self.debug_mode_var,
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            activebackground="#FFFFFF",
        )
        debug_cb.pack(anchor="w", pady=(2, 0))

        # Backup & Reset section
        backup_card = ModernCard(
            advanced_frame,
            title="💾 Backup & Reset",
            width=700,
            height=150,
        )
        backup_card.pack(fill="x", padx=20, pady=(0, 20))

        backup_form = tk.Frame(backup_card.get_widget(), bg="#FFFFFF")
        backup_form.pack(fill="both", expand=True, padx=20, pady=10)

        # Backup buttons
        backup_buttons = tk.Frame(backup_form, bg="#FFFFFF")
        backup_buttons.pack(fill="x", pady=(10, 0))

        backup_settings_btn = ModernButton(
            backup_buttons,
            "💾 Backup Settings",
            command=self._backup_settings,
            style="success",
        )
        backup_settings_btn.pack(side="left", padx=(0, 10))

        restore_settings_btn = ModernButton(
            backup_buttons,
            "📁 Restore Settings",
            command=self._restore_settings,
            style="secondary",
        )
        restore_settings_btn.pack(side="left", padx=(0, 10))

        reset_settings_btn = ModernButton(
            backup_buttons,
            "🔄 Reset to Defaults",
            command=self._reset_settings,
            style="danger",
        )
        reset_settings_btn.pack(side="left")

    def _create_action_buttons(self):
        """สร้าง action buttons"""
        action_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        action_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Button container
        button_container = tk.Frame(action_frame, bg="#FFFFFF")
        button_container.pack(anchor="e")

        # Cancel button
        cancel_btn = ModernButton(
            button_container,
            "❌ Cancel",
            command=self._cancel_changes,
            style="secondary",
        )
        cancel_btn.pack(side="right", padx=(10, 0))

        # Apply button
        apply_btn = ModernButton(
            button_container,
            "💾 Apply",
            command=self._apply_settings,
            style="success",
        )
        apply_btn.pack(side="right", padx=(10, 0))

        # Save button
        save_btn = ModernButton(
            button_container,
            "✅ Save",
            command=self._save_settings,
            style="primary",
        )
        save_btn.pack(side="right")

    def _load_settings(self):
        """โหลดการตั้งค่า"""
        try:
            settings_file = Path("config/settings.json")
            if settings_file.exists():
                with open(settings_file, "r", encoding="utf-8") as f:
                    self.settings = json.load(f)
            else:
                self.settings = self._get_default_settings()
        except Exception as e:
            print(f"Error loading settings: {e}")
            self.settings = self._get_default_settings()

    def _get_default_settings(self) -> dict:
        """ได้ค่า default settings"""
        return {
            "language": "ไทย (Thai)",
            "theme": "Modern Light",
            "font_size": "Medium",
            "batch_size": "1000",
            "max_workers": "4",
            "export_format": "Excel (.xlsx)",
            "memory_limit": "1024",
            "log_level": "INFO",
            "auto_save": True,
            "remember_window": True,
            "auto_connect": False,
            "animations": True,
            "notifications": True,
            "compact_mode": False,
            "include_headers": True,
            "compress_exports": False,
            "enable_cache": True,
            "log_to_file": True,
            "debug_mode": False,
        }

    def _populate_settings(self):
        """กรอกค่าในฟอร์ม"""
        try:
            # Text inputs
            for key, widget in self.settings_widgets.items():
                if hasattr(widget, "set_value"):
                    value = self.settings.get(key, "")
                    widget.set_value(str(value))

            # Boolean variables
            boolean_settings = {
                "auto_save": self.auto_save_var,
                "remember_window": self.remember_window_var,
                "auto_connect": self.auto_connect_var,
                "animations": self.animations_var,
                "notifications": self.notifications_var,
                "compact_mode": self.compact_mode_var,
                "include_headers": self.include_headers_var,
                "compress_exports": self.compress_exports_var,
                "enable_cache": self.enable_cache_var,
                "log_to_file": self.log_to_file_var,
                "debug_mode": self.debug_mode_var,
            }

            for key, var in boolean_settings.items():
                var.set(self.settings.get(key, False))

        except Exception as e:
            print(f"Error populating settings: {e}")

    def _collect_settings(self) -> dict:
        """รวบรวมการตั้งค่าจากฟอร์ม"""
        settings = {}

        try:
            # Text inputs
            for key, widget in self.settings_widgets.items():
                if hasattr(widget, "get_value"):
                    settings[key] = widget.get_value()

            # Boolean variables
            boolean_settings = {
                "auto_save": self.auto_save_var,
                "remember_window": self.remember_window_var,
                "auto_connect": self.auto_connect_var,
                "animations": self.animations_var,
                "notifications": self.notifications_var,
                "compact_mode": self.compact_mode_var,
                "include_headers": self.include_headers_var,
                "compress_exports": self.compress_exports_var,
                "enable_cache": self.enable_cache_var,
                "log_to_file": self.log_to_file_var,
                "debug_mode": self.debug_mode_var,
            }

            for key, var in boolean_settings.items():
                settings[key] = var.get()

            return settings

        except Exception as e:
            print(f"Error collecting settings: {e}")
            return self.settings

    def _save_settings(self):
        """บันทึกการตั้งค่า"""
        try:
            new_settings = self._collect_settings()

            if self._validate_settings(new_settings):
                self.settings = new_settings

                settings_file = Path("config/settings.json")
                settings_file.parent.mkdir(exist_ok=True)

                with open(settings_file, "w", encoding="utf-8") as f:
                    json.dump(self.settings, f, indent=2, ensure_ascii=False)

                messagebox.showinfo("Success", "Settings saved successfully!")

                if hasattr(self.controller, "apply_settings"):
                    self.controller.apply_settings(self.settings)
            else:
                messagebox.showerror("Error", "Invalid settings values")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")

    def _apply_settings(self):
        """ปรับใช้การตั้งค่าโดยไม่บันทึก"""
        try:
            new_settings = self._collect_settings()

            if self._validate_settings(new_settings):
                if hasattr(self.controller, "apply_settings"):
                    self.controller.apply_settings(new_settings)
                messagebox.showinfo("Applied", "Settings applied temporarily!")
            else:
                messagebox.showerror("Error", "Invalid settings values")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply settings: {str(e)}")

    def _cancel_changes(self):
        """ยกเลิกการเปลี่ยนแปลง"""
        self._populate_settings()
        messagebox.showinfo("Cancelled", "Changes cancelled")

    def _validate_settings(self, settings: dict) -> bool:
        """ตรวจสอบความถูกต้องของการตั้งค่า"""
        try:
            # Validate numeric values
            numeric_fields = ["batch_size", "max_workers", "memory_limit"]

            for field in numeric_fields:
                value = settings.get(field, "0")
                try:
                    num_value = int(value)
                    if num_value <= 0:
                        messagebox.showerror(
                            "Validation Error", f"{field} must be greater than 0"
                        )
                        return False
                except ValueError:
                    messagebox.showerror(
                        "Validation Error", f"{field} must be a valid number"
                    )
                    return False

            # Validate batch size range
            batch_size = int(settings.get("batch_size", 1000))
            if batch_size < 100 or batch_size > 100000:
                messagebox.showerror(
                    "Validation Error", "Batch size must be between 100 and 100,000"
                )
                return False

            # Validate max workers
            max_workers = int(settings.get("max_workers", 4))
            if max_workers < 1 or max_workers > 16:
                messagebox.showerror(
                    "Validation Error", "Max workers must be between 1 and 16"
                )
                return False

            return True

        except Exception as e:
            messagebox.showerror(
                "Validation Error", f"Settings validation failed: {str(e)}"
            )
            return False

    def _backup_settings(self):
        """สำรองการตั้งค่า"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Backup Settings",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialfilename=f"denso888_settings_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            )

            if file_path:
                current_settings = self._collect_settings()

                backup_data = {
                    "backup_date": datetime.now().isoformat(),
                    "app_version": "3.0.0",
                    "settings": current_settings,
                }

                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(backup_data, f, indent=2, ensure_ascii=False)

                messagebox.showinfo("Success", f"Settings backed up to {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {str(e)}")

    def _restore_settings(self):
        """คืนค่าการตั้งค่า"""
        try:
            file_path = filedialog.askopenfilename(
                title="Restore Settings",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            )

            if file_path:
                with open(file_path, "r", encoding="utf-8") as f:
                    backup_data = json.load(f)

                if "settings" in backup_data:
                    self.settings = backup_data["settings"]
                    self._populate_settings()
                    messagebox.showinfo("Success", "Settings restored from backup!")
                else:
                    messagebox.showerror("Error", "Invalid backup file format")

        except Exception as e:
            messagebox.showerror("Error", f"Restore failed: {str(e)}")

    def _reset_settings(self):
        """รีเซ็ตการตั้งค่าเป็นค่าเริ่มต้น"""
        result = messagebox.askyesno(
            "Reset Settings",
            "Are you sure you want to reset all settings to defaults? This cannot be undone.",
        )

        if result:
            self.settings = self._get_default_settings()
            self._populate_settings()
            messagebox.showinfo("Reset", "Settings reset to defaults!")

    def show(self):
        """Show settings page"""
        if self.main_frame:
            self.main_frame.pack(fill="both", expand=True)
            self._populate_settings()

    def hide(self):
        """Hide settings page"""
        if self.main_frame:
            self.main_frame.pack_forget()

    def get_widget(self) -> tk.Widget:
        """Get main widget"""
        return self.main_frame
