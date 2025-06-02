#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/5/31 13:53
from abc import ABC, abstractmethod
from typing import Optional


class FlyBehavior:
    """飞行行为"""

    def fly(self):
        raise NotImplementedError


class FlyWithWings(FlyBehavior):
    """用翅膀飞行"""

    def fly(self):
        print("I'm flying!!")


class FlyNoWay(FlyBehavior):
    """不支持飞行"""

    def fly(self):
        print("I can't fly")


class QuackBehavior(ABC):
    """发出声音行为"""

    @abstractmethod
    def quack(self):
        pass


class Quack(QuackBehavior):

    def quack(self):
        print('鸭子呱呱叫')


class Squeak(QuackBehavior):

    def quack(self):
        print('橡皮鸭子呱呱叫')


class MuteQuack(QuackBehavior):

    def quack(self):
        print('不会叫')


class Duck:

    def __init__(self,
                 fly_behavior: Optional[FlyBehavior] = None,
                 quack_behavior: Optional[QuackBehavior] = None
                 ):
        self._fly_behavior = fly_behavior
        self._quack_behavior = quack_behavior

    def perform_fly(self):
        if self.fly_behavior:
            self.fly_behavior.fly()

    def perform_quack(self):
        if self.quack_behavior:
            self.quack_behavior.quack()

    def swim(self):
        pass

    @abstractmethod
    def display(self):
        pass

    # def set_fly_behavior(self, fly_behavior: FlyBehavior):
    #     self.fly_behavior = fly_behavior
    #
    # def set_quack_behavior(self, quack_behavior: QuackBehavior):
    #     self.quack_behavior = quack_behavior

    @property
    def fly_behavior(self):
        return self._fly_behavior

    @fly_behavior.setter
    def fly_behavior(self, fly_behavior: FlyBehavior):
        self._fly_behavior = fly_behavior

    @property
    def quack_behavior(self):
        return self._quack_behavior

    @quack_behavior.setter
    def quack_behavior(self, quack_behavior: QuackBehavior):
        self._quack_behavior = quack_behavior


class MallardDuck(Duck):  # 继承，属于鸭子 IS-A，是一种鸭子的子类型

    def __init__(self):
        super().__init__()
        self.fly_behavior = FlyWithWings()  # 组合，拥有飞行行为 HAS-A
        self.quack_behavior = Quack()  # 组合，拥有发出声音行为 HAS-A

    def display(self):
        print("I'm a real Mallard Duck")


class ModelDuck(Duck):

    def __init__(self):
        super().__init__()
        self.fly_behavior = FlyNoWay()
        self.quack_behavior = Quack()

    def display(self):
        print("I'm a model duck")


class FlyRocketPowered(FlyBehavior):
    """利用火箭动力的飞行行为"""

    def fly(self):
        print("I'm flying with a rocket!")


if __name__ == '__main__':
    mallard = MallardDuck()
    mallard.perform_quack()
    mallard.perform_fly()

    model = ModelDuck()
    model.perform_fly()
    model.fly_behavior = FlyRocketPowered()
    # model.set_fly_behavior(FlyRocketPowered())
    model.perform_fly()
