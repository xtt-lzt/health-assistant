# ui/gui_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from service.health_service import HealthService
from service.data_center import DataCenter

# -------------------------- 通用工具：可滚动容器 --------------------------
class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_windows)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux_up)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux_down)

    def _on_mousewheel_windows(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    def _on_mousewheel_linux_up(self, event):
        self.canvas.yview_scroll(-1, "units")
    def _on_mousewheel_linux_down(self, event):
        self.canvas.yview_scroll(1, "units")

# -------------------------- 主GUI应用 --------------------------
class HealthGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("健康管理小助手")
        self.root.geometry("750x600")
        self.root.minsize(600, 450)
        self.root.resizable(True, True)
        root.option_add("*Font", "微软雅黑 10")

        # 初始化业务层
        self.health_service = HealthService()
        self.gender_var = tk.StringVar(value="male")

        # 注册数据更新回调，基础信息修改后自动刷新界面
        DataCenter.register_update_callback(self.refresh_all_page)

        # 启动逻辑
        if not self.health_service.is_profile_exists():
            self.create_profile_input_page()
        else:
            self.create_main_app_page()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def refresh_all_page(self):
        """基础信息修改后，自动刷新所有页面数据"""
        if hasattr(self, "notebook"):
            self.create_main_app_page()

    # -------------------------- 页面1：基础信息录入页面 --------------------------
    def create_profile_input_page(self):
        self.clear_window()
        self.root.title("基础信息录入 - 健康管理小助手")

        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, pady=15)
        ttk.Label(title_frame, text="欢迎使用健康管理小助手", font=("微软雅黑", 18, "bold")).pack()
        ttk.Label(title_frame, text="首次使用，请完成基础健康信息录入（带*为必填项，所有数据为运动/饮食计算提供基准）", font=("微软雅黑", 10), foreground="gray").pack(pady=5)

        scroll_container = ScrollableFrame(self.root)
        scroll_container.pack(fill=tk.BOTH, expand=True, padx=40)
        form_frame = ttk.Frame(scroll_container.scrollable_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # 表单字段
        ttk.Label(form_frame, text="* 昵称：", font=("微软雅黑", 11)).grid(row=0, column=0, sticky=tk.W, pady=8)
        self.name_entry = ttk.Entry(form_frame, width=35, font=("微软雅黑", 10))
        self.name_entry.grid(row=0, column=1, sticky=tk.W, pady=8, padx=10)

        ttk.Label(form_frame, text="* 性别：", font=("微软雅黑", 11)).grid(row=1, column=0, sticky=tk.W, pady=8)
        gender_frame = ttk.Frame(form_frame)
        gender_frame.grid(row=1, column=1, sticky=tk.W, pady=8, padx=10)
        ttk.Radiobutton(gender_frame, text="男", variable=self.gender_var, value="male").pack(side=tk.LEFT, padx=20)
        ttk.Radiobutton(gender_frame, text="女", variable=self.gender_var, value="female").pack(side=tk.LEFT, padx=20)

        ttk.Label(form_frame, text="* 年龄：", font=("微软雅黑", 11)).grid(row=2, column=0, sticky=tk.W, pady=8)
        self.age_entry = ttk.Entry(form_frame, width=35, font=("微软雅黑", 10))
        self.age_entry.grid(row=2, column=1, sticky=tk.W, pady=8, padx=10)

        ttk.Label(form_frame, text="* 身高(cm)：", font=("微软雅黑", 11)).grid(row=3, column=0, sticky=tk.W, pady=8)
        self.height_entry = ttk.Entry(form_frame, width=35, font=("微软雅黑", 10))
        self.height_entry.grid(row=3, column=1, sticky=tk.W, pady=8, padx=10)
        ttk.Label(form_frame, text="* 用于运动消耗精准计算", font=("微软雅黑", 9), foreground="gray").grid(row=3, column=2, sticky=tk.W)

        ttk.Label(form_frame, text="* 体重(kg)：", font=("微软雅黑", 11)).grid(row=4, column=0, sticky=tk.W, pady=8)
        self.weight_entry = ttk.Entry(form_frame, width=35, font=("微软雅黑", 10))
        self.weight_entry.grid(row=4, column=1, sticky=tk.W, pady=8, padx=10)
        ttk.Label(form_frame, text="* 用于运动消耗精准计算", font=("微软雅黑", 9), foreground="gray").grid(row=4, column=2, sticky=tk.W)

        ttk.Label(form_frame, text="健康目标：", font=("微软雅黑", 11)).grid(row=5, column=0, sticky=tk.W, pady=8)
        self.goal_entry = ttk.Entry(form_frame, width=35, font=("微软雅黑", 10))
        self.goal_entry.grid(row=5, column=1, sticky=tk.W, pady=8, padx=10)
        ttk.Label(form_frame, text="示例：3个月减重到55kg、每周运动3次、控糖饮食", font=("微软雅黑", 9), foreground="gray").grid(row=6, column=1, sticky=tk.W, padx=10)

        # 底部按钮
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill=tk.X, pady=20)
        cancel_btn = ttk.Button(btn_frame, text="关闭程序", command=self.root.quit, width=15)
        cancel_btn.pack(side=tk.RIGHT, padx=50)
        submit_btn = ttk.Button(btn_frame, text="确认提交", command=self.submit_profile, width=15)
        submit_btn.pack(side=tk.RIGHT, padx=10)

    def submit_profile(self):
        try:
            name = self.name_entry.get().strip()
            gender = self.gender_var.get()
            age = int(self.age_entry.get().strip())
            height = float(self.height_entry.get().strip())
            weight = float(self.weight_entry.get().strip())
            goal = self.goal_entry.get().strip()

            if not name:
                raise ValueError("昵称不能为空，请填写")
            if age <= 0:
                raise ValueError("年龄必须大于0，请重新输入")

            self.health_service.create_profile(name, gender, age, height, weight, goal)
            messagebox.showinfo("提交成功", "基础信息录入完成！数据已同步至所有功能模块")
            self.create_main_app_page()

        except ValueError as e:
            messagebox.showerror("输入错误", str(e))
        except Exception as e:
            messagebox.showerror("系统错误", f"录入失败：{str(e)}")

    # -------------------------- 页面2：主应用界面（带耦合核心区） --------------------------
    def create_main_app_page(self):
        self.clear_window()
        self.root.title("健康管理小助手")
        user_name = DataCenter.get("user_name", "用户")

        # 顶部欢迎栏
        top_bar = ttk.Frame(self.root)
        top_bar.pack(fill=tk.X, pady=10, padx=20)
        ttk.Label(top_bar, text=f"👋 欢迎回来，{user_name}！", font=("微软雅黑", 18, "bold")).pack(side=tk.LEFT)
        # 顶部快捷操作：修改档案
        edit_btn = ttk.Button(top_bar, text="修改基础档案", command=self.create_profile_input_page)
        edit_btn.pack(side=tk.RIGHT)

        # 核心：标签页容器
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # -------------------------- 标签页1：首页总览看板【核心耦合展示区】 --------------------------
        # 所有模块的联动数据都在这里展示，是整个工具的耦合核心
        overview_tab = ScrollableFrame(self.notebook)
        self.notebook.add(overview_tab, text="📊 总览看板")
        overview_content = ttk.Frame(overview_tab.scrollable_frame, padding=20)
        overview_content.pack(fill=tk.BOTH, expand=True)

        # 1. 核心基准数据卡片（来自基础信息模块，所有业务模块的计算基准）
        base_card = ttk.LabelFrame(overview_content, text="核心健康基准（自动同步至所有功能）", padding=20)
        base_card.pack(fill=tk.X, pady=10)
        base_grid = ttk.Frame(base_card)
        base_grid.pack(fill=tk.X)

        # 从DataCenter取基础数据，不用直接调用HealthService
        bmr = DataCenter.get("bmr", 0)
        recommend_cal = DataCenter.get("recommended_calories", 0)
        weight = DataCenter.get("weight_kg", 0)
        health_goal = DataCenter.get("health_goal", "暂无目标")

        ttk.Label(base_grid, text=f"当前体重：{weight} kg", font=("微软雅黑", 11, "bold")).grid(row=0, column=0, sticky=tk.W, padx=20)
        ttk.Label(base_grid, text=f"基础代谢(BMR)：{bmr} 大卡/天", font=("微软雅黑", 11, "bold")).grid(row=0, column=1, sticky=tk.W, padx=40)
        ttk.Label(base_grid, text=f"每日推荐摄入：{recommend_cal} 大卡", font=("微软雅黑", 11, "bold")).grid(row=0, column=2, sticky=tk.W, padx=40)

        # 2. 健康目标展示（基础信息 ↔ 所有业务模块的联动锚点）
        goal_card = ttk.LabelFrame(overview_content, text="我的健康目标", padding=20)
        goal_card.pack(fill=tk.X, pady=10)
        ttk.Label(goal_card, text=health_goal, font=("微软雅黑", 12)).pack(anchor=tk.W)

        # 3. 【耦合预留区】今日数据汇总（运动+饮食+心情模块的联动数据展示）
        today_card = ttk.LabelFrame(overview_content, text="今日数据汇总", padding=20)
        today_card.pack(fill=tk.X, pady=10)
        today_grid = ttk.Frame(today_card)
        today_grid.pack(fill=tk.X)

        # 饮食模块耦合预留位：直接从DataCenter取数据，不用管底层实现
        self.today_intake = DataCenter.get("today_calorie_intake", 0)
        # 运动模块耦合预留位：直接从DataCenter取数据
        self.today_consume = DataCenter.get("today_calorie_consume", 0)
        # 心情模块耦合预留位：直接从DataCenter取数据
        self.today_mood = DataCenter.get("today_latest_mood", "暂无记录")

        ttk.Label(today_grid, text=f"今日已摄入：{self.today_intake} 大卡", font=("微软雅黑", 11)).grid(row=0, column=0, sticky=tk.W, padx=20, pady=10)
        ttk.Label(today_grid, text=f"今日已消耗：{self.today_consume} 大卡", font=("微软雅黑", 11)).grid(row=0, column=1, sticky=tk.W, padx=40, pady=10)
        ttk.Label(today_grid, text=f"今日热量缺口：{self.today_intake - self.today_consume} 大卡", font=("微软雅黑", 11)).grid(row=0, column=2, sticky=tk.W, padx=40, pady=10)
        ttk.Label(today_grid, text=f"最新心情状态：{self.today_mood}", font=("微软雅黑", 11)).grid(row=1, column=0, sticky=tk.W, padx=20, pady=10)

        # 4. 快捷功能入口（模块间跳转耦合）
        quick_btn_frame = ttk.LabelFrame(overview_content, text="快捷功能", padding=20)
        quick_btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(quick_btn_frame, text="记录今日饮食", width=18, command=lambda: self.notebook.select(3)).grid(row=0, column=0, padx=15, pady=5)
        ttk.Button(quick_btn_frame, text="记录今日运动", width=18, command=lambda: self.notebook.select(2)).grid(row=0, column=1, padx=15, pady=5)
        ttk.Button(quick_btn_frame, text="记录今日心情", width=18, command=lambda: self.notebook.select(1)).grid(row=0, column=2, padx=15, pady=5)

        # -------------------------- 标签页2：心情记录模块（预留耦合口子） --------------------------
        mood_tab = ScrollableFrame(self.notebook)
        self.notebook.add(mood_tab, text="😶 心情记录")
        mood_content = ttk.Frame(mood_tab.scrollable_frame, padding=20)
        mood_content.pack(fill=tk.BOTH, expand=True)
        ttk.Label(mood_content, text="心情记录模块", font=("微软雅黑", 16, "bold")).pack(anchor=tk.W, pady=10)
        ttk.Label(mood_content, text="✅ 已自动同步基础健康数据，可用于情绪-身体状态联动分析", foreground="green").pack(anchor=tk.W, pady=5)
        # 这里直接写你们的心情记录界面，基础数据直接从DataCenter.get()拿就行

        # -------------------------- 标签页3：运动记录模块（预留耦合口子） --------------------------
        exercise_tab = ScrollableFrame(self.notebook)
        self.notebook.add(exercise_tab, text="🏃 运动记录")
        exercise_content = ttk.Frame(exercise_tab.scrollable_frame, padding=20)
        exercise_content.pack(fill=tk.BOTH, expand=True)
        ttk.Label(exercise_content, text="运动记录模块", font=("微软雅黑", 16, "bold")).pack(anchor=tk.W, pady=10)
        ttk.Label(exercise_content, text=f"✅ 已自动同步你的体重：{weight} kg，将用于精准计算运动热量消耗", foreground="green").pack(anchor=tk.W, pady=5)
        # 这里直接写你们的运动记录界面，基础数据直接从DataCenter.get()拿就行

        # -------------------------- 标签页4：饮食记录模块（预留耦合口子） --------------------------
        nutrition_tab = ScrollableFrame(self.notebook)
        self.notebook.add(nutrition_tab, text="🍚 饮食记录")
        nutrition_content = ttk.Frame(nutrition_tab.scrollable_frame, padding=20)
        nutrition_content.pack(fill=tk.BOTH, expand=True)
        ttk.Label(nutrition_content, text="饮食记录模块", font=("微软雅黑", 16, "bold")).pack(anchor=tk.W, pady=10)
        ttk.Label(nutrition_content, text=f"✅ 已自动同步你的每日推荐摄入：{recommend_cal} 大卡，将用于热量摄入对比", foreground="green").pack(anchor=tk.W, pady=5)
        # 这里直接写你们的饮食记录界面，基础数据直接从DataCenter.get()拿就行

        # -------------------------- 标签页5：健康档案详情 --------------------------
        profile_tab = ScrollableFrame(self.notebook)
        self.notebook.add(profile_tab, text="👤 健康档案")
        profile_content = ttk.Frame(profile_tab.scrollable_frame, padding=30)
        profile_content.pack(fill=tk.BOTH, expand=True)

        profile = self.health_service.get_profile()
        cal_data = profile["calculated"]
        gender_text = "男" if profile['gender'] == 'male' else "女"
        bmi = cal_data['bmi']
        bmi_tip = "偏瘦" if bmi < 18.5 else "正常" if 18.5 <= bmi < 24 else "超重" if 24 <= bmi < 28 else "肥胖"

        base_info_frame = ttk.LabelFrame(profile_content, text="基础个人信息", padding=20)
        base_info_frame.pack(fill=tk.X, pady=10)
        base_grid = ttk.Frame(base_info_frame)
        base_grid.pack(fill=tk.X)
        ttk.Label(base_grid, text=f"昵称：{profile['name']}", font=("微软雅黑", 11)).grid(row=0, column=0, sticky=tk.W, pady=6)
        ttk.Label(base_grid, text=f"性别：{gender_text}", font=("微软雅黑", 11)).grid(row=0, column=1, sticky=tk.W, padx=80, pady=6)
        ttk.Label(base_grid, text=f"年龄：{profile['age']} 岁", font=("微软雅黑", 11)).grid(row=1, column=0, sticky=tk.W, pady=6)
        ttk.Label(base_grid, text=f"身高：{profile['height_cm']} cm", font=("微软雅黑", 11)).grid(row=1, column=1, sticky=tk.W, padx=80, pady=6)
        ttk.Label(base_grid, text=f"当前体重：{profile['weight_kg']} kg", font=("微软雅黑", 11)).grid(row=2, column=0, sticky=tk.W, pady=6)

        cal_info_frame = ttk.LabelFrame(profile_content, text="核心健康指标", padding=20)
        cal_info_frame.pack(fill=tk.X, pady=10)
        cal_grid = ttk.Frame(cal_info_frame)
        cal_grid.pack(fill=tk.X)
        ttk.Label(cal_grid, text=f"BMI身体质量指数：{bmi} | 当前状态：{bmi_tip}", font=("微软雅黑", 11)).grid(row=0, column=0, sticky=tk.W, pady=6)
        ttk.Label(cal_grid, text=f"基础代谢率(BMR)：{cal_data['bmr']} 大卡/天", font=("微软雅黑", 11)).grid(row=1, column=0, sticky=tk.W, pady=6)
        ttk.Label(cal_grid, text=f"每日推荐摄入热量：{cal_data['recommended_calories']} 大卡", font=("微软雅黑", 11)).grid(row=2, column=0, sticky=tk.W, pady=6)

        if profile.get("goal"):
            goal_frame = ttk.LabelFrame(profile_content, text="我的健康目标", padding=20)
            goal_frame.pack(fill=tk.X, pady=10)
            ttk.Label(goal_frame, text=profile['goal'], font=("微软雅黑", 12)).pack(anchor=tk.W)

        # 底部关闭按钮
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, pady=15)
        close_btn = ttk.Button(bottom_frame, text="关闭程序", command=self.root.quit, width=15)
        close_btn.pack(side=tk.RIGHT, padx=30)