import os

import pygame

import modules.custom_events
from modules.entity import Turret
from modules.state_interface import State


class Play(State):
    def __init__(self, win_size) -> None:
        self.win_size = win_size
        self.turret = Turret(
            "turret.png",
            (96, 48),
            (self.win_size[0] // 2 - 29, self.win_size[1] - 48),
            60,
            1,
        )
        self.bg = pygame.image.load(os.path.join("assets", "background.png"))
        self.bg = pygame.transform.scale(self.bg, self.win_size)
        self.projectiles = []

    def update(self, dt: float) -> None:
        self.turret.update(dt)
        for p in self.projectiles:
            p.update(dt)

    def handle_input(self) -> int:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return modules.custom_events.QUIT_GAME
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return modules.custom_events.QUIT_GAME

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.turret.move(True)
            if keys[pygame.K_d]:
                self.turret.move(False)
            if not keys[pygame.K_a] and not keys[pygame.K_d]:
                self.turret.stop()
            if keys[pygame.K_SPACE]:
                prj = self.turret.shoot()
                if prj:
                    self.projectiles.append(prj)
        return -1

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.bg, (0, 0))
        self.turret.draw(surface)
        for p in self.projectiles:
            p.draw(surface)

    def collison(self) -> None:
        pass
