# dao/health_dao.py
from dao.base_dao import BaseDAO

class HealthDAO(BaseDAO):
    def __init__(self):
        # 指定存到 user_profile.json
        super().__init__("user_profile.json")

    def get_profile(self):
        """获取个人档案"""
        return self.load_all()

    def save_profile(self, profile_data):
        """保存个人档案"""
        self.save_all(profile_data)