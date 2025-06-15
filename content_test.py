import tkinter as tk


def test_content_rendering():
    """Test if content renders properly"""
    root = tk.Tk()
    root.title("🔍 Content Rendering Test")
    root.geometry("600x400+300+200")

    # Test different background colors
    colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]

    for i, color in enumerate(colors):
        frame = tk.Frame(root, bg=color, height=60)
        frame.pack(fill="x", pady=2)
        frame.pack_propagate(False)

        tk.Label(
            frame,
            text=f"Color Test {i+1}: {color}",
            bg=color,
            fg="white" if color in ["#FF0000", "#0000FF", "#FF00FF"] else "black",
            font=("Arial", 12, "bold"),
        ).pack(expand=True)

    tk.Label(
        root,
        text="หากเห็นแถบสีทั้งหมด = Content rendering ทำงานได้",
        font=("Arial", 12),
        pady=20,
    ).pack()

    def close_test():
        print("✅ Content rendering test completed")
        root.destroy()

    tk.Button(
        root,
        text="✅ เห็นหมดแล้ว - Content OK",
        command=close_test,
        font=("Arial", 12),
        bg="#00FF00",
        padx=20,
        pady=10,
    ).pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    test_content_rendering()
