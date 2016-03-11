import os, sys
from kivy.core.audio import SoundLoader


def get_resource(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    path = os.path.join(base_path, relative_path)
    return path.replace('\\', '/')


def switch_sound():
    from HoneyApp import HoneyApp
    if not HoneyApp.sound:
        HoneyApp.sound = SoundLoader.load(HoneyApp.SOUND_SETTINGS['source'])
        HoneyApp.sound.volume = HoneyApp.SOUND_SETTINGS['volume']
    else:
        if HoneyApp.sound.state == 'stop':
            HoneyApp.sound.play()
        else:
            HoneyApp.sound.stop()
