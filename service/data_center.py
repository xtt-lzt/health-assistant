# service/data_center.py
"""
全局数据中心：唯一的模块间耦合中转站
所有模块只能通过这里共享数据，不能直接import其他模块的service
基础信息修改后自动同步，所有业务模块实时获取最新基准数据
"""

class DataCenter:
    # 全局共享数据存储，key-value格式
    _shared_data = {}
    # 数据变更回调，用于界面实时更新
    _update_callbacks = []

    @classmethod
    def set(cls, key, value):
        """设置共享数据，触发更新回调"""
        cls._shared_data[key] = value
        # 触发所有注册的更新回调，实现界面实时刷新
        for callback in cls._update_callbacks:
            try:
                callback()
            except:
                pass

    @classmethod
    def get(cls, key, default=None):
        """获取共享数据"""
        return cls._shared_data.get(key, default)

    @classmethod
    def delete(cls, key):
        """删除指定数据"""
        if key in cls._shared_data:
            del cls._shared_data[key]

    @classmethod
    def clear(cls):
        """清空所有共享数据"""
        cls._shared_data.clear()

    @classmethod
    def register_update_callback(cls, callback):
        """注册数据更新回调，用于界面实时刷新"""
        cls._update_callbacks.append(callback)

    @classmethod
    def init_base_data(cls, profile):
        """初始化/更新基础信息数据，基础信息模块专用"""
        # 同步所有业务模块需要的核心基准数据
        cls.set("user_name", profile.get("name", "用户"))
        cls.set("gender", profile.get("gender", "male"))
        cls.set("age", profile.get("age", 0))
        cls.set("height_cm", profile.get("height_cm", 0))
        cls.set("weight_kg", profile.get("weight_kg", 0))
        cls.set("bmr", profile.get("calculated", {}).get("bmr", 0))
        cls.set("recommended_calories", profile.get("calculated", {}).get("recommended_calories", 0))
        cls.set("health_goal", profile.get("goal", ""))

    @classmethod
    def set_silent(cls, key, value):
        """设置共享数据，不触发更新回调"""
        cls._shared_data[key] = value