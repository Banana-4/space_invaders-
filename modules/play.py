import os

import pygame

from modules.entity import Fleet, Shield, SpaceShip, Turret
from modules.events import Event, EventID, events_proxy
from modules.state_interface import State
from modules.topbar import Topbar


class Play(State):
    def __init__(self, win_size: tuple[int, int], fps: int) -> None:
        self.win_size = win_size
        self.sprite_scale = (96, 48)
        self.turret = Turret(
            "player.png",
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
        self.topbar = Topbar("bg.png", self.win_size[0], 24, "white")
        self.fps = fps
        self.score = 0
        self.alien_fleet = Fleet(
            (win_size[0], (win_size[1] - self.topbar.height) // 3),
            self.topbar.height,
            5,
            8,
            [40, 40],
            0.1 / self.fps,
        )
        events_proxy.register(self, [EventID.SHOT_FIRED])
        self.shields = [
            Shield("shield.png", (100, 100), (0, 4 * self.win_size[1] // 5)),
            Shield("shield.png", (100, 100), (200, 4 * self.win_size[1] // 5)),
            Shield("shield.png", (100, 100), (400, 4 * self.win_size[1] // 5)),
            Shield("shield.png", (100, 100), (600, 4 * self.win_size[1] // 5)),
        ]

    def clean(self) -> None:
        self.player_prj = [p for p in self.player_prj if p.alive]
        self.alien_prj = [p for p in self.alien_prj if p.alive]
        self.alien_fleet.clean()

    def update(self, dt: float) -> None:
        self.clean()
        self.turret.update(dt)
        self.alien_fleet.update(dt)
        for p in self.player_prj:
            p.update(dt)
        for p in self.alien_prj:
            p.update(dt)
        self.collison(dt)

    def notify(self, event: Event) -> None:
        if event.id == EventID.SHOT_FIRED:
            if event.data[0] == self.turret:
                prj = event.data[0].shoot()
                if prj:
                    self.player_prj.append(prj)
            else:
                self.alien_prj.append(event.data[0].shoot())

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                events_proxy.emitte(Event(EventID.QUIT_GAME, []))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    events_proxy.emitte(Event(EventID.PAUSE_STATE, []))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.turret.move(True)
        if keys[pygame.K_d]:
            self.turret.move(False)
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            self.turret.stop()
        if keys[pygame.K_SPACE]:
            events_proxy.emitte(Event(EventID.SHOT_FIRED, [self.turret]))

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill("black")
        surface.blit(self.bg, (0, 0))
        self.turret.draw(surface)
        for p in self.alien_prj:
            p.draw(surface)
        self.alien_fleet.draw(surface)
        for p in self.player_prj:
            p.draw(surface)
        self.topbar.draw(self.score, self.turret.hp, surface)
        for shield in self.shields:
            shield.draw(surface)

    def collison(self, dt: float) -> None:
        if (
            self.turret.pos[0] < 0
            or self.turret.pos[0] > self.win_size[0] - self.turret.scale[0]
        ):
            events_proxy.emitte(
                Event(
                    EventID.BORDER_COLLISON,
                    [
                        -self.turret.pos[0]
                        if self.turret.pos[0] < 0
                        else -(
                            self.turret.pos[0] - self.win_size[0] + self.turret.scale[0]
                        )
                    ],
                )
            )

        for prj in self.alien_prj:
            if not prj.alive:
                continue
            if prj.box.colliderect(self.turret.box):
                events_proxy.emitte(Event(EventID.HIT, []))
                prj.kill()
            for shield in self.shields:
                if prj.box.colliderect(shield.box):
                    prj.kill()
                    shield.hit()
        collision = False
        for line in self.alien_fleet.fleet:
            for ship in line:
                if ship.pos[1] >= self.win_size[1] - self.win_size[1] // 5:
                    events_proxy.emitte(Event(EventID.LOSE, []))
                    collision = True
                    break
                if ship.pos[0] < 0:
                    events_proxy.emitte(Event(EventID.FLEET_COLLISION, [0]))
                    collision = True
                    break
                if ship.pos[0] > self.win_size[0] - ship.scale[0]:
                    events_proxy.emitte(
                        Event(
                            EventID.FLEET_COLLISION,
                            [self.win_size[0]],
                        )
                    )
                    collision = True
                    break
            if collision:
                break
        for prj in self.player_prj:
            for line in self.alien_fleet.fleet:
                for ship in line:
                    if not prj.alive:
                        continue
                    if prj.box.colliderect(ship.box):
                        prj.kill()
                        ship.hit()
                        self.score += ship.points
            for shield in self.shields:
                if prj.box.colliderect(shield.box):
                    prj.kill()
                    shield.hit()
