# service/health_service.py
from dao.health_dao import HealthDAO
from utils.calculator import calculate_bmi, calculate_bmr
from config import VITAL_SIGNS_RANGE
from service.data_center import DataCenter

class HealthService:
    def __init__(self):
        self.dao = HealthDAO()
        # 移除这行：self._sync_to_datacenter()

    def _sync_to_datacenter(self):
        print("HealthService._sync_to_datacenter 开始")
        profile = self.get_profile()
        print(f"获取到 profile: {profile}")
        if profile:
            print("调用 DataCenter.init_base_data")
            DataCenter.init_base_data(profile)
            print("DataCenter.init_base_data 完成")
        print("HealthService._sync_to_datacenter 结束")

    def is_profile_exists(self):
        profile = self.dao.get_profile()
        return bool(profile)

    def create_profile(self, name, gender, age, height_cm, weight_kg, goal=""):
        if not (VITAL_SIGNS_RANGE["height"][0] <= height_cm <= VITAL_SIGNS_RANGE["height"][1]):
            raise ValueError(f"身高输入异常，请输入 {VITAL_SIGNS_RANGE['height'][0]}-{VITAL_SIGNS_RANGE['height'][1]} 之间的数值")
        
        if not (VITAL_SIGNS_RANGE["weight"][0] <= weight_kg <= VITAL_SIGNS_RANGE["weight"][1]):
            raise ValueError(f"体重输入异常，请输入 {VITAL_SIGNS_RANGE['weight'][0]}-{VITAL_SIGNS_RANGE['weight'][1]} 之间的数值")

        bmi = calculate_bmi(height_cm, weight_kg)
        bmr = calculate_bmr(gender, age, height_cm, weight_kg)

        profile = {
            "name": name,
            "gender": gender,
            "age": age,
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "goal": goal,
            "calculated": {
                "bmi": bmi,
                "bmr": bmr,
                "recommended_calories": bmr * 1.55
            }
        }

        self.dao.save_profile(profile)
        # 保存后同步到DataCenter，触发界面更新
        self._sync_to_datacenter()
        return profile

    def get_profile(self):
        return self.dao.get_profile()