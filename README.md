# learn_something
## Python(/about_python)
### 装饰器(decorator)

1. 实现一个装饰器，打印函数的输入参数和返回值。
2. 实现一个装饰器，限制函数每秒最多调用1次（简单版限流）。
3. 实现一个缓存装饰器 @cache_if_positive，仅当函数的所有参数为正数时才缓存结果，否则每次调用都执行函数。
4. 超时重试装饰器：
<br>编写一个装饰器@retry_on_timeout(max_retries=3, timeout=2)，当函数执行时间超过timeout秒时自动重试，最多重试max_retries次，全部失败后抛出TimeoutError。
5. 装饰器类实现日志
<br>用类（而非函数）实现一个装饰器@Logger(prefix="DEBUG:")，在函数调用前后打印带prefix的日志（如DEBUG: Function foo started）。
6. 动态权限检查
<br>设计一个装饰器@require_role(role)，根据动态配置（如全局变量或外部函数get_current_role()）检查当前用户角色是否匹配role，否则抛出权限错误。
7. 异步函数超时装饰器
<br>为异步函数编写一个装饰器@async_timeout(seconds)，如果协程执行超过seconds秒，则强制取消任务并抛出asyncio.TimeoutError。
8. 装饰器堆叠依赖
<br>实现一个装饰器@depends_on(*dependencies)，确保被装饰函数仅在所有dependencies（其他函数）都已被调用至少一次后才允许执行，否则抛出DependencyError。
9. 元类+装饰器联动
<br>创建一个装饰器@register_plugin，将被装饰类自动注册到全局插件系统中（通过元类实现），同时确保装饰器可以叠加在其他装饰器之上而不破坏元类逻辑。
10. 测试数据处理
<br>编写一个函数process_test_results(results_str)，接收一个字符串results_str，格式为"用例1:通过,用例2:失败,用例3:通过..."
11. 测试框架基类设计
12. 测试失败重试
<br>编写带参数的装饰器@retry(max_attempts, exceptions)
13. 实现最基本的参数循环执行能力
14. 实现真正的参数化测试用例分离
15. pytest参数化用例执行灵活使用超时重试装饰器

### 元类(meta)

- 练习 1：强制类名规范
- 练习 2：自动添加版本号
- 练习 3：收集测试方法
- 练习 4：统计测试用例数量
- 练习 5：单例测试基类
- 练习 6：动态生成测试方法
- 练习 7：测试用例装饰器
- 练习 8：测试依赖管理
- 练习 9：简易测试框架
- 练习 10：模仿 pytest 的标记系统

### 生成器(generator)

1. 创建一个生成器函数，生成1到10000的整数，每次生成平方值
2. 用Faker创建生成测试数据的生成器
3. 对比生成器与列表推导式的内存消耗
4. 优化大数据生成过程
5. 生成1GB测试数据文件

### YAML

1. 实现基础YAML配置加载器
2. 实现嵌套配置项访问
3. 实现环境配置加载
4. 环境叠加+嵌套访问
5. 实现配置项类型校验
6. 实现环境变量覆盖

## pytest

### pytest_addoption

1. pytest 参数机制，自定义装置：使用request.config.getoption获取参数
2. pytest 参数机制，自定义装置：使用pytestconfig.getoption获取参数
3. pytest 参数机制，自定义装置：结合pytest.ini获取参数

### pytest_collection_modifyitems

1. 根据标签跳过特定环境用例
2. 根据 `--tags=...` 的参数查找标签，执行对应用例，实现标签交集/并集过滤

### hooks

1. 多个hooks函数简单使用示例

### plugins

1. 插件开发基础（示例：计时插件）
2. 控制多个插件的执行顺序