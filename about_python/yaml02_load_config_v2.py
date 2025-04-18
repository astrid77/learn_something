#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/18 下午3:22

"""
题目：实现嵌套配置项访问

yaml
复制
# input.yaml
database:
  host: "localhost"
  port: 5432
python
复制
print(config.database.host)  # 应输出 "localhost"
print(config.database.port)  # 应输出 5432
知识点：递归属性访问/字典嵌套解析
"""
import yaml


class Config:
    def __init__(self, data: dict):
        for k, v in data.items():
            if isinstance(v, dict):
                setattr(self, k, Config(v))
            else:
                setattr(self, k, v)


def load_yaml_config(filename):
    with open(filename, encoding='utf-8') as f:
        return Config(yaml.safe_load(f))


if __name__ == '__main__':
    config = load_yaml_config('../../python-practise-project/input.yaml')
    print(config.database.host)
    print(config.database.port)
