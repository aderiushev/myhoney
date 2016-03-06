from HoneyApp import HoneyApp
from kivy.config import Config
Config.set('graphics', 'width', 640)
Config.set('graphics', 'height', 480)
Config.set('graphics', 'resizable', 0)
Config.set('kivy', 'window_icon', 'nichosi/02.png')

Config.write()

if __name__ == '__main__':

    app = HoneyApp()
    app.prepare()
    app.run()

