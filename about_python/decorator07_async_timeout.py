#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/3/29 下午2:39

# 异步函数超时装饰器
# 为异步函数编写一个装饰器@async_timeout(seconds),
# 如果协程执行超过seconds秒，则强制取消任务并抛出asyncio.TimeoutError。
import asyncio
import functools
import random


def async_timeout(seconds=5):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            task = asyncio.create_task(func(*args, **kwargs))
            try:
                return await asyncio.wait_for(task, seconds)
            except asyncio.TimeoutError:
                raise asyncio.TimeoutError("运行超时!!")

        return wrapper

    return decorator


@async_timeout()
async def test():
    t = random.randint(1, 10)
    print(f"预计运行时间{t}秒...", end=" ")
    await asyncio.sleep(t)
    print("run returned.")
    return


async def main():
    try:
        await test()
    except Exception as e:
        print(e)


for _ in range(10):
    asyncio.run(main())

"""运行结果：（随机）
预计运行时间4秒... run returned.
预计运行时间4秒... run returned.
预计运行时间8秒... 运行超时!!
预计运行时间1秒... run returned.
预计运行时间7秒... 运行超时!!
预计运行时间9秒... 运行超时!!
预计运行时间6秒... 运行超时!!
预计运行时间3秒... run returned.
预计运行时间3秒... run returned.
预计运行时间7秒... 运行超时!!
"""
