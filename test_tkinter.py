#!/usr/bin/env python3
"""
ทดสอบ Tkinter Installation
"""

def test_tkinter():
    """ทดสอบว่า Tkinter ทำงานได้หรือไม่"""
    
    try:
        print("🧪 Testing Tkinter...")
        import tkinter as tk
        
        # สร้างหน้าต่างทดสอบ
        root = tk.Tk()
        root.title("DENSO888 - Tkinter Test")
        root.geometry("300x200")
        
        # เพิ่ม label
        label = tk.Label(root, text="✅ Tkinter works!", font=("Arial", 14))
        label.pack(expand=True)
        
        # เพิ่มปุ่มปิด
        btn = tk.Button(root, text="Close", command=root.quit)
        btn.pack(pady=10)
        
        print("✅ Tkinter OK - หน้าต่างทดสอบจะเปิดขึ้น")
        print("   กดปุ่ม Close เพื่อปิด")
        
        root.mainloop()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"❌ Tkinter Error: {e}")
        print("\n💡 Solutions:")
        print("1. Reinstall Python with 'Add Tcl/Tk and IDLE' checked")
        print("2. Try: conda install tk")  
        print("3. Use different Python version")
        return False


if __name__ == "__main__":
    if test_tkinter():
        print("\n🎉 Tkinter พร้อมใช้งาน! ลอง: python main.py")
    else:
        print("\n⚠️ ต้องแก้ไข Tkinter ก่อนใช้งาน DENSO888")
