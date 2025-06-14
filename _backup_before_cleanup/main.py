#!/usr/bin/env python3
"""
main.py - Working DENSO888 Entry Point
เฮียตอมจัดหั้ย!!! 🚀
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import sys
from pathlib import Path

def create_simple_ui():
    """สร้าง UI แบบ Simple ที่ใช้งานได้แน่นอน"""
    
    root = tk.Tk()
    root.title("🏭 DENSO888 - Working Edition")
    root.geometry("900x600")
    root.configure(bg="white")
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Header
    header = tk.Frame(root, bg="#DC0003", height=100)
    header.pack(fill="x")
    header.pack_propagate(False)
    
    title_label = tk.Label(
        header,
        text="🏭 DENSO888",
        font=("Arial", 28, "bold"),
        fg="white",
        bg="#DC0003"
    )
    title_label.pack(expand=True)
    
    # Main content
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(fill="both", expand=True, padx=40, pady=40)
    
    # Welcome section
    welcome_frame = tk.Frame(main_frame, bg="white")
    welcome_frame.pack(expand=True)
    
    tk.Label(
        welcome_frame,
        text="Excel to SQL Management System",
        font=("Arial", 18),
        bg="white",
        fg="#333"
    ).pack(pady=20)
    
    tk.Label(
        welcome_frame,
        text="Created by Thammaphon Chittasuwanna (SDM) | Innovation",
        font=("Arial", 12),
        bg="white",
        fg="#666"
    ).pack(pady=10)
    
    tk.Label(
        welcome_frame,
        text="เฮียตอมจัดหั้ย!!! 🚀",
        font=("Arial", 16, "bold"),
        bg="white",
        fg="#DC0003"
    ).pack(pady=20)
    
    # Feature buttons
    button_frame = tk.Frame(welcome_frame, bg="white")
    button_frame.pack(pady=40)
    
    def import_excel():
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if file_path:
            messagebox.showinfo("Success", f"Selected: {Path(file_path).name}")
    
    def generate_mock():
        messagebox.showinfo("Mock Data", "Mock data generation feature coming soon!")
    
    def database_config():
        messagebox.showinfo("Database", "Database configuration panel coming soon!")
    
    def about():
        about_text = """🏭 DENSO888 v2.0.0
        
Excel to SQL Management System

Created by: Thammaphon Chittasuwanna (SDM)
Department: Innovation | DENSO Corporation
Nickname: เฮียตอมจัดหั้ย!!!

© 2024 DENSO Corporation"""
        messagebox.showinfo("About DENSO888", about_text)
    
    # Create buttons
    buttons = [
        ("📊 Import Excel File", import_excel, "#DC0003"),
        ("🎲 Generate Mock Data", generate_mock, "#28A745"),
        ("🗄️ Database Config", database_config, "#007BFF"),
        ("ℹ️ About DENSO888", about, "#6C757D")
    ]
    
    for i, (text, command, color) in enumerate(buttons):
        row = i // 2
        col = i % 2
        
        btn = tk.Button(
            button_frame,
            text=text,
            command=command,
            font=("Arial", 12, "bold"),
            bg=color,
            fg="white",
            padx=30,
            pady=15,
            relief="flat",
            cursor="hand2",
            width=20
        )
        btn.grid(row=row, column=col, padx=15, pady=10)
    
    # Status bar
    status_bar = tk.Frame(root, bg="#f0f0f0", height=30)
    status_bar.pack(side="bottom", fill="x")
    status_bar.pack_propagate(False)
    
    status_label = tk.Label(
        status_bar,
        text="🟢 DENSO888 Ready - Working Edition",
        font=("Arial", 10),
        bg="#f0f0f0",
        fg="#333"
    )
    status_label.pack(side="left", padx=10, pady=5)
    
    version_label = tk.Label(
        status_bar,
        text="v2.0.0 | Optimized",
        font=("Arial", 9),
        bg="#f0f0f0",
        fg="#666"
    )
    version_label.pack(side="right", padx=10, pady=5)
    
    return root

def main():
    """Main function with error handling"""
    
    print("🏭 Starting DENSO888...")
    print("Created by: Thammaphon Chittasuwanna (SDM)")
    print("เฮียตอมจัดหั้ย!!! 🚀")
    
    try:
        # Try modern UI first
        print("🔄 Attempting to load modern interface...")
        
        # Add project root to path
        project_root = Path(__file__).parent
        sys.path.insert(0, str(project_root))
        
        try:
            from gui.windows.modern_main_window import ModernDENSO888MainWindow
            print("✅ Modern UI loaded successfully")
            app = ModernDENSO888MainWindow()
            app.run()
            return
            
        except Exception as e:
            print(f"⚠️ Modern UI failed: {e}")
            print("🔄 Falling back to simple interface...")
        
        # Fallback to simple UI
        root = create_simple_ui()
        print("✅ Simple UI loaded successfully")
        
        def on_closing():
            if messagebox.askyesno("Exit", "Exit DENSO888?"):
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Critical error: {e}")
        print("Press Enter to exit...")
        input()

if __name__ == "__main__":
    main()
