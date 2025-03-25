# 2、实现一个装饰器，限制函数每秒最多调用1次（简单版限流）。
import functools
import random
import time

# 将上次请求时间设置为全局变量
# request_time = 0


def limit_request_freq(func):
    # 将上次请求时间设置为装饰器局部变量
    request_time = 0

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 此处相对应的用非全局或者全局变量都行
        nonlocal request_time
        now = time.time()
        if request_time and now - request_time < 1:
            raise RuntimeError("请求频率受限，请稍后再试～")
        request_time = now
        return func(*args, **kwargs)

    return wrapper


@limit_request_freq
def add(x, y, a=1, b=2):
    return x + y + a + b


for i in range(10):
    time.sleep(random.random())
    try:
        print(add(i, i + 1, i + 2))
    except RuntimeError as e:
        print(e)
