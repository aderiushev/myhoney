## -*- coding: utf-8 -*-

from kivy.app import App
import os, hashlib
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from MainScreen import MainScreen
from PIL import Image, ImageFile
import datetime, time
import struct
import piexif
from Helper import get_resource


class HoneyApp(App):
    title = 'Made in case you are missing me :)'
    icon = get_resource('images/system/icon.png')
    IMAGES_DIRECTORY = get_resource('images/')
    MAX_IMAGE_WIDTH = 300
    success = [
        {'filename': IMAGES_DIRECTORY + 'nichosi/02.png', 'text': 'Молодец!'},
        {'filename': IMAGES_DIRECTORY + 'nichosi/08.png', 'text': 'Память как у черепахи!'},
        {'filename': IMAGES_DIRECTORY + 'nichosi/09.png', 'text': 'Да, это было именно так..'},
        {'filename': IMAGES_DIRECTORY + 'nichosi/13.png', 'text': 'Следующая будет посложнее :)'},
        {'filename': IMAGES_DIRECTORY + 'nichosi/14.png', 'text': 'Умничка :*'},
        {'filename': IMAGES_DIRECTORY + 'nichosi/16.png', 'text': 'Правильно, кисуля :)'},
        {'filename': IMAGES_DIRECTORY + 'nichosi/29.png', 'text': 'И как ты это вспомнила?..'}
    ]
    error = [
        {'filename': IMAGES_DIRECTORY + 'nichosi/07.png', 'text': 'Неа..'},
        {'filename': IMAGES_DIRECTORY + 'nichosi/11.png', 'text': 'Милая, наоборот!'},
        {'filename': IMAGES_DIRECTORY + 'nichosi/17.png', 'text': 'Ошибочка..'},
        {'filename': IMAGES_DIRECTORY + 'nichosi/18.png', 'text': 'Солнышко, попробуй ещё разок'},
        {'filename': IMAGES_DIRECTORY + 'nichosi/21.png', 'text': 'Ты уверена? А вот и нет!'}
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

        def compress(image, filename):
            width, height = image.size
            if width > self.MAX_IMAGE_WIDTH:
                new_height = int(round(height / (width / self.MAX_IMAGE_WIDTH)))
                image.resize((self.MAX_IMAGE_WIDTH, new_height), Image.ANTIALIAS)
            image.save(filename, optimize=True, quality=50)

            return image

        hash_images = []
        for filename in os.listdir(self.IMAGES_DIRECTORY):
            full_filename = self.IMAGES_DIRECTORY + filename
            name, extension = os.path.splitext(full_filename)
            if not os.path.isfile(full_filename):
                continue

            with Image.open(full_filename, 'r') as image:
                try:
                    image = compress(image, full_filename)
                    image = rotate(image, full_filename)
                    exif_dict = get_exif(image)
                    date = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal]
                    timestamp = int(time.mktime(datetime.datetime.strptime(date, "%Y:%m:%d %H:%M:%S").timetuple()))
                    hash_image = hashlib.md5(image.tobytes()).hexdigest()
                    if hash_image in hash_images:
                        print('Removed duplicated File: %s' % full_filename)
                        image.close()
                        os.remove(full_filename)
                    else:
                        new_full_filename = '{images_dir}{hash_image}{extension}'.format(
                            images_dir=self.IMAGES_DIRECTORY,
                            hash_image=hash_image,
                            extension=extension
                        )
                        try:
                            os.rename(full_filename, new_full_filename)
                        except OSError:
                            pass
                        self.images.append({'filename': new_full_filename, 'timestamp': timestamp})
                        hash_images.append(hash_image)
                except (OSError, TypeError, KeyError, AttributeError) as e:
                    print(e)
                    print('Removed illegal File: %s' % full_filename)
                    image.close()
                    os.remove(full_filename)
                except struct.error as e:
                    print(e)
                    pass

        print('There are %i OK images' % len(self.images))
        if len(self.images) < 2:
            raise Exception('Add more images!')

    def build(self):
        sm = ScreenManager()
        ws = WelcomeScreen(name='welcome')
        ms = MainScreen(name='main')

        sm.add_widget(ws)
        sm.add_widget(ms)

        return sm


class WelcomeScreen(Screen):
    pass
