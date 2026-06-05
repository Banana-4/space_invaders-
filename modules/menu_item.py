from typing import Callable

import pygame


class MenuItem:
    def __init__(
        self,
        name: str,
        command: Callable[[], None],
        pos: tuple[int, int] = (0, 0),
        color: str | tuple[int, int, int] = "white",
        foc_color: str | tuple[int, int, int] = "black",
        fam: str | None = "",
        size: int = 16,
        align: str = "left",
    ) -> None:
        self.name = name
        self.command = command
        self.font = pygame.font.Font(fam, size)
        self.color = color
        self.foc_color = foc_color
        self.focus = False
        self.pos = pos
        self.align = align

    def toggle_focus(self) -> None:
        self.focus = not self.focus

    def draw(self, surface: pygame.SurfaceType) -> None:
        ren_txt = self.font.render(
            self.name, True, self.foc_color if self.focus else self.color
        )
        x, y = self.pos
        if self.align == "right":
            x = surface.get_width() - ren_txt.get_width() + x
        elif self.align == "center":
            x = (surface.get_width() - ren_txt.get_width()) // 2
        surface.blit(ren_txt, (x, y))

    def exec(self) -> None:
        self.command()
