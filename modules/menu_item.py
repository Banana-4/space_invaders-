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
    ) -> None:
        self.name = name
        self.command = command
        self.font = pygame.font.Font(fam, size)
        self.color = color
        self.foc_color = foc_color
        self.focus = False
        self.pos = pos

    def toggle_focus(self) -> None:
        self.focus = not self.focus

    def draw(self, surface: pygame.SurfaceType) -> None:
        ren_txt = self.font.render(
            self.name, True, self.foc_color if self.focus else self.color
        )
        surface.blit(ren_txt, (self.pos[0] - ren_txt.get_width(), self.pos[1]))

    def exec(self) -> None:
        self.command()
