#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/6/2 15:45

from abc import abstractmethod


class Pizza:
    name: str  # 名称
    dough: str  # 面团类型
    sauce: str  # 酱料
    toppings: list  # 佐料
    veggies: list  # 原料

    def __init__(self):
        self.toppings = []  # 佐料
        self.veggies = []  # 原料

    @abstractmethod
    def prepare(self):
        pass

    def bake(self):
        print('350度烘焙25分钟')

    def cut(self):
        print('将披萨切块')

    def box(self):
        print('披萨装盒')

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def __str__(self):
        return f'{self.name}已制作完成，使用的原料有：{"、".join(self.veggies)}'


class PizzaStore:
    @abstractmethod
    def _create_pizza(self, ptype) -> Pizza:
        pass

    def order_pizza(self, ptype):
        pizza = self._create_pizza(ptype)

        pizza.prepare()
        pizza.cut()
        pizza.bake()
        pizza.box()

        print(f'{pizza}\n')
        return pizza


class Sauce:
    name: str = '酱料'


class NYSauce(Sauce):
    name = '纽约风味的酱料'


class ChicagoSauce(Sauce):
    name = '芝加哥风味的酱料'


class PizzaIngredientFactory:
    """原料工厂"""
    sauce: Sauce  # 原料工厂的原料之一：酱料

    @abstractmethod
    def create_sauce(self) -> Sauce:
        pass


class NYPizzaIngredientFactory(PizzaIngredientFactory):
    """纽约原料工厂"""

    def create_sauce(self) -> Sauce:
        return NYSauce()  # 提供纽约酱料


class ChicagoPizzaIngredientFactory(PizzaIngredientFactory):
    """芝加哥原料工厂"""

    def create_sauce(self) -> Sauce:
        return ChicagoSauce()  # 提供芝加哥原料


class CheesePizza(Pizza):
    """芝士披萨"""
    ingredient: PizzaIngredientFactory

    def __init__(self, ingredient: PizzaIngredientFactory):
        super().__init__()
        self.ingredient = ingredient  # 使用指定的原料工厂

    def prepare(self):
        print(f'{self.name}准备中...')
        self.sauce = self.ingredient.create_sauce()  # 使用指定原料工厂提供的酱料
        self.veggies.append(self.sauce.name)  # 原料列表


class NYStylePizzaStore(PizzaStore):

    def _create_pizza(self, ptype) -> Pizza:
        self.ingredient = NYPizzaIngredientFactory()  # 纽约的披萨店用纽约的原料工厂
        if ptype == 'cheese':
            pizza = CheesePizza(self.ingredient)
            pizza.set_name('纽约风味的芝士披萨')
        return pizza  # 除cheese外其他披萨会报错，先忽略


class ChicagoStylePizzaStore(PizzaStore):

    def _create_pizza(self, ptype) -> Pizza:
        self.ingredient = ChicagoPizzaIngredientFactory()  # 芝加哥的披萨店用芝加哥的原料工厂
        if ptype == 'cheese':
            pizza = CheesePizza(self.ingredient)
            pizza.set_name('芝加哥风味的芝士披萨')
        return pizza


if __name__ == '__main__':
    store = NYStylePizzaStore()
    store.order_pizza('cheese')

    store = ChicagoStylePizzaStore()
    store.order_pizza('cheese')

"""运行结果：
纽约风味的芝士披萨准备中...
将披萨切块
350度烘焙25分钟
披萨装盒
纽约风味的芝士披萨已制作完成，使用的原料有：纽约风味的酱料

芝加哥风味的芝士披萨准备中...
将披萨切块
350度烘焙25分钟
披萨装盒
芝加哥风味的芝士披萨已制作完成，使用的原料有：芝加哥风味的酱料
"""
