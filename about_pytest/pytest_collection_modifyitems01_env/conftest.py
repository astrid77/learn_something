#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/5/13 19:53

"""钩子函数开发
  - 实现 `pytest_collection_modifyitems`
  - 练习：根据标签跳过特定环境用例
"""
import os

import pytest


def pytest_collection_modifyitems(items):
    env_markers = {
        'local': ['debug', 'smoke', 'regression'],
        'test': ['debug'],
        'dev': ['regression'],
    }
    env = os.getenv('ENV')  # 获取运行环境，有多种方式设置ENV，比如可通过 ENV=dev pytest运行获取环境
    try:
        markers = env_markers[env]
    except:
        print('请先添加环境可执行的标签～')
        markers = []

    if markers:
        skip_env = pytest.mark.skip(reason=f'{env}环境跳过执行')

        for item in items:
            markers_gen = item.iter_markers()  # 返回一个生成器
            try:
                while markers_gen:
                    m = next(markers_gen)  # 获取下一个marker
                    if m.name in markers:  # 如果包含对应标签就跳过
                        break
            except:
                item.add_marker(skip_env)  # 若当前用例所有标签遍历结束都没有可执行的标签，则添加跳过标签
