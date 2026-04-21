# service/mood_service.py
from dao.mood_dao import MoodDAO
from datetime import datetime
from service.analytics_service import AnalyticsService

class MoodService:
    def __init__(self):
        self.dao = MoodDAO()
        self.analytics = AnalyticsService()

    def add_record(self, data):
        now = datetime.now()
        record = {
            "id": now.strftime("%Y%m%d_%H%M%S"),
            "timestamp": now.isoformat(),
            **data
        }
        self.dao.add_record(record)

        # 自动更新摘要
        summary = self.analytics.generate_summary()
        if summary:
            self.analytics.save_summary(summary)

        return record

    def get_all_records(self):
        return self.dao.load_all()

    def get_today_records(self):
        return self.dao.get_today_records()

    def get_latest_record(self):
        return self.dao.get_latest_record()