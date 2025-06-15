import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def debug_window_behavior():
    """Debug window state changes"""
    from gui.main_window import DENSO888GamingEdition

    app = DENSO888GamingEdition()

    # Monitor window state
    def monitor_state():
        state = app.root.state()
        visible = app.root.winfo_viewable()
        print(f"🔍 Window state: {state}, Visible: {visible}")
        app.root.after(500, monitor_state)

    # Force stay visible
    def force_visible():
        app.root.deiconify()
        app.root.lift()
        app.root.after(1000, force_visible)

    # Start monitoring
    app.root.after(100, monitor_state)
    app.root.after(100, force_visible)

    # Override any minimize attempts
    def prevent_minimize(event=None):
        print("🚫 Preventing window minimize")
        app.root.deiconify()
        return "break"

    app.root.bind("<Unmap>", prevent_minimize)

    print("🧪 Debug mode - window will stay visible")
    app.run()


if __name__ == "__main__":
    debug_window_behavior()
