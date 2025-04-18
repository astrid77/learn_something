#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/3/27 上午6:57

# 实现一个缓存装饰器 @cache_if_positive，仅当函数的所有参数为正数时才缓存结果，否则每次调用都执行函数。
import functools
import time


def cache_if_positive(cache=60):
    """缓存装饰器，如果函数的参数都为正数，缓存结果，否则直接调用请求。

    :param cache: 缓存时间，默认60秒
    """

    # 缓存结构：{缓存键: (缓存时间戳, 缓存结果)}
    _cache = {}

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 判断参数是否为正数，若是，则查看缓存，否则直接请求
            check_cache = True
            for v in [i for i in args] + [v for _, v in kwargs.items()]:
                if not isinstance(v, (int, float)) or v < 0:
                    check_cache = False
                    break

            if check_cache:
                # 生成唯一缓存键：函数名 + 参数组合
                # 用repr处理参数，确保不同结构的参数生成不同键（简单实现）
                key = (func.__name__,
                       repr(args),
                       repr(tuple(sorted(kwargs.items()))))
                if key in _cache:
                    cached_time, result = _cache[key]
                    if time.time() - cached_time < cache:
                        print("击中缓存！", end=" ")
                    else:
                        print("缓存过期，重新请求～", end=" ")
                        result = func(*args, **kwargs)
                        _cache[key] = (time.time(), result)
                else:
                    # print("没有缓存，发起请求")
                    result = func(*args, **kwargs)
                    _cache[key] = (time.time(), result)
            else:
                # print("参数中值不全是正数，不查缓存，直接请求返回。")
                result = func(*args, **kwargs)
            return result

        # 支持手动清除缓存
        def clear_cache():
            _cache.clear()
            print("清除缓存")

        wrapper.clear_cache = clear_cache
        return wrapper

    return decorator


@cache_if_positive()
def factorial(n):
    return 1 if n == 0 else n * factorial(n - 1)


print(factorial(5))  # 计算并缓存结果 120
print(factorial(5))  # 直接返回缓存结果 120
factorial.clear_cache()
print(factorial(5))  # 重新请求
try:
    print(factorial(-2))  # 每次调用均执行（不缓存）
except RecursionError as e:
    print(f"递归错误:{e}")


@cache_if_positive(cache=1)
def add(a, b):
    return a + b


print(add(2, 3))  # 缓存
print(add(2, 3))  # 命中缓存
time.sleep(1)
print(add(2, 3))  # 缓存过期
print(add(2, -1))  # 不缓存
print(add(2, -1))  # 不缓存
try:
    print(add(2, "invalid"))  # 非数值参数，不缓存（会引发类型错误）
except TypeError as e:
    print(f"类型错误：{e}")

"""运行结果：
120
击中缓存！ 120
清除缓存
120
递归错误:maximum recursion depth exceeded
5
击中缓存！ 5
缓存过期，重新请求～ 5
1
1
类型错误：unsupported operand type(s) for +: 'int' and 'str'
"""
