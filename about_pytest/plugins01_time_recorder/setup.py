#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/5/17 16:31
from setuptools import setup

setup(
    name="pytest-time-recorder",
    version="0.1",
    py_modules=["pytest_time_recorder"],
    entry_points={"pytest11": ["time_recorder = pytest_time_recorder"]},
    install_requires=["pytest>=7.0"],
)

"""
pip install -e .  # 安装插件，-e 开发环境调试，代码修改能立即生效，无需重新安装
pytest --trace-config  # 查看已加载的插件列表
"""
