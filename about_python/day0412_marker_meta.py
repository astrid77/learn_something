#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : day0412_marker_meta.py
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/12 上午11:09

"""
**练习 10：模仿 pytest 的标记系统**
**目标**：通过元类实现类似 `@pytest.mark.slow` 的标记功能，使得可以按标记筛选测试用例。
**功能需求**：
- 用 `@mark('slow')` 装饰测试方法
- 通过命令行参数 `--run-slow` 控制是否执行标记为 `slow` 的测试
"""
import argparse
import time


def mark(*tag):
    def decorator(func):
        func.__marks__ = getattr(func, '__marks__', []) + list(tag)
        return func

    return decorator


class MarkerMeta(type):
    """收集标记的元类"""

    def __new__(cls, name, bases, attrs):
        marked_cases = {}  # 所有标记过的方法字典：{'标记'：[方法名]}
        for name, method in attrs.items():
            # 获取测试方法
            if callable(method) and name.startswith('test_'):
                # 提取标记过的方法
                if hasattr(method, '__marks__'):
                    tags = method.__marks__
                    for tag in tags:
                        marked_cases.setdefault(tag, []).append(name)

        # 获取基类标记过的测试方法
        for base in bases:
            if hasattr(dir(base), '__marked_cases__'):
                marked_cases.update(base.__marked_cases__)

        # 去重
        for tag, cases in marked_cases.items():
            marked_cases[tag] = list(set(cases))
        attrs['__marked_cases__'] = dict(marked_cases)
        new_cls = super().__new__(cls, name, bases, attrs)
        return new_cls


class TestFramework(metaclass=MarkerMeta):
    """测试框架基类"""

    @classmethod
    def run_tests(cls, include=None, exclude=None):
        include = include or []  # 相当于：include = include if include else []
        exclude = exclude or []
        # 获取类的所有测试方法
        all_methods = [name for name in dir(cls)
                       if name.startswith('test_') and callable(getattr(cls, name))]
        selected = []
        for method_name in all_methods:
            # 获取方法对应的tags
            method = getattr(cls, method_name)
            tags = getattr(method, '__marks__', [])

            # 如果方法包含exclude标签，则跳过
            if any(tag in exclude for tag in tags):
                continue

            # 如果没有include标签或者包含则添加
            if not include or any(tag in include for tag in tags):
                selected.append(method_name)

        print("==========开始运行==========")
        print(f'已选用例：{selected}')
        instance = cls()  # 示例化
        result = {'passed': 0, 'failed': 0}
        for name in selected:
            start = time.time()
            if hasattr(instance, 'setup'):
                instance.setup()
            try:
                getattr(instance, name)()  # 执行效果等价于：getattr(cls, name)(instance)
                duration = time.time() - start
                print(f'{name} ✅ ({duration:.2f}秒)')
                result['passed'] += 1
            except AssertionError as e:
                duration = time.time() - start
                result['failed'] += 1
                print(f'{name} x ({duration:.2f}秒) 断言失败: {e}')
            except Exception as e:
                duration = time.time() - start
                result['failed'] += 1
                print(f'{name} x ({duration:.2f}秒) 意外错误:{e}')
            finally:
                if hasattr(instance, 'teardown'):
                    instance.teardown()

        print('==========测试结果==========')
        print(f'总用例数：{len(selected)} | 成功：{result["passed"]} | 失败：{result["failed"]}')
        if include or exclude:
            print(f'筛选条件：include={include},exclude={exclude}')


class DemoTest(TestFramework):
    """测试类"""

    @mark('fast')
    def test_quick(self):
        assert 1 + 1 == 2

    @mark('slow', 'integration')
    def test_slow(self):
        time.sleep(0.5)
        assert 2 * 2 == 5, '模拟失败'  # 这个会失败

    def test_normal(self):
        """未标记的测试方法"""
        assert 'a' in 'abc'


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--include', nargs='+', help='包含的标签')
    parser.add_argument('--exclude', nargs='+', help='排除的标签')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    # 窗口运行，模拟参数
    # args.include = ['fast', 'slow']
    # args.exclude = ['integration']

    # 命令行运行：
    # python day0412_marker_meta.py --include fast slow --exclude intergration
    # 加标签则根据标签过滤后运行，不加标签运行所有用例

    print(DemoTest.__marked_cases__)  # 查看标记的用例
    DemoTest.run_tests(
        include=args.include,
        exclude=args.exclude
    )

"""
{'fast': ['test_quick'], 'slow': ['test_slow'], 'integration': ['test_slow']}
==========开始运行==========
已选用例：['test_normal', 'test_quick', 'test_slow']
test_normal ✅ (0.00秒)
test_quick ✅ (0.00秒)
test_slow x (0.50秒) 断言失败: 模拟失败
==========测试结果==========
总用例数：3 | 成功：2 | 失败：1
"""
