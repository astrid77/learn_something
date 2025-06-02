#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/6/1 11:45
from abc import abstractmethod
from typing import Optional


class Observer:
    """观察者"""

    @abstractmethod
    def update(self, temp, humidity, pressure):
        """由主题调用更新"""
        pass


class Subject:
    """主题"""

    @abstractmethod
    def register_observer(self, observer: Observer):
        """注册"""
        pass

    @abstractmethod
    def notify_observers(self):
        """通知所有观察者"""
        pass

    @abstractmethod
    def remove_observer(self, observer: Observer):
        """移除"""
        pass


class DisplayElement:

    @abstractmethod
    def display(self):
        """显示"""
        pass


class WeatherData(Subject):
    def __init__(self):
        self._observers: list[Observer] = []
        self._temp: Optional[float, None] = None
        self._pressure: Optional[float, None] = None
        self._humidity: Optional[float, None] = None

    def register_observer(self, observer: Observer):
        self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for obs in self._observers:
            obs.update(self._temp, self._humidity, self._pressure)

    def measurements_changed(self):
        self.notify_observers()

    def set_measurements(self, temp: float, humidity: float, pressure: float):
        self._temp = temp
        self._humidity = humidity
        self._pressure = pressure
        self.measurements_changed()


class CurrentConditionsDispaly(Observer, DisplayElement):
    def __init__(self, weather_data: WeatherData):
        self._weather_data = weather_data
        self._weather_data.register_observer(self)
        self._temp: Optional[float, None] = None
        self._pressure: Optional[float, None] = None
        self._humidity: Optional[float, None] = None

    def update(self, temp, humidity, pressure):
        self._temp = temp
        self._humidity = humidity
        self._pressure = pressure
        self.display()

    def display(self):
        print(id(self))
        print(f"温度：{self._temp}\n"
              f"湿度：{self._humidity}\n"
              f"气压：{self._pressure}\n")


if __name__ == '__main__':
    weather = WeatherData()
    display = CurrentConditionsDispaly(weather)
    weather.set_measurements(80, 80, 2.34)
    display2 = CurrentConditionsDispaly(weather)
    weather.set_measurements(90, 70.5, 5)

"""运行结果：
4481847152
温度：80
湿度：80
气压：2.34

4481847152
温度：90
湿度：70.5
气压：5

4481845424
温度：90
湿度：70.5
气压：5
"""
