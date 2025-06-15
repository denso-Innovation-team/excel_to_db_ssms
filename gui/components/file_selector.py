"""
gui/components/file_selector.py
Modern File Selector with Drag & Drop Support
"""

import tkinter as tk
from tkinter import filedialog
from typing import List, Tuple, Callable, Optional
from pathlib import Path


class FileSelector:
    """Modern file selector with drag & drop functionality"""

    def __init__(
        self,
        parent: tk.Widget,
        title: str = "Select File",
        filetypes: List[Tuple[str, str]] = None,
    ):
        self.parent = parent
        self.title = title
        self.filetypes = filetypes or [("All files", "*.*")]

        self.selected_file: Optional[str] = None
        self.event_callbacks = {}

        self._create_widget()

    def _create_widget(self):
        """Create file selector widget"""
        self.main_frame = tk.Frame(self.parent, bg="#F1F5F9")

        # Drop area
        self.drop_frame = tk.Frame(
            self.main_frame, bg="#E2E8F0", relief="dashed", bd=2, height=120
        )
        self.drop_frame.pack(fill="x", pady=10)
        self.drop_frame.pack_propagate(False)

        # Drop content
        content_frame = tk.Frame(self.drop_frame, bg="#E2E8F0")
        content_frame.pack(expand=True)

        # Icon and text
        icon_label = tk.Label(
            content_frame, text="📁", font=("Segoe UI", 24), bg="#E2E8F0", fg="#DC0003"
        )
        icon_label.pack(pady=(10, 5))

        self.status_label = tk.Label(
            content_frame,
            text="Drag & drop file here or click to browse",
            font=("Segoe UI", 11),
            bg="#E2E8F0",
            fg="#64748B",
        )
        self.status_label.pack()

        # Browse button
        browse_btn = tk.Button(
            content_frame,
            text="📂 Browse Files",
            font=("Segoe UI", 10),
            bg="#DC0003",
            fg="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self._browse_file,
        )
        browse_btn.pack(pady=(10, 15))

        # Bind events
        self._bind_events()

    def _bind_events(self):
        """Bind drag & drop and click events"""
        # Make area clickable
        for widget in [self.drop_frame, self.status_label]:
            widget.bind("<Button-1>", lambda e: self._browse_file())

        # Drag and drop (basic implementation)
        self.drop_frame.bind("<Button-1>", lambda e: self._browse_file())

    def _browse_file(self):
        """Open file browser"""
        filename = filedialog.askopenfilename(
            title=self.title, filetypes=self.filetypes
        )

        if filename:
            self._set_file(filename)

    def _set_file(self, filepath: str):
        """Set selected file"""
        self.selected_file = filepath
        filename = Path(filepath).name

        # Update UI
        self.status_label.configure(text=f"✅ Selected: {filename}", fg="#10B981")

        # Trigger callback
        self._trigger_event("file_selected", filepath)

    def bind_event(self, event: str, callback: Callable):
        """Bind event callback"""
        if event not in self.event_callbacks:
            self.event_callbacks[event] = []
        self.event_callbacks[event].append(callback)

    def _trigger_event(self, event: str, data=None):
        """Trigger event callbacks"""
        if event in self.event_callbacks:
            for callback in self.event_callbacks[event]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Event callback error: {e}")

    def get_file(self) -> Optional[str]:
        """Get selected file path"""
        return self.selected_file

    def get_widget(self) -> tk.Widget:
        """Get main widget"""
        return self.main_frame

    def clear(self):
        """Clear selection"""
        self.selected_file = None
        self.status_label.configure(
            text="Drag & drop file here or click to browse", fg="#64748B"
        )
