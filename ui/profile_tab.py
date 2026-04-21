# ui/profile_tab.py
import tkinter as tk
from tkinter import ttk
from service.health_service import HealthService
from ui.widgets import ScrollableFrame

class ProfileTab:
    def __init__(self, notebook):
        self.tab = ScrollableFrame(notebook)
        notebook.add(self.tab, text="👤 健康档案")
        self.health_service = HealthService()
        self.content = ttk.Frame(self.tab.scrollable_frame, padding=30)
        self.content.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        profile = self.health_service.get_profile()
        if not profile:
            # 如果没有档案，显示提示
            ttk.Label(self.content, text="暂无档案信息，请先录入基础信息", font=("微软雅黑", 12)).pack()
            return

        cal_data = profile.get("calculated", {})
        gender_text = "男" if profile.get('gender') == 'male' else "女"
        bmi = cal_data.get('bmi', 0)
        bmi_tip = "偏瘦" if bmi < 18.5 else "正常" if 18.5 <= bmi < 24 else "超重" if 24 <= bmi < 28 else "肥胖"

        base_info_frame = ttk.LabelFrame(self.content, text="基础个人信息", padding=20)
        base_info_frame.pack(fill=tk.X, pady=10)
        base_grid = ttk.Frame(base_info_frame)
        base_grid.pack(fill=tk.X)
        ttk.Label(base_grid, text=f"昵称：{profile.get('name', '')}", font=("微软雅黑", 11)).grid(row=0, column=0, sticky=tk.W, pady=6)
        ttk.Label(base_grid, text=f"性别：{gender_text}", font=("微软雅黑", 11)).grid(row=0, column=1, sticky=tk.W, padx=80, pady=6)
        ttk.Label(base_grid, text=f"年龄：{profile.get('age', 0)} 岁", font=("微软雅黑", 11)).grid(row=1, column=0, sticky=tk.W, pady=6)
        ttk.Label(base_grid, text=f"身高：{profile.get('height_cm', 0)} cm", font=("微软雅黑", 11)).grid(row=1, column=1, sticky=tk.W, padx=80, pady=6)
        ttk.Label(base_grid, text=f"当前体重：{profile.get('weight_kg', 0)} kg", font=("微软雅黑", 11)).grid(row=2, column=0, sticky=tk.W, pady=6)

        cal_info_frame = ttk.LabelFrame(self.content, text="核心健康指标", padding=20)
        cal_info_frame.pack(fill=tk.X, pady=10)
        cal_grid = ttk.Frame(cal_info_frame)
        cal_grid.pack(fill=tk.X)
        ttk.Label(cal_grid, text=f"BMI身体质量指数：{bmi} | 当前状态：{bmi_tip}", font=("微软雅黑", 11)).grid(row=0, column=0, sticky=tk.W, pady=6)
        ttk.Label(cal_grid, text=f"基础代谢率(BMR)：{cal_data.get('bmr', 0)} 大卡/天", font=("微软雅黑", 11)).grid(row=1, column=0, sticky=tk.W, pady=6)
        ttk.Label(cal_grid, text=f"每日推荐摄入热量：{cal_data.get('recommended_calories', 0)} 大卡", font=("微软雅黑", 11)).grid(row=2, column=0, sticky=tk.W, pady=6)

        if profile.get("goal"):
            goal_frame = ttk.LabelFrame(self.content, text="我的健康目标", padding=20)
            goal_frame.pack(fill=tk.X, pady=10)
            ttk.Label(goal_frame, text=profile['goal'], font=("微软雅黑", 12)).pack(anchor=tk.W)