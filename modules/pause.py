from typing import Callable

import pygame

from modules.events import Event, EventID, events_proxy
from modules.menu import Menu, MenuItem
from modules.state_interface import State


class Pause(State):
    def __init__(self, win_size) -> None:
        self.win_size = win_size
        items = [
            ("resume", lambda: events_proxy.emitte(Event(EventID.RESUME, []))),
            (
                "restart",
                lambda: events_proxy.emitte(Event(EventID.RESTART, [])),
            ),
            ("quit", lambda: events_proxy.emitte(Event(EventID.MENU_STATE, []))),
        ]

        self.menu_size = self.win_size[0] // 3, 134
        self.menu_pos = (
            (self.win_size[0] - self.menu_size[0]) // 2,
            (self.win_size[1] - self.menu_size[1]) // 2,
        )
        self.style = {
            "font fam": None,
            "font size": 32,
            "color": (180, 240, 255),
            "active color": (255, 220, 80),
        }
        self.layout = {"padding": 16, "margin y": 40, "align": "center"}
        self.menu = Menu(
            self.menu_pos,
            self.menu_size,
            "black",
            None,
            items,
            self.style,
            self.layout,
        )
        self.focused = 0
        self.focus_move = 0

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                events_proxy.emitte(Event(EventID.QUIT_GAME, []))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    events_proxy.emitte(Event(EventID.RESUME, []))
            self.menu.handle_input(event)

    def update(self, dt: float) -> None:
        self.menu.update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        self.menu.draw(surface)
