import math
import os

import pygame


class Entity:
    def __init__(
        self, sprite: str, scale: tuple[int, int], pos: tuple[int, int]
    ) -> None:
        self.sprite = pygame.image.load(os.path.join("assets", sprite))
        self.scale = scale
        self.sprite = pygame.transform.scale(self.sprite, self.scale)
        self.box = pygame.Rect(pos, self.scale)
        print(self.box)

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.sprite, self.box.topleft)


class Turret(Entity):
    def __init__(
        self,
        sprite: str,
        scale: tuple[int, int],
        pos: tuple[int, int],
        velocity: int,
        fire_rate: float,
    ) -> None:
        super().__init__(sprite, scale, pos)
        self.velocity = velocity
        self.fire_rate = fire_rate
        self.speed = 0
        self.dt = 0
        self.sprite.set_colorkey((0, 0, 0))

    def update(self, dt: float) -> None:
        self.box.x += math.ceil(self.speed * dt)

    def move(self, left: bool = False) -> None:
        self.speed = -1 * self.velocity if left else self.velocity

    def stop(self) -> None:
        self.speed = 0

    def shoot(self, dt: float) -> None:
        if self.dt == 0:
            self.dt = self.fire_rate
            # shoot
        else:
            self.dt -= dt
