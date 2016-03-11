#!/usr/bin/python
# coding=utf-8

from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
import random, datetime
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior


class ImageButton(ButtonBehavior, Image):
    type = None

    def __init__(self, **kwargs):
        self.type = kwargs.get('type')
        super(ImageButton, self).__init__(**kwargs)
        pass


class MainScreen(Screen):
    IMAGE_TYPE_LEFT = "left"
    IMAGE_TYPE_RIGHT = "right"
    current_images = None
    image1 = None
    image2 = None
    layout = None

    def choose(self, button):
        from HoneyApp import HoneyApp

        def get_date_diff_string():
            timestamp_diff = (datetime.datetime.fromtimestamp(self.current_images[self.IMAGE_TYPE_LEFT]['timestamp']) -
                              datetime.datetime.fromtimestamp(self.current_images[self.IMAGE_TYPE_RIGHT]['timestamp']))
            return str(abs(timestamp_diff.days)) + ' дней'

        if button.type == self.IMAGE_TYPE_LEFT:
            image_chosen_timestamp = self.current_images[self.IMAGE_TYPE_LEFT]['timestamp']
            image_another_timestamp = self.current_images[self.IMAGE_TYPE_RIGHT]['timestamp']
        else:
            image_chosen_timestamp = self.current_images[self.IMAGE_TYPE_RIGHT]['timestamp']
            image_another_timestamp = self.current_images[self.IMAGE_TYPE_LEFT]['timestamp']

        if image_chosen_timestamp < image_another_timestamp:
            status = True
        else:
            status = False

        modal = ModalView(size_hint=(None, None), size=(400, 200))
        if status:
            modal.bind(on_dismiss=self.renew_images)
            modal_data = random.choice(HoneyApp.success)
        else:
            modal_data = random.choice(HoneyApp.error)

        layout = GridLayout(cols=1, rows=2, on_touch_down=modal.dismiss)
        text = '[size=18][b]{text}[/b][/size]\n' \
               '[size=11]Эта фотография была сделана: [b]{image_date_chosen}[/b]\n' \
               'Дата второй фотографии: [b]{image_date_another}[/b]\n' \
               'Разница - [b]{date_diff}[/b][/size]'.\
            format(text=modal_data['text'],
                   image_date_chosen=datetime.datetime.fromtimestamp(image_chosen_timestamp).strftime('%d.%m.%Y %H:%M'),
                   image_date_another=datetime.datetime.fromtimestamp(image_another_timestamp).strftime('%d.%m.%Y %H:%M'),
                   date_diff=get_date_diff_string())

        layout.add_widget(Label(text=text, markup=True))
        layout.add_widget(Image(source=modal_data['filename']))
        modal.add_widget(layout)
        modal.open()

    def on_enter(self):
        self.layout = GridLayout(cols=2, rows=1, spacing=10, padding=10)
        self.renew_images()

    def renew_images(self, modal=None):
        self.clear_widgets()
        self.layout.clear_widgets()
        self.current_images = self.get_random_images()

        if self.image1:
            self.remove_widget(self.image1)
        if self.image2:
            self.remove_widget(self.image2)

        self.image1 = ImageButton(
            source=self.current_images[self.IMAGE_TYPE_LEFT]['filename'],
            type=self.IMAGE_TYPE_LEFT,
            allow_stretch=True
        )
        self.image2 = ImageButton(
            source=self.current_images[self.IMAGE_TYPE_RIGHT]['filename'],
            type=self.IMAGE_TYPE_RIGHT,
        )
        self.image1.bind(on_press=self.choose)
        self.image2.bind(on_press=self.choose)

        self.layout.add_widget(self.image1)
        self.layout.add_widget(self.image2)
        self.add_widget(self.layout)

    def get_random_images(self):
        from HoneyApp import HoneyApp

        while True:
            image_random1 = random.choice(HoneyApp.images)
            image_random2 = random.choice(HoneyApp.images)

            if image_random1['filename'] == image_random2['filename']:
                continue
            else:
                return {self.IMAGE_TYPE_LEFT: image_random1, self.IMAGE_TYPE_RIGHT: image_random2}
