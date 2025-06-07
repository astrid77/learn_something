#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/6/7 17:26
from abc import abstractmethod


class CaffeineBeverageWithHook:
    """咖啡饮料"""

    def prepare_recipe(self):
        self.boil_water()
        self.brew()
        self.pour_in_cup()
        if self.customer_wants_condiments():
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

    def customer_wants_condiments(self):
        return True


class TeaHook(CaffeineBeverageWithHook):
    def brew(self):
        print('浸泡茶叶')

    def add_condiments(self):
        print('添加柠檬')


class CoffeeWithHook(CaffeineBeverageWithHook):
    def brew(self):
        print('冲泡咖啡')

    def add_condiments(self):
        print('添加奶和糖')

    def get_user_input(self):
        answer = input('Would you like milk and sugar with your coffe? (y/n)')
        return 'no' if not answer else answer

    def customer_wants_condiments(self):
        answer = self.get_user_input()
        if answer.lower().startswith('y'):
            return True
        return False


if __name__ == '__main__':
    tea_hook = TeaHook()
    coffee_hook = CoffeeWithHook()

    print('制作茶...')
    tea_hook.prepare_recipe()

    print('\n制作咖啡...')
    coffee_hook.prepare_recipe()

"""运行结果：
制作茶...
将水煮沸
浸泡茶叶
倒入杯子
添加柠檬

制作咖啡...
将水煮沸
冲泡咖啡
倒入杯子
Would you like milk and sugar with your coffe? (y/n)y
添加奶和糖
"""
