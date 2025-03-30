#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : day0330_base_test_class.py
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/3/30 下午2:01

"""
测试框架基类设计

**题目：**
1. 创建一个BaseTest类，包含类属性test_count=0。
2. 实现__init__方法自动为每个实例生成唯一ID（格式：Test_序号）。
3. 添加装饰器@log_test，记录测试执行时间到日志。
4. 创建子类UITest，重写run_test方法，支持设置超时参数。


**代码框架：**
```python
import time

def log_test(func):
    # 你的代码（记录func执行时间）

class BaseTest:
    # 你的代码（自动ID生成）

class UITest(BaseTest):
    def run_test(self, timeout=None):
        # 你的代码（模拟测试逻辑）
```

**覆盖知识点**

- 类与继承
- 装饰器（记录时间）
- 实例属性与类属性
- 方法重写与super()
"""
import functools
import random
import time

LOG = {}  # 测试日志


def log_test(func):
    """记录测试执行时间到日志"""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        global LOG
        LOG.update({self.test_id: {}})
        log = LOG[self.test_id]

        timeout = kwargs.get("timeout", None)  # 优先从关键字参数中找到timeout
        if not timeout:
            timeout = args[0]  # 再从位置参数中找
        log["timeout"] = timeout

        start = time.time()  # 开始时间
        try:
            result = func(self, *args, **kwargs)  # 执行测试
        except AssertionError as e:
            result = e

        log["result"] = result

        end = time.time()  # 结束时间
        duration = round((end - start), 2)  # 运行时间，单位：毫秒
        log["duration"] = duration

        print(f"[LOG] 用例: {self.test_id} | 运行时长: {duration:3.2f}s | 超时时间: {timeout}s")

        return result

    return wrapper


class BaseTest:
    test_count = 0

    def __init__(self):
        # 生成唯一ID（格式：Test_序号）
        BaseTest.test_count += 1  # 所有实例共享同一个类变量，修改类变量会影响所有实例
        self.test_id = f"Test_{BaseTest.test_count}"

    def run_test(self):
        """基类测试方法，须被子类重写"""
        raise NotImplementedError("请重写测试方法！")


class UITest(BaseTest):

    @log_test
    def run_test(self, timeout):
        """重写run_test方法，支持设置超时参数"""

        print(f"用例编号：{self.test_id}，开始执行，超时时间是{timeout}s")

        # 随便写一个断言，判断两个值是否一致，随机值，大概率失败
        x = random.randint(1, 3)
        time.sleep(x)  # 模拟测试耗时
        test_result = random.randint(1, 3)
        assert x == test_result, "运行结果不正确"
        return "测试通过"


for i in range(1, 5):
    UITest().run_test(random.randint(1, 5))

print(LOG)

"""运行结果：（随机）
用例编号：Test_1，开始执行，超时时间是5s
[LOG] 用例: Test_1 | 运行时长: 1.00s | 超时时间: 5s
用例编号：Test_2，开始执行，超时时间是2s
[LOG] 用例: Test_2 | 运行时长: 2.00s | 超时时间: 2s
用例编号：Test_3，开始执行，超时时间是4s
[LOG] 用例: Test_3 | 运行时长: 1.01s | 超时时间: 4s
用例编号：Test_4，开始执行，超时时间是3s
[LOG] 用例: Test_4 | 运行时长: 1.01s | 超时时间: 3s
{'Test_1': {'timeout': 5, 'result': AssertionError('运行结果不正确'), 'duration': 1.0}, 'Test_2': {'timeout': 2, 'result': AssertionError('运行结果不正确'), 'duration': 2.0}, 'Test_3': {'timeout': 4, 'result': '测试通过', 'duration': 1.01}, 'Test_4': {'timeout': 3, 'result': '测试通过', 'duration': 1.01}}
"""
