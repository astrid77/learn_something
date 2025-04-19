#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/18 下午4:31

"""题目：实现配置项类型校验

yaml
复制
server:
  port: "8080"  # 实际需要整数
python
复制
# 应抛出类型错误异常
# 期望报错：TypeError: server.port需要int类型，但得到str
知识点：动态类型检查、异常处理
"""
from pathlib import Path

import yaml


def type_check(data: dict, schema: dict):
    """类型检查"""
    for name, value in schema.items():
        if name not in data:
            raise ValueError(f"缺少必要参数：{name}")
        # 预期的参数类型
        required_type = value if isinstance(value, type) else type(value)
        if not isinstance(data[name], required_type):
            raise TypeError(f'{name}参数类型不对，预期是{required_type}，实际上是{type(data[name])}')
        # 如果嵌套参数，则继续遍历检查
        if not isinstance(value, type):
            type_check(data[name], value)


class Config:
    """将data内容转化为可以点的属性"""

    def __init__(self, data: dict):
        for k, v in data.items():
            if isinstance(v, dict):
                setattr(self, k, Config(v))
            else:
                setattr(self, k, v)


def load_yaml(file, config_dir="config"):
    """加载yaml文件内容"""
    filepath = Path(config_dir) / file
    with open(filepath, encoding='utf-8') as f:
        return yaml.safe_load(f)


if __name__ == '__main__':
    # 需要校验类型的参数
    valid_schema = {
        "url": str,
        "logging": dict,
        "server": {"port": int}
    }
    # 加载配置
    data = load_yaml('base.yaml')
    # 校验参数类型
    type_check(data, valid_schema)
    # 转换配置
    config = Config(data)
    print(config.url)
    print(config.server.port)
