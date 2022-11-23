import pygame


class Rectangle:
    def __init__(self, x, y, w, h, color):
        self.position = (x, y, w, h)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.position)

    def update(self):
        pass
