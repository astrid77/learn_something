#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/5/17 16:34
import time


def test_sleep():
    time.sleep(1)
    assert True


def test_fast():
    time.sleep(0.3)
    assert 1 + 1 == 2
