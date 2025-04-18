#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : day0408_decorator_test_meta.py
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/8 下午9:38

"""
**练习 7：测试用例装饰器**
**目标**：实现一个元类，使得用 `@testcase` 装饰器标记的方法会被自动收集为测试用例。
**示例**：
```python
class DecoratorTest(metaclass=DecoratorMeta):
    @testcase
    def case1(self):
        assert True

    def normal_method(self):
        pass

print(DecoratorTest.__test_cases__)  # 输出 ['case1']
```
"""


class DecoratorMeta(type):
    def __new__(cls, name, bases, attrs):
        test_cases = []
        for k, v in attrs.items():
            if getattr(v, '__is_test_case__', False):
                test_cases.append(k)
        attrs['__test_cases__'] = test_cases
        return super().__new__(cls, name, bases, attrs)


def testcase(func):
    # 装饰器修改方法属性，添加用例标记
    func.__is_test_case__ = True
    return func


class DecoratorTest(metaclass=DecoratorMeta):
    @testcase
    def case1(self):
        assert True

    def normal_method(self):
        pass


print(DecoratorTest.__test_cases__)  # 输出 ['case1']
