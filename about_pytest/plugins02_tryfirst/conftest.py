pytest_plugins = ["plugin_d", "plugin_b", "plugin_c", "plugin_a"]

"""
钩子执行顺序优先级（从高到低）：plugin_c >> plugin_a >> plugin_d >> plugin_b
1. tryfirst=True 的钩子（按插件注册顺序）
2. 未标记优先级的钩子（按插件注册顺序）
3. trylast=True 的钩子（按插件注册顺序）
"""
