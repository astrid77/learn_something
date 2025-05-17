#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/5/13 19:53
import os

import pytest


@pytest.mark.smoke
@pytest.mark.parametrize(('x', 'y', 'expected'), [(1, 2, 3)])
def test_add(x, y, expected):
    assert x + y == expected


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.parametrize(('x', 'y', 'expected'), [(2, 3, 5)])
def test_add1(x, y, expected):
    assert x + y == expected


@pytest.mark.debug
@pytest.mark.parametrize(('x', 'y', 'expected'), [(3, 6, 9)])
def test_add2(x, y, expected):
    assert x + y == expected


"""运行指令示例：
pytest -s -q --tags=smoke  # 2 failed, 2 passed, 2 skipped
pytest --tags=regression,smoke --tag-mode=all  # 1 failed, 1 passed, 4 skipped
"""
