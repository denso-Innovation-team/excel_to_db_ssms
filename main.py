#!/usr/bin/env python3
"""
main.py - DENSO888 Clean Entry Point
Created by: Thammaphon Chittasuwanna (SDM)
เฮียตอมจัดหั้ย!!! 🚀
"""

import sys
import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from config import config
    print(f"🏭 {config.APP_NAME} v{config.VERSION}")
    print(f"Created by: {config.AUTHOR}")
except ImportError:
    print("❌ Configuration not found")

def create_simple_gui():
    """สร้าง GUI เรียบง่าย"""
    root = tk.Tk()
    root.title(f"🏭 DENSO888")
    root.geometry("800x600")
    
    # Header
    header = tk.Frame(root, bg="#DC0003", height=80)
    header.pack(fill="x")
    header.pack_propagate(False)
    
    title = tk.Label(header, text="🏭 DENSO888", 
                    font=("Arial", 20, "bold"), fg="white", bg="#DC0003")
    title.pack(expand=True)
    
    # Content
    content = tk.Frame(root)
    content.pack(fill="both", expand=True, padx=40, pady=40)
    
    tk.Label(content, text="Excel to SQL Management System",
            font=("Arial", 14)).pack(pady=20)
    
    tk.Label(content, text="Created by: Thammaphon Chittasuwanna (SDM)\nเฮียตอมจัดหั้ย!!! 🚀",
            font=("Arial", 12), justify="center").pack(pady=10)
    
    # Buttons
    def import_excel():
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if file_path:
            messagebox.showinfo("Success", f"Selected: {Path(file_path).name}")
    
    def show_about():
        messagebox.showinfo("About", "DENSO888 v2.0.0\nThammaphon Chittasuwanna (SDM)")
    
    btn_frame = tk.Frame(content)
    btn_frame.pack(pady=30)
    
    tk.Button(btn_frame, text="📊 Import Excel", command=import_excel,
             font=("Arial", 12), bg="#DC0003", fg="white", 
             padx=20, pady=10).pack(pady=10)
    
    tk.Button(btn_frame, text="ℹ️ About", command=show_about,
             font=("Arial", 12), bg="#6C757D", fg="white",
             padx=20, pady=10).pack(pady=10)
    
    return root

def main():
    """Main function"""
    try:
        root = create_simple_gui()
        root.mainloop()
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
