import os

import pygame


class Topbar:
    def __init__(
        self, bg: str, width: int, font_size: int, color: str | tuple[int, int, int]
    ) -> None:
        self.bg = pygame.image.load(os.path.join("assets", bg))
        self.font_size = font_size
        self.width = width
        self.height = self.font_size * 2
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.font = pygame.font.Font(None, self.font_size)
        self.color = color

    def draw(self, score: int, hp: int, surface: pygame.Surface) -> None:
        surface.blit(self.bg, (0, 0))
        score_txt = self.font.render(str(score), True, self.color)
        hp_txt = self.font.render(str(hp), True, self.color)
        surface.blit(score_txt, (self.width - self.font_size, self.font_size))
        surface.blit(hp_txt, (self.font_size, self.font_size))
