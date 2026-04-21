# ui/profile_input.py
import tkinter as tk
from tkinter import ttk, messagebox
from service.health_service import HealthService
from service.data_center import DataCenter
from ui.widgets import ScrollableFrame

class ProfileInputPage:
    def __init__(self, parent, on_success_callback):
        self.parent = parent
        self.on_success = on_success_callback
        self.health_service = HealthService()
        self.gender_var = tk.StringVar(value="male")
        self.create_widgets()

    def create_widgets(self):
        title_frame = ttk.Frame(self.parent)
        title_frame.pack(fill=tk.X, pady=15)
        ttk.Label(title_frame, text="欢迎使用健康管理小助手", font=("微软雅黑", 18, "bold")).pack()
        ttk.Label(title_frame, text="首次使用，请完成基础健康信息录入（带*为必填项）", font=("微软雅黑", 10), foreground="gray").pack(pady=5)

        scroll_container = ScrollableFrame(self.parent)
        scroll_container.pack(fill=tk.BOTH, expand=True, padx=40)
        form_frame = ttk.Frame(scroll_container.scrollable_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)

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

        ttk.Label(form_frame, text="* 体重(kg)：", font=("微软雅黑", 11)).grid(row=4, column=0, sticky=tk.W, pady=8)
        self.weight_entry = ttk.Entry(form_frame, width=35, font=("微软雅黑", 10))
        self.weight_entry.grid(row=4, column=1, sticky=tk.W, pady=8, padx=10)

        ttk.Label(form_frame, text="健康目标：", font=("微软雅黑", 11)).grid(row=5, column=0, sticky=tk.W, pady=8)
        self.goal_entry = ttk.Entry(form_frame, width=35, font=("微软雅黑", 10))
        self.goal_entry.grid(row=5, column=1, sticky=tk.W, pady=8, padx=10)
        ttk.Label(form_frame, text="示例：3个月减重到55kg、每周运动3次", font=("微软雅黑", 9), foreground="gray").grid(row=6, column=1, sticky=tk.W, padx=10)

        btn_frame = ttk.Frame(self.parent)
        btn_frame.pack(fill=tk.X, pady=20)
        cancel_btn = ttk.Button(btn_frame, text="关闭程序", command=self.parent.quit, width=15)
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
            messagebox.showinfo("提交成功", "基础信息录入完成！")
            self.on_success()

        except ValueError as e:
            messagebox.showerror("输入错误", str(e))
        except Exception as e:
            messagebox.showerror("系统错误", f"录入失败：{str(e)}")