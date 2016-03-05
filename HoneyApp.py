#!/usr/bin/python
# coding=utf-8

from kivy.app import App
import os, hashlib
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from MainScreen import MainScreen
from PIL import Image, ImageFile
import datetime, time


class HoneyApp(App):
    IMAGES_DIRECTORY = 'images/'
    EXIF_PHOTO_DATE = 36867
    success = [
        {'filename': 'nichosi/02.png', 'text': 'Молодец!'},
        {'filename': 'nichosi/08.png', 'text': 'Память как у черепахи!'},
        {'filename': 'nichosi/09.png', 'text': 'Да, это было именно так..'},
        {'filename': 'nichosi/13.png', 'text': 'Следующая будет посложнее :)'},
        {'filename': 'nichosi/14.png', 'text': 'Умничка :*'},
        {'filename': 'nichosi/16.png', 'text': 'Правильно, кисуля :)'},
        {'filename': 'nichosi/29.png', 'text': 'И как ты это вспомнила?..'}
    ]
    error = [
        {'filename': 'nichosi/07.png', 'text': 'Неа..'},
        {'filename': 'nichosi/11.png', 'text': 'Милая, наоборот!'},
        {'filename': 'nichosi/17.png', 'text': 'Ошибочка..'},
        {'filename': 'nichosi/18.png', 'text': 'Солнышко, попробуй ещё разок'},
        {'filename': 'nichosi/21.png', 'text': 'Ты уверена? А вот и нет!'}
    ]
    images = []

    def prepare(self):
        self._get_images()

    def _get_images(self):
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        hash_images = []
        for root, dirs, filenames in os.walk(self.IMAGES_DIRECTORY):
            for filename in filenames:
                try:
                    full_filename = self.IMAGES_DIRECTORY + filename
                    image = Image.open(full_filename, 'r')
                    exif = image._getexif()
                    date = exif[self.EXIF_PHOTO_DATE]
                    timestamp = int(time.mktime(datetime.datetime.strptime(date, "%Y:%m:%d %H:%M:%S").timetuple()))
                    hash_image = hashlib.md5(image.tobytes()).hexdigest()
                    if hash_image in hash_images:
                        print('Removed duplicated File: %s' % full_filename)
                        os.remove(full_filename)
                    else:
                        self.images.append({'filename': full_filename, 'timestamp': timestamp})
                        hash_images.append(hash_image)
                except (OSError, TypeError, KeyError, AttributeError) as e:
                    print(e)
                    print('Removed illegal File: %s' % full_filename)
                    os.remove(full_filename)

        print('There are %i OK images' % len(self.images))

    def build(self):
        sm = ScreenManager()
        ws = WelcomeScreen(name='welcome')
        ms = MainScreen(name='main')

        sm.add_widget(ws)
        sm.add_widget(ms)

        return sm


class WelcomeScreen(Screen):
    pass