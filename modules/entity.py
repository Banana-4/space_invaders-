import os
import random

import pygame

from modules.events import Event, EventID, events_proxy


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
        self.box.y = int(self.pos[1])
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
        if not self.alive:
            self.speed = 0
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
                (self.pos[0] + self.scale[0] // 2 - 10, self.pos[1] - 40),
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
        id: int,
    ) -> None:
        super().__init__(sprite, scale, pos)
        self.speed = speed
        self.fire_chance = fire_chance
        self.hp = 1
        self.change_course = False
        self.next_row = 0
        self.id = id

    def change_direction(self) -> None:
        self.next_row = 3
        self.change_course = not self.change_course
        self.pos[0] = self.box.x
        self.speed[0] *= -1

    def update(self, dt: float) -> None:
        if self.change_course:
            if self.next_row > 0:
                self.pos[1] += self.speed[1] * dt
                self.next_row -= self.speed[1] * dt
            else:
                self.change_course = False
        else:
            self.pos[0] += self.speed[0] * dt
        num = random.random()
        if num <= self.fire_chance:
            events_proxy.emitte(Event(EventID.SHOT_FIRED, [self.id]))

    def hit(self) -> None:
        self.hp -= 1

    def kill(self):
        # add explosion on death
        pass

    def shoot(self):
        prj_speed = 70
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


class Fleet:
    def __init__(
        self,
        fleet_size: tuple[int, int],
        top: int,
        rows: int,
        columns: int,
        speed: list[float],
        fire_chance: float,
    ) -> None:
        self.gap_x = 30
        self.gap_y = 30
        self.top = top
        self.fire_chance = fire_chance
        self.rows = rows
        self.columns = columns
        self.fleet_box = pygame.Rect(0, self.top, fleet_size[0], fleet_size[1])
        self.speed = speed
        self.fleet = []
        self.sprite_scale = (
            (self.fleet_box.width - 2 * self.gap_x - self.gap_x * self.columns)
            // self.columns,
            (self.fleet_box.height - self.gap_y * self.rows - 2 * self.gap_y)
            // self.rows,
        )
        self.create_fleet()

    def create_fleet(self) -> None:
        start_x = self.gap_x
        y = self.gap_y + self.top
        for id in range(self.rows):
            x = start_x
            for _ in range(self.columns):
                self.fleet.append(
                    SpaceShip(
                        "spaceship.jpg",
                        self.sprite_scale,
                        (x, y),
                        self.speed.copy(),
                        self.fire_chance,
                        id,
                    )
                )
                x += self.sprite_scale[0] + self.gap_x
            y += self.sprite_scale[1] + self.gap_y

    def collision(self):
        for ship in self.fleet:
            ship.change_direction()

    def update(self, dt: float) -> None:
        self.fleet = [ship for ship in self.fleet if ship.hp != 0]
        for ship in self.fleet:
            ship.update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        for ship in self.fleet:
            ship.draw(surface)


class Shield:
    def __init__(
        self,
        size: tuple[int, int],
        pos: tuple[float, float],
        color: str | tuple[int, int, int],
    ) -> None:
        self.hp = 1
        self.size = size
        self.pos = pos
        self.color = color
        self.blocks = []
        print("Building shie")
        self.build_shield()

    def build_shield(self):
        def quad_curve(x):
            return ((x - self.pos[0]) ** 2) * 1 / self.size[1] + self.pos[1]

        block_size = (10, 10)
        layers = 3
        for layer in range(layers):
            blocks = []
            for x in range(
                int(self.pos[0]), int(self.pos[0]) + self.size[0] + 10, block_size[0]
            ):
                blocks.append(
                    pygame.Rect(
                        x,
                        quad_curve(x),
                        block_size[0],
                        block_size[1],
                    )
                )
            self.blocks.append(blocks)
        print(self.blocks)

    def draw(self, surface: pygame.Surface) -> None:
        for blocks in self.blocks:
            for block in blocks:
                pygame.draw.rect(surface, self.color, block)
