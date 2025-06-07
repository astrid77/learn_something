#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/6/7 15:34

class Amplifier:
    """扩音器"""

    def on(self):
        print('打开扩音器')

    def setStreamingPlayer(self, player):
        print('设置流媒体输入')

    def setSurroundSound(self):
        print('设置环绕音响')

    def setVolume(self, param):
        print(f'设置音量为{param}')

    def off(self):
        print('关闭扩音器')


class Tunner:
    pass


class StreamingPlayer:
    """流媒体播放器"""

    def on(self):
        print('打开流媒体播放器')

    def play(self, movie):
        print(f'播放{movie}')

    def stop(self):
        print('停止播放')

    def off(self):
        print('关闭流媒体播放器')


class Projector:
    """投影机"""

    def on(self):
        print('打开投影机')

    def wideScrennMode(self):
        print('设置投影机为宽屏模式')

    def off(self):
        print('关闭投影机')


class TheaterLights:
    """影院灯光"""

    def lim(self, param):
        print('调暗灯光')

    def on(self):
        print('打开灯光')


class PopcornPopper:
    """爆米花机器"""

    def on(self):
        print('打开爆米花机器')

    def pop(self):
        print('提供爆米花')

    def off(self):
        print('关闭爆米花机器')


class Screen:
    """投影机的屏幕"""

    def down(self):
        print('放下屏幕')

    def up(self):
        print('收起屏幕')


class HomeTheaterFacade:
    """家庭影院外观"""
    amp: Amplifier
    tunner: Tunner
    player: StreamingPlayer
    projector: Projector
    lights: TheaterLights
    screen: Screen
    popper: PopcornPopper

    def __init__(self, amp: Amplifier, tunner: Tunner,
                 player: StreamingPlayer,
                 projector: Projector,
                 lights: TheaterLights,
                 screen: Screen,
                 popper: PopcornPopper):
        self.amp = amp
        self.tunner = tunner
        self.player = player
        self.projector = projector
        self.lights = lights
        self.screen = screen
        self.popper = popper

    def watch_movie(self, movie: str):
        print('准备播放电影...')
        self.popper.on()
        self.popper.pop()
        self.lights.lim(10)
        self.screen.down()
        self.projector.on()
        self.projector.wideScrennMode()
        self.amp.on()
        self.amp.setStreamingPlayer(self.player)
        self.amp.setSurroundSound()
        self.amp.setVolume(5)
        self.player.on()
        self.player.play(movie)

    def end_movie(self):
        print('停止播放电影')
        self.popper.off()
        self.lights.on()
        self.screen.up()
        self.projector.off()
        self.amp.off()
        self.player.stop()
        self.player.off()


if __name__ == '__main__':
    amp = Amplifier()
    tunner = Tunner()
    player = StreamingPlayer()
    projector = Projector()
    lights = TheaterLights()
    screen = Screen()
    popper = PopcornPopper()

    home_theater = HomeTheaterFacade(amp, tunner, player, projector, lights, screen, popper)
    home_theater.watch_movie('傲慢与偏见')
    print()
    home_theater.end_movie()

"""运行结果：
准备播放电影...
打开爆米花机器
提供爆米花
调暗灯光
放下屏幕
打开投影机
设置投影机为宽屏模式
打开扩音器
设置流媒体输入
设置环绕音响
设置音量为5
打开流媒体播放器
播放傲慢与偏见

停止播放电影
关闭爆米花机器
打开灯光
收起屏幕
关闭投影机
关闭扩音器
停止播放
关闭流媒体播放器
"""
