#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : day0408_dynamic_test_meta.py
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/8 下午9:28

"""
**练习 6：动态生成测试方法**
**目标**：通过元类根据配置文件动态生成测试方法。
**输入**：配置文件 `test_config = {"test_case1": "assert 1>0", "test_case2": "assert 'a' in 'abc'"}`
**输出**：类自动生成 `test_case1`、`test_case2` 等方法。
**示例**：
```python
class DynamicTest(metaclass=DynamicTestMeta):
    _config = test_config

obj = DynamicTest()
obj.test_case1()  # 自动执行 assert 1>0
```
"""
test_config = {"test_case1": "assert 1>0,'验证1>0失败'", "test_case2": "assert False,'模拟失败'"}


class DynamicTestMeta(type):
    def __new__(cls, name, bases, attrs):
        config = attrs['_config']
        for name, assert_content in config.items():

            def method(self):
                namespace = {'self': self}  # 将self传入执行环境
                exec(assert_content, namespace)  # 动态执行断言语句

            attrs[name] = classmethod(method)
        return super(DynamicTestMeta, cls).__new__(cls, name, bases, attrs)


class DynamicTest(metaclass=DynamicTestMeta):
    _config = test_config


obj = DynamicTest()
obj.test_case1()  # 自动执行 assert 1>0

"""运行结果：
Traceback (most recent call last):
  File "/.../day0408_dynamic_test_meta.py", line 42, in <module>
    obj.test_case1()  # 自动执行 assert 1>0
  File "/.../day0408_dynamic_test_meta.py", line 31, in method
    exec(assert_content, namespace)  # 动态执行断言语句
  File "<string>", line 1, in <module>
AssertionError: 模拟失败
"""