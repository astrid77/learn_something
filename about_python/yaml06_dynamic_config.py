#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/18 下午4:53

"""题目：实现环境变量覆盖

yaml
复制
# base.yaml
cache_size: 200
python
复制
# 当设置 CACHE_SIZE=500 时
print(config.cache_size)  # 应输出 500
知识点：环境变量优先级、类型自动转换
"""

import os
import yaml
from pathlib import Path


class Config:
    def __init__(self, data: dict):
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, Config(value))
            else:
                setattr(self, key, self._apply_env(key, value))

    def _apply_env(self, key, original_value):
        """应用环境变量覆盖"""
        # 生成环境变量名（CONFIG_KEY格式）
        env_var = f"CONFIG_{key.upper()}"

        # 获取环境变量值
        env_value = os.environ.get(env_var)

        # 类型转换逻辑
        if env_value is not None:
            try:
                # 自动转换原始值的类型
                if isinstance(original_value, bool):
                    return env_value.lower() in ["true", "1"]
                elif isinstance(original_value, int):
                    return int(env_value)
                elif isinstance(original_value, float):
                    return float(env_value)
                else:
                    return env_value
            except ValueError:
                raise TypeError(
                    f"环境变量 {env_var} 类型转换失败，原始类型 {type(original_value)}"
                )
        return original_value


def load_config(file_path: str) -> Config:
    with Path(file_path).open(encoding='utf-8') as f:
        return Config(yaml.safe_load(f))


# 测试用例
if __name__ == "__main__":
    # 设置环境变量
    os.environ["CONFIG_CACHE_SIZE"] = "500"
    os.environ["CONFIG_DEBUG_MODE"] = "true"

    # 测试配置
    test_yaml = """
    cache_size: 200
    debug_mode: false
    """

    with open("temp.yaml", "w") as f:
        f.write(test_yaml)

    config = load_config("temp.yaml")
    print(config.cache_size)  # 500 (int)
    print(config.debug_mode)  # True (bool)

    Path("temp.yaml").unlink()
