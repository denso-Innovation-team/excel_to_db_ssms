# gui/core/__init__.py
"""
UI Core Components - Reusable & Maintainable
แยก UI logic เป็น modules ที่ maintain ได้ง่าย
"""

from abc import ABC, abstractmethod
from typing import Protocol, Callable, Any, Optional
import tkinter as tk
from dataclasses import dataclass


# ===== THEME PROTOCOL =====
@dataclass
class ThemeColors:
    """Theme color definitions"""

    primary: str = "#DC0003"
    primary_dark: str = "#B80002"
    primary_light: str = "#FF3333"
    secondary: str = "#2C3E50"
    success: str = "#28A745"
    warning: str = "#FFC107"
    danger: str = "#DC3545"
    background: str = "#FFFFFF"
    surface: str = "#F8F9FA"
    text_primary: str = "#2C3E50"
    text_secondary: str = "#7F8C8D"
    border: str = "#E5E8EB"


class ThemeProvider(Protocol):
    """Theme provider interface"""

    def get_colors(self) -> ThemeColors: ...
    def apply_to_widget(self, widget: tk.Widget): ...


# ===== BASE COMPONENTS =====
class BaseComponent(ABC):
    """Base class for all UI components"""

    def __init__(self, parent: tk.Widget, theme: ThemeProvider):
        self.parent = parent
        self.theme = theme
        self.colors = theme.get_colors()
        self.widget: Optional[tk.Widget] = None

    @abstractmethod
    def create(self) -> tk.Widget:
        """Create the UI component"""
        pass

    def get_widget(self) -> tk.Widget:
        """Get the underlying widget"""
        if self.widget is None:
            self.widget = self.create()
        return self.widget

    def pack(self, **kwargs):
        """Pack the component"""
        self.get_widget().pack(**kwargs)

    def grid(self, **kwargs):
        """Grid the component"""
        self.get_widget().grid(**kwargs)


# ===== BUTTON COMPONENTS =====
class ModernButton(BaseComponent):
    """Modern button with consistent styling"""

    def __init__(
        self,
        parent: tk.Widget,
        theme: ThemeProvider,
        text: str = "",
        command: Callable = None,
        style: str = "primary",
        size: str = "medium",
    ):
        super().__init__(parent, theme)
        self.text = text
        self.command = command
        self.style = style
        self.size = size

        # Style definitions
        self.styles = {
            "primary": {"bg": self.colors.primary, "fg": "white"},
            "secondary": {"bg": self.colors.secondary, "fg": "white"},
            "success": {"bg": self.colors.success, "fg": "white"},
            "danger": {"bg": self.colors.danger, "fg": "white"},
            "outline": {"bg": self.colors.background, "fg": self.colors.primary},
        }

        self.sizes = {
            "small": {"font": ("Segoe UI", 9), "padding": (8, 4)},
            "medium": {"font": ("Segoe UI", 10), "padding": (12, 8)},
            "large": {"font": ("Segoe UI", 12, "bold"), "padding": (16, 12)},
        }

    def create(self) -> tk.Widget:
        """Create the button"""
        style_config = self.styles[self.style]
        size_config = self.sizes[self.size]

        button = tk.Button(
            self.parent,
            text=self.text,
            command=self.command,
            bg=style_config["bg"],
            fg=style_config["fg"],
            font=size_config["font"],
            relief="flat",
            borderwidth=0,
            cursor="hand2",
        )

        # Apply padding
        button.configure(padx=size_config["padding"][0], pady=size_config["padding"][1])

        # Add hover effects
        self._add_hover_effects(button)

        return button

    def _add_hover_effects(self, button: tk.Button):
        """Add hover animations"""
        original_bg = button.cget("bg")
        hover_color = self._get_hover_color(original_bg)

        def on_enter(e):
            button.configure(bg=hover_color)

        def on_leave(e):
            button.configure(bg=original_bg)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def _get_hover_color(self, base_color: str) -> str:
        """Get hover color variation"""
        hover_colors = {
            self.colors.primary: self.colors.primary_light,
            self.colors.secondary: "#34495E",
            self.colors.success: "#34CE57",
            self.colors.danger: "#E4606D",
        }
        return hover_colors.get(base_color, base_color)


class IconButton(ModernButton):
    """Button with icon support"""

    def __init__(
        self,
        parent: tk.Widget,
        theme: ThemeProvider,
        icon: str = "",
        text: str = "",
        **kwargs,
    ):
        self.icon = icon
        display_text = f"{icon} {text}".strip()
        super().__init__(parent, theme, text=display_text, **kwargs)


# ===== CARD COMPONENTS =====
class Card(BaseComponent):
    """Modern card container"""

    def __init__(
        self,
        parent: tk.Widget,
        theme: ThemeProvider,
        title: str = "",
        padding: int = 20,
    ):
        super().__init__(parent, theme)
        self.title = title
        self.padding = padding
        self.content_frame: Optional[tk.Frame] = None

    def create(self) -> tk.Widget:
        """Create the card"""
        # Main card frame
        card = tk.Frame(
            self.parent,
            bg=self.colors.surface,
            relief="flat",
            borderwidth=1,
            highlightbackground=self.colors.border,
            highlightthickness=1,
        )

        # Title section
        if self.title:
            title_frame = tk.Frame(card, bg=self.colors.surface)
            title_frame.pack(fill="x", padx=self.padding, pady=(self.padding, 0))

            title_label = tk.Label(
                title_frame,
                text=self.title,
                font=("Segoe UI", 14, "bold"),
                fg=self.colors.text_primary,
                bg=self.colors.surface,
            )
            title_label.pack(anchor="w")

        # Content frame
        self.content_frame = tk.Frame(card, bg=self.colors.surface)
        padding_top = 10 if self.title else self.padding
        self.content_frame.pack(
            fill="both",
            expand=True,
            padx=self.padding,
            pady=(padding_top, self.padding),
        )

        return card

    def add_widget(self, widget_class, **kwargs) -> Any:
        """Add widget to card content"""
        if self.content_frame is None:
            self.get_widget()  # Ensure card is created

        return widget_class(self.content_frame, self.theme, **kwargs)


# ===== FORM COMPONENTS =====
class FormField(BaseComponent):
    """Consistent form field with label"""

    def __init__(
        self,
        parent: tk.Widget,
        theme: ThemeProvider,
        label: str,
        field_type: str = "entry",
        **kwargs,
    ):
        super().__init__(parent, theme)
        self.label = label
        self.field_type = field_type
        self.field_kwargs = kwargs
        self.field_widget: Optional[tk.Widget] = None

    def create(self) -> tk.Widget:
        """Create form field"""
        container = tk.Frame(self.parent, bg=self.colors.background)

        # Label
        label_widget = tk.Label(
            container,
            text=self.label,
            font=("Segoe UI", 10, "bold"),
            fg=self.colors.text_primary,
            bg=self.colors.background,
        )
        label_widget.pack(anchor="w", pady=(0, 5))

        # Field widget
        if self.field_type == "entry":
            self.field_widget = self._create_entry(container)
        elif self.field_type == "text":
            self.field_widget = self._create_text(container)
        elif self.field_type == "combo":
            self.field_widget = self._create_combobox(container)

        self.field_widget.pack(fill="x")

        return container

    def _create_entry(self, parent) -> tk.Entry:
        """Create entry widget"""
        entry = tk.Entry(
            parent,
            font=("Segoe UI", 10),
            relief="solid",
            borderwidth=1,
            **self.field_kwargs,
        )

        # Focus effects
        def on_focus_in(e):
            entry.configure(highlightbackground=self.colors.primary)

        def on_focus_out(e):
            entry.configure(highlightbackground=self.colors.border)

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        return entry

    def _create_text(self, parent) -> tk.Text:
        """Create text widget"""
        from tkinter import scrolledtext

        text = scrolledtext.ScrolledText(
            parent,
            font=("Segoe UI", 10),
            relief="solid",
            borderwidth=1,
            height=5,
            **self.field_kwargs,
        )

        return text

    def _create_combobox(self, parent):
        """Create combobox widget"""
        try:
            from tkinter import ttk

            combo = ttk.Combobox(parent, font=("Segoe UI", 10), **self.field_kwargs)
            return combo
        except ImportError:
            # Fallback to basic entry
            return self._create_entry(parent)

    def get_value(self) -> str:
        """Get field value"""
        if not self.field_widget:
            return ""

        if isinstance(self.field_widget, tk.Entry):
            return self.field_widget.get()
        elif isinstance(self.field_widget, tk.Text):
            return self.field_widget.get("1.0", tk.END).strip()
        elif hasattr(self.field_widget, "get"):
            return self.field_widget.get()

        return ""

    def set_value(self, value: str):
        """Set field value"""
        if not self.field_widget:
            return

        if isinstance(self.field_widget, tk.Entry):
            self.field_widget.delete(0, tk.END)
            self.field_widget.insert(0, value)
        elif isinstance(self.field_widget, tk.Text):
            self.field_widget.delete("1.0", tk.END)
            self.field_widget.insert("1.0", value)


# ===== LAYOUT COMPONENTS =====
class ResponsiveGrid(BaseComponent):
    """Responsive grid layout"""

    def __init__(
        self, parent: tk.Widget, theme: ThemeProvider, columns: int = 2, gap: int = 10
    ):
        super().__init__(parent, theme)
        self.columns = columns
        self.gap = gap
        self.items = []

    def create(self) -> tk.Widget:
        """Create grid container"""
        container = tk.Frame(self.parent, bg=self.colors.background)

        # Configure column weights
        for i in range(self.columns):
            container.grid_columnconfigure(i, weight=1)

        return container

    def add_item(self, item_widget: tk.Widget):
        """Add item to grid"""
        if self.widget is None:
            self.get_widget()

        row = len(self.items) // self.columns
        col = len(self.items) % self.columns

        item_widget.grid(
            row=row, column=col, padx=self.gap // 2, pady=self.gap // 2, sticky="nsew"
        )

        # Configure row weight
        self.widget.grid_rowconfigure(row, weight=1)

        self.items.append(item_widget)


class Sidebar(BaseComponent):
    """Modern sidebar navigation"""

    def __init__(self, parent: tk.Widget, theme: ThemeProvider, width: int = 250):
        super().__init__(parent, theme)
        self.width = width
        self.nav_items = []

    def create(self) -> tk.Widget:
        """Create sidebar"""
        sidebar = tk.Frame(
            self.parent,
            bg=self.colors.surface,
            width=self.width,
            relief="flat",
            borderwidth=1,
            highlightbackground=self.colors.border,
            highlightthickness=1,
        )
        sidebar.pack_propagate(False)

        return sidebar

    def add_nav_item(self, icon: str, text: str, command: Callable):
        """Add navigation item"""
        if self.widget is None:
            self.get_widget()

        nav_button = IconButton(
            self.widget,
            self.theme,
            icon=icon,
            text=text,
            command=command,
            style="outline",
            size="medium",
        )
        nav_button.pack(fill="x", padx=10, pady=2)

        self.nav_items.append(nav_button)
        return nav_button


# ===== SIMPLE THEME IMPLEMENTATION =====
class SimpleTheme:
    """Simple theme provider implementation"""

    def __init__(self, theme_name: str = "denso"):
        self.themes = {
            "denso": ThemeColors(),  # Default DENSO colors
            "dark": ThemeColors(
                primary="#6366F1",
                background="#1F2937",
                surface="#374151",
                text_primary="#F9FAFB",
                text_secondary="#D1D5DB",
            ),
        }
        self.current_theme = theme_name

    def get_colors(self) -> ThemeColors:
        """Get current theme colors"""
        return self.themes.get(self.current_theme, self.themes["denso"])

    def apply_to_widget(self, widget: tk.Widget):
        """Apply theme to widget"""
        colors = self.get_colors()
        try:
            widget.configure(bg=colors.background, fg=colors.text_primary)
        except tk.TclError:
            pass  # Widget doesn't support these options


# ===== COMPONENT FACTORY =====
class ComponentFactory:
    """Factory for creating consistent UI components"""

    def __init__(self, theme: ThemeProvider):
        self.theme = theme

    def create_button(self, parent: tk.Widget, **kwargs) -> ModernButton:
        """Create consistent button"""
        return ModernButton(parent, self.theme, **kwargs)

    def create_card(self, parent: tk.Widget, **kwargs) -> Card:
        """Create consistent card"""
        return Card(parent, self.theme, **kwargs)

    def create_form_field(self, parent: tk.Widget, **kwargs) -> FormField:
        """Create consistent form field"""
        return FormField(parent, self.theme, **kwargs)

    def create_grid(self, parent: tk.Widget, **kwargs) -> ResponsiveGrid:
        """Create responsive grid"""
        return ResponsiveGrid(parent, self.theme, **kwargs)

    def create_sidebar(self, parent: tk.Widget, **kwargs) -> Sidebar:
        """Create sidebar"""
        return Sidebar(parent, self.theme, **kwargs)


# ===== CONVENIENCE FUNCTIONS =====
def create_component_factory(theme_name: str = "denso") -> ComponentFactory:
    """Create component factory with theme"""
    theme = SimpleTheme(theme_name)
    return ComponentFactory(theme)
