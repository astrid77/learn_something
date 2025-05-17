#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/5/17 17:37
import pytest


@pytest.hookimpl
def pytest_collection_modifyitems(items):
    print("插件D的钩子执行")
