import os

import pygame

from modules.custom_events import QUIT_GAME
from modules.state_interface import State


class MainMenu(State):
    def __init__(self, win_size: tuple[int, int] = (640, 400)):
        self.marg_y_xl = 70
        self.marg_y = 38
        self.font_sizeXL = 48
        self.font_size = 32
        self.font_fam = None
        self.text_col = (180, 240, 255)
        self.win_size = win_size
        self.title_font = pygame.font.Font(self.font_fam, self.font_sizeXL)
        self.item_font = pygame.font.Font(self.font_fam, self.font_size)
        self.text = ["Space Invaders", "Play", "Highscore", "Quit"]
        self.title = self.title_font.render(self.text[0], True, self.text_col)
        self.items = [
            self.item_font.render(txt, True, self.text_col) for txt in self.text[1:]
        ]
        self.bg = pygame.image.load(os.path.join("assets", "banner.png"))
        self.bg = pygame.transform.scale(self.bg, self.win_size)

    def update(self, dt: float) -> None:
        pass

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.event.post(pygame.event.Event(QUIT_GAME))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT_GAME))

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.bg, (0, 0))
        x: int = self.win_size[0] // 2
        y: int = self.win_size[1] // 3
        surface.blit(
            self.title,
            (
                x - self.title.get_width() // 2,
                y,
            ),
        )
        y = y + self.marg_y_xl
        for i, txt in enumerate(self.items):
            surface.blit(txt, (x - txt.get_width() // 2, y + self.marg_y * i))
