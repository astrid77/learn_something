#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/3/29 下午12:22

# 装饰器类实现日志
# 用类（而非函数）实现一个装饰器@Logger(prefix="DEBUG:")
# 在函数调用前后打印带prefix的日志（如DEBUG: Function foo started）。
import functools


class Logger:
    def __init__(self, prefix="DEBUG:"):
        self.prefix = prefix

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"{self.prefix}Function {func.__name__} started, params is {args} and {kwargs}")
            result = func(*args, **kwargs)
            print(f"{self.prefix}Function {func.__name__} stopped.")
            return result

        return wrapper


@Logger()
def test(*args, **kwargs):
    print("run test")


test(1, 2, 3, a=4, b=5)

"""运行结果：
DEBUG:Function test started, params is (1, 2, 3) and {'a': 4, 'b': 5}
run test
DEBUG:Function test stopped.
"""
