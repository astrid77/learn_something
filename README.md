# learn_something
## Python
### 装饰器练习题

- 实现一个装饰器，打印函数的输入参数和返回值。
<br>代码实现：[about_python/print_input_output.py](https://github.com/astrid77/learn_something/blob/f4ebc51687f7ad6dd12ac533f92dbcd1122998de/about_python/print_input_output.py)
- 实现一个装饰器，限制函数每秒最多调用1次（简单版限流）。
<br>代码实现：[about_python/limit_request_freq.py](https://github.com/astrid77/learn_something/blob/f4ebc51687f7ad6dd12ac533f92dbcd1122998de/about_python/limit_request_freq.py)
- 实现一个缓存装饰器 @cache_if_positive，仅当函数的所有参数为正数时才缓存结果，否则每次调用都执行函数。
<br>代码实现：[about_python/day0327_cache_if_positive.py](https://github.com/astrid77/learn_something/blob/main/about_python/day0327_cache_if_positive.py)
- 超时重试装饰器：
<br>编写一个装饰器@retry_on_timeout(max_retries=3, timeout=2)，当函数执行时间超过timeout秒时自动重试，最多重试max_retries次，全部失败后抛出TimeoutError。
<br>代码实现：[about_python/day0327_retry_on_timeout.py](https://github.com/astrid77/learn_something/blob/main/about_python/day0327_retry_on_timeout.py)
- 装饰器类实现日志
<br>用类（而非函数）实现一个装饰器@Logger(prefix="DEBUG:")，在函数调用前后打印带prefix的日志（如DEBUG: Function foo started）。
<br>代码实现：`about_python/day0329_class_decorator.py`
- 动态权限检查
<br>设计一个装饰器@require_role(role)，根据动态配置（如全局变量或外部函数get_current_role()）检查当前用户角色是否匹配role，否则抛出权限错误。
<br>代码实现：`about_python/day0329_require_role.py`
- 异步函数超时装饰器
<br>为异步函数编写一个装饰器@async_timeout(seconds)，如果协程执行超过seconds秒，则强制取消任务并抛出asyncio.TimeoutError。
<br>代码实现：`about_python/day0329_async_timeout.py`
- 装饰器堆叠依赖
<br>实现一个装饰器@depends_on(*dependencies)，确保被装饰函数仅在所有dependencies（其他函数）都已被调用至少一次后才允许执行，否则抛出DependencyError。
<br>代码实现：`about_python/day0329_depends_on.py`
- 元类+装饰器联动
<br>创建一个装饰器@register_plugin，将被装饰类自动注册到全局插件系统中（通过元类实现），同时确保装饰器可以叠加在其他装饰器之上而不破坏元类逻辑。
<br>代码实现：`about_python/day0329_register_plugin.py`

### 综合练习

- 测试数据处理：`about_python/day0330_progress_test_results.py`
- 测试框架基类设计:`about_python/day0330_base_test_class.py`
- 测试失败重试：`about_python/day0330_test_failed_retry.py`