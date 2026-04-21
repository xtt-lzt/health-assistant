# ui/analytics_tab.py
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from service.analytics_service import AnalyticsService

# ========== 配置 matplotlib 中文显示 ==========
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']  # 微软雅黑/黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示异常
# ============================================

class AnalyticsTab:
    def __init__(self, notebook):
        self.tab = ttk.Frame(notebook)
        notebook.add(self.tab, text="📈 数据分析")
        self.service = AnalyticsService()

        self.create_widgets()
        self.plot_default()

    def create_widgets(self):
        # 控制栏
        control_frame = ttk.Frame(self.tab)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        # 在 create_widgets 的 control_frame 中添加
        self.view_mode = tk.StringVar(value="daily")
        ttk.Radiobutton(control_frame, text="日趋势", variable=self.view_mode, value="daily", command=self.update_plot).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(control_frame, text="日内波动(近7天)", variable=self.view_mode, value="intraday", command=self.update_plot).pack(side=tk.LEFT, padx=5)

        ttk.Label(control_frame, text="选择指标：").pack(side=tk.LEFT)
        self.field_var = tk.StringVar(value="valence")
        fields = ["valence", "stress", "sleep_hours", "anxiety", "motivation", "focus"]
        self.combo = ttk.Combobox(control_frame, textvariable=self.field_var, values=fields, state="readonly", width=15)
        self.combo.pack(side=tk.LEFT, padx=5)
        self.combo.bind("<<ComboboxSelected>>", lambda e: self.update_plot())

        ttk.Button(control_frame, text="刷新", command=self.update_plot).pack(side=tk.LEFT, padx=5)

        # 图表容器
        self.figure = Figure(figsize=(9, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.tab)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 摘要信息栏
        self.summary_text = tk.Text(self.tab, height=6, state=tk.DISABLED, font=("微软雅黑", 9))
        self.summary_text.pack(fill=tk.X, padx=10, pady=5)

        self.update_summary_text()

    def plot_default(self):
        self.update_plot()

    def update_plot(self):
        field = self.field_var.get()
        mode = self.view_mode.get()
        
        if mode == "daily":
            series = self.service.get_time_series([field], aggregate_daily=True)
            x_label = "日期"
            x_data_key = "dates"
        else:  # intraday
            series = self.service.get_intraday_series([field], days=7)
            x_label = "时间"
            x_data_key = "timestamps"
        
        if not series or not series.get(x_data_key):
            self.ax.clear()
            self.ax.text(0.5, 0.5, "暂无数据", ha='center', va='center', transform=self.ax.transAxes, fontsize=14)
            self.canvas.draw()
            return

        x_data = series[x_data_key]
        y_data = series[field]

        self.ax.clear()
        self.ax.plot(x_data, y_data, marker='o', linestyle='-', linewidth=2, markersize=5, color='#2E86AB')
        self.ax.set_title(f"{self.get_field_label(field)} {'日趋势' if mode=='daily' else '日内波动(近7天)'}", fontsize=14)
        self.ax.set_xlabel(x_label, fontsize=11)
        self.ax.set_ylabel(self.get_field_label(field), fontsize=11)

        # 智能刻度处理
        num_points = len(x_data)
        if num_points > 20:
            step = num_points // 15 + 1
            tick_positions = list(range(0, num_points, step))
            tick_labels = [x_data[i] for i in tick_positions]
        else:
            tick_positions = list(range(num_points))
            tick_labels = x_data

        self.ax.set_xticks(tick_positions)
        self.ax.set_xticklabels(tick_labels, rotation=45, ha='right', fontsize=8)
        self.ax.grid(True, linestyle='--', alpha=0.5)
        self.figure.tight_layout()
        self.canvas.draw()

        # 日内波动时摘要信息可显示统计范围
        if mode == "daily":
            self.update_summary_text()
        else:
            self.show_intraday_info(series)

    def get_field_label(self, field):
        labels = {
            "valence": "愉悦度",
            "stress": "压力指数",
            "sleep_hours": "睡眠时长(小时)",
            "anxiety": "焦虑程度",
            "motivation": "做事动力",
            "focus": "专注度"
        }
        return labels.get(field, field)

    def update_summary_text(self):
        summary = self.service.load_summary()
        if not summary:
            text = "暂无摘要数据"
        else:
            avg = summary.get("averages", {})
            trends = summary.get("trends", {})
            date_range = summary.get('date_range', ['-', '-'])
            text = f"📊 总记录数：{summary.get('total_records', 0)}  |  日期范围：{date_range[0]} 至 {date_range[1]}\n"
            text += f"😊 平均愉悦度：{avg.get('valence', '-')} (趋势：{trends.get('valence', '-')})  "
            text += f"😫 平均压力：{avg.get('stress', '-')} (趋势：{trends.get('stress', '-')})\n"
            text += f"💤 平均睡眠：{avg.get('sleep_hours', '-')}小时  "
            text += f"🎯 平均专注度：{avg.get('focus', '-')}"
        self.summary_text.configure(state=tk.NORMAL)
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert("1.0", text)
        self.summary_text.configure(state=tk.DISABLED)


    def show_intraday_info(self, series):
        info = f"📊 展示最近7天的记录，共 {len(series['timestamps'])} 个数据点。"
        self.summary_text.configure(state=tk.NORMAL)
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert("1.0", info)
        self.summary_text.configure(state=tk.DISABLED)