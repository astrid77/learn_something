#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/13 下午1:00

"""
核心目标
实现真正的参数化测试用例分离

新增要求
升级为 @adv_parametrize 装饰器

自动生成独立测试用例

支持参数类型：

元组 (1, 2, 3)

字典 {"x":5, "y":3}

自动生成用例ID：

test_func[param1]

test_func[param2]

python
复制
# 示例用法
class TestAdvanced(unittest.TestCase):
    @adv_parametrize(
        case1=(2, 3, 6),
        case2={"x":0, "y":99, "expected":0}
    )
    def test_multiply(self, x, y, expected):
        self.assertEqual(x * y, expected)
验收标准
测试报告展示独立用例计数

支持混合参数类型

实现至少3种参数传递方式
"""
import inspect
import unittest


def adv_parametrize(**test_cases):
    def decorator(func):
        # 在函数对象上存储测试用例信息
        func._adv_parametrize_cases = test_cases
        return func

    return decorator


def generate_dynamic_cases(test_cls):
    # 遍历类中所有方法
    # 仅遍历用户自定义方法
    for name, method in list(vars(test_cls).items()):
        # 过滤条件：可调用对象 + 有标记 + 非特殊方法
        if (callable(method)
                and hasattr(method, '_adv_parametrize_cases')
                and not name.startswith('__')):

            cases = method._adv_parametrize_cases

            # 动态生成测试方法
            for case_id, params in dict(cases).items():
                def create_test_case(p=params, m=method):
                    if inspect.ismethod(m):  # 判断是否为已实例化的方法
                        def test_case(self):
                            # __func__获取原始函数
                            return m.__func__(self, **p) if isinstance(p, dict) else m.__func__(self, *p)
                    else:
                        def test_case(self):
                            return m(self, **p) if isinstance(p, dict) else m(self, *p)
                    return test_case

                case_name = f"test_{name.split('_', 1)[1]}[{case_id}]"
                setattr(test_cls, case_name, create_test_case())

            # 安全删除原始方法
            if hasattr(test_cls, name):
                delattr(test_cls, name)

    return test_cls


@generate_dynamic_cases
class TestAdvanced(unittest.TestCase):
    @adv_parametrize(
        case1=(2, 3, 6),
        case2={"x": 0, "y": 99, "expected": 0}
    )
    def test_multiply(self, x, y, expected):
        self.assertEqual(x * y, expected)


"""
✅ test_multiply[case1]
✅ test_multiply[case2]
"""
