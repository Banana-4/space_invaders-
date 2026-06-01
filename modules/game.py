import pygame

from modules.events import Event, EventID, events_proxy
from modules.main_menu import MainMenu
from modules.play import Play
from modules.state_interface import State


class Game:
    def __init__(self, win_size: tuple[int, int] = (400, 800)) -> None:
        self.win_size = win_size
        pygame.init()
        self.caption: str = "Space Invaders"
        self.win: pygame.Surface = pygame.display.set_mode(self.win_size)
        pygame.display.set_caption(self.caption)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.run = True
        self.fps = 60
        self.state: State = MainMenu([], self.win_size)
        events_proxy.register(
            self,
            [
                EventID.QUIT_GAME,
                EventID.MENU_STATE,
                EventID.PLAY_STATE,
                EventID.HIGHSCHORE_STATE,
            ],
        )

    def main(self) -> None:  # game loop
        dt = 0
        while self.run:
            dt = self.clock.tick(self.fps) / 1000
            self.handle_input()
            self.update(dt)
            self.draw()

    def update(self, dt: float) -> None:
        events_proxy.notify()
        self.state.update(dt)

    def notify(self, event: Event) -> None:
        if event.id == EventID.QUIT_GAME:
            self.run = False
        elif event.id == EventID.PLAY_STATE:
            self.state = Play(self.win_size, self.fps)
        elif event.id == EventID.HIGHSCHORE_STATE:
            pass
        elif event.id == EventID.MENU_STATE:
            self.state = MainMenu([], self.win_size)

    def handle_input(self) -> None:
        self.state.handle_input()

    def draw(self) -> None:
        self.win.fill("black")
        self.state.draw(self.win)
        pygame.display.flip()
