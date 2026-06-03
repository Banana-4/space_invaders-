import pygame

from modules.events import Event, EventID, events_proxy
from modules.highscore import Highscores
from modules.main_menu import MainMenu
from modules.pause import Pause
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
        self.active_states = []
        events_proxy.register(
            self,
            [
                EventID.QUIT_GAME,
                EventID.MENU_STATE,
                EventID.PLAY_STATE,
                EventID.HIGHSCORE_STATE,
                EventID.PAUSE_STATE,
                EventID.RESUME,
                EventID.RESTART,
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
        old_state = None
        if event.id == EventID.QUIT_GAME:
            self.run = False
        elif event.id == EventID.PLAY_STATE:
            old_state = self.state
            self.state = Play(self.win_size, self.fps)
        elif event.id == EventID.HIGHSCORE_STATE:
            old_state = self.state
            self.state = Highscores(self.win_size)
        elif event.id == EventID.MENU_STATE:
            old_state = self.state
            self.state = MainMenu([], self.win_size)
        elif event.id == EventID.PAUSE_STATE:
            self.active_states.append(self.state)
            self.state = Pause(self.win_size)
        elif event.id == EventID.RESUME:
            self.state = self.active_states.pop()
        elif event.id == EventID.RESTART:
            old_state = self.active_states.pop()
            self.state = Play(self.win_size, self.fps)
            if old_state:
                events_proxy.unregister(old_state)

    def handle_input(self) -> None:
        self.state.handle_input()

    def draw(self) -> None:
        self.state.draw(self.win)
        pygame.display.flip()
