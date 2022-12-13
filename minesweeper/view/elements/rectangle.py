import pygame
import pygame.gfxdraw


class Rectangle:
    def __init__(self, x, y, w, h, color, corner_radius=0):
        self.position = (x, y, w, h)
        self.color = color
        self.corner_radius = corner_radius

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
                f"Both height (rect.height) and width (rect.width) must be > 2 * corner radius ({corner_radius})"
            )

        # need to use anti aliasing circle drawing routines to smooth the corners
        pygame.gfxdraw.aacircle(
            surface,
            rect.left + corner_radius,
            rect.top + corner_radius,
            corner_radius,
            color,
        )
        pygame.gfxdraw.aacircle(
            surface,
            rect.right - corner_radius - 1,
            rect.top + corner_radius,
            corner_radius,
            color,
        )
        pygame.gfxdraw.aacircle(
            surface,
            rect.left + corner_radius,
            rect.bottom - corner_radius - 1,
            corner_radius,
            color,
        )
        pygame.gfxdraw.aacircle(
            surface,
            rect.right - corner_radius - 1,
            rect.bottom - corner_radius - 1,
            corner_radius,
            color,
        )

        pygame.gfxdraw.filled_circle(
            surface,
            rect.left + corner_radius,
            rect.top + corner_radius,
            corner_radius,
            color,
        )
        pygame.gfxdraw.filled_circle(
            surface,
            rect.right - corner_radius - 1,
            rect.top + corner_radius,
            corner_radius,
            color,
        )
        pygame.gfxdraw.filled_circle(
            surface,
            rect.left + corner_radius,
            rect.bottom - corner_radius - 1,
            corner_radius,
            color,
        )
        pygame.gfxdraw.filled_circle(
            surface,
            rect.right - corner_radius - 1,
            rect.bottom - corner_radius - 1,
            corner_radius,
            color,
        )

        rect_tmp = pygame.Rect(rect)

        rect_tmp.width -= 2 * corner_radius
        rect_tmp.center = rect.center
        pygame.draw.rect(surface, color, rect_tmp)

        rect_tmp.width = rect.width
        rect_tmp.height -= 2 * corner_radius
        rect_tmp.center = rect.center
        pygame.draw.rect(surface, color, rect_tmp)

    def draw(self, surface):
        if self.corner_radius == 0:
            pygame.draw.rect(surface, self.color, self.position)
        else:
            self.draw_rounded_rect(surface, pygame.Rect(self.position), self.color, self.corner_radius)

    def update(self):
        pass
