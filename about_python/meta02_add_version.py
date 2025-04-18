#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : day0408_add_version.py
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/8 下午8:50


"""**练习 2：自动添加版本号**
**目标**：通过元类为所有类自动添加 `__version__ = "1.0.0"` 属性。
**示例**：
```python
class MyClass(metaclass=VersionMeta):
    pass

print(MyClass.__version__)  # 输出 "1.0.0"
```
"""


class VersionMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs['__version__'] = '1.0.0'
        return super(VersionMeta, cls).__new__(cls, name, bases, attrs)


class MyClass(metaclass=VersionMeta):
    pass


print(MyClass.__version__)  # 输出 "1.0.0"
