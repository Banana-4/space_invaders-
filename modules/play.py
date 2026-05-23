import os

import pygame

import modules.custom_events
from modules.entity import SpaceShip, Turret
from modules.state_interface import State
from modules.topbar import Topbar


class Play(State):
    def __init__(self, win_size: tuple[int, int], fps: int) -> None:
        self.win_size = win_size
        self.sprite_scale = (96, 48)
        self.sprite_ship_scale = (
            (self.win_size[0] - 20) // 8,
            30,
        )
        print(self.sprite_ship_scale)
        self.turret = Turret(
            "turret.png",
            self.sprite_scale,
            (
                self.win_size[0] // 2 - self.sprite_scale[0] // 2,
                self.win_size[1] - self.sprite_scale[1],
            ),
            60,
            1,
        )
        self.bg = pygame.image.load(os.path.join("assets", "background.png"))
        self.bg = pygame.transform.scale(self.bg, self.win_size)
        self.player_prj = []
        self.alien_prj = []
        self.alien_fleet = []
        self.topbar = Topbar("bg.png", self.win_size[0], 24, "white")
        self.fps = fps
        self.score = 0
        self.create_fleet()

    def create_fleet(self):
        start_x = 10
        y = 10 + self.topbar.height
        for _ in range(5):
            x = start_x
            for _ in range(8):
                self.alien_fleet.append(
                    SpaceShip(
                        "spaceship.jpg",
                        self.sprite_ship_scale,
                        (x, y),
                        [100, 60],
                        0.0005 / self.fps,
                    )
                )
                x += self.sprite_ship_scale[0] + 10
            y += self.sprite_ship_scale[1] + 10

    def update(self, dt: float) -> None:
        self.turret.update(dt)
        for ship in self.alien_fleet:
            ship.update(dt)
        for p in self.player_prj:
            p.update(dt)
        for p in self.alien_prj:
            p.update(dt)
        self.collison()
        self.player_prj = [p for p in self.player_prj if p.alive]
        self.alien_prj = [p for p in self.alien_prj if p.alive]
        self.alien_fleet = [ship for ship in self.alien_fleet if ship.hp != 0]

    def handle_input(self) -> int:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return modules.custom_events.QUIT_GAME
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return modules.custom_events.QUIT_GAME
            if event.type == modules.custom_events.SHOT_FIRED:
                self.alien_prj.append(self.alien_fleet[0].shoot())
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
                self.player_prj.append(prj)

        return -1

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.bg, (0, 0))
        self.turret.draw(surface)
        for ship in self.alien_fleet:
            ship.draw(surface)
        for p in self.player_prj:
            p.draw(surface)
        for p in self.alien_prj:
            p.draw(surface)
        self.topbar.draw(self.score, self.turret.hp, surface)

    def collison(self) -> None:
        border = 1
        prj_hit = 2

        if (
            self.turret.pos[0] < 0
            or self.turret.pos[0] > self.win_size[0] - self.turret.scale[0]
        ):
            self.turret.collision(border)

        for prj in self.alien_prj:
            if not prj.alive:
                continue
            if prj.box.colliderect(self.turret.box):
                self.turret.collision(prj_hit)
                prj.kill()
        for ship in self.alien_fleet:
            if ship.pos[0] < 0 or ship.pos[0] > self.win_size[0] - ship.scale[0]:
                ship.collision(border)
            for prj in self.player_prj:
                if prj.box.colliderect(ship.box):
                    prj.kill()
                    ship.collision(prj_hit)
