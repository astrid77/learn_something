#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/5/17 14:34

"""动态过滤逻辑
  - 开发支持 `--tags=smoke,regression` 的参数
  - 练习：实现标签交集/并集过滤
"""

import pytest


def pytest_collection_modifyitems(config, items):
    tags = config.getoption('--tags')

    if tags:
        tags = tags.split(',')
        mode = config.getoption('--tag-mode')

        skip_tag = pytest.mark.skip(reason='未包含指定标签，跳过执行')
        for item in items:
            item_markers = [marker.name for marker in item.iter_markers()]

            if (mode == 'all' and not all(tag in item_markers for tag in tags)) or (
                    mode == 'any' and not any(tag in item_markers for tag in tags)):
                item.add_marker(skip_tag)


def pytest_addoption(parser):
    parser.addoption('--tags')
    parser.addoption('--tag-mode', default='any', choices=['all', 'any'])
