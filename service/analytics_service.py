# service/analytics_service.py
import json
import os
from datetime import datetime, timedelta
from config import DATA_DIR

class AnalyticsService:
    def __init__(self):
        self.summary_file = os.path.join(DATA_DIR, "mood_summary.json")
        self.mood_file = os.path.join(DATA_DIR, "mood_records.json")

    def load_all_records(self):
        """加载所有心情记录"""
        if not os.path.exists(self.mood_file):
            return []
        try:
            with open(self.mood_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []

    def generate_summary(self, records=None):
        """生成统计摘要（与之前相同）"""
        if records is None:
            records = self.load_all_records()
        if not records:
            return None

        sorted_records = sorted(records, key=lambda x: x.get("timestamp", ""))

        numeric_fields = [
            "valence", "arousal", "stress", "anxiety",
            "motivation", "focus", "procrastination",
            "social_desire", "social_fatigue", "social_sensitivity",
            "sleep_hours", "sleep_quality", "appetite",
            "confidence", "self_criticism", "optimism", "workload"
        ]

        sums = {field: 0.0 for field in numeric_fields}
        counts = {field: 0 for field in numeric_fields}
        for r in sorted_records:
            for field in numeric_fields:
                val = r.get(field)
                if val is not None:
                    try:
                        sums[field] += float(val)
                        counts[field] += 1
                    except:
                        pass

        averages = {}
        for field in numeric_fields:
            if counts[field] > 0:
                averages[field] = round(sums[field] / counts[field], 2)
            else:
                averages[field] = None

        trends = {}
        for field in numeric_fields:
            values = []
            for r in sorted_records:
                val = r.get(field)
                if val is not None:
                    try:
                        values.append(float(val))
                    except:
                        pass
            if len(values) >= 3:
                first_half = values[:len(values)//2]
                second_half = values[len(values)//2:]
                avg_first = sum(first_half) / len(first_half)
                avg_second = sum(second_half) / len(second_half)
                diff = avg_second - avg_first
                if diff > 0.5:
                    trends[field] = "上升"
                elif diff < -0.5:
                    trends[field] = "下降"
                else:
                    trends[field] = "平稳"
            else:
                trends[field] = "数据不足"

        date_range = [
            sorted_records[0]["timestamp"][:10],
            sorted_records[-1]["timestamp"][:10]
        ]

        latest = sorted_records[-1].copy()
        latest.pop("note", None)
        latest["timestamp"] = latest["timestamp"][:10]

        summary = {
            "last_updated": datetime.now().isoformat(),
            "total_records": len(records),
            "date_range": date_range,
            "averages": averages,
            "trends": trends,
            "latest": latest
        }
        return summary

    def save_summary(self, summary):
        with open(self.summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

    def load_summary(self):
        if not os.path.exists(self.summary_file):
            return None
        try:
            with open(self.summary_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None

    def get_time_series(self, fields=None, aggregate_daily=True):
        """
        获取时间序列数据。
        aggregate_daily=True 时，同一天多条记录取平均值。
        """
        records = self.load_all_records()
        if not records:
            return None

        sorted_records = sorted(records, key=lambda x: x.get("timestamp", ""))

        if fields is None:
            fields = ["valence", "stress", "sleep_hours"]

        if aggregate_daily:
            # 按天聚合
            daily_data = {}
            for r in sorted_records:
                date = r["timestamp"][:10]
                if date not in daily_data:
                    daily_data[date] = {field: [] for field in fields}
                for field in fields:
                    val = r.get(field)
                    if val is not None:
                        try:
                            daily_data[date][field].append(float(val))
                        except:
                            pass

            dates = sorted(daily_data.keys())
            series = {"dates": dates}
            for field in fields:
                values = []
                for date in dates:
                    vals = daily_data[date][field]
                    if vals:
                        values.append(round(sum(vals) / len(vals), 2))
                    else:
                        values.append(None)
                series[field] = values
            return series
        else:
            # 不聚合，保留每个记录点
            dates = [r["timestamp"][:10] for r in sorted_records]
            series = {"dates": dates}
            for field in fields:
                values = []
                for r in sorted_records:
                    val = r.get(field)
                    if val is not None:
                        try:
                            values.append(float(val))
                        except:
                            values.append(None)
                    else:
                        values.append(None)
                series[field] = values
            return series

    def get_intraday_series(self, fields=None, days=7):
        """
        获取最近 N 天的日内详细数据（不聚合），用于展示日内波动。
        """
        records = self.load_all_records()
        if not records:
            return None

        sorted_records = sorted(records, key=lambda x: x.get("timestamp", ""))

        if days:
            cutoff = (datetime.now() - timedelta(days=days)).isoformat()
            sorted_records = [r for r in sorted_records if r.get("timestamp", "") >= cutoff]

        if fields is None:
            fields = ["valence", "stress", "sleep_hours"]

        timestamps = []
        series = {field: [] for field in fields}

        for r in sorted_records:
            ts = r["timestamp"].replace("T", " ")[:16]  # 精确到分钟
            timestamps.append(ts)
            for field in fields:
                val = r.get(field)
                if val is not None:
                    try:
                        series[field].append(float(val))
                    except:
                        series[field].append(None)
                else:
                    series[field].append(None)

        return {"timestamps": timestamps, **series}