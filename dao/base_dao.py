# dao/base_dao.py
import json
import os
from config import DATA_DIR

class BaseDAO:
    def __init__(self, filename):
        """
        初始化 DAO
        :param filename: 存储的文件名，例如 'user_profile.json'
        """
        self.file_path = os.path.join(DATA_DIR, filename)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """如果文件不存在，创建一个空的"""
        if not os.path.exists(self.file_path):
            self.save_all({}) # 档案用字典，记录用列表，这里先默认字典

    def load_all(self):
        """读取所有数据"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def save_all(self, data):
        """保存所有数据"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)