from .text_object import TextObject


class Label(TextObject):
    def __init__(self, x, y, text, color, font, centralized):
        super().__init__(x, y, lambda: text, color, font)
        self.text = text
        self.centralized = centralized

    def draw(self, surface, **kwargs):
        text_surface, self.bounds = self.get_surface(self.text)
        if self.centralized:
            pos = (self.pos[0] - self.bounds.width // 2, self.pos[1])
        else:
            pos = self.pos
        surface.blit(text_surface, pos)
