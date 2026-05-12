import pygame


class Button:
    def __init__(
        self,
        txt: str,
        font_fam: str,
        fs: int,
        pad: int,
        color: str | tuple[int, int, int],
        focus_color: str | tuple[int, int, int],
    ) -> None:
        self.txt = txt
        self.size = fs
        self.font = pygame.font.Font(font_fam, self.size)
        self.pad = pad
        self.color = color
        self.focus_color = focus_color
        self.text_box = pygame.Rect(
            len(self.txt) * self.size + self.pad, self.size * 2 + self.pad, 0, 0
        )
        self._focus = False

    def update(self, dt: float) -> None:
        pass

    @property
    def focus(self) -> bool:
        return self._focus

    @focus.setter
    def focus(self, active: bool) -> None:
        self._focus = active

    def draw(self, surface: pygame.Surface, pos: tuple[int, int]) -> None:
        render = self.font.render(
            self.txt, True, self.focus_color if self._focus else self.color
        )
        self.text_box.x = pos[0]
        self.text_box.y = pos[1]
        surface.blit(render, self.text_box)
