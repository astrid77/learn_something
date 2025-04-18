#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/3/29 下午4:00

# 装饰器堆叠依赖
# 实现一个装饰器@depends_on(*dependencies)，确保被装饰函数仅在所有dependencies（其他函数）都已被调用至少一次后才允许执行，否则抛出DependencyError。
import functools

called_functions = {}


class DependencyError(Exception):
    pass


def depends_on(*dependencies):
    def decorator(func):
        for d in dependencies:
            @functools.wraps(d)
            def wrapper_dep(*args, _d=d, **kwargs):
                # 因为多个函数共享一个wrapper_dep，该值会指向循环中的最后一个函数，需要通过将当前运行的函数d，重新赋值使用
                result = _d(*args, **kwargs)
                called_functions[_d.__name__] = True
                return result
            # 自动为依赖的函数添加装饰器，标记运行状态（不推荐，维护困难）
            globals()[d.__name__] = wrapper_dep
            called_functions[d.__name__] = False

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for d in dependencies:
                if not called_functions.get(d.__name__, False):
                    raise DependencyError(f"Dependency '{d.__name__}' not called.")
            result = func(*args, **kwargs)
            called_functions[func.__name__] = True
            return result

        return wrapper

    return decorator


def test1():
    return "run test1."


def test2():
    return "run test2."


@depends_on(test1, test2)
def test():
    return "run test."


try:
    print(test())
except DependencyError as e:
    print(e)

print(test1())
print(test2())

print(test())

"""运行结果：
Dependency 'test1' not called.
run test1.
run test2.
run test.
"""
