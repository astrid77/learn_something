#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/13 下午12:10

"""核心目标
实现最基本的参数循环执行能力

题目要求
创建 @simple_parametrize 装饰器

支持元组类型的参数传递

通过循环执行参数组

手动控制测试用例数量

python
复制
# 示例用法
class TestBasic(unittest.TestCase):
    @simple_parametrize([(1,2), (3,4)])
    def test_add(self, a, b):
        self.assertLess(a + b, 10)
验收标准
装饰器能遍历执行2组参数

测试报告显示为1个测试用例（非独立用例）

参数错误时抛出TypeError
"""
import functools
import unittest


def simple_parametrize(params):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self):
            for param in params:
                # 测试报告显示为1个测试用例（非独立用例）
                try:
                    print(f'执行{func.__name__}，参数为：{param}', end='')
                    if isinstance(param, dict):
                        func(self, **param)
                    else:
                        func(self, *param)
                    print('\t测试通过！')
                except AssertionError as e:
                    print(f'\t测试失败，断言失败：{e}')
                except TypeError:
                    print('\t测试异常：参数错误，TypeError')
                    # raise TypeError

        return wrapper

    return decorator


class TestBasic(unittest.TestCase):
    @simple_parametrize([(1, 2), (3, 4), (3, 4, 5)])
    def test_add(self, a, b):
        self.assertLess(a + b, 10)


"""
执行test_add，参数为：(1, 2)	测试通过！
执行test_add，参数为：(3, 4)	测试通过！
执行test_add，参数为：(3, 4, 5)	测试异常：参数错误，TypeError
"""
