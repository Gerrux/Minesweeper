class Image:
    def __init__(self, image, x, y, w, h):
        self.position = (x, y, x + w, y + h)
        self.image = image

    def draw(self, surface):
        surface.blit(self.image, self.position)

    def update(self):
        pass
