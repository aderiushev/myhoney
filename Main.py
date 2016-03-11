#!/usr/bin/env python
# -*- coding: utf-8 -*-
from HoneyApp import HoneyApp
from kivy.config import Config
from kivy.lang import Builder
from Helper import get_resource
import time

Config.set('graphics', 'width', 640)
Config.set('graphics', 'height', 480)
Config.set('graphics', 'resizable', 0)
Config.set('kivy', 'window_icon', get_resource('data/images/nichosi/02.png'))

Config.write()


Builder.load_string("""
<WelcomeScreen>:
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: "{image_bg}"
    BoxLayout:
        padding: 20
        orientation: 'vertical'
        Image:
            source: "{image_title}"
        Label:
            padding: (20, 20)
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            markup: True
            valign: 'middle'
            text_size: self.size
            text: "[size=19][color=333333][b]Привет, Кися! :)[/b] Давай поиграем в игру. Правила такие: ты должна вспомнить, какая из двух фотографий была раньше. [i]Готова?[i] [b]Поехали![/b][/color][/size]"
        Button:
            markup: True
            text: '[b]Поняла[/b]'
            size_hint: (1, 0.3)
            on_press: root.manager.current = 'main'
            background_color: 2.5, 0.5, 0.9, 1

<MainScreen>:
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: "{image_bg}"

""".format(
        image_bg=get_resource('data/images/system/bg.jpg'),
        image_title=get_resource('data/images/nichosi/08.png'),
))

if __name__ == '__main__':
    microtime_start = int(round(time.time() * 1000))
    app = HoneyApp(microtime_start=microtime_start)
    app.prepare()
    app.run()

