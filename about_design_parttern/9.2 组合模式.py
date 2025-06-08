#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/6/8 14:30
from abc import ABC, abstractmethod
from typing import List


class MenuComponent(ABC):
    """菜单组件的抽象基类"""

    def add(self, component: 'MenuComponent') -> None:
        raise NotImplementedError("不支持添加操作")

    def remove(self, component: 'MenuComponent') -> None:
        raise NotImplementedError("不支持移除操作")

    def get_child(self, i: int) -> 'MenuComponent':
        raise NotImplementedError("不支持获取子项")

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_price(self) -> float:
        pass

    @abstractmethod
    def is_vegetarian(self) -> bool:
        pass

    @abstractmethod
    def print(self) -> None:
        pass


class MenuItem(MenuComponent):
    """叶子节点：菜单项"""

    def __init__(self, name: str, description: str,
                 vegetarian: bool, price: float):
        self.name = name
        self.description = description
        self.vegetarian = vegetarian
        self.price = price

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description

    def get_price(self) -> float:
        return self.price

    def is_vegetarian(self) -> bool:
        return self.vegetarian

    def print(self) -> None:
        veg_str = " (素食)" if self.vegetarian else ""
        print(f"  {self.name}{veg_str}, ¥{self.price:.2f}")
        print(f"    -- {self.description}")


class Menu(MenuComponent):
    """组合节点：菜单（可以包含菜单项或子菜单）"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.components: List[MenuComponent] = []

    def add(self, component: MenuComponent) -> None:
        self.components.append(component)

    def remove(self, component: MenuComponent) -> None:
        self.components.remove(component)

    def get_child(self, i: int) -> MenuComponent:
        return self.components[i]

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description

    def get_price(self) -> float:
        raise NotImplementedError("菜单没有价格")

    def is_vegetarian(self) -> bool:
        raise NotImplementedError("菜单没有素食属性")

    def print(self) -> None:
        print(f"\n{self.name}, {self.description}")
        print("-" * 50)

        for component in self.components:
            component.print()


class Waitress:
    """女招待类 - 客户端"""

    def __init__(self, all_menus: MenuComponent):
        self.all_menus = all_menus

    def print_menu(self) -> None:
        self.all_menus.print()

    def print_vegetarian_menu(self) -> None:
        print("\n===== 素食菜单 =====")
        self._print_vegetarian(self.all_menus)

    def _print_vegetarian(self, component: MenuComponent) -> None:
        try:
            if component.is_vegetarian():
                print(f"  {component.get_name()}, ¥{component.get_price():.2f}")
                print(f"    -- {component.get_description()}")
        except NotImplementedError:
            pass

        try:
            for child in component.components:
                self._print_vegetarian(child)
        except AttributeError:
            pass


def build_menu_system() -> MenuComponent:
    """构建整个菜单系统"""

    # 顶层菜单
    all_menus = Menu("主菜单", "所有菜单的总和")

    # 早餐菜单
    breakfast_menu = Menu("早餐菜单", "早晨供应")
    breakfast_menu.add(MenuItem("煎饼", "配枫糖浆", True, 12.99))
    breakfast_menu.add(MenuItem("华夫饼", "配蓝莓", True, 14.99))
    breakfast_menu.add(MenuItem("培根鸡蛋", "配吐司", False, 18.99))

    # 午餐菜单
    lunch_menu = Menu("午餐菜单", "中午供应")
    lunch_menu.add(MenuItem("蔬菜汤", "时令蔬菜", True, 16.99))
    lunch_menu.add(MenuItem("烤鸡三明治", "配沙拉", False, 22.99))
    lunch_menu.add(MenuItem("凯撒沙拉", "新鲜蔬菜", True, 18.99))

    # 晚餐菜单
    dinner_menu = Menu("晚餐菜单", "晚上供应")
    dinner_menu.add(MenuItem("牛排", "配烤土豆", False, 68.99))
    dinner_menu.add(MenuItem("烤三文鱼", "配蔬菜", False, 58.99))
    dinner_menu.add(MenuItem("素食意面", "配番茄酱", True, 36.99))

    # 甜点菜单（作为晚餐的子菜单）
    dessert_menu = Menu("甜点菜单", "餐后甜点")
    dessert_menu.add(MenuItem("苹果派", "配香草冰淇淋", True, 18.99))
    dessert_menu.add(MenuItem("巧克力蛋糕", "双层巧克力", True, 22.99))
    dessert_menu.add(MenuItem("奶酪拼盘", "精选奶酪", False, 28.99))

    # 添加到晚餐菜单
    dinner_menu.add(dessert_menu)

    # 咖啡菜单（独立菜单）
    cafe_menu = Menu("咖啡菜单", "全天供应")
    cafe_menu.add(MenuItem("浓缩咖啡", "纯正意大利风味", True, 12.99))
    cafe_menu.add(MenuItem("卡布奇诺", "现磨咖啡", True, 16.99))
    cafe_menu.add(MenuItem("热巧克力", "比利时巧克力", True, 14.99))

    # 将所有菜单添加到顶层菜单
    all_menus.add(breakfast_menu)
    all_menus.add(lunch_menu)
    all_menus.add(dinner_menu)
    all_menus.add(cafe_menu)

    return all_menus


if __name__ == "__main__":
    # 构建菜单系统
    menu_system = build_menu_system()

    # 创建女招待
    waitress = Waitress(menu_system)

    print("=" * 50)
    print("餐厅完整菜单:")
    print("=" * 50)
    waitress.print_menu()

    print("\n" + "=" * 50)
    print("素食选项:")
    print("=" * 50)
    waitress.print_vegetarian_menu()

"""运行结果：
==================================================
餐厅完整菜单:
==================================================

主菜单, 所有菜单的总和
--------------------------------------------------

早餐菜单, 早晨供应
--------------------------------------------------
  煎饼 (素食), ¥12.99
    -- 配枫糖浆
  华夫饼 (素食), ¥14.99
    -- 配蓝莓
  培根鸡蛋, ¥18.99
    -- 配吐司

午餐菜单, 中午供应
--------------------------------------------------
  蔬菜汤 (素食), ¥16.99
    -- 时令蔬菜
  烤鸡三明治, ¥22.99
    -- 配沙拉
  凯撒沙拉 (素食), ¥18.99
    -- 新鲜蔬菜

晚餐菜单, 晚上供应
--------------------------------------------------
  牛排, ¥68.99
    -- 配烤土豆
  烤三文鱼, ¥58.99
    -- 配蔬菜
  素食意面 (素食), ¥36.99
    -- 配番茄酱

甜点菜单, 餐后甜点
--------------------------------------------------
  苹果派 (素食), ¥18.99
    -- 配香草冰淇淋
  巧克力蛋糕 (素食), ¥22.99
    -- 双层巧克力
  奶酪拼盘, ¥28.99
    -- 精选奶酪

咖啡菜单, 全天供应
--------------------------------------------------
  浓缩咖啡 (素食), ¥12.99
    -- 纯正意大利风味
  卡布奇诺 (素食), ¥16.99
    -- 现磨咖啡
  热巧克力 (素食), ¥14.99
    -- 比利时巧克力

==================================================
素食选项:
==================================================

===== 素食菜单 =====
  煎饼, ¥12.99
    -- 配枫糖浆
  华夫饼, ¥14.99
    -- 配蓝莓
  蔬菜汤, ¥16.99
    -- 时令蔬菜
  凯撒沙拉, ¥18.99
    -- 新鲜蔬菜
  素食意面, ¥36.99
    -- 配番茄酱
  苹果派, ¥18.99
    -- 配香草冰淇淋
  巧克力蛋糕, ¥22.99
    -- 双层巧克力
  浓缩咖啡, ¥12.99
    -- 纯正意大利风味
  卡布奇诺, ¥16.99
    -- 现磨咖啡
  热巧克力, ¥14.99
    -- 比利时巧克力
"""
