#!/usr/bin/python
# coding=utf-8

from kivy.app import App
import os, hashlib
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from MainScreen import MainScreen
from PIL import Image, ImageFile
import datetime, time
import struct
import piexif


class HoneyApp(App):
    IMAGES_DIRECTORY = 'images/'
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

        def get_exif(image):
            return piexif.load(image.info["exif"])

        def rotate(image, filename):
            if "exif" in image.info:
                exif_dict = get_exif(image)

                if piexif.ImageIFD.Orientation in exif_dict["0th"]:
                    orientation = exif_dict["0th"].pop(piexif.ImageIFD.Orientation)
                    exif_bytes = piexif.dump(exif_dict)

                    if orientation == 2:
                        image = image.transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 3:
                        image = image.rotate(180)
                    elif orientation == 4:
                        image = image.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 5:
                        image = image.rotate(-90).transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 6:
                        image = image.rotate(-90)
                    elif orientation == 7:
                        image = image.rotate(90).transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 8:
                        image = image.rotate(90)

                    image.save(filename, exif=exif_bytes)

            return image

        hash_images = []
        for root, dirs, filenames in os.walk(self.IMAGES_DIRECTORY):
            for filename in filenames:
                try:
                    full_filename = self.IMAGES_DIRECTORY + filename
                    image = Image.open(full_filename, 'r')
                    rotate(image, full_filename)
                    exif_dict = get_exif(image)
                    date = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal]
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
                except struct.error as e:
                    pass

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