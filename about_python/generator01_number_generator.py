#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/12 下午1:31

"""
# 练习：创建一个生成器函数 number_generator
# 要求：生成1到10000的整数，每次生成平方值
# 测试：使用next()获取前3个值并打印
# 预期输出：1, 4, 9
"""


def number_generator():
    for i in range(1, 10001):
        yield i ** 2


ng = number_generator()
for _ in range(3):
    print(next(ng))
