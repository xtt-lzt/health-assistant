# 健康管理小助手

一个基于 Python 的个人健康追踪工具，支持基础档案管理、每日心情多维记录、数据趋势可视化和 AI 智能健康分析。

## 功能特色

- 健康档案：录入身高、体重、年龄等信息，自动计算 BMI 和基础代谢率。
- 心情记录：多维度记录每日情绪、压力、睡眠、社交状态等，数据本地保存。
- 数据分析：生成各项指标的趋势图表，支持按天聚合与日内波动查看。
- AI 健康助手：对接豆包大模型，根据你的健康数据提供个性化分析和建议。

## 环境要求

- Python 3.8 或以上
- pip

## 安装与运行

1. 克隆仓库
   git clone https://github.com/xtt-lzt/health-assistant.git
   
   cd health-assistant

3. 安装依赖
   pip install -r requirements.txt

4. 配置 API Key
   在config.py中填入你的 API Key。
   示例API Key 获取地址：https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey

5. 运行程序
   python main.py

首次运行会在当前目录自动创建 data 文件夹，用于存储你的个人数据。

## 数据存储

所有数据均保存在 data 文件夹中，包括：
- user_profile.json：基础档案
- mood_records.json：心情记录
- mood_summary.json：统计摘要

## 注意事项

- 若未配置 API Key，AI 功能将无法使用。

## 许可证

MIT License
