# ui/mood_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
from ui.widgets import ScrollableFrame
from service.mood_service import MoodService

class MoodTab:
    def __init__(self, notebook):
        self.tab = ScrollableFrame(notebook)
        notebook.add(self.tab, text="😶 心情记录")
        self.service = MoodService()

        self.content = ttk.Frame(self.tab.scrollable_frame, padding=20)
        self.content.pack(fill=tk.BOTH, expand=True)

        self.create_input_form()
        self.create_history_section()

        # 延迟同步，避免在界面构建时触发回调
        # self.tab.after_idle(self.service.sync_summary_to_datacenter)

    def create_input_form(self):
        form_frame = ttk.LabelFrame(self.content, text="记录此刻状态", padding=15)
        form_frame.pack(fill=tk.X, pady=(0, 20))

        self.vars = {}
        row = 0

        # 1. 情绪核心
        ttk.Label(form_frame, text="情绪状态", font=("微软雅黑", 11, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(0,5))
        row += 1
        row = self._add_scale(form_frame, row, "valence", "愉悦度", 1, 10)
        row = self._add_scale(form_frame, row, "arousal", "唤醒度/精力", 1, 10)

        # 2. 压力与焦虑
        ttk.Label(form_frame, text="压力与焦虑", font=("微软雅黑", 11, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(10,5))
        row += 1
        row = self._add_scale(form_frame, row, "stress", "压力指数", 1, 10)
        row = self._add_scale(form_frame, row, "anxiety", "焦虑程度", 1, 10)

        # 3. 动力与执行力
        ttk.Label(form_frame, text="动力与执行力", font=("微软雅黑", 11, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(10,5))
        row += 1
        row = self._add_scale(form_frame, row, "motivation", "做事动力", 1, 10)
        row = self._add_scale(form_frame, row, "focus", "专注度", 1, 10)
        row = self._add_scale(form_frame, row, "procrastination", "拖延程度", 1, 10)

        # 4. 社交能量
        ttk.Label(form_frame, text="社交能量", font=("微软雅黑", 11, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(10,5))
        row += 1
        row = self._add_scale(form_frame, row, "social_desire", "想社交程度", 1, 10)
        row = self._add_scale(form_frame, row, "social_fatigue", "社交疲惫感", 1, 10)
        row = self._add_scale(form_frame, row, "social_sensitivity", "人际敏感程度", 1, 10)

        # 5. 身体状态
        ttk.Label(form_frame, text="身体状态", font=("微软雅黑", 11, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(10,5))
        row += 1
        row = self._add_entry(form_frame, row, "sleep_hours", "睡眠时长(小时)")
        row = self._add_scale(form_frame, row, "sleep_quality", "睡眠质量", 1, 10)
        row = self._add_scale(form_frame, row, "appetite", "食欲", 1, 10)

        ttk.Label(form_frame, text="身体不适（逗号分隔）:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.vars["physical_symptoms"] = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.vars["physical_symptoms"], width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(form_frame, text="运动情况:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.vars["exercise"] = tk.StringVar(value="无")  # 默认值
        ttk.Combobox(form_frame, textvariable=self.vars["exercise"],
                     values=["无", "轻度运动", "中度运动", "剧烈运动"], width=15).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        # 6. 认知状态
        ttk.Label(form_frame, text="认知状态", font=("微软雅黑", 11, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(10,5))
        row += 1
        row = self._add_scale(form_frame, row, "confidence", "自信水平", 1, 10)
        row = self._add_scale(form_frame, row, "self_criticism", "自我否定程度", 1, 10)
        row = self._add_scale(form_frame, row, "optimism", "乐观倾向", 1, 10)

        # 7. 环境因素
        ttk.Label(form_frame, text="环境因素", font=("微软雅黑", 11, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(10,5))
        row += 1
        ttk.Label(form_frame, text="天气:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.vars["weather"] = tk.StringVar(value="晴")  # 默认值
        ttk.Combobox(form_frame, textvariable=self.vars["weather"],
                     values=["晴", "多云", "阴", "雨", "雪"], width=10).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        row = self._add_scale(form_frame, row, "workload", "工作/学习负荷", 1, 10)

        ttk.Label(form_frame, text="摄入咖啡因:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.vars["caffeine"] = tk.BooleanVar(value=False)
        ttk.Checkbutton(form_frame, variable=self.vars["caffeine"]).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(form_frame, text="饮酒:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.vars["alcohol"] = tk.BooleanVar(value=False)
        ttk.Checkbutton(form_frame, variable=self.vars["alcohol"]).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(form_frame, text="熬夜:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.vars["stay_up"] = tk.BooleanVar(value=False)
        ttk.Checkbutton(form_frame, variable=self.vars["stay_up"]).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        # 备注
        ttk.Label(form_frame, text="备注:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.vars["note"] = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.vars["note"], width=30).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        # 保存按钮
        btn_frame = ttk.Frame(self.content)
        btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(btn_frame, text="保存记录", command=self.save_record, width=15).pack()

    def _add_scale(self, parent, row, key, label, min_val, max_val):
        ttk.Label(parent, text=f"{label} ({min_val}-{max_val}):").grid(row=row, column=0, sticky=tk.W, pady=5)
        var = tk.IntVar(value=5)  # 默认中间值
        self.vars[key] = var
        scale = ttk.Scale(parent, from_=min_val, to=max_val, orient=tk.HORIZONTAL,
                          variable=var, length=200)
        scale.grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Label(parent, textvariable=var, width=3).grid(row=row, column=2, padx=5)
        return row + 1

    def _add_entry(self, parent, row, key, label):
        ttk.Label(parent, text=f"{label}:").grid(row=row, column=0, sticky=tk.W, pady=5)
        var = tk.StringVar(value="")  # 默认为空，后续处理
        self.vars[key] = var
        ttk.Entry(parent, textvariable=var, width=20).grid(row=row, column=1, sticky=tk.W, pady=5)
        return row + 1

    def create_history_section(self):
        hist_frame = ttk.LabelFrame(self.content, text="最近记录", padding=10)
        hist_frame.pack(fill=tk.BOTH, expand=True)

        self.history_tree = ttk.Treeview(hist_frame, columns=("time", "valence", "stress", "note"), show="headings", height=5)
        self.history_tree.heading("time", text="时间")
        self.history_tree.heading("valence", text="愉悦度")
        self.history_tree.heading("stress", text="压力")
        self.history_tree.heading("note", text="备注")
        self.history_tree.column("time", width=150)
        self.history_tree.column("valence", width=80)
        self.history_tree.column("stress", width=80)
        self.history_tree.column("note", width=200)
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(hist_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        self.refresh_history()

    def refresh_history(self):
        """刷新历史记录列表，增加异常处理以防组件无效"""
        try:
            # 检查 Treeview 是否仍然有效
            if not self.history_tree.winfo_exists():
                return
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)
            records = self.service.get_all_records()[:10]
            for r in records:
                time_str = r["timestamp"][5:16].replace("T", " ")
                self.history_tree.insert("", tk.END, values=(
                    time_str,
                    r.get("valence", "-"),
                    r.get("stress", "-"),
                    r.get("note", "")
                ))
        except tk.TclError:
            # 如果组件已被销毁，忽略错误
            pass

    def save_record(self):
        """收集表单数据并保存，缺失字段自动填充默认值"""
        try:
            data = {}
            # 1. 所有评分项默认值为5（中间值）
            for key, var in self.vars.items():
                if isinstance(var, tk.IntVar):
                    data[key] = var.get()
                elif isinstance(var, tk.StringVar):
                    val = var.get().strip()
                    if key == "sleep_hours":
                        # 睡眠时长：若未填则默认为8小时
                        try:
                            data[key] = float(val) if val else 8.0
                        except ValueError:
                            data[key] = 8.0
                    elif key == "physical_symptoms":
                        # 身体不适：若为空则设为空列表
                        data[key] = [s.strip() for s in val.split(",") if s.strip()]
                    elif key == "exercise":
                        # 运动情况：若未选则默认为"无"
                        data[key] = val if val else "无"
                    elif key == "weather":
                        # 天气：若未选则默认为"晴"
                        data[key] = val if val else "晴"
                    elif key == "note":
                        data[key] = val
                    else:
                        data[key] = val if val else ""
                elif isinstance(var, tk.BooleanVar):
                    data[key] = var.get()

            # 确保关键字段存在（理论上都会有，但加个安全兜底）
            if "valence" not in data:
                data["valence"] = 5
            if "arousal" not in data:
                data["arousal"] = 5

            # 保存记录
            self.service.add_record(data)
            messagebox.showinfo("成功", "心情记录已保存")
            # 刷新历史列表
            self.refresh_history()
        except Exception as e:
            messagebox.showerror("错误", f"保存失败：{str(e)}")