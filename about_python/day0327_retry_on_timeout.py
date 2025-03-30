#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : day0327_retry_on_timeout.py
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/3/27 下午9:19

# 题目：超时重试装饰器
# 要求：编写一个装饰器@retry_on_timeout(max_retries=3, timeout=2)，当函数执行时间超过timeout秒时自动重试，最多重试max_retries次，全部失败后抛出TimeoutError。
# 知识点：带参数的装饰器、并发执行（如队列/多线程）

import functools
import queue
import random
import time
import threading


def retry_on_timeout(max_retries=3, timeout=2):
    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_retries):
                q = queue.Queue()
                msg = f"\r第{i + 1}次尝试请求中..."

                def target():
                    try:
                        print(msg, end="")
                        value = func(*args, **kwargs)
                        q.put((True, value))
                    except Exception as e:
                        q.put((False, e))

                t = threading.Thread(target=target)
                t.daemon = True
                t.start()
                t.join(timeout)
                if t.is_alive():
                    if i == max_retries - 1:
                        print("\r" + " " * len(msg) + "\r", end="")
                        raise TimeoutError("请求超时！")
                    continue
                else:
                    success, result = q.get()
                    print("\r" + " " * len(msg) + "\r", end="")
                    if success:
                        return result
                    else:
                        raise result

        return wrapper

    return decorator


@retry_on_timeout()
def add(x, y):
    time.sleep(random.random() * 7)  # 随机，但大概率超时
    return x + y


print(add(1, 2))

"""运行结果：
Traceback (most recent call last):
  File ".../day0327_retry_on_timeout.py", line 64, in <module>
    print(test(1, 2))
  File ".../day0327_retry_on_timeout.py", line 43, in wrapper
    raise TimeoutError("请求超时！")
TimeoutError: 请求超时！

# 或者

3
"""
