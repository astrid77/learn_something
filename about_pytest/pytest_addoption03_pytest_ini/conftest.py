#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/5/5 下午5:05

import pytest


def pytest_addoption(parser):
    # 注册命令行参数 --env
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        choices=['dev', 'prod'],
        help="选择环境: dev 或 prod"
    )

    # 注册 pytest.ini 中的自定义配置项
    parser.addini(
        "dev_base_url",  # 配置项名称（与 pytest.ini 中的键名一致）
        type="string",  # 配置项类型（string, bool, args, pathlist 等）
        default="http://localhost:8001",  # 默认值（可选）
        help="开发环境的 Base URL1"
    )
    parser.addini(
        "prod_base_url",
        type="string",
        default="https://api.example1.com",
        help="生产环境的 Base URL1"
    )


@pytest.fixture(scope="session")
def base_url(request):
    env = request.config.getoption("--env")  # 获取命令行参数
    config_key = f"{env}_base_url"  # 动态拼接配置键名
    url = request.config.getini(config_key)  # 读取 pytest.ini 中的值
    return url


"""参数值优先级：命令行参数 >> pytest.ini >> pytest_addoption中addini设置的默认值"""
