#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/26 下午2:04

"""pytest测试用例添加超时重试机制
知识点：灵活使用装饰器"""

import functools
import queue
import random
import threading
import time
import pytest


def retry_by_own(reruns=1, timeout=3, delay=0):
    """
    超时重试
    :param reruns: 重试次数
    :param timeout: 超时时间（秒）
    :param delay: 延迟重试时间（秒）
    :return:
    """

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            def target():
                try:
                    result = (True, func(*args, **kwargs))
                except Exception as e:
                    result = (False, e)
                q.put(result)
                return result

            nonlocal reruns
            while reruns >= 0:
                reruns -= 1
                q = queue.Queue()
                thread = threading.Thread(target=target)
                thread.daemon = True
                thread.start()
                thread.join(timeout)

                if thread.is_alive():
                    if reruns <= 0:
                        raise TimeoutError('请求超时')
                else:
                    success, result = q.get()
                    if success:
                        print('测试通过')
                        return result
                    else:
                        if type(result) in (TimeoutError,):
                            time.sleep(delay)
                        else:
                            raise result

        return wrapper

    return decorator


def retry_with_pytest(reruns=1, timeout=3, delay=0):
    """使用pytest相关装饰器进行重试和超时处理"""
    return pytest.mark.flaky(reruns=reruns, reruns_delay=delay)(pytest.mark.timeout(timeout))


def retry_with_mix_decorator(reruns=1, timeout=3, delay=0):
    """混合模式：利用插件重试 + 自定义条件"""

    def decorator(func):
        def wrapper(*args, **kwargs):

            def target():
                try:
                    result = (True, func(*args, **kwargs))
                except Exception as e:
                    result = (False, e)
                q.put(result)
                return result

            q = queue.Queue()
            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()
            thread.join(timeout)

            if thread.is_alive():
                raise TimeoutError('请求超时')
            else:
                success, result = q.get()
                if success:
                    print('测试通过')
                    return result
                else:
                    raise result

        return pytest.mark.flaky(reruns=reruns, reruns_delay=delay)(functools.wraps(func)(wrapper))

    return decorator


@retry_with_mix_decorator(reruns=3, timeout=3, delay=1)
@pytest.mark.parametrize('case', [1, 2, 3, 4, 5])
def test_example(case):
    time.sleep(random.randint(1, 5))
    assert random.choice([True, False])
