from typing import Callable

import pygame


class MenuItem:
    def __init__(
        self,
        option_name: str,
        command: Callable[[], None],
        color: str = "white",
        foc_color: str = "black",
        fam: str = None,
        size: int = 16,
    ) -> None:
        self.option_name = option_name
        self.command = command
        self.font = pygame.font.Font(fam, size)
        self.color = color
        self.foc_color = foc_color
        self.focus = False

    def recive(self, event: pygame.Event) -> None:
        if event.type == FOCUSED_ITEM:
            self.focus = True
        if event.type == SELECT_ITEM:
            self.command()

    def draw(self) -> None:
        pass
