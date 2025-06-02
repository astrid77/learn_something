#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/5/31 13:33
from abc import ABC, abstractmethod

# 方式一
# class Animal:
#
#     def make_sound(self):
#         raise NotImplementedError('子类必须实现make_sound方法')

# 方式二
class Animal(ABC):
    """抽象类"""

    @abstractmethod
    def make_sound(self):
        """子类必须实现该方法，表示所有动物都能发出声音"""
        pass


class Dog(Animal):

    def make_sound(self):
        self._bark()

    def _bark(self):  # 单下划线表示仅内部调用，相当于java的private
        print("汪汪叫")


class Cat(Animal):

    def make_sound(self):
        self._meow()

    def _meow(self):
        print("喵喵叫")


if __name__ == '__main__':
    dog = Dog()
    dog.make_sound()

    cat = Cat()
    cat.make_sound()
