#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/18 下午3:06

"""
题目：实现基础YAML配置加载器
需求：读取YAML文件中timeout和max_connections两个顶层配置项

# input.yaml
timeout: 30
max_connections: 100

# python
print(config.timeout)       # 应输出 30
print(config.max_connections) # 应输出 100
知识点：基础文件解析、字典键值访问
"""
import yaml
from pathlib import Path


class Config:
    def __init__(self, data: dict):
        # 调试输出
        print(f"[DEBUG] 初始化Config，输入数据类型: {type(data)}")
        print(f"[DEBUG] 输入数据内容: {data}")

        for key, value in data.items():
            setattr(self, key, value)

    def __getattr__(self, name):
        """访问不存在的属性时抛出明确错误"""
        raise AttributeError(f"'{self.__class__.__name__}'对象没有'{name}'配置项")


def load_config(file_path: str) -> Config:
    try:
        with Path(file_path).open(encoding='utf-8') as f:
            raw_data = yaml.safe_load(f)
    except FileNotFoundError:
        raise RuntimeError(f"配置文件 {file_path} 不存在")

    if not isinstance(raw_data, dict):
        raise TypeError(
            f"YAML文件应解析为字典，实际得到 {type(raw_data).__name__}\n"
            f"文件内容预览: {str(raw_data)[:50]}..."
        )

    return Config(raw_data)


# 测试
try:
    config = load_config("../../python-practise-project/input.yaml")
    print(config.timeout)
    print(config.name)
except Exception as e:
    print(f"错误信息: {str(e)}")

"""
[DEBUG] 初始化Config，输入数据类型: <class 'dict'>
[DEBUG] 输入数据内容: {'timeout': 30, 'max_connections': 100}
30
错误信息: 'Config'对象没有'name'配置项
"""
