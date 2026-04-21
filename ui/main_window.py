# ui/main_window.py
import tkinter as tk
from tkinter import ttk
from service.health_service import HealthService
from service.data_center import DataCenter
from ui.profile_input import ProfileInputPage
from ui.overview_tab import OverviewTab
from ui.profile_tab import ProfileTab
from ui.mood_tab import MoodTab
from ui.ai_tab import AITab
from ui.analytics_tab import AnalyticsTab
# 移除内嵌的 ScrollableFrame 类定义

class MainWindow:
    def __init__(self, root):
        print("MainWindow.__init__ 开始")
        self.root = root
        self.root.title("健康管理小助手")
        self.root.geometry("750x600")
        self.root.minsize(600, 450)
        self.root.resizable(True, True)
        root.option_add("*Font", "微软雅黑 10")
        print("基本设置完成")

        self.health_service = HealthService()
        print("HealthService 创建完成")
        DataCenter.register_update_callback(self.refresh_window)
        print("回调注册完成")

        if not self.health_service.is_profile_exists():
            print("档案不存在，进入录入页")
            self.show_profile_input()
        else:
            print("档案存在，同步数据并进入主应用")
            self.health_service._sync_to_datacenter()
            self.show_main_app()
        print("MainWindow.__init__ 结束")

        self._refreshing = False   # 添加刷新锁
        DataCenter.register_update_callback(self.refresh_window)
    def refresh_window(self):
        if self._refreshing:
            return
        if hasattr(self, "notebook"):
            self._refreshing = True
            try:
                self.show_main_app()
            finally:
                self._refreshing = False
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def refresh_window(self):
        if hasattr(self, "notebook"):
            self.show_main_app()

    def show_profile_input(self):
        self.clear_window()
        ProfileInputPage(self.root, self.show_main_app)

    def show_main_app(self):
        print("show_main_app 开始")
        self.clear_window()
        print("clear_window 完成")
        user_name = DataCenter.get("user_name", "用户")
        print(f"user_name = {user_name}")

        top_bar = ttk.Frame(self.root)
        top_bar.pack(fill=tk.X, pady=10, padx=20)
        print("top_bar 创建完成")
        ttk.Label(top_bar, text=f"👋 欢迎回来，{user_name}！", font=("微软雅黑", 18, "bold")).pack(side=tk.LEFT)
        edit_btn = ttk.Button(top_bar, text="修改基础档案", command=self.show_profile_input)
        edit_btn.pack(side=tk.RIGHT)
        print("顶部标签和按钮添加完成")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        print("notebook 创建完成")

        print("开始创建 OverviewTab")
        OverviewTab(self.notebook)
        print("OverviewTab 创建完成")

        print("开始创建 MoodTab")
        MoodTab(self.notebook)
        print("MoodTab 创建完成")

        print("开始创建 AnalyticsTab")
        AnalyticsTab(self.notebook)
        print("AnalyticsTab 创建完成")

        print("开始创建 AITab")
        AITab(self.notebook)   
        print("AITab 创建完成")

        print("开始创建 ProfileTab")
        ProfileTab(self.notebook)
        print("ProfileTab 创建完成")

        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, pady=15)
        close_btn = ttk.Button(bottom_frame, text="关闭程序", command=self.root.quit, width=15)
        close_btn.pack(side=tk.RIGHT, padx=30)
        print("底部按钮创建完成")
        print("show_main_app 结束")