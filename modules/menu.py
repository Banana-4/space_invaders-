import os
from typing import Callable

import pygame

from modules.events import Event, EventID, events_proxy
from modules.menu_item import MenuItem

# STYLE OPTIONS: font family, font size, color, active color
# LAYOUT OPTIONS: padding, margin_y, align: left, center, right


class Menu:
    def __init__(
        self,
        pos: tuple[int, int],
        menu_size: tuple[int, int],
        canvas_clr: str | tuple,
        bg_image: str | None,
        items: list[tuple[str, Callable[[], None]]],
        style: dict,
        layout: dict,
    ) -> None:
        self.pos = pos
        self.canvas = pygame.Surface(menu_size)
        self.canvas_bg = (
            pygame.transform.scale(
                pygame.image.load(os.path.join("assets", bg_image)),
                (self.canvas.get_width(), self.canvas.get_height()),
            )
            if bg_image
            else None
        )
        self.canvas_clr = canvas_clr

        self.style = style
        self.layout = layout
        self.menu_items = self.gen_menu_items(items)
        self.focused = 0
        self.focus_move = 0
        self.menu_items[self.focused].toggle_focus()

    def gen_menu_items(
        self, items: list[tuple[str, Callable[[], None]]]
    ) -> list[MenuItem]:
        menu_items = []
        x = self.layout["padding"]
        y_start = self.layout["padding"]
        y = y_start
        for name, callback in items:
            menu_items.append(
                MenuItem(
                    name,
                    callback,
                    (x, y),
                    self.style["color"],
                    self.style["active color"],
                    self.style["font fam"],
                    self.style["font size"],
                    self.layout["align"],
                )
            )
            y += self.layout["margin y"]
        return menu_items

    def handle_input(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.focus_move = -1
            elif event.key == pygame.K_DOWN:
                self.focus_move = 1
            elif event.key == pygame.K_RETURN:
                self.menu_items[self.focused].exec()

    def update(self, dt: float) -> None:
        self.menu_items[self.focused].toggle_focus()
        self.focused = (self.focused + self.focus_move) % len(self.menu_items)
        self.focus_move = 0
        self.menu_items[self.focused].toggle_focus()

    def draw(self, surface: pygame.Surface) -> None:
        if self.canvas_clr == "transperent":
            self.canvas.fill("black")
            self.canvas.set_colorkey("black")
        else:
            self.canvas.fill(self.canvas_clr)

        if self.canvas_bg:
            self.canvas.blit(self.canvas_bg, (0, 0))
        for item in self.menu_items:
            item.draw(self.canvas)
        surface.blit(self.canvas, self.pos)
