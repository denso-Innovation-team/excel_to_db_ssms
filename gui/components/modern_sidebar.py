"""
gui/components/modern_sidebar.py
Fixed Sidebar Layout - แก้ปัญหา padding ซ้อนกันและ responsive layout
"""

import tkinter as tk
from datetime import datetime
from typing import List, Dict, Any, Callable

# Import theme เดิม
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
from gui.themes.modern_theme import modern_theme


class ModernSidebar:
    """Fixed Sidebar with proper layout management"""

    def __init__(
        self,
        parent: tk.Widget,
        menu_items: List[Dict[str, Any]],
        callback: Callable[[str], None],
    ):
        self.parent = parent
        self.menu_items = menu_items
        self.callback = callback
        self.theme = modern_theme
        self.current_selection = None
        self.menu_buttons = {}

        # สร้าง sidebar widget
        self.widget = self._create_sidebar()

    def _create_sidebar(self):
        """สร้าง sidebar ด้วย layout ที่ถูกต้อง"""
        # Main sidebar container - ไม่มี padding ซ้อน
        sidebar = tk.Frame(
            self.parent,
            bg=self.theme.colors.surface,
            width=self.theme.spacing.sidebar_width,
            relief="flat",
            bd=0,
        )
        sidebar.pack_propagate(False)

        # Configure layout sections
        self._create_brand_section(sidebar)
        self._create_navigation_section(sidebar)
        self._create_footer_section(sidebar)

        return sidebar

    def _create_brand_section(self, parent):
        """Brand section ด้วย proper spacing"""
        # Brand container - ใช้ spacing จาก theme
        brand_frame = tk.Frame(
            parent,
            bg=self.theme.colors.surface,
            height=self.theme.spacing.header_height + self.theme.spacing.md,
        )
        brand_frame.pack(fill="x")
        brand_frame.pack_propagate(False)

        # Brand content - centered properly
        brand_content = tk.Frame(brand_frame, bg=self.theme.colors.surface)
        brand_content.pack(expand=True, padx=self.theme.spacing.lg)

        # Logo/Title
        logo_label = tk.Label(
            brand_content,
            text="🏭 DENSO888",
            font=self.theme.fonts.get("heading_lg"),
            bg=self.theme.colors.surface,
            fg=self.theme.colors.primary,
        )
        logo_label.pack(anchor="w")

        # Subtitle
        subtitle_label = tk.Label(
            brand_content,
            text="Professional Edition",
            font=self.theme.fonts.get("body_sm"),
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_secondary,
        )
        subtitle_label.pack(anchor="w", pady=(2, 0))

    def _create_navigation_section(self, parent):
        """Navigation section ด้วย consistent spacing"""
        # Navigation container
        nav_container = tk.Frame(parent, bg=self.theme.colors.surface)
        nav_container.pack(fill="both", expand=True, padx=self.theme.spacing.sm)

        # Navigation title
        nav_title = tk.Label(
            nav_container,
            text="NAVIGATION",
            font=self.theme.fonts.get("caption"),
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_tertiary,
        )
        nav_title.pack(
            anchor="w",
            padx=self.theme.spacing.md,
            pady=(self.theme.spacing.sm, self.theme.spacing.xs),
        )

        # Menu items container
        menu_container = tk.Frame(nav_container, bg=self.theme.colors.surface)
        menu_container.pack(fill="both", expand=True)

        # Create menu items
        for item in self.menu_items:
            self._create_menu_item(menu_container, item)

    def _create_menu_item(self, parent: tk.Widget, item: Dict[str, Any]):
        """สร้าง menu item ด้วย layout ที่เป็นมืออาชีพ"""
        item_id = item["id"]

        # Item container - no nested padding
        item_container = tk.Frame(parent, bg=self.theme.colors.surface)
        item_container.pack(fill="x", pady=1)

        # Main navigation button
        button = tk.Button(
            item_container,
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda: self._handle_nav_click(item_id),
            anchor="w",
        )
        button.pack(fill="x")

        # Button content layout
        self._setup_button_content(button, item)
        self._setup_hover_effects(button, item_id)

        # Store reference
        self.menu_buttons[item_id] = button

    def _setup_button_content(self, button: tk.Button, item: Dict[str, Any]):
        """Setup button content ด้วย proper layout"""
        # Main content frame - single level padding
        content_frame = tk.Frame(
            button,
            bg=self.theme.colors.surface,
            padx=self.theme.spacing.md,
            pady=self.theme.spacing.sm,
        )
        content_frame.pack(fill="both", expand=True)

        # Icon and text layout
        layout_frame = tk.Frame(content_frame, bg=self.theme.colors.surface)
        layout_frame.pack(fill="x")

        # Icon
        icon_label = tk.Label(
            layout_frame,
            text=item.get("icon", "📋"),
            font=("Inter", 14),
            bg=self.theme.colors.surface,
            fg=self.theme.colors.primary,
        )
        icon_label.pack(side="left", padx=(0, self.theme.spacing.sm))

        # Title
        title_label = tk.Label(
            layout_frame,
            text=item.get("title", "Menu Item"),
            font=self.theme.fonts.get("body_md"),
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
            anchor="w",
        )
        title_label.pack(side="left", fill="x", expand=True)

        # Description (if exists)
        if item.get("description"):
            desc_label = tk.Label(
                content_frame,
                text=item["description"],
                font=self.theme.fonts.get("caption"),
                bg=self.theme.colors.surface,
                fg=self.theme.colors.text_secondary,
                anchor="w",
            )
            desc_label.pack(fill="x", pady=(2, 0))

        # Store references for color updates
        button.content_frame = content_frame
        button.layout_frame = layout_frame
        button.icon_label = icon_label
        button.title_label = title_label

    def _setup_hover_effects(self, button: tk.Button, item_id: str):
        """Setup hover effects แบบ performance-friendly"""

        def on_enter(event):
            if item_id != self.current_selection:
                self._update_item_colors(button, self.theme.colors.gray_100)

        def on_leave(event):
            if item_id != self.current_selection:
                self._update_item_colors(button, self.theme.colors.surface)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def _update_item_colors(self, button: tk.Button, bg_color: str):
        """Update colors efficiently - no recursive loops"""
        try:
            button.configure(bg=bg_color)

            # Update only direct children
            if hasattr(button, "content_frame"):
                button.content_frame.configure(bg=bg_color)
            if hasattr(button, "layout_frame"):
                button.layout_frame.configure(bg=bg_color)
            if hasattr(button, "icon_label"):
                button.icon_label.configure(bg=bg_color)
            if hasattr(button, "title_label"):
                button.title_label.configure(bg=bg_color)

        except tk.TclError:
            pass  # Handle widget destruction gracefully

    def _handle_nav_click(self, item_id: str):
        """Handle navigation click ด้วย proper state management"""
        if item_id == self.current_selection:
            return

        # Update visual state
        old_selection = self.current_selection
        self.current_selection = item_id

        # Reset old selection
        if old_selection and old_selection in self.menu_buttons:
            self._update_item_colors(
                self.menu_buttons[old_selection], self.theme.colors.surface
            )

        # Highlight new selection
        if item_id in self.menu_buttons:
            self._update_item_colors(
                self.menu_buttons[item_id], self.theme.colors.primary_light
            )

            # Update text color for active state
            button = self.menu_buttons[item_id]
            if hasattr(button, "title_label"):
                button.title_label.configure(fg=self.theme.colors.primary_dark)

        # Execute callback
        if self.callback:
            try:
                self.callback(item_id)
            except Exception as e:
                print(f"Navigation callback error: {e}")

    def _create_footer_section(self, parent):
        """Footer section ด้วย proper spacing"""
        # Footer container
        footer_frame = tk.Frame(
            parent,
            bg=self.theme.colors.surface,
            height=self.theme.spacing.xl + self.theme.spacing.lg,
        )
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)

        # Footer content
        footer_content = tk.Frame(
            footer_frame,
            bg=self.theme.colors.surface,
            padx=self.theme.spacing.lg,
            pady=self.theme.spacing.md,
        )
        footer_content.pack(expand=True, fill="both")

        # Version info
        version_label = tk.Label(
            footer_content,
            text="DENSO888 Professional v3.0",
            font=self.theme.fonts.get("caption"),
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_tertiary,
        )
        version_label.pack(anchor="w")

        # Status indicator
        self.status_label = tk.Label(
            footer_content,
            text="🟢 System Ready",
            font=self.theme.fonts.get("caption"),
            bg=self.theme.colors.surface,
            fg=self.theme.colors.success,
        )
        self.status_label.pack(anchor="w", pady=(4, 0))

    def select_item(self, item_id: str):
        """Programmatically select menu item"""
        if item_id in self.menu_buttons:
            self._handle_nav_click(item_id)

    def update_status(self, status: str, status_type: str = "info"):
        """Update footer status"""
        status_colors = {
            "info": self.theme.colors.text_secondary,
            "success": self.theme.colors.success,
            "warning": self.theme.colors.warning,
            "error": self.theme.colors.error,
        }

        status_icons = {"info": "🔵", "success": "🟢", "warning": "🟡", "error": "🔴"}

        icon = status_icons.get(status_type, "🔵")
        color = status_colors.get(status_type, status_colors["info"])

        if hasattr(self, "status_label"):
            self.status_label.configure(text=f"{icon} {status}", fg=color)

    def get_widget(self) -> tk.Widget:
        """Get main sidebar widget"""
        return self.widget


# Enhanced Status Bar Component
class ModernStatusBar:
    """Professional status bar ด้วย consistent design"""

    def __init__(self, parent: tk.Widget):
        self.parent = parent
        self.theme = modern_theme
        self.widget = self._create_status_bar()

    def _create_status_bar(self):
        """สร้าง status bar แบบ professional"""
        # Main status bar container
        status_bar = tk.Frame(
            self.parent, bg=self.theme.colors.surface, height=32, relief="flat", bd=0
        )
        status_bar.pack_propagate(False)

        # Status bar content ด้วย proper padding
        content_frame = tk.Frame(
            status_bar,
            bg=self.theme.colors.surface,
            padx=self.theme.spacing.lg,
            pady=self.theme.spacing.xs,
        )
        content_frame.pack(fill="both", expand=True)

        # Left section - Status message
        self.status_label = tk.Label(
            content_frame,
            text="Ready",
            font=self.theme.fonts.get("body_sm"),
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_secondary,
        )
        self.status_label.pack(side="left")

        # Right section - System info
        right_section = tk.Frame(content_frame, bg=self.theme.colors.surface)
        right_section.pack(side="right")

        # Database status
        self.db_status = tk.Label(
            right_section,
            text="🔴 Database: Disconnected",
            font=self.theme.fonts.get("body_sm"),
            bg=self.theme.colors.surface,
            fg=self.theme.colors.error,
        )
        self.db_status.pack(side="right", padx=(self.theme.spacing.md, 0))

        # Current time
        self.time_label = tk.Label(
            right_section,
            text="",
            font=self.theme.fonts.get("body_sm"),
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_tertiary,
        )
        self.time_label.pack(side="right")

        # Start time updater
        self._update_time()

        return status_bar

    def _update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=current_time)
        self.widget.after(1000, self._update_time)

    def update_status(self, text: str, status_type: str = "info"):
        """Update status message"""
        status_colors = {
            "info": self.theme.colors.text_secondary,
            "success": self.theme.colors.success,
            "warning": self.theme.colors.warning,
            "error": self.theme.colors.error,
        }
        color = status_colors.get(status_type, status_colors["info"])
        self.status_label.configure(text=text, fg=color)

    def update_db_status(self, connected: bool):
        """Update database connection status"""
        if connected:
            self.db_status.configure(
                text="🟢 Database: Connected", fg=self.theme.colors.success
            )
        else:
            self.db_status.configure(
                text="🔴 Database: Disconnected", fg=self.theme.colors.error
            )

    def get_widget(self) -> tk.Widget:
        """Get status bar widget"""
        return self.widget

# Enhanced Layout Management - Added by Professional Patch
        
    def _create_sidebar(self):
        """สร้าง sidebar ด้วย layout ที่ถูกต้อง - NO PADDING OVERLAP"""
        sidebar = tk.Frame(
            self.parent,
            bg=self.theme.colors.surface,
            width=self.theme.spacing.sidebar_width,
            relief='flat',
            bd=0
        )
        sidebar.pack_propagate(False)
        
        # Sections ด้วย proper spacing
        self._create_brand_section(sidebar)
        self._create_navigation_section(sidebar) 
        self._create_footer_section(sidebar)
        
        return sidebar
        
    def _create_nav_item(self, parent, item):
        """Create nav item ด้วย single-level padding"""
        item_container = tk.Frame(parent, bg=self.theme.colors.surface)
        item_container.pack(fill='x', pady=1)
        
        button = tk.Button(
            item_container,
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
            relief='flat',
            bd=0,
            cursor='hand2',
            command=lambda: self._handle_nav_click(item['id']),
            padx=self.theme.spacing.md,
            pady=self.theme.spacing.sm
        )
        button.pack(fill='x')
        
        # Content layout - NO NESTED FRAMES
        self._setup_button_content(button, item)
        return button
