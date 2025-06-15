import tkinter as tk
from tkinter import messagebox


class MinimalDENSO888:
    """Minimal version to test basic functionality"""

    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_content()

    def setup_window(self):
        """Setup basic window"""
        self.root.title("🏭 DENSO888 Minimal Test")
        self.root.geometry("800x600+200+100")
        self.root.configure(bg="#1A1A2E")

        # Force visibility
        self.root.lift()
        self.root.focus_force()

    def create_content(self):
        """Create simple test content"""
        # Header
        header = tk.Frame(self.root, bg="#FF0066", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🏭 DENSO888 Gaming Edition - Minimal Test",
            font=("Arial", 14, "bold"),
            bg="#FF0066",
            fg="white",
        ).pack(expand=True)

        # Content area
        content = tk.Frame(self.root, bg="#0A0A0F")
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Test elements
        tk.Label(
            content,
            text="🎮 CONTENT TEST",
            font=("Arial", 20, "bold"),
            bg="#0A0A0F",
            fg="#00FFFF",
        ).pack(pady=30)

        tk.Label(
            content,
            text="Created by: Thammaphon Chittasuwanna (SDM)\nเฮียตอมจัดหั้ย!!! 🚀",
            font=("Arial", 12),
            bg="#0A0A0F",
            fg="#FFFFFF",
            justify="center",
        ).pack(pady=20)

        # Test buttons
        button_frame = tk.Frame(content, bg="#0A0A0F")
        button_frame.pack(pady=30)

        tk.Button(
            button_frame,
            text="✅ Content Works!",
            font=("Arial", 12, "bold"),
            bg="#00FF88",
            fg="black",
            padx=20,
            pady=10,
            command=self.test_success,
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="🚀 Launch Full Version",
            font=("Arial", 12, "bold"),
            bg="#FF0066",
            fg="white",
            padx=20,
            pady=10,
            command=self.launch_full,
        ).pack(side="left", padx=10)

    def test_success(self):
        """Test success callback"""
        messagebox.showinfo(
            "Test Success",
            "🎉 Content rendering works!\n\nDENSO888 should work normally.",
        )

    def launch_full(self):
        """Launch full version"""
        self.root.destroy()
        try:
            # Import and run full version
            from gui.main_window import DENSO888GamingEdition

            app = DENSO888GamingEdition()
            app.run()
        except Exception as e:
            messagebox.showerror("Launch Error", f"Full version error: {e}")

    def run(self):
        """Run minimal test"""
        print("🧪 Running DENSO888 Minimal Test...")
        self.root.mainloop()


if __name__ == "__main__":
    app = MinimalDENSO888()
    app.run()
