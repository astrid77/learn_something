#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/5/17 15:11

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev", help="Environment: dev/stage/prod")


def pytest_configure(config):
    print(f">>> 当前环境: {config.getoption('--env')}")


def pytest_collection_modifyitems(items):
    # 反转测试顺序
    items.reverse()


def pytest_collectstart(collector):
    print(f"开始收集: {collector.nodeid}")


def pytest_runtest_setup(item):
    print(f"准备运行: {item.nodeid}")


def pytest_runtest_teardown(item):
    print(f"清理: {item.nodeid}")


def pytest_terminal_summary(terminalreporter):
    if 'passed' in terminalreporter.stats:
        print(f"通过测试数: {len(terminalreporter.stats['passed'])}")


def pytest_unconfigure(config):
    print(">>> 测试结束，释放资源")

"""pytest --env=dev -rs -s

>>> 当前环境: dev
========================================================================== test session starts ==========================================================================
platform darwin -- Python 3.9.6, pytest-8.3.5, pluggy-1.5.0
rootdir: .../hooks01_example
configfile: pytest.ini
collecting ... 开始收集: 
开始收集: .
开始收集: test_demo.py
collected 3 items                                                                                                                                                       

test_demo.py 准备运行: test_demo.py::test_add2[3-6-9]
.清理: test_demo.py::test_add2[3-6-9]
准备运行: test_demo.py::test_add1[2-3-5]
.清理: test_demo.py::test_add1[2-3-5]
准备运行: test_demo.py::test_add[1-2-3]
.清理: test_demo.py::test_add[1-2-3]

通过测试数: 3

=========================================================================== 3 passed in 0.01s ===========================================================================
>>> 测试结束，释放资源

"""