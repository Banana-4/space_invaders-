import os

import pygame


class Entity:
    def __init__(
        self, sprite: str, scale: tuple[int, int], pos: tuple[float, float]
    ) -> None:
        self.sprite = pygame.image.load(os.path.join("assets", sprite))
        self.scale = scale
        self.sprite = pygame.transform.scale(self.sprite, self.scale)
        self.pos = [pos[0], pos[1]]
        self.box = pygame.Rect(pos, self.scale)

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        self.box.x = int(self.pos[0])
        surface.blit(self.sprite, self.box)


class Projectile(Entity):
    def __init__(
        self,
        sprite: str,
        scale: tuple[int, int],
        pos: tuple[float, float],
        speed: float,
    ) -> None:
        super().__init__(sprite, scale, pos)
        self.speed = speed
        self.alive = True

    def update(self, dt: float) -> None:
        self.pos[1] += self.speed * dt
        self.box.y = int(self.pos[1])

    def kill(self) -> None:
        self.alive = False


class Turret(Entity):
    def __init__(
        self,
        sprite: str,
        scale: tuple[int, int],
        pos: tuple[int, int],
        velocity: float,
        fire_rate: float,
    ) -> None:
        super().__init__(sprite, scale, pos)
        self.velocity = velocity
        self.fire_rate = fire_rate
        self.speed = 0
        self.p_speed = -2 * self.velocity
        self.cd = 0
        self.hp = 3

    def update(self, dt: float) -> None:
        self.pos[0] += self.speed * dt
        self.cd -= dt

    def move(self, left: bool = False) -> None:
        self.speed = (-1 * self.velocity) if left else self.velocity

    def stop(self) -> None:
        self.speed = 0

    def collision(self, type: int) -> None:
        if type == 1:
            self.pos[0] = self.box.x
        if type == 2:
            self.hp -= 1

    def shoot(self):
        if self.cd <= 0:
            self.cd = self.fire_rate
            return Projectile(
                "ammo.png",
                (20, 40),
                (self.pos[0] + self.scale[0] // 2 - 10, self.pos[1] - 10),
                self.p_speed,
            )


class SpaceShip(Entity):
    def __init__(
        self,
        sprite: str,
        scale: tuple[int, int],
        pos: tuple[float, float],
        speed: list[float],
        fire_chance: float,
    ) -> None:
        super().__init__(sprite, scale, pos)
        self.speed = speed
        self.fire_chance = fire_chance
        self.hp = 1

    def update(self, dt: float) -> None:
        if self.down:
            self.pos[1] += self.scale[1]
            self.speed[0] *= -1
            self.down = False
        else:
            self.pos[0] += self.speed[0] * dt

    def collision(self, type: int) -> None:
        if type == 0:
            self.box.x = int(self.pos[0])
            self.box.y = int(self.pos[1])
        if type == 1:
            self.pos[0] = self.box.x
            self.down = True
        if type == 2:
            self.hp -= 1

    def shoot(self):
        prj_speed = 40
        prj_size = (20, 40)
        return Projectile(
            "ammo.png",
            prj_size,
            (
                self.pos[0] + self.scale[0] // 2 - prj_size[0] // 2,
                self.pos[1] + prj_size[1],
            ),
            prj_speed,
        )
