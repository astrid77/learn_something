#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/6/1 11:45
from abc import abstractmethod, ABC
from typing import Optional, Union


class Observer(ABC):
    """观察者"""

    @abstractmethod
    def update(self, observerable, arg):
        """由主题调用更新"""
        pass


class Observerable:
    """可观察者"""
    _observers = []
    changed = False

    def register_observer(self, observer: Observer):
        self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)

    def notify_observers(self, arg=None):
        if self.changed:
            for obs in self._observers:
                obs.update(self, arg)
        else:
            self.changed = False

    def set_changed(self):
        self.changed = True


class DisplayElement:

    @abstractmethod
    def display(self):
        """显示"""
        pass


class WeatherData(Observerable):
    _temp: float  # python新版本可不指定默认值
    _humidity: float
    _pressure: float

    def measurements_changed(self):
        self.set_changed()
        self.notify_observers()

    def get_temperature(self) -> float:
        return self._temp

    def get_humility(self) -> float:
        return self._humidity

    def get_pressure(self) -> float:
        return self._pressure

    def set_measurements(self, temp: float, humidity: float, pressure: float):
        self._temp = temp
        self._humidity = humidity
        self._pressure = pressure
        self.measurements_changed()


class CurrentConditionsDispaly(Observer, DisplayElement):
    _temp: float  # python新版本可不指定默认值
    _humidity: Optional[float]  # 值类型可以为float和None时，可以用 Optional[float] 相当于 Union[float, None]
    _pressure: Union[float, None]

    def __init__(self, observerable: Observerable):
        self._observerable = observerable
        observerable.register_observer(self)

    def update(self, observerable, arg):
        if isinstance(observerable, WeatherData):
            self._temp = observerable.get_temperature()
            self._pressure = observerable.get_pressure()
            self._humidity = observerable.get_humility()
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
