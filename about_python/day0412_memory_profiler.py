#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : day0412_memory_profiler.py
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/12 下午2:01

"""
# 练习：对比生成器与列表推导式的内存消耗
# 要求：
# a) 用列表推导式生成100万条包含随机整数的记录
# b) 用生成器实现相同功能
# c) 使用memory-profiler测量两者内存差异
# 提示：安装包 pip install memory-profiler
"""
from memory_profiler import profile, memory_usage
import random
import time
import sys
from pympler import asizeof  # 需要安装：pip install pympler

# 配置参数
NUM_ELEMENTS = 10 ** 6
RANDOM_SEED = 42


def measure_time(func):
    """计时装饰器（新增内存追踪）"""

    def wrapper(*args, **kwargs):
        # 内存测量前做垃圾回收
        gc.collect()

        # 记录初始内存
        start_mem = memory_usage(-1, interval=0.1)[0]

        print(f"\n***********{func.__name__}***********")

        # 执行函数并计时
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start_time

        # 记录峰值内存
        end_mem = memory_usage(-1, interval=0.1, max_usage=True)

        print(f"  → 耗时: {elapsed:.4f}秒")
        print(f"  → 峰值内存: {end_mem - start_mem:.4f} MB")
        return result

    return wrapper


@measure_time
@profile(precision=2)
def test_list():
    """列表版本（完整内存统计）"""
    random.seed(RANDOM_SEED)
    data = [random.randint(1, 100) for _ in range(NUM_ELEMENTS)]

    # 精确内存统计（需要pympler）
    print(f"  → 列表对象内存: {asizeof.asizeof(data) / 1024 / 1024:.2f} MB")
    # 基本统计（无需额外库）
    print(f"  → sys.getsizeof: {sys.getsizeof(data) / 1024 / 1024:.2f} MB")

    return sum(data)


@measure_time
@profile(precision=2)
def test_generator():
    """生成器版本（完整内存统计）"""
    random.seed(RANDOM_SEED)
    data = (random.randint(1, 100) for _ in range(NUM_ELEMENTS))

    # 测量生成器对象本身
    print(f"  → 生成器对象内存: {asizeof.asizeof(data) / 1024:.2f} KB")
    print(f"  → sys.getsizeof: {sys.getsizeof(data) / 1024:.2f} KB")

    # 必须消费生成器以测量完整内存
    result = sum(data)

    return result


if __name__ == "__main__":
    import gc

    gc.disable()  # 避免GC影响测量

    print(f"=== 测试开始，数据量：{NUM_ELEMENTS} ===")
    list_total = test_list()
    gen_total = test_generator()

    assert list_total == gen_total
    print("\n=== 测试通过 ===")

"""
=== 测试开始，数据量：1000000 ===

***********test_list***********
  → 列表对象内存: 8.06 MB
  → sys.getsizeof: 8.06 MB
Filename: /Users/wangzhixing/PycharmProjects/python-practise-project/day0412_memory_profiler.py

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    53    15.21 MiB    15.21 MiB           1   @measure_time
    54                                         @profile(precision=2)
    55                                         def test_list():
    56                                             "列表版本（完整内存统计）"
    57    15.21 MiB     0.00 MiB           1       random.seed(RANDOM_SEED)
    58    22.96 MiB     7.75 MiB     1000003       data = [random.randint(1, 100) for _ in range(NUM_ELEMENTS)]
    59                                         
    60                                             # 精确内存统计（需要pympler）
    61    25.16 MiB     2.21 MiB           1       print(f"  → 列表对象内存: {asizeof.asizeof(data) / 1024 / 1024:.2f} MB")
    62                                             # 基本统计（无需额外库）
    63    25.16 MiB     0.00 MiB           1       print(f"  → sys.getsizeof: {sys.getsizeof(data) / 1024 / 1024:.2f} MB")
    64                                         
    65    25.16 MiB     0.00 MiB           1       return sum(data)


  → 耗时: 84.4806秒
  → 峰值内存: 2.5547 MB

***********test_generator***********
  → 生成器对象内存: 0.44 KB
  → sys.getsizeof: 0.11 KB
Filename: /Users/wangzhixing/PycharmProjects/python-practise-project/day0412_memory_profiler.py

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    68    17.53 MiB    17.53 MiB           1   @measure_time
    69                                         @profile(precision=2)
    70                                         def test_generator():
    71                                             "生成器版本（完整内存统计）"
    72    17.53 MiB     0.00 MiB           1       random.seed(RANDOM_SEED)
    73    17.54 MiB     0.00 MiB     2000003       data = (random.randint(1, 100) for _ in range(NUM_ELEMENTS))
    74                                         
    75                                             # 测量生成器对象本身
    76    17.54 MiB     0.01 MiB           1       print(f"  → 生成器对象内存: {asizeof.asizeof(data) / 1024:.2f} KB")
    77    17.54 MiB     0.00 MiB           1       print(f"  → sys.getsizeof: {sys.getsizeof(data) / 1024:.2f} KB")
    78                                         
    79                                             # 必须消费生成器以测量完整内存
    80    17.54 MiB     0.00 MiB           1       result = sum(data)
    81                                         
    82    17.54 MiB     0.00 MiB           1       return result


  → 耗时: 107.6489秒
  → 峰值内存: 0.0117 MB

=== 测试通过 ===
"""
