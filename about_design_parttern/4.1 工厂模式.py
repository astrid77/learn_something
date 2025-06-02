#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/6/2 13:32
from abc import abstractmethod


class Pizza:
    name: str  # 名称
    dough: str  # 面团类型
    sauce: str  # 酱料
    toppings: list  # 佐料

    def __init__(self):
        self.toppings = []  # 佐料

    def prepare(self):
        print(f'{self.name}准备中...')
        print(f'揉搓{self.dough}...')
        print(f'添加{self.sauce}...')
        print(f'添加佐料：{"、".join(self.toppings)}')

    def bake(self):
        print('350度烘焙25分钟')

    def cut(self):
        print('将披萨切块')

    def box(self):
        print('披萨装盒')

    def get_name(self):
        return self.name


class PizzaStore:
    @abstractmethod
    def _create_pizza(self, ptype) -> Pizza:
        pass

    def order_pizza(self, ptype):
        pizza = self._create_pizza(ptype)
        print(f'---下单一个{pizza.name}---')

        pizza.prepare()
        pizza.cut()
        pizza.bake()
        pizza.box()

        print('订单制作完成\n')
        return pizza


class NYStyleCheesePizza(Pizza):

    def __init__(self):
        super().__init__()
        self.name = '纽约风味的芝士披萨'
        self.sauce = '大蒜番茄酱'
        self.dough = '薄饼'
        self.toppings.append('意大利高级干酪')


class ChicagoStyleCheesePizza(Pizza):

    def __init__(self):
        super().__init__()
        self.name = '芝加哥风味的芝士披萨'
        self.sauce = '小番茄酱料'
        self.dough = '厚饼'
        self.toppings.append('意大利白干酪')

    def cut(self):
        print('将披萨切成正方形')


class NYStylePizzaStore(PizzaStore):

    def _create_pizza(self, ptype) -> Pizza:
        if ptype == 'cheese':
            pizza = NYStyleCheesePizza()
        return pizza


class ChicagoStylePizzaStore(PizzaStore):

    def _create_pizza(self, ptype) -> Pizza:
        if ptype == 'cheese':
            pizza = ChicagoStyleCheesePizza()
        return pizza


if __name__ == '__main__':
    NYStore = NYStylePizzaStore()
    ChicagoStore = ChicagoStylePizzaStore()

    NYStore.order_pizza('cheese')

    ChicagoStore.order_pizza('cheese')

"""运行结果：
---下单一个纽约风味的芝士披萨---
纽约风味的芝士披萨准备中...
揉搓薄饼...
添加大蒜番茄酱...
添加佐料：意大利高级干酪
将披萨切块
350度烘焙25分钟
披萨装盒
订单制作完成

---下单一个芝加哥风味的芝士披萨---
芝加哥风味的芝士披萨准备中...
揉搓厚饼...
添加小番茄酱料...
添加佐料：意大利白干酪
将披萨切成正方形
350度烘焙25分钟
披萨装盒
订单制作完成
"""
