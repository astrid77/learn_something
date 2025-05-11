#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/5/5 下午5:47


def test_api(base_url):
    import requests
    response = requests.get(f"{base_url}/data")
    assert response.status_code == 200

