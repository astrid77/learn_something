#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : day0408_test_stats_meta.py
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/8 下午8:57

"""**练习 4：统计测试用例数量**
**目标**：在练习3的基础上，添加 `test_count` 属性，动态统计当前类的测试用例数量。
**扩展**：支持统计子类继承的父类测试用例数量。
**示例**：
```python
class BaseTest(metaclass=TestStatsMeta):
    def test_base(self):
        pass

class SubTest(BaseTest):
    def test_sub(self):
        pass

print(SubTest.test_count)  # 输出 2（继承父类+自身）
```
"""


class TestStatsMeta(type):
    __test_cases__ = []

    def __new__(cls, name, bases, attrs):
        test_cases = []
        for k, v in attrs.items():
            if str(k).startswith('test_') and callable(v):
                test_cases.append(k)

        # 从父类获取测试用例
        for base in bases:
            test_cases.extend(getattr(base, '__test_cases__', []))

        attrs['__test_cases__'] = test_cases
        attrs['test_count'] = len(test_cases)
        return super(TestStatsMeta, cls).__new__(cls, name, bases, attrs)


class BaseTest(metaclass=TestStatsMeta):
    def test_base(self):
        pass


class SubTest(BaseTest):
    def test_sub(self):
        pass


print(SubTest.test_count)  # 输出 2（继承父类+自身）
