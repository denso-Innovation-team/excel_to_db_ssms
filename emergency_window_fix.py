import tkinter as tk


def emergency_window_test():
    """Test basic Tkinter window visibility"""
    try:
        root = tk.Tk()
        root.title("🚨 DENSO888 Emergency Window Test")
        root.geometry("400x300+100+100")
        root.configure(bg="red")

        # Force to front
        root.lift()
        root.attributes("-topmost", True)

        label = tk.Label(
            root,
            text="🚨 EMERGENCY TEST\n\nIf you see this, Tkinter works!\n\nClick OK to continue",
            font=("Arial", 14),
            bg="red",
            fg="white",
            pady=50,
        )
        label.pack(expand=True)

        def close_test():
            print("✅ Emergency test passed - Tkinter window visible!")
            root.destroy()

        ok_button = tk.Button(
            root,
            text="OK - I can see this window",
            command=close_test,
            font=("Arial", 12),
            bg="white",
            fg="red",
            padx=20,
            pady=10,
        )
        ok_button.pack(pady=20)

        # Remove topmost after 2 seconds
        root.after(2000, lambda: root.attributes("-topmost", False))

        print("🚨 Emergency test window created")
        root.mainloop()

    except Exception as e:
        print(f"❌ Emergency test failed: {e}")


if __name__ == "__main__":
    emergency_window_test()
