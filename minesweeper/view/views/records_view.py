import json

import pygame

from .view import BaseView
from ..elements.button import Button
from ..elements.image import Image
from ..elements.label import Label
from ..elements.rectangle import Rectangle
from ...assets.colors import PRIMARY_COLOR, SECONDARY_COLOR
from ...config import (
    CAPTION,
    ICON,
    FRAME_RATE,
    FONT,
    FONT_SIZE,
    SOUNDS,
    MENU_BACKGROUND,
)


class RecordsView(BaseView):
    def __init__(self, controller):
        BaseView.__init__(
            self,
            caption=CAPTION,
            width=600,
            height=800,
            background_color=pygame.Color(SECONDARY_COLOR),
            frame_rate=FRAME_RATE,
            icon=pygame.image.load(self.get_path_assets(ICON)),
        )
        self.objects = []
        self.font = pygame.font.Font(self.get_path_assets(FONT), FONT_SIZE)
        self.background_image = Image(
            pygame.image.load(self.get_path_assets(MENU_BACKGROUND)), 0, 0, 600, 800
        )
        self.objects.append(self.background_image)
        self.mouse_handlers = []
        self.sound_effect = pygame.mixer.Sound(self.get_path_assets(SOUNDS["click"]))
        self.controller = controller
        self.controller.set_view(self)
        self.show_record_labels()
        self.create_menu_button()

    def show_record_labels(self):
        background_records = Rectangle(150, 275, 300, 250, pygame.Color(SECONDARY_COLOR), corner_radius=20)
        self.objects.append(background_records)
        src = self.get_path_assets("model/records.json")
        with open(src, "r") as read_file:
            data = json.load(read_file)
        counter = 0
        text_records = []
        for key, value in data.items():
            if value != 0:
                minutes = value / 1000 / 60
                seconds = value / 1000 % 60

                if seconds < 10:
                    seconds_string = "0" + str(int(seconds))
                else:
                    seconds_string = str(int(seconds))

                if minutes < 10:
                    minutes_string = "0" + str(int(minutes))
                else:
                    minutes_string = str(int(minutes))

                timer_string = f"{minutes_string}:{seconds_string}"
            else:
                timer_string = "no record"

            text = f'{key.capitalize()}: {timer_string}'
            record = Label(
                175,
                300 + (30 + 10) * counter,
                text,
                pygame.Color(PRIMARY_COLOR),
                self.font,
                centralized=True
            )
            text_records.append(record)
            counter += 1

        self.objects += text_records[:]

    def create_menu_button(self):
        def on_menu(button):
            self.sound_effect.play()
            self.controller.set_view_state("menu")
            self.view_run = False

        menu_button = Button(
                225,
                450,
                150,
                50,
                "MENU",
                on_menu,
                padding=5,
                font=self.font,
                corner_radius=15,
        )
        self.objects.append(menu_button)
        self.mouse_handlers.append(menu_button.handle_mouse_event)

    def update(self):
        pass