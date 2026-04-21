# main.py
import tkinter as tk
from ui.main_window import MainWindow
import os
import os

def main():
    root = tk.Tk()
    # 设置图标（Windows 用 .ico）
    icon_path = os.path.join(os.path.dirname(__file__), "assets", "health_icon.ico")
    if os.path.exists(icon_path):
        root.iconphoto(True, tk.PhotoImage(file=icon_path))
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()