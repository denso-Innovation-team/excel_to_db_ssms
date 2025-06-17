"""
Emergency UI Fix - แก้ปัญหา Layout พังเละ
"""

import tkinter as tk


class FixedMainWindow:
    """แก้ไข MainWindow ให้ทำงานได้จริง"""

    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_fixed_layout()

    def setup_window(self):
        """ตั้งค่าหน้าต่างให้ถูกต้อง"""
        self.root.title("🏭 DENSO888 Professional Edition - FIXED")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)

        # สำคัญ: กำหนด weight ให้ถูกต้อง
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def create_fixed_layout(self):
        """Layout ที่ทำงานได้จริง - ไม่ซ้อนมั่ว"""

        # 1. Sidebar (ซ้าย)
        self.sidebar = tk.Frame(self.root, bg="#F8F9FA", width=250)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # 2. Main Content (ขวา)
        self.content = tk.Frame(self.root, bg="#FFFFFF")
        self.content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # 3. Status Bar (ล่าง)
        self.status_bar = tk.Frame(self.root, bg="#E5E7EB", height=30)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.status_bar.grid_propagate(False)

        self.create_sidebar_content()
        self.create_main_content()
        self.create_status_content()

    def create_sidebar_content(self):
        """Sidebar ที่ทำงานได้"""
        # Header
        header = tk.Label(
            self.sidebar, text="🏭 DENSO888", font=("Arial", 16, "bold"), bg="#F8F9FA"
        )
        header.pack(pady=20)

        # Navigation Menu
        menu_items = [
            ("📊 Dashboard", self.show_dashboard),
            ("📁 Import Excel", self.show_import),
            ("🗄️ Database", self.show_database),
            ("🎲 Mock Data", self.show_mock),
        ]

        for text, command in menu_items:
            btn = tk.Button(
                self.sidebar,
                text=text,
                command=command,
                bg="#FFFFFF",
                relief="flat",
                anchor="w",
                padx=20,
                pady=10,
                width=20,
            )
            btn.pack(fill="x", padx=10, pady=2)

            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#E3F2FD"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#FFFFFF"))

    def create_main_content(self):
        """Main content area ที่แสดงผลได้จริง"""
        # Title
        title = tk.Label(
            self.content, text="Welcome to DENSO888", font=("Arial", 24, "bold")
        )
        title.pack(pady=20)

        # Stats Cards Container
        stats_frame = tk.Frame(self.content)
        stats_frame.pack(fill="x", pady=20)

        # Configure grid
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)

        # Stats Cards
        stats = [
            ("📊 Tables", "21", "#3B82F6"),
            ("📝 Records", "30,614", "#10B981"),
            ("📁 Imports", "12", "#F59E0B"),
            ("🎲 Mock Data", "7,364", "#8B5CF6"),
        ]

        for i, (title, value, color) in enumerate(stats):
            card = self.create_stat_card(stats_frame, title, value, color)
            card.grid(row=0, column=i, padx=10, sticky="ew")

        # Action Buttons
        actions_frame = tk.Frame(self.content)
        actions_frame.pack(fill="x", pady=30)

        actions = [
            ("📊 Import Excel", "#3B82F6"),
            ("🎲 Generate Mock Data", "#10B981"),
            ("🗄️ Database Setup", "#F59E0B"),
            ("📈 View Analytics", "#8B5CF6"),
        ]

        for i, (text, color) in enumerate(actions):
            btn = tk.Button(
                actions_frame,
                text=text,
                bg=color,
                fg="white",
                font=("Arial", 12),
                padx=20,
                pady=10,
                relief="flat",
            )
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=5, sticky="ew")

        # Configure action buttons grid
        actions_frame.grid_columnconfigure(0, weight=1)
        actions_frame.grid_columnconfigure(1, weight=1)

    def create_stat_card(self, parent, title, value, color):
        """สร้าง stat card ที่แสดงผลได้"""
        card = tk.Frame(parent, bg="white", relief="solid", bd=1, padx=15, pady=15)

        # Title
        title_label = tk.Label(
            card, text=title, font=("Arial", 10), bg="white", fg="#6B7280"
        )
        title_label.pack()

        # Value
        value_label = tk.Label(
            card, text=value, font=("Arial", 20, "bold"), bg="white", fg=color
        )
        value_label.pack(pady=(5, 0))

        return card

    def create_status_content(self):
        """Status bar content"""
        status_label = tk.Label(
            self.status_bar,
            text="🟢 Ready | Database: Disconnected | 13:39:45",
            bg="#E5E7EB",
            fg="#374151",
            font=("Arial", 9),
        )
        status_label.pack(side="left", padx=10, pady=5)

    # Navigation Methods
    def show_dashboard(self):
        print("📊 Dashboard clicked - ทำงานได้!")

    def show_import(self):
        print("📁 Import clicked - ทำงานได้!")

    def show_database(self):
        print("🗄️ Database clicked - ทำงานได้!")

    def show_mock(self):
        print("🎲 Mock Data clicked - ทำงานได้!")

    def run(self):
        """เริ่มแอป"""
        self.root.mainloop()


# Quick Test
if __name__ == "__main__":
    app = FixedMainWindow()
    app.run()
