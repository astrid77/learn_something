#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/5/31 15:16
from abc import abstractmethod


class WeaponBehavior:
    """武器行为"""

    @abstractmethod
    def use_weapon(self):
        """使用武器"""
        pass


class KnifeBehavior(WeaponBehavior):
    def use_weapon(self):
        return '匕首'


class BowAndArrowBehavior(WeaponBehavior):
    def use_weapon(self):
        return '弓箭'


class AxeBehavior(WeaponBehavior):
    def use_weapon(self):
        return '斧头'


class SwordBehavior(WeaponBehavior):
    def use_weapon(self):
        return '宝剑'


class Character:
    """人物"""

    def __init__(self, w: WeaponBehavior = None):
        self._weapon = w

    @property
    def weapon(self):
        return self._weapon

    @weapon.setter
    def weapon(self, w: WeaponBehavior):
        self._weapon = w

    def fight(self):
        """战斗"""
        if self._weapon is None:
            print(f"{self.__class__.__name__} has no weapon!")
            return

        weapon = self._weapon.use_weapon()
        print(f"{self.__class__.__name__} use {weapon} fight")

    @abstractmethod
    def display(self) -> None:
        pass

class Queen(Character):
    def display(self) -> None:
        print("I'm a Queen")


class King(Character):
    def display(self) -> None:
        print("I'm a King")


class Troll(Character):
    def display(self) -> None:
        print("I'm a Troll")


class Knight(Character):
    def display(self) -> None:
        print("I'm a Knight")


if __name__ == '__main__':
    queen = Queen()
    queen.fight()
    queen.weapon = KnifeBehavior()
    queen.fight()

    king = King(KnifeBehavior())
    king.fight()

    king.weapon = BowAndArrowBehavior()
    king.fight()
