#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/6/7 17:26
from abc import abstractmethod


class CaffeineBeverage:
    """咖啡饮料"""

    def prepare_recipe(self):
        self.boil_water()
        self.brew()
        self.pour_in_cup()
        self.add_condiments()

    def boil_water(self):
        print('将水煮沸')

    @abstractmethod
    def brew(self):
        print('浸泡或冲泡')

    def pour_in_cup(self):
        print('倒入杯子')

    @abstractmethod
    def add_condiments(self):
        print('添加调料')


class Tea(CaffeineBeverage):
    def brew(self):
        print('浸泡茶叶')

    def add_condiments(self):
        print('添加柠檬')


class Coffee(CaffeineBeverage):
    def brew(self):
        print('冲泡咖啡')

    def add_condiments(self):
        print('添加奶和糖')

if __name__ == '__main__':
    tea = Tea()
    tea.prepare_recipe()
    print()
    coffee = Coffee()
    coffee.prepare_recipe()

"""运行结果：
将水煮沸
浸泡茶叶
倒入杯子
添加柠檬

将水煮沸
冲泡咖啡
倒入杯子
添加奶和糖
"""