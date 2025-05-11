#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/5/11 17:43

def test_timeout(timeout):
    print(f"超时时间: {timeout}s")
    assert timeout > 0


"""运行指令：
pytest -s --timeout=40
"""
