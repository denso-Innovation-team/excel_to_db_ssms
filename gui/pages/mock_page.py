import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

"""
gui/pages/mock_page.py
Mock Data Generation Page
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading

from gui.components.modern_button import ModernButton, ActionButton
from gui.components.modern_input import LabeledInput
from gui.components.modern_card import ModernCard, ClickableCard


class MockPage:
    """Mock data generation page"""

    def __init__(self, parent: tk.Widget, controller):
        self.parent = parent
        self.controller = controller
        self.main_frame = None
        self.selected_template = None
        self.template_cards = {}
        self.count_entry = None
        self.table_name_entry = None

        self._create_mock_page()
        self._load_templates()

    def _create_mock_page(self):
        """สร้างหน้า mock data generation"""
        self.main_frame = tk.Frame(self.parent, bg="#FFFFFF")

        # Header
        self._create_header()

        # Template selection
        self._create_template_section()

        # Generation options
        self._create_options_section()

        # Preview and generation
        self._create_generation_section()

    def _create_header(self):
        """สร้าง header section"""
        header_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        header_frame.pack(fill="x", padx=20, pady=(20, 0))

        # Title
        title_label = tk.Label(
            header_frame,
            text="🎲 Mock Data Generator",
            font=("Segoe UI", 18, "bold"),
            bg="#FFFFFF",
            fg="#1F2937",
        )
        title_label.pack(anchor="w")

        # Description
        desc_label = tk.Label(
            header_frame,
            text="Generate realistic test data for development and testing",
            font=("Segoe UI", 12),
            bg="#FFFFFF",
            fg="#6B7280",
        )
        desc_label.pack(anchor="w", pady=(5, 0))

    def _create_template_section(self):
        """สร้าง template selection section"""
        template_card = ModernCard(
            self.main_frame,
            title="📋 Data Templates",
            content="Choose a template to generate mock data",
            width=800,
            height=400,
        )
        template_card.pack(fill="x", padx=20, pady=20)

        # Templates container
        self.templates_frame = tk.Frame(template_card.get_widget(), bg="#FFFFFF")
        self.templates_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Configure grid for 2 columns
        self.templates_frame.grid_columnconfigure(0, weight=1)
        self.templates_frame.grid_columnconfigure(1, weight=1)

    def _create_options_section(self):
        """สร้าง generation options section"""
        options_card = ModernCard(
            self.main_frame,
            title="⚙️ Generation Options",
            width=800,
            height=200,
        )
        options_card.pack(fill="x", padx=20, pady=(0, 20))

        options_frame = tk.Frame(options_card.get_widget(), bg="#FFFFFF")
        options_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Create form layout
        form_frame = tk.Frame(options_frame, bg="#FFFFFF")
        form_frame.pack(fill="x")

        # Number of records
        self.count_entry = LabeledInput(
            form_frame,
            "Number of Records:",
            "entry",
            placeholder="1000",
            width=15,
        )
        self.count_entry.pack(side="left", padx=(0, 20))

        # Table name
        self.table_name_entry = LabeledInput(
            form_frame,
            "Table Name:",
            "entry",
            placeholder="mock_data_table",
            width=25,
        )
        self.table_name_entry.pack(side="left", fill="x", expand=True)

        # Selected template info
        self.template_info_frame = tk.Frame(options_frame, bg="#FFFFFF")
        self.template_info_frame.pack(fill="x", pady=(15, 0))

        self.selected_info = tk.Label(
            self.template_info_frame,
            text="💡 Please select a template above",
            font=("Segoe UI", 11),
            bg="#FFFFFF",
            fg="#6B7280",
        )
        self.selected_info.pack(anchor="w")

    def _create_generation_section(self):
        """สร้าง generation section"""
        gen_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        gen_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Progress section
        self.progress_frame = tk.Frame(gen_frame, bg="#FFFFFF")
        self.progress_frame.pack(fill="x", pady=(0, 15))

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=400,
            mode="determinate",
        )

        self.progress_label = tk.Label(
            self.progress_frame,
            text="Ready to generate",
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            fg="#6B7280",
        )
        self.progress_label.pack(anchor="w", pady=(0, 5))

        # Action buttons
        button_frame = tk.Frame(gen_frame, bg="#FFFFFF")
        button_frame.pack(anchor="e")

        # Preview button
        self.preview_button = ModernButton(
            button_frame,
            "👁️ Preview Sample",
            command=self._preview_data,
            style="secondary",
        )
        self.preview_button.pack(side="right", padx=(10, 0))

        # Generate button
        self.generate_button = ActionButton(
            button_frame,
            "🎲 Generate Data",
            command=self._generate_data,
        )
        self.generate_button.pack(side="right")

    def _load_templates(self):
        """โหลด mock data templates"""
        if hasattr(self.controller, "get_mock_templates"):
            templates = self.controller.get_mock_templates()
        else:
            # Default templates
            templates = [
                {
                    "id": "employees",
                    "title": "👥 Employee Records",
                    "description": "Staff data with departments, salaries, and contact information",
                    "recommended_count": "1,000 - 10,000",
                },
                {
                    "id": "sales",
                    "title": "💰 Sales Transactions",
                    "description": "Customer orders with products, quantities, and revenue data",
                    "recommended_count": "5,000 - 50,000",
                },
                {
                    "id": "inventory",
                    "title": "📦 Inventory Items",
                    "description": "Product catalog with stock levels and supplier information",
                    "recommended_count": "500 - 5,000",
                },
                {
                    "id": "financial",
                    "title": "💳 Financial Records",
                    "description": "Accounting transactions with approvals and fiscal reporting",
                    "recommended_count": "1,000 - 25,000",
                },
            ]

        self._display_templates(templates)

    def _display_templates(self, templates):
        """แสดง template cards"""
        # Clear existing cards
        for widget in self.templates_frame.winfo_children():
            widget.destroy()

        self.template_cards = {}

        for i, template in enumerate(templates):
            row = i // 2
            col = i % 2

            # Create clickable card
            card = ClickableCard(
                self.templates_frame,
                title=template["title"],
                content=f"{template['description']}\n\nRecommended: {template['recommended_count']} records",
                icon="📊",
                command=lambda t=template: self._select_template(t),
                width=350,
                height=150,
            )
            card.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

            self.template_cards[template["id"]] = card

    def _select_template(self, template):
        """เลือก template"""
        self.selected_template = template

        # Update visual selection
        for template_id, card in self.template_cards.items():
            if template_id == template["id"]:
                # Highlight selected card
                card.card_frame.configure(
                    highlightbackground="#3B82F6", highlightthickness=2
                )
            else:
                # Reset other cards
                card.card_frame.configure(
                    highlightbackground="#E2E8F0", highlightthickness=1
                )

        # Update info
        self.selected_info.configure(
            text=f"✅ Selected: {template['title']} | {template['recommended_count']} records recommended"
        )

        # Auto-suggest table name and count
        self._suggest_defaults(template)

    def _suggest_defaults(self, template):
        """แนะนำค่า default สำหรับ template"""
        # Suggest table name
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        table_name = f"mock_{template['id']}_{timestamp}"
        self.table_name_entry.set_value(table_name)

        # Suggest count based on template
        suggested_counts = {
            "employees": "5000",
            "sales": "10000",
            "inventory": "2000",
            "financial": "5000",
        }
        count = suggested_counts.get(template["id"], "1000")
        self.count_entry.set_value(count)

    def _preview_data(self):
        """Preview sample data"""
        if not self.selected_template:
            messagebox.showwarning("Warning", "Please select a template first")
            return

        try:
            # Generate a small sample
            if hasattr(self.controller, "generate_mock_data"):
                # Show loading
                self.progress_label.configure(text="Generating preview...")
                self.progress_bar.pack(fill="x", pady=(0, 10))
                self.progress_var.set(50)

                def generate_preview():
                    try:
                        # Generate 5 sample records
                        success = self.controller.generate_mock_data(
                            self.selected_template["id"],
                            5,
                            f"preview_{self.selected_template['id']}",
                        )

                        self.main_frame.after(
                            0, lambda: self._show_preview_result(success)
                        )
                    except Exception as e:
                        self.main_frame.after(
                            0, lambda: self._show_preview_error(str(e))
                        )

                threading.Thread(target=generate_preview, daemon=True).start()
            else:
                self._show_mock_preview()

        except Exception as e:
            messagebox.showerror("Error", f"Preview failed: {str(e)}")

    def _show_preview_result(self, success):
        """แสดงผลลัพธ์ preview"""
        self.progress_bar.pack_forget()
        self.progress_label.configure(text="Ready to generate")

        if success:
            messagebox.showinfo(
                "Preview",
                "✅ Sample data generated successfully!\nCheck your database for the preview table.",
            )
        else:
            messagebox.showerror("Preview", "❌ Failed to generate preview data")

    def _show_preview_error(self, error):
        """แสดง error ของ preview"""
        self.progress_bar.pack_forget()
        self.progress_label.configure(text="Ready to generate")
        messagebox.showerror("Preview Error", f"Preview failed: {error}")

    def _show_mock_preview(self):
        """แสดง mock preview (fallback)"""
        preview_data = {
            "employees": [
                "ID: EMP001, Name: สมชาย ใจดี, Department: Engineering, Salary: 45,000",
                "ID: EMP002, Name: วิชาย รักดี, Department: Manufacturing, Salary: 38,000",
                "ID: EMP003, Name: John Smith, Department: IT, Salary: 55,000",
            ],
            "sales": [
                "TXN001: Toyota Parts A1, Qty: 10, Price: 25,500 THB, Customer: ABC Corp",
                "TXN002: Engine Module B2, Qty: 5, Price: 125,000 THB, Customer: XYZ Ltd",
                "TXN003: Sensor Unit C3, Qty: 15, Price: 67,500 THB, Customer: DEF Inc",
            ],
            "inventory": [
                "PROD001: Engine Parts - Model 123, Stock: 150, Supplier: DENSO Corp",
                "PROD002: Brake System - Model 456, Stock: 85, Supplier: Bosch",
                "PROD003: ECU Module - Model 789, Stock: 45, Supplier: Continental",
            ],
            "financial": [
                "FIN001: Sales Revenue, 125,000 THB, 2024-12-01, Approved",
                "FIN002: Equipment Purchase, -85,000 THB, 2024-12-02, Pending",
                "FIN003: Salary Payment, -150,000 THB, 2024-12-03, Approved",
            ],
        }

        template_id = self.selected_template["id"]
        sample = preview_data.get(template_id, ["Sample data not available"])

        preview_text = f"Sample {self.selected_template['title']}:\n\n" + "\n".join(
            sample
        )
        messagebox.showinfo("Data Preview", preview_text)

    def _generate_data(self):
        """Generate mock data"""
        if not self.selected_template:
            messagebox.showwarning("Warning", "Please select a template first")
            return

        count_str = self.count_entry.get_value()
        table_name = self.table_name_entry.get_value()

        if not count_str or not table_name:
            messagebox.showwarning("Warning", "Please specify count and table name")
            return

        try:
            count = int(count_str)
            if count <= 0 or count > 1000000:
                messagebox.showwarning(
                    "Warning", "Count must be between 1 and 1,000,000"
                )
                return
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid number")
            return

        # Confirm large data generation
        if count > 50000:
            result = messagebox.askyesno(
                "Large Dataset",
                f"You're about to generate {count:,} records. This may take some time. Continue?",
            )
            if not result:
                return

        def generate_async():
            try:
                # Show progress
                self.main_frame.after(0, lambda: self._start_generation_progress())

                if hasattr(self.controller, "generate_mock_data"):
                    success = self.controller.generate_mock_data(
                        self.selected_template["id"], count, table_name
                    )

                    self.main_frame.after(
                        0, lambda: self._finish_generation(success, count, table_name)
                    )
                else:
                    # Mock success
                    import time

                    time.sleep(2)
                    self.main_frame.after(
                        0, lambda: self._finish_generation(True, count, table_name)
                    )

            except Exception as e:
                self.main_frame.after(0, lambda: self._finish_generation_error(str(e)))

        threading.Thread(target=generate_async, daemon=True).start()

    def _start_generation_progress(self):
        """เริ่ม progress สำหรับ generation"""
        self.progress_label.configure(text="Generating mock data...")
        self.progress_bar.pack(fill="x", pady=(0, 10))
        self.progress_var.set(0)

        # Disable buttons
        self.generate_button.set_loading(True)
        self.preview_button.get_widget().configure(state="disabled")

    def _finish_generation(self, success, count, table_name):
        """จบ generation"""
        self.progress_bar.pack_forget()
        self.progress_label.configure(text="Ready to generate")
        self.progress_var.set(0)

        # Enable buttons
        self.generate_button.set_loading(False)
        self.preview_button.get_widget().configure(state="normal")

        if success:
            messagebox.showinfo(
                "Generation Complete",
                f"✅ Successfully generated {count:,} records in table '{table_name}'",
            )
        else:
            messagebox.showerror("Generation Failed", "❌ Failed to generate mock data")

    def _finish_generation_error(self, error):
        """จบ generation ด้วย error"""
        self.progress_bar.pack_forget()
        self.progress_label.configure(text="Ready to generate")

        # Enable buttons
        self.generate_button.set_loading(False)
        self.preview_button.get_widget().configure(state="normal")

        messagebox.showerror("Generation Error", f"Generation failed: {error}")

    def show(self):
        """Show mock page"""
        if self.main_frame:
            self.main_frame.pack(fill="both", expand=True)

    def hide(self):
        """Hide mock page"""
        if self.main_frame:
            self.main_frame.pack_forget()

    def get_widget(self) -> tk.Widget:
        """Get main widget"""
        return self.main_frame
