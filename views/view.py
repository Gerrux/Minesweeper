import sys
import pygame

from collections import defaultdict


class BaseView:
    def __init__(self, caption, width, height, background_color, frame_rate, icon):
        self.frame_rate = frame_rate
        self.view_run = True
        self.objects = []
        pygame.mixer.init(44100, -16, 2, 4096)
        pygame.init()
        pygame.display.set_icon(icon)
        pygame.font.init()
        self.surface = pygame.display.set_mode((width, height))
        self.background_color = background_color
        self.surface.fill(background_color)
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []

    def update(self):
        for o in self.objects:
            o.update()

    def draw(self):
        for o in self.objects:
            o.draw(self.surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                for handler in self.mouse_handlers:
                    if event.type == pygame.MOUSEMOTION:
                        handler(event.type, event.pos)
                    else:
                        handler(event.type, event.pos, event.button)

    def run(self):
        while self.view_run:
            self.surface.fill(self.background_color)

            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frame_rate)
