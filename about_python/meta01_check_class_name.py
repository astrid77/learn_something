#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : day0408_check_class_name.py
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/8 下午8:45

"""**练习 1：强制类名规范**
**目标**：创建一个元类，强制所有使用该元类的类必须以 `Test` 开头命名，否则抛出 `TypeError`。
**示例**：
```python
class TestClass(metaclass=NamingMeta):  # 合法
    pass

class InvalidClass(metaclass=NamingMeta):  # 抛出错误
    pass
```
"""


class NamingMeta(type):
    def __new__(cls, name, bases, attrs):
        if not name.startswith('Test'):
            raise TypeError(f'类名必须以Test开头！非法类：{name}')
        else:
            print(f'类名符合规范：{name}')
        return super(NamingMeta, cls).__new__(cls, name, bases, attrs)


class TestClass(metaclass=NamingMeta):  # 合法
    pass


class InvalidClass(metaclass=NamingMeta):  # 抛出错误
    pass


"""运行结果：
Traceback (most recent call last):
  File "/.../day0408_check_class_name.py", line 33, in <module>
    class InvalidClass(metaclass=NamingMeta):  # 抛出错误
  File "/.../day0408_check_class_name.py", line 23, in __new__
    raise TypeError(f'类名必须以Test开头！非法类：{name}')
TypeError: 类名必须以Test开头！非法类：InvalidClass
类名符合规范：TestClass
"""
