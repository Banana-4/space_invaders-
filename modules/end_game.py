import csv
import os
from datetime import date

import pygame

from modules.events import Event, EventID, events_proxy
from modules.menu import Menu
from modules.state_interface import State


class Save:
    def __init__(self, pos: tuple[int, int], score, font: pygame.Font, color) -> None:
        self.pos = pos
        self.score = score
        self.name: list[str] = []
        self.font = font
        self.label = self.font.render("Name: ", True, color)
        self.file = os.path.join("data", "scores.csv")
        self.date = date.today()
        self.color = color
        self.max = 16

    def handle_input(self, event: pygame.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.write_score()
            if event.key == pygame.K_BACKSPACE:
                if self.name:
                    self.name.pop()
            elif event.unicode.isalnum():
                if len(self.name) < self.max:
                    self.name.append(pygame.key.name(event.key))

    def write_score(self) -> None:
        name = "".join(self.name)
        if not name:
            return
        with open(self.file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, self.score, self.date])
            events_proxy.emitte(Event(EventID.HIGHSCORE_STATE, []))

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.label, self.pos)
        x = self.label.get_width() + self.pos[0]
        for ch in self.name:
            ch = self.font.render(ch, True, self.color)
            surface.blit(ch, (x, self.pos[1]))
            x += ch.get_width()


class EndGame(State):
    def __init__(self, win_size: tuple[int, int], score: int) -> None:
        self.win_size = win_size
        self.score = score
        self.msg = f"Score: {score}"
        self.menu_items = [
            ("Save Score", self.save_score),
            ("play again", lambda: events_proxy.emitte(Event(EventID.PLAY_STATE, []))),
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
        self.txt = self.font.render(self.msg, True, self.style["color"])
        self.bg_sprite = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "bg.png")), self.win_size
        )

        self.get_name = Save(
            (self.win_size[0] // 2, self.win_size[1] // 2),
            self.score,
            self.font,
            self.style["color"],
        )
        self.save = False

    def save_score(self) -> None:
        self.save = True

    def update(self, dt: float) -> None:
        self.menu.update(dt)

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                events_proxy.emitte(Event(EventID.QUIT_GAME, []))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    events_proxy.emitte(Event(EventID.MENU_STATE, []))
            if self.save:
                self.get_name.handle_input(event)
            else:
                self.menu.handle_input(event)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.bg_sprite, (0, 0))
        surface.blit(self.txt, (300, self.win_size[1] // 4))
        if self.save:
            self.get_name.draw(surface)
        else:
            self.menu.draw(surface)
