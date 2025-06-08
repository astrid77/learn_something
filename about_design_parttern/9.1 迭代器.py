#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/6/8 11:28
from abc import ABC, abstractmethod
from typing import List, Optional


# 菜单项类
class MenuItem:
    def __init__(self, name: str, description: str, vegetarian: bool, price: float):
        self.name = name
        self.description = description
        self.vegetarian = vegetarian
        self.price = price

    def __str__(self) -> str:
        veg_str = " [素食]" if self.vegetarian else ""
        return f"{self.name} (¥{self.price:.2f}) - {self.description}{veg_str}"


# 迭代器接口
class Iterator(ABC):
    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self) -> MenuItem:
        pass


# 煎饼屋菜单 (使用列表)
class PancakeHouseMenu:
    def __init__(self):
        self.menu_items: List[MenuItem] = []
        self.add_item("传统煎饼", "配鸡蛋和吐司", True, 12.99)
        self.add_item("蓝莓煎饼", "新鲜蓝莓制作", True, 14.49)
        self.add_item("华夫饼", "配蓝莓或草莓", True, 15.59)

    def add_item(self, name: str, description: str,
                 vegetarian: bool, price: float) -> None:
        self.menu_items.append(MenuItem(name, description, vegetarian, price))

    def create_iterator(self) -> Iterator:
        return PancakeHouseMenuIterator(self.menu_items)


# 煎饼屋菜单迭代器
class PancakeHouseMenuIterator(Iterator):
    def __init__(self, items: List[MenuItem]):
        self.items = items
        self.position = 0

    def has_next(self) -> bool:
        return self.position < len(self.items)

    def next(self) -> MenuItem:
        item = self.items[self.position]
        self.position += 1
        return item


# 餐厅菜单 (使用固定大小数组)
class DinerMenu:
    MAX_ITEMS = 6

    def __init__(self):
        self.menu_items: List[Optional[MenuItem]] = [None] * self.MAX_ITEMS
        self.number_of_items = 0

        self.add_item("蔬菜汤", "时令蔬菜汤", True, 13.29)
        self.add_item("热狗", "酸菜配黄芥末", False, 13.05)
        self.add_item("烤鸡", "土豆泥配蔬菜", False, 30.99)

    def add_item(self, name: str, description: str,
                 vegetarian: bool, price: float) -> None:
        if self.number_of_items >= self.MAX_ITEMS:
            print("错误：菜单已满！无法添加新菜品")
            return

        self.menu_items[self.number_of_items] = MenuItem(
            name, description, vegetarian, price
        )
        self.number_of_items += 1

    def create_iterator(self) -> Iterator:
        return DinerMenuIterator(self.menu_items, self.number_of_items)


# 餐厅菜单迭代器
class DinerMenuIterator(Iterator):
    def __init__(self, items: List[Optional[MenuItem]], item_count: int):
        self.items = items
        self.item_count = item_count
        self.position = 0

    def has_next(self) -> bool:
        # 跳过空位置
        while (self.position < self.item_count and
               self.items[self.position] is None):
            self.position += 1
        return self.position < self.item_count

    def next(self) -> MenuItem:
        if not self.has_next():
            raise StopIteration()
        item = self.items[self.position]
        self.position += 1
        return item


# 女招待 (客户端)
class Waitress:
    def __init__(self, pancake_menu: PancakeHouseMenu, diner_menu: DinerMenu):
        self.pancake_menu = pancake_menu
        self.diner_menu = diner_menu

    def print_menu(self) -> None:
        print("====== 早餐菜单 ======")
        self._print_menu(self.pancake_menu.create_iterator())

        print("\n====== 午餐菜单 ======")
        self._print_menu(self.diner_menu.create_iterator())

    def _print_menu(self, iterator: Iterator) -> None:
        while iterator.has_next():
            menu_item = iterator.next()
            print(menu_item)


# 测试代码
if __name__ == "__main__":
    pancake_menu = PancakeHouseMenu()
    diner_menu = DinerMenu()

    waitress = Waitress(pancake_menu, diner_menu)
    waitress.print_menu()


"""运行结果：
====== 早餐菜单 ======
传统煎饼 (¥12.99) - 配鸡蛋和吐司 [素食]
蓝莓煎饼 (¥14.49) - 新鲜蓝莓制作 [素食]
华夫饼 (¥15.59) - 配蓝莓或草莓 [素食]

====== 午餐菜单 ======
蔬菜汤 (¥13.29) - 时令蔬菜汤 [素食]
热狗 (¥13.05) - 酸菜配黄芥末
烤鸡 (¥30.99) - 土豆泥配蔬菜
"""