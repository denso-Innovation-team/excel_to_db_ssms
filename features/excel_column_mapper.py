"""
Excel Column Mapper Widget
ฟีเจอร์ให้ user เลือก columns และกำหนดชื่อใหม่
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional, Callable


class ExcelColumnMapper:
    """Excel Column Mapping Interface"""

    def __init__(
        self,
        parent: tk.Widget,
        columns: List[str],
        confirm_callback: Optional[Callable] = None,
    ):
        self.parent = parent
        self.columns = columns
        self.confirm_callback = confirm_callback

        # Column mappings: original -> new name
        self.column_mappings = {}
        self.selected_columns = set(columns)  # All selected by default

        self.create_window()

    def create_window(self):
        """Create column mapping window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📋 Excel Column Mapping")
        self.window.geometry("800x600")
        self.window.configure(bg="#FFFFFF")
        self.window.grab_set()
        self.window.transient(self.parent)

        # Center window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - 400
        y = (self.window.winfo_screenheight() // 2) - 300
        self.window.geometry(f"800x600+{x}+{y}")

        self.create_widgets()

    def create_widgets(self):
        """Create mapping interface widgets"""
        # Header
        header = tk.Label(
            self.window,
            text="📋 Configure Excel Columns",
            font=("Segoe UI", 18, "bold"),
            fg="#DC0003",
            bg="#FFFFFF",
        )
        header.pack(pady=20)

        # Instructions
        instructions = tk.Label(
            self.window,
            text="Select columns to import and customize their names for the database:",
            font=("Segoe UI", 12),
            fg="#2C3E50",
            bg="#FFFFFF",
        )
        instructions.pack(pady=(0, 20))

        # Main content frame
        content_frame = tk.Frame(self.window, bg="#FFFFFF")
        content_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        # Create treeview for column mapping
        self.create_column_tree(content_frame)

        # Control buttons
        self.create_control_buttons(content_frame)

        # Action buttons
        self.create_action_buttons()

    def create_column_tree(self, parent):
        """Create column mapping treeview"""
        tree_frame = tk.Frame(parent, bg="#FFFFFF")
        tree_frame.pack(fill="both", expand=True, pady=(0, 20))

        # Column headers
        columns = ("select", "original", "new_name", "data_type")
        self.tree = ttk.Treeview(
            tree_frame, columns=columns, show="headings", height=15
        )

        # Configure columns
        self.tree.heading("select", text="✓ Include")
        self.tree.heading("original", text="Original Column Name")
        self.tree.heading("new_name", text="Database Column Name")
        self.tree.heading("data_type", text="Detected Type")

        self.tree.column("select", width=80, anchor="center")
        self.tree.column("original", width=200)
        self.tree.column("new_name", width=200)
        self.tree.column("data_type", width=120, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Populate tree
        self.populate_tree()

        # Bind events
        self.tree.bind("<Double-1>", self.on_tree_double_click)

    def populate_tree(self):
        """Populate tree with column data"""
        for col in self.columns:
            # Detect data type (simplified)
            data_type = self.detect_data_type(col)

            # Clean column name for database
            clean_name = self.clean_column_name(col)

            # Insert into tree
            item = self.tree.insert(
                "",
                "end",
                values=("✓", col, clean_name, data_type),  # Selected by default
            )

            # Store mapping
            self.column_mappings[col] = clean_name

    def detect_data_type(self, column_name: str) -> str:
        """Simple data type detection based on column name"""
        name_lower = column_name.lower()

        if any(word in name_lower for word in ["id", "number", "count", "qty"]):
            return "INTEGER"
        elif any(word in name_lower for word in ["price", "amount", "salary", "cost"]):
            return "DECIMAL"
        elif any(word in name_lower for word in ["date", "time", "created", "updated"]):
            return "DATETIME"
        elif any(word in name_lower for word in ["active", "enabled", "flag"]):
            return "BOOLEAN"
        else:
            return "TEXT"

    def clean_column_name(self, name: str) -> str:
        """Clean column name for database use"""
        import re

        # Convert to string and strip
        clean = str(name).strip()

        # Replace special characters with underscore
        clean = re.sub(r"[^\w\s]", "_", clean)

        # Replace spaces with underscore
        clean = re.sub(r"\s+", "_", clean)

        # Remove multiple underscores
        clean = re.sub(r"_+", "_", clean)

        # Remove leading/trailing underscores
        clean = clean.strip("_").lower()

        # Ensure not empty
        if not clean:
            clean = "column"

        return clean

    def create_control_buttons(self, parent):
        """Create control buttons"""
        button_frame = tk.Frame(parent, bg="#FFFFFF")
        button_frame.pack(fill="x", pady=(0, 20))

        # Select/Deselect all
        select_all_btn = tk.Button(
            button_frame,
            text="✓ Select All",
            command=self.select_all,
            font=("Segoe UI", 10),
            bg="#28A745",
            fg="#FFFFFF",
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2",
        )
        select_all_btn.pack(side="left", padx=(0, 10))

        deselect_all_btn = tk.Button(
            button_frame,
            text="✗ Deselect All",
            command=self.deselect_all,
            font=("Segoe UI", 10),
            bg="#DC3545",
            fg="#FFFFFF",
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2",
        )
        deselect_all_btn.pack(side="left", padx=(0, 10))

        # Reset names
        reset_btn = tk.Button(
            button_frame,
            text="🔄 Reset Names",
            command=self.reset_names,
            font=("Segoe UI", 10),
            bg="#FFC107",
            fg="#212529",
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2",
        )
        reset_btn.pack(side="left")

    def create_action_buttons(self):
        """Create action buttons"""
        action_frame = tk.Frame(self.window, bg="#FFFFFF")
        action_frame.pack(side="bottom", fill="x", padx=30, pady=20)

        # Cancel button
        cancel_btn = tk.Button(
            action_frame,
            text="Cancel",
            command=self.window.destroy,
            font=("Segoe UI", 12),
            bg="#6C757D",
            fg="#FFFFFF",
            relief="flat",
            padx=30,
            pady=10,
            cursor="hand2",
        )
        cancel_btn.pack(side="right", padx=(10, 0))

        # Confirm button
        confirm_btn = tk.Button(
            action_frame,
            text="✓ Apply Mapping",
            command=self.confirm_mapping,
            font=("Segoe UI", 12, "bold"),
            bg="#DC0003",
            fg="#FFFFFF",
            relief="flat",
            padx=30,
            pady=10,
            cursor="hand2",
        )
        confirm_btn.pack(side="right")

    def on_tree_double_click(self, event):
        """Handle tree double-click for editing"""
        item = self.tree.selection()[0]
        column = self.tree.item(item, "column")

        if column == "#1":  # Select column
            self.toggle_selection(item)
        elif column == "#3":  # New name column
            self.edit_column_name(item)

    def toggle_selection(self, item):
        """Toggle column selection"""
        values = list(self.tree.item(item, "values"))
        original_col = values[1]

        if values[0] == "✓":
            values[0] = "✗"
            self.selected_columns.discard(original_col)
        else:
            values[0] = "✓"
            self.selected_columns.add(original_col)

        self.tree.item(item, values=values)

    def edit_column_name(self, item):
        """Edit column name"""
        values = list(self.tree.item(item, "values"))
        original_col = values[1]
        current_name = values[2]

        # Simple dialog for name input
        new_name = tk.simpledialog.askstring(
            "Edit Column Name",
            f"Enter new name for column '{original_col}':",
            initialvalue=current_name,
        )

        if new_name and new_name.strip():
            clean_name = self.clean_column_name(new_name.strip())
            values[2] = clean_name
            self.tree.item(item, values=values)
            self.column_mappings[original_col] = clean_name

    def select_all(self):
        """Select all columns"""
        for item in self.tree.get_children():
            values = list(self.tree.item(item, "values"))
            values[0] = "✓"
            self.tree.item(item, values=values)
            self.selected_columns.add(values[1])

    def deselect_all(self):
        """Deselect all columns"""
        for item in self.tree.get_children():
            values = list(self.tree.item(item, "values"))
            values[0] = "✗"
            self.tree.item(item, values=values)
            self.selected_columns.discard(values[1])

    def reset_names(self):
        """Reset all column names to cleaned originals"""
        for item in self.tree.get_children():
            values = list(self.tree.item(item, "values"))
            original_col = values[1]
            clean_name = self.clean_column_name(original_col)
            values[2] = clean_name
            self.tree.item(item, values=values)
            self.column_mappings[original_col] = clean_name

    def confirm_mapping(self):
        """Confirm and apply column mapping"""
        if not self.selected_columns:
            messagebox.showwarning(
                "No Columns Selected", "Please select at least one column to import."
            )
            return

        # Get final mappings for selected columns only
        final_mappings = {}
        selected_list = []

        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            if values[0] == "✓":  # Selected
                original_col = values[1]
                new_name = values[2]
                final_mappings[original_col] = new_name
                selected_list.append(original_col)

        if self.confirm_callback:
            self.confirm_callback(selected_list, final_mappings)

        self.window.destroy()
