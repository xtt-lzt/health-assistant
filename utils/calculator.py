# utils/calculator.py

def calculate_bmi(height_cm, weight_kg):
    """
    计算 BMI (身体质量指数)
    :param height_cm: 身高 (厘米)
    :param weight_kg: 体重 (千克)
    :return: BMI 数值
    """
    if height_cm <= 0:
        return 0
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 1)

def calculate_bmr(gender, age, height_cm, weight_kg):
    """
    计算 BMR (基础代谢率)，使用 Mifflin-St Jeor 公式
    :param gender: 'male' 或 'female'
    :param age: 年龄
    :param height_cm: 身高 (厘米)
    :param weight_kg: 体重 (千克)
    :return: BMR 数值 (大卡)
    """
    if gender == 'male':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    return round(bmr)