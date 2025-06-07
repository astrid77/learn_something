#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/6/5 21:02
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


class MacroCommand(Command):
    commands: List[Command]

    def __init__(self, commands: List[Command]):
        self.commands = commands

    def excute(self):
        for command in self.commands:
            command.excute()

    def undo(self):
        for command in self.commands:
            command.undo()


class Light:
    """电灯"""
    name: str

    def __init__(self, name):
        self.name = name

    def off(self):
        print(f'{self.name} is off.')

    def on(self):
        print(f'{self.name} is on.')


class LightOnCommand(Command):
    light: Light

    def __init__(self, light: Light):
        self.light = light

    def excute(self):
        self.light.on()

    def undo(self):
        print('撤销操作，', end='')
        self.light.off()


class LightOffCommand(Command):
    light: Light

    def __init__(self, light: Light):
        self.light = light

    def excute(self):
        self.light.off()

    def undo(self):
        print('撤销操作，', end='')
        self.light.on()


class Stereo:
    """音响"""
    name: str

    def __init__(self, name):
        self.name = name

    def off(self):
        print(f'{self.name} is off.')

    def on(self):
        print(f'{self.name} is on.')

    def set_cd(self):
        print(f'{self.name} is set for CD input.')

    def set_volume(self, volume: int):
        print(f'{self.name} volume set to {volume}.')


class StereoOnWithCDCommand(Command):
    stereo: Stereo

    def __init__(self, stereo: Stereo):
        self.stereo = stereo

    def excute(self):
        self.stereo.on()
        self.stereo.set_cd()
        self.stereo.set_volume(11)

    def undo(self):
        print('撤销操作，', end='')
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


class RemoteControl:
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
    remote_control = RemoteControl()
    living_room_light = Light("Living Room light")
    kitchen_light = Light("Kitchen light")
    stereo = Stereo("Living Room Stereo")

    living_room_light_on = LightOnCommand(living_room_light)
    living_room_light_off = LightOffCommand(living_room_light)

    kitchen_light_on = LightOnCommand(kitchen_light)
    kitchen_light_off = LightOffCommand(kitchen_light)

    stereo_on = StereoOnWithCDCommand(stereo)
    stereo_off = StereoOffWithCDCommand(stereo)

    remote_control.set_command(0, living_room_light_on, living_room_light_off)
    remote_control.set_command(1, kitchen_light_on, kitchen_light_off)
    remote_control.set_command(2, stereo_on, stereo_off)

    party_on_macro = [living_room_light_on, kitchen_light_on, stereo_on]
    party_on = MacroCommand(party_on_macro)
    party_off = MacroCommand([living_room_light_off, kitchen_light_off, stereo_off])
    remote_control.set_command(3, party_on, party_off)

    print(remote_control)
    print()

    print('---Pushing Macro On---')
    remote_control.on_button_was_pushed(3)
    print()

    print('---Pushing Macro Off---')
    remote_control.off_button_was_pushed(3)

    print()
    print('---Pushing Macro Undo---')
    remote_control.undo_button_was_pushed()

"""运行结果：
[卡槽1]LightOnCommand	LightOffCommand
[卡槽2]LightOnCommand	LightOffCommand
[卡槽3]StereoOnWithCDCommand	StereoOffWithCDCommand
[卡槽4]MacroCommand	MacroCommand
[卡槽5]NoCommand	NoCommand
[卡槽6]NoCommand	NoCommand
[卡槽7]NoCommand	NoCommand

---Pushing Macro On---
Living Room light is on.
Kitchen light is on.
Living Room Stereo is on.
Living Room Stereo is set for CD input.
Living Room Stereo volume set to 11.

---Pushing Macro Off---
Living Room light is off.
Kitchen light is off.
Living Room Stereo is off.

---Pushing Macro Undo---
撤销操作，Living Room light is on.
撤销操作，Kitchen light is on.
撤销操作，Living Room Stereo is on.
"""
