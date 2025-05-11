学习资料： https://pytest.cn/en/8.2.x/how-to/usage.html

# 测试文件发现规则

pytest 将运行当前目录及其子目录中所有形式为 `test_*.py` 或 `*_test.py` 的文件.

如果没有指定参数，则从 testpaths（如果已配置）或当前目录开始收集。或者，可以在目录、文件名或节点 ID 的任意组合中使用命令行参数。
<br>递归进入目录，除非它们与 norecursedirs 匹配。
<br>在这些目录中，搜索 test_*.py 或 *_test.py 文件，由其 测试包名称 导入。
<br>从这些文件中收集测试项：
- test 前缀的测试函数或类外的测试方法。
- test 前缀的测试函数或 Test 前缀的测试类中的测试方法（没有 `__init__` 方法）。装饰有 @staticmethod 和 @classmethods 的方法也被考虑在内。

测试方法在类中时，请确保使用 Test 为你的类添加前缀，否则该类将被跳过。

在 Python 模块中，pytest 还使用标准 `unittest.TestCase` 子类化技术来发现测试。

# 运行pytest

在模块中运行测试 `pytest test_mod.py`

在目录中运行测试 `pytest testing/`

按关键字表达式运行测试 `pytest -k 'MyClass and not method'`(在 Windows 上运行此命令时，请在表达式中使用 "" 而不是 '')

`pytest -q test_sysexit.py` 

`-q/--quiet` 标志在此示例和后续示例中保持输出简短。


## 按收集参数运行测试

传递相对于工作目录的模块文件名，后跟使用 :: 字符分隔的类名和函数名等说明符，以及用 [] 括起来的来自参数化的参数。

- 要在模块中运行特定测试
<br>pytest tests/test_mod.py::test_func
- 要在类中运行所有测试
<br>pytest tests/test_mod.py::TestClass
- 指定特定测试方法
<br>pytest tests/test_mod.py::TestClass::test_method
- 指定测试的特定参数化
<br>pytest tests/test_mod.py::test_func[x1,y2]
- 按标记表达式运行测试（将运行用 @pytest.mark.slow 装饰器装饰的所有测试）
<br>pytest -m slow
- 从包中运行测试
<br>pytest --pyargs pkg.testing
- 从文件中读取参数：可以使用 @ 前缀从文件中读取上述所有内容
<br>`pytest @tests_to_run.txt` (可以使用 `pytest --collect-only -q` 生成此文件)，文件示例如下：
    ```bash
    tests/test_file.py
    tests/test_mod.py::test_func[x1,y2]
    tests/test_mod.py::TestClass
    -m slow
    ```
- 通过 python -m pytest 调用 pytest
<br>这几乎等同于直接调用命令行脚本 pytest [...]，除了通过 python 调用还会将当前目录添加到 sys.path 中。
- 从 Python 代码调用 pytest
<br>`retcode = pytest.main()`
或者
`retcode = pytest.main(["-x", "mytestdir"])`

## 其他常用命令

- `-s` 显示所有测试中的输出（如 print()），不加该命令时，测试通过时不显示 print() 内容
- `--tb` 是 traceback 的缩写，控制测试失败时的错误回溯信息显示方式
    - `--tb=no` 表示完全不显示错误回溯信息。
    - `--tb=auto`（默认）：显示简化的回溯。
    - `--tb=long`：显示完整的详细回溯。
    - `--tb=short`：显示较短的回溯。
    - `--tb=line`：每个失败仅显示一行摘要。
- `--collect-only` 让 pytest 收集并列出所有可被发现的测试项，但不会真正执行这些测试
    - 添加 -v 参数显示更详细信息，`pytest --collect-only -v`
- `-v` 查看测试用例的完整名称，通常用于查看使用 ids 关键字参数自定义在测试 ID 中用于特定固定装置值的字符串
`@pytest.fixture(params=[0, 1], ids=["spam", "ham"])`
- `-r` 在测试会话结束后生成一个结果摘要报告
    - `-rs`是组合参数，s 是 -r 的参数，表示只显示 跳过的测试（skipped tests） 的详细信息
    - 常用参数：E(Error) F(Failure) s(Skipped) x(XFAIL) X(XPASS) p(Passed) a(All except passed) A(All)
- `--lf`、`--last-failed` - 仅重新运行失败项。
- `--ff`、`--failed-first` - 先运行失败项，然后再运行其余测试。
- `--cache-clear` 选项允许在测试运行之前移除所有跨会话缓存内容（通常不需要）。
- `--lfnf/--last-failed-no-failures` 选项控制 `--last-failed` 的行为。确定上次运行中没有测试失败时的行为。
	有两个选项：
	- `all`：当没有已知的测试失败时，运行所有测试（完整的测试套件）。这是默认设置。
	- `none`：当没有已知的测试失败时，仅发出一个消息，说明这一点，然后成功退出。

	示例：
	```bash
	pytest --last-failed --last-failed-no-failures all    # runs the full test suite (default behavior)
	pytest --last-failed --last-failed-no-failures none   # runs no tests and exits successfully
	```
- `--cache-show` 命令行选项查看缓存的内容
- `--cache-clear` 选项来指示 pytest 清除所有缓存文件和值
- `--sw`、`--stepwise` 逐步运行，测试套件将运行到第一次失败，然后停止。在下次调用时，测试将从上次失败的测试继续，然后运行到下一个失败的测试。
- `--stepwise-skip` 选项忽略一个失败的测试，而是在第二个失败的测试上停止测试执行。提供 `--stepwise-skip` 也将隐式启用 `--stepwise`。

## 管理日志记录
pytest 自动捕获级别为 `WARNING` 或以上的日志消息，并以与捕获的 stdout 和 stderr 相同的方式在每个失败测试的单独部分中显示它们。
默认情况下，每个捕获的日志消息都会显示模块、行号、日志级别和消息。

如果需要，可以通过传递特定的格式化选项来将日志和日期格式指定为日志记录模块支持的任何内容
`pytest --log-format="%(asctime)s %(levelname)s %(message)s" \
        --log-date-format="%Y-%m-%d %H:%M:%S"`

这些选项还可以通过 `pytest.ini` 文件进行自定义
```text
[pytest]
log_format = %(asctime)s %(levelname)s %(message)s
log_date_format = %Y-%m-%d %H:%M:%S
```

可以通过 `--log-disable={logger_name}` 禁用特定的日志记录器。此参数可以传递多次`pytest --log-disable=main --log-disable=testing`

还可以使用以下方法完全禁用对失败测试中捕获的内容（stdout、stderr 和日志）的报告 `pytest --show-capture=no`

# 断言

pytest 允许您使用标准 Python assert 来验证 Python 测试中的预期和值。

## 关于预期异常的断言

为了编写关于引发异常的断言，您可以使用 pytest.raises() 作为上下文管理器。

```python
import pytest


with pytest.raises(ZeroDivisionError) as excinfo:
    1 / 0
assert excinfo.value
assert excinfo.type is ZeroDivisionError
```
excinfo 是 ExceptionInfo 实例，它是对实际引发异常的包装。主要关注的属性是 .type、.value 和 .traceback。

**匹配异常消息**

你可以将 match 关键字参数传递给上下文管理器，以测试正则表达式是否与异常的字符串表示形式匹配
`pytest.raises(ValueError, match=r".* 123 .*")`

**匹配异常组**

可以使用 excinfo.group_contains() 方法来测试作为 ExceptionGroup 一部分返回的异常。

如果你只想匹配特定级别的异常，你可以指定一个 depth 关键字参数；直接包含在顶级 ExceptionGroup 中的异常将匹配 depth=1。

```python
import pytest


def test_exception_in_group_at_given_depth():
    with pytest.raises(ExceptionGroup) as excinfo:
        raise ExceptionGroup(
            "Group message",
            [
                RuntimeError(),
                ExceptionGroup(
                    "Nested group",
                    [
                        TypeError(),
                    ],
                ),
            ],
        )
    assert excinfo.group_contains(RuntimeError, depth=1)
    assert excinfo.group_contains(TypeError, depth=2)
    assert not excinfo.group_contains(RuntimeError, depth=2)
    assert not excinfo.group_contains(TypeError, depth=1)
```

### 为失败断言定义您自己的解释

通过实现 pytest_assertrepr_compare 钩子，为失败断言定义您自己的解释。

```python
from test_foocompare import Foo


def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, Foo) and isinstance(right, Foo) and op == "==":
        return [
            "Comparing Foo instances:",
            f"   vals: {left.val} != {right.val}",
        ]
```

# fixture

## 基本语法

使用 @pytest.fixture 装饰器定义 fixture：
```python
import pytest

@pytest.fixture
def my_fixture():
    # 初始化资源（setup）
    data = "Hello, pytest!"
    yield data  # 返回数据给测试用例
    # 清理资源（teardown）
    print("资源清理完成")

def test_example(my_fixture):
    assert my_fixture == "Hello, pytest!"
```

fixture 可以依赖其他 fixture，测试用例可以传递多个 fixture。

## 常用参数

1. **scope**
<br>作用：定义 fixture 的生命周期作用域，控制其初始化和清理的频率。
<br>可选值：
    - "function"（默认）：每个测试函数执行一次。
    - "class"：每个测试类执行一次。
    - "module"：每个模块（文件）执行一次。
    - "session"：整个测试会话（所有测试）执行一次。
2. **params**
<br>作用：参数化 fixture，生成多组测试数据。
<br>使用场景：为依赖该 fixture 的测试函数生成多组参数化用例。
3. **autouse**
<br>作用：自动应用 fixture，无需在测试函数中显式声明。
<br>使用场景：全局配置（如日志初始化、临时目录创建）。
4. **ids**
<br>作用：为参数化 fixture 的每组参数生成可读的标识符。
<br>使用场景：提升测试报告的可读性。
5. **name**
<br>作用：重命名 fixture，解决命名冲突或简化调用名称。
<br>使用场景：当 fixture 函数名与测试参数名冲突时。

## 生命周期管理

- 作用域默认function（作用域优先级：session > module > class > function）
- Setup/Teardown 逻辑：使用 yield 分离初始化与清理 或者 通过 request.addfinalizer() 注册清理函数

## 查看 Fixture 执行顺序

可以通过 `pytest --setup-show <测试文件>` 命令查看 详细的 SETUP/TEARDOWN 顺序，如：`pytest --setup-show pytest01_study_notes.py`

```text
SETUP    S _session_faker
        SETUP    F mail_admin
        SETUP    F receiving_user (fixtures used: mail_admin)
        SETUP    F sending_user (fixtures used: mail_admin)
        SETUP    F email (fixtures used: receiving_user, sending_user)
        pytest01_study_notes.py::test_email_received (fixtures used: _session_faker, email, mail_admin, receiving_user, request, sending_user).
        TEARDOWN F email
        TEARDOWN F sending_user
        TEARDOWN F receiving_user
        TEARDOWN F mail_admin
TEARDOWN S _session_faker
```
其中，参数列表顺序无关：在测试用例的 (fixtures used: ...) 列表中，fixture 的声明顺序可能是字母顺序或代码中定义的顺序，与实际的 SETUP 顺序无关。

## fixture(夹具)执行顺序

1. **作用域层级**：更大作用域的 fixture 优先初始化，因为它们需要被多个小作用域共享
2. **依赖优先**：如果一个 fixture 依赖其他 fixture，被依赖的 fixture 会优先初始化
3. **声明顺序**：若多个 fixture 无依赖关系且作用域相同，则按它们在测试函数参数或依赖链中的声明顺序初始化
4. **LIFO 原则**：清理时 TEARDOWN 顺序与 初始化 SETUP 顺序相反，最小作用域的优先清理

## 内置fixture

### request

提供对测试用例或 fixture 的上下文信息的访问能力

**常用属性**：

- request.node: 当前测试用例的节点对象（如函数、类）。
    - 通过 request.node.get_closest_marker 获取测试用例的标记（如 @pytest.mark.slow）
- request.function: 当前测试函数对象。
- request.cls: 当前测试类对象（如果测试在类中）。
- request.module: 当前测试所在的模块对象。
    - `request.module.__name__`
- request.config: pytest 的全局配置对象。
    - 通过 request.config.getoption 或 request.config.getini 获取 pytest 命令行或配置文件中的参数
    ```python
    base_url = request.config.getoption("--base-url")  # 获取命令行参数，pytest --base-url=http://api.example.com test_demo.py
    ```
- request.param: 获取其他 fixture 的参数或动态生成的配置值.

**常用方法**:

- 通过 request.addfinalizer() 或 request.addcleanup() 注册清理函数.
  ```text
  addfinalizer vs addcleanup：
  addfinalizer: 严格遵循 LIFO（后进先出）顺序执行。
  addcleanup: 在测试结束后按注册顺序执行，且即使前面的清理函数抛出异常，后续清理函数仍会执行。
  ```

## tmp_path
可以使用 tmp_path 固定装置，它将为每个测试函数提供一个唯一的临时目录（类型为 pathlib.Path），测试结束后自动清理。

```python
def test_create_file(tmp_path):
    # 创建子目录
    sub_dir = tmp_path / "sub"
    sub_dir.mkdir()
    
    # 创建文件并写入内容
    file_path = sub_dir / "test.txt"
    file_path.write_text("Hello pytest!")
	
	# 检查文件是否存在
	assert file_path.exists()
    
    # 读取文件内容并验证
    assert file_path.read_text() == "Hello pytest!"
```

默认情况下，pytest 为最近 3 次 pytest 调用保留临时目录。

临时目录创建为系统临时目录的子目录。基本名称将为 `pytest-NUM`，其中 NUM 将随着每次测试运行而递增。默认情况下，将删除超过 3 个临时目录的条目。此行为可以通过 `pytest.ini` 文件中 `[pytest]` 下的 `tmp_path_retention_count` 和 `tmp_path_retention_policy` 进行配置。

使用 `--basetemp` 选项将在每次运行之前删除目录，实际上意味着只保留最近一次运行的临时目录。
可以按如下方式覆盖默认临时目录设置 `pytest --basetemp=mydir`

## tmp_path_factory 

tmp_path_factory 是一个会话作用域固定装置，可用于从任何其他固定装置或测试创建任意临时目录。

若需在多个测试间共享临时目录，使用 tmp_path_factory 并指定作用域：
```python
@pytest.fixture(scope="module")
def shared_temp_dir(tmp_path_factory):
    # 创建模块级别的临时目录
    return tmp_path_factory.mktemp("shared_data")

def test_shared_1(shared_temp_dir):
    file = shared_temp_dir / "data.txt"
    file.write_text("test data")

def test_shared_2(shared_temp_dir):
    file = shared_temp_dir / "data.txt"
    assert file.read_text() == "test data"
```

注意：共享目录会绕过测试隔离，需谨慎使用。

## caplog
更改捕获的日志消息的日志级别.
```python
def test_foo(caplog):
    caplog.set_level(logging.CRITICAL, logger="root.baz")
```

可以使用以下方法更改任何日志记录器的级别
```python
def test_bar(caplog):
    with caplog.at_level(logging.CRITICAL, logger="root.baz"):
        pass
```

当您想要断言消息的内容时，遍历`caplog.records`
```python
def test_baz(caplog):
    func_under_test()
    for record in caplog.records:
        assert record.levelname != "CRITICAL"
    assert "wally" not in caplog.text
```
caplog.records 属性仅包含当前阶段的记录，因此在 setup 阶段中，它仅包含设置日志，与 call 和 teardown 阶段相同。
要访问其他阶段的日志，请使用 `caplog.get_records(when)` 方法。
```python
@pytest.fixture
def window(caplog):
    window = create_window()
    yield window
    for when in ("setup", "call"):
        messages = [
            x.message for x in caplog.get_records(when) if x.levelno == logging.WARNING
        ]
        if messages:
            pytest.fail(f"warning messages encountered during testing: {messages}")
```

如果您只想确保在给定的日志记录器名称下使用给定的严重性和消息记录了某些消息，还可以使用 record_tuples
```python
def test_foo(caplog):
    logging.getLogger().info("boo %s", "arg")

    assert caplog.record_tuples == [("root", logging.INFO, "boo arg")]
```
还可以调用 `caplog.clear()` 来重置测试中捕获的日志记录

## 其他

### pytest.param()

`pytest.param()` 是一个包装函数，用于为参数化的值添加额外信息。它的核心语法是：
```python
pytest.param(value, marks=..., id=...)
```
- value: 参数值（可以是单个值或元组）。
- marks: 要应用的标记（如 pytest.mark.skip、pytest.mark.xfail）。
- id: 自定义标识符（覆盖默认的测试用例名称）。

**在 @pytest.mark.parametrize 中的用法**

为当前包含的测试用例的每组参数附加标记。

**在参数化夹具（Fixture）中的用法**

为夹具的每组参数附加标记，这些标记会传递给所有依赖该夹具的测试用例。

### pytest.mark

pytest.mark 是 Pytest 中用于标记测试用例的工具，可以通过标签对测试进行分类、过滤或附加特殊行为。

#### 注册标记

1、第一种：**pytest.ini 配置文件中注册**

当传递 --strict-markers 命令行标志时，使用 @pytest.mark.name_of_the_mark 装饰器应用的任何未知标记都将触发错误.

```ini
[pytest]
addopts = --strict-markers
markers =
    slow: 标记为耗时较长的测试
    ui: 用户界面相关测试
    smoke: 冒烟测试
    custom_marker: 其他自定义标记
```

`@pytest.mark.slow` 标记测试用例或者测试类

`pytest -m slow` 命令行运行指定标记的测试
```bash
# 运行所有标记为 "slow" 的测试
pytest -m slow

# 运行所有未标记为 "slow" 的测试
pytest -m "not slow"

# 同时选择多个标记（AND 逻辑）
pytest -m "slow and ui"

# 运行标记为 "smoke" 或 "ui" 的测试（OR 逻辑）
pytest -m "smoke or ui"
```

2、第二种：**在 pyproject.toml 文件中注册自定义标记**

```text
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "serial",
]
```

3、第三种：**在 pytest_configure 钩子中以编程方式注册新标记**

```python
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "env(name): mark test to run only on named environment"
    )
```

#### 内置常用标记

- 跳过测试 `@pytest.mark.skip(reason="功能未实现")`
- 条件跳过 `@pytest.mark.skipif(sys.version_info < (3, 8), reason="需要 Python 3.8 或更高版本")`
- 预期失败 `@pytest.mark.xfail(reason="已知问题，待修复")`
- 参数化 `@pytest.mark.parametrize("a, b, expected", [(1, 2, 3), (4, 5, 9)])`
可以在类或模块上使用参数化标记，可以堆叠 parametrize 装饰器

**注意事项**

- **类级标记**：类的标记会被所有方法继承。
- **多重标记**：一个测试可以同时有多个标记。
- **标记唯一性**：避免使用重复或易混淆的标记名称。
- **配置验证**：运行前检查 pytest.ini 是否正确注册自定义标记。
- **版本兼容性**：确保 Pytest 版本 ≥ 3.6（旧版本语法可能不同）。

#### @pytest.mark.usefixtures(...)

`@pytest.mark.usefixtures(...)` 是 Pytest 中用于在测试类或模块级别自动应用 Fixture 的装饰器，它允许你不必在每个测试函数中显式声明 Fixture 参数，而是直接复用预定义的 Fixture 逻辑

**注意事项**

- 返回值不可见：若需使用 Fixture 返回的对象，仍需通过参数传递。
- 执行顺序：多个 Fixture 按声明顺序执行。
- 避免滥用：过度使用可能导致测试逻辑不直观。

### pytestmark

可以在 测试模块 中的全局级别声明，以将一个或多个 标记 应用于所有测试函数和方法。可以是单个标记或标记列表（按从左到右的顺序应用）。

```python
import pytest

pytestmark = pytest.mark.webtest
# 或者
# pytestmark = [pytest.mark.integration, pytest.mark.slow]
# 或者
# pytestmark = pytest.mark.usefixtures("cleandir")
```

或者所有测试所需的固定装置放入 ini 文件中（在项目根目录下创建 pytest.ini 文件，添加自定义配置项（需放在 `[pytest]` 区块下））

```ini
# content of pytest.ini
[pytest]
usefixtures = cleandir
```

**警告**

请注意，此标记在固定装置函数中不起作用。例如，这不会按预期工作
```python
@pytest.mark.usefixtures("my_other_fixture")
@pytest.fixture
def my_fixture_that_sadly_wont_use_my_other_fixture(): ...
```

### pytest_plugins

可以在 测试模块 和 conftest.py 文件 中的全局级别声明，以注册其他插件。可以是 str 或 Sequence[str]。
比如：如果您想使用不使用入口点的项目的 fixture，则可以在顶部 conftest.py 文件中定义 pytest_plugins 以将该模块注册为插件。

```python
pytest_plugins = "myapp.testsupport.myplugin"
# 或者
# pytest_plugins = ("myapp.testsupport.tools", "myapp.testsupport.regression")
```

### pytest.ini配置文件

pytest.ini 配置示例如下：

```text
[pytest]
addopts = -v --cov=src --cov-report=term-missing
testpaths = tests
markers =
    slow: mark test as slow-running
    integration: integration test
filterwarnings =
    ignore::DeprecationWarning
log_cli = true
log_level = INFO
```

使用 pytestconfig 内置 fixture 获取 pytest.ini 中的配置

```python
@pytest.fixture(scope="session")
def db_connection(pytestconfig):
    # 从 pytest.ini 读取配置
    db_host = pytestconfig.getini("db_host")
```

`pytest --help`  # 查看addopts是否生效
`pytest --markers`  # 查看注册的标记

**注意事项**：

在pytest中使用`pytest.ini`文件进行配置可以显著提升测试管理的效率和一致性。以下是关键注意事项及使用方式的总结：

1. **文件位置**  
   `pytest.ini`应位于项目的**根目录**（即运行`pytest`命令的位置），确保pytest能自动识别。

2. **语法正确性**  
   - 使用`.ini`格式的节（`[section]`）和键值对。
   - 所有配置需在`[pytest]`节下，否则无效。
   - 避免拼写错误，例如`addopts`而非`addopt`。

3. **版本兼容性**  
   部分配置项可能仅支持特定pytest版本，需查阅对应版本的文档。

4. **配置优先级**  
   命令行参数 > `pytest.ini`配置。例如，命令行指定`-s`会覆盖`addopts`中的设置。

5. **编码问题**  
   文件默认使用UTF-8编码，若含非ASCII字符（如中文注释），需确保编辑器保存为UTF-8。

6. **避免多配置文件冲突**  
   若项目同时存在`tox.ini`或`setup.cfg`，需确认`[pytest]`节的配置是否被正确读取，建议统一使用`pytest.ini`。

### pytestconfig

可以使用 pytest config 对象设置/获取缓存值
```python
# content of test_caching.py
import pytest


def expensive_computation():
    print("running expensive computation...")


@pytest.fixture
def mydata(pytestconfig):
    val = pytestconfig.cache.get("example/value", None)  # 获取值
    if val is None:
        expensive_computation()
        val = 42
        pytestconfig.cache.set("example/value", val)  # 设置值
    return val


def test_function(mydata):
    assert mydata == 23
```

### pytest_addoption

pytest_addoption 是一个用于添加自定义命令行参数的钩子函数

- pytest_addoption 会在 pytest 启动时 的初始化阶段被调用
- pytest_addoption 必须定义在 conftest.py 或 插件文件 中，才能被 pytest 发现。
- 命令行参数 > pytest.ini 配置 > 代码中的默认值

# 名词解释

**固定装置**在 pytest 中通常指的是 `@pytest.fixture` 装饰器，而由它标记的函数被称为 **夹具（Fixture）**

`@pytest.fixture` 装饰器 + 被装饰的函数 = 完整的夹具（Fixture）体系

