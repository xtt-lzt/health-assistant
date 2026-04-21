# config.py
import os
import sys

# ========== 豆包（火山引擎）配置 ==========
API_KEY = "your-api-key-here"
URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
MODEL = "doubao-1-5-pro-32k-250115"

# 判断是否为 PyInstaller 打包后的可执行文件
if getattr(sys, 'frozen', False):
    # 打包后，exe 所在目录为可写目录
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # 开发环境，使用脚本所在目录
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

VITAL_SIGNS_RANGE = {
    "weight": (30, 200),
    "height": (100, 220),
    "bmi": (18.5, 23.9)
}