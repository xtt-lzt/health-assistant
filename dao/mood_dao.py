# dao/mood_dao.py
import json
import os
from config import DATA_DIR

class MoodDAO:
    def __init__(self):
        self.file_path = os.path.join(DATA_DIR, "mood_records.json")
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            self.save_all([])

    def load_all(self):
        """返回所有记录列表（按时间倒序）"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return sorted(data, key=lambda x: x.get("timestamp", ""), reverse=True)
                return []
        except (json.JSONDecodeError, IOError):
            return []

    def save_all(self, records):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)

    def add_record(self, record):
        records = self.load_all()
        records.append(record)
        self.save_all(records)
        return record

    def get_today_records(self):
        """获取今日所有记录（用于计算摘要）"""
        from datetime import datetime
        today_str = datetime.now().strftime("%Y-%m-%d")
        all_records = self.load_all()
        return [r for r in all_records if r.get("timestamp", "").startswith(today_str)]

    def get_latest_record(self):
        records = self.load_all()
        return records[0] if records else None