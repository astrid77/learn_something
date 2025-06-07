#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/6/7 14:46
from abc import ABC, abstractmethod


class Duck(ABC):
    """鸭子"""

    @abstractmethod
    def quack(self):
        pass

    @abstractmethod
    def fly(self):
        pass


class MallardDuck(Duck):
    """绿头鸭"""

    def quack(self):
        print("Quack")

    def fly(self):
        print("I'm flying")


class Turkey(ABC):
    """火鸡"""

    @abstractmethod
    def gobble(self):
        pass

    @abstractmethod
    def fly(self):
        pass


class WildTurkey(Turkey):
    """野鸡"""

    def gobble(self):
        print('Gobble gobble')

    def fly(self):
        print("I'm flying a short distance")


class TurkeyAdapter(Duck):
    turkey: Turkey

    def __init__(self, turkey: Turkey):
        self.turkey = turkey

    def quack(self):
        self.turkey.gobble()

    def fly(self):
        for _ in range(5):
            self.turkey.fly()


class DuckAdapter(Turkey):
    duck: Duck

    def __init__(self, duck: Duck):
        self.duck = duck
        self.__reset()

    def __reset(self):
        self.rand = (_ for _ in range(4))

    def gobble(self):
        self.duck.quack()

    def fly(self):
        try:
            next(self.rand)
        except StopIteration:
            self.duck.fly()
            self.__reset()


if __name__ == '__main__':
    duck = MallardDuck()
    turkey = WildTurkey()
    turkey_adapter = TurkeyAdapter(turkey)
    duck_adapter = DuckAdapter(duck)
    print('The Turkey says...')
    turkey.gobble()
    turkey.fly()

    print('\nThe Duck says...')
    duck.quack()
    duck.fly()

    print('\nThe TurkeyAdapter says...')
    turkey_adapter.quack()
    turkey_adapter.fly()

    print('\nThe DuckAdapter says...')
    duck_adapter.gobble()
    for _ in range(10):
        duck_adapter.fly()

"""运行结果：
The Turkey says...
Gobble gobble
I'm flying a short distance

The Duck says...
Quack
I'm flying

The TurkeyAdapter says...
Gobble gobble
I'm flying a short distance
I'm flying a short distance
I'm flying a short distance
I'm flying a short distance
I'm flying a short distance

The DuckAdapter says...
Quack
I'm flying
I'm flying
"""
