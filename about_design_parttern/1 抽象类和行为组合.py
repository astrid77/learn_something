#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/5/25 15:26


from abc import ABCMeta, abstractmethod


# 1. 定义飞行行为接口（策略模式核心）
class FlyBehavior(metaclass=ABCMeta):
    @abstractmethod
    def fly(self, name: str):
        pass


# 具体飞行行为实现
class FlyWithWings(FlyBehavior):
    def fly(self, name: str):
        print(f'{name}通过翅膀飞行')


class FlyNoWay(FlyBehavior):
    def fly(self, name: str):
        print(f'{name}不能飞行')


# 2. 正确定义鸭子抽象基类
class Duck(metaclass=ABCMeta):
    def __init__(self, name: str = "鸭子"):
        self.name = name
        self.fly_behavior = None  # 行为组合而非继承

    # 强制子类必须实现的方法
    @abstractmethod
    def display(self):
        pass

    # 通用方法可直接实现
    def swim(self):
        print(f"{self.name}正在游泳")

    # 委托给行为对象
    def perform_fly(self):
        if self.fly_behavior:
            self.fly_behavior.fly(self.name)
        else:
            raise ValueError("未设置飞行行为")


# 3. 具体鸭子类型实现
class MallardDuck(Duck):
    def __init__(self, name="绿头鸭"):
        super().__init__(name)
        self.fly_behavior = FlyWithWings()

    def display(self):
        print(f"我是{self.name}, 头是绿色的")


class RubberDuck(Duck):
    def __init__(self, name="橡皮鸭"):
        super().__init__(name)
        self.fly_behavior = FlyNoWay()

    def display(self):
        print(f"我是{self.name}, 黄颜色的橡皮鸭")


# 4. 动态修改行为能力
class DynamicDuck(Duck):
    def __init__(self, name="可变鸭"):
        super().__init__(name)
        self.fly_behavior = FlyNoWay()

    def display(self):
        print(f"我是{self.name}, 飞行能力可动态修改")

    def set_fly_behavior(self, behavior: FlyBehavior):
        self.fly_behavior = behavior


if __name__ == '__main__':
    # 标准鸭子
    mallard = MallardDuck()
    mallard.display()
    mallard.perform_fly()

    # 不会飞的鸭子
    rubber_duck = RubberDuck()
    rubber_duck.display()
    rubber_duck.perform_fly()

    # 动态修改行为的鸭子
    dynamic_duck = DynamicDuck("变身鸭")
    dynamic_duck.perform_fly()  # 初始不能飞

    # 动态添加飞行能力
    dynamic_duck.set_fly_behavior(FlyWithWings())
    dynamic_duck.perform_fly()  # 现在能飞了

    ducks: list[Duck] = [mallard, rubber_duck, dynamic_duck]

    for d in ducks:
        print("")
        d.display()
        d.perform_fly()
