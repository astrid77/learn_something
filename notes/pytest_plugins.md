# pytest插件

- **内置插件**：从 pytest 的内部 `_pytest` 目录加载。
- **外部插件**：通过 setuptools 入口点 发现的模块
- **conftest.py 插件**：在测试目录中自动发现的模块

所有规范和实现都遵循 `pytest_` 前缀命名约定

## 工具启动时的插件发现顺序

`pytest` 在工具启动时按以下方式加载插件模块

1. 扫描命令行以查找 `-p no:name` 选项并阻止加载该插件(包括内置插件)
2. 加载所有内置插件
3. 扫描命令行以查找 `-p name` 选项并加载指定的插件
4. 加载所有通过 setuptools 入口点 注册的插件
5. 加载所有通过 PYTEST_PLUGINS 环境变量指定的插件
6. 加载所有“初始” `conftest.py` 文件
    - 确定测试路径：在命令行上指定，否则在 testpaths 中指定（如果已定义并且从 rootdir 运行），否则在当前目录中
    - 对于每个测试路径，加载 `conftest.py` 和 `test*/conftest.py`

## 插件生命周期

---

### **一、插件加载阶段**

| 钩子函数                  | 执行时机     | 典型用途            | 执行次数 |
|-----------------------|----------|-----------------|------|
| `pytest_addoption`    | 命令行参数解析前 | 注册自定义命令行参数      | 1次   |
| `pytest_configure`    | 配置初始化完成后 | 全局配置初始化/环境检查    | 1次   |
| `pytest_sessionstart` | 测试会话开始前  | 创建全局资源（如数据库连接池） | 1次   |

---

### **二、测试收集阶段**

| 钩子函数                            | 执行时机        | 典型用途       | 执行次数 |
|---------------------------------|-------------|------------|------|
| `pytest_collection_start`       | 开始收集测试用例前   | 修改收集器行为    | 1次   |
| `pytest_generate_tests`         | 动态生成参数化测试时  | 动态创建测试用例   | 多次   |
| `pytest_make_parametrize_id`    | 参数化用例ID生成时  | 自定义参数化用例名称 | 多次   |
| `pytest_collection_modifyitems` | 收集完所有测试用例后  | 过滤/排序/标记用例 | 1次   |
| `pytest_collection_finish`      | 测试用例收集完全结束后 | 统计收集结果     | 1次   |

---

### **三、测试执行阶段**

| 钩子函数                            | 执行时机            | 典型用途      | 执行次数 |
|---------------------------------|-----------------|-----------|------|
| `pytest_runtest_protocol`       | 单个测试用例执行前后      | 自定义用例执行流程 | 每个用例 |
| `pytest_runtest_setup`          | 测试用例setup阶段前    | 前置条件检查    | 每个用例 |
| `pytest_runtest_call`           | 执行测试用例函数体时      | 替换用例执行逻辑  | 每个用例 |
| `pytest_runtest_teardown`       | 测试用例teardown阶段后 | 后置清理操作    | 每个用例 |
| `pytest_fixture_setup`          | 夹具执行前           | 监控夹具执行    | 每个夹具 |
| `pytest_fixture_post_finalizer` | 夹具清理完成后         | 检查夹具释放情况  | 每个夹具 |

---

### **四、报告与收尾阶段**

| 钩子函数                               | 执行时机      | 典型用途      | 执行次数 |
|------------------------------------|-----------|-----------|------|
| `pytest_terminal_summary`          | 终端报告生成前   | 添加自定义统计信息 | 1次   |
| `pytest_html_results_table_header` | HTML报告生成时 | 修改报告表格头   | 1次   |
| `pytest_html_results_table_row`    | HTML报告生成时 | 修改报告表格行内容 | 每个用例 |
| `pytest_sessionfinish`             | 测试会话完全结束后 | 持久化测试数据   | 1次   |
| `pytest_unconfigure`               | 配置销毁前     | 清理全局资源    | 1次   |

---

### **五、特殊场景钩子**

| 钩子函数                        | 执行时机        | 典型用途      |
|-----------------------------|-------------|-----------|
| `pytest_keyboard_interrupt` | 用户触发Ctrl+C时 | 优雅处理中断    |
| `pytest_plugin_registered`  | 新插件被注册时     | 监控插件加载顺序  |
| `pytest_warning_captured`   | 捕获到警告时      | 自定义警告处理逻辑 |

---

### **六、执行顺序可视化**

``` 
pytest启动
  ├─ pytest_addoption (注册参数)
  ├─ pytest_configure (全局配置)
  ├─ pytest_sessionstart (会话开始)
  │
  ├─ 测试收集阶段
  │   ├─ pytest_collection_start
  │   ├─ pytest_generate_tests
  │   ├─ pytest_collection_modifyitems
  │   └─ pytest_collection_finish
  │
  ├─ 测试执行阶段（循环每个用例）
  │   ├─ pytest_runtest_protocol
  │   │   ├─ pytest_runtest_setup
  │   │   ├─ pytest_runtest_call
  │   │   └─ pytest_runtest_teardown
  │   └─ pytest_fixture_setup/post_finalizer
  │
  └─ 报告与收尾
      ├─ pytest_terminal_summary
      ├─ pytest_sessionfinish
      └─ pytest_unconfigure
```

---

### **七、核心区别总结**

| **维度**   | **配置阶段钩子** | **收集阶段钩子** | **执行阶段钩子** |
|----------|------------|------------|------------|
| **执行频率** | 全局一次       | 按需触发       | 每个用例/夹具触发  |
| **典型操作** | 参数注册/环境初始化 | 用例过滤/动态生成  | 执行控制/资源管理  |
| **修改影响** | 影响整个测试会话   | 影响测试集组成    | 影响单个测试行为   |
| **错误处理** | 导致测试无法启动   | 导致用例缺失     | 导致单个测试失败   |
