#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : day0408_singleton_meta.py
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/8 下午9:06


"""**练习 5：单例测试基类**
**目标**：通过元类实现一个单例模式的基类 `SingletonTest`，确保所有子类只能被实例化一次。
**示例**：
```python
class DatabaseTest(SingletonTest):
    def __init__(self):
        self.connection = "DB Connected"

t1 = DatabaseTest()
t2 = DatabaseTest()
print(t1 is t2)  # 输出 True
```
"""


class SingletonMeta(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super().__call__(*args, **kwargs)
        return cls._instance[cls]


class SingletonTest(metaclass=SingletonMeta):
    pass


class DatabaseTest(SingletonTest):
    def __init__(self):
        self.connection = "DB Connected"


t1 = DatabaseTest()
t2 = DatabaseTest()
print(t1 is t2)  # 输出 True
