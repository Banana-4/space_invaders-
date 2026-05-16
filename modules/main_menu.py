import os
from typing import Callable

import pygame

from modules.custom_events import HIGHSCHORE_STATE, PLAY_STATE, QUIT_GAME
from modules.menu_item import MenuItem
from modules.state_interface import State


class MainMenu(State):
    def __init__(
        self,
        items: list[tuple[str, Callable[[], bool]]],
        win_size: tuple[int, int] = (640, 400),
    ):
        self.marg_y_xl = 70
        self.marg_y = 38
        self.font_sizeXL = 48
        self.font_size = 32
        self.font_fam = None
        self.text_col = (180, 240, 255)
        self.active_color = (255, 220, 80)
        self.win_size = win_size
        self.focused = 0
        # test items list
        items = [
            ("Play", lambda: pygame.event.post(pygame.event.Event(PLAY_STATE))),
            (
                "Highscore",
                lambda: pygame.event.post(pygame.event.Event(HIGHSCHORE_STATE)),
            ),
            ("Quit", lambda: pygame.event.post(pygame.event.Event(pygame.QUIT))),
        ]
        self.menu_items = self.gen_menu_items(items)
        self.bg = pygame.image.load(os.path.join("assets", "banner.png"))
        self.bg = pygame.transform.scale(self.bg, self.win_size)

    def update(self, dt: float) -> None:
        self.menu_items[self.focused].toggle_focus()

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.event.post(pygame.event.Event(QUIT_GAME))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT_GAME))
                if event.key == pygame.K_UP:
                    self.focused -= 1
                    if self.focused < 0:
                        self.focused = len(self.menu_items) - 1
                if event.key == pygame.K_DOWN:
                    self.focused += 1
                    if self.focused == len(self.menu_items):
                        self.focused = 0
                if event.key == pygame.K_RETURN:
                    self.menu_items[self.focused].exec()

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.bg, (0, 0))
        for item in self.menu_items:
            item.draw(surface)

    def gen_menu_items(self, items: list[tuple[str, Callable[[], bool]]]):
        x, y = self.win_size[0] - self.win_size[0] // 5, self.win_size[1] // 2
        menu_items = []
        for name, callback in items:
            menu_items.append(
                MenuItem(
                    name,
                    callback,
                    (x, y),
                    self.text_col,
                    self.active_color,
                    self.font_fam,
                    self.font_size,
                )
            )
            y += self.marg_y
            menu_items[0].toggle_focus()
        return menu_items
