#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/3/30 下午1:58

"""测试数据处理

**题目：**
编写一个函数process_test_results(results_str)，接收一个字符串results_str，格式为"用例1:通过,用例2:失败,用例3:通过..."，要求：
1. 将字符串解析为字典，键为用例名，值为是否通过（布尔值）。
2. 返回通过率（百分比，保留两位小数）和失败用例名的列表。
3. 使用列表推导式、类型转换、字符串格式化。

**示例输入**

"登录测试:通过,权限测试:失败,界面测试:通过"

**示例输出**

`(66.67, \['权限测试'\])`

**覆盖知识点**
- 字符串操作（split、strip）
- 字典与列表推导式
- 函数返回值（元组）
- 浮点数精度控制（round）
"""


def process_test_results(results_str: str) -> tuple:
    """解析运行结果，按格式返回

    :param results_str: 运行结果字符串，格式为"用例1:通过,用例2:失败,用例3:通过...
    :return: 返回一个元组：(用例通过率，失败用例名列表)
    """

    failed_cases = []  # 失败用例名列表
    pass_percent = 0  # 用例通过率

    # 这里是按严格的格式要求做的处理，如果格式可能异常的话，就需要加额外的判断
    results_dict = {value.split(":")[0].strip(): value.split(":")[1].strip() for value in results_str.split(",") if
                    ":" in value}

    for k, v in results_dict.items():
        if v == "失败":
            failed_cases.append(k)

    if results_dict:
        pass_percent = round((len(results_dict) - len(failed_cases)) / len(results_dict.items()), 2)

    result = (pass_percent, failed_cases)
    return result


def test():
    result_str = "用例1:通过,用例2:失败,用例3:通过"
    pass_percent, failed_cases = process_test_results(result_str)
    print(pass_percent, failed_cases)

    assert "用例2" in failed_cases, "失败用例统计错误"
    assert "用例1" not in failed_cases and "用例3" not in failed_cases, "失败用例中错误包含了成功用例"
    assert isinstance(pass_percent, float), "成功率格式不正确"


if __name__ == '__main__':
    test()

"""运行结果：
0.67 ['用例2']
"""
