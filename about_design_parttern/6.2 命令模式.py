#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/6/5 22:04

from abc import ABCMeta, abstractmethod, ABC
from typing import List


class Command(ABC):

    @abstractmethod
    def excute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class NoCommand(Command):

    def excute(self):
        pass

    def undo(self):
        pass


class Stereo:
    """音响"""
    name: str
    HIGH = 90
    MEDIUM = 40
    LOW = 10
    OFF = 0
    _volume: int

    def __init__(self, name):
        self.name = name
        self._volume = Stereo.OFF

    def off(self):
        print(f'{self.name} is off.')

    def on(self):
        print(f'{self.name} is on.')

    def set_cd(self):
        print(f'{self.name} is set for CD input.')

    def set_volume(self, volume: int):
        self._volume = volume
        print(f'{self.name} volume set to {volume}.')

    def get_volume(self):
        return self._volume

    def volume_high(self):
        print(f'音量设置为{Stereo.HIGH}')
        self._volume = Stereo.HIGH

    def volume_medium(self):
        print(f'音量设置为{Stereo.MEDIUM}')
        self._volume = Stereo.MEDIUM

    def volume_low(self):
        print(f'音量设置为{Stereo.LOW}')
        self._volume = Stereo.LOW


class StereoOnWithCDCommand(Command):
    stereo: Stereo
    pre_volume: int

    def __init__(self, stereo: Stereo):
        self.stereo = stereo

    def excute(self):
        self.pre_volume = self.stereo.get_volume()
        self.stereo.on()
        self.stereo.set_cd()
        self.stereo.set_volume(Stereo.MEDIUM)

    def undo(self):
        print('撤销操作，', end='')


class StereoHighVolumeWithCDCommand(Command):
    pre_volume: int

    def __init__(self, stereo: Stereo):
        self.stereo = stereo

    def excute(self):
        self.pre_volume = self.stereo.get_volume()
        self.stereo.volume_high()

    def undo(self):
        print('撤销操作，', end='')
        if self.pre_volume == Stereo.HIGH:
            self.stereo.volume_high()
        elif self.pre_volume == Stereo.MEDIUM:
            self.stereo.volume_medium()
        elif self.pre_volume == Stereo.LOW:
            self.stereo.volume_low()
        else:
            self.stereo.off()


class StereoLowVolumeWithCDCommand(Command):
    pre_volume: int

    def __init__(self, stereo: Stereo):
        self.stereo = stereo

    def excute(self):
        self.pre_volume = self.stereo.get_volume()
        self.stereo.volume_low()

    def undo(self):
        print('撤销操作，', end='')
        if self.pre_volume == Stereo.HIGH:
            self.stereo.volume_high()
        elif self.pre_volume == Stereo.MEDIUM:
            self.stereo.volume_medium()
        elif self.pre_volume == Stereo.LOW:
            self.stereo.volume_low()
        else:
            self.stereo.off()


class StereoOffWithCDCommand(Command):
    stereo: Stereo

    def __init__(self, stereo: Stereo):
        self.stereo = stereo

    def excute(self):
        self.stereo.off()

    def undo(self):
        print('撤销操作，', end='')
        self.stereo.on()


class RemoteControlWithUndo:
    """遥控器"""
    on_commands: List[Command]
    off_commands: List[Command]
    undo_command: Command

    def __init__(self):
        self.on_commands = []
        self.off_commands = []
        no_command = NoCommand()
        for _ in range(7):
            self.on_commands.append(no_command)
            self.off_commands.append(no_command)
        self.undo_command = no_command

    def set_command(self, slot: int, on_command: Command, off_command: Command):
        self.on_commands[slot] = on_command
        self.off_commands[slot] = off_command

    def on_button_was_pushed(self, slot: int):
        self.on_commands[slot].excute()
        self.undo_command = self.on_commands[slot]

    def off_button_was_pushed(self, slot: int):
        self.off_commands[slot].excute()
        self.undo_command = self.off_commands[slot]

    def undo_button_was_pushed(self):
        self.undo_command.undo()

    def __str__(self):
        buffer_str = []
        for i in range(len(self.on_commands)):
            buffer_str.append(
                f'[卡槽{i + 1}]{self.on_commands[i].__class__.__qualname__}\t{self.off_commands[i].__class__.__qualname__}')
        return "\n".join(buffer_str)


if __name__ == '__main__':
    remote_control = RemoteControlWithUndo()
    stereo = Stereo('音响')
    stereo_off = StereoOffWithCDCommand(stereo)
    stereo_high_volume = StereoHighVolumeWithCDCommand(stereo)
    stereo_low_volume = StereoLowVolumeWithCDCommand(stereo)

    remote_control.set_command(0, stereo_high_volume, stereo_off)
    remote_control.set_command(1, stereo_low_volume, stereo_off)
    print(remote_control)

    remote_control.on_button_was_pushed(0)
    remote_control.off_button_was_pushed(0)
    remote_control.undo_button_was_pushed()

    remote_control.on_button_was_pushed(1)
    remote_control.undo_button_was_pushed()

"""运行结果：
[卡槽1]StereoHighVolumeWithCDCommand	StereoOffWithCDCommand
[卡槽2]StereoLowVolumeWithCDCommand	StereoOffWithCDCommand
[卡槽3]NoCommand	NoCommand
[卡槽4]NoCommand	NoCommand
[卡槽5]NoCommand	NoCommand
[卡槽6]NoCommand	NoCommand
[卡槽7]NoCommand	NoCommand
音量设置为90
音响 is off.
撤销操作，音响 is on.
音量设置为10
撤销操作，音量设置为90
"""
