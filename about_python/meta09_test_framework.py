#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : day0408_test_framework.py
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/8 下午10:14

"""
**练习 9：简易测试框架**
**目标**：结合元类实现一个完整测试框架，支持以下功能：
1. 自动收集 `test_` 方法
2. 支持 `setup()` 和 `teardown()`
3. 统计执行结果（成功/失败数）
4. 生成 HTML 测试报告（可选）

**示例输出**：
```text
Running 3 tests...
✓ test_add (0.002s)
✗ test_subtract (AssertionError: 5-3 != 3)
✓ test_multiply (0.001s)
Results: 2 passed, 1 failed
```
"""


class TestCollectorMeta(type):

    def __new__(cls, name, bases, attrs):
        cases = {name: method for name, method in attrs.items()
                 if callable(method) and str(name).startswith('test_')}

        for base in bases:
            if hasattr(base, '__test_cases__'):
                cases.update(base.__test_cases__)

        new_cls = super().__new__(cls, name, bases, attrs)
        new_cls.__test_count__ = len(cases)
        new_cls.__test_cases__ = cases
        return new_cls


class TestFramework(metaclass=TestCollectorMeta):
    @classmethod
    def get_test_count(cls):
        return cls.__test_count__

    @classmethod
    def run_tests(cls):
        instance = cls()
        for name, method in instance.__test_cases__.items():
            if hasattr(instance, 'setup'):
                instance.setup()
            print(f'Running {name}...')
            method(instance)
            if hasattr(instance, 'teardown'):
                instance.teardown()


class MathTests(TestFramework):
    def setup(self):
        print('setup')

    def test_addition(self):
        assert 1 + 1 == 2, "加法测试失败"

    def test_subtraction(self):
        assert 5 - 3 == 2, "减法测试失败"

    def helper_method(self):
        """非测试方法不会被收集"""
        pass

    def teardown(self):
        print('teardown')


class AdvancedTests(MathTests):
    def test_multiplication(self):
        assert 2 * 3 == 6, "乘法测试失败"


print("MathTests 用例数:", MathTests.get_test_count())  # 输出 2
print("AdvancedTests 用例数:", AdvancedTests.get_test_count())  # 输出 3

print("\n执行 MathTests:")
MathTests.run_tests()

print("\n执行 AdvancedTests:")
AdvancedTests.run_tests()

"""运行结果：
MathTests 用例数: 2
AdvancedTests 用例数: 3

执行 MathTests:
setup
Running test_addition...
teardown
setup
Running test_subtraction...
teardown

执行 AdvancedTests:
setup
Running test_multiplication...
teardown
setup
Running test_addition...
teardown
setup
Running test_subtraction...
teardown
"""
