from typing import Callable

import pygame
from pygame.constants import QUIT

from modules.events import Event, EventID, events_proxy
from modules.menu_item import MenuItem
from modules.state_interface import State


class Pause(State):
    def __init__(self, win_size) -> None:
        self.win_size = win_size
        self.canvas = pygame.Surface((self.win_size[0] // 3, self.win_size[1] // 3))
        self.font_size = 32
        self.font_fam = None
        self.txt_clr = (180, 240, 255)
        self.act_txt_clr = (255, 220, 80)
        items = [
            ("resume", lambda: events_proxy.emitte(Event(EventID.RESUME, []))),
            (
                "restart",
                lambda: events_proxy.emitte(Event(EventID.RESTART, [])),
            ),
            ("quit", lambda: events_proxy.emitte(Event(EventID.MENU_STATE, []))),
        ]
        self.menu_items = self.gen_menu_items(items)
        self.focused = 0
        self.focus_move = 0
        self.menu_items[self.focused].toggle_focus()

    def gen_menu_items(
        self, items: list[tuple[str, Callable[[], None]]]
    ) -> list[MenuItem]:
        menu_items = []
        x = 16
        y_start = 40
        y = y_start
        for name, callback in items:
            menu_items.append(
                MenuItem(
                    name,
                    callback,
                    (x, y),
                    self.txt_clr,
                    self.act_txt_clr,
                    self.font_fam,
                    self.font_size,
                )
            )
            y += y_start
        return menu_items

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                events_proxy.emitte(Event(EventID.QUIT_GAME, []))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.focus_move = -1
                if event.key == pygame.K_DOWN:
                    self.focus_move = 1
                if event.key == pygame.K_RETURN:
                    self.menu_items[self.focused].exec()

    def update(self, dt: float) -> None:
        self.menu_items[self.focused].toggle_focus()
        self.focused = (self.focused + self.focus_move) % len(self.menu_items)
        self.focus_move = 0
        self.menu_items[self.focused].toggle_focus()

    def draw(self, surface: pygame.Surface) -> None:
        self.canvas.fill("black")
        for item in self.menu_items:
            item.draw(self.canvas)
        surface.blit(
            self.canvas,
            (
                (self.win_size[0] - self.canvas.get_width()) // 2,
                (self.win_size[1] - self.canvas.get_height()) // 2,
            ),
        )
