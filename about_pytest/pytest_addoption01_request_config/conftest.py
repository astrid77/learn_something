#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/5/11 17:42

import pytest


def pytest_addoption(parser):
    parser.addoption("--timeout", type=int, default=None, help="超时时间（秒）")


@pytest.fixture(scope="session")
def timeout(request):
    cmd_timeout = request.config.getoption("--timeout")
    return cmd_timeout
