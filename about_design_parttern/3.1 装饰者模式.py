#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/6/2 11:36
from abc import ABC, abstractmethod


class Beverage(ABC):
    """饮料"""
    description = "Unknown Beverage"

    def get_description(self) -> str:
        return self.description

    @abstractmethod
    def cost(self) -> float:  # python中无需区分double和float
        pass


class CondimentDecorator(Beverage):
    """调料"""

    @abstractmethod
    def get_description(self) -> str:
        pass


class Espresso(Beverage):
    """浓缩咖啡"""

    def get_description(self) -> str:
        return "浓缩咖啡"

    def cost(self) -> float:
        return 1.99


class HouseBlend(Beverage):
    """综合咖啡"""

    def get_description(self) -> str:
        return "综合咖啡"

    def cost(self) -> float:
        return 0.89


class DarkRoast(Beverage):
    """深焙咖啡"""

    def get_description(self) -> str:
        return "深焙咖啡"

    def cost(self) -> float:
        return 0.99


class Decaf(Beverage):
    """低咖啡因"""

    def get_description(self) -> str:
        return "低咖啡因"

    def cost(self) -> float:
        return 1.05


class Mocha(CondimentDecorator):
    """摩卡"""

    def __init__(self, beverage: Beverage):
        self.beverage = beverage

    def get_description(self) -> str:
        return self.beverage.get_description() + '+摩卡'

    def cost(self) -> float:
        return self.beverage.cost() + 0.2


class Soy(CondimentDecorator):
    """豆浆"""

    def __init__(self, beverage: Beverage):
        self.beverage = beverage

    def get_description(self) -> str:
        return self.beverage.get_description() + '+豆浆'

    def cost(self) -> float:
        return self.beverage.cost() + 0.15


class Whip(CondimentDecorator):
    """奶泡"""

    def __init__(self, beverage: Beverage):
        self.beverage = beverage

    def get_description(self) -> str:
        return self.beverage.get_description() + '+奶泡'

    def cost(self) -> float:
        return self.beverage.cost() + 0.1


class Milk(CondimentDecorator):
    """牛奶"""

    def __init__(self, beverage: Beverage):
        self.beverage = beverage

    def get_description(self) -> str:
        return self.beverage.get_description() + '+牛奶'

    def cost(self) -> float:
        return self.beverage.cost() + 0.1


if __name__ == '__main__':
    beverage = Espresso()
    print(f"{beverage.get_description()}：${beverage.cost()}")

    beverage2 = DarkRoast()
    beverage2 = Mocha(beverage2)
    beverage2 = Mocha(beverage2)
    beverage2 = Whip(beverage2)
    print(f"{beverage2.get_description()}：${beverage2.cost()}")

    beverage3 = HouseBlend()
    beverage3 = Soy(beverage3)
    beverage3 = Mocha(beverage3)
    beverage3 = Whip(beverage3)
    print(f"{beverage3.get_description()}：${beverage3.cost()}")

"""运行结果：
浓缩咖啡：$1.99
深焙咖啡+摩卡+摩卡+奶泡：$1.49
综合咖啡+豆浆+摩卡+奶泡：$1.34
"""

