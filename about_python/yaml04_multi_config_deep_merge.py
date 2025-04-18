#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/18 下午5:05

"""题目：环境叠加+嵌套访问

# base.yaml
url: example.com
logging:
  level: "INFO"
  path: "/var/log"
server:
  port: "8080"

# dev.yaml
url: dev.example.com
logging:
  path: "/tmp"
report: "report"

# 当加载dev环境时
print(config.logging.level)  # 应输出 "INFO" (继承base)
print(config.logging.path)   # 应输出 "/tmp" (覆盖)
知识点：配置继承与覆盖机制
"""

import yaml
import os
from pathlib import Path


class Config:
    def __init__(self, data: dict):
        self._source_data = data
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, Config(value))
            else:
                setattr(self, key, value)

    def __str__(self):
        return f'{self._source_data}'


def deep_merge(base: dict, update: dict) -> dict:
    """递归合并嵌套字典"""

    # 浅拷贝，仅复制字典的最外层键值对，内部的嵌套对象仍然是原对象的引用，一般来说修改merged会影响base
    # 但这里每次递归调用 deep_merge 都会创建新的字典对象，每次只修改副本第一层数据，不会影响原base
    merged = base.copy()

    for key, value in update.items():
        # 处理嵌套字典合并
        if isinstance(value, dict) and key in base and isinstance(base[key], dict):
            merged[key] = deep_merge(base[key], value)
        else:
            merged[key] = value

    return merged


def load_env_config(config_dir="config") -> Config:
    # 加载基础配置
    base_file = Path(config_dir) / "base.yaml"
    with open(base_file, 'r', encoding='utf-8') as f:
        base = yaml.safe_load(f) or {}

    # 加载环境配置
    env = os.environ.get("ENV", "dev")
    env_file = Path(config_dir) / f"{env}.yaml"
    env_config = {}
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            env_config = yaml.safe_load(f) or {}

    # 深度合并配置
    merged = deep_merge(base, env_config)
    return Config(merged)


# 测试用例
if __name__ == "__main__":
    os.environ["ENV"] = "dev"
    config = load_env_config()

    print(config.logging.level)  # 应输出 INFO (来自base)
    print(config.logging.path)  # 应输出 /tmp (来自dev覆盖)
