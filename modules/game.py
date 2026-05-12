import pygame

from modules.custom_events import QUIT_GAME
from modules.main_menu import MainMenu
from modules.state_interface import State


class Game:
    def __init__(self, win_size: tuple[int, int] = (640, 400)) -> None:
        if win_size[0] > 0 and win_size[1] > 0:
            self.win_size = win_size
        else:
            self.win_size = (640, 400)
        pygame.init()
        self.caption: str = "Space Invaders"
        self.win: pygame.Surface = pygame.display.set_mode(self.win_size)
        pygame.display.set_caption(self.caption)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.run = True
        self.fps = 60
        self.state: State = MainMenu(self.win_size)

    def main(self) -> None:  # game loop
        dt = 0
        while True:
            dt = self.clock.tick(self.fps)
            if self.run:
                self.handle_input()
                self.update(dt)
                self.draw()
            else:
                break

    def update(self, dt: float) -> None:
        self.state.update(dt)

    def handle_input(self) -> None:
        self.state.handle_input()
        for event in pygame.event.get():
            if event.type == QUIT_GAME:
                self.run = False

    def draw(self) -> None:
        self.win.fill("black")
        self.state.draw(self.win)
        pygame.display.flip()
