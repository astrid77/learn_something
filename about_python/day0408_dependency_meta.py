#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : day0408_dependency_meta.py
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/8 下午9:48

"""
**练习 8：测试依赖管理**
**目标**：通过元类实现测试方法的依赖关系管理（如 `test_b` 依赖 `test_a` 先执行）。
**输入**：用装饰器标记依赖关系 `@depends_on('test_a')`
**示例**：
```python
class OrderTest(metaclass=DependencyMeta):
    def test_a(self):
        print("Run test_a")

    @depends_on('test_a')
    def test_b(self):
        print("Run test_b")

# 执行时应保证 test_a 在 test_b 之前运行
```
"""


class DependencyMeta(type):
    def __new__(cls, name, bases, attrs):
        test_cases = []
        for k, v in attrs.items():
            if not k.startswith('test_') or not callable(v):
                continue
            depends = getattr(v, '__depends__', '')
            if depends and depends not in test_cases and k not in test_cases:
                test_cases.extend([depends, k])
            elif depends and depends not in test_cases and k in test_cases:
                ind = test_cases.index(k)
                test_cases.insert(ind, depends)
            elif depends and depends in test_cases and k not in test_cases:
                test_cases.append(k)
            elif depends and depends in test_cases and k in test_cases:
                # 依赖用例和当前用例都已经保存过，依赖用例位置是否可挪动不好判断，当前用例是别的依赖用例可以往前挪
                # raise ValueError("复杂场景，可能涉及循环依赖，暂时跳过")
                print(f"复杂场景，可能涉及循环依赖，暂时跳过:{depends}、{k}")
            elif not depends and k not in test_cases:
                test_cases.append(k)
            elif not depends and k in test_cases:
                pass
        attrs['__test_cases__'] = test_cases
        print(test_cases)
        return super().__new__(cls, name, bases, attrs)


def depends_on(name):
    def decorator(func):
        func.__depends__ = name
        return func

    return decorator


class OrderTest(metaclass=DependencyMeta):

    @depends_on('test_f')
    def test_a(self):
        print("Run test_a")

    @depends_on('test_a')
    def test_b(self):
        print("Run test_b")

    @depends_on('test_d')
    def test_c(self):
        print("Run test_c")

    @depends_on('test_e')
    def test_d(self):
        print("Run test_d")

    @depends_on('test_c')
    def test_e(self):
        print("Run test_e")

    def test_f(self):
        print("Run test_f")

# 执行时应保证 test_a 在 test_b 之前运行
