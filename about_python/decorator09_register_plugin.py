#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/3/29 下午5:22

# 元类+装饰器联动
# 创建一个装饰器@register_plugin，将被装饰类自动注册到全局插件系统中（通过元类实现），同时确保装饰器可以叠加在其他装饰器之上而不破坏元类逻辑。
import sys
from dis import dis

PLUGINS = {}  # 全局插件注册表


class PluginMeta(type):
    """元类：自动将标记为插件的类注册到 PLUGINS"""
    __is_plugin__ = False

    def __init__(cls, name, bases, attrs):
        super(PluginMeta, cls).__init__(name, bases, attrs)

        if getattr(cls, "__is_plugin__", False):
            plugin_key = f"{cls.__module__}.{cls.__name__}"
            PLUGINS[plugin_key] = cls


def _create_mixed_meta(original_meta):
    """动态创建兼容性元类，修复 MRO 冲突"""
    # 创建新的元类，继承自 PluginMeta 和 original_meta
    return type(
        f'MixedMeta_{original_meta.__name__}',
        (PluginMeta, original_meta),
        {}
    )


def register_plugin(cls):
    """装饰器：将类标记为插件，动态处理元类兼容性"""
    # 标记该类为插件
    cls.__is_plugin__ = True
    # 获取原始元类
    original_meta = type(cls)

    # 如果已经是 PluginMeta 的实例，则直接返回
    if isinstance(cls, PluginMeta):
        return cls

    # 动态创建兼容性元类
    try:
        MixedMeta = _create_mixed_meta(original_meta)
    except TypeError:
        print("无法创建混合元类，直接替换成 PluginMeta")
        return PluginMeta(cls.__name__, cls.__bases__, dict(cls.__dict__))

    # 创建新类，继承原始基类并使用混合元类
    new_cls = MixedMeta(cls.__name__, cls.__bases__, dict(cls.__dict__))

    # 修复模块引用和名称
    new_cls.__module__ = cls.__module__
    sys.modules[cls.__module__].__dict__[cls.__name__] = new_cls

    return new_cls


def test_basic_registration():
    """基础注册功能测试"""
    global PLUGINS
    PLUGINS.clear()

    @register_plugin
    class BasicPlugin:
        pass

    key = f"{__name__}.BasicPlugin"
    assert key in PLUGINS, "插件未成功注册"
    assert PLUGINS[key].__name__ == "BasicPlugin", "类名错误"


def test_decorator_stack():
    """装饰器叠加测试"""
    global PLUGINS
    PLUGINS.clear()

    def another_decorator(cls):
        cls.custom_attr = 42
        return cls

    @another_decorator
    @register_plugin
    class StackedPlugin:
        pass

    key = f"{__name__}.StackedPlugin"
    assert key in PLUGINS, "叠加装饰器后注册失败"
    assert hasattr(StackedPlugin, "custom_attr"), "装饰器属性丢失"
    assert StackedPlugin.custom_attr == 42, "装饰器属性值错误"


def test_meta_conflict():
    """元类冲突场景测试"""
    global PLUGINS
    PLUGINS.clear()

    class CustomMeta(type):
        def __init__(cls, name, bases, attrs):
            super().__init__(name, bases, attrs)
            cls.meta_tag = "custom_meta"

    @register_plugin
    class ConflictClass(metaclass=CustomMeta):
        pass

    key = f"{__name__}.ConflictClass"
    assert key in PLUGINS, "元类冲突导致注册失败"
    assert hasattr(ConflictClass, "meta_tag"), "原始元类逻辑未执行"
    assert ConflictClass.meta_tag == "custom_meta", "元类属性错误"
    assert isinstance(ConflictClass, PluginMeta), "未正确继承插件元类"


def test_inheritance_chain():
    """继承链测试"""
    global PLUGINS
    PLUGINS.clear()

    class BaseClass:
        pass

    @register_plugin
    class ChildClass(BaseClass):
        pass

    key = f"{__name__}.ChildClass"
    assert key in PLUGINS, "继承类注册失败"
    assert issubclass(ChildClass, BaseClass), "继承关系破坏"


if __name__ == '__main__':
    test_basic_registration()
    test_decorator_stack()
    test_meta_conflict()
    dis(test_meta_conflict)
    test_inheritance_chain()
    print("所有测试通过！")
