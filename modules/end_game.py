import pygame

from modules.events import Event, EventID, events_proxy
from modules.menu import Menu
from modules.state_interface import State


class EndGame(State):
    def __init__(self, win_size: tuple[int, int], win: bool) -> None:
        self.win_size = win_size

        self.menu_items = [
            ("play again", lambda: events_proxy.emitte(Event(EventID.RESTART, []))),
            (
                "quit to menu",
                lambda: events_proxy.emitte(Event(EventID.MENU_STATE, [])),
            ),
        ]
        self.menu_size = self.win_size[0] // 3, 200
        self.menu_pos = (
            (self.win_size[0] - self.menu_size[0]),
            (self.win_size[1] - self.menu_size[1]),
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
            self.menu_items,
            self.style,
            self.layout,
        )
        self.font = pygame.font.Font(self.style["font fam"], self.style["font size"])
        msg: str = "Victory" if win else "Defeat"
        self.txt = self.font.render(msg, True, self.style["color"])
        bg: str = "vitory.png" if win else "defeat.png"
        self.bg_sprite = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", bg)), self.win_size
        )

    def update(self, dt: float) -> None:
        self.menu.update(dt)

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                events_proxy.emitte(Event(EventID.QUIT_GAME, []))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    events_proxy.emitte(Event(EventID.MENU_STATE, []))
            self.menu.handle_input(event)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.bg_sprite, (0, 0))
        surface.blit(self.txt, (300, self.win_size[1] // 4))
        self.menu.draw(surface)
