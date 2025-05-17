#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/5/17 14:59

"""创建能解析以下参数的解析器
# --env=prod/stage, -v (verbose), --tags=smoke,regression
# 输出解析后的参数字典
"""


def pytest_configure(config):
    # print(dir(config))
    # 打印原始命令行参数
    print("[RAW ARGS]", config.invocation_params.args)

    # 打印解析后的参数（包括 pytest 内置参数）
    # print("[PARSED ARGS]")
    # for key, value in config.option.__dict__.items():
    #     print(f"  {key}: {value}")

    # 获取所有参数
    env = config.getoption("--env")
    tags = config.getoption("--tags").split(',') if config.getoption("--tags") else []
    verbose = config.getoption("--verbose")

    print(f"当前环境: {env}")
    print(f"过滤标签: {tags}")
    print(f"详细模式: {verbose}")


def pytest_addoption(parser):
    # 添加 --env 参数（选项限制为 prod/stage）
    parser.addoption(
        "--env",
        action="store",
        default="prod",
        choices=["prod", "stage"],
        help="Environment to run tests: prod or stage"
    )

    # 添加 --tags 参数（逗号分割的字符串）
    parser.addoption(
        "--tags",
        action="store",
        default="",
        help="Comma-separated list of tags (e.g., 'smoke,regression')"
    )
