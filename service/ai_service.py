# service/ai_service.py
import json
import os
import requests
from config import DATA_DIR

# ========== 豆包（火山引擎）配置 ==========
API_KEY = "your-api-key-here"
URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
MODEL = "doubao-1-5-pro-32k-250115"
# =========================================

def get_all_health_data():
    """读取所有本地健康数据"""
    data = {}

    # 基础档案
    profile_path = os.path.join(DATA_DIR, "user_profile.json")
    if os.path.exists(profile_path):
        with open(profile_path, 'r', encoding='utf-8') as f:
            data["profile"] = json.load(f)

    # 心情记录（最近10条，避免token爆炸）
    mood_path = os.path.join(DATA_DIR, "mood_records.json")
    if os.path.exists(mood_path):
        with open(mood_path, 'r', encoding='utf-8') as f:
            all_moods = json.load(f)
            data["mood_records"] = all_moods[-10:] if all_moods else []

    return data


def anonymize_data(raw_data):
    """脱敏处理"""
    data = raw_data.copy()

    if "profile" in data:
        profile = data["profile"].copy()
        profile["name"] = "用户"  # 匿名化昵称
        data["profile"] = profile

    if "mood_records" in data:
        records = []
        for r in data["mood_records"]:
            rec = r.copy()
            # 只保留日期（YYYY-MM-DD）
            if "timestamp" in rec:
                rec["timestamp"] = rec["timestamp"][:10]
            # 删除备注（可能含敏感词）
            rec.pop("note", None)
            records.append(rec)
        data["mood_records"] = records

    return data


def chat(prompt, system_prompt="你是人工智能助手"):
    """基础对话，不附带数据"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    data = {
        "model": MODEL,
        "messages": messages
    }

    resp = requests.post(URL, json=data, headers=headers, timeout=60)

    if resp.status_code == 200:
        return resp.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"API错误 {resp.status_code}: {resp.text}")


def get_health_summary():
    """获取健康数据摘要（供 AI 使用）"""
    from service.analytics_service import AnalyticsService
    analytics = AnalyticsService()
    summary = analytics.load_summary()
    if not summary:
        # 如果没有摘要，尝试生成一次
        summary = analytics.generate_summary()
        if summary:
            analytics.save_summary(summary)
    return summary

def chat_with_health_data(user_prompt):
    """使用摘要数据进行分析"""
    summary = get_health_summary()
    if not summary:
        return "暂无足够的健康数据，请先记录一些心情数据。"

    # 脱敏处理
    safe_summary = summary.copy()
    # 基础档案也可以加入
    import json, os
    profile_path = os.path.join(DATA_DIR, "user_profile.json")
    if os.path.exists(profile_path):
        with open(profile_path, 'r', encoding='utf-8') as f:
            profile = json.load(f)
            profile["name"] = "用户"
            safe_summary["profile"] = profile

    system_prompt = f"""你是一位专业的健康管理顾问。
以下是用户的健康数据摘要（已脱敏）：
{json.dumps(safe_summary, ensure_ascii=False, indent=2)}

请根据这些统计数据，针对用户的问题提供科学、个性化的建议。"""

    return chat(user_prompt, system_prompt)