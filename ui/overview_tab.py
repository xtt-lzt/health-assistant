# ui/overview_tab.py
import tkinter as tk
from tkinter import ttk
from service.data_center import DataCenter
from ui.widgets import ScrollableFrame

class OverviewTab:
    def __init__(self, notebook):
        self.tab = ScrollableFrame(notebook)
        notebook.add(self.tab, text="📊 总览看板")
        self.content = ttk.Frame(self.tab.scrollable_frame, padding=20)
        self.content.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        # 核心基准数据
        bmr = DataCenter.get("bmr", 0)
        recommend_cal = DataCenter.get("recommended_calories", 0)
        weight = DataCenter.get("weight_kg", 0)

        base_card = ttk.LabelFrame(self.content, text="核心健康基准", padding=20)
        base_card.pack(fill=tk.X, pady=10)
        base_grid = ttk.Frame(base_card)
        base_grid.pack(fill=tk.X)
        ttk.Label(base_grid, text=f"当前体重：{weight} kg", font=("微软雅黑", 11, "bold")).grid(row=0, column=0, sticky=tk.W, padx=20)
        ttk.Label(base_grid, text=f"基础代谢(BMR)：{bmr} 大卡/天", font=("微软雅黑", 11, "bold")).grid(row=0, column=1, sticky=tk.W, padx=40)
        ttk.Label(base_grid, text=f"每日推荐摄入：{recommend_cal} 大卡", font=("微软雅黑", 11, "bold")).grid(row=0, column=2, sticky=tk.W, padx=40)

        # 健康目标
        health_goal = DataCenter.get("health_goal", "暂无目标")
        goal_card = ttk.LabelFrame(self.content, text="我的健康目标", padding=20)
        goal_card.pack(fill=tk.X, pady=10)
        ttk.Label(goal_card, text=health_goal, font=("微软雅黑", 12)).pack(anchor=tk.W)

        # 今日数据汇总
        today_intake = DataCenter.get("today_calorie_intake", 0)
        today_consume = DataCenter.get("today_calorie_consume", 0)
        today_mood = DataCenter.get("today_latest_mood", "暂无记录")

        today_card = ttk.LabelFrame(self.content, text="今日数据汇总", padding=20)
        today_card.pack(fill=tk.X, pady=10)
        today_grid = ttk.Frame(today_card)
        today_grid.pack(fill=tk.X)
        ttk.Label(today_grid, text=f"今日已摄入：{today_intake} 大卡", font=("微软雅黑", 11)).grid(row=0, column=0, sticky=tk.W, padx=20, pady=10)
        ttk.Label(today_grid, text=f"今日已消耗：{today_consume} 大卡", font=("微软雅黑", 11)).grid(row=0, column=1, sticky=tk.W, padx=40, pady=10)
        ttk.Label(today_grid, text=f"今日热量缺口：{today_intake - today_consume} 大卡", font=("微软雅黑", 11)).grid(row=0, column=2, sticky=tk.W, padx=40, pady=10)
        ttk.Label(today_grid, text=f"最新心情状态：{today_mood}", font=("微软雅黑", 11)).grid(row=1, column=0, sticky=tk.W, padx=20, pady=10)

        # 快捷功能
        quick_btn_frame = ttk.LabelFrame(self.content, text="快捷功能", padding=20)
        quick_btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(quick_btn_frame, text="记录今日饮食", width=18).grid(row=0, column=0, padx=15, pady=5)
        ttk.Button(quick_btn_frame, text="记录今日运动", width=18).grid(row=0, column=1, padx=15, pady=5)
        ttk.Button(quick_btn_frame, text="记录今日心情", width=18).grid(row=0, column=2, padx=15, pady=5)