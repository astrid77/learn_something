# 1、实现一个装饰器，打印函数的输入参数和返回值
import functools


def print_input_output(func):
    """打印输入输出的装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        input_list = []
        input_list.extend([f"{x}" for x in args])
        input_list.extend(f"{x}={y}" for x, y in kwargs.items())

        input_to_str = ",".join(input_list)
        print(f"{func.__name__}函数的输入参数为：({input_to_str})")
        output = func(*args, **kwargs)
        print(f"{func.__name__}函数的返回值为：{output}")
        return output

    return wrapper


@print_input_output
def add(x, y, a=1, b=2):
    return x + y + a + b


add(11, 22)
add(1, 2, a=3, b=4)

"""运行结果：
add函数的输入参数为：(11,22)
add函数的返回值为：36
add函数的输入参数为：(1,2,a=3,b=4)
add函数的返回值为：10
"""
