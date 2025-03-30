#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : day0330_test_failed_retry.py
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/3/30 下午3:54

"""
失败重试装饰器

**题目：**
编写带参数的装饰器@retry(max_attempts, exceptions), 实现：

1. 对函数进行重试，最多尝试max_attempts次。
2. 仅捕获指定异常类型（如AssertionError）。
3. 每次失败后写入日志文件retry.log（时间、异常信息）。
4. 最终仍失败则抛出原始异常。

**使用示例：**
```python
@retry(max_attempts=3, exceptions=(AssertionError, TimeoutError))
def network_test():
    # 模拟可能失败的操作
```

**覆盖知识点**

- 带参数的装饰器
- 文件操作（追加写入）
- 异常处理（特定类型捕获）
- 函数嵌套定义
"""
import functools
import random
import time

LOG_FILE = "retry.log"  # 错误重试的日志记录文件


def operate_file(log_file, error_msg, mode="a"):
    """将 error_msg 存入 log_file"""
    with open(log_file, mode) as f:
        f.write(error_msg)


def retry(max_attempts, exceptions, log_file=LOG_FILE):
    """带参数的重试装饰器

    :param max_attempts: 最大尝试次数
    :param exceptions: 需要捕获的异常类型（元组）
    :param log_file: 重试日志文件
    """

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)  # 运行测试，若测试通过则返回
                except Exception as e:
                    error_template = "[{time}] 第{attempt}次失败: {error}\n"
                    error_msg = error_template.format(time=time.strftime('%Y-%m-%d %H:%M:%S'), attempt=i, error=e)
                    operate_file(log_file, error_msg)  # 将错误写入文件
                    # 若不是可重试的异常或者已经达到最大的尝试次数，就抛出异常
                    if not isinstance(e, exceptions) or i == max_attempts:
                        raise  # 用 raise 或 raise e from None 保留原始异常信息

        return wrapper

    return decorator


@retry(max_attempts=3, exceptions=(AssertionError, TimeoutError))
def network_test():
    # 模拟可能失败的操作
    assert random.choice([True, False, True, True]), "模拟失败"  # 模拟失败，大概率通过
    1 / random.choice([0, 1, 0])  # 随机触发异常，大概率异常
    return "测试通过"


try:
    operate_file(LOG_FILE, "", "w")  # 不存在文件则创建，已存在则清空文件
    print(network_test())
except:
    with open(LOG_FILE, "r") as log:
        print(log.read())

"""运行结果：（随机）
测试通过

或者

[2025-03-30 17:41:15] 第1次失败: 模拟失败
[2025-03-30 17:41:15] 第2次失败: division by zero
"""
