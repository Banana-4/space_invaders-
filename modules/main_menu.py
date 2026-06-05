import os
from typing import Callable

import pygame

from modules.events import Event, EventID, events_proxy
from modules.menu import Menu
from modules.menu_item import MenuItem
from modules.state_interface import State


class MainMenu(State):
    def __init__(
        self,
        items: list[tuple[str, Callable[[], None]]],
        win_size: tuple[int, int] = (640, 400),
    ):
        self.style = {
            "font fam": None,
            "font size": 32,
            "color": (180, 240, 255),
            "active color": (255, 220, 80),
        }
        self.layout = {"padding": 16, "margin y": 50, "align": "lef"}
        self.win_size = win_size
        self.menu_size = (self.win_size[0] // 3, self.win_size[1] // 3)
        self.menu_pos = (
            self.win_size[0] - self.win_size[0] // 3,
            self.win_size[1] - 500,
        )
        # items list
        items = [
            ("Play", lambda: events_proxy.emitte(Event(EventID.PLAY_STATE, []))),
            (
                "Highscore",
                lambda: events_proxy.emitte(Event(EventID.HIGHSCORE_STATE, [])),
            ),
            ("Quit", lambda: events_proxy.emitte(Event(EventID.QUIT_GAME, []))),
        ]
        self.menu = Menu(
            self.menu_pos,
            self.menu_size,
            "transperent",
            None,
            items,
            self.style,
            self.layout,
        )
        self.bg = pygame.image.load(os.path.join("assets", "banner.png"))
        self.bg = pygame.transform.scale(self.bg, self.win_size)

    def update(self, dt: float) -> None:
        self.menu.update(dt)

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                events_proxy.emitte(Event(EventID.QUIT_GAME, []))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    events_proxy.emitte(Event(EventID.QUIT_GAME, []))
            self.menu.handle_input(event)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill("black")
        surface.blit(self.bg, (0, 0))
        self.menu.draw(surface)
