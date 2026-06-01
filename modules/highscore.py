import csv
import os

import pygame

from modules.events import Event, EventID, events_proxy
from modules.state_interface import State


class Highscores(State):
    def __init__(self, win_size) -> None:
        self.win_size = win_size
        self.csv_file = os.path.join("data", "scores")
        self.scores: list[str] = []
        try:
            with open(self.csv_file, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.scores.append(f"{row['name']}  {row['score']}  {row['date']}")
        except FileNotFoundError:
            events_proxy.emitte(Event(EventID.MENU_STATE, []))
        self.font = pygame.font.Font(None, 32)
        self.color = (180, 240, 255)
        self.bg = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "background.png")), self.win_size
        )
        self.rtr_cmd = lambda: events_proxy.emitte(Event(EventID.MENU_STATE, []))
        self.rtr_color = (255, 220, 80)

    def update(self, dt: float) -> None:
        return super().update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.bg, (0, 0))
        y = 50
        x = self.win_size[0] // 2 - 100
        surface.blit(
            self.font.render("Highscores", True, self.color),
            (x, y),
        )
        for score in self.scores:
            y += 50
            text = self.font.render(score, True, self.color)
            surface.blit(text, (x, y))

        surface.blit(
            self.font.render("RETURN", True, self.rtr_color),
            (x, y + y // 2),
        )

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                events_proxy.emitte(Event(EventID.QUIT_GAME, []))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    events_proxy.emitte(Event(EventID.MENU_STATE, []))
                if event.key == pygame.K_RETURN:
                    self.rtr_cmd()
