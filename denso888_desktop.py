#!/usr/bin/env python3
"""
DENSO888 - Excel to Database Desktop App
Ready-to-run Tkinter version
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from pathlib import Path
import threading
import sys
import os

# Add existing modules
sys.path.insert(0, str(Path(__file__).parent))
from src.config.database import db_manager
from src.config.settings import settings
from src.processors.excel_reader import ExcelReader
from src.processors.data_validator import DataValidator
from src.processors.database_writer import DatabaseWriter


class DENSO888App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DENSO888 - Excel to Database by สูตรเฮียตอมจัดหั้ย!!!")
        self.root.geometry("800x600")
        self.root.configure(bg="#fef2f2")

        # Variables
        self.selected_file = None
        self.table_name = tk.StringVar()
        self.duplicate_action = tk.StringVar(value="replace")
        self.processing = False

        self.setup_ui()

    def setup_ui(self):
        """Setup main UI"""

        # Header
        header_frame = tk.Frame(self.root, bg="#DC0032", height=100)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="DENSO888",
            font=("Arial", 24, "bold"),
            bg="#DC0032",
            fg="white",
        )
        title_label.pack(pady=20)

        subtitle_label = tk.Label(
            header_frame,
            text="Excel to Database by สูตรเฮียตอมจัดหั้ย!!!",
            font=("Arial", 12),
            bg="#DC0032",
            fg="white",
        )
        subtitle_label.pack()

        # Main content
        main_frame = tk.Frame(self.root, bg="#fef2f2")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # File selection section
        file_section = tk.LabelFrame(
            main_frame,
            text="1. เลือกไฟล์ Excel",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#DC0032",
        )
        file_section.pack(fill="x", pady=(0, 15))

        file_frame = tk.Frame(file_section, bg="white")
        file_frame.pack(fill="x", padx=15, pady=15)

        self.file_label = tk.Label(
            file_frame, text="ยังไม่ได้เลือกไฟล์", font=("Arial", 12), bg="white", fg="gray"
        )
        self.file_label.pack(side="left")

        select_btn = tk.Button(
            file_frame,
            text="เลือกไฟล์ Excel",
            command=self.select_file,
            bg="#DC0032",
            fg="white",
            font=("Arial", 12, "bold"),
            cursor="hand2",
        )
        select_btn.pack(side="right")

        # Configuration section
        config_section = tk.LabelFrame(
            main_frame,
            text="2. กำหนดการนำเข้า",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#DC0032",
        )
        config_section.pack(fill="x", pady=(0, 15))

        config_frame = tk.Frame(config_section, bg="white")
        config_frame.pack(fill="x", padx=15, pady=15)

        # Table name
        tk.Label(config_frame, text="ชื่อตาราง:", font=("Arial", 12), bg="white").grid(
            row=0, column=0, sticky="w", pady=5
        )

        table_entry = tk.Entry(
            config_frame, textvariable=self.table_name, font=("Arial", 12), width=30
        )
        table_entry.grid(row=0, column=1, sticky="w", padx=(10, 0), pady=5)

        # Duplicate handling
        tk.Label(
            config_frame, text="จัดการข้อมูลซ้ำ:", font=("Arial", 12), bg="white"
        ).grid(row=1, column=0, sticky="w", pady=5)

        duplicate_frame = tk.Frame(config_frame, bg="white")
        duplicate_frame.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=5)

        options = [
            ("เขียนทับ (Replace)", "replace"),
            ("ข้าม (Skip)", "skip"),
            ("เพิ่มต่อ (Append)", "append"),
        ]

        for i, (text, value) in enumerate(options):
            tk.Radiobutton(
                duplicate_frame,
                text=text,
                variable=self.duplicate_action,
                value=value,
                bg="white",
                font=("Arial", 10),
            ).pack(side="left", padx=(0, 15))

        # Process section
        process_section = tk.LabelFrame(
            main_frame,
            text="3. ประมวลผล",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#DC0032",
        )
        process_section.pack(fill="x", pady=(0, 15))

        process_frame = tk.Frame(process_section, bg="white")
        process_frame.pack(fill="x", padx=15, pady=15)

        # Generate sample button
        sample_btn = tk.Button(
            process_frame,
            text="สร้างข้อมูลตัวอย่าง",
            command=self.generate_sample,
            bg="#f0f0f0",
            font=("Arial", 11),
            cursor="hand2",
        )
        sample_btn.pack(side="left")

        # Process button
        self.process_btn = tk.Button(
            process_frame,
            text="เริ่มนำเข้าข้อมูล",
            command=self.start_processing,
            bg="#DC0032",
            fg="white",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            state="disabled",
        )
        self.process_btn.pack(side="right")

        # Progress section
        progress_section = tk.LabelFrame(
            main_frame,
            text="4. สถานะการประมวลผล",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#DC0032",
        )
        progress_section.pack(fill="both", expand=True)

        progress_frame = tk.Frame(progress_section, bg="white")
        progress_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame, variable=self.progress_var, maximum=100
        )
        self.progress_bar.pack(fill="x", pady=(0, 10))

        # Status text
        self.status_text = tk.Text(
            progress_frame, height=10, font=("Consolas", 10), bg="#f8f8f8"
        )
        self.status_text.pack(fill="both", expand=True)

        # Scrollbar for status text
        scrollbar = tk.Scrollbar(self.status_text)
        scrollbar.pack(side="right", fill="y")
        self.status_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.status_text.yview)

    def select_file(self):
        """Select Excel file"""
        file_path = filedialog.askopenfilename(
            title="เลือกไฟล์ Excel",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")],
        )

        if file_path:
            self.selected_file = file_path
            filename = Path(file_path).name
            self.file_label.config(text=filename, fg="green")

            # Auto-generate table name
            table_name = Path(file_path).stem.replace(" ", "_").replace("-", "_")
            self.table_name.set(table_name)

            # Enable process button
            self.process_btn.config(state="normal")

            self.log_status(f"✅ เลือกไฟล์: {filename}")

    def generate_sample(self):
        """Generate sample Excel file"""
        try:
            # Create sample data directory
            Path("data/samples").mkdir(parents=True, exist_ok=True)

            # Generate sample data
            data = {
                "SaleID": [f"SAL{i+1:05d}" for i in range(1000)],
                "CustomerName": [f"Customer_{i+1}" for i in range(1000)],
                "ProductName": [f"Product_{i%10+1}" for i in range(1000)],
                "Quantity": [random.randint(1, 100) for i in range(1000)],
                "UnitPrice": [random.uniform(100, 1000) for i in range(1000)],
                "TotalAmount": [0] * 1000,  # Will calculate
                "SaleDate": [
                    f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
                    for i in range(1000)
                ],
            }

            # Calculate total amount
            for i in range(1000):
                data["TotalAmount"][i] = data["Quantity"][i] * data["UnitPrice"][i]

            df = pd.DataFrame(data)
            sample_file = "data/samples/sample_sales_1000.xlsx"
            df.to_excel(sample_file, index=False)

            messagebox.showinfo("สำเร็จ", f"สร้างข้อมูลตัวอย่าง: {sample_file}")
            self.log_status(f"✅ สร้างข้อมูลตัวอย่าง: {sample_file}")

        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถสร้างข้อมูลตัวอย่างได้: {e}")
            self.log_status(f"❌ ข้อผิดพลาด: {e}")

    def start_processing(self):
        """Start processing in background thread"""
        if not self.selected_file or not self.table_name.get().strip():
            messagebox.showwarning("คำเตือน", "กรุณาเลือกไฟล์และกรอกชื่อตาราง")
            return

        if self.processing:
            return

        # Disable button during processing
        self.process_btn.config(state="disabled", text="กำลังประมวลผล...")
        self.progress_var.set(0)

        # Start background thread
        thread = threading.Thread(target=self.process_file, daemon=True)
        thread.start()

    def process_file(self):
        """Process Excel file"""
        try:
            self.processing = True

            # Test connection first
            self.log_status("🔍 ทดสอบการเชื่อมต่อฐานข้อมูล...")
            self.update_progress(10)

            if not db_manager.test_connection():
                raise Exception("ไม่สามารถเชื่อมต่อฐานข้อมูลได้")

            self.log_status("✅ เชื่อมต่อฐานข้อมูลสำเร็จ")
            self.update_progress(20)

            # Read Excel file
            self.log_status("📊 อ่านไฟล์ Excel...")
            reader = ExcelReader(self.selected_file)
            info = reader.get_sheet_info()

            self.log_status(
                f"📋 พบข้อมูล: {info['total_rows']:,} แถว, {len(info['columns'])} คอลัมน์"
            )
            self.update_progress(30)

            # Initialize processors
            validator = DataValidator()
            writer = DatabaseWriter(self.table_name.get())

            # Create table
            self.log_status("🔧 สร้างตารางในฐานข้อมูล...")
            first_chunk = next(reader.read_chunks(chunk_size=100))
            clean_chunk = validator.clean_dataframe(first_chunk)

            # Auto-detect types
            type_mapping = self.detect_column_types(info["columns"])
            typed_chunk = validator.validate_data_types(clean_chunk, type_mapping)

            writer.create_table_from_dataframe(typed_chunk, type_mapping=type_mapping)
            self.log_status(f"✅ สร้างตาราง '{self.table_name.get()}' สำเร็จ")
            self.update_progress(40)

            # Process data
            self.log_status("⚡ กำลังนำเข้าข้อมูล...")

            # Reset reader
            reader = ExcelReader(self.selected_file)
            total_inserted = 0
            chunk_count = 0

            for chunk in reader.read_chunks(chunk_size=5000):
                chunk_count += 1

                # Process chunk
                clean_chunk = validator.clean_dataframe(chunk)
                typed_chunk = validator.validate_data_types(clean_chunk, type_mapping)

                # Insert to database
                inserted = writer.bulk_insert_batch(typed_chunk)
                total_inserted += inserted

                # Update progress
                progress = 40 + (chunk_count * 5000 / info["total_rows"]) * 50
                self.update_progress(min(progress, 90))

                self.log_status(
                    f"📥 นำเข้าแล้ว: {total_inserted:,}/{info['total_rows']:,} แถว"
                )

            # Verify results
            self.update_progress(95)
            table_info = writer.get_table_info()
            final_count = table_info.get("row_count", 0)

            self.update_progress(100)
            self.log_status(f"🎉 สำเร็จ! นำเข้าข้อมูล {final_count:,} แถว")
            self.log_status(
                f"🗄️ ตารางในฐานข้อมูล: {settings.DB_NAME}.{self.table_name.get()}"
            )

            # Show success message
            self.root.after(
                0,
                lambda: messagebox.showinfo(
                    "สำเร็จ",
                    f"นำเข้าข้อมูลสำเร็จ!\n"
                    f"ตาราง: {self.table_name.get()}\n"
                    f"จำนวนแถว: {final_count:,}",
                ),
            )

        except Exception as e:
            error_msg = f"❌ ข้อผิดพลาด: {e}"
            self.log_status(error_msg)
            self.root.after(0, lambda: messagebox.showerror("ข้อผิดพลาด", str(e)))

        finally:
            self.processing = False
            self.root.after(
                0, lambda: self.process_btn.config(state="normal", text="เริ่มนำเข้าข้อมูล")
            )

    def detect_column_types(self, columns):
        """Auto-detect column types"""
        type_mapping = {}
        patterns = {
            "datetime": ["date", "time", "วันที่", "เวลา"],
            "integer": ["id", "age", "count", "number", "จำนวน"],
            "float": ["price", "salary", "amount", "total", "ราคา"],
            "boolean": ["active", "enabled", "is_", "has_"],
        }

        for column in columns:
            col_lower = column.lower()
            column_type = "string"

            for data_type, pattern_list in patterns.items():
                if any(pattern in col_lower for pattern in pattern_list):
                    column_type = data_type
                    break

            type_mapping[column] = column_type

        return type_mapping

    def update_progress(self, value):
        """Update progress bar"""
        self.root.after(0, lambda: self.progress_var.set(value))

    def log_status(self, message):
        """Log status message"""

        def update_text():
            self.status_text.insert(tk.END, f"{message}\n")
            self.status_text.see(tk.END)

        self.root.after(0, update_text)

    def run(self):
        """Run the application"""
        self.root.mainloop()


if __name__ == "__main__":
    import random

    app = DENSO888App()
    app.run()
