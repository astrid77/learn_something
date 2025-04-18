#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/18 下午3:51


"""题目：实现环境配置加载
文件结构：

复制
config/
  base.yaml
  dev.yaml
  prod.yaml
python
复制
# 当设置 ENV=prod 时
print(config.db_url)  # 应输出 "cluster.prod.example.com"
知识点：环境变量读取、多文件加载策略
"""

import yaml
import os
from pathlib import Path


class Config:
    def __init__(self, data: dict):
        """递归构建配置对象"""
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, Config(value))
            else:
                setattr(self, key, value)


def load_multi_config(config_dir="config"):
    # 加载基础配置
    base_file = Path(config_dir) / "base.yaml"
    with open(base_file, 'r', encoding='utf-8') as f:
        base = yaml.safe_load(f) or {}

    # 获取当前环境（默认dev）
    env = os.environ.get("ENV", "dev")
    env_file = Path(config_dir) / f"{env}.yaml"

    # 加载环境配置
    env_config = {}
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            env_config = yaml.safe_load(f) or {}

    # 合并配置（环境配置覆盖基础配置）
    return Config({**base, **env_config})


# 测试用例
if __name__ == "__main__":
    # 模拟设置环境变量
    os.environ["ENV"] = "prod"

    # 初始化配置
    config = load_multi_config()

    # 验证配置项
    print(config.url)  # 应输出 prod.yaml 中定义的地址
