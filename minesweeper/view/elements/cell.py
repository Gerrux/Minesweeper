import os

import pygame

from minesweeper.config import GAME_SPRITES


class Cell:
    def __init__(
        self, bounds, image, on_left_click=lambda x: None, on_right_click=lambda x: None
    ):
        self.bounds = bounds
        self.image = image
        self.state = "normal"
        self.is_pressed = False
        self.is_block = False
        self.on_left_click = on_left_click
        self.on_right_click = on_right_click
        self.normal_image = pygame.transform.scale(
            pygame.image.load(self.get_path_assets(GAME_SPRITES["cell_surf"])),
            (bounds.w, bounds.h),
        )
        self.hover_image = pygame.transform.scale(
            pygame.image.load(self.get_path_assets(GAME_SPRITES["cell_surf_select"])),
            (bounds.w, bounds.h),
        )

    @property
    def back_image(self):
        return dict(
            normal=self.normal_image, hover=self.hover_image, pressed=self.image
        )[self.state]

    @staticmethod
    def get_path_assets(path):
        asset_path = f"{os.path.normpath(os.path.dirname(os.path.abspath(os.path.join(__file__, '../..'))))}\{os.path.normpath(path)}"
        return asset_path

    def draw(self, surface):
        surface.blit(self.back_image, self.bounds)

    def update(self):
        pass

    def handle_mouse_event(self, type_event, pos, button=None):
        if type_event == pygame.MOUSEMOTION:
            self.handle_mouse_move(pos)
        elif type_event == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
        elif type_event == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(button)

    def handle_mouse_move(self, pos):
        if not self.is_pressed:
            if self.bounds.collidepoint(pos):
                if self.state != "pressed":
                    self.state = "hover"
            else:
                self.state = "normal"

    def handle_mouse_down(self, pos):
        if not self.is_pressed:
            if self.bounds.collidepoint(pos):
                self.state = "pressed"

    def handle_mouse_up(self, button):
        if not self.is_pressed:
            if self.state == "pressed":
                if button == 1 and not self.is_block:
                    self.on_left_click(self)
                elif button == 3:
                    self.on_right_click(self)
