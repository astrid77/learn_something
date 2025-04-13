#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : day0408_test_collector_meta.py
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/8 下午8:53

"""**练习 3：收集测试方法**
**目标**：实现一个元类，自动收集所有以 `test_` 开头的方法，并存储到 `__test_cases__` 列表中。
**示例**：
```python
class MathTest(metaclass=TestCollectorMeta):
    def test_add(self):
        assert 1+1 == 2

    def helper(self):
        pass

print(MathTest.__test_cases__)  # 输出 ['test_add']
```
"""


class TestCollectorMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs['__test_cases__'] = []
        for k, v in attrs.items():
            if str(k).startswith('test_') and callable(v):
                attrs['__test_cases__'].append(k)
        return super(TestCollectorMeta, cls).__new__(cls, name, bases, attrs)


class MathTest(metaclass=TestCollectorMeta):
    def test_add(self):
        assert 1 + 1 == 2

    def helper(self):
        pass


print(MathTest.__test_cases__)  # 输出 ['test_add']
