#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/5/11 18:22

def test_env(env):
    assert env == 'test', '非test环境不运行'

"""运行指令：
pytest --env=test
"""