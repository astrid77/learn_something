#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/5/13 19:53
import os

import pytest

# os.environ["ENV"] = "test"  # 设置运行环境


@pytest.mark.smoke
@pytest.mark.parametrize(('x', 'y', 'expected'), [(1, 2, 3), (1, 3, 5)])
def test_add(x, y, expected):
    assert x + y == expected


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.parametrize(('x', 'y', 'expected'), [(2, 2, 2), (2, 3, 5)])
def test_add1(x, y, expected):
    assert x + y == expected


@pytest.mark.debug
@pytest.mark.parametrize(('x', 'y', 'expected'), [(3, 3, 3), (3, 6, 9)])
def test_add2(x, y, expected):
    assert x + y == expected


"""pytest -m smoke  # 只运行标记为 smoke 的测试"""
