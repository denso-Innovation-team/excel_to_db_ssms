"""
gui/components/modern_input.py
Modern Input Components - Entry, Dropdown, File Picker
"""

import tkinter as tk
from tkinter import ttk, filedialog
from typing import Callable, Optional, List


class ModernEntry:
    """Modern text input with validation"""

    def __init__(
        self,
        parent: tk.Widget,
        placeholder: str = "",
        width: int = 20,
        validation: Optional[Callable] = None,
    ):
        self.parent = parent
        self.placeholder = placeholder
        self.width = width
        self.validation = validation
        self.is_valid = True

        self.var = tk.StringVar()
        self.entry = self._create_entry()
        self._setup_placeholder()
        self._setup_validation()

    def _create_entry(self) -> tk.Entry:
        """สร้าง entry widget"""
        entry = tk.Entry(
            self.parent,
            textvariable=self.var,
            font=("Segoe UI", 11),
            bg="white",
            fg="#1E293B",
            relief="solid",
            bd=1,
            highlightthickness=2,
            highlightcolor="#3B82F6",
            highlightbackground="#E2E8F0",
            width=self.width,
            insertbackground="#3B82F6",
        )
        return entry

    def _setup_placeholder(self):
        """ตั้งค่า placeholder text"""
        if not self.placeholder:
            return

        def on_focus_in(event):
            if self.var.get() == self.placeholder:
                self.var.set("")
                self.entry.configure(fg="#1E293B")

        def on_focus_out(event):
            if self.var.get() == "":
                self.var.set(self.placeholder)
                self.entry.configure(fg="#9CA3AF")

        # Set initial placeholder
        self.var.set(self.placeholder)
        self.entry.configure(fg="#9CA3AF")

        self.entry.bind("<FocusIn>", on_focus_in)
        self.entry.bind("<FocusOut>", on_focus_out)

    def _setup_validation(self):
        """ตั้งค่า validation"""
        if not self.validation:
            return

        def validate(event=None):
            value = self.get_value()
            if value == self.placeholder:
                return

            self.is_valid = self.validation(value)
            if self.is_valid:
                self.entry.configure(highlightbackground="#10B981")
            else:
                self.entry.configure(highlightbackground="#EF4444")

        self.var.trace("w", lambda *args: validate())

    def get_value(self) -> str:
        """ได้ค่าจาก entry"""
        value = self.var.get()
        return "" if value == self.placeholder else value

    def set_value(self, value: str):
        """ตั้งค่า entry"""
        self.var.set(value)
        if value:
            self.entry.configure(fg="#1E293B")

    def is_empty(self) -> bool:
        """เช็คว่าเป็นค่าว่างหรือไม่"""
        return self.get_value() == ""

    def pack(self, **kwargs):
        self.entry.pack(**kwargs)

    def grid(self, **kwargs):
        self.entry.grid(**kwargs)

    def get_widget(self) -> tk.Entry:
        return self.entry


class ModernCombobox:
    """Modern dropdown selection"""

    def __init__(
        self,
        parent: tk.Widget,
        values: List[str],
        placeholder: str = "Select...",
        width: int = 20,
    ):
        self.parent = parent
        self.values = values
        self.placeholder = placeholder
        self.width = width

        self.var = tk.StringVar()
        self.combobox = self._create_combobox()

    def _create_combobox(self) -> ttk.Combobox:
        """สร้าง combobox widget"""
        style = ttk.Style()
        style.configure(
            "Modern.TCombobox",
            fieldbackground="white",
            background="white",
            foreground="#1E293B",
            selectbackground="#3B82F6",
            selectforeground="white",
        )

        combobox = ttk.Combobox(
            self.parent,
            textvariable=self.var,
            values=self.values,
            state="readonly",
            style="Modern.TCombobox",
            width=self.width,
            font=("Segoe UI", 11),
        )

        # Set placeholder
        if self.placeholder:
            combobox.set(self.placeholder)

        return combobox

    def get_value(self) -> str:
        """ได้ค่าที่เลือก"""
        value = self.var.get()
        return "" if value == self.placeholder else value

    def set_value(self, value: str):
        """ตั้งค่าที่เลือก"""
        if value in self.values:
            self.var.set(value)

    def update_values(self, new_values: List[str]):
        """อัพเดทรายการตัวเลือก"""
        self.values = new_values
        self.combobox.configure(values=new_values)

    def bind(self, event: str, callback: Callable):
        """ผูก event"""
        self.combobox.bind(event, callback)

    def pack(self, **kwargs):
        self.combobox.pack(**kwargs)

    def grid(self, **kwargs):
        self.combobox.grid(**kwargs)

    def get_widget(self) -> ttk.Combobox:
        return self.combobox


class FileSelector:
    """File selection component"""

    def __init__(
        self,
        parent: tk.Widget,
        placeholder: str = "Select file...",
        file_types: List[tuple] = None,
        width: int = 40,
    ):
        self.parent = parent
        self.placeholder = placeholder
        self.file_types = file_types or [("All files", "*.*")]
        self.width = width
        self.selected_file = ""

        self.frame = tk.Frame(parent, bg="white")
        self.entry = ModernEntry(self.frame, placeholder, width - 10)
        self.button = self._create_button()

        self._layout_components()

    def _create_button(self) -> tk.Button:
        """สร้างปุ่มเลือกไฟล์"""
        from .modern_button import ModernButton

        button = ModernButton(
            self.frame,
            "📁",
            command=self._select_file,
            style="secondary",
            width=3,
        )
        return button

    def _layout_components(self):
        """จัดวาง components"""
        self.entry.pack(side="left", padx=(0, 5), fill="x", expand=True)
        self.button.pack(side="right")

    def _select_file(self):
        """เปิด file dialog"""
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=self.file_types,
            initialdir=".",
        )

        if file_path:
            self.selected_file = file_path
            # แสดงเฉพาะชื่อไฟล์
            import os

            filename = os.path.basename(file_path)
            self.entry.set_value(filename)

    def get_file_path(self) -> str:
        """ได้ path ของไฟล์ที่เลือก"""
        return self.selected_file

    def get_filename(self) -> str:
        """ได้ชื่อไฟล์ที่เลือก"""
        import os

        return os.path.basename(self.selected_file) if self.selected_file else ""

    def clear(self):
        """ล้างการเลือกไฟล์"""
        self.selected_file = ""
        self.entry.set_value("")

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)

    def get_widget(self) -> tk.Frame:
        return self.frame


class LabeledInput:
    """Input พร้อม label"""

    def __init__(
        self, parent: tk.Widget, label: str, input_type: str = "entry", **kwargs
    ):
        self.parent = parent
        self.label_text = label
        self.input_type = input_type

        self.frame = tk.Frame(parent, bg="white")
        self.label = self._create_label()
        self.input_widget = self._create_input(**kwargs)

        self._layout_components()

    def _create_label(self) -> tk.Label:
        """สร้าง label"""
        return tk.Label(
            self.frame,
            text=self.label_text,
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#374151",
            anchor="w",
        )

    def _create_input(self, **kwargs):
        """สร้าง input widget ตามประเภท"""
        if self.input_type == "entry":
            return ModernEntry(self.frame, **kwargs)
        elif self.input_type == "combobox":
            return ModernCombobox(self.frame, **kwargs)
        elif self.input_type == "file":
            return FileSelector(self.frame, **kwargs)
        else:
            return ModernEntry(self.frame, **kwargs)

    def _layout_components(self):
        """จัดวาง components"""
        self.label.pack(anchor="w", pady=(0, 5))
        self.input_widget.pack(fill="x")

    def get_value(self):
        """ได้ค่าจาก input"""
        if hasattr(self.input_widget, "get_value"):
            return self.input_widget.get_value()
        return ""

    def set_value(self, value):
        """ตั้งค่า input"""
        if hasattr(self.input_widget, "set_value"):
            self.input_widget.set_value(value)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)

    def get_widget(self) -> tk.Frame:
        return self.frame


class FormBuilder:
    """Builder สำหรับสร้างฟอร์ม"""

    def __init__(self, parent: tk.Widget):
        self.parent = parent
        self.form_frame = tk.Frame(parent, bg="white")
        self.fields = {}

    def add_field(self, name: str, label: str, input_type: str = "entry", **kwargs):
        """เพิ่มฟิลด์ในฟอร์ม"""
        field = LabeledInput(self.form_frame, label, input_type, **kwargs)
        field.pack(fill="x", pady=(0, 15))
        self.fields[name] = field
        return self

    def get_values(self) -> dict:
        """ได้ค่าทั้งหมดจากฟอร์ม"""
        values = {}
        for name, field in self.fields.items():
            values[name] = field.get_value()
        return values

    def set_values(self, values: dict):
        """ตั้งค่าฟอร์ม"""
        for name, value in values.items():
            if name in self.fields:
                self.fields[name].set_value(value)

    def validate(self) -> bool:
        """ตรวจสอบความถูกต้องของฟอร์ม"""
        for field in self.fields.values():
            if hasattr(field.input_widget, "is_valid"):
                if not field.input_widget.is_valid:
                    return False
        return True

    def pack(self, **kwargs):
        self.form_frame.pack(**kwargs)

    def grid(self, **kwargs):
        self.form_frame.grid(**kwargs)

    def get_widget(self) -> tk.Frame:
        return self.form_frame
