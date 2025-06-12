"""
gui/main_window.py
Main window controller for DENSO888 GUI application
"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Changed from PIL to Pillow import
import threading
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


# Placeholder imports - will be replaced with actual components
class DENSO888Theme:
    """Placeholder theme class"""

    def __init__(self):
        self.colors = {
            "primary": "#DC0003",
            "secondary": "#F5F5F5",
            "accent": "#333333",
            "success": "#28A745",
            "warning": "#FFC107",
            "danger": "#DC3545",
            "white": "#FFFFFF",
            "light": "#F8F9FA",
        }

    def apply_to_root(self, root):
        """Apply theme to root window"""
        style = ttk.Style(root)
        style.theme_use("clam")

        # Configure custom styles
        style.configure(
            "Primary.TButton",
            background=self.colors["primary"],
            foreground=self.colors["white"],
        )


class HeaderComponent:
    """Placeholder header component"""

    def __init__(self, parent, config):
        self.frame = ttk.Frame(parent)

        # Logo placeholder
        logo_label = ttk.Label(
            self.frame,
            text="🏭 DENSO888",
            font=("Segoe UI", 16, "bold"),
            foreground="#DC0003",
        )
        logo_label.pack(side="left")

        # Title
        title_label = ttk.Label(self.frame, text="Excel to SQL by เฮียตอมจัดหั้ย!!!")
        title_label.pack(side="left", padx=(10, 0))

    def pack(self, **kwargs):
        """Pack the header frame"""
        self.frame.pack(**kwargs)


class DataSourceTab:
    """Placeholder data source tab"""

    def __init__(self, parent, config, callback):
        self.frame = ttk.Frame(parent)
        self.config = config
        self.callback = callback

        # Mock data section
        mock_frame = ttk.LabelFrame(self.frame, text="Mock Data Generation")
        mock_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(mock_frame, text="Select data type and size:").pack(
            anchor="w", padx=5, pady=5
        )

        # Excel file section
        excel_frame = ttk.LabelFrame(self.frame, text="Excel File Import")
        excel_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(excel_frame, text="Select Excel file:").pack(
            anchor="w", padx=5, pady=5
        )
        ttk.Button(excel_frame, text="Browse...", command=self._browse_file).pack(
            padx=5, pady=5
        )

    def _browse_file(self):
        """Browse for Excel file"""
        messagebox.showinfo("Info", "File browser not implemented yet")

    def load_settings(self, settings):
        """Load tab settings"""
        pass

    def get_settings(self):
        """Get current tab settings"""
        return {}

    def validate(self):
        """Validate tab inputs"""
        return True

    def get_config(self):
        """Get data source configuration"""
        return {
            "type": "mock",
            "template": "employees",
            "rows": 1000,
            "table_name": "test_data",
        }

    def get_current_data_info(self):
        """Get current data information"""
        return {"type": "mock", "rows": 1000, "has_valid_data": True}

    def refresh(self):
        """Refresh tab data"""
        pass


class DatabaseTab:
    """Placeholder database tab"""

    def __init__(self, parent, config, callback):
        self.frame = ttk.Frame(parent)
        self.config = config
        self.callback = callback

        # Database type selection
        type_frame = ttk.LabelFrame(self.frame, text="Database Type")
        type_frame.pack(fill="x", padx=10, pady=10)

        ttk.Radiobutton(type_frame, text="SQLite (Local)", value="sqlite").pack(
            anchor="w", padx=5, pady=2
        )
        ttk.Radiobutton(type_frame, text="SQL Server", value="sqlserver").pack(
            anchor="w", padx=5, pady=2
        )

        # Connection settings
        conn_frame = ttk.LabelFrame(self.frame, text="Connection Settings")
        conn_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(
            conn_frame, text="Test Connection", command=self._test_connection
        ).pack(padx=5, pady=5)

    def _test_connection(self):
        """Test database connection"""
        messagebox.showinfo("Info", "Connection test not implemented yet")

    def load_settings(self, settings):
        """Load tab settings"""
        pass

    def get_settings(self):
        """Get current tab settings"""
        return {}

    def validate(self):
        """Validate tab inputs"""
        return True

    def get_config(self):
        """Get database configuration"""
        from config.settings import DatabaseConfig

        return DatabaseConfig.from_env()

    def get_current_database_info(self):
        """Get current database information"""
        return {"type": "sqlite", "connection_status": {"connected": True}}

    def refresh(self):
        """Refresh tab data"""
        pass


class ProcessingTab:
    """Placeholder processing tab"""

    def __init__(self, parent, config, callback):
        self.frame = ttk.Frame(parent)
        self.config = config
        self.callback = callback

        # Control buttons
        control_frame = ttk.Frame(self.frame)
        control_frame.pack(fill="x", padx=10, pady=10)

        self.start_btn = ttk.Button(
            control_frame,
            text="🚀 Start Processing",
            command=self._start_processing,
            style="Primary.TButton",
        )
        self.start_btn.pack(side="left", padx=5)

        self.stop_btn = ttk.Button(
            control_frame,
            text="⏹️ Stop",
            command=self._stop_processing,
            state="disabled",
        )
        self.stop_btn.pack(side="left", padx=5)

        # Progress section
        progress_frame = ttk.LabelFrame(self.frame, text="Progress")
        progress_frame.pack(fill="x", padx=10, pady=10)

        self.progress_bar = ttk.Progressbar(
            progress_frame, length=400, mode="determinate"
        )
        self.progress_bar.pack(fill="x", padx=5, pady=5)

        self.status_label = ttk.Label(progress_frame, text="Ready to process")
        self.status_label.pack(anchor="w", padx=5, pady=5)

        # Results section
        results_frame = ttk.LabelFrame(self.frame, text="Results")
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.results_text = tk.Text(results_frame, height=10, width=60)
        self.results_text.pack(fill="both", expand=True, padx=5, pady=5)

    def _start_processing(self):
        """Start processing"""
        if self.callback:
            self.callback("start", {})

    def _stop_processing(self):
        """Stop processing"""
        if self.callback:
            self.callback("stop", {})

    def set_processing_enabled(self, enabled):
        """Enable/disable processing"""
        state = "normal" if enabled else "disabled"
        self.start_btn.config(state=state)

    def set_processing_state(self, processing):
        """Set processing state"""
        if processing:
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
        else:
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")

    def update_progress(self, progress_data):
        """Update progress display"""
        progress = progress_data.get("progress", 0)
        message = progress_data.get("message", "")

        self.progress_bar["value"] = progress
        self.status_label.config(text=message)

    def update_data_preview(self, data_info):
        """Update data preview"""
        pass

    def update_database_status(self, db_info):
        """Update database status"""
        pass

    def show_results(self, result):
        """Show processing results"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Processing completed successfully!\n")
        self.results_text.insert(
            tk.END, f"Rows processed: {result.get('rows_processed', 0):,}\n"
        )
        self.results_text.insert(
            tk.END, f"Duration: {result.get('duration', 0):.2f} seconds\n"
        )

    def show_error(self, error_message):
        """Show error message"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Error: {error_message}\n")

    def refresh(self):
        """Refresh tab data"""
        pass


class LogsTab:
    """Placeholder logs tab"""

    def __init__(self, parent, config):
        self.frame = ttk.Frame(parent)
        self.config = config

        # Log display
        self.log_text = tk.Text(self.frame, height=20, width=80, font=("Consolas", 9))
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Control buttons
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Clear Logs", command=self.clear_logs).pack(
            side="right"
        )

    def add_log(self, message, level="info"):
        """Add log message"""
        timestamp = self.frame.winfo_toplevel().tk.call(
            "clock", "format", self.frame.winfo_toplevel().tk.call("clock", "seconds")
        )
        log_entry = f"[{timestamp}] {level.upper()}: {message}\n"

        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)

    def clear_logs(self):
        """Clear all logs"""
        self.log_text.delete(1.0, tk.END)
        self.add_log("Logs cleared")


class DENSO888MainWindow:
    """Main application window controller"""

    def __init__(self):
        try:
            from config.settings import get_config

            self.config = get_config()
        except ImportError:
            # Fallback configuration
            class MockConfig:
                app_name = "DENSO888 - Excel to SQL"
                version = "1.0.0"
                author = "เฮียตอมจัดหั้ย!!!"

                class ui:
                    window_width = 1200
                    window_height = 800
                    min_width = 1000
                    min_height = 700
                    theme_colors = {
                        "primary": "#DC0003",
                        "success": "#28A745",
                        "warning": "#FFC107",
                        "danger": "#DC3545",
                        "accent": "#333333",
                    }

            self.config = MockConfig()

        self.root = tk.Tk()
        self.theme = DENSO888Theme()
        self.data_processor: Optional[Any] = None
        self.processing_thread: Optional[threading.Thread] = None

        # Initialize GUI components
        self._setup_window()
        self._init_components()
        self._setup_events()

        logger.info("DENSO888 Application initialized")

    def _setup_window(self):
        """Initialize main window properties"""
        self.root.title(f"{self.config.app_name} v{self.config.version}")
        self.root.geometry(
            f"{self.config.ui.window_width}x{self.config.ui.window_height}"
        )
        self.root.minsize(self.config.ui.min_width, self.config.ui.min_height)

        # Apply theme
        self.theme.apply_to_root(self.root)

        # Center window
        self._center_window()

    def _center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (self.config.ui.window_width // 2)
        y = (screen_height // 2) - (self.config.ui.window_height // 2)

        self.root.geometry(f"+{x}+{y}")

    def _init_components(self):
        """Initialize GUI components"""
        # Header component
        self.header = HeaderComponent(self.root, self.config)
        self.header.pack(fill="x", padx=20, pady=(20, 10))

        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

        # Initialize tabs
        self.data_source_tab = DataSourceTab(
            self.notebook, self.config, self._on_data_source_changed
        )
        self.database_tab = DatabaseTab(
            self.notebook, self.config, self._on_database_changed
        )
        self.processing_tab = ProcessingTab(
            self.notebook, self.config, self._on_processing_action
        )
        self.logs_tab = LogsTab(self.notebook, self.config)

        # Add tabs to notebook
        self.notebook.add(self.data_source_tab.frame, text="📊 ข้อมูลต้นทาง")
        self.notebook.add(self.database_tab.frame, text="🗄️ ฐานข้อมูล")
        self.notebook.add(self.processing_tab.frame, text="⚡ ประมวลผล")
        self.notebook.add(self.logs_tab.frame, text="📋 บันทึก")

        # Footer
        self._create_footer()

    def _create_footer(self):
        """Create application footer"""
        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(fill="x", side="bottom", padx=20, pady=(0, 20))

        # Status indicator
        self.status_frame = ttk.Frame(footer_frame)
        self.status_frame.pack(side="left")

        ttk.Label(self.status_frame, text="สถานะ:").pack(side="left")
        self.status_label = ttk.Label(
            self.status_frame,
            text="พร้อมใช้งาน",
            foreground=self.config.ui.theme_colors["success"],
        )
        self.status_label.pack(side="left", padx=(5, 0))

        # Version info
        version_info = (
            f"{self.config.app_name} v{self.config.version} | by {self.config.author}"
        )
        ttk.Label(
            footer_frame,
            text=version_info,
            foreground=self.config.ui.theme_colors["accent"],
        ).pack(side="right")

    def _setup_events(self):
        """Setup event handlers"""
        # Window closing event
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        # Tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    # Event handlers
    def _on_data_source_changed(self, event_data: Dict[str, Any]):
        """Handle data source changes"""
        logger.debug(f"Data source changed: {event_data}")

        # Update processing tab with new data info
        if "preview_data" in event_data:
            self.processing_tab.update_data_preview(event_data["preview_data"])

        # Enable/disable processing based on data availability
        has_data = event_data.get("has_valid_data", False)
        self.processing_tab.set_processing_enabled(has_data)

    def _on_database_changed(self, event_data: Dict[str, Any]):
        """Handle database configuration changes"""
        logger.debug(f"Database configuration changed: {event_data}")

        # Update processing tab with database status
        self.processing_tab.update_database_status(
            event_data.get("connection_status", {})
        )

    def _on_processing_action(self, action: str, data: Dict[str, Any]):
        """Handle processing actions"""
        logger.info(f"Processing action: {action}")

        if action == "start":
            self._start_processing()
        elif action == "stop":
            self._stop_processing()
        elif action == "clear_logs":
            self.logs_tab.clear_logs()

    def _on_tab_changed(self, event):
        """Handle tab selection changes"""
        selected_tab = self.notebook.select()
        tab_text = self.notebook.tab(selected_tab, "text")
        logger.debug(f"Tab changed to: {tab_text}")

    def _start_processing(self):
        """Start data processing in background thread"""
        if self.processing_thread and self.processing_thread.is_alive():
            messagebox.showwarning("กำลังประมวลผล", "มีการประมวลผลข้อมูลอยู่แล้ว")
            return

        try:
            # Import data processor
            from core.data_processor import DataProcessor

            # Create data processor
            self.data_processor = DataProcessor(
                data_source_config=self.data_source_tab.get_config(),
                database_config=self.database_tab.get_config(),
                processing_config=self.config,
            )

            # Start processing thread
            self.processing_thread = threading.Thread(
                target=self._process_data_thread, daemon=True
            )
            self.processing_thread.start()

            # Update UI state
            self.processing_tab.set_processing_state(True)
            self._update_status("เริ่มการประมวลผลข้อมูล...", "warning")

            logger.info("Data processing started")

        except Exception as e:
            logger.error(f"Failed to start processing: {e}")
            messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถเริ่มการประมวลผลได้:\n{str(e)}")

    def _stop_processing(self):
        """Stop data processing"""
        if self.data_processor:
            self.data_processor.stop()

        self.processing_tab.set_processing_state(False)
        self._update_status("หยุดการประมวลผล", "warning")

        logger.info("Data processing stopped")

    def _process_data_thread(self):
        """Data processing thread function"""
        try:
            # Setup progress callback
            def progress_callback(progress_data):
                self.root.after(
                    0, lambda: self.processing_tab.update_progress(progress_data)
                )

            # Setup log callback
            def log_callback(message, level="info"):
                self.root.after(0, lambda: self.logs_tab.add_log(message, level))

            # Run processing
            if not self.data_processor:
                raise RuntimeError("Data processor not initialized")

            result = self.data_processor.process(
                progress_callback=progress_callback, log_callback=log_callback
            )

            # Handle completion
            self.root.after(0, lambda: self._on_processing_complete(result))

        except Exception as e:
            logger.error(f"Processing thread error: {e}")
            self.root.after(0, lambda: self._on_processing_error(str(e)))

    def _on_processing_complete(self, result: Dict[str, Any]):
        """Handle processing completion"""
        self.processing_tab.set_processing_state(False)

        if result.get("success", False):
            self.processing_tab.show_results(result)
            self._update_status("ประมวลผลสำเร็จ", "success")

            # Show success notification
            messagebox.showinfo(
                "สำเร็จ",
                f"นำเข้าข้อมูลสำเร็จ!\n"
                f"จำนวนแถว: {result.get('rows_processed', 0):,}\n"
                f"เวลาที่ใช้: {result.get('duration', 0):.2f} วินาที",
            )
        else:
            error_msg = result.get("error", "Unknown error")
            self.processing_tab.show_error(error_msg)
            self._update_status("ประมวลผลล้มเหลว", "danger")

            messagebox.showerror("ข้อผิดพลาด", f"การประมวลผลล้มเหลว:\n{error_msg}")

        logger.info(f"Processing completed: {result}")

    def _on_processing_error(self, error_message: str):
        """Handle processing error"""
        self.processing_tab.set_processing_state(False)
        self.processing_tab.show_error(error_message)
        self._update_status("เกิดข้อผิดพลาดในการประมวลผล", "danger")

        messagebox.showerror("ข้อผิดพลาด", f"เกิดข้อผิดพลาดในการประมวลผล:\n{error_message}")

        logger.error(f"Processing error: {error_message}")

    def _update_status(self, message: str, status_type: str = "info"):
        """Update footer status"""
        color_map = {
            "info": self.config.ui.theme_colors["accent"],
            "success": self.config.ui.theme_colors["success"],
            "warning": self.config.ui.theme_colors["warning"],
            "danger": self.config.ui.theme_colors["danger"],
        }

        self.status_label.config(
            text=message, foreground=color_map.get(status_type, color_map["info"])
        )
        self.root.update_idletasks()

    def _on_closing(self):
        """Handle application closing"""
        try:
            # Check if processing is running
            if self.processing_thread and self.processing_thread.is_alive():
                result = messagebox.askyesnocancel(
                    "กำลังประมวลผล", "มีการประมวลผลข้อมูลอยู่ ต้องการหยุดและปิดโปรแกรมหรือไม่?"
                )

                if result is None:  # Cancel
                    return
                elif result:  # Yes - stop and close
                    self._stop_processing()
                else:  # No - don't close
                    return

            # Close database connections
            if self.data_processor:
                self.data_processor.cleanup()

            # Close application
            self.root.destroy()
            logger.info("Application closed successfully")

        except Exception as e:
            logger.error(f"Error during application closing: {e}")
            self.root.destroy()

    def run(self):
        """Start the application main loop"""
        try:
            logger.info("Starting DENSO888 GUI application")
            self.root.mainloop()
        except KeyboardInterrupt:
            logger.info("Application interrupted by user")
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")
            messagebox.showerror("ข้อผิดพลาดร้ายแรง", f"เกิดข้อผิดพลาดร้ายแรง:\n{str(e)}")
        finally:
            logger.info("Application terminated")
