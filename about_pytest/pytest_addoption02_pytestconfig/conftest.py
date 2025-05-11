#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/5/11 18:22
from random import choices

import pytest


def pytest_addoption(parser):
    parser.addoption('--env',
                     choices=['test', 'prod', 'dev'],
                     help='请指定测试运行环境')


def pytest_configure(config):
    env = config.getoption("--env")
    print(f"\n[全局环境] {env}")  # 在测试开始前明确展示


@pytest.fixture
def env(pytestconfig):
    return pytestconfig.getoption('--env')
