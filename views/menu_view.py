import sys

import pygame

from assets.colors import SECONDARY_COLOR
from .elements.button import Button
from .elements.image import Image
from .view import BaseView
import config as c


class MenuView(BaseView):
    def __init__(self, controller):
        BaseView.__init__(self,
                          caption=c.CAPTION,
                          width=600,
                          height=800,
                          background_color=pygame.Color(SECONDARY_COLOR),
                          frame_rate=c.FRAME_RATE,
                          icon=pygame.image.load(c.ICON))
        self.objects = []
        self.font = pygame.font.Font(c.FONT, c.FONT_SIZE)
        self.background_image = None
        self.mouse_handlers = []
        self.menu_buttons = []
        self.sound_effect = pygame.mixer.Sound(c.SOUNDS["click"])
        self.controller = controller
        self.controller.set_view(self)
        self.create_menu()

    def create_menu(self):
        def start_game():
            self.sound_effect.play()
            self.controller.switch_screen("game")
            self.view_run = False

        def on_play_easy(button):
            self.controller.set_game_mode("easy")
            start_game()

        def on_play_medium(button):
            self.controller.set_game_mode("medium")
            start_game()

        def on_play_hard(button):
            self.controller.set_game_mode("hard")
            start_game()

        def on_quit(button):
            sys.exit()

        self.background_image = Image(pygame.image.load(c.MENU_BACKGROUND), 0, 0, 600, 800)
        self.objects.append(self.background_image)
        for i, (text, click_handler) in enumerate((('EASY', on_play_easy),
                                                   ('MEDIUM', on_play_medium),
                                                   ('HARD', on_play_hard),
                                                   ('QUIT', on_quit))):
            b = Button(225,
                       300 + (50 + 10) * i,
                       150,
                       50,
                       text,
                       click_handler,
                       padding=5,
                       font=self.font,
                       corner_radius=15)
            self.objects.append(b)
            self.menu_buttons.append(b)
            self.mouse_handlers.append(b.handle_mouse_event)

    def update(self):
        pass
