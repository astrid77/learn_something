#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : day0329_require_role.py
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/3/29 下午1:53

# 动态权限检查
# 设计一个装饰器@require_role(role)，根据动态配置（如全局变量或外部函数get_current_role()）
# 检查当前用户角色是否匹配role，否则抛出权限错误。
import functools
import random


def get_current_role(user_id):
    # 实际场景需要根据user_id查询后返回用户角色，但这里直接随机返回一个
    roles = ["admin", "tech service", "other"]
    return random.choice(roles)


def require_role(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        role = get_current_role(user_id=args[0])
        print(role, end=": ")

        if role != "other":
            return func(*args, **kwargs)
        else:
            raise PermissionError("无权限访问！")

    return wrapper


@require_role
def test(user_id, /, *args, **kwargs):
    print(f"Hi {user_id}, run test.")
    # print(f"request params is {args} and {kwargs}.")


for i in range(10):
    try:
        test(f"10086-{i}", 1, 2, a=3, b=4)
    except Exception as e:
        print(e)

"""运行结果：（随机的）
other: 无权限访问！
other: 无权限访问！
admin: Hi 10086-2, run test.
other: 无权限访问！
tech service: Hi 10086-4, run test.
tech service: Hi 10086-5, run test.
tech service: Hi 10086-6, run test.
admin: Hi 10086-7, run test.
admin: Hi 10086-8, run test.
tech service: Hi 10086-9, run test.
"""
