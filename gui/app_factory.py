"""
GUI Factory Pattern for DENSO888
Supports multiple UI implementations
"""

from abc import ABC, abstractmethod
from typing import Optional
import tkinter as tk

class BaseWindow(ABC):
    """Abstract base class for all windows"""
    
    def __init__(self, config=None):
        self.config = config
        self.root = None
        
    @abstractmethod
    def create_window(self) -> tk.Tk:
        pass
        
    @abstractmethod
    def run(self) -> int:
        pass

class AppFactory:
    """Factory for creating GUI applications"""
    
    @staticmethod
    def create_app(mode: str = "auto", config=None) -> BaseWindow:
        """Create application based on mode"""
        
        if mode == "modern":
            from .modern_ui import ModernWindow
            return ModernWindow(config)
        elif mode == "classic":
            from .classic_ui import ClassicWindow  
            return ClassicWindow(config)
        else:
            # Auto-detect best mode
            try:
                from .modern_ui import ModernWindow
                return ModernWindow(config)
            except ImportError:
                from .classic_ui import ClassicWindow
                return ClassicWindow(config)
