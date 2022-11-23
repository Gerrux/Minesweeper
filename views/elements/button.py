import pygame
import pygame.gfxdraw

from assets.colors import *
from .text_object import TextObject


class Button:
    def __init__(self, x, y, w, h, text,
                 on_click=lambda x: None,
                 padding=0,
                 font=None,
                 centralized=True,
                 corner_radius=0):
        self.state = 'normal'
        self.on_click = on_click
        self.bounds = pygame.Rect(x, y, w, h)
        self.corner_radius = corner_radius
        self.centralized = centralized
        self.text = TextObject(x + padding, y + padding, lambda: text, SECONDARY_COLOR, font)

    @property
    def back_color(self):
        return dict(normal=BUTTON_NORMAL_COLOR,
                    hover=BUTTON_HOVER_COLOR,
                    pressed=BUTTON_PRESSED_COLOR)[self.state]

    def draw(self, surface):
        if self.corner_radius == 0:
            pygame.draw.rect(surface, self.back_color, self.bounds)
        else:
            self.draw_rounded_rect(surface, self.bounds, self.back_color, self.corner_radius)
        if self.centralized:
            x = self.bounds.centerx
            try:
                y = self.bounds.y + (self.bounds.h - self.text.bounds[-1]) / 2
            except TypeError:
                y = self.bounds.y + (self.bounds.h - self.text.bounds[-1].h) / 2
            self.text.pos = (x, y)
        self.text.draw(surface, self.centralized)

    @staticmethod
    def draw_rounded_rect(surface, rect, color, corner_radius):
        """
        Draw a rectangle with rounded corners.
        Would prefer this:
            pygame.draw.rect(surface, color, rect, border_radius=corner_radius)
        but this option is not yet supported in my version of pygame so do it ourselves.

        We use anti-aliased circles to make the corners smoother
        """
        if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
            raise ValueError(
                f"Both height (rect.height) and width (rect.width) must be > 2 * corner radius ({corner_radius})")

        # need to use anti aliasing circle drawing routines to smooth the corners
        pygame.gfxdraw.aacircle(surface, rect.left + corner_radius, rect.top + corner_radius, corner_radius, color)
        pygame.gfxdraw.aacircle(surface, rect.right - corner_radius - 1, rect.top + corner_radius, corner_radius, color)
        pygame.gfxdraw.aacircle(surface, rect.left + corner_radius, rect.bottom - corner_radius - 1, corner_radius,
                                color)
        pygame.gfxdraw.aacircle(surface, rect.right - corner_radius - 1, rect.bottom - corner_radius - 1, corner_radius,
                                color)

        pygame.gfxdraw.filled_circle(surface, rect.left + corner_radius, rect.top + corner_radius, corner_radius, color)
        pygame.gfxdraw.filled_circle(surface, rect.right - corner_radius - 1, rect.top + corner_radius, corner_radius,
                                     color)
        pygame.gfxdraw.filled_circle(surface, rect.left + corner_radius, rect.bottom - corner_radius - 1, corner_radius,
                                     color)
        pygame.gfxdraw.filled_circle(surface, rect.right - corner_radius - 1, rect.bottom - corner_radius - 1,
                                     corner_radius, color)

        rect_tmp = pygame.Rect(rect)

        rect_tmp.width -= 2 * corner_radius
        rect_tmp.center = rect.center
        pygame.draw.rect(surface, color, rect_tmp)

        rect_tmp.width = rect.width
        rect_tmp.height -= 2 * corner_radius
        rect_tmp.center = rect.center
        pygame.draw.rect(surface, color, rect_tmp)

    def update(self):
        pass

    def handle_mouse_event(self, type_event, pos, button=None):
        if type_event == pygame.MOUSEMOTION:
            self.handle_mouse_move(pos)
        elif type_event == pygame.MOUSEBUTTONDOWN and button == 1:
            self.handle_mouse_down(pos)
        elif type_event == pygame.MOUSEBUTTONUP and button == 1:
            self.handle_mouse_up()

    def handle_mouse_move(self, pos):
        if self.bounds.collidepoint(pos):
            if self.state != 'pressed':
                self.state = 'hover'
        else:
            self.state = 'normal'

    def handle_mouse_down(self, pos):
        if self.bounds.collidepoint(pos):
            self.state = 'pressed'

    def handle_mouse_up(self):
        if self.state == 'pressed':
            self.on_click(self)
            self.state = 'hover'
