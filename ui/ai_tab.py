# ui/ai_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from service.ai_service import chat, chat_with_health_data

class AITab:
    def __init__(self, notebook):
        self.tab = ttk.Frame(notebook)
        notebook.add(self.tab, text="🤖 AI 分析")
        self.create_widgets()

    def create_widgets(self):
        # 使用 grid 布局，确保输入框可见
        self.tab.grid_rowconfigure(0, weight=1)  # 聊天区可扩展
        self.tab.grid_rowconfigure(1, weight=0)  # 输入区固定高度
        self.tab.grid_columnconfigure(0, weight=1)

        # 聊天显示区域（可滚动）
        chat_frame = ttk.LabelFrame(self.tab, text="AI 健康助手", padding=10)
        chat_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))

        self.chat_text = tk.Text(
            chat_frame,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=("微软雅黑", 10),
            bg="#f5f5f5",
            fg="#333333",
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        scrollbar = ttk.Scrollbar(chat_frame, command=self.chat_text.yview)
        self.chat_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 滚轮绑定
        self.chat_text.bind("<MouseWheel>", self._on_mousewheel)
        self.chat_text.bind("<Button-4>", self._on_mousewheel_linux)
        self.chat_text.bind("<Button-5>", self._on_mousewheel_linux)

        self.chat_text.tag_configure("user", foreground="#0066cc", font=("微软雅黑", 10, "bold"))
        self.chat_text.tag_configure("ai", foreground="#2d6a4f", font=("微软雅黑", 10, "bold"))
        self.chat_text.tag_configure("thinking", foreground="#888888", font=("微软雅黑", 10, "italic"))

        # 输入区域（固定在底部）
        input_frame = ttk.Frame(self.tab)
        input_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))

        self.input_text = tk.Text(
            input_frame,
            height=4,
            wrap=tk.WORD,
            font=("微软雅黑", 10),
            relief=tk.FLAT,
            padx=8,
            pady=8,
            borderwidth=1,
            highlightthickness=1,
            highlightcolor="#cccccc",
            highlightbackground="#dddddd"
        )
        self.input_text.pack(fill=tk.X, pady=(0, 5))
        self.input_text.bind("<Control-Return>", lambda e: self.send_message())

        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(fill=tk.X)
        ttk.Button(btn_frame, text="清空对话", command=self.clear_chat).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="📊 健康分析", command=self.health_analysis).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="发送", command=self.send_message).pack(side=tk.RIGHT)

        # 欢迎语
        self.append_to_chat("AI", "你好！我是你的健康助手，有什么可以帮你的？")

    def _on_mousewheel(self, event):
        self.chat_text.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_linux(self, event):
        if event.num == 4:
            self.chat_text.yview_scroll(-1, "units")
        elif event.num == 5:
            self.chat_text.yview_scroll(1, "units")

    def send_message(self):
        prompt = self.input_text.get("1.0", tk.END).strip()
        if not prompt:
            return

        self.append_to_chat("你", prompt)
        self.input_text.delete("1.0", tk.END)

        self.thinking_id = self.append_thinking()
        self.disable_input(True)

        thread = threading.Thread(target=self._call_ai, args=(prompt,), daemon=True)
        thread.start()

    def health_analysis(self):
        prompt = self.input_text.get("1.0", tk.END).strip()
        if not prompt:
            prompt = "请根据我的健康数据，给我一份综合分析和建议"

        self.append_to_chat("你", prompt)
        self.input_text.delete("1.0", tk.END)

        self.thinking_id = self.append_thinking()
        self.disable_input(True)

        thread = threading.Thread(target=self._call_ai_with_data, args=(prompt,), daemon=True)
        thread.start()

    def _call_ai(self, prompt):
        try:
            response = chat(prompt, system_prompt="你是人工智能助手")
        except Exception as e:
            response = f"AI 调用失败：{str(e)}"
        self.tab.after(0, self._on_ai_response, response)

    def _call_ai_with_data(self, prompt):
        try:
            response = chat_with_health_data(prompt)
        except Exception as e:
            response = f"AI 调用失败：{str(e)}"
        self.tab.after(0, self._on_ai_response, response)

    def _on_ai_response(self, response):
        self.remove_thinking(self.thinking_id)
        self.append_to_chat("AI", response)
        self.disable_input(False)
        self.input_text.focus_set()

    def append_to_chat(self, sender, message):
        self.chat_text.configure(state=tk.NORMAL)
        if sender == "你":
            self.chat_text.insert(tk.END, f"\n【{sender}】\n", "user")
        elif sender == "AI":
            self.chat_text.insert(tk.END, f"\n【{sender}】\n", "ai")
        else:
            self.chat_text.insert(tk.END, f"\n【{sender}】\n", "system")
        self.chat_text.insert(tk.END, f"{message}\n")
        self.chat_text.see(tk.END)
        self.chat_text.configure(state=tk.DISABLED)

    def append_thinking(self):
        self.chat_text.configure(state=tk.NORMAL)
        start_pos = self.chat_text.index(tk.END)
        self.chat_text.insert(tk.END, "\n【AI】\n", "ai")
        self.chat_text.insert(tk.END, "🤔 思考中...\n", "thinking")
        self.chat_text.see(tk.END)
        self.chat_text.configure(state=tk.DISABLED)
        return start_pos

    def remove_thinking(self, pos):
        self.chat_text.configure(state=tk.NORMAL)
        try:
            end = self.chat_text.index(f"{pos} + 3 lines")
            self.chat_text.delete(pos, end)
        except:
            pass
        self.chat_text.configure(state=tk.DISABLED)

    def disable_input(self, disabled):
        state = tk.DISABLED if disabled else tk.NORMAL
        self.input_text.configure(state=state)
        for child in self.tab.winfo_children():
            if isinstance(child, ttk.Button):
                child.configure(state=state)

    def clear_chat(self):
        self.chat_text.configure(state=tk.NORMAL)
        self.chat_text.delete("1.0", tk.END)
        self.chat_text.configure(state=tk.DISABLED)
        self.append_to_chat("AI", "对话已清空，有什么我可以帮你的？")